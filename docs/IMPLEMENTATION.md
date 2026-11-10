# Ordered implementation checklist

Execute in dependency order. Each item states what to build and the evidence needed to mark it complete in the ignored root TASKS.md. The November 10 foreground checkpoint has real broker/worker, native routing and fault evidence in [RUNTIME_EVIDENCE.md](RUNTIME_EVIDENCE.md). Phase 0's full exit remains open because persistent `execute_code` and background lifecycle are unsupported. Estimated effort is provisional; availability is unknown.

## Phase 0 — establish the native premise (first focused checkpoint)

**Dependency:** architecture and selected public seam. **Budget checkpoint:** roughly three focused hours; investigate the riskiest interfaces first rather than scaffold every module.

1. Read root TASKS.md, inspect Git status and existing files. Record actual machine OS, Python and Docker versions. Probe Docker deliberately; do not auto-install or claim it is available. Keep fixtures under this project or scoped temporary directories; exclude restricted/unrelated directories.
2. Obtain a disposable v0.23.0 Hermes checkout in `dev/` or a dedicated temporary directory; resolve and record its full commit SHA. Read its local instruction files. Prepare Hermes through its supported installation/dependency workflow, not by altering an existing user profile. Record any long-running operation/session ID in TASKS before yielding.
3. Create a minimal native manifest/entrypoint/provider with exact public registration and classifications. Confirm `hermes plugins doctor <plugin-path> --ci` from the disposable install. Registration performs no command/network startup. Refuse plugin-host isolation explicitly.
4. Create a tiny selected fixture and a separate server decoy with the same relative filenames but different marker content. The server container has no mount of the selected project or Docker socket. Record mount inspection as evidence of this distinction.
5. Implement the smallest supported `_run_bash`/pipe-handle adapter against a local worker transport, using the final direction of identity/authentication rather than an unauthenticated general execution API. In the spike, short commands only; do not call a synchronous stub a complete backend.
6. Invoke actual registered native `read_file`, `patch` and `terminal` test commands through real Hermes runtime, not only `env.execute()`. Run `execute_code`, `write_file` and `search_files` smoke calls too. Worker markers change as expected; server markers/hashes do not.
7. Exercise the real approval-policy entry: deny a dangerous command through Hermes. Assert the operation never appears in broker/worker acceptance or launch records. Do not create a second custom approval prompt to make this pass.
8. Disconnect transport before dispatch and after worker launch. Verify zero server fallback, an explicit missing/uncertain result, and no automatic replay. Source-inspect and test core recreation with the persistent fence.
9. Probe stdout drain, no-newline stdin, timeout, stop and native background/yield paths. Establish which subclass hooks core actually invokes. An incomplete lifecycle prevents a full native-workflow claim.
10. Save a short evidence report: source version, topology, exact calls, marker hashes, failures, unresolved contracts and measured elapsed times. Commit no generated credentials, state or TASKS.md.

**Exit:** native registration/routing/approval/identity are demonstrated, or a specific failing public contract is recorded. If the premise fails, stop the full build and resolve the public seam or reassess direction. Do not spend the deadline polishing custom tools that abandon the native-workflow differentiator.

## Phase 1 — source package, settings and schema foundation

**Dependency:** Phase 0 premise holds.

1. Establish relative plugin imports and standalone worker imports. Add pyproject metadata for the source package, Python floor and zero plugin runtime dependencies. Omit a duplicate entry point if directory registration is canonical. Separate historical `research/collect.py` dependencies from plugin requirements.
2. Add `errors.py`: stable code enum and structured safe exceptions. Distinguish normal shell failure, definite no-start, connection unavailable, unknown effects, cancellation pending, stale binding, integrity failure and unsupported runtime.
3. Add immutable settings validation: worker ID, project alias, supported timeout/resource bounds, control directory and secret mapping. Read host keys through get_secret in active profile context. Pass captured values explicitly into adapter/broker startup; do not use a global unscoped token cache.
4. Implement canonical protocol codec and every field validator from PROTOCOL.md. Reject duplicates, invalid integer types, unknown required fields, oversize base64 before decoding and malformed IDs. Verify codec round trips on bytes, Unicode and newline-free stdin.
5. Define ledger schema version 1 and transaction migrations. Build store APIs around state transitions, not arbitrary SQL from command handlers. Use unique keys, foreign keys, full synchronization, private directories and atomic spool publication.
6. Implement HMAC signing/verification and nonce dedup. Test valid requests, invalid body/path/identity, stale/future times, reused nonce and retries with new nonce. Raw key never appears in exception objects or log context.
7. Finalize plugin.yaml declarations against actual runtime registration. Keep backend ID `workbench_link`, plugin ID `workbench-link`, settings secret env `WORKBENCH_LINK_TOKEN`. Test missing token permits management guidance while execution remains unavailable.

