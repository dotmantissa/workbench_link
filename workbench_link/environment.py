"""Public BaseEnvironment subclass and an owned pipe-backed ProcessHandle."""

import hashlib
import os
import select
import re
import subprocess
import threading
import time

from tools.environments.base import BaseEnvironment

from . import control, protocol as p
from .errors import Code, LinkError
from .ledger import new_id


class LinkProcess:
    def __init__(self, directory, envelope):
        self.directory, self.envelope = directory, envelope
        self.operation_id = envelope['operation_id']
        read_fd, self.write_fd = os.pipe()
        os.set_blocking(self.write_fd, False)
        self.stdout = os.fdopen(read_fd, 'rb', buffering=0)
        self.returncode = None
        self.receipt = None
        self.failure = None
        self.done = threading.Event()
        self.cancel_requested = threading.Event()
        self.thread = threading.Thread(target=self._transfer, daemon=True)
        self.thread.start()

    def _write(self, data):
        position = 0
        deadline = time.monotonic() + 3
        while position < len(data):
            if time.monotonic() >= deadline:
                raise LinkError(Code.OUTPUT_LIMIT, 'Native output pipe stopped draining.', self.operation_id)
            if not select.select([], [self.write_fd], [], .1)[1]:
                continue
            try:
                position += os.write(self.write_fd, data[position:])
            except BlockingIOError:
                continue

    def _transfer(self):
        offset = 0
        digest = hashlib.sha256()
        deadline = time.monotonic() + self.envelope['timeout_seconds'] + 10
        try:
            # Retry delivery only with the immutable operation ID/hash. An ambiguous
            # IPC response never authorizes another operation or local shell fallback.
            try:
                control.request(self.directory, 'submit', envelope=self.envelope)
            except LinkError as exc:
                if exc.code != Code.WORKER_UNAVAILABLE:
                    raise
                control.request(self.directory, 'submit', envelope=self.envelope)
            while time.monotonic() < deadline:
                status = control.request(self.directory, 'operation_status', operation_id=self.operation_id)
                while offset < status['output_bytes']:
                    response = control.request(self.directory, 'read_output', operation_id=self.operation_id, offset=offset)
                    data = p.unb64(response['data_b64'], p.CHUNK_LIMIT)
                    if not data:
                        raise LinkError(Code.INTEGRITY_FAILURE, 'Broker output contains a gap.', self.operation_id)
                    self._write(data); offset += len(data); digest.update(data)
                if status['receipt']:
                    receipt = p.receipt(status['receipt'])
                    if receipt['output_bytes'] != offset or receipt['output_sha256'] != digest.hexdigest():
                        raise LinkError(Code.INTEGRITY_FAILURE, 'Native output failed final receipt verification.', self.operation_id)
                    self.receipt = receipt
                    if not receipt['output_complete']:
                        raise LinkError(Code.OUTPUT_LIMIT, 'Output is incomplete and cannot be used as file data.', self.operation_id)
                    self.returncode = receipt['exit_code'] if receipt['terminal_kind'] == 'completed' else 130
                    return
                if status['state'] in ('UNKNOWN', 'RESOLVED_UNKNOWN'):
                    raise LinkError(Code.OUTCOME_UNKNOWN, 'Command effects are unknown. Reconcile receipts; do not replay the command.', self.operation_id)
                if status['state'] == 'NOT_STARTED':
                    raise LinkError(Code.NOT_STARTED, 'No start grant was issued; this command did not run.', self.operation_id)
                time.sleep(.05)
            raise LinkError(Code.CANCEL_PENDING, 'Termination has not been confirmed within the command deadline.', self.operation_id)
        except (LinkError, OSError) as exc:
            self.failure = exc if isinstance(exc, LinkError) else LinkError(Code.OUTCOME_UNKNOWN, 'Output transport failed; effects may have occurred.', self.operation_id)
            self.returncode = 125
            try:
                control.request(self.directory, 'cancel', operation_id=self.operation_id)
            except LinkError:
                pass
        finally:
            os.close(self.write_fd)
            self.done.set()

    def poll(self):
        return self.returncode if self.done.is_set() else None

    def wait(self, timeout=None):
        if not self.done.wait(timeout):
            raise subprocess.TimeoutExpired('workbench-link', timeout)
        return self.returncode

    def kill(self):
        self.cancel_requested.set()
        try:
            control.request(self.directory, 'cancel', operation_id=self.operation_id)
        except LinkError:
            # The broker's persistent operation gate and independent lease remain.
            pass


