"""Immutable settings with no global token cache or implicit configuration reads."""

import ipaddress
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from .errors import Code, LinkError
from .protocol import integer, slug


def key_bytes(value: str) -> bytes:
    # The error must never include the supplied credential.
    if type(value) is not str or not 64 <= len(value) <= 256:
        raise LinkError(Code.AUTH_FAILED, "Supply a hexadecimal worker key of 32–128 bytes.")
    try:
        result = bytes.fromhex(value)
    except ValueError:
        result = b""
    if len(result) * 2 != len(value) or result.hex() != value:
        raise LinkError(Code.AUTH_FAILED, "Supply a canonical lowercase hexadecimal worker key.")
    return result


def broker_url(value: str, local_test: bool = False) -> str:
    try:
        u = urlsplit(value)
        port = u.port
    except ValueError:
        raise LinkError(Code.BAD_REQUEST, "Invalid broker URL.") from None
    if not u.hostname or u.username is not None or u.password is not None or u.query or u.fragment or u.path not in ("", "/"):
        raise LinkError(Code.BAD_REQUEST, "Broker URL must contain only scheme, host and port.")
    loopback = u.hostname == "localhost"
    try:
        loopback = loopback or ipaddress.ip_address(u.hostname).is_loopback
    except ValueError:
        pass
    if u.scheme != "https" and not (u.scheme == "http" and loopback and local_test):
        raise LinkError(Code.AUTH_FAILED, "Verified HTTPS is required; explicit local tests may use literal loopback HTTP.")
    if port is not None and not 1 <= port <= 65535:
        raise LinkError(Code.BAD_REQUEST, "Invalid broker port.")
    return value.rstrip("/")


@dataclass(frozen=True)
class Settings:
    worker_id: str
    project_alias: str
    control_dir: Path
    timeout: int = 120
    memory_mb: int = 512
    cpus: int = 1

    def __post_init__(self):
        slug(self.worker_id)
        slug(self.project_alias, "project_alias")
        integer(self.timeout, "timeout", 1, 600)
        integer(self.memory_mb, "memory_mb", 128, 4096)
        integer(self.cpus, "cpus", 1, 4)
        if not self.control_dir.is_absolute() or len(str(self.control_dir / "control.sock").encode()) > 103:
            raise LinkError(Code.BAD_REQUEST, "Use an absolute private control directory with a shorter Unix socket path.")