**Exit:** codec/auth/ledger invariants pass meaningful unit tests; plugin loads through doctor without starting services; standalone worker import does not load Hermes.

## Phase 2 — broker and private control plane

**Dependency:** Phase 1 schemas/storage/auth.

1. Implement explicit broker startup from registered Hermes CLI. Resolve profile data through plugin_data_dir, lock ownership and reject a second broker for that profile. Create owner-only Unix socket with peer-UID checks. Refuse stale socket takeover until prior PID/socket owner is checked safely.
2. Implement bounded framing/deadlines and handler dispatch for status, bind, submit, output, cancel, reconcile and shutdown. Distinguish adapter submit from human management actions in audit metadata. Neither endpoint stores the key in its database.
3. Implement worker-only HTTP listener with strict methods/paths/content lengths/timeouts. Bound active request threads before allocating work; reserve capacity for heartbeat/cancel and close excess connections. No arbitrary files, operator actions or general job-submit endpoint.
4. Add hello/registration and immutable binding acceptance. Worker chooses its project ID; host operator accepts exact worker instance/project/image capabilities. Conflicting aliases/instances produce a reviewable refused state.
5. Add queued operation creation, durable start-grant transaction and duplicate identity handling. Cancellation racing a grant is serialized by the ledger transaction. A grant cannot outlive or cross its binding generation.
6. Add output chunk commits/acknowledgements and verified receipts. Native control reads return contiguous bytes; gaps/conflicts never produce success. Bound spool sizes and reject disk-full execution without an in-memory fallback.
7. Add lease/fence maintenance on independent monotonic loop. On broker restart recover unresolved operations to a safe fenced state before accepting execution. Restoring connected status does not clear fences.
8. Add structured status and bounded logs. Log metadata/state changes, never raw key, HMAC headers, user stdin or command output by default. Support bundle is explicit and includes limits/redaction notes.
9. Add graceful shutdown: stop granting work, persist cancel intentions, wait boundedly for worker receipts, retain unresolved fences, close sockets and join threads within a global shutdown deadline.

**Exit:** broker control/API integration tests prove auth separation, persistence, start-grant races, capacity and restart fencing. Broker executes no shell commands.

## Phase 3 — selected-project worker and container runner

**Dependency:** broker protocol; Docker and selected OS verified.

1. Implement standalone worker argparse: broker URL, worker ID, explicit project root, image digest, state directory and optional trusted CA. Credential through getpass or explicitly supplied env; no token CLI argument or token file.
2. Validate only the selected path: absolute resolved directory, safe root policy, unsupported mount separator rejection, owner/write checks and no recursive discovery. Register a stable project ID in worker app state. Print exact mount/exposure and require the local user's explicit start invocation; host cannot choose a new root.
3. Write the source Dockerfile with a real pinned official base digest, Bash/Python/ripgrep/coreutils/git and runner source. Build explicitly, record image ID/digest and inspect capabilities. Do not invent digest values or fetch binaries from unofficial sources.
4. Implement fixed Docker argv for one binding environment. Set no host network/PID/socket/extra volumes, non-root UID/GID, no-new-privileges, dropped caps, bounded resources/read-only root/tmpfs. Preserve selected project write permissions. Startup self-test validates required tools, cwd and scratch.
5. Implement runner separate from user stdin: process group spawn, merged output pipe, stdin forwarding, monotonic execution deadline, TERM/KILL and final receipt. Keep control descriptors/data separate from shell input and do not inject transport credentials.
6. Implement worker ledger acceptance/grant/launch-intent commits before process spawn. Replayed IDs/hash retrieve existing states; conflicting hashes fail. Crash after LAUNCHING never defaults to another spawn.
7. Implement worker outbound poll/upload/result loops with independent heartbeat. Authenticated non-loopback connections use verified HTTPS; loopback-only development mode is explicit. Disable automatic redirects and ambient loopback proxies.
8. Implement bounded output spool/sequence retry. Backpressure/disk limits must terminate or fence an operation, while heartbeat/cancel still progress. Output completion digest is committed before final receipt publication.
9. Implement cancellation and container-stop fallback. Confirm Docker stopped state before reporting termination; invalidate environment when whole-container stop loses shell state. A stopped container does not mean project effects were undone.
10. Implement in-container lease watchdog and worker-restart cleanup of only matching labeled containers. Test actual worker SIGKILL: active children must stop within the lease budget plus kill grace, or this gate fails. Recovered partial launch evidence stays unknown.
11. Implement receipt-first reconnect/recovery. Old-instance results are accepted only for matching historical operations; they cannot renew a new generation's lease. New worker acceptance waits for old work reconciliation.