class WorkbenchEnvironment(BaseEnvironment):
    is_local = False
    uses_host_filesystem = False
    _stdin_mode = 'payload'
    _passwordless_sudo_probe_supported = False

    def __init__(self, directory, identity, cwd, timeout):
        if not cwd.startswith('/workspace') or (cwd != '/workspace' and not cwd.startswith('/workspace/')):
            raise LinkError(Code.BAD_REQUEST, 'Workbench commands must start under /workspace.')
        p.integer(timeout, 'timeout', 1, p.TIMEOUT_LIMIT)
        self.directory, self.identity = directory, identity
        self.execution_lock = threading.Lock()
        self.execution_slots = threading.BoundedSemaphore(8)
        self.process_lock = threading.Lock()
        self.current_process = None
        self.closed = False
        self.process_identities = {}
        self.termination_target = None
        super().__init__(cwd=cwd, timeout=timeout)
        self.init_session()
        if not self._snapshot_ready:
            raise LinkError(Code.UNSUPPORTED_RUNTIME,
                'Workbench shell snapshot could not be initialized. Inspect status and reconcile uncertain operations.')

    def _run_bash(self, cmd_string, *, login=False, timeout=120, stdin_data=None):
        with self.process_lock:
            if self.closed:
                raise LinkError(Code.BINDING_STALE, 'This native environment is closed.')
            if self.current_process and self.current_process.poll() is None:
                raise LinkError(Code.WORKSPACE_BUSY, 'This environment already has a running operation.')
            obj = {'protocol_version': 1, 'profile_id': self.identity['profile_id'],
                   'binding_id': self.identity['binding_id'], 'generation': self.identity['generation'],
                   'environment_id': self.identity['environment_id'], 'operation_id': new_id(),
                   'worker_id': self.identity['worker_id'], 'worker_instance_id': self.identity['instance_id'],
                   'project_id': self.identity['project_id'], 'script': cmd_string, 'login': login,
                   'lifecycle': 'session',
                   'stdin_b64': p.b64((stdin_data or '').encode('utf-8')), 'timeout_seconds': timeout}
            if self.termination_target:
                obj['terminate_process'] = self.termination_target
            obj['payload_sha256'] = p.payload_hash(obj)
            self.current_process = LinkProcess(self.directory, p.envelope(obj))
            return self.current_process

    def execute(self, command, cwd='', *, timeout=None, stdin_data=None,
                rewrite_compound_background=True, bounded_capture=False, yield_handler=None):
        if not self.execution_slots.acquire(blocking=False):
            raise LinkError(Code.WORKSPACE_BUSY, 'Native request queue is full.')
        if not self.execution_lock.acquire(timeout=30):
            self.execution_slots.release()
            raise LinkError(Code.WORKSPACE_BUSY, 'Workbench environment is busy. Wait for the active operation receipt.')
        try:
            # Hermes's public non-local process contract sends this scalar form
            # for teardown. A shell killing its wrapper alone leaves the job's
            # children alive; route it to identity-checked container tree control.
            match = re.fullmatch(r'kill ([0-9]+) 2>/dev/null', command)
            if not match:
                match = re.fullmatch(r'pkill -TERM -P ([0-9]+) 2>/dev/null; kill \1 2>/dev/null; true', command)
            if match:
                target = self.process_identities.get(int(match[1]))
                if not target:
                    raise LinkError(Code.NOT_STARTED, 'Native teardown PID has no recorded environment identity.')
                self.termination_target = target
            result = super().execute(command, cwd, timeout=timeout, stdin_data=stdin_data,
                rewrite_compound_background=rewrite_compound_background,
                bounded_capture=bounded_capture, yield_handler=yield_handler)
            process = self.current_process
            if process and process.receipt:
                for identity in process.receipt.get('detached_processes', []):
                    self.process_identities.setdefault(identity['pid'], identity)
            result['workbench_link'] = {
                'worker_id': self.identity['worker_id'], 'project_id': self.identity['project_id'],
                'binding_id': self.identity['binding_id'], 'generation': self.identity['generation'],
                'operation_id': process.operation_id if process else None,
                'outcome': process.receipt['terminal_kind'] if process and process.receipt else 'unknown',
                'termination_scope': process.receipt.get('termination_scope', 'environment') if process and process.receipt else None,
                'detached_processes': process.receipt.get('detached_processes', []) if process and process.receipt else [],
                'remote_exit_code': process.receipt['exit_code'] if process and process.receipt else None}
            if process and process.failure:
                raise process.failure
            if process and process.receipt and process.receipt['terminal_kind'] == 'cancelled':
                # The worker stops the container after cancellation. Its /tmp shell
                # snapshot is lost; never reuse this object's old state implicitly.
                self.closed = True
                control.request(self.directory, 'close_environment', environment_id=self.identity['environment_id'])
                result['workbench_link']['shell_state_lost'] = True
                result['output'] = (result.get('output') or '') + '\n[Workbench container stopped; shell state was lost. Start a new session after checking status.]'
            return result
        finally:
            self.termination_target = None
            self.execution_lock.release()
            self.execution_slots.release()

    def cleanup(self):
        if self.closed:
            return
        self.closed = True
        process = self.current_process
        if process and process.poll() is None:
            process.kill()
            process.done.wait(4)
        try:
            response = control.request(self.directory, 'close_environment', environment_id=self.identity['environment_id'])
            deadline = time.monotonic() + 8
            while not response['termination_confirmed'] and time.monotonic() < deadline:
                time.sleep(.1)
                response = control.request(self.directory, 'close_environment', environment_id=self.identity['environment_id'])
        except LinkError:
            pass
        if process and process.done.is_set():
            process.stdout.close()
