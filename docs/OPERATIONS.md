# Installation and recovery

Version 0.1.0 uses one Linux/Docker project worker and one foreground Hermes CLI profile. Follow [README.md](../README.md) for source installation, key setup, image build and exact launch commands. All management requests use the profile's private Unix socket; the worker HTTP listener exposes no operator actions.

| Command | Behavior |
|---|---|
| `serve --listen HOST --port PORT` | Foreground broker; remote connections require `--tls-cert` and `--tls-key`; explicit loopback tests use `--local-test` |
| `bind --instance-id UUID --project-id UUID --image sha256:…` | Accept exact live worker identities; never changes its chosen project root |
| `status [--json]` | Connection, immutable binding/generation, bounded recent operations and environment-stop evidence |
| `doctor [--json]` | Status plus private IPC, worker identity and active-binding checks |
| `operations [--json]` | Same bounded recent metadata; no command output |
| `inspect UUID [--json]` | State and receipt for any retained operation |
| `inspect UUID --output` | Explicit exact retained output bytes; partial output is possible and must be assessed using its receipt |
| `cancel UUID [--json]` | Durable cancellation intent; pending is distinct from confirmed termination |
| `recover [--json]` | Read/reconcile current receipts for up to two seconds; never dispatches or replays commands |
| `stop [--json]` | Request all environment cleanup, fence execution, wait up to eight seconds for stopped evidence |
| `resolve UUID --note TEXT [--json]` | Interactive human resolution of an irreducible UNKNOWN after confirmed container stop; type the full operation ID |
| `reset [--json]` | Require stopped environments and reconciled outcomes, retain history, close the old generation and create a new binding generation |
| `/workbench-link` | Read-only current-profile status; no switching or fence resolution |

Exit codes: 0 for successful management, 2 for bad input/setup/authentication, 3 for unavailable or pending state. Status/doctor report ready only for a connected ACTIVE binding. `cancel` may return 3 while termination is pending. JSON is machine-readable; text requires no color.

## Normal shutdown

Run `hermes workbench-link stop` while both services remain available. Inspect the environment's `stop_evidence` in status. Cleanup closes its container, background jobs, persistent kernel and scratch; project edits remain. Ctrl-C then closes the foreground worker and broker. `reset` creates a new generation for further work; begin a new Hermes session so it does not reuse closed shell state.

The container watchdog also stops children on worker/lease loss. Its fifteen-second lease is failure control for trusted project execution, not protection against hostile code using the same container identity.

## Unknown outcomes

Preserve both private state directories. `recover` observes receipt-first uploads; reconnection does not remove a fence. A late immutable receipt may establish the original outcome without another shell execution.

If the worker crashed, restart it with the same project/state/image. It stops only its recorded, ownership-checked containers and reports historical stop evidence and receipts. It announces a new instance UUID.

For an operation still UNKNOWN, inspect the project with your own local tools, then use `resolve UUID --note 'Inspection findings'`. Resolution requires an interactive terminal and exact UUID confirmation. It records RESOLVED_UNKNOWN with no invented exit code; effects remain unknown. A model-facing tool cannot resolve it. `reset` remains necessary; if the worker instance changed, bind the newly announced exact identities after reset.

Cancellation and limits do not undo edits. An incomplete output receipt cannot be consumed as successful native file data. Output failures, conflicting receipts and uncertainty retain fences until explicit safe reset/reconciliation.

## Maintenance and limits

Control requests have three-second deadlines. Worker requests use verified TLS, fresh HMAC nonces and bounded response deadlines. Work capacity is bounded, with heartbeat/result/recovery admitted separately from normal work after parsing.

Each operation has a 16 MiB output limit, 4 MiB stdin limit and 600-second runner deadline. The runner has 128 PIDs, bounded CPU/memory and a 128 MiB scratch filesystem. Native background jobs belong to the environment; PTY/stdin interaction, foreground yield handoff and persist_on_release are outside this release. Hermes's non-local log/poll/wait/kill paths are supported.

Payload/stdin/output spools may contain project secrets. State is private (0700 directories, 0600 files), with a 512 MiB spool quota per service. There is no timed purge or encryption-at-rest claim. Archive quiescent, fully reconciled state deliberately before starting a fresh state directory; never discard unresolved evidence. No raw transport key or vendor credentials are stored in either ledger.

Updates require quiescent matching worker/plugin source. Schema 1 upgrades additively to schema 2; unknown schemas refuse startup. Removing plugin source does not erase durable state. Key rotation is a deliberate quiescent restart with a matching supplied key on both services.
