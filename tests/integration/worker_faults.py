"""Actual Docker cancellation, daemon-death watchdog and broker-restart fences."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from workbench_link import control, protocol as p
from workbench_link.broker import Broker
from workbench_link.errors import Code, LinkError
from workbench_link.ledger import new_id
from workbench_link.settings import Settings


def wait_until(fn, seconds=25):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if value := fn():
            return value
        time.sleep(.1)
    raise TimeoutError('Fault scenario exceeded its deadline.')


def scenario(image, kind):
    with tempfile.TemporaryDirectory(prefix='fault-', dir=ROOT / '.runtime') as directory:
        root = Path(directory)
        project = root / 'project'
        project.mkdir()
        key = os.urandom(32)
        settings = Settings('dev', 'fixture', root / 'broker')
        broker = Broker(settings, key, ('127.0.0.1', 0), local_test=True).start()
        env = dict(os.environ, WORKBENCH_LINK_TOKEN=key.hex(), PYTHONPATH=str(ROOT))
        worker = subprocess.Popen([sys.executable, '-m', 'workbench_link.worker',
            '--broker', f'http://127.0.0.1:{broker.http.server_address[1]}',
            '--worker-id', 'dev', '--alias', 'fixture', '--project', str(project),
            '--image', image, '--state-dir', str(root / 'worker'), '--local-test'],
            env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        identity = None
        try:
            registration = wait_until(lambda: control.request(root / 'broker', 'status')['registrations'])[0]
            control.request(root / 'broker', 'bind', instance_id=registration['instance_id'],
                            project_id=registration['project_id'], image=image)
            identity = control.request(root / 'broker', 'open_environment')
            detached = kind in ('session_death', 'session_restart')
            script = ('python - <<\'PY\'\nimport sys\nsys.stdout.buffer.write(bytes(range(256)) * 8192)\nPY'
                      if kind in ('output', 'session_output') else
                      "python - <<'PY'\nimport sys\nsys.stdout.buffer.write(b'x' * (17 * 1024 * 1024))\nPY" if kind == 'output_limit' else
                      'while true; do printf x >> effects.txt; sleep 0.1; done')
            if detached:
                script = '(while true; do printf x >> effects.txt; sleep .1; done) >/tmp/bg.log 2>&1 & printf launched'
            if kind == 'inherited_output':
                script = 'yes x & printf foreground'
            envelope = {'protocol_version': 1, 'profile_id': identity['profile_id'],
                'binding_id': identity['binding_id'], 'generation': identity['generation'],
                'environment_id': identity['environment_id'], 'operation_id': new_id(),
                'worker_id': 'dev', 'worker_instance_id': registration['instance_id'],
                'project_id': registration['project_id'], 'script': script, 'stdin_b64': '',
                'login': False, 'timeout_seconds': 2 if kind == 'timeout' else 60}
            if detached or kind in ('session_output', 'inherited_output'):
                envelope['lifecycle'] = 'session'
            envelope['payload_sha256'] = p.payload_hash(envelope)
            control.request(root / 'broker', 'submit', envelope=envelope)
            operation_id = envelope['operation_id']
            if kind in ('output', 'session_output', 'output_limit', 'inherited_output'):
                def finished_output():
                    if worker.poll() is not None:
                        raise RuntimeError(worker.stderr.read().decode())
                    value = control.request(root / 'broker', 'operation_status', operation_id=operation_id)
                    if value['state'] == 'UNKNOWN':
                        raise RuntimeError(f'Output became unknown after {value["output_bytes"]} bytes')
                    return value if value['receipt'] else None
                status = wait_until(finished_output, 60)
                receipt = status['receipt']
                output = bytearray()
                while len(output) < receipt['output_bytes']:
                    output.extend(p.unb64(control.request(root / 'broker', 'read_output',
                        operation_id=operation_id, offset=len(output))['data_b64'], p.CHUNK_LIMIT))
                if kind in ('output_limit', 'inherited_output'):
                    assert not receipt['output_complete'] and receipt['error_code'] == 'OUTPUT_LIMIT', receipt
                    assert receipt['terminal_kind'] == 'cancelled' and receipt['termination_confirmed'], receipt
                    assert broker.ledger.status()['binding']['state'] == 'FENCED'
                    return {'scenario': kind, 'ok': True, 'output_bytes': len(output), 'truncated_success_refused': True}
                assert bytes(output) == bytes(range(256)) * 8192
                assert hashlib.sha256(output).hexdigest() == receipt['output_sha256']
                assert receipt['terminal_kind'] == 'completed' and receipt['exit_code'] == 0
                return {'scenario': kind, 'exact_bytes': len(output), 'ok': True}
            wait_until(lambda: (project / 'effects.txt').exists())
            if detached:
                status = wait_until(lambda: (value if (value := control.request(root / 'broker', 'operation_status', operation_id=operation_id))['receipt'] else None))
                assert status['state'] == 'COMPLETED' and status['receipt']['detached_processes']
            started = time.monotonic()
            if kind == 'cancel':
                control.request(root / 'broker', 'cancel', operation_id=operation_id)
            elif kind in ('worker_death', 'session_death'):
                worker.kill()
                worker.wait(timeout=3)
            elif kind == 'runner_death':
                subprocess.run(['docker', 'kill', '--signal', 'KILL',
                                'workbench-link-' + identity['environment_id']],
                               check=True, capture_output=True, timeout=5)
            elif kind in ('broker_restart', 'session_restart'):
                address = broker.http.server_address
                broker.close()
                broker = Broker(settings, key, address, local_test=True).start()
                assert broker.ledger.operation(operation_id)['state'] == ('COMPLETED' if detached else 'UNKNOWN')
            if kind in ('cancel', 'timeout'):
                status = wait_until(lambda: (value if (value := control.request(root / 'broker',
                    'operation_status', operation_id=operation_id))['receipt'] else None))
                assert status['receipt']['terminal_kind'] == 'cancelled', status
                assert status['receipt']['termination_confirmed'], status
            elif not detached:
                wait_until(lambda: broker.ledger.operation(operation_id)['state'] == 'UNKNOWN')
            else:
                wait_until(lambda: broker.ledger.status()['binding']['state'] == 'FENCED')
            name = 'workbench-link-' + identity['environment_id']

            def stopped():
                result = subprocess.run(['docker', 'inspect', '--format', '{{.State.Running}}', name],
                                        capture_output=True, timeout=3, check=False)
                return result.returncode != 0 or result.stdout.strip() == b'false'
            wait_until(stopped)
            elapsed_ms = int((time.monotonic() - started) * 1000)
            frozen = (project / 'effects.txt').read_bytes()
            time.sleep(.5)
            assert frozen == (project / 'effects.txt').read_bytes(), 'Effects continued after stopped evidence.'
            if kind != 'timeout':
                assert broker.ledger.status()['binding']['state'] == 'FENCED'
                fresh = dict(envelope, operation_id=new_id())
                fresh['payload_sha256'] = p.payload_hash(fresh)
                try:
                    broker.ledger.submit(fresh)
                except LinkError as exc:
                    assert exc.code == Code.OUTCOME_UNKNOWN, exc
                else:
                    raise AssertionError('A fresh operation bypassed the project fence.')
            return {'scenario': kind, 'ok': True, 'stopped_ms': elapsed_ms,
                    'effects_frozen': True, 'state': broker.ledger.operation(operation_id)['state']}
        finally:
            if worker.poll() is None:
                worker.terminate()
                try:
                    worker.wait(timeout=7)
                except subprocess.TimeoutExpired:
                    worker.kill()
                    worker.wait(timeout=2)
            if identity:
                name = 'workbench-link-' + identity['environment_id']
                subprocess.run(['docker', 'rm', '--force', name], capture_output=True, timeout=5, check=False)
            broker.close()
            worker.stderr.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True)
    parser.add_argument('--scenario')
    args = parser.parse_args()
    (ROOT / '.runtime').mkdir(exist_ok=True)
    for kind in ('output', 'session_output', 'output_limit', 'inherited_output', 'cancel', 'timeout', 'worker_death', 'runner_death', 'broker_restart', 'session_death', 'session_restart'):
        if args.scenario and args.scenario != kind:
            continue
        print(json.dumps(scenario(args.image, kind)), flush=True)


if __name__ == '__main__':
    main()
