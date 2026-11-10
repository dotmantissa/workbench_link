# Validation, evidence and release gates

The supported release checks now have measured results in [RUNTIME_EVIDENCE.md](RUNTIME_EVIDENCE.md): 35 unit/socket tests, eleven Docker fault cases, worker smoke, isolated native Hermes routing and fresh standalone wheel installation pass on the final source/image. Clean dedicated-profile directory installation, Plugin Doctor and catalog validation also pass. Full cold-home Hermes dependency setup timed out before plugin enablement; the documented prerequisite is an installed Hermes runtime.

The matrix below defines acceptance scenarios, including future coverage. It is not a claim that every permutation has been exercised. Local trusted-CA/hostname and capacity checks passed; physical WAN/NAT, other operating systems, gateway/delegated workspace isolation, PTY and jobs surviving environment release remain outside version 0.1.0. A live-model agent conversation has not been run. Additional crash-window barriers, adversarial path races, slow-output backpressure and exhaustive disk/SQLite failure permutations remain extended reliability work. Match tests to failure consequences and do not infer functional success from document lint, source inspection or mocked registration.

## 1. Test topology on the available local machine

Use one Linux machine with Docker if its prerequisite check succeeds:

- **Server environment:** disposable Hermes v0.23.0 container and separately running broker process. Plugin source read-only; decoy project only; no worker project or Docker socket mounted.
- **Local worker:** host process with explicitly selected small project and private state. Docker CLI permitted only to trusted worker/test orchestrator.
- **Project environment:** worker-created bounded container mounting selected fixture at `/workspace`. Distinct filesystem from server decoy.
- **Connection:** worker outbound requests to broker port published on literal loopback; no public listener/remote machine needed.
- **Fault controller:** deterministic local proxy/test hooks for drop/delay/duplicate/ack-loss cases, restricted to the test topology. Never a production approval bypass or self-updater.

Test source paths only under this project/scoped temporary directories. No broad home search, restricted-directory traversal or unrelated-project access. Tests label their containers with unique run IDs and clean only those IDs.

If Docker is absent/unavailable, record prerequisite failure and finish code/unit work independently; do not pretend container/runtime validation passed. Installing system prerequisites is a separate concrete implementation decision, not automatic source-document behavior.

## 2. Native runtime without depending on paid inference

Registration tests use real PluginManager discovery/doctor in an isolated HERMES_HOME. Tool workflow tests use the real agent/tool/approval pipeline with either an explicitly configured available model or a deterministic local OpenAI-compatible model fixture that emits correctly shaped native tool requests. The latter scripts model responses only; it does not mock provider registration, tool execution, approval or file behavior.

Validate the fixture transport against the released Hermes provider interface before relying on it. Derive tool schemas from the runtime; do not guess arguments. Document the fixture when reporting results. An interactive approval test supplies an actual denial through the normal approval UI/policy harness; it never auto-approves or disables guards.

For the final demo, use a real available model if one is explicitly configured through Hermes. Do not inspect credential stores, silently spend credits, or fabricate an agent run. If inference remains unavailable, report deterministic runtime integration separately from a live-model demonstration.

## 3. Release matrix

