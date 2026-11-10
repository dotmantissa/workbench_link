# Installation, commands and recovery specification

This document preserves the broader intended interfaces. The implemented November 10 checkpoint uses `serve`, `bind`, `status`, `doctor` and `/workbench-link`; exact runnable setup is in [README.md](../README.md). Other commands below remain planned. No frontend is required.

## 1. Host setup

Prerequisites: supported Hermes release, Linux host, one dedicated Workbench profile with one active foreground CLI session initially, source plugin installed/enabled and `plugins.isolation: in_process`. The host does not need Docker for real deployment; Docker is used for the local test topology. Gateway execution/multiplexing is gated until identity/refusal behavior is tested.

1. Install source through the normal Hermes plugin workflow. Development uses the documented local-directory workflow verified in the disposable release; publication uses a catalog name only after acceptance.
2. Set the plugin-specific `worker_token` through Hermes's secret settings route, or explicitly provide `WORKBENCH_LINK_TOKEN` in the launch environment. A generated key is shared deliberately with the worker; it is never extracted from another application's login.
3. Launch `hermes workbench-link broker --listen 127.0.0.1:8765`. The command captures active profile settings/secret using public helpers. Broker remains an explicit foreground process by default; a documented service unit may supervise it later. No daemon starts on plugin registration.
4. For remote use, put an operator-managed verified HTTPS reverse proxy in front of the worker API. Only the worker namespace is forwarded. The private Unix operator socket is never exposed.
5. After worker acceptance, select `terminal.backend: workbench_link` through normal Hermes configuration and start a new session in this profile. The plugin does not overwrite selection silently.

In a server test container, broker may listen on `0.0.0.0` only inside that container, with its host port published on `127.0.0.1`. This is an explicit local-test topology; not a default public listener.

## 2. Local worker setup

1. Verify Python and Docker daemon access explicitly. Missing Docker yields prerequisite guidance; no install/pull happens during agent execution.
2. Build the shipped source image from its pinned official base and record the image digest. Select a tiny test project without credentials for first use.
3. Run from checkout or installed source package:

```text
python -m workbench_link.worker run \
  --broker http://127.0.0.1:8765 \
  --worker-id local-dev \
  --project /absolute/path/to/selected-project \
  --image <locally-built-pinned-image-id> \
  --state-dir <private-worker-state-directory> \
  --local-test
```

4. Supply the shared key through the secret prompt or explicitly provided `WORKBENCH_LINK_TOKEN`. No token argument, token URL/query or saved token file. Unattended startup requires a supplied secret and never waits for input.
5. Startup prints the chosen project, image, allowed mount and network policy. The invocation is the local owner's acceptance of that project. There is no remote command to mount another directory.
6. Worker connects outbound and announces project/instance identity. Host operator runs `hermes workbench-link accept --worker local-dev --project <project-id>` only after inspecting those facts. Acceptance is tied to the exact instance and runtime; it cannot clear unresolved prior work.

The worker's Docker access is trusted host authority. Agent commands receive only the project bind mount and container filesystem; no Docker socket, host home or worker state. Project secrets inside the chosen directory are still readable by commands and can be returned to Hermes.

## 3. Command inventory

| Command | Effect | Unattended behavior |
|---|---|---|
| `hermes workbench-link status [--json]` | profile-scoped identity/state from private IPC | bounded error if broker absent |
| `hermes workbench-link doctor [--json]` | deliberate local configuration/IPC/runtime checks | no prompts, fixed deadlines |
| `hermes workbench-link broker ...` | starts broker foreground | missing key fails |
| `hermes workbench-link accept ...` | accepts announced worker/project instance | explicit IDs required; no automatic selection |
| `hermes workbench-link operations [--json]` | bounded recent metadata/receipt list | no raw output by default |
| `hermes workbench-link inspect <operation-id> [--output]` | receipt/status; output on explicit request | bounded private read |
| `hermes workbench-link cancel <operation-id>` | durable cancellation request | never reports stopped without receipt |
| `hermes workbench-link recover` | reconciles stored receipts | never dispatches/replays shell |
| `hermes workbench-link resolve <operation-id> --note ...` | human resolution of irreducible unknown after stopped environment | refuses unattended clearing |
| `hermes workbench-link stop` | stops binding/broker with bounded cleanup | pending outcomes remain fenced |
| `/workbench status` | read-only selected profile binding/session note | available in supported chat contexts |

