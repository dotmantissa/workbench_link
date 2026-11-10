"""Standalone selected-project worker. Only outbound authenticated broker calls."""

import argparse
import fcntl
import getpass
import json
import os
import queue
import shutil
import signal
import subprocess
import threading
import time
from pathlib import Path

from . import protocol as p
from .errors import Code, LinkError
from .ledger import new_id
from .settings import key_bytes
from .store import Store
from .transport import WorkerClient


def selected_project(value):
    path = Path(value)
    if not path.is_absolute():
        p.bad('Select an absolute project directory.')
    resolved = path.resolve(strict=True)
    if resolved in (Path('/'), Path.home()) or not resolved.is_dir():
        p.bad('Select a dedicated project, not a filesystem or home root.')
    if any(c in str(resolved) for c in ',\n\r\x00'):
        p.bad('Project path contains an unsupported Docker mount separator.')
    if not os.access(resolved, os.R_OK | os.W_OK | os.X_OK) or resolved.stat().st_uid != os.getuid():
        p.bad('Selected project must be readable, writable and owned by this worker user.')
    return resolved


class DockerRunner:
    def __init__(self, docker, image, project, instance, binding, environment, *, memory_mb=512, cpus=1):
        self.docker = docker
        self.name = 'workbench-link-' + environment
        self.lock = threading.Lock()
        self.events = queue.Queue(maxsize=128)
        self.stopped = False
        self.stop_confirmed = False
        argv = [docker, 'run', '--name', self.name, '--interactive', '--network', 'none',
                '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                '--user', f'{os.getuid()}:{os.getgid()}', '--pids-limit', '128',
                '--memory', f'{memory_mb}m', '--cpus', str(cpus),
                '--tmpfs', f'/tmp:rw,nosuid,nodev,size=128m,mode=1777',
                '--mount', f'type=bind,source={project},target=/workspace',
                '--label', 'workbench-link=true', '--label', f'workbench-link.owner={os.getuid()}',
                '--label', f'workbench-link.instance={instance}', '--label', f'workbench-link.binding={binding}',
                '--label', f'workbench-link.environment={environment}', image]
        self.process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL, bufsize=0)
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        try:
            ready = self.events.get(timeout=5)
            if ready.get('kind') != 'ready' or ready.get('cwd') != '/workspace':
                raise LinkError(Code.UNSUPPORTED_RUNTIME, 'Worker image did not pass runner startup.')
        except (queue.Empty, LinkError):
            self.close()
            raise LinkError(Code.UNSUPPORTED_RUNTIME, 'Worker image did not become ready; inspect the pinned image and selected mount.') from None

    def _read(self):
        try:
            while raw := self.process.stdout.readline(p.WIRE_LIMIT + 2):
                if not raw.endswith(b'\n') or len(raw) > p.WIRE_LIMIT + 1:
                    raise ValueError
                self.events.put(p.decode(raw[:-1]), timeout=2)
        except (OSError, ValueError, LinkError, queue.Full):
            pass
        finally:
            try:
                self.events.put({'kind': 'unknown'}, timeout=.2)
            except queue.Full:
                pass

    def send(self, obj):
        data = p.canonical(obj) + b'\n'
        with self.lock:
            if self.stopped:
                raise LinkError(Code.WORKER_UNAVAILABLE, 'Runner control is closed.')
            # A bounded pipe write: a stopped/unresponsive runner must not block heartbeat forever.
            import select
            fd = self.process.stdin.fileno()
            os.set_blocking(fd, False)
            deadline = time.monotonic() + 2
            offset = 0
            while offset < len(data):
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not select.select([], [fd], [], remaining)[1]:
                    raise LinkError(Code.WORKER_UNAVAILABLE, 'Runner control deadline exceeded.')
                try:
                    offset += os.write(fd, data[offset:offset + 65536])
                except BlockingIOError:
                    continue

    def close(self):
        with self.lock:
            if self.stopped:
                return self.stop_confirmed
            self.stopped = True
            try:
                self.process.stdin.close()
            except OSError:
                pass
        try:
            subprocess.run([self.docker, 'stop', '--time', '2', self.name],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5, check=False)
            stopped = subprocess.run([self.docker, 'inspect', '--format', '{{.State.Running}}', self.name],
                                     capture_output=True, timeout=3, check=False)
            confirmed = stopped.returncode == 0 and stopped.stdout.strip() == b'false'
            self.stop_confirmed = confirmed
            if confirmed:
                subprocess.run([self.docker, 'rm', self.name], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=3, check=False)
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill(); self.process.wait(timeout=1)
            self.reader.join(1)
            self.process.stdout.close()
            return confirmed
        except (OSError, subprocess.TimeoutExpired):
            return False