| ID | Scenario | Required observable evidence |
|---|---|---|
| N01 | native discovery/doctor | actual plugin loads, exact surfaces, zero register-time process/network work |
| N02 | provider-host isolation unsupported | clear refusal before worker/container creation |
| N03 | native read/search | worker marker found; server marker not returned |
| N04 | native write/patch | worker byte/hash changes; server decoy unchanged |
| N05 | terminal tests | actual worker test suite output/exit; decoy test remains different |
| N06 | execute_code | native wrapper/probes execute in worker environment |
| N07 | normal approval denial | zero broker acceptance/start grant/worker spawn for denied command |
| N08 | cwd/env | cd/export persist; relative file tools agree on cwd |
| N09 | exact stdin | Unicode, trailing/no newline and bounded payload hash agree |
| N10 | foreground output | contiguous stream, actual returncode and cwd markers retained correctly |
| N11 | native timeout/stop | requested/confirmed termination distinguished; descendants gone or container stopped |
| N12 | background/yield | supported lifecycle or verified refusal; no orphan path |
| N13 | explicit fetch/spill | byte/hash correct; missing/oversized transfer fails clearly |
| N14 | host-looking upload path | absent worker path errors; no server read fallback |
| N15 | prompt/Python probe | server facts not substituted; no premature command dispatch |
| N16 | profile isolation | separate settings/data/binding; slash command scope accurate |
| N17 | simultaneous task/environment | busy refusal without overlapping project writes |
| N18 | core retry/recreation | persistent fence blocks fresh IDs and new environments |
| R01 | disconnect before start grant | provable no-start; no later silent execution |
| R02 | disconnect after effect before receipt | unknown fence; filesystem effect counted once |
| R03 | lost terminal acknowledgement | recovered same receipt, no repeat command |
| R04 | broker restart | ledger recovered, unresolved work fenced before grants |
| R05 | worker SIGKILL | watchdog/container cleanup within deadline; no old-instance reexecution |
| R06 | runner death | accurate exit/unknown evidence, no false completion |
| R07 | container replacement | binding stale/recreated state and lost scratch reported |
| R08 | cancel versus natural exit | real receipt wins; cancel request alone not termination |
| R09 | duplicate/conflicting operation | same ID/hash dedup; conflicting hash refused/fenced |
| R10 | duplicate/reordered/corrupt chunks | contiguous verified data or explicit integrity failure |
| R11 | full disk/spool/queue | bounded refusal/termination, no memory-only durability downgrade |
| R12 | migration/version mismatch | safe transactional read/update or clear refusal, preserved history |
| S01 | wrong key/body/path/nonce/time | rejected before grant/state mutation |
| S02 | worker API tries operator action | no exposed route and no private-socket authority |
| S03 | mount/secret policy | selected mount only; no transport token, host home, Docker socket or worker state |
| S04 | URL/redirect rules | external HTTP/redirect/userinfo rejected; TLS verification retained |
| S05 | stale instance/generation | old grant cannot start current work or clear fences |
| S06 | output disclosure/logging | no keys/HMAC/stdin in default logs; explicit output access only |
| O01 | clean setup | fresh operator follows README/CLI successfully without frontend |
| O02 | missing prerequisites/config | actionable bounded error, no silent installation/startup |
| O03 | unknown recovery | recover reads receipt only; human resolve preserves unknown history |
| O04 | graceful shutdown | bounded process cleanup and durable unresolved state |
| C01 | doctor/catalog validation | actual commands exit 0 with warnings reviewed |

Any failure in N03–N07, N18, R02/R03/R05, S02/S03 or C01 blocks the claimed competitive minimum. Do not average those failures into a passing score.

## 4. Fixtures and falsifiable assertions

**Project:** tiny Python project with one deterministic bug and unittest suite, initially failing. Native patch fixes the function; test passes. A separate server decoy has different marker text and a deliberately different failing case. Store before/after file hashes and actual test returncodes.

**Side-effect counter:** operation appends one unique line and flushes/fsyncs, then waits at a fault barrier before producing a receipt. Drop connection/kill a process after the append. After recovery, counter contains exactly one occurrence and the same unresolved/receipt identity. A second user command while fenced produces no new append. This tests the dangerous crash window, rather than claiming all shell effects are transactional.

**Process tree:** bash launches a child and grandchild that ignore TERM. Cancel/timeout/worker death must remove them or confirm their entire container stopped. Do not test only a sleeping parent PID. Report lease/kill grace elapsed time and any unconfirmed state honestly.