**Exit:** local broker/worker/container integration proves exact byte output, no host secrets/mounts, grant dedup, cancellation, daemon-death cleanup and honest uncertain outcomes.

## Phase 4 — complete native environment adapter

**Dependency:** durable broker/worker lifecycle. Reuse Phase 0 adapter findings, replacing temporary code rather than keeping parallel implementations.

1. Implement provider create_environment through private control IPC. Capture immutable profile/worker/project/generation. Refuse stale, busy, unavailable or fenced binding. Container overrides/resources are explicitly matched or refused.
2. Subclass BaseEnvironment with supported constructor and initialization. Set non-host flags, payload stdin mode as needed, stable default cwd/cache path and explicit approval guards. Initial snapshot must route to the worker; no host/Python setup probe may run there accidentally.
3. Implement pipe-backed ProcessHandle: cached poll/returncode, condition-variable wait, exact stdout fd, cancellation request and bounded transport thread shutdown. Test with actual native fd/drain behavior. Expose no remote PID as a host `pid` attribute.
4. Transport `_run_bash` script/login/stdin/timeout unchanged into a durable operation. Handle pipe closure/EPIPE by requesting cancellation and retaining the fence until termination evidence. No duplicate send with a fresh operation ID during transport retry.
5. Wrap execute narrowly to serialize environment state and preserve every native option/field. Decorate with workbench identity/outcome, native returncode and truthful interruption text. Known command exit 1 remains a completed failure, not degraded infrastructure.
6. Implement bounded cleanup idempotently: no shell on server, cancel active operation, close binding/container when safe, retain state on uncertainty. Session-end hooks are not assumed to mean final teardown; use environment cleanup and public finalization semantics verified in Phase 0.
7. Verify cwd and exported-env snapshots across multiple calls and native relative file operations. Container loss reports recreation and lost scratch state; project files remain unchanged except actual command effects.
8. Validate real read/write/patch/search/terminal/execute_code, exact stdin, fetch_realpath/fetch_file and oversized output failure. Test missing server attachment paths honestly; automatic sync remains excluded unless a supported tested seam exists.
9. Prove native background/yield behavior through real tool executor. Handle child lifecycle with existing handle/runner or refuse through a verified public path. Do not silently accept background flags that cleanup cannot honor.
10. Exercise real profile/retry/delegation behavior. A second environment gets busy/refusal, and fresh operation IDs cannot evade a project fence. Read-only slash status shows actual profile binding without inventing task/session linkage.

**Exit:** complete native matrix passes and no custom file/shell replacement is needed. Doctor and catalog validation pass again after real integration edits.

## Phase 5 — CLI operation and recovery polish

**Dependency:** safe native workflow.

