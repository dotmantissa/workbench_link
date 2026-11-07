# Replacement direction: Workbench Link

Implementation authority: [ARCHITECTURE.md](ARCHITECTURE.md). User-confirmed delivery is a native plugin with no frontend; development uses one local machine and isolated execution environments. Native runtime proof is still pending.

Prepared November 7, 2026. Data Clinic is set aside at the user's request. The selection order is ecosystem pain → demand → useful missing functionality → public implementation path → reliable solo delivery → polish → creativity. Novelty is secondary.

**Recommendation: Workbench Link, a native terminal-environment plugin that lets a remote Hermes agent read, edit and test a selected project on the user's local machine through one consistent execution backend.** Skills, memory and reasoning stay on the Hermes host. The worker executes the project operations. The exact name is provisional.

This is a stronger problem premise than Data Clinic because users explicitly request this capability, describe the work it blocks, and identify shortcomings in existing approaches. It is a credible direction to advance to an implementation feasibility spike. It is not a claim that the whole gap is uncovered, that demand implies adoption, or that winning is predictable.

No plugin has been built or runtime-tested. The public API/source checks described here support feasibility, not completed functionality. The immediate next implementation should prove the native backend path before building a full transport/UI.

## Evidence of need

| Source | Observed evidence on November 7 | What it establishes |
| --- | --- | --- |
| [#18715: remote agent with local tool execution](https://github.com/NousResearch/hermes-agent/issues/18715) | Open; 45 thumbs-up, 47 total reactions, 33 comments. The request explicitly says “Remote brain, local hands,” with terminal, files, code and local development resources. Multiple comments describe an always-on server plus local project machines. | Direct demand for the proposed capability family and concrete development workflows. Counts are not unique prospective customers or a representative survey. |
| [#1855: multi-backend terminal](https://github.com/NousResearch/hermes-agent/issues/1855) | Open; 17 thumbs-up, 11 comments. Describes losing cwd/environment state with one-shot SSH and wanting explicit execution targets. | Adjacent demand for predictable workspace execution and persistent command state. Some proposed features may already be partially supported elsewhere. |
| [#38519: frontend-only Desktop](https://github.com/NousResearch/hermes-agent/issues/38519) | Open; 35 thumbs-up, 39 total reactions, 26 comments. Wants a client for an agent already running on another machine. | Remote-host/client usage is an actual ecosystem pattern; it does not independently prove demand for our particular worker. |
| #18715 discussion and Talaria README | Existing plugin and protocol proposals; discussion repeatedly raises mixed execution targets, file edits on one machine with tests on another, cancellation and no server fallback. | The problem is about correct execution placement, not just exposing an extra remote command. |

The issue counts must not be added into a market-size estimate. Reactions can overlap, comments include implementation debate and AI-generated triage, and open status is not proof a feature is absent. I inspected bodies, comments, existing solutions and released source before choosing the narrower gap.

## The useful outcome

A developer keeps Hermes on a server with its persistent agent state. Their project is on a laptop, alongside its working tree and development environment. Asking the remote agent to repair the project should cause the source inspection, file change and test run to happen in that same chosen workspace. The user should be able to see where the work ran.

The MVP job is: **connect one local project, ask Hermes for a code change, inspect the local diff, and run the project's tests in that workspace.**

The practical benefit is avoiding repeated project copying and target confusion while keeping an always-on remote agent. This is a repeatable development workflow rather than an occasional data-migration task. Those are product hypotheses grounded in explicit requests, not measured time savings.

## What already exists, and the precise improvement

[Talaria](https://github.com/Kaylachuuu/hermes-talaria) already supplies named devices, a helper, its own file/shell tools and browser/screen features. Its latest inspected README explicitly says Hermes' own terminal/file tools are not rerouted. It also says server cancellation does not reach the helper. I have not run it and do not assume every advertised limitation still exists at an older pinned version.

Workbench Link would use the **native environment provider**, so `terminal`, `read_file`, `write_file`, `patch`, `search_files` and `execute_code` use one backend rather than separate device-tool names beside the host tools. That is a functional improvement: editing and testing operate against the same filesystem without relying on the model to select the right tool family for every step.

Core SSH already runs commands and file operations on reachable remote machines. We must not advertise remote execution as missing altogether. The reason to build a new backend is a local worker connecting outward to the Hermes host, with project setup/status, consistent native routing and explicit disconnect handling. If the finished product is merely an SSH wrapper, it does not justify this direction.

We should build original source. Do not fork/rebrand Talaria or a bundled backend. The catalog restricts forks/skins; public provider integration is the proper architecture. Credit issue discussions and any legitimately reused libraries, and do not copy code without its license and attribution.

## Released public API supports the approach

The v0.23.0 [Terminal Environment Provider guide](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin) documents:

- `agent.terminal_env_provider.TerminalEnvironmentProvider`.
- `ctx.register_terminal_environment_provider(...)`.
- A `create_environment(cwd, timeout, task_id, ..., **kwargs)` factory returning the supported environment contract.
- Native terminal/code/file tools using the environment's execution path.
- `is_remote`, `is_container`, `default_cwd`, credential stripping and approval classification.
- An optional stream interface for browser/computer-use placement, which the MVP will exclude.

I fetched the guide, provider ABC, native factory and BaseEnvironment source from tag v0.23.0. The factory calls the registered provider and carries `task_id`. This is a source-level confirmation that an additive backend exists; no private table patching or built-in tool replacement is necessary.

Do not import the private native factory in the plugin. Reading it was evidence gathering. Implement against the documented provider/environment contracts.

Set `skip_container_guards = False` explicitly because this backend can change a real user project. Leave `uses_host_filesystem` false for the worker environment so file tools cannot take the server's direct filesystem path. Cheap availability/probe methods must not make network calls or register background work.

A native environment object is in-process only; document that limitation and validate actual installation. A selected backend/provider setting is profile-scoped. **Do not promise an arbitrary per-session Server/This Computer picker, unchanged cron routing within the same profile, or complete split-runtime parity.** Those need additional supported routing behavior and actual tests. First prove one configured project-working profile/backend. Server-only tasks must remain on a profile/backend explicitly configured for server execution.

The desired worker connection is outbound and authenticated, using the host's supported own-plugin backend routes. Its compatibility with gateway authentication, profile routing, async execution and the native environment interface is the highest-risk integration question. Do not design around it through unauthenticated relay endpoints or private core hooks.

## Competitive minimum and cut lines

| Include | Bound the implementation |
| --- | --- |
| One remote Hermes host, one worker, one project | No device fleet, shared-team routing or dynamic machine selection. |
| Native terminal/file/code operations | Prove that reads, writes, searches and tests hit the same worker filesystem. |
| Local project worker | Initially Linux with a project mounted into a local Docker environment. Only the explicitly granted project is mounted; no Docker socket or arbitrary host-path mount API. Docker is an explicit prerequisite, not a hidden dependency. |
| Selected workspace identity | Freeze the worker/project identity for an environment's life. A changed target requires a new attachment/environment. |
| Useful status and setup | Connected target, workspace, current operation and errors; a minimal native settings/status surface plus commands. No elaborate dashboard before routing works. |
| Bounded command/results protocol | Operation IDs, timeouts, output limits, authentication and cancellation where actually supported. |
| Normal Hermes approvals | No YOLO child agent, no broad auto-approval and no disguised server shell fallback. |
| Explicit failure outcomes | Offline means refusal; uncertain operation results remain uncertain until reconciled. |

Exclude browser/screen control, arbitrary local MCP relay, Windows/macOS support claims, mobile apps, peer-to-peer discovery, skill/memory synchronization, global terminal overrides, full split-runtime protocol and a custom agent framework.

Linux/container-first narrows demand coverage: it does not satisfy every Windows/macOS user or access every workstation-native app. That is preferable to untested cross-platform claims. If container prerequisites make the user advantage disappear in a workflow test, reconsider this scope rather than hide the setup burden.

Do not promise persistent shell environment variables until the supported process interface works. At minimum verify cwd and file consistency across calls. A native BaseEnvironment has process/file-transfer plumbing beyond a tiny `execute()` stub; uploads, spills, downloads and cleanup need focused integration checks.

## Reliability boundaries

The main risks are wrong-target changes, approval bypass, credential exposure, repeated effects after lost acknowledgements and leaked processes. These are central to the feature, not optional polish.

Enforce a frozen workspace binding in the provider/worker protocol. Include the execution target in every result and the status surface. On disconnect, return an infrastructure error rather than creating a server environment or silently targeting another worker. Account for prompt-time probes so no command runs before attachment is confirmed.

Use stable operation IDs and a worker-side execution ledger. Duplicate delivery must not execute a job twice. This does **not** establish exactly-once effects: a worker can crash after a side effect but before recording its result. Such a job must become unknown, with further writes fenced until explicit reconciliation; no automatic replay. Normal app retries must not evade that fence.

Distinguish requested cancellation, acknowledged cancellation and actual termination. A dropped connection does not prove a process stopped. Do not claim robust cancellation unless the installed native path and worker process tree have been tested. Exclude background commands from the supported initial workflow if their lifecycle is not reliable.

Read Hermes-side secrets through declared host secret routes. The companion must accept its own explicitly supplied connection material without reading Hermes/vendor/browser credential files. Keep connection credentials out of model-visible subprocess environments, logs, operation arguments and result payloads. Use established TLS/authentication facilities; test authentication and profile boundaries before any real project data is used. Do not claim a pairing/REST request proves a human approved an operation.

Project contents and command output travel to the remote Hermes host and may reach its selected model. The worker is a user-started long-running process; disclose what it reads, runs and stores. Containers limit the mounted filesystem but are not a blanket security guarantee. Do not add telemetry or automatic background installation.

## Judge scrutiny

| Criterion | Why this is stronger | Remaining objection |
| --- | --- | --- |
| Usefulness | Direct requests describe precisely blocked work; a correct local edit/test loop has immediate value and potential repeat use. | Setup cost, Docker requirements and profile selection could still make SSH/Talaria preferable. Adoption must be tested. |
| Reliability | Consistent native placement and refusal on loss can remove an identified failure class. | A remote execution bridge is consequential; an incomplete protocol could be worse than existing options. |
| Polish | A visible target and short setup can make a confusing host/client distinction understandable. | Networking/auth/setup can consume the remaining time. Focus on the smallest honest working flow. |
| Creativity | A provider changes Hermes' actual execution environment, a central capability mentioned in the brief. | Remote execution is established; winning depends on usefulness and dependable integration, not claiming invention. |

The recommendation is to advance this direction, not to declare a favorite. It has a stronger demand/functionality basis than Data Clinic and a documented extension seam. Its biggest risk is delivery. A failed native-backend spike should stop the build early.

## Immediate implementation gate

Time-box the first vertical spike to approximately three focused hours, then reassess against actual progress and remaining availability. The time box is a decision checkpoint, not a promise that the entire feature can be implemented in three hours.

1. Load a minimal original provider through a disposable real v0.23.0 Hermes installation.
2. Connect a minimal worker using supported authenticated host routes; no custom public unauthenticated endpoint or credential-store access.
3. Place different marker files in a server fixture and a worker fixture. Through **native** tools, read and patch the worker marker and run a small test. The server marker must remain unchanged.
4. Deny one potentially destructive operation through normal Hermes policy. Prove that nothing reaches the worker.
5. Disconnect the worker. Native calls must fail with no execution on the server and no automatic replay of an uncertain write.
6. Confirm the environment factory/context identity and profile scope. If this requires private patches or a guaranteed per-session selector the API cannot provide, stop that design.

An isolated two-process/container test proves placement separation, not real cross-machine setup. Before demo claims, rehearse on two actual machines or clearly label the narrower environment used.

If the source-supported integration works, continue with authentication/lifecycle hardening, project setup, installation validation and a real code-change demo. If routing only works via duplicate custom tools, it loses its main improvement over Talaria. If incoming SSH alone provides the entire useful outcome, reassess the worker proposition. Do not rescue either result by adding browser/fleet features.

## Demonstration and submission

The sub-90-second demo should show an installed plugin, a project on the worker, its visible target, a real Hermes edit and native test run, the local diff, and a brief disconnect refusal with the server decoy intact. Use a genuine bug/test pair rather than invented catastrophic behavior. A crafted fixture is acceptable when disclosed; no prewritten model/tool outcomes.

Validate the exact pinned source with native PluginManager/doctor/catalog checks and a fresh installation. Ship reviewable source, truthful supported-platform metadata, disclosures, and a matching full-SHA catalog entry. A source-built worker may be included; no opaque committed binaries or self-updater. Use only official pinned dependencies/images and disclose setup downloads.

The deadline is November 11, 2026, 22:00 UTC / 23:00 Lagos under the supplied brief. Preserve time for the public repository, catalog PR, working X demo tagging @NousResearch, and form submission. Do not equate elapsed clock hours with productive solo hours or treat maintainer-triggered CI as local validation.

## Evidence and limits

The new source snapshots live in ignored `research/sources/pivot-*` files. Bodies/comments were fetched from public GitHub APIs; Talaria, memory-rewind and s3 READMEs were read as public product claims; no fetched code was executed. Query/source snapshots record candidate issue metadata. The initial broad query excluding “hackathon” produced a distorted tiny subset and was discarded in favor of broad issue/feature queries.

Alternatives considered: native backup (already shipped; granular history also exists), cloud/profile sync (direct demand but existing tools and credential/host-setting complications), document knowledge (direct demand but qmd/MemoBase/local RAG coverage), mobile/voice (high demand, substantial existing coverage and too much scope), permission tiers/browser handoff (important but core-owned surfaces exceed a safe plugin sprint), and AccessCheck (not promoted merely because the earlier idea failed; specific Hermes demand was not established).

This decision supersedes the Data Clinic recommendation/build plan. The research, judge review and previous plan remain intact as historical context.
