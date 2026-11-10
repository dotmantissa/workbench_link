"""Clean profile discovery/enable, CLI, host refusal and missing-key rehearsal.

Run in the supported pinned Hermes environment with --hermes-source. No model,
worker, broker, user profile or credential file is required. HERMES_HOME must
select this repository's disposable, already installed Hermes runtime.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hermes-source', required=True)
    args = parser.parse_args()
    source = Path(args.hermes_source).resolve(strict=True)
    sys.path.insert(0, str(source))
    import hermes_yaml as yaml
    (ROOT / '.runtime').mkdir(exist_ok=True)
    runtime_home = Path(os.environ['HERMES_HOME']).resolve(strict=True)
    if not runtime_home.is_relative_to(ROOT / 'dev/runtime'):
        parser.error('HERMES_HOME must select the disposable runtime under dev/runtime.')
    profiles = runtime_home / 'profiles'
    profiles.mkdir(exist_ok=True)
    # Named profiles share the installed Hermes dependency environment through
    # public root selection. The plugin/configuration itself starts entirely fresh.
    with tempfile.TemporaryDirectory(prefix='install-', dir=ROOT / '.runtime') as directory, \
         tempfile.TemporaryDirectory(prefix='install-', dir=profiles) as profile:
        root = Path(directory)
        home = Path(profile)
        installed = home / 'plugins' / 'workbench-link'; installed.mkdir(parents=True)
        for name in ('__init__.py', 'plugin.yaml', 'pyproject.toml', 'README.md', 'LICENSE'):
            shutil.copy2(ROOT / name, installed / name)
        shutil.copytree(ROOT / 'workbench_link', installed / 'workbench_link',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        (home / 'config.yaml').write_text(yaml.safe_dump({'terminal': {
            'backend': 'workbench_link', 'cwd': '/workspace'}, 'plugins': {
            'isolation': 'in_process', 'entries': {'workbench-link': {
                'settings': {'control_dir': str(root / 'broker')}}}}}))
        environment = {**os.environ, 'HERMES_HOME': str(home),
                       'PYTHONPATH': str(source) + os.pathsep + os.environ.get('PYTHONPATH', ''),
                       'PYTHONDONTWRITEBYTECODE': '1'}
        environment.pop('WORKBENCH_LINK_TOKEN', None)
        environment.pop('HERMES_PLUGIN_HOST_PROCESS', None)
        # Force the supported launcher to verify this profile's runtime selection.
        environment.pop('__HERMES_ACTIVATED', None)

        def run(arguments, expected=0, env=None, prepare=False):
            command = [str(source / 'scripts/run-in-hermes-env'), 'python'] if prepare else [sys.executable]
            print(json.dumps({'step': arguments, 'prepare': prepare}), flush=True)
            process = subprocess.Popen([*command, *arguments],
                                       env=env or environment, cwd=source,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, start_new_session=True)
            try:
                stdout, stderr = process.communicate(timeout=900 if prepare else 240)
            except subprocess.TimeoutExpired:
                # Stop setup descendants before deleting their temporary home.
                os.killpg(process.pid, signal.SIGKILL)
                stdout, stderr = process.communicate()
                raise RuntimeError(f'Installation step timed out: {arguments}\n{stdout}\n{stderr}') from None
            assert process.returncode == expected, (arguments, stdout, stderr)
            return stdout

        run(['-m', 'hermes_cli.main', 'plugins', 'enable', 'workbench-link'], prepare=True)
        run(['-m', 'hermes_cli.main', 'plugins', 'doctor', str(installed), '--ci'])
        help_text = run(['-m', 'hermes_cli.main', 'workbench-link', '--help'])
        assert all(name in help_text for name in ('serve', 'bind', 'inspect', 'recover', 'resolve', 'reset'))
        unavailable = json.loads(run(['-m', 'hermes_cli.main', 'workbench-link', 'status', '--json'], expected=3))
        assert unavailable['code'] == 'WORKER_UNAVAILABLE', unavailable
        run(['-c', "import json; from model_tools import handle_function_call; "
             "r=json.loads(handle_function_call('terminal', {'command':'printf unintended'}, task_id='missing-key')); "
             "assert 'AUTH_FAILED' in r.get('error',''), r"])
        run(['-c', "import model_tools; from hermes_cli.plugins import get_plugin_manager; "
                    "items=get_plugin_manager().list_plugins(); "
                    "p=next(x for x in items if x['name']=='workbench-link'); "
                    "assert 'UNSUPPORTED_RUNTIME' in str(p.get('error','')), p"],
                   env={**environment, 'HERMES_PLUGIN_HOST_PROCESS': '1'})
        assert not (root / 'broker').exists(), 'Discovery or missing setup started broker state.'
        print(json.dumps({'ok': True, 'clean_directory_enable_doctor_cli': True,
                          'fresh_named_profile': True,
                          'missing_key_refused': True, 'host_isolation_refused': True,
                          'registration_started_no_broker': True}))


if __name__ == '__main__':
    main()
