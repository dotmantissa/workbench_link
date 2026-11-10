"""Explicit local Docker topology test; run with --image <inspected image ID>."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from workbench_link import control, protocol as p
from workbench_link.broker import Broker
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
            print(json.dumps({'ok': True, 'output_exact': True, 'selected_mount_only': True,
                              'no_container_key': True, 'duplicate_grant_effects': 1, 'image': args.image}))
        finally:
            worker.stop_event.set(); thread.join(6)
            worker.close(); broker.close()
            if thread.is_alive():
                raise RuntimeError('Worker did not stop within shutdown budget.')


if __name__ == '__main__':
    main()
