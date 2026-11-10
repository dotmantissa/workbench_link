# Hermes compatibility

Workbench Link 0.1.0 targets Hermes `>=0.23.0,<0.24.0` and is verified against v0.23.0 (`2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19`). Hermes uses its supported Python 3.14 runtime; the standalone worker/library supports Python 3.11+ on Linux. The plugin has no third-party Python runtime dependencies.

| Integration | Contract |
|---|---|
| Plugin loading | Root `plugin.yaml` and relative `__init__.py` directory entrypoint |
| Provider | Public `agent.terminal_env_provider.TerminalEnvironmentProvider` registered through `ctx` |
| Environment | Documented `tools.environments.base.BaseEnvironment` subclass; native shell snapshots and file operations |
| Process handle | Owned pipe with `poll`, `wait`, `kill`, `stdout` and cached `returncode`; remote PIDs are not host PIDs |
| Configuration | `ctx.get_config`, profile-scoped plugin storage and Hermes secret settings |
| Approvals | Container guards remain enabled because the project mount contains persistent user data |
| Isolation | Requires `plugins.isolation: in_process`; isolated plugin-host loading refuses explicitly |
| Native processes | Persistent code kernels and background log/poll/wait/kill; `persist_on_release` refused before dispatch |
| Additional Docker configuration | Extra mounts, environment forwarding and incompatible image/resource overrides refused |

The manifest, terminal backend and worker module names are respectively `workbench-link`, `workbench_link` and `workbench_link.worker`. Directory discovery does not require installing the worker wheel, and the worker wheel does not replace the directory-plugin manifest.

## Upstream interfaces

- [Terminal environment provider guide](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin)
- [Provider source at v0.23.0](https://github.com/NousResearch/hermes-agent/blob/v0.23.0/agent/terminal_env_provider.py)
- [BaseEnvironment source at v0.23.0](https://github.com/NousResearch/hermes-agent/blob/v0.23.0/tools/environments/base.py)
- [Plugin public API](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/public-api)

Runtime upgrades require repeating the native integration and installation checks in [testing](testing.md). Gateway profile multiplexing, delegated sessions, screen/browser streams and automatic attachment synchronization have separate lifecycle contracts and are not supported by this release.
