"""Explicit local Docker topology test; run with --image <inspected image ID>."""

import argparse
import contextlib
import io
import json
import os
import subprocess
import socket
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from workbench_link import control, protocol as p
from workbench_link.broker import Broker, WorkerHandler
from workbench_link.cli import setup_parser, run_cli
from workbench_link.ledger import new_id
from workbench_link.settings import Settings
from workbench_link.worker import Worker


def wait_until(fn, seconds=15):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        result = fn()
        if result:
            return result
        time.sleep(.1)
    raise TimeoutError('Integration condition did not become true.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True)
    args = parser.parse_args()
    (ROOT / '.runtime').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='smoke-', dir=ROOT / '.runtime') as directory:
        root = Path(directory)
        project = root / 'project'; project.mkdir()
        (project / 'marker.txt').write_bytes(b'WORKER\n')
        key = os.urandom(32)
        broker = Broker(Settings('dev', 'fixture', root / 'broker'), key, ('127.0.0.1', 0), local_test=True).start()
        worker = Worker(f'http://127.0.0.1:{broker.http.server_address[1]}', 'dev', project,
                        args.image, root / 'worker', key, alias='fixture', local_test=True)
        errors = []

        def run_worker():
            try:
                worker.run()
            except BaseException as exc:
                errors.append(exc)
        thread = threading.Thread(target=run_worker)
        thread.start()
        try:
            wait_until(lambda: control.request(root / 'broker', 'status')['registrations'])
            control.request(root / 'broker', 'bind', instance_id=worker.instance, project_id=worker.project_id, image=args.image)
            identity = control.request(root / 'broker', 'open_environment')
            envelope = {'protocol_version': 1, 'profile_id': identity['profile_id'],
                'binding_id': identity['binding_id'], 'generation': identity['generation'],
                'environment_id': identity['environment_id'], 'operation_id': new_id(),
                'worker_id': 'dev', 'worker_instance_id': worker.instance, 'project_id': worker.project_id,
                'script': "cat; printf '\\n'; cat marker.txt; test -z \"${WORKBENCH_LINK_TOKEN:-}\"; printf changed > marker.txt",
                'stdin_b64': p.b64('字\r\nno newline'.encode()), 'login': False, 'timeout_seconds': 10}
            envelope['payload_sha256'] = p.payload_hash(envelope)
            control.request(root / 'broker', 'submit', envelope=envelope)
            status = wait_until(lambda: (value if (value := control.request(root / 'broker', 'operation_status',
                               operation_id=envelope['operation_id']))['receipt'] else None), 20)
            output = p.unb64(control.request(root / 'broker', 'read_output', operation_id=envelope['operation_id'], offset=0)['data_b64'], p.CHUNK_LIMIT)
            assert output == '字\r\nno newline\nWORKER\n'.encode(), output
            assert status['receipt']['exit_code'] == 0, status
            assert (project / 'marker.txt').read_bytes() == b'changed'
            assert not errors, errors
            inspected = subprocess.run(['docker', 'inspect', worker.runner.name], capture_output=True, text=True, check=True)
            container = json.loads(inspected.stdout)[0]
            assert len(container['Mounts']) == 1
            assert container['Mounts'][0]['Source'] == str(project)
            assert container['HostConfig']['NetworkMode'] == 'none'
            assert container['HostConfig']['ReadonlyRootfs'] is True
            assert container['Config']['User'] == f'{os.getuid()}:{os.getgid()}'
            assert all(not entry.startswith('WORKBENCH_LINK_TOKEN=') for entry in container['Config']['Env'])
            # Repeated delivery observes the same receipt, with no second marker effect.
            control.request(root / 'broker', 'submit', envelope=envelope)
            assert len(broker.ledger.status()['operations']) == 1
            # Drop the actual HTTP acknowledgement after the broker commits a
            # terminal receipt. Recovery must upload the same receipt, not run again.
            dropped = threading.Event()
            class DropResultAck(WorkerHandler):
                def reply(self, code, obj):
                    if self.path == '/v1/worker/result' and not dropped.is_set():
                        dropped.set()
                        self.connection.shutdown(socket.SHUT_RDWR)
                        self.close_connection = True
                        return
                    super().reply(code, obj)
            broker.http.RequestHandlerClass = DropResultAck
            second = dict(envelope, operation_id=new_id(), script='printf x >> counter.txt', stdin_b64='')
            second['payload_sha256'] = p.payload_hash(second)
            control.request(root / 'broker', 'submit', envelope=second)
            wait_until(lambda: (worker.store.get('operation', second['operation_id']) or {}).get('state') == 'ACKNOWLEDGED', 25)
            assert dropped.is_set() and (project / 'counter.txt').read_bytes() == b'x'
            wait_until(lambda: broker.ledger.status()['environments'][0]['stop_evidence'])
            parser = argparse.ArgumentParser(); setup_parser(parser)
            for arguments in (['inspect', second['operation_id'], '--json'], ['recover', '--json'],
                              ['stop', '--json'], ['reset', '--json'], ['doctor', '--json']):
                with contextlib.redirect_stdout(io.StringIO()) as capture:
                    code = run_cli(parser.parse_args(arguments), broker.settings, '')
                result = json.loads(capture.getvalue())
                assert code == 0 and result['ok'], (arguments, code, result)
            assert broker.ledger.status()['binding']['generation'] == 2
            assert not errors, errors
            print(json.dumps({'ok': True, 'output_exact': True, 'selected_mount_only': True,
                              'no_container_key': True, 'duplicate_grant_effects': 1,
                              'lost_receipt_ack_effects': 1, 'operator_recovery_verified': True, 'image': args.image}))
        finally:
            worker.stop_event.set(); thread.join(6)
            worker.close(); broker.close()
            if thread.is_alive():
                raise RuntimeError('Worker did not stop within shutdown budget.')


if __name__ == '__main__':
    main()
