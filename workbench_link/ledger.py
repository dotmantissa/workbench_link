"""Broker transitions. Every grant, cancellation and fence shares one writer lock.

This module has no execution or transport code. A recovered grant is evidence of
possible effects, never permission to replay a command.
"""

import time
import uuid

from . import protocol as p
from .errors import Code, LinkError

TERMINAL = frozenset({'COMPLETED', 'CANCELLED', 'NOT_STARTED', 'RESOLVED_UNKNOWN'})
GRANTED = frozenset({'START_GRANTED', 'RUNNING', 'UNKNOWN'})


def new_id():
    return str(uuid.uuid4())


class Ledger:
    def __init__(self, store):
        self.store = store
        self.db = store.db
        with store.transaction():
            self.db.execute('''CREATE TABLE IF NOT EXISTS registrations(
                instance_id TEXT PRIMARY KEY, worker_id TEXT NOT NULL,
                project_id TEXT NOT NULL, alias TEXT NOT NULL, image TEXT NOT NULL,
                capability_json BLOB NOT NULL)''')
            self.db.execute('''CREATE TABLE IF NOT EXISTS bindings(
                binding_id TEXT PRIMARY KEY, generation INTEGER UNIQUE NOT NULL,
                instance_id TEXT NOT NULL REFERENCES registrations(instance_id),
                state TEXT NOT NULL, fence_reason TEXT)''')
            self.db.execute('''CREATE TABLE IF NOT EXISTS environments(
                environment_id TEXT PRIMARY KEY,
                binding_id TEXT NOT NULL REFERENCES bindings(binding_id),
                state TEXT NOT NULL)''')
            self.db.execute('''CREATE TABLE IF NOT EXISTS operations(
                operation_id TEXT PRIMARY KEY,
                environment_id TEXT NOT NULL REFERENCES environments(environment_id),
                binding_id TEXT NOT NULL REFERENCES bindings(binding_id),
                payload_sha256 TEXT NOT NULL, payload_ref TEXT NOT NULL,
                state TEXT NOT NULL, grant_id TEXT UNIQUE, grant_deadline REAL,
                cancel_requested INTEGER NOT NULL DEFAULT 0,
                output_bytes INTEGER NOT NULL DEFAULT 0, next_sequence INTEGER NOT NULL DEFAULT 0,
                receipt_json BLOB, created REAL NOT NULL, updated REAL NOT NULL)''')
            self.db.execute('''CREATE TABLE IF NOT EXISTS output_chunks(
                operation_id TEXT REFERENCES operations(operation_id), sequence INTEGER,
                byte_offset INTEGER NOT NULL, byte_count INTEGER NOT NULL,
                digest TEXT NOT NULL, spool_ref TEXT NOT NULL,
                PRIMARY KEY(operation_id,sequence))''')

    def _one(self, query, args=()):
        row = self.db.execute(query, args).fetchone()
        return dict(row) if row else None

    def _binding(self, binding_id=None):
        query = '''SELECT b.*,r.worker_id,r.project_id,r.alias,r.image
                   FROM bindings b JOIN registrations r ON b.instance_id=r.instance_id'''
        row = self._one(query + (' WHERE binding_id=?' if binding_id else
                                ' ORDER BY generation DESC LIMIT 1'), (binding_id,) if binding_id else ())
        if row is None:
            raise LinkError(Code.WORKER_UNAVAILABLE, 'No accepted project. Start a worker, then bind its exact identity.')
        return row

    def _active(self, binding_id):
        binding = self._binding(binding_id)
        latest = self._binding()
        if binding['binding_id'] != latest['binding_id'] or binding['state'] == 'CLOSED':
            raise LinkError(Code.BINDING_STALE, 'Binding generation is closed; create a new native environment.')
        if binding['state'] == 'FENCED':
            raise LinkError(Code.OUTCOME_UNKNOWN, 'Project is fenced. Reconcile receipts before executing more commands.')
        return binding

    def _fence(self, binding_id, reason, operation_id=None):
        self.db.execute("UPDATE bindings SET state='FENCED',fence_reason=? WHERE binding_id=?",
                        (reason, binding_id))
        self.store.event(operation_id, 'FENCED', {'binding_id': binding_id, 'reason': reason})

    def _op(self, operation_id):
        p.identifier(operation_id, 'operation_id')
        row = self._one('SELECT * FROM operations WHERE operation_id=?', (operation_id,))
        if row is None:
            raise LinkError(Code.NOT_STARTED, 'Operation is not in this ledger.', operation_id)
        return row

    def _identity(self, op, instance_id, payload_hash):
        binding = self._binding(op['binding_id'])
        if binding['instance_id'] != instance_id:
            raise LinkError(Code.BINDING_STALE, 'Worker instance does not own this operation.', op['operation_id'])
        if op['payload_sha256'] != payload_hash:
            self._fence(op['binding_id'], 'PAYLOAD_CONFLICT', op['operation_id'])
            return False
        return True

    def hello(self, worker_id, instance_id, project_id, alias, image, capabilities):
        p.slug(worker_id); p.identifier(instance_id); p.identifier(project_id); p.slug(alias)
        if type(image) is not str or not image.startswith('sha256:'):
            p.bad('An inspected Docker image ID is required.')
        p.hash_field(image[7:], 'image')
        if type(capabilities) is not dict or len(p.canonical(capabilities)) > 4096:
            p.bad('Invalid worker capabilities.')
        values = (instance_id, worker_id, project_id, alias, image, p.canonical(capabilities))
        with self.store.transaction():
            old = self.db.execute('SELECT * FROM registrations WHERE instance_id=?', (instance_id,)).fetchone()
            if old and tuple(old) != values:
                raise LinkError(Code.BINDING_STALE, 'Worker registration is immutable for this instance.')
            self.db.execute('INSERT OR IGNORE INTO registrations VALUES(?,?,?,?,?,?)', values)
        return {'ok': True, 'instance_id': instance_id}

    def bind(self, instance_id, project_id, image):
        p.identifier(instance_id); p.identifier(project_id)
        with self.store.transaction():
            registration = self._one('SELECT * FROM registrations WHERE instance_id=?', (instance_id,))
            if not registration or registration['project_id'] != project_id or registration['image'] != image:
                raise LinkError(Code.BINDING_STALE, 'Accept the exact registered instance, project and image ID.')
            previous = self._one('SELECT * FROM bindings ORDER BY generation DESC LIMIT 1')
            if previous:
                if previous['instance_id'] == instance_id:
                    return self._binding(previous['binding_id'])
                if previous['state'] == 'FENCED' or self.db.execute(
                        "SELECT 1 FROM environments WHERE binding_id=? AND state='OPEN'", (previous['binding_id'],)).fetchone():
                    raise LinkError(Code.WORKSPACE_BUSY, 'Close and reconcile the previous environment before replacing its binding.')
                self.db.execute("UPDATE bindings SET state='CLOSED' WHERE binding_id=?", (previous['binding_id'],))
            binding_id = new_id()
            generation = previous['generation'] + 1 if previous else 1
            self.db.execute("INSERT INTO bindings VALUES(?,?,?,'ACTIVE',NULL)", (binding_id, generation, instance_id))
            self.store.event(None, 'BOUND', {'binding_id': binding_id, 'generation': generation})
            return self._binding(binding_id)

    def open_environment(self):
        with self.store.transaction():
            binding = self._binding()
            self._active(binding['binding_id'])
            if self.db.execute("SELECT 1 FROM environments WHERE state='OPEN'").fetchone():
                raise LinkError(Code.WORKSPACE_BUSY, 'One native environment is already open for this profile.')
            environment_id = new_id()
            self.db.execute("INSERT INTO environments VALUES(?,?,'OPEN')", (environment_id, binding['binding_id']))
            return dict(binding, profile_id=self.store.profile_id, environment_id=environment_id)

    def submit(self, envelope):
        envelope = p.envelope(envelope)
        conflict = False
        with self.store.transaction():
            existing = self._one('SELECT * FROM operations WHERE operation_id=?', (envelope['operation_id'],))
            if existing:
                if existing['payload_sha256'] != envelope['payload_sha256']:
                    self._fence(existing['binding_id'], 'PAYLOAD_CONFLICT', envelope['operation_id'])
                    conflict = True
                else:
                    return self.operation(envelope['operation_id'])
            else:
                binding = self._active(envelope['binding_id'])
                for name, actual in [('profile_id', self.store.profile_id), ('generation', binding['generation']),
                        ('worker_id', binding['worker_id']), ('worker_instance_id', binding['instance_id']),
                        ('project_id', binding['project_id'])]:
                    if envelope[name] != actual:
                        raise LinkError(Code.BINDING_STALE, 'Execution identity does not match the accepted binding.')
                env = self._one('SELECT * FROM environments WHERE environment_id=?', (envelope['environment_id'],))
                if not env or env['binding_id'] != binding['binding_id'] or env['state'] != 'OPEN':
                    raise LinkError(Code.BINDING_STALE, 'Native environment is closed or belongs to another binding.')
                if self.db.execute("SELECT 1 FROM operations WHERE binding_id=? AND state NOT IN ('COMPLETED','CANCELLED','NOT_STARTED','RESOLVED_UNKNOWN')",
                                   (binding['binding_id'],)).fetchone():
                    raise LinkError(Code.WORKSPACE_BUSY, 'A prior operation is still active or uncertain.')
                ref = self.store.publish(p.canonical(envelope))
                now = time.time()
                self.db.execute('''INSERT INTO operations(operation_id,environment_id,binding_id,
                    payload_sha256,payload_ref,state,created,updated) VALUES(?,?,?,?,?,'QUEUED',?,?)''',
                    (envelope['operation_id'], envelope['environment_id'], binding['binding_id'],
                     envelope['payload_sha256'], ref, now, now))
                self.store.event(envelope['operation_id'], 'QUEUED', {'source': 'native_adapter'})
        if conflict:
            raise LinkError(Code.PAYLOAD_CONFLICT, 'Operation ID was reused with a different payload; project fenced.', envelope['operation_id'])
        return self.operation(envelope['operation_id'])

    def poll(self, instance_id):
        with self.store.lock:
            binding = self._binding()
            if binding['instance_id'] != instance_id:
                return {'ok': True, 'envelope': None, 'binding': None}
            if binding['state'] != 'ACTIVE':
                return {'ok': True, 'envelope': None, 'binding': binding}
            row = self._one("SELECT * FROM operations WHERE binding_id=? AND state='QUEUED' AND cancel_requested=0 ORDER BY created LIMIT 1",
                            (binding['binding_id'],))
            return {'ok': True, 'binding': binding,
                    'envelope': p.envelope(p.decode(self.store.read(row['payload_ref']))) if row else None}

    def accept(self, instance_id, operation_id, payload_hash):
        conflict = False
        with self.store.transaction():
            op = self._op(operation_id)
            if not self._identity(op, instance_id, payload_hash):
                conflict = True
            else:
                self._active(op['binding_id'])
                if op['cancel_requested'] or op['state'] in TERMINAL or op['state'] == 'UNKNOWN':
                    raise LinkError(Code.NOT_STARTED, 'Start grant refused; never launch this operation.', operation_id)
                if op['grant_id']:
                    if time.time() > op['grant_deadline']:
                        self.db.execute("UPDATE operations SET state='UNKNOWN' WHERE operation_id=?", (operation_id,))
                        self._fence(op['binding_id'], 'GRANT_EXPIRED', operation_id)
                    else:
                        return {'ok': True, 'start_grant_id': op['grant_id'], 'launch_seconds': max(0, op['grant_deadline'] - time.time())}
                elif op['state'] == 'QUEUED':
                    grant = new_id()
                    self.db.execute("UPDATE operations SET state='START_GRANTED',grant_id=?,grant_deadline=?,updated=? WHERE operation_id=?",
                                    (grant, time.time() + 5, time.time(), operation_id))
                    self.store.event(operation_id, 'START_GRANTED', {'grant_id': grant})
                    return {'ok': True, 'start_grant_id': grant, 'launch_seconds': 5}
        if conflict:
            raise LinkError(Code.PAYLOAD_CONFLICT, 'Conflicting acceptance; project fenced.', operation_id)
        raise LinkError(Code.OUTCOME_UNKNOWN, 'Start grant expired; reconcile without relaunching.', operation_id)

    def running(self, instance_id, operation_id, payload_hash, grant_id):
        conflict = False
        with self.store.transaction():
            op = self._op(operation_id)
            if not self._identity(op, instance_id, payload_hash):
                conflict = True
            else:
                if op['grant_id'] != grant_id:
                    raise LinkError(Code.BINDING_STALE, 'Runner does not own the start grant.', operation_id)
                if op['state'] == 'START_GRANTED':
                    self.db.execute("UPDATE operations SET state='RUNNING',updated=? WHERE operation_id=?", (time.time(), operation_id))
                    self.store.event(operation_id, 'RUNNING', {})
                return {'ok': True, 'cancel_requested': bool(op['cancel_requested']) or op['state'] == 'UNKNOWN'}
        if conflict:
            raise LinkError(Code.PAYLOAD_CONFLICT, 'Conflicting launch report; project fenced.', operation_id)

    def output(self, instance_id, operation_id, sequence, offset, data, chunk_hash):
        p.integer(sequence, 'sequence'); p.integer(offset, 'offset', 0, p.OUTPUT_LIMIT)
        p.hash_field(chunk_hash)
        if not data or len(data) > p.CHUNK_LIMIT or p.digest(data) != chunk_hash:
            p.bad('Invalid output chunk.')
        error = None
        with self.store.transaction():
            op = self._op(operation_id)
            if self._binding(op['binding_id'])['instance_id'] != instance_id:
                raise LinkError(Code.BINDING_STALE, 'Output belongs to another worker instance.', operation_id)
            if op['grant_id'] is None:
                p.bad('Output requires a committed start grant.')
            old = self._one('SELECT * FROM output_chunks WHERE operation_id=? AND sequence=?', (operation_id, sequence))
            if old:
                if (old['byte_offset'], old['byte_count'], old['digest']) != (offset, len(data), chunk_hash):
                    self._fence(op['binding_id'], 'OUTPUT_CONFLICT', operation_id)
                    error = Code.OUTPUT_CONFLICT
            elif op['state'] in TERMINAL:
                p.bad('Terminal output cannot be extended.')
            elif sequence != op['next_sequence'] or offset != op['output_bytes']:
                raise LinkError(Code.BAD_REQUEST, f"Output gap; expected sequence {op['next_sequence']} at byte {op['output_bytes']}.", operation_id)
            elif offset + len(data) > p.OUTPUT_LIMIT:
                self._fence(op['binding_id'], 'OUTPUT_LIMIT', operation_id)
                error = Code.OUTPUT_LIMIT
            else:
                ref = self.store.publish(data)
                self.db.execute('INSERT INTO output_chunks VALUES(?,?,?,?,?,?)', (operation_id, sequence, offset, len(data), chunk_hash, ref))
                self.db.execute('UPDATE operations SET output_bytes=?,next_sequence=? WHERE operation_id=?', (offset + len(data), sequence + 1, operation_id))
        if error:
            raise LinkError(error, 'Unusable output; cancel and reconcile the operation.', operation_id)
        return {'ok': True, 'next_sequence': sequence + 1, 'next_offset': offset + len(data)}

    def result(self, instance_id, receipt):
        receipt = p.receipt(receipt)
        error = None
        with self.store.transaction():
            op = self._op(receipt['operation_id'])
            if not self._identity(op, instance_id, receipt['payload_sha256']):
                error = Code.PAYLOAD_CONFLICT
            else:
                binding = self._binding(op['binding_id'])
                if (receipt['binding_id'], receipt['generation'], receipt['worker_instance_id'], receipt['start_grant_id']) != (
                        op['binding_id'], binding['generation'], instance_id, op['grant_id']):
                    raise LinkError(Code.BINDING_STALE, 'Receipt does not match the original grant.', op['operation_id'])
                encoded = p.canonical(receipt)
                if op['receipt_json']:
                    if bytes(op['receipt_json']) == encoded:
                        return {'ok': True, 'acknowledged': True}
                    error = Code.INTEGRITY_FAILURE
                elif receipt['output_bytes'] != op['output_bytes'] or receipt['last_sequence'] != op['next_sequence'] - 1:
                    raise LinkError(Code.BAD_REQUEST, 'Upload all contiguous output before its receipt.', op['operation_id'])
                else:
                    try:
                        if p.digest(self._read_output(op['operation_id'], maximum=p.OUTPUT_LIMIT)) != receipt['output_sha256']:
                            error = Code.INTEGRITY_FAILURE
                    except LinkError:
                        error = Code.INTEGRITY_FAILURE
                if error is None:
                    state = {'completed': 'COMPLETED', 'cancelled': 'CANCELLED', 'not_started': 'NOT_STARTED'}[receipt['terminal_kind']]
                    self.db.execute('UPDATE operations SET state=?,receipt_json=?,updated=? WHERE operation_id=?',
                                    (state, encoded, time.time(), op['operation_id']))
                    self.store.event(op['operation_id'], state, {'exit_code': receipt['exit_code']})
                    if not receipt['output_complete']:
                        self._fence(op['binding_id'], 'INCOMPLETE_OUTPUT', op['operation_id'])
            if error:
                self._fence(op['binding_id'], str(error), op['operation_id'])
        if error:
            raise LinkError(error, 'Receipt conflict or integrity failure; project fenced.', receipt['operation_id'])
        return {'ok': True, 'acknowledged': True}

    def _read_output(self, operation_id, offset=0, maximum=p.CHUNK_LIMIT):
        p.integer(offset, 'offset', 0, p.OUTPUT_LIMIT); p.integer(maximum, 'maximum', 1, p.OUTPUT_LIMIT)
        with self.store.lock:
            self._op(operation_id)
            rows = self.db.execute('SELECT * FROM output_chunks WHERE operation_id=? ORDER BY sequence', (operation_id,)).fetchall()
            result = bytearray()
            expected = 0
            for sequence, row in enumerate(rows):
                if row['sequence'] != sequence or row['byte_offset'] != expected:
                    raise LinkError(Code.INTEGRITY_FAILURE, 'Stored output is not contiguous.', operation_id)
                data = self.store.read(row['spool_ref'])
                if len(data) != row['byte_count'] or p.digest(data) != row['digest']:
                    raise LinkError(Code.INTEGRITY_FAILURE, 'Stored output failed verification.', operation_id)
                expected += len(data)
                result.extend(data)
            return bytes(result[offset:offset + maximum])

    def read_output(self, operation_id, offset=0, maximum=p.CHUNK_LIMIT):
        error = None
        with self.store.transaction():
            try:
                result = self._read_output(operation_id, offset, maximum)
            except LinkError as exc:
                if exc.code != Code.INTEGRITY_FAILURE:
                    raise
                self._fence(self._op(operation_id)['binding_id'], 'INTEGRITY_FAILURE', operation_id)
                error = exc
        if error:
            raise error
        return result

    def operation(self, operation_id):
        with self.store.lock:
            op = self._op(operation_id)
            return {'ok': True, 'operation_id': operation_id, 'state': op['state'],
                    'cancel_requested': bool(op['cancel_requested']), 'output_bytes': op['output_bytes'],
                    'receipt': p.decode(op['receipt_json']) if op['receipt_json'] else None}

    def cancel(self, operation_id):
        with self.store.transaction():
            op = self._op(operation_id)
            if op['state'] not in TERMINAL:
                self.db.execute('UPDATE operations SET cancel_requested=1,updated=? WHERE operation_id=?', (time.time(), operation_id))
                if op['grant_id'] is None:
                    self.db.execute("UPDATE operations SET state='NOT_STARTED' WHERE operation_id=?", (operation_id,))
                else:
                    self._fence(op['binding_id'], 'CANCEL_PENDING', operation_id)
                self.store.event(operation_id, 'CANCEL_REQUESTED', {'had_grant': op['grant_id'] is not None})
        return self.operation(operation_id)

    def recover_startup(self):
        with self.store.transaction():
            for row in self.db.execute("SELECT * FROM operations WHERE state NOT IN ('COMPLETED','CANCELLED','NOT_STARTED','RESOLVED_UNKNOWN')").fetchall():
                state = 'UNKNOWN' if row['grant_id'] else 'NOT_STARTED'
                self.db.execute('UPDATE operations SET state=?,cancel_requested=1 WHERE operation_id=?', (state, row['operation_id']))
                if row['grant_id']:
                    self._fence(row['binding_id'], 'BROKER_RESTART', row['operation_id'])
                self.store.event(row['operation_id'], 'RECOVERED_' + state, {})
            # A dead adapter cannot retain an environment lock after restart.
            self.db.execute("UPDATE environments SET state='CLOSED'")

    def disconnect(self, instance_id):
        with self.store.transaction():
            for row in self.db.execute("SELECT o.* FROM operations o JOIN bindings b ON o.binding_id=b.binding_id WHERE b.instance_id=? AND o.state IN ('START_GRANTED','RUNNING')", (instance_id,)).fetchall():
                self.db.execute("UPDATE operations SET state='UNKNOWN',cancel_requested=1 WHERE operation_id=?", (row['operation_id'],))
                self._fence(row['binding_id'], 'LEASE_EXPIRED', row['operation_id'])

    def close_environment(self, environment_id):
        p.identifier(environment_id)
        with self.store.transaction():
            active = self.db.execute("SELECT operation_id FROM operations WHERE environment_id=? AND state NOT IN ('COMPLETED','CANCELLED','NOT_STARTED','RESOLVED_UNKNOWN')", (environment_id,)).fetchall()
        for row in active:
            self.cancel(row['operation_id'])
        with self.store.transaction():
            self.db.execute("UPDATE environments SET state='CLOSED' WHERE environment_id=?", (environment_id,))
        return {'ok': True}

    def status(self):
        with self.store.lock:
            registrations = [dict(row) for row in self.db.execute('SELECT instance_id,worker_id,project_id,alias,image FROM registrations')]
            latest = self._one('SELECT binding_id FROM bindings ORDER BY generation DESC LIMIT 1')
            return {'ok': True, 'profile_id': self.store.profile_id, 'registrations': registrations,
                    'binding': self._binding(latest['binding_id']) if latest else None,
                    'operations': [self.operation(row[0]) for row in self.db.execute('SELECT operation_id FROM operations ORDER BY created DESC LIMIT 20')]}
