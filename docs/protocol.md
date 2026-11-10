# Protocol and durable state contract

The implemented wire protocol is version 1 with explicit optional session extensions. Ledger schema is version 2. Plugin/Hermes versions are independent. Both services share [protocol.py](../workbench_link/protocol.py); unsupported fields and mismatched required behavior fail closed.

## Encoding and identities

Canonical UTF-8 JSON uses sorted keys, compact separators, no duplicate keys or nonfinite numbers. Integers reject booleans. UUIDs are canonical lowercase strings; worker/project aliases are bounded ASCII slugs. Base64 is canonical and checked before allocation. Limits: 256 KiB script, 4 MiB stdin, 64 KiB output chunk, 16 MiB operation output, 6 MiB wire/control frame and 600 seconds per runner operation.

The immutable envelope requires:

```text
protocol_version, profile_id, binding_id, generation, environment_id,
operation_id, worker_id, worker_instance_id, project_id,
script, login, stdin_b64, timeout_seconds, payload_sha256
```

`payload_sha256` hashes canonical JSON of every envelope field except the digest itself. Retries retain all IDs, payload and hash. Reusing an operation ID with a different payload fences the original binding. Normal scripts are native BaseEnvironment-wrapped commands, stored in private container scratch and executed through fixed Bash argv. Runner control and command stdin are separate pipes. Neither broker nor worker executes user shell on the host.

Optional `lifecycle` is `operation` (default) or `session`. Operation mode requires all command descendants stopped before completion. The native adapter uses session mode: detached processes belong to the environment and may outlive a foreground call.

Optional `terminate_process: {pid, start_ticks}` is session-only. The pinned native scalar kill and kernel teardown forms map to this identity-checked container tree-control operation. The original script remains part of the durable audit hash; runner control terminates the recorded process tree rather than killing only its shell wrapper or a recycled PID. TERM targets the parent first; KILL includes its private launch group to catch children spawned during grace. Other native commands use the normal shell path.

## Worker API and authentication

Only POST under `/v1/worker/` is accepted:

| Endpoint | Effect |
|---|---|
| `hello` | Immutable instance/project/image/capability registration |
| `heartbeat` | Binding/generation/active operation renewal, cancel and close requests |
| `poll` | Zero/one queued envelope plus matching binding and close requests |
| `accept` | Durable idempotent start grant, with a five-second launch window |
| `running` | Launch report for the original grant |
| `output` | Contiguous chunk commit and acknowledgement |
| `result` | Verified immutable terminal receipt acknowledgement |
| `recover` | At most 32 historical operation states; no execution |
| `environment_stopped` | Historical instance/generation container-stop evidence |

The worker persists ACCEPTED, GRANTED and LAUNCHING before launch. Anything already LAUNCHING/RUNNING/UNKNOWN is never automatically spawned again. Terminal output/receipts are uploaded with the historical instance identity before new registration on restart. A lost receipt acknowledgement retries the same receipt, not the command.

HMAC-SHA256 signs this ASCII string, with newlines and no trailing newline:

```text
WBL1
POST
EXACT_PATH
UNIX_TIMESTAMP
NONCE
WORKER_ID
WORKER_INSTANCE_UUID
SHA256_OF_RAW_BODY
```

Headers: `X-WBL-Version`, `X-WBL-Worker`, `X-WBL-Instance`, `X-WBL-Time`, `X-WBL-Nonce`, `X-WBL-Body-SHA256`, `X-WBL-Signature`. Keys are deliberately supplied canonical lowercase hex encoding 32–128 bytes. Validate configured worker, exact path, ±30-second clock tolerance, body digest and constant-time signature before consuming the nonce. Nonces persist for 120 seconds with a 4096-entry cap. Retries use fresh nonces.

HTTP 400 reports malformed/oversized requests, 401 authentication failure, 409 conflicts/fences, 429 capacity, and 503 storage unavailability. Redirects and chunked requests are refused. Request handlers, body reads and responses are bounded. TLS handshakes run in bounded handlers rather than blocking the accept loop. Non-loopback transport requires verified HTTPS; plain HTTP requires explicit loopback local-test mode. HMAC is peer authentication, not command approval; Hermes's normal policy still applies.

## Private control

