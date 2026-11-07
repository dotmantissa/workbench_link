"""Private SQLite/spool primitives. Transactions publish effects before acknowledgement."""

import contextlib
import ctypes
import os
import sqlite3
import stat
import threading
import time
import uuid
from pathlib import Path

from .errors import Code, LinkError
from .protocol import canonical, decode, digest

SCHEMA_VERSION = 1
SPOOL_LIMIT = 512 * 1024 * 1024


def private_dir(path: Path) -> Path:
    path = Path(path)
    if not path.is_absolute():
        raise LinkError(Code.STORAGE_UNAVAILABLE, "State directory must be absolute.")
    # Reject symlink components before resolving or opening app state.
    for component in [*reversed(path.parents), path]:
        if component.is_symlink():
            raise LinkError(Code.STORAGE_UNAVAILABLE, "State directories cannot use symlinks.")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
        raise LinkError(Code.STORAGE_UNAVAILABLE, "State directory must be owned by this user with mode 0700.")
    # Linux statfs on the selected directory only. Reject known remote filesystems.
    if os.name == "posix" and hasattr(os, "uname") and os.uname().sysname == "Linux":
        buffer = ctypes.create_string_buffer(256)
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.statfs(os.fsencode(path), buffer) != 0:
            raise LinkError(Code.STORAGE_UNAVAILABLE, "Cannot verify state filesystem.")
        magic = ctypes.c_ulong.from_buffer(buffer).value
        if magic in (0x6969, 0xFF534D42, 0x517B):
            raise LinkError(Code.STORAGE_UNAVAILABLE, "Network filesystems are unsupported for durable state.")
    return path


class Store:
    def __init__(self, root: Path):
        self.root = private_dir(root)
        self.spool = private_dir(root / "spool")
        self.lock = threading.RLock()
        dbpath = root / "ledger.sqlite3"
        if dbpath.is_symlink():
            raise LinkError(Code.STORAGE_UNAVAILABLE, "Ledger cannot be a symlink.")
        fd = os.open(dbpath, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        os.close(fd)
        if stat.S_IMODE(dbpath.stat().st_mode) & 0o077:
            raise LinkError(Code.STORAGE_UNAVAILABLE, "Ledger must be private (0600).")
        self.db = sqlite3.connect(dbpath, isolation_level=None, check_same_thread=False, timeout=2)
        self.db.row_factory = sqlite3.Row
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        if version not in (0, SCHEMA_VERSION):
            self.db.close()
            raise LinkError(Code.UNSUPPORTED_RUNTIME, "Unknown ledger schema; update source without modifying this ledger.")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA synchronous=FULL")
        if self.db.execute("PRAGMA journal_mode=WAL").fetchone()[0] != "wal":
            raise LinkError(Code.STORAGE_UNAVAILABLE, "Ledger filesystem does not support WAL.")
        with self.transaction():
            self.db.execute("CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)")
            self.db.execute("CREATE TABLE IF NOT EXISTS nonces(worker TEXT,nonce TEXT,expires REAL NOT NULL,PRIMARY KEY(worker,nonce))")
            self.db.execute("CREATE TABLE IF NOT EXISTS records(kind TEXT,id TEXT,value BLOB NOT NULL,PRIMARY KEY(kind,id))")
            self.db.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,operation_id TEXT,kind TEXT NOT NULL,metadata BLOB NOT NULL,created REAL NOT NULL)")
            self.db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            self.db.execute("INSERT OR IGNORE INTO meta VALUES('profile_id',?)", (str(uuid.uuid4()),))

    @contextlib.contextmanager
    def transaction(self):
        with self.lock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                yield
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    def consume_nonce(self, worker: str, nonce: str, now: float) -> bool:
        with self.transaction():
            self.db.execute("DELETE FROM nonces WHERE expires<?", (now,))
            if self.db.execute("SELECT COUNT(*) FROM nonces").fetchone()[0] >= 4096:
                return False
            try:
                self.db.execute("INSERT INTO nonces VALUES(?,?,?)", (worker, nonce, now + 120))
            except sqlite3.IntegrityError:
                return False
            return True

    @property
    def profile_id(self):
        with self.lock:
            return self.db.execute("SELECT value FROM meta WHERE key='profile_id'").fetchone()[0]

    def get(self, kind: str, identifier: str):
        with self.lock:
            row = self.db.execute("SELECT value FROM records WHERE kind=? AND id=?", (kind, identifier)).fetchone()
            return decode(row[0]) if row else None

    def put(self, kind: str, identifier: str, value: dict):
        self.db.execute("INSERT INTO records VALUES(?,?,?) ON CONFLICT(kind,id) DO UPDATE SET value=excluded.value",
                        (kind, identifier, canonical(value)))

    def all(self, kind: str):
        with self.lock:
            return [decode(row[0]) for row in self.db.execute("SELECT value FROM records WHERE kind=? ORDER BY id", (kind,))]

    def event(self, identifier: str | None, kind: str, metadata: dict):
        self.db.execute("INSERT INTO events(operation_id,kind,metadata,created) VALUES(?,?,?,?)",
                        (identifier, kind, canonical(metadata), time.time()))

    def publish(self, data: bytes) -> str:
        # Call under writer lock: quota admission and publication are serialized.
        with self.lock:
            name = digest(data)
            dest = self.spool / name
            if dest.exists():
                if self.read(name) != data:
                    raise LinkError(Code.INTEGRITY_FAILURE, "Spool digest conflict.")
                return name
            used = sum(p.stat().st_size for p in self.spool.iterdir() if p.is_file())
            if used + len(data) > SPOOL_LIMIT:
                raise LinkError(Code.OUTPUT_LIMIT, "Private spool quota reached.")
            temporary = self.spool / (str(uuid.uuid4()) + ".tmp")
            try:
                fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(fd, "wb") as f:
                    f.write(data); f.flush(); os.fsync(f.fileno())
                os.replace(temporary, dest)
                fd = os.open(self.spool, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
            except OSError:
                temporary.unlink(missing_ok=True)
                raise LinkError(Code.STORAGE_UNAVAILABLE, "Cannot durably publish private spool.") from None
            return name

    def read(self, name: str) -> bytes:
        if len(name) != 64 or any(c not in "0123456789abcdef" for c in name):
            raise LinkError(Code.INTEGRITY_FAILURE, "Invalid spool reference.")
        try:
            fd = os.open(self.spool / name, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, "rb") as f:
                data = f.read(SPOOL_LIMIT + 1)
        except OSError:
            raise LinkError(Code.INTEGRITY_FAILURE, "Referenced spool is missing or unreadable; commands will not be replayed.") from None
        if digest(data) != name:
            raise LinkError(Code.INTEGRITY_FAILURE, "Spool data failed integrity verification.")
        return data

    def close(self):
        with self.lock:
            self.db.close()