**Bytes:** generated UTF-8 text with Unicode, CRLF, no final newline and split multibyte output boundaries; native write/read/patch hashes must agree. Native textual tools may have documented decoding semantics; measure against those semantics, not a binary capability they never offered.

**Paths:** explicit project names/relative paths with spaces, nested cwd and symlink pointing to an unmounted external host path. It must not reveal that host file. Container-internal symlinks to its own readable system files are not a promised denial boundary. Race-safe selected-root validation is tested; no broad local scan is performed.

**Limits:** command/stdin/output just below/at/above bounds, incremental chunk retry, paused reader, full local spool and SQLite commit failure. Large full-fidelity file data must fail explicitly rather than be truncated into a successful patch result.

## 5. Unit tests with independent value

Test state-machine transitions across crash/cancel/grant races, credential signing tamper/replay, canonical encoding edge cases, generation/identity validation, private framing limits and retention preserving active dedup tombstones. Table-driven tests compare externally specified outcomes, not private method names or implementation line counts.

Use temporary owner-only directories and no credentials. Property-style generated cases may use stdlib deterministic randomized inputs; do not add a heavyweight test dependency solely for coverage. If extra test tooling is justified, pin it and keep it separate from plugin runtime requirements.

## 6. Verification commands after code exists

Implemented commands:

```sh
python -W error::ResourceWarning -m unittest discover -s tests/unit -q
python tests/integration/worker_smoke.py --image sha256:INSPECTED_IMAGE_ID
python tests/integration/worker_faults.py --image sha256:INSPECTED_IMAGE_ID
hermes plugins doctor /absolute/path/to/plugin --ci
hermes plugins validate /absolute/path/to/plugin --install-deps
```

Run `tests/integration/native_smoke.py --hermes-source dev/hermes --image sha256:INSPECTED_IMAGE_ID` and `tests/integration/install_smoke.py --hermes-source dev/hermes` through the supported disposable Hermes runtime; see [README.md](../README.md) for its environment invocation. These tests use isolated profiles and never rewrite the user's main HERMES_HOME.

## 7. Evidence record

For each important integration run save: run ID, full plugin/Hermes commit, OS/Python/Docker/image versions, exact topology/mounts, command invocation, case IDs, actual exit results, marker/counter hashes, measured delays, known failures and cleanup result. Evidence must identify deterministic model fixtures versus real-model runs.

Keep redacted summaries in `evidence/`; raw state/output remains ignored/private. Inspect a support artifact before sharing because command output may include project data despite token redaction. Do not store sensitive values in TASKS.md or test fixture goldens.

## 8. Remote and platform claim boundaries

Local isolated testing is valid functional evidence. It does not establish real NAT/public reverse-proxy TLS, WAN throughput, roaming, laptop suspend/resume behavior on another OS or operation across separate physical machines. A future remote rehearsal uses the same pinned source and repeats N03–N07, R02/R03/R05 and S04 with actual host/worker separation. Until then README/demo label the topology plainly.

## 9. Packaging and catalog review

Check manifest version/name/floor/declarations against runtime and package metadata; no bare third-party dependency floors because minimum has none. Scan source tree for committed `.pyc`, binaries, archives, generated env/runtime files and unreviewable payloads. Official image setup is explicit/source-pinned and disclosed.

Catalog disclosure names network, selected project access, Docker CLI, background processes, stored spools/receipts and no telemetry. Full SHA pins are real and match validated code. Doctor/catalog warnings about documented subclass imports are reviewed, not suppressed. No private-core override, auto-approval, credential-file read or self-update is acceptable.

## 10. Judge-facing result

Usefulness: one native read/edit/test workflow, compared honestly with core SSH and custom device tools. Reliability: receipts, real denial and failure/recovery evidence. Polish: fresh setup/status/error clarity and small demonstration. Creativity: a coherent native workspace link rather than a prompt-only recipe. There are no published rubric weights or defensible winning probabilities; evaluate the functioning entry against these outcomes.
