"""Only this module imports Hermes; standalone services remain independent."""

import json
import os
from pathlib import Path

from agent.secret_scope import get_secret
from agent.terminal_env_provider import TerminalEnvironmentProvider
from hermes_cli.config import load_config_readonly
from plugins.plugin_storage import plugin_data_dir

from . import control
from .errors import Code, LinkError
from .settings import Settings, key_bytes


def settings_for(ctx):
    configured = ctx.get_config('control_dir', '')
    if type(configured) is not str:
        raise LinkError(Code.BAD_REQUEST, 'control_dir must be a path string.')
    # Hermes creates the plugin data root; private state is in our own 0700 child.
    directory = Path(configured) if configured else plugin_data_dir('workbench-link') / 'control'
    return Settings(ctx.get_config('worker_id', 'local-dev'), ctx.get_config('project_alias', 'project'),
                    directory, ctx.get_config('timeout', 120), ctx.get_config('memory_mb', 512), ctx.get_config('cpus', 1))


class WorkbenchProvider(TerminalEnvironmentProvider):
    name = 'workbench_link'
    display_name = 'Workbench Link'
    is_remote = True
    is_container = True
    supports_streams = False
    session_isolated_when_nonpersistent = False

    def __init__(self, ctx):
        self.ctx = ctx

    @property
    def skip_container_guards(self):
        return False

    @property
    def default_cwd(self):
        return '/workspace'

    @property
    def cache_path_base(self):
        return '/tmp/.hermes'

    @property
    def strip_env_keys(self):
        return frozenset({'WORKBENCH_LINK_TOKEN'})

    @property
    def env_description(self):
        return 'the selected Workbench Link project container (Linux)'

    def is_available(self):
        # Configuration-only picker probe; transport checks are deliberate CLI actions.
        try:
            key_bytes(get_secret('WORKBENCH_LINK_TOKEN', ''))
            return True
        except LinkError:
            return False

    def setup_instructions(self):
        return ['Set the Workbench Link worker key through Hermes plugin settings.',
                'Start `hermes workbench-link serve`, start the selected worker, then accept its binding.',
                'Select terminal.backend: workbench_link in this foreground CLI profile.']

    def create_environment(self, *, cwd, timeout, task_id='default', image=None, container_config=None, **kwargs):
        from .environment import WorkbenchEnvironment
        key_bytes(get_secret('WORKBENCH_LINK_TOKEN', ''))
        settings = settings_for(self.ctx)
        identity = control.request(settings.control_dir, 'open_environment')
        try:
            # The backend reads its own inspected image; core's generic image is not its configuration.
            # Refuse an explicitly pinned Docker override rather than imply it changes the local mount.
            if container_config and container_config.get('docker_image_pinned'):
                if image != identity['image']:
                    raise LinkError(Code.UNSUPPORTED_RUNTIME, 'Pinned image override differs from the accepted worker image.')
            return WorkbenchEnvironment(settings.control_dir, identity, cwd or '/workspace', timeout)
        except BaseException:
            control.request(settings.control_dir, 'close_environment', environment_id=identity['environment_id'])
            raise


def register(ctx):
    if os.environ.get('HERMES_PLUGIN_HOST_PROCESS') == '1':
        raise LinkError(Code.UNSUPPORTED_RUNTIME,
            'Workbench Link requires plugins.isolation: in_process for its native environment handles.')
    from .cli import setup_parser, run_cli
    ctx.register_terminal_environment_provider(WorkbenchProvider(ctx))
    def guard_lifecycle(tool_name=None, args=None, **kwargs):
        if load_config_readonly().get('terminal', {}).get('backend') != 'workbench_link':
            return None
        args = args or {}
        command = args.get('command', '')
        background = (tool_name == 'terminal' and
            (args.get('background') or (isinstance(command, str) and command.rstrip().endswith('&'))))
        if tool_name == 'execute_code' or background:
            return {'action': 'block', 'message':
                'UNSUPPORTED_RUNTIME: Workbench Link currently supports foreground terminal and native file tools. '
                'Persistent execute_code kernels and background jobs require lifecycle support that is not implemented. '
                'No operation was dispatched.'}
        return None
    ctx.register_hook('pre_tool_call', guard_lifecycle)
    ctx.register_cli_command('workbench-link', 'Manage the selected project worker', setup_parser,
                            lambda args: run_cli(args, settings_for(ctx), get_secret('WORKBENCH_LINK_TOKEN', '')))

    def status_command(raw_args=''):
        if raw_args.strip():
            return 'Use /workbench-link without arguments to inspect the current profile binding.'
        try:
            result = control.request(settings_for(ctx).control_dir, 'status')
            return json.dumps(result, ensure_ascii=False, sort_keys=True)
        except LinkError as exc:
            return str(exc)
    ctx.register_command('workbench-link', status_command, description='Show the current profile project binding')