class Worker:
    def __init__(self, url, worker_id, project, image, state_dir, key, *, alias='project', local_test=False,
                 ca_file=None, memory_mb=512, cpus=1):
        self.project = selected_project(project)
        p.slug(worker_id); p.slug(alias)
        self.docker = shutil.which('docker')
        if not self.docker:
            raise LinkError(Code.UNSUPPORTED_RUNTIME, 'Docker is required on the project worker.')
        if not image.startswith('sha256:'):
            p.bad('Supply an inspected immutable Docker image ID, not a mutable tag.')
        p.hash_field(image[7:], 'image')
        p.integer(memory_mb, 'memory_mb', 128, 4096); p.integer(cpus, 'cpus', 1, 4)
        inspected = subprocess.run([self.docker, 'image', 'inspect', '--format', '{{.Id}}', image],
                                   capture_output=True, timeout=5, check=False)
        if inspected.returncode or inspected.stdout.decode().strip() != image:
            raise LinkError(Code.UNSUPPORTED_RUNTIME, 'The pinned worker image is not installed locally.')
        self.image, self.alias, self.memory_mb, self.cpus = image, alias, memory_mb, cpus
        self.store = Store(Path(state_dir))
        self.lock_fd = os.open(self.store.root / 'worker.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(self.lock_fd); self.store.close()
            raise LinkError(Code.WORKSPACE_BUSY, 'Another worker owns this state directory.') from None
        self.instance = new_id()
        registration = self.store.get('project', 'selected')
        if registration and registration['root'] != str(self.project):
            os.close(self.lock_fd)
            self.store.close()
            raise LinkError(Code.BINDING_STALE, 'Worker state belongs to a different selected root; use separate state.')
        self.project_id = registration['project_id'] if registration else new_id()
        with self.store.transaction():
            self.store.put('project', 'selected', {'root': str(self.project), 'project_id': self.project_id})
        self.client = WorkerClient(url, worker_id, self.instance, key, local_test=local_test, ca_file=ca_file)
        self.stop_event = threading.Event()
        self.binding = None
        self.runner = None
        self.active_operation = None
        self.last_lease = time.monotonic()
        self.heartbeat_thread = None

    def _cleanup_previous(self):
        # Inventory exactly our previously recorded container names, never unrelated containers.
        for record in self.store.all('container'):
            name = record['name']
            inspected = subprocess.run([self.docker, 'inspect', '--format',
                '{{index .Config.Labels "workbench-link.instance"}} {{index .Config.Labels "workbench-link.owner"}}', name],
                capture_output=True, timeout=3, check=False)
            if inspected.returncode:
                continue
            if inspected.stdout.decode().strip() != f"{record['instance']} {os.getuid()}":
                raise LinkError(Code.BINDING_STALE, 'Recorded container ownership is ambiguous; refusing automatic cleanup.')
            stopped = subprocess.run([self.docker, 'stop', '--time', '2', name], capture_output=True, timeout=5, check=False)
            if stopped.returncode:
                raise LinkError(Code.OUTCOME_UNKNOWN, 'A previous worker container could not be stopped.')
            subprocess.run([self.docker, 'rm', name], capture_output=True, timeout=3, check=False)
        for record in self.store.all('operation'):
            if record['state'] not in ('TERMINAL', 'ACKNOWLEDGED', 'NOT_STARTED'):
                with self.store.transaction():
                    self.store.put('operation', record['envelope']['operation_id'], dict(record, state='UNKNOWN'))

    def _heartbeats(self):
        while not self.stop_event.wait(.5):
            try:
                binding = self.binding
                response = self.client.post('heartbeat', {
                    'binding_id': binding['binding_id'] if binding else None,
                    'generation': binding['generation'] if binding else None,
                    'active_operation_id': self.active_operation})
                self.last_lease = time.monotonic()
                runner = self.runner
                if runner:
                    runner.send({'action': 'cancel' if response['cancel_requested'] else 'renew'})
            except (LinkError, OSError):
                if time.monotonic() - self.last_lease >= 15:
                    if self.runner:
                        self.runner.close()
                    self.stop_event.set()

    def _post_outputs_receipt(self, record):
        envelope = record['envelope']
        original = WorkerClient(self.client.url.geturl(), self.client.worker_id,
                                envelope['worker_instance_id'], self.client.key,
                                local_test=self.client.url.scheme == 'http')
        original.context = self.client.context
        for chunk in record.get('chunks', []):
            original.post('output', {**{name: value for name, value in chunk.items() if name != 'spool_ref'},
                                     'data_b64': p.b64(self.store.read(chunk['spool_ref']))})
        if record.get('receipt'):
            original.post('result', record['receipt'])
            with self.store.transaction():
                self.store.put('operation', envelope['operation_id'], dict(record, state='ACKNOWLEDGED'))

    def execute(self, envelope):
        envelope = p.envelope(envelope)
        operation_id = envelope['operation_id']
        record = self.store.get('operation', operation_id)
        if record:
            if record['envelope']['payload_sha256'] != envelope['payload_sha256']:
                raise LinkError(Code.PAYLOAD_CONFLICT, 'Duplicate operation payload conflict.', operation_id)
            if record['state'] in ('TERMINAL', 'ACKNOWLEDGED'):
                self._post_outputs_receipt(record)
            # No replay for LAUNCHING, RUNNING or UNKNOWN.
            return
        record = {'envelope': envelope, 'state': 'ACCEPTED', 'chunks': []}
        with self.store.transaction():
            self.store.put('operation', operation_id, record)
        if not self.runner or self.runner.name != 'workbench-link-' + envelope['environment_id']:
            if self.runner and not self.runner.close():
                raise LinkError(Code.OUTCOME_UNKNOWN, 'Old environment could not be stopped.')
            name = 'workbench-link-' + envelope['environment_id']
            with self.store.transaction():
                self.store.put('container', envelope['environment_id'], {'name': name, 'instance': self.instance})
            self.runner = DockerRunner(self.docker, self.image, self.project, self.instance,
                envelope['binding_id'], envelope['environment_id'], memory_mb=self.memory_mb, cpus=self.cpus)
        self.active_operation = operation_id
        try:
            grant_requested = time.monotonic()
            grant = self.client.post('accept', {'operation_id': operation_id, 'payload_sha256': envelope['payload_sha256']})
            record.update(state='GRANTED', grant=grant['start_grant_id'])
            with self.store.transaction():
                self.store.put('operation', operation_id, record)
            record['state'] = 'LAUNCHING'
            with self.store.transaction():
                self.store.put('operation', operation_id, record)
            if time.monotonic() - grant_requested >= grant['launch_seconds']:
                raise LinkError(Code.OUTCOME_UNKNOWN, 'Start grant expired before launch; do not replay.', operation_id)
            self.runner.send({'action': 'execute', 'envelope': envelope, 'start_grant_id': grant['start_grant_id']})
            while not self.stop_event.is_set():
                try:
                    event = self.runner.events.get(timeout=.2)
                except queue.Empty:
                    continue
                if event['kind'] == 'running':
                    record['state'] = 'RUNNING'
                    with self.store.transaction():
                        self.store.put('operation', operation_id, record)
                    self.client.post('running', {'operation_id': operation_id, 'payload_sha256': envelope['payload_sha256'],
                                                'start_grant_id': grant['start_grant_id']})
                elif event['kind'] == 'output':
                    data = p.unb64(event['data_b64'], p.CHUNK_LIMIT)
                    ref = self.store.publish(data)
                    chunk = {name: event[name] for name in ('operation_id', 'sequence', 'offset', 'sha256')}
                    chunk['spool_ref'] = ref
                    record['chunks'].append(chunk)
                    with self.store.transaction():
                        self.store.put('operation', operation_id, record)
                    self.client.post('output', {name: value for name, value in event.items() if name != 'kind'})
                elif event['kind'] == 'result':
                    record.update(state='TERMINAL', receipt=p.receipt(event['receipt']))
                    with self.store.transaction():
                        self.store.put('operation', operation_id, record)
                    self._post_outputs_receipt(record)
                    if event['receipt']['terminal_kind'] == 'cancelled':
                        self.runner.close(); self.runner = None
                    return
                else:
                    raise LinkError(Code.OUTCOME_UNKNOWN, 'Runner stopped without a verified receipt.', operation_id)
        except (LinkError, OSError):
            if record['state'] not in ('TERMINAL', 'ACKNOWLEDGED'):
                record['state'] = 'UNKNOWN' if record.get('grant') else 'ACCEPTED'
                with self.store.transaction():
                    self.store.put('operation', operation_id, record)
            if self.runner:
                self.runner.close(); self.runner = None
            raise
        finally:
            self.active_operation = None

    def run(self):
        self._cleanup_previous()
        # Receipt-first recovery uses the historical signed instance identity.
        for record in self.store.all('operation'):
            if record['state'] == 'TERMINAL':
                self._post_outputs_receipt(record)
        self.client.post('hello', {'protocol_version': 1, 'project_id': self.project_id,
            'alias': self.alias, 'image': self.image, 'capabilities': {
                'bash': True, 'python': True, 'ripgrep': True, 'memory_mb': self.memory_mb, 'cpus': self.cpus}})
        print(json.dumps({'worker_id': self.client.worker_id, 'instance_id': self.instance,
                          'project_id': self.project_id, 'image': self.image,
                          'selected_mount': str(self.project) + ' → /workspace (writable)'}), flush=True)
        self.heartbeat_thread = threading.Thread(target=self._heartbeats, daemon=True)
        self.heartbeat_thread.start()
        while not self.stop_event.is_set():
            try:
                for record in self.store.all('operation'):
                    if record['state'] == 'TERMINAL':
                        self._post_outputs_receipt(record)
                response = self.client.post('poll', {})
                self.binding = response.get('binding')
                if response.get('envelope'):
                    self.execute(response['envelope'])
                else:
                    self.stop_event.wait(.1)
            except LinkError as exc:
                if exc.code != Code.WORKER_UNAVAILABLE:
                    raise
                self.stop_event.wait(.5)

    def close(self):
        self.stop_event.set()
        if self.heartbeat_thread:
            self.heartbeat_thread.join(4)
        if self.runner:
            self.runner.close()
        os.close(self.lock_fd)
        self.store.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Operate one explicitly selected project through a Docker worker.')
    parser.add_argument('--broker', required=True)
    parser.add_argument('--worker-id', default='local-dev')
    parser.add_argument('--project', required=True)
    parser.add_argument('--alias', default='project')
    parser.add_argument('--image', required=True, help='Inspected immutable sha256 image ID')
    parser.add_argument('--state-dir', required=True)
    parser.add_argument('--local-test', action='store_true')
    parser.add_argument('--ca-file')
    parser.add_argument('--memory-mb', type=int, default=512)
    parser.add_argument('--cpus', type=int, default=1)
    args = parser.parse_args(argv)
    worker = None
    try:
        secret = os.environ.get('WORKBENCH_LINK_TOKEN') or getpass.getpass('Worker key (hex): ')
        worker = Worker(args.broker, args.worker_id, args.project, args.image, args.state_dir, key_bytes(secret),
                        alias=args.alias, local_test=args.local_test, ca_file=args.ca_file,
                        memory_mb=args.memory_mb, cpus=args.cpus)
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, lambda *_: worker.stop_event.set())
        worker.run()
        return 0
    except LinkError as exc:
        print(str(exc)); return 3
    except (OSError, ValueError, subprocess.TimeoutExpired):
        print('Worker setup failed. Check selected project permissions and Docker/image availability.'); return 2
    finally:
        if worker:
            worker.close()


if __name__ == '__main__':
    raise SystemExit(main())
