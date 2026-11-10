# Runtime evidence — November 10, 2026

This is a verified foreground implementation checkpoint. It is not a full release: the original native matrix includes persistent `execute_code` and background lifecycle support, and those contracts remain unresolved.

## Source and environment

- Hermes v0.23.0, full tagged source SHA `2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19`.
- Disposable installation prepared through Hermes's `scripts/run-in-hermes-env` / package-manager workflow, with state and runtime isolated under this project's ignored `dev/` tree. No private core patches or raw dependency mutation.
- Hermes's supported Python 3.14.9 runtime; standalone worker/unit suite also exercised with Python 3.11.17.
- Linux/WSL Ubuntu-26.04; Docker client/server 29.1.3. Tests use the authorized user's fresh Docker group context.
- Official runner base: `python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f`.
- Final tested local image ID: `sha256:88dbbcbbb780e3d0f98b2ec2aa49ed9aaae466a87ab2a56d0566aaf5ed56251d`.
- Runner source, protocol and errors are copied into the image. Build outputs and fixture state remain ignored. An image ID is a local immutable identity, not a published registry artifact.

## Native topology and results

`tests/integration/native_smoke.py` starts a profile broker and outbound project worker on the local machine. A separate Hermes server container mounts only the disposable Hermes source/runtime (read-only), test client/package source (read-only), its profile, its server decoy and the private control socket directory. Docker inspect verifies the exact mount set: **no selected-project mount, no Docker socket, and no server network**. The worker container alone mounts the selected project at `/workspace`.

The server and worker fixture each contain `marker.txt`, `maths.py` and `test_maths.py`. The server marker is `SERVER`; the worker marker is `WORKER`. Actual `model_tools.handle_function_call` dispatch through real plugin discovery demonstrated:

| Check | Observed result |
|---|---|
| Native `read_file` | `WORKER` content |
| Native `patch` | Changed `return a - b` to `return a + b` in the worker |
| Native `terminal` | `python test_maths.py` returned `PASS`, exit 0 |
| Native `write_file` | Created and verified worker `created.txt` |
| Native `search_files` | Found worker content at `/workspace/created.txt` |
| Exact adapter stdin | Unicode, CRLF and final bytes without a newline preserved |
| Shell snapshot | `/workspace/nested` cwd and an exported variable survived later calls |
| File extraction | `fetch_file` bytes and `fetch_realpath` matched the worker |
| Real Hermes approval entry | Denial callback returned blocked; operation list unchanged |
| Unsupported native calls | `execute_code`, explicit background and trailing `&` refused by the public pre-tool hook before dispatch |
| Disconnected worker | Real terminal call returned `WORKER_UNAVAILABLE`; operation list unchanged; neither marker changed |
| Server decoy | All three original hashes unchanged |

Measured local elapsed times in the isolated server run: read 1556 ms, patch 1268 ms, foreground test 263 ms, write 671 ms, search 756 ms. These are one development observation, not latency guarantees.

Unchanged decoy SHA-256 values:

```text
marker.txt     cc2ba4e05b99dce8c716a28386bef8a465189c862a5e6f0b89a703ad2ae168ba
maths.py       e1a894022d1a082987b87adecb623438c9e386d86b2b621cff4a5fe7fdf7edc8
test_maths.py  281c96d1db1ed7ef1d8997f4e6fa47720b985e7887095e68171f76aab3644e50
```

## Worker, durability and fault evidence

`tests/integration/worker_smoke.py` proved exact input/output, writable selected-project effects, fixed Docker isolation settings, absent worker credential in the command container and duplicate operation delivery with one ledger identity.

`tests/integration/worker_faults.py` uses actual subprocess workers and Docker containers:

| Fault/check | Result in final worker-code run |
|---|---|
| Binary output across many chunks | All 2,097,152 bytes matched; receipt SHA-256 verified |
| Explicit cancellation | `CANCELLED`, termination confirmed, stopped in 535 ms; project effects frozen |
| Two-second runner timeout | `CANCELLED`, stopped in 2134 ms; effects frozen |
| Worker SIGKILL | Container stopped and broker operation `UNKNOWN` in 14982 ms; effects frozen; fresh-ID dispatch fenced |
| Broker restart during execution | Initially recovered `UNKNOWN`; late `CANCELLED` receipt accepted, stopped in 579 ms; binding fence retained |

The suite checks stopped container evidence and stable project effects after each fault. Worker-death timing includes the broker's 15-second detection interval; container control EOF may stop children sooner. The watchdog protects against loss of the daemon/lease in this tested topology. It is not a sandbox against malicious same-user code.

The 24 unit/socket tests additionally cover strict codec/HMAC/nonces, actual private socket framing/ownership, grant/cancellation races, conflicting identities/output, missing spools, receipt integrity, restart fences, and the runner-close/heartbeat race. Repeated unconfirmed cleanup stays unconfirmed.

## Validation and remaining gate

Hermes `plugins doctor <staged-source> --ci` passed real discovery/import/registration. `plugins validate <staged-source> --install-deps` passed manifest, registered declarations, security scanning and no-core-override checks. A preliminary private-import warning for `EnvironmentConnectionError` was removed by using this plugin's `LinkError`. The native environment requires `plugins.isolation: in_process`; plugin-host execution is explicitly refused.

Staging only plugin source was necessary because Doctor refuses recursive copies when its scratch directory is inside the plugin repository. Downloaded Hermes, runtime, state, credentials and the recovery checklist were excluded.

The initial real `execute_code` attempt failed: Hermes v0.23.0 launches a detached persistent kernel, then concurrently polls/ships file-RPC through `env.execute()`. This runner terminates descendants before a foreground receipt and admits one active operation per environment. The detached kernel lost its scratch state, and the concurrent RPC call received a busy refusal. This is a demonstrated public-contract mismatch, not a passing native-code result. The public pre-tool hook now refuses that unsupported path before any operation.

Before a full release: resolve that persistent-process/concurrent-control contract, implement human fence recovery/reset, test profile/delegation behavior, exercise remote TLS and capacity/output-quota failures, rehearse a clean installation, and complete the remaining matrix in [VALIDATION.md](VALIDATION.md). No physical two-machine run, catalog publication, demo submission or adoption result is claimed.