Profile-owned 0700 directory, 0600 Unix socket and Linux peer-UID checks. Frames use a four-byte unsigned network-order length then canonical JSON, with a three-second deadline. No TCP admin fallback exists.

Actions: `status`, `bind`, `open_environment`, `submit`, `operation_status`, `read_output`, `cancel`, `close_environment`, `recover`, `stop`, `resolve_unknown`, `reset`. Worker HTTP cannot perform these operator actions. The same-user host/operator is trusted; model project commands have no broker socket mount.

## Operations and receipts

Broker states are QUEUED → START_GRANTED → RUNNING → COMPLETED/CANCELLED, with NOT_STARTED permitted before a grant. Missing launch/termination proof produces UNKNOWN. A matching late receipt can resolve UNKNOWN to a known terminal state without replay, while its fence remains. Human reconciliation records RESOLVED_UNKNOWN with no success exit code. Worker states are ACCEPTED → GRANTED → LAUNCHING → RUNNING → TERMINAL → ACKNOWLEDGED.

Chunks have sequence starting at zero, contiguous byte offset, canonical base64 and SHA-256. Exact duplicates acknowledge; conflicts fence. Spools publish by fsync/atomic rename before database references. A receipt requires all chunks and a verified final digest/count. Range reads verify selected chunks; final receipt verification covers all bytes. Missing spools never trigger command replay.

Required receipt fields:

```text
operation_id, payload_sha256, binding_id, generation, worker_instance_id,
start_grant_id, terminal_kind, exit_code, output_bytes, output_sha256,
last_sequence, termination_confirmed, termination_method,
output_complete, error_code, worker_elapsed_ms
```

`terminal_kind` is completed/cancelled/not_started. Completed includes the actual foreground exit code, including shell failures. Other kinds have a null exit code. Zero output requires SHA-256 of empty bytes and sequence -1. Incomplete output requires an error and is never successful file data.

Optional `termination_scope` defaults to environment. Session receipts must declare it explicitly. A completed foreground receipt uses `foreground` plus mandatory `detached_processes: [{pid, start_ticks}, …]`. It proves foreground capture/termination only. Background output lives in native job logs and is retrieved by subsequent operations. Cancellation uses environment scope with no surviving processes. Scope cannot be weakened for an operation-mode envelope.

The broker records potential session ownership at grant time, before launch. Therefore a lost receipt cannot hide detached work. Process inventory snapshots and worker container inventory are durable. The container remains the final ownership/cleanup boundary, including processes created after a snapshot.

## Environment lifecycle and fences

One OPEN/CLOSING environment is admitted per profile. Session close enters CLOSING until `environment_stopped` matches the exact environment/binding/generation/worker instance and confirms `container_stop`. Only then is the environment CLOSED with empty live inventory. Stopped evidence does not undo project effects or invent an operation receipt.

Broker restart and lease loss fence every potentially live session environment even if its foreground launch is COMPLETED. Unknown operation history remains. Late receipts/stopped evidence cannot reopen the environment or clear the fence. Stop fences execution; reset requires no unresolved operations and no live/pending session environments, retains the closed-generation tombstone and creates a new generation. Replayed old generations cannot execute.

Worker/container lease is fifteen seconds. The PID-1 runner stops children on renewal loss/control EOF; worker restart checks only recorded container names and ownership, then confirms stopped state. Cancellation escalates TERM/KILL and container-stop fallback. This watchdog is failure control for trusted code, not an adversarial boundary against same-user container code.

Human resolution requires UNKNOWN, confirmed stopped environment, a nonsecret note and exact operation confirmation. The CLI refuses noninteractive resolution. History remains unknown; reset authorizes future distinct commands, never replay.

## Storage

SQLite uses WAL, FULL synchronization, foreign keys and serialized writer transactions. Broker tables: meta, registrations, bindings, environments, operations, output_chunks, nonces, records and events. Environment schema 2 adds session_owned, inventory_json and stop_json. Schema 1 reopens additively; unknown schemas refuse startup.

Each service uses private local filesystem state and a 512 MiB spool quota. Referenced data cannot be regenerated. Payloads/stdin/output remain retained until deliberate quiescent operator maintenance; timed deletion/purge is outside version 0.1.0. Neither ledger stores the transport key. No encryption-at-rest or exactly-once effect guarantee is claimed.
