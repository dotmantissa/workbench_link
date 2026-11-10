"""Real Hermes discovery and native tool routing; requires its supported runtime.

Run through the pinned Hermes scripts/run-in-hermes-env, with Docker access.
Only disposable fixture directories under this repository are selected.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from workbench_link import control
from workbench_link.broker import Broker
from workbench_link.settings import Settings
from workbench_link.worker import Worker


def wait_until(fn, seconds=20):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if result := fn():
            return result
        time.sleep(.1)
    raise TimeoutError('Native integration condition did not become true.')


def native_client(control_dir, decoy):
    home = Path(os.environ['HERMES_HOME'])
    os.chdir(decoy)
    try:
        from model_tools import handle_function_call
        from hermes_cli.plugins import get_plugin_manager
        from tools.terminal_tool_lifecycle import cleanup_all_environments, get_active_env
        from tools.terminal_tool import set_approval_callback
        loaded = next(item for item in get_plugin_manager().list_plugins()
                      if item['name'] == 'workbench-link')
        assert not loaded.get('error'), loaded
        timings = {}

        def call(name, arguments):
            started = time.monotonic()
            result = json.loads(handle_function_call(name, arguments, task_id='native-fixture',
                                                    session_id='native-fixture'))
            timings[name] = int((time.monotonic() - started) * 1000)
            print(json.dumps({'tool': name, 'result': result}), flush=True)
            assert not result.get('error'), result
            return result

        read = call('read_file', {'path': '/workspace/marker.txt'})
        assert 'WORKER' in json.dumps(read) and 'SERVER' not in json.dumps(read), read
        call('patch', {'path': '/workspace/maths.py', 'old_string': 'return a - b',
                       'new_string': 'return a + b'})
        tested = call('terminal', {'command': 'python test_maths.py'})
        assert 'PASS' in json.dumps(tested), tested
        call('write_file', {'path': '/workspace/created.txt', 'content': 'worker-created\n'})
        found = call('search_files', {'path': '/workspace', 'pattern': 'worker-created'})
        assert 'created.txt' in json.dumps(found), found
        before = control.request(control_dir, 'status')['operations']
        for name, arguments in (
            ('execute_code', {'code': "print('must not run')"}),
            ('terminal', {'command': 'sleep 30', 'background': True}),
            ('terminal', {'command': 'sleep 30 &'})):
            refusal = json.loads(handle_function_call(name, arguments, task_id='native-fixture'))
            assert 'UNSUPPORTED_RUNTIME' in refusal.get('error', ''), refusal
        assert before == control.request(control_dir, 'status')['operations']
        env = get_active_env('native-fixture')
        assert env and not env.uses_host_filesystem
        exact = env.execute('cat', stdin_data='字\r\nno newline')
        assert exact['output'] == '字\r\nno newline', exact
        env.execute('mkdir -p nested; cd nested; export WB_TEST_VALUE=retained')
        persisted = env.execute('printf "%s:%s" "$PWD" "$WB_TEST_VALUE"')
        assert persisted['output'] == '/workspace/nested:retained', persisted
        env.execute('cd /workspace')
        fetched = home / 'fetched.txt'
        env.fetch_file('/workspace/marker.txt', fetched, max_bytes=1024)
        assert fetched.read_bytes() == b'WORKER\n'
        assert env.fetch_realpath('/workspace/marker.txt') == '/workspace/marker.txt'
        denied = []

        def deny(command, description, **kwargs):
            denied.append(command)
            return 'deny'
        before = control.request(control_dir, 'status')['operations']
        set_approval_callback(deny)
        result = json.loads(handle_function_call('terminal',
            {'command': 'rm -rf /workspace/approval-sentinel'}, task_id='native-fixture'))
        assert denied and result.get('status') == 'blocked', result
        after = control.request(control_dir, 'status')['operations']
        assert before == after, (before, after)
        (home / 'disconnect-request').touch()
        wait_until(lambda: not control.request(control_dir, 'status')['connected'])
        before = control.request(control_dir, 'status')['operations']
        refused = json.loads(handle_function_call('terminal',
            {'command': 'printf fallback > marker.txt'}, task_id='native-fixture'))
        assert refused.get('error') and 'WORKER_UNAVAILABLE' in refused['error'], refused
        assert before == control.request(control_dir, 'status')['operations']
        print(json.dumps({'ok': True, 'native_tools': list(timings), 'timings_ms': timings,
            'approval_denied_before_dispatch': True, 'stdin_exact': True,
            'cwd_env_persisted': True, 'file_fetch_verified': True,
            'unsupported_code_background_refused_before_dispatch': True,
            'disconnect_refused_without_dispatch_or_fallback': True}), flush=True)
    finally:
        from tools.terminal_tool_lifecycle import cleanup_all_environments
        cleanup_all_environments()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image')
    parser.add_argument('--server-control')
    parser.add_argument('--server-decoy')
    parser.add_argument('--hermes-source', required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(Path(args.hermes_source).resolve(strict=True)))
    if args.server_control:
        native_client(Path(args.server_control), Path(args.server_decoy))
        return
    if not args.image:
        parser.error('--image is required for the Docker topology')
    (ROOT / '.runtime').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='native-', dir=ROOT / '.runtime') as directory:
        root = Path(directory)
        project, decoy, home = root / 'project', root / 'server', root / 'home'
        for path in (project, decoy, home):
            path.mkdir()
        for target, marker in ((project, 'WORKER'), (decoy, 'SERVER')):
            (target / 'marker.txt').write_text(marker + '\n')
            (target / 'maths.py').write_text('def add(a, b):\n    return a - b\n')
            (target / 'test_maths.py').write_text('from maths import add\nassert add(2, 3) == 5\nprint("PASS")\n')
        original = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in decoy.iterdir()}
        key = os.urandom(32)
        os.environ['HERMES_HOME'] = str(home)
        os.environ['WORKBENCH_LINK_TOKEN'] = key.hex()
        os.environ['HERMES_INTERACTIVE'] = '1'
        os.environ.pop('HERMES_SINGLE_QUERY_SESSION', None)
        os.environ.pop('HERMES_YOLO', None)
        import hermes_yaml as yaml
        (home / 'config.yaml').write_text(yaml.safe_dump({
            'terminal': {'backend': 'workbench_link', 'cwd': '/workspace', 'timeout': 20},
            'approvals': {'mode': 'manual', 'timeout': 3},
            'plugins': {'isolation': 'in_process', 'enabled': ['workbench-link'], 'entries': {'workbench-link': {
                'enabled': True, 'settings': {'worker_id': 'dev', 'project_alias': 'fixture',
                    'control_dir': str(root / 'broker')}}}}}))
        installed = home / 'plugins' / 'workbench-link'
        installed.mkdir(parents=True)
        for filename in ('__init__.py', 'plugin.yaml'):
            shutil.copy2(ROOT / filename, installed / filename)
        shutil.copytree(ROOT / 'workbench_link', installed / 'workbench_link',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        broker = Broker(Settings('dev', 'fixture', root / 'broker'), key,
                        ('127.0.0.1', 0), local_test=True).start()
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
            control.request(root / 'broker', 'bind', instance_id=worker.instance,
                            project_id=worker.project_id, image=args.image)
            server_name = 'workbench-link-native-' + worker.instance
            mounts = [ROOT / 'dev', ROOT / 'workbench_link', Path(__file__).resolve(),
                      home, decoy, root / 'broker']
            argv = ['docker', 'run', '--name', server_name, '--network', 'none',
                    '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                    '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,mode=1777',
                    '--env', 'WORKBENCH_LINK_TOKEN', '--env', 'HERMES_HOME',
                    '--env', 'HERMES_INTERACTIVE', '--env', 'PYTHONPATH', '--env', 'PYTHONDONTWRITEBYTECODE=1',
                    '--entrypoint', sys.executable]
            for mounted in mounts:
                mode = ',readonly' if mounted in mounts[:3] else ''
                argv += ['--mount', f'type=bind,source={mounted},target={mounted}{mode}']
            argv += [args.image, str(Path(__file__).resolve()), '--hermes-source',
                     str(Path(args.hermes_source).resolve()), '--server-control', str(root / 'broker'),
                     '--server-decoy', str(decoy)]

            def disconnect_worker():
                while not worker.stop_event.wait(.1):
                    if (home / 'disconnect-request').exists():
                        worker.stop_event.set()
                        return
            monitor = threading.Thread(target=disconnect_worker, daemon=True)
            monitor.start()
            try:
                tested = subprocess.run(argv, env=os.environ, text=True, capture_output=True,
                                        timeout=120, check=False)
                print(tested.stdout, end='', flush=True)
                if tested.returncode:
                    print(tested.stderr, file=sys.stderr)
                assert tested.returncode == 0, 'Native server fixture failed.'
                inspected = json.loads(subprocess.run(['docker', 'inspect', server_name],
                    capture_output=True, text=True, timeout=5, check=True).stdout)[0]
                sources = {entry['Source'] for entry in inspected['Mounts']}
                assert sources == {str(path) for path in mounts}, sources
                assert str(project) not in sources and '/var/run/docker.sock' not in sources
                assert inspected['HostConfig']['NetworkMode'] == 'none'
            finally:
                subprocess.run(['docker', 'rm', '--force', server_name], capture_output=True,
                               timeout=5, check=False)
                worker.stop_event.set()
                monitor.join(2)
            assert (project / 'maths.py').read_text().endswith('return a + b\n')
            assert (project / 'created.txt').read_text() == 'worker-created\n'
            assert (project / 'marker.txt').read_bytes() == b'WORKER\n'
            assert original == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in decoy.iterdir()}
            assert not errors, errors
            print(json.dumps({'ok': True, 'isolated_hermes_server': True,
                'server_has_no_project_mount_or_docker_socket': True,
                'decoy_unchanged': original, 'image': args.image}), flush=True)
        finally:
            os.chdir(ROOT)
            worker.stop_event.set()
            thread.join(6)
            worker.close()
            broker.close()
            if thread.is_alive():
                raise RuntimeError('Worker shutdown exceeded its budget.')
            os.environ.pop('WORKBENCH_LINK_TOKEN', None)


if __name__ == '__main__':
    main()
