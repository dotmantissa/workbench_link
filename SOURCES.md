# Evidence register

Accessed November 7, 2026. Full public-source snapshots are retained locally in `research/sources/`; marketplace metadata in `research/marketplace-entries.json`; hackathon-related PR bodies in `research/current-entries.md`. These caches are research evidence, not an endorsement of fetched code. No fetched code was executed.

## Competition and runtime

- **User-supplied Hermes Plugin Hackathon announcement**: authoritative working brief for rubric, prizes, deadline and submission steps. Original organizer social post was not independently retrieved.
- [Plugin developer guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins): native tools, lifecycle, storage, manifests and public surfaces. Live docs read; some examples contain version/manifest inconsistencies, so implementation must follow the running release and validator.
- [Catalog admission](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission): pinned public repo, validation, public APIs, credentials, approvals, source-only payloads and disclosure.
- [Desktop Plugin SDK](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk): native route/sidebar surfaces, own backend REST and upload, scoped storage and SDK boundaries.
- **Release-specific check:** fetched `website/docs/developer-guide/desktop-plugin-sdk.md` and `website/docs/developer-guide/plugins/index.md` from tag `v0.23.0` through GitHub's contents API. The release docs include `ROUTES_AREA`, `ctx.rest` upload transport, native tool/slash-command registration and durable plugin storage. This is source/documentation verification; runtime integration still needs the first build spike. Generic plugin RPC appears in live docs but was absent from the fetched release guide, so the plan uses own documented REST routes instead.
- [Public plugin API](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/public-api): documented imports and extension contract.
- [Middleware](https://hermes-agent.nousresearch.com/docs/developer-guide/middleware) and [hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks): approval/block shapes and fail-open failure semantics. Middleware is not needed for the proposed minimum.
- [v0.23.0 release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0): released November 5, 2026; conversation rewind, tool budgets, delegation and marketplace size.
- [Marketplace](https://hermes-agent.nousresearch.com/docs/plugins): embedded public snapshot decoded as 1,064 plugin metadata entries. Descriptions can be truncated; relevant repository READMEs were also read.
- [Catalog tree](https://github.com/NousResearch/hermes-agent/tree/main/plugin-catalog): Git tree snapshot had 1,066 paths. The GitHub directory-contents endpoint returns at most 1,000 entries; it was not used as the complete catalog count.
- [Current hackathon-related PR discovery](https://github.com/NousResearch/hermes-agent/issues?q=hackathon): GitHub API search returned 134 records. Includes PRs/issues and updates, not a verified competitor roster.
- [ChangeFreeze entry #149474](https://github.com/NousResearch/hermes-agent/pull/149474): entrant corroboration of November 11, 2026 at 17:00 EST. Not an independent official rules source.

## Confirmed winner sources

- [Codegeist Unleashed 2023 organizer announcement](https://www.atlassian.com/blog/developer/codegeist-unleashed-2023-winners): placements and GoMood's live Stage Show win.
  - [Tably team submission](https://devpost.com/software/tably-turn-confluence-pages-into-databases): typed extraction, review, export, model consistency challenges; first-place badge.
  - [GoMood team submission](https://devpost.com/software/secretia-project): support sentiment workflow, dashboards, RICE selection and incremental scope.
- [Codegeist 2024 organizer announcement](https://www.atlassian.com/blog/developer/codegeist-2024-winners): category and bonus placements.
  - [Runbook Rabbit team submission](https://devpost.com/software/runbook-rabbit-let-rovo-be-your-jira-agent-s-new-assistant): exact source highlighting, Jira events, native Forge/Rovo implementation, solo author.
  - [Compass Whiteboard team submission](https://devpost.com/software/compass-whiteboard): transitive dependencies, React Flow, reviewed save/reset and persistent layout.
  - [Budgety team submission](https://devpost.com/software/budgety-financial-management-assistant): financial charts, stakeholder discovery, existing product base, date inconsistencies and explicit quality limits. Time-saving claims are team claims, not independently measured.
- [Microsoft AI Agents Hackathon 2025 organizer winners](https://microsoft.github.io/AI_Agents_Hackathon/winners/): verified overall/category placements and event rubric. Some explanatory passages speculate about architecture; team submissions supersede them for implementation details.
  - [RiskWise submission #526](https://github.com/microsoft/AI_Agents_Hackathon/issues/526): actual procurement/schedule architecture, tool grounding, UI and reporting.
  - [TARIFFED! submission #349](https://github.com/microsoft/AI_Agents_Hackathon/issues/349): concrete HTS database, Azure tools, UI, demo and solo team.
  - [WorkWizee submission #587](https://github.com/microsoft/AI_Agents_Hackathon/issues/587): implemented Teams/Jira/Bitbucket endpoints and separately listed pending integrations. The 40% saving is a team claim, not an independently established result.
- [DataHub Agent Hackathon 2026 organizer winners](https://datahub.com/blog/meet-the-winners-of-build-with-datahub-the-agent-hackathon/): confirmed Blackbox, Hindsight, Schema-Drift Auto-Repair, Culprit and Paracelsus wins; ContextSeal and RippleProof honorable mentions; evidence/verification descriptions and July 6–August 10 build period.
  - [Project Blackbox team submission](https://devpost.com/software/project-blackbox) and [repository](https://github.com/alejandro-publius/blackbox-datahub): engine boundaries, actual repair/PR artifacts, synthetic fixture disclosures and evaluations. The repository was read, not executed or independently audited.
  - [Hindsight submission](https://devpost.com/software/hindsight-cpxymj), [Schema-Drift submission](https://devpost.com/software/schema-drift-auto-repair-agent), [Culprit submission](https://devpost.com/software/culprit-a-stack-trace-for-model-decay), [Paracelsus submission](https://devpost.com/software/paracelsus), [ContextSeal submission](https://devpost.com/software/contextseal), [RippleProof submission linked by organizer](https://devpost.com/software/blastradius): pointers from the organizer, not all individually inspected in this pass. The research table uses the organizer's descriptions for these projects.

## Hermes audience, pain and competitors

- [Hermes user stories](https://hermes-agent.nousresearch.com/docs/user-stories): curated real-use references, including business operations, customer/stock systems and field work. Aggregated testimonials are not representative demand measurements.
- [CSV context expansion issue #134201](https://github.com/NousResearch/hermes-agent/issues/134201): open at the snapshot; reported large raw CSV prompt expansion with synthetic reproduction. Not independently reproduced.
- [Locale-encoded attachment issue #84206](https://github.com/NousResearch/hermes-agent/issues/84206): open at the snapshot; specific strict UTF-8 failure and example encodings. Not independently reproduced.
- [Spreadsheet feature request #4438](https://github.com/NousResearch/hermes-agent/issues/4438) and [live-document contract request #120324](https://github.com/NousResearch/hermes-agent/issues/120324): open at snapshot; evidence of interest/friction, not evidence that proposed surfaces exist.
- [Cash Desk #150374](https://github.com/NousResearch/hermes-agent/pull/150374): current invoice/bank matching and reminder entry. Sufficiently direct collision to reject invoice chasing; its functionality is described by the entrant, not tested here.
- [Rescue #150015](https://github.com/NousResearch/hermes-agent/pull/150015), [Excubitor #150261](https://github.com/NousResearch/hermes-agent/pull/150261), [Workgraph #150453](https://github.com/NousResearch/hermes-agent/pull/150453), [ProofGate #149185](https://github.com/NousResearch/hermes-agent/pull/149185), [citation-guard #150613](https://github.com/NousResearch/hermes-agent/pull/150613): current safety/recovery/provenance competition. PR bodies inspected; tests and performance claims not independently run.
- [office-desk](https://github.com/DECRUX9812/hermes-office): inspected README describes backups, receipts, guarded editing and a Desktop review page. It materially limits claims of novelty for any generic safe spreadsheet editor.
- [hermes-tabular](https://github.com/frankiethull/hermes-tabular): inspected README describes a pack of tabular ML skills and model families rather than the proposed operational import contract.
- [freight-reconciliation](https://github.com/harrylabsj/hermes-plugin-freight-reconciliation): inspected README describes deterministic local bill/trip/rate reconciliation, redacted model projections and review. A meaningful adjacent incumbent.
- [OpenRefine documentation](https://openrefine.org/docs): established data-cleaning alternative. Use as a baseline for user discovery rather than implying the category is new.
- [OpenRefine running/history manual](https://openrefine.org/docs/manual/running): judge-review reinspection of the saved snapshot confirms persistent change history across restarts, undo/redo and reusable JSON operations. These materially weaken novelty claims based on persistence, audit history or replay alone. See JUDGE_REVIEW.md; OpenRefine was not executed.
- [HubSpot import file requirements](https://knowledge.hubspot.com/import-and-export/set-up-your-import-file): file formats, UTF-8, property types, dates and record identifiers; target-contract reference.
- [HubSpot import errors](https://knowledge.hubspot.com/import-and-export/troubleshoot-import-errors): existing in-wizard error fixes and error export. Shows why “fix a CSV” alone is weak differentiation.
- [Microsoft Power Apps imports](https://learn.microsoft.com/en-us/power-apps/user/import-data): another established import workflow; not a second target for the minimum build.

## Leads not counted as confirmed winners

READMEs for [Chathletique](https://github.com/colinfrisch/chathletique-mcp), [voice email via Resend](https://github.com/rubens-shoji/resend-mcp-hackathon), and [Inspector](https://github.com/wlu03/Inspector) claim hackathon wins. These claims were not independently matched to an organizer result during this pass. Inspector is useful product-shape context for the AccessCheck alternate, not a confirmed placement in the winner table.

Some guessed winner URLs returned 404. Google/DuckDuckGo/Brave/Mojeek searches were challenged or unavailable; Bing returned irrelevant results. Salesforce Help returned a loading shell, Intuit's candidate report hostname did not resolve, and Hacker News returned an access error. None supports a factual claim in the recommendation. A small curated hackathon wiki was a discovery lead only; placements above use primary sources instead.

## Demand-led replacement research — November 7, 2026

The active decision is in [DIRECTION_DECISION.md](DIRECTION_DECISION.md). Public API/README evidence is source verification, not runtime/adoption proof. New raw issue, comment and source snapshots are ignored under `research/sources/pivot-*`.

- [Remote Hermes/local tools #18715](https://github.com/NousResearch/hermes-agent/issues/18715): 45 thumbs-up, 47 total reactions, 33 comments at snapshot; exact split-runtime/local-workspace demand and discussion of existing solutions. Counts do not estimate market size.
- [Multi-backend terminal #1855](https://github.com/NousResearch/hermes-agent/issues/1855): 17 thumbs-up, 11 comments; cwd/state/explicit-target problems.
- [Frontend-only Desktop #38519](https://github.com/NousResearch/hermes-agent/issues/38519): 35 thumbs-up, 39 total reactions, 26 comments; related remote-host/client usage.
- [Talaria README](https://github.com/Kaylachuuu/hermes-talaria): existing named-device remote tools/helper/browser/screen; currently inspected README explicitly says native Hermes terminal/file tools are not rerouted and server cancel does not reach its helper. Not executed or audited.
- [Terminal Environment Provider guide](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin): fetched with `agent/terminal_env_provider.py`, `tools/terminal_tool_backends.py` and `tools/environments/base.py` from tag v0.23.0. Public registration/ABC and native factory participation verified; private factory read for evidence only, not proposed as a plugin import.
- [Backup request #12238](https://github.com/NousResearch/hermes-agent/issues/12238): 28 thumbs-up, 42 total reactions; comments identify native backup/import and interim skill work. [memory-rewind](https://github.com/AhmetArif0/hermes-memory-rewind) already offers granular local history/restore.
- [Cross-device sync #20510](https://github.com/NousResearch/hermes-agent/issues/20510): 23 thumbs-up, existing Git-sync approaches and concrete cross-OS/profile confusion. Full credential synchronization conflicts with the permitted plugin credential boundary.
- [Knowledgebase #844](https://github.com/NousResearch/hermes-agent/issues/844), [workspace #531](https://github.com/NousResearch/hermes-agent/issues/531), and [semantic session search #44075](https://github.com/NousResearch/hermes-agent/issues/44075): direct demand, but qmd, MemoBase, local RAG and existing memory/search providers supply substantial coverage. #844 comments point to implementations; their performance was not independently tested.
- [Permission tiers #527](https://github.com/NousResearch/hermes-agent/issues/527) and [cross-platform browser handoff #149488](https://github.com/NousResearch/hermes-agent/issues/149488): meaningful needs, but complete solutions need core-owned authorization/lease/routing seams rather than a safe narrow plugin sprint.

Broad open-issue/feature queries replaced an initial query excluding “hackathon” that returned a distorted tiny subset. Issue search totals, reaction counts and advertised implementations are not adoption measurements. A guessed release path `hermes_cli/plugins_context.py` returned 404 and supports no conclusion.

## Architecture contract verification — November 7, 2026

- Additional v0.23.0 BaseEnvironment output/process-handle, built-in Docker, plugin management and dashboard extension source snapshots fetched with HTTP 200 and stored with SHA-256 hashes in ignored research/sources/architecture-fetch-manifest.json. Sources were inspected, not executed. The design chooses a separate plugin-owned broker instead of relying on an unproved gateway worker-auth route.
- [Architecture](ARCHITECTURE.md) and [API contracts](docs/API_CONTRACTS.md) distinguish source facts from runtime gates. Real execute uses returncode, not the simplified guide's exit_code; native timeout/interruption can precede remote termination confirmation.
- Local environment probe reports Linux/WSL2, Python 3.14.4 and no Docker executable on PATH. No Docker/Hermes runtime integration has been performed. User confirms one local test machine and no frontend requirement.
- Historical Data Clinic judge review belongs to the separate research archive; it is not included in this repository or the current project plan.
