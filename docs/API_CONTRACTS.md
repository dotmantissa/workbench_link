# Hermes compatibility: evidence and integration gates

Baseline inspected: released tag **v0.23.0**, published November 5, 2026. Source inspection is not a runtime result. The implementation spike must resolve each row below through actual discovery and native calls.

| Surface | Source-verified behavior | Implementation consequence |
|---|---|---|
| `TerminalEnvironmentProvider` | documented ABC in `agent.terminal_env_provider` | import public provider, register through ctx |
| `ctx.register_terminal_environment_provider` | documented native registration | no built-in tool overrides |
| `create_environment` | keyword cwd/timeout/task/image/container config + additive kwargs | accept exact public signature; task identity is opaque |
| `BaseEnvironment` | documented subclass option; `_run_bash` + cleanup; shared snapshots/wait/files | use superclass behavior rather than copying private helpers |
| `ProcessHandle` | duck type poll/kill/wait/stdout/returncode; Popen or SDK-like handles | own pipe-backed cached handle; no private `_ThreadedProcessHandle` import |
| Results | real `execute` implementation returns output + `returncode` | guide's simple exit_code sample is not enough |
| Native file routing | non-host environment file tools use execute | explicit uses_host_filesystem=False; marker tests |
| Approval classification | skip_container_guards defaults to is_container | explicitly False because project mount persists |
| Provider isolation | native environments refused under isolated plugin host | use `plugins.isolation: in_process` |
| `is_available` / picker probe | cheap, no network/startup | cached configured status; deliberate CLI health is separate |
| `default_cwd` | absolute backend path; core sanitizes host-looking cwd | `/workspace`; no server home hints |
| `supports_streams` | opt-in exec_prefix for desktop/browser follow | False; no screen/browser promise |
| Secret settings | type secret with env mapping; read via get_secret | host-owned key, no `.env` parsing |
| `ctx.get_config` | plugin settings namespace | avoid whole-core config reads |
| `plugin_data_dir` | profile-scoped persistent plugin state | separate broker ledger/IPC per profile |
| CLI | register_cli_command(name, help, setup_fn, handler_fn) | native management entry |
| Slash command | register_command; session context differs from task context | read-only profile/binding status; no switching map guess |

## Primary references

- [Terminal Environment Provider guide](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin)
- [v0.23.0 provider source](https://github.com/NousResearch/hermes-agent/blob/v0.23.0/agent/terminal_env_provider.py)
- [v0.23.0 BaseEnvironment](https://github.com/NousResearch/hermes-agent/blob/v0.23.0/tools/environments/base.py)
- [v0.23.0 process-handle source](https://github.com/NousResearch/hermes-agent/blob/v0.23.0/tools/environments/base_output.py)
- [Native plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins)
- [Plugin public API](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/public-api)
- [Catalog submission](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission)

Core factory and built-in Docker source were read to understand behavior, not selected as imports or code to fork. New source snapshots and SHA-256 hashes are in ignored `research/sources/architecture-fetch-manifest.json`. Developer evidence must record the resolved release commit before executing the integration fixture.

## Unresolved runtime contracts

1. Real namespaced directory import and relative package imports; no duplicate pip discovery.
2. Cached/provider creation and shell initialization call order, including prompt-time probes.
3. Own pipe handle with actual output collector, marker parsing, stdin, interrupts and deadline worker.
4. Background/yield-to-background registration and cleanup, including native execute_code behavior.
5. Native uploaded files/cache mapping, spill and explicit fetch paths without private FileSyncManager imports.
6. Active-profile settings/data under gateway multiplexing; no assumption that slash session ID equals factory task ID.
7. Normal denial reaching zero provider execution for dangerous native calls with the selected container backend.
8. Core recreation/retry behavior while binding-level unknown fence persists.
9. Doctor/validate's declared-provider/CLI/command metadata requirements and scanner treatment of documented subclass seams.

Any unsupported seam is a reason to change scope or request an upstream hook. It is not permission to monkey-patch core, private registries or gateway authentication. The broker avoids the previously uncertain gateway worker-auth route entirely by owning its separate transport.