1. Implement commands exactly as OPERATIONS.md, with native help, invalid-input examples, concise text and `--json`. Exit codes distinguish success, bad input and unavailable/fenced state; no output relies on color alone.
2. Implement doctor/status using explicit bounded checks. Print actual selected profile, worker/project/generation/connection/operation, image and prerequisite errors. Missing setup includes one next action rather than a generic traceback.
3. Implement receipt reconciliation independent of native terminal execution. `recover` does not dispatch commands or clear an unknown fence merely because connection returns.
4. Implement explicit unknown resolution: require known stopped environment, operation ID, explanation and interactive confirmation for command-line human invocation. Refuse unattended clearing; support no model-exposed resolver tool. Preserve unknown history.
5. Implement stop/reset with bounded cleanup and state preservation. Do not kill containers outside the worker's exact labels. Document key rotation and quiescent source updates.
6. Rewrite README for actual implemented behavior: prerequisites, exact install/start steps, source image build, local topology example, errors, data disclosure and unsupported remote/OS claims.
7. Add a short bundled operational skill only if useful for agent guidance: inspect status before local project tasks, use native tools, explain unavailable/unknown states and never retry uncertain commands. It may teach use; it must not enforce the guarantees. If added, declare/register it and validate; omit if it adds no measurable value.

**Exit:** a fresh operator can complete setup and recover from a known failure using documentation, without a frontend or hidden manual edits. Required confirmation here is a product behavior for future unknown-state resolution, not a pause in the present authorized planning task.

## Phase 6 — adversarial verification and release artifact

**Dependency:** feature-complete native slice; detailed cases in VALIDATION.md.

1. Run targeted unit tests for changed state/auth/encoding logic. Run local process/container integration tests with fault injection. Fix failures, update TASKS/evidence, and repeat affected checks; do not repeatedly broaden tests without a new concern.
2. Run actual native tool routing, approval denial, prompt probes, timeout/stop/yield and profile-isolation tests. Preserve decoy hashes and dispatch counts. Do not substitute mocked registration for runtime success.
3. Kill broker/worker/runner at each meaningful crash window; lose acknowledgements; duplicate requests/chunks; exhaust output/disk/queue bounds; verify no unbounded hang or second filesystem effect.
4. Rehearse installation from a clean directory source package, missing prerequisites and mismatched versions. Verify removal/update quiescence, ledger migration and older schema reopening. Source repository contains no token/env/runtime spool or generated bytecode.
5. Run `hermes plugins doctor <plugin-path> --ci` and `hermes plugins validate <plugin-path> --install-deps` in the supported disposable Hermes release. Inspect every scanner warning and declare reality accurately. Record exact commands/results.
6. Verify README local links/help examples, manifest/package version/floor consistency and supported-platform language. Record observed startup/command/status latency, with local topology plainly named.
7. Prepare source commit only after user-directed release work begins. Catalog entry uses public owner/repo, quoted version, truthful compatibility and full tested 40-character SHA. No placeholder listing is submitted.

**Exit:** source pin and evidence correspond to what the demo runs. No publication has occurred merely because these tasks are planned.

## Phase 7 — hackathon demonstration and submission

**Dependency:** release gates passed; publication/submission explicitly instructed later.

1. Record ≤85 seconds to leave encoding/platform margin below 90: 0–10 seconds problem/target; 10–45 native read/edit/test; 45–58 server decoy unchanged; 58–75 disconnect/denial and honest recovery; 75–85 result/install name. Show live working terminal, not a slide-only promise.
2. Use a preinstalled tiny fixture and an actual relevant bug/test fix. Do not fabricate output, speed up long waits without disclosure or hide failed setup. State that demo isolates host/worker on one local machine.
3. Prepare standalone repository README and catalog PR disclosure. Add a screenshot only if it clarifies CLI behavior; no UI is required.
4. When authorized, open catalog PR, post demo on X tagging @NousResearch, then submit both URLs in the form. Opening PR is sufficient for the form; maintainer-triggered checks may run later. Track deadlines and final links in TASKS without secrets.

## Time and scope control

Working estimate: 32–45 focused hours after the first premise checkpoint if the public contracts cooperate. The state/runner failure paths are the highest risk; this estimate must be revised after actual Phase 0 results. Calendar availability does not equal productive hours.

- November 7: settle native premise and essential environment prerequisites.
- November 8: broker/worker loop and durable grant/result handling.
- November 9: complete native adapter, cancellation and failure injection.
- November 10: release validation, fresh setup rehearsal and demo recording.
- November 11: only critical fixes and authorized publication/submission; leave several hours before 22:00 UTC.

No frontend is scheduled. Extra OS support, remote-host provisioning, WebSockets, fleet support and automatic attachment synchronization are deferred. If native routing or approval preservation cannot be established early, the honest response is a scope/direction decision, not a guarantee that the project still has time to win.
