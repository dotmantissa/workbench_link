# Release verification

Version 0.1.0 runtime source was verified at commit [`27dc435`](https://github.com/dotmantissa/workbench_link/commit/27dc435f7ed4306f10ab63dafd9fe979f4920e9e) on November 10, 2026. The repository layout and documentation changes preserve that runtime source. These results cover one foreground Hermes CLI profile/environment and one Linux/Docker project worker.

## Environment

| Component | Tested version |
|---|---|
| Hermes | v0.23.0, `2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19` |
| Python | Hermes 3.14.9; standalone tests/worker 3.11.17 |
| Host | Ubuntu 26.04 under WSL |
| Docker | Client/server 29.1.3 |
| Runner base | `python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f` |
| Local image | `sha256:3a2fd8b7fe768c3635f9e9b07f1e987b4816da03ce99b939b5cbca1c4c984095` |

Hermes was prepared through its supported package manager in an isolated runtime. Tests dispatched real native tools directly; no model inference was used. The image ID identifies a locally built artifact, not a published registry image.

## Native integration

The Hermes server ran in a separate container with a decoy project and private control socket. Its exact mount set excluded the worker project and Docker socket, and its network was disabled. The worker alone mounted the selected project at `/workspace`.

| Behavior | Observed result |
|---|---|
| Read, write, search and patch | Worker marker returned; file created; subtraction bug fixed |
| Terminal test | Actual project test printed PASS with exit 0 |
| Persistent code | Variable retained across calls; kernel reused |
| Kernel tool RPC | Native read_file returned worker content; one tool call |
| Kernel reset | Previous variable absent in fresh kernel |
| Background wait/kill | Output collected; TERM-ignoring descendants stopped; effects frozen |
| Shell and stdin | Cwd/export persisted; Unicode, CRLF and no-final-newline input exact |
| File extraction | Bytes/realpath correct; oversized transfer refused |
| Approval denial | Normal Hermes denial callback blocked command with zero new operations |
| Profile/environment isolation | Separate profile could not borrow binding; second environment refused |
| Server-only path | Failed without host fallback |
| Timeout and closure | Confirmed stop, generation reset and clean recreation |
| Disconnect | WORKER_UNAVAILABLE with no new dispatch or fallback |
| Server decoy | All original file hashes unchanged |

The native read took 1743 ms and patch 1547 ms in this local run; kernel calls took 2.16–4.62 seconds. These are development observations, not latency guarantees.

## Fault and durability checks

Worker smoke verified exact bytes, mount/user/network policy, absent transport key, duplicate delivery and operator inspect/recover/stop/reset/doctor. Dropping the actual HTTP acknowledgement after receipt commit recovered the same receipt with exactly one counter effect.

| Fault | Result |
|---|---|
| Foreground and session binary output | Both returned 2,097,152 exact bytes with matching receipt hash |
| Output limit | 16,777,216 retained bytes; incomplete OUTPUT_LIMIT cancellation and fence |
| Continuous inherited-pipe output | Explicitly incomplete/cancelled; no truncated success |
| Cancel | Confirmed CANCELLED; effects frozen; stopped in 370 ms |
| Two-second timeout | Confirmed CANCELLED; effects frozen; stopped in 2124 ms |
| Worker / runner SIGKILL | UNKNOWN and fenced; effects frozen in 14875 / 16056 ms |
| Broker restart during execution | Late CANCELLED receipt accepted; fence retained; stopped in 439 ms |
| Detached job after completed launch, worker death | Historical completion preserved; environment stopped/fenced in 14998 ms |
| Detached job after completed launch, broker restart | Environment stopped/fenced in 729 ms |

All eleven cases passed. Fresh operation IDs could not bypass fences. Disconnect timing includes the fifteen-second detection interval; control EOF can stop children sooner. Cancellation does not undo edits.

## Unit, transport and installation

All 35 unit/socket tests passed with ResourceWarnings treated as errors. Coverage includes schemas/HMAC/nonces, actual private and TLS sockets, grant/cancel races, duplicate/conflicting chunks/receipts, missing spools, output integrity, restart/session fences, historical stop/unknown resolution, schema-1 migration preserving real history, unknown-version refusal and quota/fsync failures.

TLS checks accepted a trusted certificate and rejected wrong-host/untrusted certificates. A stalled handshake did not block another connection, and saturated work capacity left heartbeats available.

A fresh standalone wheel install passed imports outside the checkout, worker console help and dependency checks. Plugin Doctor and catalog validation passed real discovery, declarations, security scanning and no-core-override checks. The generic validator isolation note was assessed against the required in_process configuration and explicit host-mode refusal.

Fresh named-profile installation passed enablement, Doctor, CLI help/status, missing-key refusal and unsupported host isolation without starting broker state. It used an already installed supported Hermes runtime, matching the documented prerequisite.

Repository packaging checks were repeated after the layout cleanup: all 35 tests passed on both Python 3.11 and 3.14, wheel/source distributions built successfully, and the extracted source distribution passed Plugin Doctor and catalog validation. The source archive contains the manifest, directory entrypoint, Docker files, docs and tests, with no development runtime or private state. Clean-profile installation passed again. Docker smoke and all eleven fault cases passed on the rebuilt image `sha256:19cdc9008e0d8343b1b91143f6866949955bc969bd8049ab7d60dadafb54cb10` with Python 3.14. The runtime source is unchanged.

## Limits of the evidence

Cold full-home Hermes dependency setup timed out before plugin enablement at 240 and 900 seconds. That is separate from the passing plugin installation into an installed Hermes profile.

Physical WAN/NAT behavior, other worker platforms, gateway multiplexing, delegated environment isolation, PTY/background stdin and jobs surviving environment closure have not been verified. No live-model conversation is represented by these tests. Further crash-window barriers, adversarial path races, slow-reader backpressure and exhaustive storage-failure permutations remain additional reliability work.

Use the commands in [testing](testing.md) to reproduce the implemented suites. [Architecture](architecture.md) and [protocol](protocol.md) define the ownership and recovery boundaries.