No model-facing management tool may clear a fence, accept another project, rotate keys or alter backend selection. Slash command cannot infer factory task identity from `session_id`. Status labels “Profile binding” unless a real environment/session association is known.

## 4. Status format and error copy

Normal status is compact:

```text
Workbench Link — ready
Profile: workbench-dev
Target: local-dev / example-project
Generation: 3   Cwd: /workspace
Operation: none
```

Unavailable:

```text
WORKER_UNAVAILABLE — local-dev has not renewed its connection.
No command was dispatched. Start the selected worker, then check status.
```

Uncertain:

```text
OUTCOME_UNKNOWN — operation <id> may have changed example-project.
Execution is blocked for this project generation.
Run: hermes workbench-link recover
If no receipt can establish the outcome, inspect the project locally and resolve it explicitly.
```

Cancellation pending:

```text
CANCEL_PENDING — cancellation requested for operation <id>.
Termination has not been confirmed; further execution remains blocked.
```

Color supplements words. Respect non-TTY output and NO_COLOR. No ANSI animation, image assets or branded ASCII art is needed. Help names supported scope, shows an example and points to one specific next step for a missing prerequisite. `--json` contains schema version and codes, never raw keys or sensitive headers.

## 5. Normal use

1. Start broker and worker, accept the worker/project, select the Workbench profile and start a new Hermes session.
2. Check `/workbench status`; verify intended profile and target.
3. Ask Hermes to inspect a bug, edit the relevant file and run its tests. Hermes uses existing native tools. Normal host policy may ask for approval; denial means zero worker dispatch.
4. Cwd and exported env persist within the environment. The selected project mount persists edits. Changing target requires teardown and a new binding/session; no mid-command switching.
5. Stop the worker/binding when done. Containers/scratch terminate; explicit project edits remain. The plugin does not undo them.

## 6. Recovery flows

**Disconnected before grant:** show unavailable/no-start only if the ledger proves no valid launch grant. Connection restoration permits a fresh user request; it does not silently execute a timed-out queue item.

**Disconnected after grant or during execution:** mark unknown/cancel pending and fence. Worker kills/stops according to lease deadline and stores receipts. Recover fetches those facts. Known completed result is delivered without another shell run. Missing proof stays unknown.

**Broker restarted:** read durable ledgers, fence unresolved generations, reconnect worker and reconcile receipts before accepting new execution. A new native environment cannot remove this state.

**Worker restarted or laptop slept:** old instance is stale. Stop/reconcile matching old containers, resend stored receipts, explicitly accept new instance. Lost snapshot/scratch is reported; project changes are inspected as needed.

**Cancel:** request is immediate but confirmation may lag. Natural exit/cancel race is reported from actual receipt. If process-group kill is inconclusive, stop the whole environment and invalidate it. Never say effects were rolled back.

**Unknown without recoverable receipt:** local human inspects the project through their own normal tools, stops the environment, and records a note using resolve. The CLI confirms the operation ID/project and explains that history remains unknown. It cannot be automated by a model prompt or called during cron. No automatic replay follows resolution.

**Key mismatch/rotation:** authentication fails before dispatch. Stop/quiesce, change Hermes-owned key and explicitly supply matching worker key, restart and reaccept if needed. No plugin reads vendor logins to fix it.

**Disk/output limit:** stop/confirm termination, mark explicit limit/integrity failure, retain receipt/partial output within quota and prevent native parsers seeing truncated data as successful. If state cannot be persisted, refuse new execution.

## 7. Data disclosure and maintenance

Network: command payload, explicit stdin and output move between broker and worker; no public SaaS dependency. Processes: explicit broker/worker and Docker project container. Files: selected project read/write, own app state, source image build and logs. Command/stdin/output spools can contain secrets even though transport keys are never stored there. No telemetry.

Updates are quiescent, source-pinned catalog changes. Stop active environments; reconcile unresolved work; update source/worker together; migrate ledger transactionally; restart and accept current identity. Version mismatch fails closed. Removing plugin source does not silently erase durable uncertainty history. An explicit purge command, if later implemented, must refuse active/unresolved state and explain data loss.

## 8. Deferred operational support

Real remote hosting instructions follow actual tested deployment, not the current local demonstration. macOS/Windows worker instructions follow their own validated container/path behavior. No browser/desktop setup is part of this plugin. Automatic service installation, extra runtime images and attachment synchronization are convenience work after the native reliability gates.
