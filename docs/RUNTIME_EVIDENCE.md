# Runtime evidence — November 10, 2026

Version 0.1.0 supports one foreground Hermes CLI profile/environment and one explicitly selected Linux/Docker project worker. Persistent native code kernels, concurrent file-tool RPC and tracked background jobs now pass the real runtime checks. The earlier foreground-only checkpoint and its lifecycle failures are superseded by the results below.

## Source and environment

- Hermes v0.23.0, tagged source SHA `2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19`.
- Disposable runtime prepared through Hermes's supported `scripts/run-in-hermes-env` and package manager. No private core patches or raw dependency mutation.
- Hermes Python 3.14.9; standalone unit/worker/package checks on Python 3.11.17.
- Linux/WSL Ubuntu-26.04; Docker client/server 29.1.3.
- Runner base: `python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f`.
- Tested final local image: `sha256:3a2fd8b7fe768c3635f9e9b07f1e987b4816da03ce99b939b5cbca1c4c984095`.
- The image copies only package init, runner, protocol and errors. Its local immutable ID is not a published registry artifact. Fixtures, downloaded Hermes, runtimes and build outputs remain ignored.

These checks validate the working source following checkpoint `c2cbf7c`; the subsequent Git commit records the source and these results together. They are direct native runtime integrations without paid inference or a simulated model conversation.

## Native topology and results

`tests/integration/native_smoke.py` runs a profile broker and outbound project worker outside a separate Hermes server container. The server mounts disposable Hermes source/runtime read-only, test client/package source read-only, a private profile, server decoy and private control socket directory. Docker inspect verifies the exact mount set: **no selected project, Docker socket or server network**. Only the worker container mounts the selected project at `/workspace`.

Final native run `70460` exited 0:

| Check | Observed result |
|---|---|
| Native read/search/write/patch | Worker marker found, worker file created, subtraction patched to addition |
| Native terminal test | Actual `python test_maths.py` printed `PASS`, exit 0 |
| Persistent `execute_code` | First call printed 42; reused kernel printed 43 using retained variable |
| Concurrent kernel file RPC | Native `read_file` called from `hermes_tools`, returned WORKER; one tool call |
| Kernel reset | Old variable absent; fresh kernel reported reset |
| Background wait | Native process wait returned BACKGROUND and FINISHED |
| Background kill | TERM-ignoring job and descendants terminated; project effects stayed frozen |
| Unsupported persistence | `persist_on_release` refused before any new operation |
| Exact adapter stdin | Unicode, CRLF and final bytes without newline preserved |
| Shell state | Nested cwd and exported variable survived later calls |
| File extraction | Worker bytes and realpath correct; oversized transfer refused and destination absent |
| Real Hermes approval entry | Actual denial callback blocked dangerous command; operation list unchanged |
| Profile/environment scope | Separate real profile could not borrow binding; second environment refused without dispatch |
| Server-only path | Native file read failed instead of returning server marker |
| Environment closure | Confirmed container-stop evidence, then clean recreation |
| Native one-second timeout | Confirmed stop, reset generation, successful fresh environment |
| Disconnect | WORKER_UNAVAILABLE without a new operation or server fallback |
| Server decoy | All original hashes unchanged |

Representative native durations in this run: read 1743 ms, patch 1547 ms, write 670 ms, search 759 ms. Kernel calls took 2.16–4.62 seconds. These are local development observations, not latency guarantees; the harness stores only the most recent duration for repeated tool names.

Unchanged server decoy SHA-256:

```text
marker.txt     cc2ba4e05b99dce8c716a28386bef8a465189c862a5e6f0b89a703ad2ae168ba
maths.py       e1a894022d1a082987b87adecb623438c9e386d86b2b621cff4a5fe7fdf7edc8
test_maths.py  281c96d1db1ed7ef1d8997f4e6fa47720b985e7887095e68171f76aab3644e50
```

## Worker, durability and faults

Worker smoke `80222` exited 0 with exact input/output, writable selected-project effects, fixed mount/network/user/read-only-root policy, absent transport key in the command container, duplicate delivery and one operation identity. It also dropped the actual terminal HTTP acknowledgement after receipt commit: receipt recovery completed with exactly one counter effect. Operator inspect/recover/stop/reset/doctor passed; reset advanced the generation.

Fault suite `40212` and targeted runner-death run `70473` exited 0 on the final image:

| Case | Observed result |
|---|---|
| Foreground binary output | 2,097,152 exact bytes and matching receipt SHA-256 |
| Session binary output | Same exact 2,097,152 bytes and receipt hash |
| Output quota | 16,777,216 retained bytes; OUTPUT_LIMIT, incomplete output, confirmed cancellation and fence |
| Continuous inherited background output | Explicitly incomplete/cancelled and fenced; bounded cutoff never reported as successful file data |
| Explicit cancel | CANCELLED; stopped in 370 ms; effects frozen |
| Two-second timeout | CANCELLED; stopped in 2124 ms; effects frozen |
| Worker SIGKILL | UNKNOWN; stopped/fenced in 14875 ms; effects frozen |
| Runner SIGKILL | UNKNOWN; stopped/fenced in 16056 ms; effects frozen |
| Broker restart during execution | Recovered UNKNOWN, accepted late CANCELLED receipt; stopped in 439 ms; fence retained |
| Detached job after COMPLETED launch, worker death | Launch remains COMPLETED; environment stopped/fenced in 14998 ms; effects frozen |
| Detached job after COMPLETED launch, broker restart | Environment stopped/fenced in 729 ms; effects frozen |

Fresh operation IDs cannot bypass fault fences. Completed launch receipts remain historical facts while the independently owned session environment is stopped. Timing includes the broker's 15-second disconnect detection; container control EOF can terminate processes sooner. Cancellation does not undo project edits. The watchdog is failure control for trusted project execution, not a sandbox against hostile code under the same container user.

## Unit, transport and packaging checks

`dev/runtime/venv311/bin/python -W error::ResourceWarning -m unittest discover -s tests/unit -q` passed 35 tests in final run `5110` (1.693 seconds). The schema-1 regression preserves real historical receipts/output and fences an unresolved grant across migration and restart. Coverage includes strict encoding/HMAC/nonces, actual private sockets and ownership, grant/cancel races, pre-grant disconnect refusal, duplicate/conflicting identities/chunks/receipts, missing spools, output integrity, session restart/death fences, historical stop/reset/unknown resolution, additive schema migration, unknown-version refusal, quota/fsync failures and noninteractive resolver refusal.

Actual TLS socket tests verified trusted CA/hostname success, wrong hostname/untrusted CA rejection, and continued accepting while another client stalls its handshake. Work-capacity saturation leaves heartbeat capacity available. This is local transport evidence, not WAN deployment evidence.

Fresh standalone wheel installation `30359` passed imports from outside the checkout, worker console help and `pip check`. The rebuilt wheel SHA-256 is `78a0d1b2ca0f35a3a79e3a8c7c90167d5466637c6e2bd89b1037dcabfd61d6ca`. The wheel supplies the standalone worker/library; Hermes installs the directory plugin with its manifest and root entrypoint.

Current staged source passed Plugin Doctor `26673`: real discovery, manifest parsing, import and registration, zero replacement tools and one declared hook. Catalog validation `29718` passed manifest, declarations, capability probe, dependency, security and no-core-override checks. Its generic host-isolation note was reviewed: the README requires `in_process`, and actual host-mode discovery refuses explicitly.

Fresh dedicated-profile installation `50073` exited 0: directory discovery/enable, Doctor, native CLI help/status, missing-key AUTH_FAILED and host-isolation UNSUPPORTED_RUNTIME all passed. Registration/missing setup created no broker state. The profile started with clean plugin/configuration/key state and shared the supported dependency environment of an already installed disposable Hermes, matching the README setup prerequisite. This is separate from installing Hermes itself on a cold machine.

Staging only the plugin avoids recursive copies of this repository's ignored development runtime.

## Failures corrected and claim boundaries

The earlier native kernel lost its detached state, concurrent RPC was refused, and native scalar kill left descendants running. Session ownership, bounded request serialization, PID/start-time inventory and identity-checked process-tree termination now cover those public native seams. The final runner also tracks newly spawned group members during termination and rejects continuous inherited-pipe capture as incomplete.

The clean-home launcher originally inherited another home's activation sentinel and skipped setup. The harness now clears that sentinel, initializes through the supported package manager and kills its own setup process group before temporary-home cleanup on timeout. Full cold-home Hermes dependency initialization timed out at 240 seconds and again at 900 seconds (`10164`), before plugin enablement. Both remain failed cold Hermes setup rehearsals. The passing named-profile installation uses the documented prerequisite of an installed Hermes runtime; cold dependency-download behavior remains unverified.

Supported scope and unmeasured scenarios are explicit in [README.md](../README.md) and [VALIDATION.md](VALIDATION.md). There is no physical two-machine/WAN, other-OS, gateway multiplexing/delegated workspace isolation, PTY/background stdin or jobs surviving environment closure claim. No live-model conversation, catalog publication, demo submission or adoption result is claimed by these tests.
