# Current hackathon-related PRs — source snapshot

## feat(plugin-catalog): add Hackathon Judge
https://github.com/NousResearch/hermes-agent/pull/150334
State: open; created 2026-11-06T22:25:16Z

## What does this PR do?

Adds **one catalog entry**, `plugin-catalog/hackathon-judge.yaml`, for [Hackathon Judge](https://github.com/Brianmacu-BMS/hermes-hackathon-judge), an original plugin submitted by its repository owner for the Hermes Plugin Hackathon. No Hermes core, workflow, validator or policy files change.

Hackathon Judge performs bounded static inspection of local plugin source against packaged official catalog/hackathon requirements, reports file/line findings, and supports evidence-bound human reviewer decisions. It keeps code readiness, submission preparation, submitted entry and catalog admission separate. It is advisory, never official certification; heuristics, author attestations and supplied URLs are not proof of acceptance.

Unlike a prompt-only checklist, it implements deterministic manifest/payload/dependency/registration checks, SHA-256-bound candidate/policy/evidence validation, stale-review rejection, finding dispositions and structured validator-receipt checks. Static audits never import candidate code. Captured policy does not update itself.

## Exact entry and public surfaces

- Repository: https://github.com/Brianmacu-BMS/hermes-hackathon-judge
- Pin: **`bd24c8905864e9a714de7d34eb143c29c2ee9dda`**; reachable from repository `main` after [source PR #1](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/pull/1) merged. The merge commit has the identical tested tree; this entry deliberately retains the exact SHA named by the qualification receipts.
- Version **"0.2.1"**, tier **community**, category **tools**, `requires_hermes: ">=0.22.5"` matching `plugin.yaml`.
- **Linux only** in catalog metadata. Focused Windows boundary coverage is not full installed Windows support; macOS installed support is not claimed.
- Tool `hackathon_judge`; slash command `/judge-plugin`; CLI `hermes hackathon-judge`; namespaced skill `hackathon-judge:judge-plugin`.
- Registration/runtime use public `ctx.register_*` and `ctx.dispatch_tool` APIs. No hooks, middleware, required credential environment variables, core overrides, login backend, custom Desktop renderer or web UI. There is no custom UI requiring screenshots; the native commands return text/JSON.

## Rule 13 disclosures

| Behavior | Scope |
|---|---|
| Network | No runtime registration/audit/review/reporting network calls, remote GitHub/X/form verification, self-updater or policy auto-refresh. Explicit development/CI setup downloads pinned Hermes/tool/dependency sources on disposable runners; it is not imported by registration. |
| File reads | Reads the explicitly selected candidate tree, supplied catalog/submission/review documents, SHA-bound evidence under the review document directory, and packaged policy sources. Credential stores/recognized sensitive files are refused or skipped without reading/hashing their contents. Unknown secret-bearing ordinary source names cannot be reliably identified; audit credential-free source only. |
| Commands | Static runtime spawns none. Optional `validate` requires authorization for the exact trusted candidate plus `trusted_code: true`, then uses normal host terminal dispatch for `hermes plugins validate PATH --json`. This executes candidate code and is not a sandbox. It does not request `--install-deps` or bypass host approvals. |
| Writes | Runtime returns results to its caller; stdout redirection and saving review evidence are operator actions. It does not mutate candidate/config/authentication/memory. Explicit release/demo/test helpers write their requested output/temporary fixture directories. |
| Background activity | No watchers, schedules, persistent helpers or unattended interactive flows. |
| Credentials | No runtime credentials requested, read from credential files, stored, refreshed or rotated. No vendor-client impersonation. |
| Telemetry/models | None: no analytics, usage reporting, plugin-owned model calls, provider routing or auxiliary-model changes. |
| Dependencies/payloads | Runtime bounds: `PyYAML>=6.0,<7`, `packaging>=24,<27`; [dependency policy](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/blob/bd24c8905864e9a714de7d34eb143c29c2ee9dda/docs/dependency-policy.md). No inherited Hermes release-age guarantee is claimed. Source-only repository, no committed executable binaries/bytecode or opaque payload archives. |

## Actual validation at this pin

- Full official **Doctor --ci** and **plugins validate --install-deps --json**: **15/15 checks on Hermes 0.22.5 and 0.23.0**, on disposable GitHub-hosted Ubuntu machines. [Complete native acceptance and qualification logs](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/actions/runs/42299619949).
- Actual install/enable/discovery, registered tool/static audit, discovered slash handler, namespaced skill, native CLI exits **0/1/2/3**, alias refusal, trusted-code refusal and static candidate nonexecution are exercised. Native PluginContext reaches the real terminal: an exact temporary `approvals.deny` rule blocks fixture execution, then ordinary policy allows explicitly trusted benign validation after removing that test rule. No synthetic terminal success or blanket auto-approval. This proves policy-denial behavior, not interactive approval-card UI acceptance.
- [Linux/Windows push CI](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/actions/runs/42299619897) and [PR CI](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/actions/runs/42299626947): Linux Python **3.11–3.14**, normal/optimized, **207 passed / six Windows-only skips / 213 total per run**; focused native Windows **3.11/3.14** path/URL/checkout suites, both modes. All six real junction cases execute and pass on Windows.
- All **51 installed file hashes** match anonymous public Git blobs and a reproducible source archive; extracted-artifact contracts pass in normal/optimized modes. These are our source-repository results, **not a claim that this upstream PR's admission CI has already run**.
- Current upstream standalone structural validator accepts this entry without errors/warnings and validates all 1,065 catalog files with zero errors (five existing warnings elsewhere). The current runtime catalog parser accepts its exact pin/metadata, with no name/repo collision or removal-list match. The upstream source-only payload scanner also passes the pinned checkout. Static preflight has complete inventory and no failed checks; manual requirements remain manual, and its raw `needs_review` result is not relabelled as certification.

Both official validators retain this exact caution for maintainer review:

```
security scan caution: dump_all_env (scan.py:133), python_os_environ (requirements.json:96)
```

[scan.py:133](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/blob/bd24c8905864e9a714de7d34eb143c29c2ee9dda/hackathon_judge/scan.py#L133) is a credential-path regex evaluated against AST string literals; [requirements.json:96](https://github.com/Brianmacu-BMS/hermes-hackathon-judge/blob/bd24c8905864e9a714de7d34eb143c29c2ee9dda/hackathon_judge/requirements.json#L96) quotes the credential-scope policy. Neither dumps the environment nor reads a credential store. The warnings are retained, not suppressed.

## Remaining external steps

Please run/review the upstream admission checks and pinned source before merging. Our separate native qualification is not upstream maintainer approval or catalog acceptance. No automatic merge is requested.

The under-90-second working demo/X post and hackathon form submission remain the owner's steps; neither is claimed complete here. Historical `submission/` drafts inside the pinned source are preparation templates, not current publication receipts. The development Hermes environment remains uninstalled/inactive; native activation was confined to disposable runners.


## plugin-catalog: add fluent (Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150353
State: open; created 2026-11-06T23:27:06Z

Adds **fluent** to the plugin catalog: `plugin-catalog/fluent.yaml`, pinned to
[`182c430`](https://github.com/Bruno-coder21/fluent/tree/182c4301f2437e784e9022f1f38576e1d68c3f5f).
Hermes Agent Plugin Hackathon entry.

![fluent](https://raw.githubusercontent.com/Bruno-coder21/fluent/182c4301f2437e784e9022f1f38576e1d68c3f5f/docs/banner.png)

## What it does

Hermes already checks the code it writes; **fluent checks the shell commands it runs**,
against the real `--help` and man pages of the program installed on the user's machine,
before they run.

```
agent> ffmpeg -y -i in.mp4 -c:v libx264 --crf 28 out.mp4
🛡️ fluent caught `--crf` in ffmpeg → `-crf`
agent> ffmpeg -y -i in.mp4 -c:v libx264 -crf 28 out.mp4      ✓ encoded
```

- **Adopt**: `/fluent adopt <program>` reads the help of the program and of each of its
  commands, plus its man pages, into a card (commands, options, which take a value, a
  risk class per command). git, gh, docker, ffmpeg, curl, tar, jq and rsync each adopt in
  under 5 s, with a live progress message.
- **Guard**: `pre_tool_call` on `terminal` blocks a command that uses a long option the
  installed program doesn't have, with the closest real one, so the agent fixes it on the
  next turn instead of failing and retrying.
- **Ask**: commands it classifies as destructive go to Hermes's own approval prompt.
- **Learn**: when an unknown program rejects an option, it offers once to adopt it.
- **Grow**: a dashboard tab draws the agent's tree (a branch per program, a fruit per
  error caught); `@cli:<program> [command]` puts a card into the conversation.

Reliability: 311 real-world valid commands across 8 programs are never blocked; 17
typical AI mistakes are all caught with the right fix; 542 tests. It only judges long
options, on commands read with high confidence, for the exact binary that will run, on
the local backend; it is silent otherwise.

![Your agent's tree](https://raw.githubusercontent.com/Bruno-coder21/fluent/182c4301f2437e784e9022f1f38576e1d68c3f5f/docs/screenshots/agent-tree.png)

## Hermes surfaces used

- Hooks: `pre_tool_call` (block / approve escalation), `post_tool_call` (learn offers),
  `transform_terminal_output` (warn-mode note). All wrapped so they never raise.
- Slash command `/fluent` (`ctx.register_command`), context reference `@cli:`
  (`ctx.register_context_reference`), live messages (`ctx.post_message` / `edit`).
- Dashboard tab (`dashboard/manifest.json`, plain IIFE using the plugin SDK) and one
  read-only backend route `GET /api/plugins/fluent/summary` (runs off the event loop).
- Imports: `plugins.plugin_storage`, `agent.context_references`,
  `hermes_cli.config.load_config_readonly` (all on the public list). No core overrides.

## Disclosure (rule 13)

- `/fluent adopt <program>` **runs that program on the host** (not the terminal backend)
  with `--version`/`-version`/`version`/`-V` and `--help`/`-h`/`help`, plus
  `<command> --help` per subcommand **only when the help carries a git, Go/cobra,
  argparse or click marker** (git: `--list-cmds=main,nohelpers` and `<command> -h`;
  ffmpeg: `-hide_banner -h full`; curl: `--help all`; `git filter-branch` is never run).
  No shell, closed stdin, empty temporary cwd, own process group killed on timeout,
  filtered environment (`PATH`, `HOME`, `USER`, `LOGNAME`, `TMPDIR`, XDG dirs; no keys or
  tokens), 5 s per call, about 25 s per program. A program that ignores those arguments
  runs normally; the README says to adopt only programs you trust to print help.
- Reads man pages from the standard man directories and `terminal.backend` from config.
- In `block` mode (default) it vetoes commands with options the installed program lacks.
- Escalates destructive commands to Hermes's approval prompt with a per-subcommand rule
  key (`fluent:<program>:<command>[:<option>]`); never approves, skips or disables an
  approval; skips what Hermes core already asks. Unattended runs follow Hermes policy
  (default deny).
- Posts one-line notices in the conversation; writes only under
  `<HERMES_HOME>/plugin-data/fluent/`; no network, model or telemetry calls.

## Checks

- `hermes plugins validate --install-deps` on a clean clone at the pinned SHA: passed
  (security scan `safe`, no core override).
- `python3 scripts/validate_plugin_catalog.py plugin-catalog/fluent.yaml`: OK.
- Submitted by the repository owner (rule 5).

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: add hermes-rescue (Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150015
State: open; created 2026-11-06T11:42:45Z

**Hermes Agent Plugin Hackathon entry.**

Rescue keeps the agent from breaking Hermes and says what really went wrong. It targets two open pain clusters: #144562 (agents destructively "repairing" their own install) and #147620 (failure notices that hide the cause the product already knows).

**What it does**
- Refuses agent tool calls that would delete or hand-edit Hermes's own data (sessions, state.db, memories, skills, settings, profiles, keys) and names the supported command instead. Refusals hold in YOLO mode.
- Sends edits to settings, SOUL.md or memory files to Hermes's approval gate with a snapshot first; `/rescue undo` or one click in the Desktop pane puts them back.
- When a reply fails or quietly comes from a backup, adds one plain line per attempt with the real cause and the fix.

**Surfaces:** `pre_tool_call` (block / approve), `post_tool_call`, `api_request_error`, `post_api_request`, `transform_llm_output`, `on_session_end`; a `/rescue` slash command (uses `ctx.ask_choice` and `ctx.post_message`); a Desktop half (`desktop/plugin.js`: status-bar chip + pane) with a `dashboard/plugin_api.py` backend.

**Disclosures:** reads tool-call arguments; writes `plugin-data/hermes-rescue/rescue.db` and snapshots under `plugin-data/hermes-rescue/snapshots/` (never `.env`, `auth.json` or the other credential stores Hermes lists); undo of `state.db` only adds back missing conversations and messages; a short-lived background thread posts the failed-turn note with `ctx.post_message`; never auto-approves; no network, shell or model calls, no stored credentials, no telemetry.

**Validation:** `scripts/validate_plugin_catalog.py` passes for the entry (and the whole catalog). `hermes plugins validate --install-deps` passes at the pinned commit (security scan safe, desktop surface OK, no private core imports). 218 tests on Python 3.11, 3.13 and 3.14. Run end to end against real Hermes on Linux with a scripted model (`demo/run_demo.sh`), and on Windows in Hermes Desktop v0.23.0 with a real model (screenshots in the entry).

**Found while building:** a turn that runs out of retries returns before `finalize_turn`, so neither `transform_llm_output` nor `on_session_end` fires for it, although the hooks doc says `on_session_end` always fires. Rescue works around it with `post_message`; happy to open an issue.

## catalog: add ChangeFreeze
https://github.com/NousResearch/hermes-agent/pull/149474
State: open; created 2026-11-05T12:33:06Z

## Summary
Adds **ChangeFreeze** to the community catalog. Submitted by arults.

## What it does
An AI helper can ship code at a bad time and break something that is live.

You set a quiet window. During that window, Hermes asks you before it ships. Everyday work still runs. When the window ends, shipping continues again.

Short demo: https://github.com/arults/hermes-changefreeze/releases/download/v0.1.0-demo/changefreeze-demo.mp4

Project: https://github.com/arults/hermes-changefreeze

## Maintainer note
The catalog file pins the project revision. Upstream checks on that revision passed, including the security scan (safe).

## Hackathon
NousResearch Hermes Agent Plugin Hackathon (due 2026-11-11 17:00 EST).

## Add Excubitor plugin to catalog
https://github.com/NousResearch/hermes-agent/pull/150261
State: open; created 2026-11-06T19:49:30Z

## Plugin

**Excubitor** — night sentry for Hermes turns.

One per-turn SQLite ledger that:

1. Dedups inbound gateway replays (`pre_gateway_dispatch`)
2. Blocks no-progress tool loops (`pre_tool_call` / `post_tool_call`)
3. Enforces day/session USD spend caps
4. Alerts when a turn hangs past a reply deadline

## Surfaces

- Hooks listed in `plugin-catalog/excubitor.yaml`
- Optional Hermes Desktop status-bar chip (`desktop/plugin.js`)
- `/excubitor` status command

## Risk / disclosure

- Default notifier is log-only; optional `ntfy` / webhook only if configured
- One background watch thread; SQLite under plugin-data; no credentials or telemetry
- Fail-open on internal errors (never takes Hermes down)
- Limitation: `event.internal` bypasses gateway hooks (documented)

## Evidence

- Public repo: https://github.com/catalystberry842-alt/excubitor
- Pinned SHA: `b4e8345db04e6736a6b9379c85033ebeb4cad61b`
- CI green on that pin; live scenarios A–G pass (see repo `AUDIT.md` / `docs/evidence`)

Hackathon entry for the Hermes Agent Plugin Hackathon.


## plugin-catalog: add word-miner (vocabulary + spaced repetition from any text)
https://github.com/NousResearch/hermes-agent/pull/150545
State: open; created 2026-11-07T06:58:02Z

Adds `plugin-catalog/word-miner.yaml`.

**What it does:** turns lyrics, subtitles, articles or chat into a personal vocabulary deck and runs short daily spaced-repetition sessions inside Hermes (any language pair). SM-2-like scheduler with response-time adjustment, 3+3+3+1 sessions, two-stage graduation, append-only event log. Tools `deck_add_words`, `deck_session`, `deck_grade`, `deck_stats`, slash `/deck`, bundled mining skill, Desktop flashcard page.

**Disclosure:** local only — stores decks and review history in `$HERMES_HOME/plugin-data/word-miner` (SQLite). No outbound network calls, no shell commands, no credentials, no background processes. Desktop page uses only the plugin SDK.

**Hermes surfaces:** see `capabilities` in the entry; all through `register(ctx)` public APIs, no core overrides (`hermes plugins validate . --install-deps` passes at the pinned SHA; catalog validator OK).
**Requires:** see `requires_hermes` (also declared in `plugin.yaml`).
**Hackathon:** submitted to the Hermes Agent Plugin Hackathon. Demo video link will be added here.

## feat(plugin-catalog): add valun (Hermes Agent Plugin Hackathon)
https://github.com/NousResearch/hermes-agent/pull/150363
State: open; created 2026-11-06T23:56:53Z


**Valun** lets a Hermes agent make service-for-credit deals with *other, independently controlled* agents. You tell
your agent what you want and your limits; it finds a counterparty, negotiates, signs every commitment with **its own
key generated on your machine**, delivers or reviews the work, and on accepting a delivery **issues a credit note**
that a real [Basis](https://github.com/BetterMoneyLabs/basis-tracker) tracker records. The owner's limits are enforced
by the server at every action; the agent cannot talk its way around them.

What it does that a prompt or a skill cannot:
- **Its own key, kept out of the conversation.** `hermes valun join` generates a secp256k1 key locally (pure-Python Basis
  Schnorr signer, checked against Basis's official test vectors) and stores it in the profile's secrets; tools sign with
  it and never return it. (With Hermes's local terminal toolset enabled a model could read profile secrets through shell
  commands; see the disclosure.)
- **Limits enforced outside the model.** Owner ceilings (per deal, total owed, minimum price, counterparties, expiry,
  payer coverage) plus stricter limits the agent records from your conversation (`valun_set_limits`) are checked by the
  server; loosening a recorded limit asks you.
- **Verify, then sign.** The plugin recomputes terms hashes, checks the counterparty's signature against its registered
  key, checks credit-note templates against its own record, and measures deliveries against the agreed terms (word
  count, number of links, whether link domains exist) for both the seller before sending and the buyer before accepting.
- **One-command onboarding and a doctor.** `hermes valun join` (invite to working agent) and `hermes valun doctor`.

Experimental, stated everywhere: PC (pilot credits) are synthetic with no monetary value; the pilot tracker has no
blockchain connection and no reserve; an issued credit note is an outstanding promise; **nothing is settled**.

## Hermes surfaces used
- 9 tools (toolset `valun`): `valun_status`, `valun_directory`, `valun_inbox`, `valun_deal`, `valun_propose`,
  `valun_respond`, `valun_deliver`, `valun_review_delivery`, `valun_set_limits`. Tools other than `valun_status` are
  hidden (check_fn) until the agent is connected.
- 1 hook, `pre_tool_call`: with `confirm_commitments` on (default), signing tools and loosening a recorded limit return
  Hermes's own approval directive with the exact terms; under cron and other unattended runs Hermes denies them. The
  plugin never bypasses approvals.
- 1 CLI command, `hermes valun join | enroll | status | doctor`, run by the person in a terminal (refuses inside an agent
  session).
- Secrets only through Hermes: read with `agent.secret_scope.get_secret`, written with `hermes config set`.

## Disclosure (catalog rule 13)
- **Network calls:** the Valun server in `server_url` (default `https://valun-desk.fly.dev`, run by the Valun project):
  participant id, signed statements, deal content the agent shares, and the goals/limits it records (private to the
  participant). DNS lookups (no page fetch) of the host names of links in a delivery being reviewed or sent
  (`check_link_hosts`, default on). No telemetry.
- **Stored credentials:** `VALUN_AGENT_TOKEN` and `VALUN_SIGNING_SECRET` in the profile's `.env`, written by
  `hermes valun join` / `enroll` through `hermes config set`. The owner token is shown once (or written to a file the
  person names) and never stored by the plugin.
- **Local data:** `plugin-data/valun/issued-notes.json` (the agent's own record of credit notes it issued; no secrets).
- **Shell commands:** only `hermes valun join` / `enroll` run `hermes config set` (argument list via `sys.executable`,
  no shell). `join --direct-tools` also sets `tools.tool_search.enabled off` in that profile.
- **Background processes / self-updates / binaries:** none.


## Entry
`plugin-catalog/valun.yaml` (one file): repo https://github.com/fitzss/hermes-plugin-valun, pinned at
`f504d2660727bf90ee1375e6b071acd5c6b63de5` (version 0.2.0), maintainer `fitzss` (repository owner), tier `community`,
category `tools`, `requires_hermes: ">=0.22.7"` (also declared in `plugin.yaml`). MIT licensed; standard library only, no
binaries. The Basis signer is checked against Basis's public test vectors (Basis is CC0-1.0).

## How to test
1. `hermes plugins validate <checkout at f504d266> --install-deps`
2. `hermes plugins install https://github.com/fitzss/hermes-plugin-valun --enable` (press Enter at the two secret prompts),
   then `hermes valun doctor`.
3. Joining the live pilot needs an invite code from the operator; reviewers can ask for one in this PR.

## Checks
- `scripts/validate_plugin_catalog.py plugin-catalog/valun.yaml`: OK.
- `hermes plugins validate --install-deps` at the pinned commit: passes (security scan safe; declared tools and hooks
  match registrations; no core override). 20 offline unit tests pass (signer test vectors, delivery measurements, limit
  logic).
- Installed from the public URL into a fresh Hermes home (Windows 11, Hermes v0.22.7): enabled at the pinned commit;
  `doctor` runs.
- End-to-end on the live pilot (earlier commits with the same tools): install into a clean profile, `hermes valun join`,
  `doctor`, and autonomous deals between separately configured Hermes agents (negotiation, a credit refusal under a
  coverage policy, deliveries refused by the plugin until they met the terms, credit notes recorded and reconciled).
- Known issue, disclosed in `known_issues`: on Windows, Hermes v0.22.7 fails to enable a git-installed plugin when the
  Hermes home path is longer than 44 characters (MAX_PATH); not specific to this plugin.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: add reapx (Hermes Agent Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150004
State: open; created 2026-11-06T11:22:27Z

**PR title (draft):** `plugin-catalog: add reapx at 1.0.0`
**Entry file:** `plugin-catalog/reapx.yaml` — one file; `sha` pinned to a full 40-character commit (the post-trim head); `version: "1.0.0"` (matches `plugin.yaml`); `requires_hermes: ">=0.22.6"`. **Repo:** `https://github.com/BigBossRabbit/reapx` (pinned).

**What it does.** ReapX turns the bookmarks you saved on X into registered Hermes skills — without the paid X API. `reapx_harvest` runs harvest → map → categorize → two-track assess (integrate-into-your-makeup / business-opportunity) → generate → register (`reapx:<name>`), incrementally via a persistent seen-ledger, with an optional LLM-enrichment layer (map / categorize / assess) that runs through the host (`ctx.llm`) and a deterministic rules engine as the bit-for-bit fallback — and `reapx_review` so everything LLM-shaped lands in front of a human before it is relied on. It hands the agent a skill it did not have 60 seconds earlier (handler-time `register_skill`, live in the same session) — more than a prompt or a skill could do: four tools, host-owned LLM calls, and capability the agent gains mid-session.

**Which Hermes surfaces it uses** (per `plugin.yaml`): **4 tools** — `reapx_harvest` (browser mode, the product), `reapx_import` (export mode), `reapx_status` (read-only), `reapx_review` (read-only, item by item) — `provides_hooks: []`; **1 registered auxiliary LLM task** (`reapx_enricher`); 1 bundled index skill (`reapx:index`); 1 optional automation blueprint (`reapx:harvest` — a ready-made cron job you must explicitly schedule); zero override arguments ever passed (no `tools.override`, no provider/model/agent/profile overrides on `ctx.llm`); `requires_env`: **none** (no credentials at all); `config_schema` settings form (harvest mode, browser, browser profile, max scrolls, import dir, enrichment engine, LLM items per run, skills per category, register generated skills); `python_dependencies`: jinja2 + websocket-client; `requires_hermes: ">=0.22.6"`.

**Rule-13 disclosure list** (what a user would want to know before installing):

- **Network calls to third-party services:** **x.com** (harvest mode only) — pages of *your own* account (`x.com/i/history`), read through your own logged-in browser session (a read-only copy of your browser's `Cookies` file, a temporary headless browser, deleted after the run). **No paid X API. No other websites. No telemetry, no usage reporting, no phone-home of any kind.** **Your LLM provider** (only if `enrich: llm`, the default): the map / categorize / assess stages send bookmark text (public tweet content) through the **Hermes host** (`ctx.llm`) to your active provider/model, host-owned credentials — **the plugin never sees or stores any key**. `enrich: rules` = zero LLM calls. **GitHub is never contacted** by the plugin.
- **Reads outside the plugin's own data:** (harvest mode) your browser's **`Cookies` SQLite file** — read-only, copied to a temporary profile, source never modified; **never decrypted; no cookie value is ever read, logged, printed, or persisted**; expired logins fail as a clean error. (harvest mode) browser **install locations** (app bundles / PATH / Windows roots) to find the browser binary, and **profile directory names** (never contents) for cookie-store resolution. (export mode) **one file you point `reapx_import` at — nothing else.** (both) the plugin's own plugin-data store (ledger, registry, generated skills). **No keychain, no auth.json, no .env, no other tool's login is ever read.**
- **Shell commands / processes:** (harvest mode) launches **your own browser binary, headless**, with a remote-debugging flag on a **random free port** against the temporary profile; terminated (then killed) and the profile deleted in a `finally` block — no orphan processes, no `pkill`, no hardcoded ports. **No other commands are run; no shell-out to other CLIs.**
- **Long-running background processes:** **none of the plugin's own.** A harvest runs inside a tool call (bounded by the max-scrolls hard cap) while you watch. The optional automation blueprint (`reapx:harvest`) is a ready-made cron job you must **explicitly schedule**; it runs non-interactive by design (an expired login is a reported error, never a hang).
- **Stored credentials:** **none.** The plugin stores no keys, tokens, or cookies. LLM credentials are the host's (`ctx.llm`); the browser session stays in your browser (a deleted temp copy excepted); the X API is not used.
- **Data + writes:** everything the plugin writes lives in its own plugin-data store (survives plugin updates): harvested bookmarks, the seen-ledger, generated skills, assessment output. **Nothing is uploaded anywhere** (the optional LLM enrichment above excepted). Uninstalling the plugin leaves your data; removing the data dir removes everything.
- **Lineage (rule 16):** derived from **starlearner-nexus** (same owner) — different transport (the logged-in-browser bookmark harvest vs the GitHub REST stars API), different harvest engine (browser locator, CDP launcher, the scroll-to-exhaust fetcher, the bookmark→schema mapper), and the capability the original lacks (X bookmark capture, session-liveness detection). Disclosed here and in both READMEs.
- **Browser seam (a design point, disclosed):** the repo carries a **draft issue** asking the hermes-agent maintainers for a proper, consented browser-session capability; the day a real one exists, browser mode gates on it. The settings-form row is the consent-at-configure surface; this PR and the README disclose everything.

**Screenshots:** **none — no UI.** The agent chat is the surface (tool calls and results). Nothing to show.

**Version:** `1.0.0` · **Repo:** `https://github.com/BigBossRabbit/reapx` (pinned full 40-char sha) · `requires_hermes: ">=0.22.6"` · MIT.


## plugin-catalog: add hindsight-curator (bulk curation of stale Hindsight memories)
https://github.com/NousResearch/hermes-agent/pull/150546
State: open; created 2026-11-07T06:58:07Z

Adds `plugin-catalog/hindsight-curator.yaml`.

**What it does:** finds stale or contradicted Hindsight memories by topic, shows a dry-run plan, invalidates them in bulk with a reason, writes one checkpoint fact with the current truth, and restores from a local journal. Tools `curate_scan/plan/apply/restore/checkpoint/history`, slash `/memory-curate`. Separate from the listed `hindsight` provider plugin (does not replace or patch it); uses only Hindsight's public HTTP API.

**Disclosure:** network calls only to the configured Hindsight base URL (list/GET, PATCH invalidate/restore, retain one checkpoint). Optional Bearer auth via `HINDSIGHT_API_KEY` read through Hermes secrets. Writes invalidations/restores/checkpoint to that server (apply requires an explicit plan id; dry run by default). Stores plans and apply journal in plugin-data. No shell, no daemons, never reads other plugins' config or credential files.

**Hermes surfaces:** see `capabilities` in the entry; all through `register(ctx)` public APIs, no core overrides (`hermes plugins validate . --install-deps` passes at the pinned SHA; catalog validator OK).
**Requires:** see `requires_hermes` (also declared in `plugin.yaml`).
**Hackathon:** submitted to the Hermes Agent Plugin Hackathon. Demo video link will be added here.

## plugin-catalog: archytan-lite 0.1.0 (Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150099
State: open; created 2026-11-06T14:38:02Z

Adds **archytan-lite** 0.1.0, my entry for the Hermes Agent Plugin Hackathon. One file: `plugin-catalog/archytan-lite.yaml`, pinned to [`3874816`](https://github.com/High-ArchyTech-Solutions/hermes-archytan-lite/tree/38748165b089f776acf9d6119eaeafdb76eed83e).

Every tool call Hermes makes goes to Archytan Lite, an authorization gate running in its own container with its own Ed25519 key, before the tool runs. Hermes asks, the gate decides, and only an ALLOW lets the call through. Every decision, allowed or refused, is a signed, hash-chained receipt you can check later without trusting Hermes or the plugin.

**Demo (75 s, on X):** https://x.com/HighArchyTech/status/2118745676712423467

### How it works
- A `pre_tool_call` hook turns each call into checks on what it touches: file paths; each program and git subcommand a terminal command runs (`git/push`), plus the paths, redirects and URLs it names; hosts for `web_extract`; tool names for MCP, browser, `execute_code`, admin and unmapped tools. Every check must be allowed.
- Each ALLOW carries a single-use capability. The plugin authorizes every check first and redeems them only when all passed, right before the tool runs, so a refused call spends nothing.
- Refusals use the `block` directive, so they hold under `/yolo` and `approvals.mode: off`. The message tells the model not to retry or route around it.
- Relative paths resolve against the workspace and the resolved path is handed back with `modify`, and every terminal command runs in the directory it was checked in, so what was checked is what runs.
- A command the plugin can't read precisely (`$VAR`, `$(...)`, backticks, here-docs, loops, a `cd` part-way through) is refused as `unreadable-command`. An error in the hook, an unreachable gate, a bad signature or a receipt that doesn't match the request refuses the call.
- `hermes archytan setup|status|log|verify|reload|policy` and `/archytan`. `verify` runs the gate's `--verify-chain`, which names the exact receipt where anything was edited, reordered or removed.

### The agent can't loosen it
The policy, callers file and signing key live under `plugin-data/archytan-lite/` and in a Docker volume, outside the workspace the starter policy lets the agent write. File writes, shell redirects and every path a command names are checked. `docker`, `hermes`, interpreters, `execute_code`, the browser, `cronjob_manage create`, `skill_manage`, kanban writes and `manage_catalog`/`manage_connections` are refused by the starter policy. Writes under `.git` need a separate grant, because hooks and `core.fsmonitor` are commands git runs later. Kanban writes are refused because another profile's worker picks them up and that profile may not run the plugin.

### Disclosure
- The gate is proprietary software by the plugin's maintainer (High ArchyTech Solutions), free under its [Community license](https://github.com/High-ArchyTech-Solutions/archytan-lite-community/blob/main/ARCHYTAN-LITE-LICENSE.txt). Image `ghcr.io/high-archytech-solutions/archytan-lite@sha256:205703a7fc67a9e96aa0930fd9dda83fe2b9694b724b13dea8c1854948e82071` (2.7.1, amd64 and arm64). The plugin never pulls it unless the user passes `--pull`; the README tells users to pull it themselves. Public home, release notes and schemas: [archytan-lite-community](https://github.com/High-ArchyTech-Solutions/archytan-lite-community).
- Only `hermes archytan setup|reload|verify` and `/archytan verify` run anything: `docker`, with only PATH, HOME and Docker's own environment variables. Setup creates the volume `archytan-hermes-data` and the container `archytan-hermes` (`--restart unless-stopped`, port bound to 127.0.0.1:8431).
- Network: the hook sends each gated call's action, resource id (path, program, host or tool name) and `hermes:<session id>` to that local gate. Never argument contents or results. No telemetry.
- Credential: setup stores the caller token through `hermes_cli.config.save_env_value_secure` as `ARCHYTAN_LITE_HERMES_TOKEN`; the hook reads it with `get_secret`. The callers file holds only its SHA-256.
- Files: policy, callers, public key and a capped `decisions.jsonl` (tool, action, resource, decision, trace id) under `plugin-data/archytan-lite/`.
- No Python dependencies: `lite_client.py` is the gate's MIT client (`archytan-lite` 2.1.1 on PyPI, same authors) copied byte for byte, and a test holds it to the published file's hash. It needs only `httpx` and `cryptography`.
- Until setup has run, every gated tool call is refused, by design.

### Tested
- Unit tests for the command reader and the tool mapping, and live tests against throwaway gates from the pinned image: real ALLOW and BLOCK, a wrong public key, a wrong token, an unreachable gate, a gate without capabilities, an unexpected policy hash, a capability spent before the plugin's own redeem, rate limits, a policy reload changing both the decision and the signed policy hash, and a receipt edited in SQLite caught by `--verify-chain`.
- `tests/test_in_hermes.py` loads the plugin with Hermes 0.22.6's own plugin manager and sends calls through `model_tools.handle_function_call` with `HERMES_YOLO_MODE=1` and `approvals.mode: off`: refused calls don't run, allowed ones run on the checked path.
- Mutation checks: each security line was weakened in turn and the suite failed on every one.
- Live on Hermes 0.22.7 (Windows 10, Docker sandbox terminal backend, claude-sonnet-5) in a separate profile with `--yolo`: `git commit` ran, `git push`, `rm -rf build`, `python -m pytest`, `execute_code` and reading `/etc/passwd` were refused, and `hermes archytan verify` checked all 31 receipts.
- `hermes plugins validate` passes at the pinned commit (security scan: safe).



## plugin-catalog: add starlearner-nexus (Hermes Agent Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150059
State: open; created 2026-11-06T12:56:54Z

**PR title (draft):** `plugin-catalog: add starlearner-nexus at 1.2.0`
**Entry file:** `plugin-catalog/starlearner-nexus.yaml` — one file; `sha` pinned to a full 40-character commit; `version: "1.2.0"` (matches `plugin.yaml`); `requires_hermes: ">=0.22.6"`. **Repo:** `https://github.com/BigBossRabbit/starlearner-nexus-hermes-skill` (pinned).

**What it does.** StarLearner-Nexus turns the repositories you star on GitHub into a living library of registered Hermes skills. `starlearner_sync` runs fetch → map (the LLM curation pass) → categorize → two-track assess (integrate-into-your-makeup / business-opportunity) → generate → register (`starlearner-nexus:<name>`), incrementally via a persistent seen-ledger (a repo is never processed twice), with the optional LLM enrichment running through the host (`ctx.llm`), a deterministic rules engine as the bit-for-bit fallback, and `starlearner_review` putting everything LLM-shaped in front of a human. It hands the agent a skill it did not have 60 seconds earlier (handler-time `register_skill`, live in the same session) — more than a prompt or a skill could do: three tools, one auxiliary LLM task with host-owned credentials, and capability the agent gains mid-session.

**Which Hermes surfaces it uses** (per `plugin.yaml`): **3 tools** — `starlearner_sync`, `starlearner_status`, `starlearner_review` (status/review read-only) — `provides_hooks: []`; **+ 1 registered auxiliary LLM task** (`starlearner_enricher`); 1 bundled index skill (`starlearner-nexus:index`); 1 optional automation blueprint (`starlearner-nexus:sync` — a ready-made cron job you must explicitly schedule); zero override arguments ever passed (no `tools.override`, no provider/model/agent/profile overrides on `ctx.llm`); **1 declared `requires_env` secret** (`STARLEARNER_GITHUB_TOKEN`, the rich format: name + description + the PAT-creation doc URL + `secret: true`) read **only** through the host's secret scope; `config_schema` settings form (enrichment engine, LLM items per run, skills per category, max star pages, register generated skills); `python_dependencies`: jinja2 + requests (the fetch is **in-process** — no `gh`, no `curl`, no `jq`, no subprocess); `requires_hermes: ">=0.22.6"`.

**Rule-13 disclosure list** (what a user would want to know before installing):

- **Network calls to third-party services:** **api.github.com** (one endpoint): `GET /user/starred` — the repositories **you** have starred — authenticated with **your** read-only GitHub token, over HTTPS, paginated, bounded (the max-pages hard cap). **Nothing else on GitHub is called.** **Your LLM provider** (only if `enrich: llm`, the default): the map / categorize / assess stages send **public repo metadata** (name, description, topics, language, stars) through the **Hermes host** (`ctx.llm`) to your active provider/model, host-owned credentials — **the plugin never sees or stores any key**. `enrich: rules` = zero LLM calls. **No telemetry, no usage reporting, no phone-home of any kind.**
- **Reads outside the plugin's own data:** **none.** No browser, no cookies, no other applications' files, no other tool's login. (The plugin's own plugin-data store + one setting-declared token are the only things it touches.)
- **Shell commands / processes:** **none.** The GitHub fetch is an in-process HTTPS request; no `gh`, no `curl`, no `jq`, no subprocesses of any kind. (The standalone mode's `gh`-CLI option and curl script are not part of the plugin.)
- **Long-running background processes:** **none of the plugin's own.** A sync runs inside a tool call (bounded: a per-page timeout, the max-pages hard cap). The optional automation blueprint (`starlearner-nexus:sync`) is a ready-made cron job you must **explicitly schedule** — non-interactive: a missing token, a rate limit, or a 401 is a reported error, never a hang.
- **Stored credentials:** **one, and the plugin doesn't store it.** Your GitHub token is a `requires_env` secret: prompted (hidden) at `hermes plugins install`, **saved by Hermes** to the active profile, and read back only through the host's secret scope (`agent.secret_scope.get_secret`) — profile-scoped, never a bare environment read, never in the plugin's files, logs, errors, or results. It leaves your machine only to `api.github.com`, in the `Authorization` header of `GET /user/starred`. A **read-only** token (classic `public_repo`, or a fine-grained read-only public-repos token) is all it needs. LLM credentials are entirely the host's.
- **Data + writes:** everything the plugin writes lives in its own plugin-data store: the raw stars fetch, the seen-ledger, generated skills, assessment output. Your starred-repo list (public repo metadata) stays on your machine (LLM enrichment excepted + disclosed). Uninstalling the plugin leaves your data.
- **Lineage (rule 16, the other side):** origin of the **reapx** entry (same owner; reapx is derived from this plugin, replaces the GitHub-stars transport with a logged-in-browser bookmark harvest, and discloses that in its entry).

**Screenshots:** **none — no UI.** The agent chat is the surface (the hidden token prompt at install + tool calls and results). Nothing to show.

**Version:** `1.2.0` · **Repo:** `https://github.com/BigBossRabbit/starlearner-nexus-hermes-skill` (pinned full 40-char sha) · `requires_hermes: ">=0.22.6"` · MIT.


## plugin-catalog: add pow-tracker (Hermes Agent Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150003
State: open; created 2026-11-06T11:22:24Z

**PR title (draft):** `plugin-catalog: add pow-tracker at 0.3.0`
**Entry file:** `plugin-catalog/pow-tracker.yaml` — one file; `sha` pinned to a full 40-character commit; `version: "0.3.0"` (matches `plugin.yaml`); `requires_hermes: ">=0.22.6"` (never newer than the current release). **Repo:** `https://github.com/BigBossRabbit/pow-tracker` (pinned).

**What it does.** POW Tracker is multi-client proof-of-work time tracking that lives in the Hermes web dashboard. Each client is a folder with its own SQLite time database inside it; entries are OPEN (a timer running) or CLOSED (duration fixed); invoices aggregate billable time per task with per-entry rate overrides, exportable as CSV (PDF via an optional extra); and a background auto-capture thread opens and closes `auto` entries from file activity while you work. It has run a real multi-client operation in production since August, and no client data ships with the tree. That is more than a prompt or a skill could do: zero tools, a whole live dashboard, a background capture thread, and local per-client billing — and it registers nothing.

**Which Hermes surfaces it uses** (per `plugin.yaml`): the **dashboard block** — `dashboard/plugin_api.py` (a FastAPI router the dashboard host mounts at its plugin API route), `dashboard/plugin.js` (the pane/tab), `dashboard/manifest.json` (the web-dashboard host's discovery manifest) — plus a `config_schema` settings form (clients root, legacy clients root for migration, ignored folders, default rate, currency, company — all generic defaults). **0 tools, 0 hooks, 0 middleware**: `register(ctx)` registers nothing; `capabilities: []` is empty *on purpose* (rule 06: declared capabilities match reality — nothing more, nothing less). `python_dependencies`: fastapi + pydantic (reportlab stays an optional, lazily-imported extra for PDF). `requires_hermes: ">=0.22.6"`.

**Rule-13 disclosure list** (what a user would want to know before installing):

- **Network calls to third-party services:** none. The plugin makes no outbound network requests of any kind. No telemetry, no usage reporting.
- **Reads outside the plugin's own data:** the configured clients-root tree — **file modification times only**; file names and contents are never read, recorded, or sent anywhere. The folders walked can be limited per client (each client DB's own settings).
- **Shell commands:** none.
- **Long-running background processes:** the auto-capture thread — a daemon thread inside the dashboard/gateway process, polling while the plugin is loaded. Switched off per client (each client DB's `auto_capture` setting).
- **Stored credentials:** none — no secrets used, stored, or read.
- **Data + writes:** everything it stores (the client registry and every per-client time DB) is plain SQLite inside the user's own clients tree. Nothing is uploaded anywhere. No client data ships with the tree — source only, no databases, no exports, no client names.

**Screenshots:** the dashboard gallery — track view (a timer running), entries view (live `auto` entries appearing), tasks view, invoice view (billable time grouped per task), rate tab (per-client settings), the settings form. **Generic demo data only** — no real client names, no amounts.

**Version:** `0.3.0` · **Repo:** `https://github.com/BigBossRabbit/pow-tracker` (pinned full 40-char sha) · `requires_hermes: ">=0.22.6"` · MIT.


## Add community entry: agenda-guardian (Hermes Agent Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/149965
State: open; created 2026-11-06T09:38:40Z

## What it is
`agenda-guardian` is a day and week planner for people whose discipline cannot be the plan. You write your rules once (work hours, protected time, focus window, longest stretch, tasks per day), estimate each task, and report the real time when it is done. From the third finished task of a kind, the planner multiplies your estimates by your own median error (real / estimate, clamped to 0.7-3) and says so. Tasks are placed in the free time around the meetings of any calendar source, every block states the rule it comes from (and whether you set that rule or it is still a default), and a full day says what does not fit instead of squeezing it in.

Activities that are not tasks (sport, a long call, a daily course) are placed from the numbers the user gives. Asked where they could go, the plugin reads the next days and the eight weeks before, and answers with reasons taken from the calendar itself: the evenings that were free, the weekdays that are usually taken (with the title it found as proof), how heavy a day usually is, and the days it kept in reserve. It asks about what the calendar cannot show, and writes nothing until the user says yes.

**Version 0.5 removes the last syntax the user had to learn.** It comes from reading the real Telegram exchanges of one afternoon (Hermes gateway logs and session database) after 0.3 and 0.4 were in use. Five things went wrong, and each is answered:
- **History vetoed free days.** A day the calendar showed free was left out because it was "usually taken" in the last eight weeks, so a saved Tuesday-afternoon activity found no slot and the agent rebuilt the plan by hand and wrote the events with another tool. History now only orders the days (usually-taken ones come last) and explains them; a free day is never ruled out.
- **The help taught a format language.** The full command list was sent back at least four times in one afternoon, and the user then typed `work_hours=... protected=...` and `real=90`. `/day` alone and `/day help` are now five lines with no format; `/day help all` lists the commands. The texts the agent relays no longer cite command syntax.
- **Anything but a format-free command goes to the agent.** `help`, `list`, `tasks`, `plan`, `now`, `brief`, `nudge`, `ok`, `confirm`, `undo`, `write` and `cron` stay with the plugin; every other `/day ...` (a sentence, one word, `set k=v`) is rewritten for the agent by the gateway hook.
- **Interrogation before action.** A missing time window used to be refused. It is now the user's work hours, said in the answer and never saved as if the user had given it; more sessions than days means "so many a day"; a bare duration ("1h30") answers the last question asked. The system prompt tells the agent to assume a sensible figure, say it, and let the user's yes or correction settle it, and to move an event as `day_undo` then a new proposal.
- **A command typed while the agent is answering** is queued by Hermes and reaches the agent as plain text, not the plugin. The README now says so (Limits).

It is deterministic (no model call anywhere). Reading is the default. Writing to a Google calendar is off until the user types `/day write on`; then it only adds events it marks as its own, only after a validated proposal, and it can only remove those. Optional morning brief and block reminders are two script-only (`no_agent`) cron jobs; after a written session ends, the reminder asks how long it really took, which feeds the next proposal. Onboarding starts from what the Hermes profile already has (time zone, a signed-in Google Workspace skill, existing reminders). English and French throughout.

Repo: https://github.com/Moodtuner997/hermes-agenda-guardian (version 0.5.0, MIT, Python standard library only, pinned to `94508fff2e4cc9a0a47bd67a426cce1a0dd35df5`).

## Hermes surfaces used
- `ctx.register_command("day")` (slash command) and `ctx.register_cli_command("guardian")`. The terminal command is `hermes guardian`, not `hermes day`, because `day-panel` already registers `hermes day`.
- Fifteen tools: `day_setup`, `day_add_task`, `day_plan`, `day_done`, `day_tasks`, `day_schedule`, `day_kind`, `day_habit`, `day_propose` (read-only), `day_week_plan` (read-only), `day_stage` (read-only: it only registers a proposal), `day_confirm`, `day_undo`, `day_took`, `day_week` (read-only). No tool turns calendar writing on.
- `ctx.register_system_prompt_section("agenda-guardian", ...)`: about 1,700 characters of rules for the agent (talk plainly and never ask the user for a format, give the numbers in one `day_week_plan` call and say the figures you assumed, show the reasons, ask what is planned outside the calendar, write only after a clear yes and never with another tool, never alter an event the user created).
- `ctx.register_hook("pre_gateway_dispatch", ...)`: one hook, described under Disclosure. It is guarded, so an older Hermes without it still loads the plugin.
- `ctx.dispatch_tool("cronjob_manage")` to create the two script-only jobs (only after `/day cron on`), so Hermes' own checks apply.
- A dashboard tab (`dashboard/manifest.json`, `dist/index.js`, `plugin_api.py`): today's plan, and a Week view with the user's events, what the plugin wrote (solid) and what it proposes (dashed, with reasons and answer buttons).
- No middleware, no core overrides.

## Disclosure (rule 13)
- **Network:** none by default. With `calendar=ics:https://...` it fetches that URL; with `calendar=google` or `calendar=cmd:` it runs the program you configure (no shell, 25 s timeout), which has its own network access.
- **Reads outside the plugin's own data:** the calendar source you configure (event titles, times, status), for the next days and the eight weeks before when asked for a proposal. For onboarding only: the `timezone` and `language` lines of `HERMES_HOME/config.yaml`, whether the Google Workspace skill and its `google_token.json` exist (the token is never opened), and the name and schedule of your other cron jobs in `cron/jobs.json` (prompts are not read).
- **Hook:** `pre_gateway_dispatch` receives each incoming chat message and acts on one case only: a message that starts with `/day` followed by anything but one of the format-free commands (`help`, `list`, `tasks`, `plan`, `now`, `brief`, `nudge`, `ok`, `confirm`, `undo`, `write`, `cron`). That message's text is rewritten into an ordinary request for the agent, prefixed with a pointer to the plugin's tools. It reads nothing else, stores nothing, never drops a message, and does nothing on any error.
- **Writes:** its own data folder (one SQLite file: rules, tasks, activity sheets, habits, proposals, and the record of what it wrote). Only after `/day cron on`: two small Python scripts in `HERMES_HOME/scripts/` and two cron jobs named `agenda-guardian-brief` and `agenda-guardian-nudge`. **To the user's Google calendar, only after the user typed `/day write on` and validated a proposal:** new events (up to three per session) whose description carries `[agenda-guardian:<session>:<part>]`, created and removed through the Google Workspace skill's `calendar create` and `calendar delete` on the primary calendar. It never edits an existing event. Before a deletion it checks that the event id is in its own record and that the marker is still on the event; any other id is refused without calling the calendar, and an event the user rewrote or deleted is left alone. `/day write off` stops all writing.
- **Shell commands:** only the calendar program you configure, and, with `google`, that script's `calendar create` / `calendar delete` for the writes above. **Background processes, stored credentials, telemetry, model calls:** none.
- **Approvals (rule 12):** the plugin touches no tool call; `day_schedule on` goes through `cronjob_manage`. The yes before a calendar write is collected by the agent in conversation (the system prompt section and the `day_confirm` description say so); what the plugin enforces itself is the switch the user types, recorded-events-only deletion, a 24 hour expiry of proposals, and a re-read of the slots before writing. It cannot stop another tool from writing to the calendar (see Limits in the README).

## How it differs from existing entries
- `day-panel` shows a Today page built from sections you list. It does not plan, learn or write. Different job; the CLI names are kept apart.
- `morning-briefing` is a daily newspaper (weather, calendar, news). `agenda-guardian` plans your own tasks and activities inside your own rules and calibrates against your real durations.
- `yandex_calendar` reads and writes Yandex calendars on request. `agenda-guardian` reads any source (Google Workspace skill, ICS file or URL, JSON file, or a command that prints event JSON), and writes only to Google, only events it created, only behind a user-typed switch and a validated proposal that explains itself from the user's own calendar history.

## Validation
- 107 unit tests (`python -m pytest tests -q`, no Hermes needed): calibration, planner, ICS reader, French texts, onboarding discovery, reasons from history, the refusal to delete an event the plugin did not write (the calendar is never called), rewritten and deleted events, a week of two activities placed around each other and around an appointment, written and taken back with the calendar identical to before; staged blocks written and removed, refused on a clash or an overlap; every command of the dispatcher is in the list the hook uses. For 0.5: a replay of the real request (history that calls three afternoons usually taken, three appointments that week) fails on 0.4.0 (`0 == 1` session for the saved Tuesday sport) and passes on 0.5.0; a missing window is assumed and said; more sessions than days becomes "so many a day"; the short help contains no format. A stand-in for the Google script records every call, so the tests prove which events were and were not touched.
- `hermes plugins validate` passes on a fresh clone at the pinned SHA (Windows 11, Hermes 0.22.7, `--install-deps`; declared tools and hooks match the registrations); `scripts/validate_plugin_catalog.py` passes on this entry.
- `tests/e2e_hermes.py` passes against a real Hermes install in a throwaway home: real tool calls through the registry (including `day_week_plan`, `day_stage` and a refused `day_confirm`), the hook through Hermes' own hook dispatcher, real cron creation through `cronjob_manage`, and the generated scripts run by Hermes' own script runner, without a model.
- **A real agent turn (0.5.0, Windows 11, Claude subscription provider, an invented calendar):** a request with no window for the sport and no length for the dog walk produced one `plan:week` proposal with the assumptions listed, the reasons, and no question about a format or a window. Database afterwards: one proposal, no activity sheet saved, nothing written.
- **A real write, once, on a real Google calendar** (0.3.0, the author's, through the Google Workspace skill on Linux arm64, with the author's written go for one named test session): three events carrying the marker were created, read back, then removed by `undo`. A fingerprint of the calendar's event ids over the same window was identical before and after, and writing was switched back off.
- A real proposal read eight weeks of a real Google calendar and answered in French with reasons (Linux arm64, 0.3.0).
- `platforms` lists what was tested; macOS is untested. **Not yet exercised:** the `/day <sentence>` rewrite on a live gateway message (the logs show it never fired on the real Telegram gateway, the user only typed commands), whether the real agent, which also has the Google skill and a terminal, now goes through the plugin instead of around it (the plugin cannot block another tool), the duration question sent by the reminder cron, and Telegram/WhatsApp delivery.

Happy to adjust anything.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: usage-guard 0.5.0 (Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/149796
State: open; created 2026-11-06T01:59:18Z

Bumps **usage-guard** to **0.5.0**, my entry for the Hermes Agent Plugin Hackathon.

usage-guard stops a Hermes agent at your subscription limit. It reads your plan's real usage windows through Hermes, and once a window reaches your limit it refuses the next provider call **before it is sent**, so an account that allows paid extra usage never spends overage by accident. Unattended runs (`/goal`, cron) are exactly the workload that needs it.

**Demo video (34 s):** https://x.com/mister__ideas/status/2118649143409426588

**New in 0.5.0** ([changelog](https://github.com/mister-ideas/usage-guard/blob/d59f798e848f5310f9e3d8673c01f383207c695e/CHANGELOG.md)):
- **A status-bar chip in Hermes Desktop.** A shield shows the highest usage window. It turns yellow near the limit and red when blocked, and its tooltip lists every window, its reset and your limit.
- **`/usage-guard`** prints what the guard would decide right now for each guarded provider.
- Both read the guard's own cache through a read-only route, so checking never spends a usage request.
- **Reliability fixes** so the guard never locks out an agent that is under its limit:
  - usage reads now work under a multiplexed gateway;
  - a 1% Anthropic window misreported as 100% (#139916) no longer refuses;
  - a window whose reset passed no longer refuses on the clock alone.
- The refusal states the limit plainly, and `hydrate_from_paths` is declared in the manifest.

**Hermes surfaces:** `llm_execution` and `llm_request` middleware, the `pre_llm_call` hook, a slash command, one read-only dashboard route, and a Desktop status-bar chip on the plugin SDK. It does not patch Hermes core.

**Disclosure (rule 13):**
- **It refuses requests.** Main-loop provider calls for the providers in `provider_keys` are refused at `threshold_percent`. By default (`fail_open: false`) they are also refused when the usage reading is missing, stale or malformed.
- Network: none of its own. Usage is read through Hermes's `agent.account_usage.fetch_account_usage`, at most once per source every 180 s by default.
- Data: one cache file, `plugin-data/usage-guard/usage.json` (windows, timestamps, failure reasons; never credentials). Borrowing other files (`hydrate_from_paths`) is off by default.
- The Desktop chip polls the read-only status route every 60 s and after each turn, while Desktop is open.
- Not gated on stock Hermes: auxiliary calls (compression, titles, vision, MoA advisors); #140694 would close that.
- Known issue: with several profiles on one gateway, `/usage-guard` can answer for the launch profile. The guard and the chip are correct.

**Screenshots:** in the entry's `screenshots:` and in the [README](https://github.com/mister-ideas/usage-guard/blob/d59f798e848f5310f9e3d8673c01f383207c695e/README.md).



## plugin-catalog: git-review 0.3.0 (Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/149795
State: open; created 2026-11-06T01:59:15Z

Bumps **git-review** to **0.3.0**, my entry for the Hermes Agent Plugin Hackathon.

git-review is a Git review pane for Hermes Desktop. It shows exactly what the agent changed in its last turn, next to the chat. You cite the lines that are wrong back to the agent, then stage, commit, push and open the pull request without leaving Hermes.

**Demo video (82 s):** https://x.com/mister__ideas/status/2118649092817432606

**New in 0.3.0** ([changelog](https://github.com/mister-ideas/git-review/blob/a1944377c3f8d5699668b67379be9bf63ca0cee7/CHANGELOG.md)):
- **Last agent turn is exact.** The plugin records a snapshot of the working tree when you send a message, so the turn shows only the agent's own edits, including edits to untracked files.
- **The agent drives the pane again.** `git_review_select` follows Hermes's tool contract, and with several profiles on one gateway the request reaches the pane of the profile you are chatting in.
- **Ship path.** Stage, Unstage and Discard sit in every file header. Stepping through commits never shows the previous commit under the new header. Search lists content matches in the folder tree.
- **⌘⌥G toggles the pane** where Desktop supports it (#147157). Older Desktops keep the open-only shortcut.
- It reads its settings through the public `hermes_cli.config` API (rule 9). `hermes plugins validate --install-deps` passes with no warnings.

**Hermes surfaces:** the Desktop plugin SDK (pane, status-bar count, palette action, keybinding), one dashboard plugin router, `ctx.register_tool` (`git_review_select`). It does not patch Hermes core.

**Disclosure (rule 13):**
- Shell commands: `git` subprocesses with timeouts and output caps (reads listed in the entry). For Last agent turn it also runs `git add -A` and `write-tree` against a throwaway index and an object store inside `plugin-data/git-review/turn-snapshots/`; the repository's index and objects are never written. Snapshots are pruned (newest 16, three days).
- Writes to your repository only when you click: add, restore, reset, rm, commit, push. Discard asks first. Hooks and repository-defined programs stay off unless `run_repo_programs` is set; `read_only` refuses every write.
- Network: only what you click (`git push`, `gh`/`glab` for pull requests) and the PR badge's local `gh pr list` / `glab mr list`. **Generate commit message** sends the staged diff and the last ten commit subjects to the focused chat's model through Hermes.
- Reads outside its data: authorized repositories only, this profile's `config.yaml`, and the `cwd` column of `state.db` (read-only).
- No credentials, no telemetry, no background processes. The pane polls the local backend while it is open.

**Screenshots:** in the entry's `screenshots:` and in the [README](https://github.com/mister-ideas/git-review/blob/a1944377c3f8d5699668b67379be9bf63ca0cee7/README.md).



## catalog: add screenpipe plugin (ambient recall from local Screenpipe corpus)
https://github.com/NousResearch/hermes-agent/pull/149490
State: open; created 2026-11-05T13:12:33Z

## What the plugin does

`screenpipe` gives a Hermes agent ambient recall of the user's local [Screenpipe](https://screenpi.pe) corpus (OCR screen text + audio transcripts). While the user chats, a **fail-silent `pre_llm_call` hook** matches the message against recent captures and injects up to 3 short, timestamped excerpts (opt-out killswitch, per-session cooldown, 600-char budget, 1.5 s HTTP timeout — it can never block or break a turn). Explicit surfaces: `screenpipe_search`, `screenpipe_around` (timeline summary around a timestamp), `screenpipe_status` tools, and a `/recall` slash command. Durable SQLite query cache/counters via `plugin_db()`.

## Surfaces used

- General plugin, manifest v2, `register(ctx)` — no core overrides, no patching
- `ctx.register_tool` ×3, `ctx.register_hook("pre_llm_call")`, `ctx.register_command("/recall")`
- `ctx.plugin_db()` for durable cache
- `provides_tools:` / `provides_hooks:` declared and validate-matched; zero `python_dependencies` (stdlib `urllib` only)

## Disclosures

- Integrates a third-party product (Screenpipe) — standalone repo per the third-party-product policy; repo is owner-submitted.
- Local network callers only: `http://localhost:3030` (configurable `api_url`) with 1.5 s timeouts; all failures degrade to structured errors / silent no-op.
- `requires_env: SCREENPIPE_API_KEY` (optional, `secret: true`) read solely via `agent.secret_scope.get_secret`; when unset the plugin retries unauthenticated (Screenpipe can run authless locally).
- Hook is observer-safe: returns `None` unless all relevance gates pass; never mutates tools/schemas (prompt-cache safe, tested).
- `hermes plugins validate --install-deps` passes clean at the pinned SHA `1f178730b5365192f3494fb41c50784a13df6472`; 58 pytest tests green; live smoke record in `docs/smoke.md`.

Hackathon entry (Hermes Plugin Hackathon, Nov 2026).


## catalog: add delegation-scout plugin (learning subagent router)
https://github.com/NousResearch/hermes-agent/pull/149491
State: open; created 2026-11-05T13:13:27Z

## What the plugin does

`delegation-scout` is a `delegation.backend` that routes every `delegate_task` child by task shape, then **learns**: a `post_tool_call` observer records each scout-routed outcome (status per route label) into a durable `plugin_db()` SQLite table, and `route_task` nudges future picks toward routes with a materially higher success rate (≥5 samples, ≥15-point margin — both tested at the boundary). The model sees a deterministic `mode: [auto, quick, deep]` task parameter; core owns the whole subagent lifecycle.

`scout_stats` exposes the learning as a tool: route counts, per-route success rates, recent decisions. Ships deterministic `task_parameters`/`description` (byte-stable per config — the prompt-cache rule); history lookups happen only inside `route_task`.

## Surfaces used

- `ctx.register_delegation_provider()` (public seam; documented at /docs/developer-guide/delegation-provider-plugin)
- `ctx.register_hook("post_tool_call")` — public observer seam; no middleware, no patching
- `ctx.register_tool("scout_stats")`, `ctx.plugin_db()`
- Declared via `provides_tools:` / `provides_hooks:`; zero runtime dependencies

## Disclosures

- No network calls anywhere in the plugin (routing is config-driven; `is_available()` reads config only).
- No credentials, no env reads.
- Refusals are per-task via `DelegationRouteError` with the standard fix message; a missing route class inherits the core default rather than crashing (tested).
- `hermes plugins validate --install-deps` passes clean at the pinned SHA `f33b8c87b5ade8a4e0f212239eb6467daa579681`; 39 pytest tests green incl. an e2e run through the real PluginManager on a temp `HERMES_HOME` and source-verified hook wiring (`docs/outcome-seam.md` documents the seam evidence).

Hackathon entry (Hermes Plugin Hackathon, Nov 2026).


## plugin-catalog: add vibe-relay (quota-aware delegation with gate-verified acceptance)
https://github.com/NousResearch/hermes-agent/pull/150547
State: open; created 2026-11-07T06:58:11Z

Adds `plugin-catalog/vibe-relay.yaml`.

**What it does:** vibecoding without burning your best model. A delegation provider routes `delegate_task` by live quota (parent keeps the work above a threshold, otherwise a configured cheap executor/profile). Every delegated task carries `allowed` path globs and a `gate`; `post_tool_call` captures gate PASS bound to a working-tree hash, `pre_verify` keeps the turn going until a fresh PASS exists, `vibe_accept` checks changed paths ⊆ allowed. Near the stop threshold `/vibe park` writes a handoff and creates one one-shot cron at reset+buffer (blueprint `resume-after-reset`). Bundles DEV Framework tools and a 14-skill Agent Workshop (agent build/debug loop, architecture audit, harness/evals, context budget, memory engineering, known-errors, frozen-tree review, releases, executor orchestration, field acceptance, TDD, debugging).

**Disclosure:** quota via public `agent.account_usage.fetch_account_usage(..., read_only=True)` at most once per 180 s, cached in plugin-data. `df_init` runs the vendored DEV Framework installer as a local Python child process writing framework files into the repository the agent names. Acceptance runs read-only `git status/diff/ls-files`. `df_check` never executes repo commands itself — it returns the gate command for the agent to run through `terminal` (normal approvals). Cron only on explicit `/vibe park`. No credential-file reads, no YOLO shells, no child `hermes` processes.

**Hermes surfaces:** see `capabilities` in the entry; all through `register(ctx)` public APIs, no core overrides (`hermes plugins validate . --install-deps` passes at the pinned SHA; catalog validator OK).
**Requires:** see `requires_hermes` (also declared in `plugin.yaml`).
**Hackathon:** submitted to the Hermes Agent Plugin Hackathon. Demo video link will be added here.

## catalog: add agentmail-frontdoor, odoo-prod-guard, and fleet-memory
https://github.com/NousResearch/hermes-agent/pull/149142
State: open; created 2026-11-04T23:01:51Z

## Why

Three community plugins from https://github.com/tylerjharden/hermes-hackathon-ipp. Each one is a native package with tools. Two also ship a desktop pane. One is a memory provider.

## What changed

- `plugin-catalog/agentmail-frontdoor.yaml`
- `plugin-catalog/odoo-prod-guard.yaml`
- `plugin-catalog/fleet-memory.yaml`

## Scope

Adds three community entries. Does not change Hermes core.

## Disclosures

- agentmail-frontdoor calls `https://api.agentmail.to` when `AGENTMAIL_API_KEY` is a real key. It creates drafts with `POST /v0/inboxes/{inbox_id}/drafts` and updates labels with `PATCH` on the thread. It does not call the send endpoints. `pre_tool_call` blocks sends to recipients outside the allowlist and returns an approve directive for allowlisted sends. The placeholder key `mock` stays on a local SQLite ledger.
- odoo-prod-guard calls the configured Odoo base URL over HTTPS when `ODOO_URL`, `ODOO_DB`, `ODOO_USER`, and `ODOO_API_KEY` are real. Reads use JSON-2. On `env: prod`, a write that is not on `routine_allowlist` returns an approve directive. The plugin does not approve its own calls. Placeholder secrets stay on fixture responses. The desktop pane reads gate history from the profile data directory.
- fleet-memory stores notes under the active profile `hermes_home`. With a real `NOTION_TOKEN`, `sync_turn` searches `https://api.notion.com/v1/search` on a `spawn_context_thread`. It does not create or edit Notion pages. The placeholder `mock` does not open a socket. The desktop pane shows recall counts from that local store.

Secrets are read with `agent.secret_scope.get_secret`. None of the plugins read `.env` or `auth.json`, run shell commands, send telemetry, or patch Hermes core.

## Verification

`pytest` from the plugin repo: 24 passed. Offline demos: `python plugins/agentmail-frontdoor/demo.py`, `python plugins/odoo-prod-guard/demo.py`, `python plugins/fleet-memory/demo.py`. `hermes` on PyPI in the build environment was 0.19.0, behind GitHub release v0.22.7, so `hermes plugins validate` was not run. Re-run `hermes plugins validate plugins/<name> --install-deps` on Hermes `>=0.22.0` before merge.

## feat(plugin-catalog): add citation-guard (Hermes Agent Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/150613
State: open; created 2026-11-07T09:29:34Z

## What it is

`citation-guard` catches fabricated, mismatched and retracted references before anyone relies on them.
Every reference is checked against the registries that issue the identifiers: doi.org, Crossref,
PubMed and arXiv. It reports, per reference:

- **`id_not_found`**: the DOI / PMID / arXiv id does not exist;
- **`wrong_id`**: the id exists but belongs to a different work (a real DOI glued to an invented title);
- **`retracted`**: retraction, withdrawal or removal notice (Crossref `updated-by`, which carries the Retraction Watch database; PubMed "Retracted Publication");
- **`not_found`**: no id, and no matching record in Crossref, PubMed or arXiv (fabricated, or not indexed; it says so);
- **`metadata_mismatch`**: the work exists but the year or first author differs;
- **`unchecked`**: a registry could not be reached in time. A network failure is never reported as "fake".

It is deterministic (no model call, no API key, Python standard library only).

Repo: https://github.com/ChienNguyen23/hermes-citation-guard (version 0.1.0, MIT), pinned to
`40825e81aba35c9542db1ac73bfb76191ec32145`.

## Hermes surfaces used

- `ctx.register_hook("transform_llm_output", ...)`: when a final reply contains references, a short warning footer is **appended**. The reply text is never rewritten; replies with no references, or whose references all verify, return `None`. Footer runs under a time budget (`guard_timeout_s`, default 15 s); references not checked in time are listed as not checked.
- `ctx.register_tool("verify_citations", ...)`: structured JSON per reference, including the closest real record when the cited one is wrong.
- `ctx.register_command("citecheck", ...)`: full report for a file (`.md`, `.txt`, `.bib`, `.docx`) or pasted text.

No middleware, no core overrides. Imports: `tools.registry` (`tool_result` / `tool_error`) and `plugins.plugin_storage.plugin_data_dir`, both on the public list, each with a fallback.

## Disclosure (rule 13)

- **Network:** `api.crossref.org`, `doi.org`, `eutils.ncbi.nlm.nih.gov`, `export.arxiv.org`, read-only public metadata APIs. Only the reference itself is sent (its id, title, first author and year), never the rest of the conversation. User-Agent `citation-guard/0.1.0`; the optional `contact_email` setting is sent only to Crossref and NCBI as their polite-pool contact. Requests are paced to each registry's limits (Crossref as reported in its own response headers; NCBI 3/s; arXiv one call every 3 s).
- **Reads outside the plugin's own data:** only the file a user names in `/citecheck <path>`.
- **Writes:** a 7-day cache of registry answers at `<hermes home>/plugin-data/citation-guard/registry_cache.json`.
- **Shell commands, stored credentials, telemetry:** none.
- **Background work:** none started; lookups still in flight when a reply's time budget ends finish on their worker threads and only warm the cache.
- **Approvals (rule 12):** not involved; the plugin gates no tool call.

## How it differs from existing entries

`doi-ref` (#132104, open) attaches a DOI's metadata when the user writes `@doi:...`: it enriches input.
`citation-guard` audits what the agent outputs: it finds references in the reply, also without any
identifier (title search with author/year agreement), and decides whether each one is real and correct.
No catalog entry checks references for fabrication today.

## Evidence

- `hermes plugins validate . --install-deps`: **Validation passed** (manifest, config schema, loadable, capability probe, declared tools/hooks match registrations, no built-in collisions, security scan **safe**, no core override).
- `hermes plugins doctor`: discovery, import and registration pass.
- `tests/hermes_integration.py` inside a real Hermes install: **17/17**. Tool through `registry.dispatch`, hook through `invoke_hook("transform_llm_output", ...)`, command through the plugin command table.
- `tests/test_offline.py`: 54 offline tests (extraction incl. BibTeX and agent-style lists, every verdict against a fake registry, network-down behaviour, the hook).
- Seeded error-injection benchmark on real PubMed Central references. Two disjoint samples: dev (100 references / 50 articles) and held-out (80 / 40 other articles). Each reference is checked as written and in five corrupted forms. On the **held-out set before the last fixes**: false alarms 4/160 (2.5%), corrupted references caught 97.5–100% per form. Final code: 1/200 dev and 0/160 held-out false alarms. The remaining dev "false alarm" is a real error in the source article (a 2008 reference carrying the DOI of a 2015 paper), which the plugin flags correctly. Tables and raw results in `bench/`.

## How to test

1. `hermes plugins install ChienNguyen23/hermes-citation-guard --ref 40825e81aba35c9542db1ac73bfb76191ec32145 --enable`
2. In a chat: `/citecheck` with the repo's `tests/fixtures_mixed.md` (10 references: 4 real, 2 retracted, a non-existent DOI, a real DOI on the wrong paper, an invented paper, wrong author/year).
3. Ask for "six key papers on <narrow topic> with DOIs" and read the footer under the answer.

Tested on macOS 15 (Apple Silicon), Python 3.14, Hermes main at `bd312c9`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## catalog: add blastradius (measure destructive commands before they run)
https://github.com/NousResearch/hermes-agent/pull/150476
State: open; created 2026-11-07T04:20:23Z

Adds `blastradius` to the catalog.

## What it does

Hermes asks "allow this command?" It never says what the command will destroy. This plugin measures the target before the call runs, and splits the answer into the part git can restore and the part it cannot:

```
⛔ blast radius: rm in /home/me/proj
   84 file(s), 914 bytes
   tracked by git : 3    (recoverable)
   UNTRACKED      : 81   (gone permanently)
```

That split is the whole point. `git clean -fd` deletes exactly the untracked set: the `.env`, the local database, the migration nobody committed. A regex can flag `rm -rf` as dangerous. Only opening the target can say that 81 of these 84 files are unrecoverable.

## Hermes surfaces used

- `pre_tool_call` hook. Returns `{"action": "block"}` for `terminal` calls whose destructive target can be measured (`rm`, `git clean -f*`, `git reset --hard`, `truncate -s 0`, `mv`). This is the same mechanism `plugins/security-guidance` already uses, so it adds no new privilege model.
- `blast_radius` tool. Runs the same measurement on demand and executes nothing.
- `blast_allow` tool. After the user has seen the number and said yes, it permits exactly that command once, for five minutes. The grant is spent on the next matching call and the gate closes again.
- `/blast <command>` command, for a preview without asking the agent.

No core overrides, no self-updater, no network access at runtime, no credentials.

## Relationship to what already ships

- `tools/approval_floors.py` matches command shapes and asks "may I?"
- `tools/approval_smart.py` asks an auxiliary LLM "how risky is this?"
- `plugins/security-guidance` scans the content of files being written

All three are useful and none of them opens the target directory. This entry adds a measurement, not another opinion.

## What it deliberately does not measure

Damage that happens inside a program (`python cleanup.py`), anything over SSH, `rm` inside a subshell or after a pipe, and SQL strings. Those cases are reported as unmeasured, never guessed. The README states this limit instead of hiding it.

## Verification

- `hermes plugins validate` passes, with declared tools and hooks matching registrations
- `hermes plugins doctor` passes, reporting 2 tools and 1 hook
- `hermes plugins install valenciayuna/hermes-plugin-blastradius --ref <this sha>` on a clean `HERMES_HOME` installs and validates
- `tests/blast_proof.py` runs 21 checks against a real git repo: 84 files on disk, 3 committed, 81 untracked, asserting the reported split is 3 and 81, that `git clean -fd` counts the untracked set, that a plain rename is not gated while `mv` onto an existing file is, that a confirmed command passes exactly once and the grant expires, and that read-only commands and unrecognised scripts are left alone.

## Disclosure on rule 3 (pin maturity)

The pinned commit is minutes old. This plugin was written for the Hermes plugin hackathon, whose submission window closes on 11 Nov, so a two-week-old pin is not achievable inside it. The PR is opened with a fresh pin on purpose rather than waiting. If the maintainers prefer, I can re-pin later once the SHA ages, or withdraw the entry until it does.

## Hackathon

Submitted to the Hermes Agent Plugin Hackathon. Demo video link will be added once recorded.


## feat(plugin-catalog): add OpenRouter Everything
https://github.com/NousResearch/hermes-agent/pull/150282
State: open; created 2026-11-06T20:54:42Z

## Summary

Adds OpenRouter Everything to the community catalog for the Hermes Agent Plugin Hackathon. It unifies OpenRouter-backed web search and fetch, image and video generation, text-to-speech and transcription, plus decisions, structured extraction, reranking and embeddings. Users can choose models per capability and receive warnings for known task/model mismatches.

Hermes already includes OpenRouter image and video backends; this plugin combines those use cases with web and voice providers and additional structured tools behind one key. It registers five native providers, five agent tools, a CLI and a slash command through Hermes plugin APIs.

Pinned plugin commit: `ec6974a96f9965e59d23bf1d5c5e4f2eb7333338`.

## Disclosure

- Sends prompts, documents, search queries, URLs and supplied media to OpenRouter or the operator-configured API relay, using the profile's OpenRouter key. Requests and server tools can incur charges. OpenRouter's server tools may access third-party search engines and web pages.
- Reads local reference images and audio supplied by the user, downloads generated media (including image URLs returned by the service, potentially from other hosts), and writes output files. Video generation polls its job while the request is running; no persistent background service or self-updater is installed.
- Reads Hermes configuration. CLI setup can save the key through Hermes configuration and activate the plugin's providers. Model/engine settings and the configuration agent tool can modify profile configuration, including provider selection; see the README for exact fields and override behavior.
- No extra telemetry or shell commands. Alpha endpoints use the same configured origin as the v1 API and reject unsupported base-URL formats.

## Verification

- `hermes plugins validate . --install-deps` passed against a fresh clone at the pinned commit.
- Offline regression suite: 76 tests and 31 subtests passed.
- `python scripts/validate_plugin_catalog.py plugin-catalog/` passed (existing warnings in unrelated entries).
- Plugin payload scan passed; pinned banner URL returned HTTP 200.
- Tested plugin registration and setup against Hermes v0.22.0 in an isolated profile; the catalog and manifest both require `>=0.22.0`.

The hackathon demo and entry-form submission are separate steps; this PR does not claim they are complete.


## Add zambo-receipts to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149226
State: open; created 2026-11-05T02:52:10Z

## Zambo Receipts — plugin catalog entry

Adds `plugin-catalog/zambo-receipts.yaml` for the Hermes Agent Plugin Hackathon.

**What it does.** Zambo Receipts hooks the Hermes session lifecycle. Every tool call is journaled to Zambo as it happens, and when the session ends the plugin wraps the session into a verifiable AER-1 receipt that anyone can open and check at a public link. It registers 3 tools (`zambo_verify_receipt`, `zambo_wrap_session`, `zambo_session_status`), 3 hooks (`on_session_start`, `post_tool_call`, `on_session_end`), a `/receipt` slash command, and a bundled skill. The pinned commit is the plugin repo's current `main`.

**Local gate results** (Hermes built from this repo, plugin at the pinned sha):

- `hermes plugins doctor . --ci` — OK: runtime discovery, manifest parsing, import, and registration passed (3 tools, 3 hooks)
- `hermes plugins validate . --install-deps` — Validation passed: manifest, fields, requires_hermes, config schema, requires_env, loadable, capability probe, declared tools/hooks/middleware matching registrations, no built-in collisions, security scan safe, no core override
- The plugin's own test suite: 7/7 pass

**Live proof.** A real Hermes-style session run through the shipped plugin: 4 tool calls journaled live, session auto-wrapped on end, receipt verified through the public verify API: https://zambo.dev/run/3d23c2f2-abcf-488e-ba0f-80e2eb9b4def

**Hackathon demo post:** https://x.com/brennanzambo/status/2118169960044286125

**Risk disclosure** (also in the catalog description and the plugin README):

- While enabled, the plugin sends each tool call's name, duration, result size, and a SHA-256 hash of the result to zambo.dev. Result contents are sent only when the user opts into `journal_results: "full"` (truncated to 4,000 characters).
- Failed sends buffer in a durable outbox under `$HERMES_HOME/plugin-data/zambo-receipts/` and flush later; the wrap commits the SHA-256 digest of the full local call log either way.
- A per-install caller id is stored in the plugin data directory so each install uses its own Zambo free tier. No credentials or API keys are involved.
- Zero declared Python dependencies (standard library; `requests` used opportunistically when present). No self-updating code, no core overrides, public `register_*` APIs only.


## catalog: add Hermes Strudel Studio v0.2.4
https://github.com/NousResearch/hermes-agent/pull/150357
State: open; created 2026-11-06T23:33:39Z

## Summary
Add Hermes Strudel Studio for the Nous Hermes plugin hackathon.
- Repo: https://github.com/mojomast/poptart
- Pin: `13de04319ebafa64ea1960575717718b733527b4` (`v0.2.4`)
- Subdir: `integration/hermes`; requires Hermes `>=0.22.7`
- One composable `poptart_studio` tool and Desktop SandboxedFrame pane.
- Scheduler-timed mini-notation highlighting uses the Hermes accent.

## Disclosures
- Lazily starts an authenticated Node sidecar on loopback.
- Random token stored mode 0600 under plugin-data; never sent to guests.
- Music evaluates after user Play/apply in isolated frames, not an OS sandbox.
- Patterns may fetch remote samples/CDN resources and produce browser audio.
- AGPL-3.0-or-later; bundled third-party GPL notices apply.
- No self-updater.

## Validation
YAML-only; secret scans, duplicate-key tests, catalog validator, and `hermes plugins validate` passed (one existing `invisible_unicode` caution in bundled minified JS).


## catalog: add headway (proof-of-progress circuit breaker)
https://github.com/NousResearch/hermes-agent/pull/149777
State: open; created 2026-11-06T00:53:08Z

## Summary

Add **Headway** to the plugin catalog: a proof-of-progress circuit breaker for Hermes Agent.

**Repo:** https://github.com/hanii090/headway-hermes-plugin
**Pinned SHA:** `d43e24318d8198a373b8fff147f56d0a4367301a`
**Maintainer:** hanii090 (owner)
**Tier:** community · **Category:** tools · **Version:** 0.1.0

## Problem

An agent can run varied successful terminal commands (`pwd`, `ls`, `git status`, …) and still make no progress. Exact-argument loop hashes miss this; exit code 0 means the command ran, not that the task moved. Motivating case: Hermes issue [#67889](https://github.com/NousResearch/hermes-agent/issues/67889) (terminal thrashing outside `idempotent_no_progress`).

Existing catalog / nearby work covers argument repetition ([degeneracy-guard](https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/degeneracy-guard.yaml)), consecutive-failure escalation ([escalation-governor](https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/escalation-governor.yaml)), tqdm rendering cleanup ([progress-squash](https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/progress-squash.yaml)), undo/snapshots, and near-identical command detection (PR #103180). Headway’s lane is **observable workspace/evidence novelty**, not command similarity.

## What it does

- Public `tool_execution` middleware + `pre_llm_call` (goal capture / user-turn reset)
- Deterministic local workspace fingerprints before/after terminal, file-mutation, and read/search calls
- Normalized result evidence (strip timestamps, PIDs, ANSI, absolute workspace paths)
- Read-coverage expansion counts as progress; poller-style no-ops filtered
- After configurable no-progress streaks: inject structured advisory recovery packet
- Optional **enforce** mode blocks subsequent same-class calls without executing them
- Real file write / evidence / coverage change resets the streak
- Slash `/headway` (+ reset / mode), `hermes headway status`, optional read-only dashboard API
- Atomic session/workspace-scoped JSON under `plugin_data_dir`

## Disclosure (admission rule 13)

| Topic | Detail |
| --- | --- |
| Network | None in production |
| Credentials / env | None; `requires_env: []` |
| Shell / git / subprocess | None in production plugin code. `scripts/demo.py` alone uses `subprocess` for a local demo |
| Self-updater | None |
| Core overrides | None — public middleware/hooks/slash/CLI/dashboard API only |
| Desktop | Intentionally omitted |
| Writes outside plugin data | Reads bounded local workspace for fingerprints only; state writes only under Hermes plugin data dir |
| Telemetry | None |

## Known limits (also in entry `known_issues`)

- Bounded head/tail and total-size/file-count sampling can miss workspace changes
- Only local filesystem state is measured; non-local `TERMINAL_ENV` backends are skipped; external side effects are out of scope
- Non-string tool results are preserved; advisory packets append only to string results
- No multi-process state locking

## Verification (at pinned SHA)

```bash
python3 -m pytest -q   # 37 passed
python3 scripts/demo.py  # exit 0 — varied terminal thrash → intervention; write resets streak
```

## Capabilities (must match pin)

```yaml
capabilities:
  provides_tools: []
  provides_hooks:
    - pre_llm_call
  provides_middleware:
    - tool_execution
  requires_env: []
```

## Install (after merge)

```bash
hermes plugins install headway
hermes plugins enable headway
# restart gateway/session
```

Hackathon submission context: Hermes Agent Plugin Hackathon; plugin is MIT-licensed.

## Add Gateway Guardian to plugin catalog
https://github.com/NousResearch/hermes-agent/pull/150379
State: open; created 2026-11-07T00:43:53Z

Hermes Agent Plugin Hackathon entry.

Plugin: https://github.com/kawsthingz/kawsthingz-hermes-gateway-guardian
Pinned SHA: 287a732d0501ef9b1623584f6fe49fef3e7a95a9

What it does: Telegram/gateway reliability guard for Hermes. Detects 409 polling conflicts, duplicate pollers, freezes, stale locks and missed deliveries, shows one health state (OK/DEGRADED/BLOCKED) and an approved recovery plan.

Surfaces used: ctx.register_tool for gateway_guardian_status and gateway_guardian_recover, ctx.register_command for /gateway-guardian. No hooks, no middleware, no network, no credentials.

Disclosure: read-only status by default. Recovery never restarts, kills or rebinds anything by itself; it records the intent and prints the operator plan. No message bodies are stored, only pattern counts and recovery intents. No telemetry.

Validation: unit tests pass; hermes plugins validate passes; hermes plugins doctor passes. Live status on the build box returned BLOCKED from real 409/polling log patterns.

## catalog: add hermes-persona-stickers
https://github.com/NousResearch/hermes-agent/pull/149543
State: open; created 2026-11-05T14:54:57Z

## Why
Submit `hermes-persona-stickers` to the Hermes plugin catalog for the Nous Research Hermes Agent Plugin Hackathon (Nov 2026). Goal: give Hermes a persona-consistent visual reaction voice with sub-30ms sticker stamps instead of waiting on diffusion mid-chat.

## What
Adds `plugin-catalog/hermes-persona-stickers.yaml` pinning https://github.com/EricBlack47/hermes-persona-stickers @ `20ec01721598cc335125a80be66f35fa9951de03`.

The plugin registers:
- tool `generate_persona_sticker`
- hook `post_llm_call`
- slash command `/sticker`

Surfaces: Hermes tools / hooks / commands (Telegram/Discord/Slack via `MEDIA:<path>`). Instant path uses in-repo pre-baked RGBA bases + Pillow caption overlay; optional local ComfyUI only for offline base forging.

## Disclosure (rule 13)
- Writes sticker PNG/WebP files under `~/.hermes/stickers/`
- Optional HTTP to configured ComfyUI URL (default `http://127.0.0.1:8188`) only when forge mode is used
- No third-party network, no telemetry, no self-update, no shell commands
- Ships pre-baked persona assets in the pinned commit

## Test plan
- [ ] Catalog CI `hermes plugins validate` against the pinned SHA
- [ ] Install: `hermes plugins install hermes-persona-stickers`
- [ ] `/sticker tsundere 哼！` returns `MEDIA:` path and renders

## Add write-gate to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/150594
State: open; created 2026-11-07T08:26:44Z

## What does this PR do?

Adds **write-gate** to the plugin catalog: a deterministic, dependency-free pre-write content gate for Hermes Agent.

Before a file write runs, a `pre_tool_call` hook parses the exact bytes about to be written with stdlib parsers (JSON, TOML, Python `ast`), rejects NUL bytes, oversized content and user-declared regex contracts. On failure it returns `{"action": "block", "message": ...}` with the precise line/column and the failing contract. Hermes short-circuits the tool and hands that text to the model as the tool-call error, so the agent repairs the content and retries **inside the same tool-calling loop** — no broken file is ever created, no human in the loop, no extra turn.

This is enforcement rather than an instruction: a prompt or a skill can be ignored or crowded out of context, a parser cannot.

Plugin: https://github.com/2vic1/hermes-write-gate (pinned at `7aa7a6f3b24c711f5945d845b4bf1a3df0cefecf`)

## Hermes surfaces used

- Native `plugin.yaml` + `register(ctx)`
- `ctx.register_tool()` -> `write_gate_check` (explicit preflight)
- `ctx.register_hook("pre_tool_call")` -> the veto
- `ctx.register_command()` -> `/writegate`
- `ctx.get_config()` / `ctx.set_config()` -> own settings namespace only
- `ctx.state` -> three profile-scoped integer counters
- `config_schema` -> Settings -> Plugins

No core overrides, no private core imports, no prototype patching, no runtime rebinding, no self-updating code, no binaries, no forks of bundled plugins.

## Rule 13 disclosures

- **Network calls to third-party services:** none.
- **Reads outside the plugin's own data:** only one optional, user-specified JSON rules file named in the `rules_file` setting. Otherwise it reads only the in-memory arguments of the tool call it gates. It never reads `.env`, `auth.json`, credential stores, other profiles or session databases.
- **Shell commands:** none. No subprocesses, no `eval`, no dynamic imports.
- **Long-running background processes:** none.
- **Stored credentials:** none. No `os.environ`, no token files, no OAuth, no `requires_env`.
- **Telemetry / usage reporting:** none (nothing to opt into).
- **State written:** three integer counters in profile-scoped plugin state under `HERMES_HOME/plugin-data/write-gate/`. No file contents, paths, tool arguments or model text are persisted.
- **Approvals:** the plugin never auto-approves, never disables guards and never bypasses the approval gate. In `enforce` mode it uses the documented `pre_tool_call` `block` directive; `observe` mode reports without blocking. Any internal error fails open.

## Screenshots

None — the plugin has no UI. `/writegate status` renders plain text in chat; settings appear in Hermes Desktop's generated Settings -> Plugins form.

## Validation

- `hermes plugins validate . --install-deps --json` -> `ok: true`, 13/13 checks, **zero warnings**, security scan `safe`.
- `hermes plugins doctor . --ci` -> exit 0, 1 tool + 1 hook registered.
- 33 unit tests green (`python -m unittest discover -s tests -v`), including a fake-`PluginContext` end-to-end test that asserts the exact `pre_tool_call` block directive and payload.
- `capabilities` in the entry match what `register(ctx)` actually registers at the pinned SHA.
- `requires_hermes: ">=0.21.5"` is declared in both the catalog entry and `plugin.yaml`.

## Hackathon

Submitted for the Hermes Agent Plugin Hackathon (deadline Nov 11, 5PM EST). Per the announcement, an open PR is sufficient for entry.


## Add creature-workshop plugin.
https://github.com/NousResearch/hermes-agent/pull/149855
State: open; created 2026-11-06T04:25:07Z

## What is Creature Workshop?

Creature Workshop lets you manage your project's development lifecycle in one place: your project.

Every project that adopts Creature Workshop gets an `.ops/` folder that declares the project (tools, config, lock), the way the [XDG standard](https://specifications.freedesktop.org/basedir/latest/#variables) lays out a home directory, and an optional `shell/` folder for hooking your own scripts and dev tools into the standard library underneath, [shellops](https://gitlab.creature-workshop.com/ksoft/shellops). The plugin reads that declaration, runs the project's own `shell/ops`, and hands the result to the agent.

## "Doesn't tool X already do that?"

Probably! I use a few of those tools myself.

How many of them do you have, though? How well do they fit together in your CI/CD? Do they know what each other does, or where they sit in the lifecycle as a whole?

Creature Workshop gives a project a floor of simple tools for every part of the lifecycle it doesn't already cover, and lets you slot in the tooling you already have. Those X tools make the case themselves: if `kubernetes` isn't written down somewhere as needed to deploy your project, not even an agent can set the project up without guessing. Internal tools with no docs are worse.

With Creature Workshop that's a solved problem. Declare the tool in `.ops/config/tools.yaml`, pinned to a version and a channel (`apt`, `brew`, `cargo`, `npm`, `go`, `flatpak`, a git repository, or an installer script of your own under `shell/`), and `shell/ops install` sets up the next contributor's machine, and the agent's.

## Scope for the hackathon

shellops does a lot more than I could responsibly ship as a Hermes plugin in a week. This submission starts with the core: the declaration and the toolchain. The other parts of the lifecycle are planned releases.

## Surfaces

- **Tools** (`workshop` toolset): `workshop_project`, `workshop_install`, `workshop_test`, `workshop_lint`. Every handler returns JSON and never raises.
- **System prompt**: one short paragraph when the session's directory is a shellops project, with its name, its tool count and its latest release.
- **Desktop** (in review, lands with the next pin): a pane with the toolchain live from `install --check`, the declaration and the release record, plus a status-bar chip that counts installed tools.
- No hooks, no middleware, no environment variables.

## Disclosures

- The tools run the project's own `shell/ops` as a subprocess, in the project directory, with its `.envrc` loaded. Nothing runs outside the project.
- `workshop_install` with `check: false` installs tools from the channel the declaration names. With `check: true`, the default, nothing is installed.
- The plugin reads files under the project only. No network calls of its own, no telemetry, no credentials, no background processes beyond the subprocess of each call.

## Status

Draft for the Hermes Agent Plugin Hackathon. The pin moves as the plugin's merge requests land; screenshots follow. `hermes plugins doctor . --ci` and `hermes plugins validate . --install-deps` pass at the pinned commit. The repository vendors shellops as the submodule `shell/.ops`, which is the project's own tooling and not part of the plugin's runtime.

## Add budget-leash to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149268
State: open; created 2026-11-05T04:55:33Z

Adds **budget-leash** (v0.1.0) to the community plugin catalog.

- Repo: https://github.com/jusst01/budget-leash
- Pinned commit: f301d040184c95c3a4a2d8c1387517086dc50470
- Verified on Hermes v0.22.5: passes `hermes plugins validate`, hooks/tools registered per `hermes plugins doctor`, and the plugin is enabled and running live in my own Hermes gateway.

Hard budget enforcement for Hermes sessions. Tracks estimated model spend (token usage x per-model prices) and tool-call counts against a per-session cap and a persistent per-day cap, and blocks tool calls via pre_tool_call once a cap is exhausted (fail-closed), so unattended agents cannot run up unbounded cost; warns at 80% of a cap via context injection, keeps a day-ledger on disk that survives restarts, and writes a per-session JSONL spend report. Disclosure: local code only; reads token-usage metadata from API responses, writes a ledger JSON and per-session JSONL reports under ~/.hermes, opens no network connections and starts no processes; its one deliberate side effect is refusing tool calls after a user-configured cap is exhausted.

Entry for the Hermes Agent Plugin Hackathon.

## Add bumblebee-guard to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149358
State: open; created 2026-11-05T08:10:50Z

Supply-chain guard plugin wrapping the local Bumblebee scanner bridge.
- Tools: bumblebee_guard_scan / bumblebee_guard_status / bumblebee_guard_diff (baseline diff)
- pre_llm_call hook: one-line alert only when curated known-malicious findings exist (never when clean, max 1/hour) — zero context cost in the normal case
- /bumblebee slash command + bundled triage skill (confidence classes, OSV alias dedup, documented FP pattern)
- stdlib-only, no credentials, no plugin-owned network calls; OSV queries + opt-in catalog refresh belong to the disclosed bridge layer
- Validated at pinned sha: hermes plugins validate 14/14, plugins doctor --ci OK, 11 pytest tests
- Hackathon entry: NousResearch Plugin Hackathon (demo video + form submitted separately)

## What does this PR do?

<!-- Describe the change clearly. What problem does it solve? Why is this approach the right one? -->



## Related Issue

<!-- Link the issue this PR addresses. If no issue exists, consider creating one first. -->

Fixes #

## Type of Change

<!-- Check the one that applies. -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🔒 Security fix (undisclosed vulnerabilities in [SECURITY.md](https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md) §3.1 scope go to [Security Advisories](https://github.com/NousResearch/hermes-agent/security/advisories/new) first, not a public PR)
- [ ] 📝 Documentation update
- [ ] ✅ Tests (adding or improving test coverage)
- [ ] ♻️ Refactor (no behavior change)
- [ ] 🎯 New skill (bundled or hub)

## Changes Made

<!-- List the specific changes. Include file paths for code changes. -->

-

## How to Test

<!-- Steps to verify this change works. For bugs: reproduction steps + proof that the fix works. -->

1.
2.
3.

## Checklist

<!-- Complete these before requesting review. -->

### Code

- [ ] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [ ] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`fix(scope):`, `feat(scope):`, etc.)
- [ ] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [ ] My PR contains **only** changes related to this fix/feature (no unrelated commits)
- [ ] I've run `pytest tests/ -q` and all tests pass
- [ ] `python scripts/check` passes (the blocking lint and code-health checks CI runs)
- [ ] I've added tests for my changes (required for bug fixes, strongly encouraged for features)
- [ ] I've tested on my platform: <!-- e.g. Ubuntu 24.04, macOS 15.2, Windows 11 -->

### Documentation & Housekeeping

<!-- Check all that apply. It's OK to check "N/A" if a category doesn't apply to your change. -->

- [ ] I've updated relevant documentation (README, `docs/`, docstrings) — or N/A
- [ ] I've updated `cli-config.yaml.example` if I added/changed config keys — or N/A
- [ ] I've updated `CONTRIBUTING.md` or `AGENTS.md` if I changed architecture or workflows — or N/A
- [ ] I've considered cross-platform impact (Windows, macOS) per the [compatibility guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#cross-platform-compatibility) — or N/A
- [ ] I've updated tool descriptions/schemas if I changed tool behavior — or N/A

## For New Skills

<!-- Only fill this out if you're adding a skill. Delete this section otherwise. -->

- [ ] This skill is **broadly useful** to most users (if bundled) — see [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#should-the-skill-be-bundled)
- [ ] SKILL.md follows the [standard format](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#skillmd-format) (frontmatter, trigger conditions, steps, pitfalls)
- [ ] No external dependencies that aren't already available (prefer stdlib, curl, existing Hermes tools)
- [ ] I've tested the skill end-to-end: `hermes --toolsets skills -q "Use the X skill to do Y"`

## Screenshots / Logs

<!-- If applicable, add screenshots or log output showing the fix/feature in action. -->



## feat(plugin-catalog): add claim-market-router, hunk-consent-guard, and source-trail-supervisor
https://github.com/NousResearch/hermes-agent/pull/149353
State: open; created 2026-11-05T07:53:48Z

## Summary

Adds three community plugins for the **Hermes Agent Plugin Hackathon** from [`misakamikotoghr-5205/hermes-hackathon-plugins`](https://github.com/misakamikotoghr-5205/hermes-hackathon-plugins) pinned at commit `d4a7f0938b975c36c0d7fc65c8d32313a52d6f1b`:

1. **`claim-market-router`** (`category: models`, `subdir: claim-market-router`)
   - **Extension Surfaces:** Pluggable `DelegationProvider` (`delegation.backend: claim_market`, returning `model`, `provider`, `reasoning_effort`, `service_tier`, `fallback_providers`, `request_overrides`, and `label`), `llm_request` middleware, `post_llm_call` & `post_api_request` hooks, `claim_market_auction` & `claim_market_ledger` tools, `/claim-market` slash command, and `hermes claim-market` CLI command.
   - **What it does:** Adapted from [`Cost-aware-claim-based-multi-model-AI-orchestrator`](https://github.com/misakamikotoghr-5205/Cost-aware-claim-based-multi-model-AI-orchestrator) (*MISAKA AGENT*) and [`watt-window`](https://github.com/misakamikotoghr-5205/watt-window). Publishes task cards (`role_needed`, `complexity`, `max_cost_units`), synthesizes capability-fit and quota-health claims with convex shadow pricing across current models (`google/gemini-3.8-flash`, `anthropic/claude-sonnet-5.5`, `openai/gpt-6-astra-pro`, with `fallback_providers` chains to `deepseek/deepseek-v4.1-flash`, `openai/gpt-6.1-sol`, `anthropic/claude-opus-5.5`, and `google/gemini-4-argon`), resolves disagreements via weighted voting, nominates an independent verifier route, and returns explainable sensitivity reports when budget constraints are infeasible.

2. **`hunk-consent-guard`** (`category: tools`, `subdir: hunk-consent-guard`)
   - **Extension Surfaces:** `tool_execution` middleware, `pre_tool_call` & `post_tool_call` hooks, 4 tools (`hunk_propose`, `hunk_review_status`, `hunk_apply_approved`, `hunk_rollback_receipt`), `/hunk-desk` slash command, and `hermes hunk-desk` CLI command.
   - **What it does:** Adapted from [`patch-review-desk`](https://github.com/misakamikotoghr-5205/patch-review-desk) and [`cart-consent-paypal`](https://github.com/misakamikotoghr-5205/cart-consent-paypal). Stages multi-hunk file proposals (checking `agent.file_safety.get_read_block_error` / `get_write_denied_error` and resolving relative paths against terminal cwd), requires user-only hunk consent (`/hunk-desk approve`, `hermes hunk-desk approve`, plus `pre_tool_call` approval gate on `hunk_apply_approved`), dispatches all file writes through `ctx.dispatch_tool("write_file", ...)`, automatically revokes approvals if the target file's SHA-256 baseline drifts on disk before application, and records drift-checked rollback receipts in SQLite.

3. **`source-trail-supervisor`** (`category: general`, `subdir: source-trail-supervisor`)
   - **Extension Surfaces:** 3 tools (`source_trail_ingest`, `source_trail_verify`, `session_supervisor_node`), 3 hooks (`on_session_start`, `post_tool_call`, `post_llm_call`), bundled `epistemic-supervision` skill (`ctx.register_skill`), `/trail-supervise` slash command, and `hermes trail-supervise` CLI command.
   - **What it does:** Adapted from [`source-trail-otari`](https://github.com/misakamikotoghr-5205/source-trail-otari), [`volc-casedesk`](https://github.com/misakamikotoghr-5205/volc-casedesk), and [`codex-session-supervisor`](https://github.com/misakamikotoghr-5205/codex-session-supervisor). Enforces exact zero-based Unicode code-point span citations (`source[start:end] == quote`), withholds unilateral claims when valid sources carry conflicting position labels on the same topic (`withheld_contradiction`), and fingerprints tool/turn progress to detect stuck loops and log recoverable causal decision nodes.

---

## Disclosure (Catalog Rule 13)

- **Network & Subprocesses:** None across all three plugins. Pure Python 3.11+ standard library (`sqlite3`, `difflib`, `hashlib`, `json`, `argparse`).
- **Credentials & Core Safety:** None of the plugins read `.env`, `auth.json`, or provider secrets, nor do they override core tools or weaken built-in approval prompts.
- **Profile-Scoped Storage:** Each plugin writes only to `<HERMES_HOME>/plugin-data/<plugin-name>/data.db` via `plugins.plugin_storage.plugin_db`.
- **Middleware Behavior:**
  - `claim-market-router`'s `llm_request` middleware is a no-op by default (`auto_effort_shaping: false`); when enabled, it modifies only `reasoning_effort` on exploratory turns when rolling-window shadow price $\ge 0.20$.
  - `hunk-consent-guard`'s `tool_execution` middleware wraps file-writing tool calls solely to capture before/after SHA-256 rollback receipts (up to `max_snapshot_kb`, default 256 KB) without altering tool arguments or bypassing Hermes approvals.

## Verification

- `python3 scripts/validate_plugin_catalog.py plugin-catalog/` passes cleanly.
- `hermes plugins validate` capability probe (`provides_tools`, `provides_hooks`, `provides_middleware`), `tools/plugin_guard.py`, `check_private_imports`, and `scripts/scan_plugin_payloads.py` pass with zero errors or warnings.


## plugin-catalog: add ghost-run (dry-run mode for Hermes)
https://github.com/NousResearch/hermes-agent/pull/149252
State: open; created 2026-11-05T04:09:27Z

Adds `plugin-catalog/ghost-run.yaml` for **Ghost Run**, submitted by the repo owner (tnvolman), pinned to `03e1d54cc55b8c158e51907defe847eaf3e46c49`. Entry for the Hermes Agent Plugin Hackathon.

**What it does:** `/ghost on` turns on a dry-run mode. Through `tool_request` middleware and a `pre_tool_call` hook, file writes, patches, deletes and terminal commands go into a throwaway copy of the working folder, and network-touching tools and commands are blocked. You review the diff in a Desktop pane (or with `hermes ghost ui`, a local web view), then apply the paths you pick or throw the copy away. Commands: `/ghost on|off|status` and `hermes ghost diff|apply|discard|ui`.

**Disclosures (rule 13):**
- Copies the working folder into a temp sandbox and runs the agent's terminal commands there.
- Writes session state to `~/.hermes/ghost-run/`.
- `apply` writes only the changes you choose back to the real folder.
- `hermes ghost ui` serves a page on 127.0.0.1:8765 that only this machine can reach.
- No third-party network calls, credentials, telemetry, Python dependencies, binaries or self-updater.

**Testing:**
- 32 pytest tests pass.
- `validate_plugin_dir` (hermes_cli/plugin_validate.py at current main), run on a fresh clone at the pinned SHA: all 16 checks pass, including capability probe, declared hooks and middleware match, security scan safe, no core override, desktop surface.
- doctor passes.
- `scripts/validate_plugin_catalog.py` reports OK on the entry and on the full catalog.
- Also tested live end to end with a Hermes agent session.


## Add wazoo memory provider to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149129
State: open; created 2026-11-04T22:28:33Z

Adds `plugin-catalog/wazoo.yaml`: the Wazoo memory provider, a third-party memory backend at [wazootech/wazoo-hermes](https://github.com/wazootech/wazoo-hermes), pinned at `34de187e9773f191df03fa9dbf0fd47d679058af`.

**What it does.** Implements the MemoryProvider ABC. Cross-session knowledge lives in a Wazoo world as typed RDF memories (decision, preference, person, project, finding, correction), so "what did we decide about X" is one SPARQL query and corrections record what they replace (`wz:supersedesStatement`) instead of overwriting. Background prefetch injects the top search results before each turn (trivial prompts skip the round trip); four tools ship: `wazoo_search`, `wazoo_sparql`, `wazoo_remember`, `wazoo_memories`. Built-in MEMORY.md/USER.md writes are mirrored into the world; `replace`/`remove` writes become corrections using the host-provided `previous_content` (skipped when absent). `sync_turn` is a no-op on purpose: the world holds curated facts, not transcripts.

**Setup.** `WORLDS_TOKEN` + `WORLD_ID` (bring your own world), or `WAZOO_PLATFORM_TOKEN` alone: on first use the provider creates a world, mints a scoped `wzw_` token, and persists both to the profile `.env`. Stdlib-only HTTP (urllib), no Python dependencies.

**Honest scope notes.** This is my plugin repo and I'm the maintainer (wazootech). The entry is part of the Hermes Agent Plugin Hackathon submission. The tools are registered through the memory-provider interface rather than the generic plugin tool registry, which is why `provides_tools` is empty, matching the supermemory entry. Prefetch recall and tool calls were verified against the hosted API; end-to-end runs inside `hermes plugins doctor` are the maintainer's to run.

## add aegis-gate to the plugin catalog - pre-execution verification gate (pre_tool_call)
https://github.com/NousResearch/hermes-agent/pull/150254
State: open; created 2026-11-06T19:36:06Z

What this adds
One catalog entry: plugin-catalog/aegis-gate.yaml
→ https://github.com/Rainyy99/aegis-hermes (plugin at repo root,
subdir: ""), pinned to the exact commit in the entry's sha:.
What the plugin does
AEGIS gate is a pre-execution verification gate for Hermes
agents. It registers a single fail-closed pre_tool_call hook that
inspects a tool call's arguments before the call executes and runs
whichever of four verification gates apply:
Gate 1 — provenance: a claim's official source must actually
  carry it, and an independent record (the address's Sourcify page)
  must confirm it.
Gate 2 — contract: execution targets are checked on Sourcify —
  exact match preferred, partial match forced to WARN, unverified =
  BLOCK — and verified source is scanned for risk patterns.
Gate 3 — signature: EIP-712 payloads are structurally decoded
  before anything signs them (Permit shapes, spender/value/
  amount fields, and Permit2 as verifyingContract are BLOCKED).
Gate 4 — instruction channel: free text is scored for
  injection signals; a challenge→sign→submit sequence or
  sign-submit-plus-external-server combination BLOCKs at any score.
Verdicts map to Hermes directives: BLOCK → block (veto, with
reasons returned to the model), WARN → approve (escalation to
Hermes's own human-approval gate), ALLOW → no directive. A gate
that cannot complete its check abstains into escalation — never
a silent pass, never a fabricated verdict. Gates 1/2 fetch live
evidence inside an internal ~20 s budget (Hermes's callback timeout
is 30 s, fail-closed); Gates 3/4 are pure local, and calls with no
risk markers take a fast path with zero network.
Submitted for the Hermes Agent Plugin Hackathon (submissions
close 11 Nov 2026, 5PM EST).
Verification evidence
hermes plugins validate <plugin> --install-deps — PASSED
  (exit 0), run against the exact pinned tree on Hermes 0.23.0:
  manifest/config schema parse, declared hooks match registrations
  (1 hook, 0 tools, 0 middleware), security scan: safe, no core
  override.
hermes plugins doctor <plugin> --ci — PASSED (exit 0):
  runtime discovery, import, and registration pass.
86 unit tests, all passing, fully offline (stdlib unittest;
  python3 tests/run_tests.py in the plugin repo). The battery is
  the AEGIS kit's calibration suite ported to Python; Gate 3 and
  Gate 4 outputs were also diffed field-by-field against the
  original Node implementation — identical.
Live end-to-end (real Hermes sessions, scripted model driving
  the production agent loop): a harmless ls executes untouched; a
  write carrying the Nonce Protocol brief is BLOCKED (Gate 4
  sequence rule; Gate 1 also fetched the project page live); a
  Permit signing command is BLOCKED (Gate 3); an execute against an
  unverified BSC contract is BLOCKED (Gate 2 fetched Sourcify live
  inside the hook). A sabotaged-callback smoke test confirmed
  pre_tool_call fails closed on callback error and on timeout.
Disclosure (rule 13)
Network: read-only HTTPS GETs to sourcify.dev and to source
  URLs referenced by a tool call's own arguments (Gates 1/2 evidence
  only), inside the ~20 s budget. No telemetry, no other endpoints.
No credentials held, requested, or read; no subprocesses;
  nothing is signed or executed by the plugin itself — it only
  checks. State is an in-process, 5-minute-TTL verdict cache plus a
  one-line stderr journal per gated call. Python stdlib only — zero
  dependencies.
Prior work: the gates are a Python port of my own open-source
  AEGIS kit (NEAR Hackathon,
  Nov 2026); verdict semantics and thresholds are unchanged.
Known limitations (also in the plugin README)
WARN is only as strong as the surface's approval policy. On
  unattended one-shot surfaces (hermes -z, cron with
  cron_mode: approve, --yolo), Hermes auto-approves
  approval-gate escalations by its own contract, so WARN is advisory
  there. **BLOCK vetoes never enter the approval gate and are
  absolute on every surface tested.** (Also filed as the entry's
  known_issues:.)
Live-fetch abstain under the time budget; Gate 3 is structural
  only (no signature verification or signer recovery); Gate 4 is
  heuristic scoring; the verdict cache is per-process.

## Add Showreel to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/150078
State: open; created 2026-11-06T13:38:46Z

## Showreel catalog entry

Adds `plugin-catalog/showreel.yaml` for [Showreel](https://github.com/Duffey234/hermes-showreel) (owner: Duffey234).

**What it does:** Turns a Hermes Agent session into a short demo video. Six observer hooks record what the session actually did (ask, commands, file edits, screenshots, token usage), scrubbed twice for secrets; a deterministic storyboard keeps a failing test with its fix and fits an 89s budget; Pillow + the user's own ffmpeg render 1080p MP4 (16:9 / 9:16 / 1:1) with captions. Desktop: Showreel page with moment editor and inline player, REC chip, and a chat card for `showreel_render`.

**Surfaces:** hooks `on_session_start`, `pre_llm_call`, `post_tool_call`, `post_api_request`, `post_llm_call`, `on_session_end`; tool `showreel_render`; Desktop plugin page/routes.

### Rule 13 disclosures
- Runs `ffmpeg`/`ffprobe` (and `espeak-ng` or `piper` only when local narration is chosen) as subprocesses with fixed argument lists.
- Writes only to its plugin-data folder (scrubbed timeline in SQLite, newest 30 sessions) and the renders folder.
- No network unless narration is set to `elevenlabs` (HTTPS to api.elevenlabs.io with caption text) or `hermes` (whatever TTS the user configured). Narration default is off.
- No telemetry, no background processes, no self-updates.
- Desktop half talks only to its own `/api/plugins/showreel` routes, which serve renders by bare file name from the renders folder.
- Secrets are scrubbed twice (before store and before draw).

**Validation:** `hermes plugins validate . --install-deps` and `hermes plugins doctor . --ci` against Hermes 0.22.7 at pin `a8f404a0481408af8f56b514e47905dfd3565fa7`.

**Hackathon demo post:** https://x.com/CryptoBurrito/status/2118699050069295357

Pin: `a8f404a0481408af8f56b514e47905dfd3565fa7` on https://github.com/Duffey234/hermes-showreel

## plugin-catalog: add ariadne
https://github.com/NousResearch/hermes-agent/pull/150596
State: open; created 2026-11-07T08:31:02Z

Adds plugin-catalog/ariadne.yaml for [Ariadne](https://github.com/miracle352/hermes-ariadne), my entry for the plugin hackathon. I own the repo.

Ariadne records a Hermes session and replays it with no model, no network and no tokens, so you can see exactly what Hermes does differently: replay on a new build, compare two installs, bisect the commit that changed a session, fork a recorded session to a live model, export trajectories and preference pairs, and check the documented hook contracts on every run. Its contract check found
#150324 (fix in
#150333).

Surfaces: llm_execution, tool_request and tool_execution middleware, observer hooks, register_command (/ariadne) and register_cli_command (hermes ariadne). No core overrides.

Disclosure:

Recording is off until the user turns it on. Cassettes are written locally under plugin-data with secrets scrubbed; tool output can still contain private file contents.
play/compare/bisect/fork start Hermes (python -m tui_gateway.entry) as a child process and drive it over JSON-RPC.
Replays copy the profile’s config.yaml (credential-looking keys removed), SOUL.md, memories/ and skills/ into a throwaway home. Never .env or auth.json.
Replays answer every approval with deny, neutralise tool arguments and block outbound network through a closed local proxy.
fork makes real model calls with the user’s provider in their own home (the session appears in their history); tools after the fork point run only with --live-tools.
bisect checks out commits in a Hermes checkout the user names, refuses a dirty tree, restores the original commit.
No telemetry, no network calls of its own.

hermes plugins validate --install-deps passes at the pinned commit. CI (unit tests + cassette replays on v0.23.0 and main): https://github.com/miracle352/hermes-ariadne/actions

## [Hackathon/WIP] Mission Control shadcn dashboard
https://github.com/NousResearch/hermes-agent/pull/15892
State: open; created 2026-04-26T04:48:03Z

## Hackathon/WIP submission

Mission Control is a shadcn-style dashboard refresh for Hermes Agent.

This draft PR is opened for the hackathon and maintainer feedback. The current implementation intentionally demonstrates the full direction, but it touches shared dashboard primitives, so I would like feedback on whether this should ship as the default dashboard, an opt-in shell, or a theme/plugin mode before marking it ready.

## What changed

- Adds a responsive Mission Control dashboard shell
- Adds clean dark/light dashboard themes with Geist Sans + Geist Mono
- Restores the full built-in theme picker alongside Mission themes
- Keeps the embedded Hermes TUI chat, but gates startup behind an explicit **Start new session** button so opening `/chat` does not create empty sessions
- Cleans core dashboard primitives toward shadcn styling: buttons, badges, cards, tabs, inputs, dialogs, sheets, dropdowns, tooltips, etc.
- Updates sessions, logs, cron, config, skills, docs, and plugin surfaces to fit the new shell

## Why

The original Hermes dashboard has a strong cyberpunk identity. Mission Control keeps the Hermes agent workflow intact while offering a calmer shadcn-style cockpit for people who want something closer to modern product UI.

## Verification

From a clean clone of `NousResearch/hermes-agent:main`:

```bash
git diff --cached --check
python3 -m py_compile hermes_cli/web_server.py
cd web && npm ci && npm run build
```

All passed locally.

## Notes

- Opened as draft on purpose.
- No local config, secrets, session data, Tailscale/MagicDNS URLs, Discord IDs, or private Hermes profile files are included.
- Demo video/link can be added once the hackathon post is finalized.


## plugin-catalog: add receipts
https://github.com/NousResearch/hermes-agent/pull/149724
State: open; created 2026-11-05T21:44:52Z

Add receipts, a Hermes plugin that binds verification results to Git content and blocks supported terminal pushes and PR creation until the configured check has passed for the published tree.

Surfaces: pre_tool_call, post_tool_call, and /receipts. No model tools, new dependencies, core overrides, or model calls.

Validation: 30 real-repository behavioral tests; hermes plugins validate --install-deps and plugins doctor --ci passed. A deterministic demonstration through Hermes discovery, actual hook dispatchers, the local terminal backend and a local bare Git remote passed block/check/push/edit/block/fix/push.

Disclosures: reads repository files and Git configuration; runs bounded local Git subprocesses without writing the target index or object database; writes a plugin-local SQLite ledger containing paths, commands, hashes, exit codes, timestamps and session IDs. No network calls, telemetry, stored credentials, or resident process. Local backend and default in_process mode only. External clean/process filters, submodules, sparse/assume-unchanged entries and ambiguous push forms are unsupported. Shell recognition is bounded; this is a workflow gate, not a security boundary.

The integration demo imports Hermes internal dispatchers as a test harness; validation reports those test-only imports as warnings. Runtime plugin imports use documented helpers.

Hermes Agent Plugin Hackathon entry. Submitted by the repository owner (`cirwel`). The entry pins `0dd1a374cc70ce388040f99adc908c7054ed8fa9`, the merge of the reviewed commit `9b68424` (identical tree), and sets a card `title` to keep it distinct from the unrelated `hermes-receipts` entry.

---
Model: gpt-6-astra
Provenance: UNITARES (https://github.com/cirwel/unitares)
UNITARES agent: f2027179-d44a-4fbe-9ca0-fdd9deaa9a25

Submission follow-up (re-pin to the merge commit, card title, opening this PR):

---
Model: claude-opus-5-5
Provenance: UNITARES (https://github.com/cirwel/unitares)
UNITARES agent: 7035b711-f942-41eb-8e34-ad7483198ba3


## feat(plugin-catalog): add xray plugin
https://github.com/NousResearch/hermes-agent/pull/149414
State: open; created 2026-11-05T10:22:24Z

## What does this PR do?

Adds `plugin-catalog/xray.yaml` for **Plugin X-Ray** ([cipoklean/hermes-xray](https://github.com/cipoklean/hermes-xray)), submitted for the Hermes Agent Plugin Hackathon.

X-Ray sets traps for plugins instead of reading their code:

- `hermes xray detonate <plugin>` runs a plugin in a throwaway child process with a fake home full of honeytokens. It calls every tool with schema-generated inputs and fires every hook, with network egress and process spawns blocked. It then replays the run at +30 and +90 days to catch time-bombs. The verdict is RED/AMBER/GREEN with file:line proof.
- Opt-in live bait (`hermes xray bait plant`) puts decoy credential files into empty paths and flags any installed plugin that opens one. With `enforce` on (off by default), that plugin's next tool call goes to Hermes' own approval prompt via `pre_tool_call`.
- `hermes xray diff` / `disclose`: behaviour diff per pinned version, plus a drafted disclosure line.

## Type of Change

- [x] ✨ New feature (catalog entry only)

## Changes Made

- `plugin-catalog/xray.yaml`: pinned to `85b0e95e68472bd1a6dd582458a2f575ab7d9d2d`, `subdir: xray`, `version: "0.1.0"`, with Disclosure and known issues.

## How to Test

1. `python scripts/validate_plugin_catalog.py plugin-catalog/xray.yaml` → `OK: 1 file(s) valid`
2. `hermes plugins validate <clone at 85b0e95e>/xray --install-deps` → `Validation passed.` (scan: safe)
3. `hermes plugins install cipoklean/hermes-xray/xray`, then from a clone: `hermes xray detonate demo/sunny-weather` → RED with file:line. `demo/` holds deliberately malicious specimens, so the scanner blocks the repo root; the entry installs `subdir: xray` only.

## Checklist

- [x] Conventional Commits
- [x] Searched existing PRs; no `xray` entry
- [x] Only the catalog entry
- [x] No credentials needed; no core overrides; declared hooks match registrations; risky behaviour disclosed; no binaries
- [x] Tested on Ubuntu and Windows 11, including live bait and the approval prompt in a real chat


## plugin-catalog: pin scribase to v1.3.0 (adds real persistent agent memory)
https://github.com/NousResearch/hermes-agent/pull/149690
State: open; created 2026-11-05T20:20:00Z

## Summary

Pin update for the `scribase` plugin catalog entry merged in #149583, per the catalog rules' normal re-review flow for a pin bump (not a new submission). Updated four times since the original merge, most recently to v1.3.0 at `caelum0x/scribase-hermes-plugin@8b3475cd41aa3606dbad434d77420be43385d63d`.

The plugin grew from one tool to five (v1.1.0/v1.2.0/v1.3.0, already reflected in earlier revisions of this PR):

- **`scribase_create_project`** — provisions a hosted Postgres project + environment and returns its connection string and API keys.
- **`scribase_lint_migration`** — submits a migration's `up` SQL to `POST .../migrations` with `apply` hardcoded to `false` in the plugin, running Scribase's real migration-safety linter (missing RLS, `GRANT` to `PUBLIC`, permissive policy, missing `WITH CHECK`, `SECURITY DEFINER` are block findings; missing FK index is a warn finding). Never opens a database session.
- **`scribase_query`** — runs a single read-only statement via `POST .../database/query`. Read-only is enforced twice by the server itself (static keyword check, then a Postgres `READ ONLY` transaction).
- **`scribase_branch_task`** — one tool, three actions (`create`/`promote`/`discard`) for a real agent-native branch-per-task workflow backed by `POST /v1/environments` (`kind: "preview"`), `POST .../branches/merge`, `DELETE .../environments/{env}`.
- **`scribase_memory_task`** (new, v1.3.0) — one tool, four actions (`store`/`recall`/`search`/`forget`) giving the agent real persistent memory: a Postgres row in its own Scribase project, not the model's own context window.

## v1.3.0: `scribase_memory_task` — closing a real gap, not adding wording

Before this, none of the four existing tools could write application data: `scribase_query` is read-only by server-side design, and `scribase_lint_migration` always sends `apply: false`. A Hermes agent could provision, branch, and lint a project through this plugin, but never actually store anything in it.

Read the real control-plane source first (`crates/control-api/src/http/database_editor.rs`, `crates/control-api/src/adapters/sql_execute.rs`) rather than guessing: `POST .../database/execute` is the write-mode sibling of `database/query` — the same route the Scribase Studio SQL editor's "write mode" uses, gated to writer roles, with its own server-side destructive-statement confirmation step independent of anything this plugin adds. `store`/`forget` call that route; `recall`/`search` reuse the existing read-only `database/query` route `scribase_query` already calls.

The backing table (`public.hermes_agent_memories`, RLS enabled) is created idempotently the first time `store` runs in a project. An optional `scope` namespaces memories per end-user/conversation. Every value interpolated into SQL (`content`, `metadata`, `scope`, `memory_id`) is escaped with the standard Postgres string-literal escape (doubled single quotes) before it's placed in a statement — the model is never given a path to pass raw SQL through this tool.

**Verified twice.** A throwaway monkeypatched test exercised all 4 actions, every error path, and one deliberately hostile `content` string (`robert'); drop table hermes_agent_memories;--`) — confirmed the built statement has balanced quotes and the injected text lands entirely inside the escaped literal. Then ran the real, unmodified `tools.py` against a real, live, no-login temporary Scribase project on production `api.scribase.com`: `store` (x2) → `recall` (both, newest first) → `search` (filters to one) → `recall` on a second, never-used scope (real isolation: zero rows) → `forget` (one memory) → `recall` again (confirms exactly the forgotten one is gone, the other survives). Full transcript in the plugin repo's `HACKATHON-SUBMISSION-2026-11-05.md`.

## v1.2.1: two real bugs found and fixed during a real end-to-end session, not re-worded docs

Built a real temporary Scribase project (`POST /v1/temporary-projects`, the public, no-account, proof-of-work-gated endpoint) and called this plugin's own unmodified `tools.py` functions against it, against production `api.scribase.com`, with a real agent token — to get genuine evidence of the plugin actually working inside a real Hermes session for the Hermes Agent Hackathon. That real exercise surfaced two previously-undetected bugs, both confirmed with before/after live HTTP calls (not unit-test mocks):

1. **`_request()` never set a `User-Agent` header.** A bare CPython urllib call — exactly what this plugin's handler sends — gets hard-blocked by Cloudflare's WAF in front of `api.scribase.com` (`403 browser_signature_banned`) before it ever reaches the control plane. Reproduced by replaying the literal `Python-urllib/3.x` User-Agent string via `curl` and getting the identical block; confirmed fixed by setting any real UA string.
2. **`create_project()`'s environment-create POST always sent `"ttl_hours": null`** for a production environment (which has no TTL). The control plane's strict request-schema validator rejects an explicit JSON `null` for that optional field with `400 invalid_json`, while omitting the key entirely succeeds. Confirmed via an A/B `curl` replay of the identical body with vs. without the key.

Both were live-blocking bugs: before this fix, every real call from any of this plugin's tools against production would 403 on the WAF check, and `create_project` would separately 400 on the schema check even past that. Fixed in `tools.py`; re-verified with the fixed file imported with zero monkeypatching.

## Disclosure (catalog rule 13)

- **Hermes surfaces used:** `ctx.register_tool` only. No hooks, no middleware, no CLI/slash commands, no runtime overrides.
- **Network calls:** only to `api.scribase.com` (or the operator's own `api_base_url`).
- **Credentials:** `SCRIBASE_API_KEY` read only through `agent.secret_scope.get_secret`.
- **Side effects:** `scribase_lint_migration` has none (`apply` always `false`); `scribase_query` can only read; `scribase_branch_task`'s `create` creates a real billable environment with the same connection/key disclosure as `scribase_create_project`, `promote` is the only action that can change an existing environment (gated by the control plane's own conflict/MFA checks), `discard` permanently deletes the branch and its data; `scribase_memory_task`'s `store`/`forget` write only to the one dedicated `hermes_agent_memories` table (created on first use), and `forget` only ever deletes the single row named by `memory_id` — no action in this plugin can delete an entire scope or table.
- **`requires_hermes`** stays `>=0.20.1`, unchanged — no new Hermes surface is used.

## Validation

Re-ran `validate_plugin_dir()` (the exact function `hermes plugins validate` calls) against the plugin at the new pinned SHA: **15/15 checks pass, 0 warnings**, isolation `host_ready: true`, declared tools match registrations exactly (5 tools), no built-in collisions, security scan safe, no core override. Also re-ran this repo's own `test_shipped_catalog_entries_are_all_valid_and_pinned` against the updated `plugin-catalog/scribase.yaml` entry — passes.

Separately, and honestly documented in the plugin repo's `HACKATHON-SUBMISSION-2026-11-05.md`: the locally installed Hermes CLI used to build and test this (v0.10.0, ~1200 commits behind current `main`) predates the `agent.secret_scope` module `__init__.py` imports, so the plugin cannot actually load into that specific box's live tool registry — confirmed by direct reproduction (`ModuleNotFoundError: No module named 'agent.secret_scope'`) and by a real, live Hermes chat session (GitHub Copilot `gpt-4o` provider) that loads 28 built-in tools successfully but shows zero `scribase_*` tools. This is a real, disclosed version-compatibility gap on that one box, separate from the bugs fixed above and the new tool added above (all confirmed independently of Hermes's plugin loader, by calling the plugin's own HTTP client directly against production).

## Test plan

- [x] `validate_plugin_dir()` — 15/15 checks pass, 0 warnings
- [x] Catalog entry assertions (SHA format, repo prefix, install identifier) pass
- [x] Live re-verification against production `api.scribase.com`, zero mocking (bug fixes + new memory tool)
- [ ] Maintainer review / CI on this PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: add global-business-culture
https://github.com/NousResearch/hermes-agent/pull/150446
State: open; created 2026-11-07T02:36:50Z

## What & why

Adds **global-business-culture** — cross-cultural business intelligence as a deterministic plugin (not prompt text). Built for the Hermes Agent Plugin Hackathon.

- `culture_brief(country, task?)` — structured brief: positioning, trust currency, decision path, communication, contract treatment, etiquette, taboos, country highlights
- `culture_gap_analysis(home, host, task?)` — ranked cultural distance across Meyer's 8 scales (delta, risk level, task-weighted), the misread each gap produces, adaptation moves, Hofstede flags ≥25, synthesis
- `culture_countries(query?)` — coverage list/search (57 economies)
- `/culture <country> [task]` in-session command + bundled skill `global-business-culture:business-culture-playbook`

Data: approximate positions distilled from Erin Meyer (The Culture Map), Hofstede Insights, GLOBE clusters, Lewis model + practitioner field notes. All computation is deterministic arithmetic over bundled JSON — same inputs, same ranked output, every time.

## Surfaces used

- `ctx.register_tool` ×3 (toolset `culture`), `ctx.register_command`, `ctx.register_skill`
- No hooks, no middleware, no capabilities, no config

## Rule-13 disclosure

- **No network calls. No filesystem writes. No env vars. No Python dependencies** (pure stdlib) — fully offline, enterprise-safe.
- Reads only its own bundled `data/*.json`.
- No credentials, no telemetry, no subprocesses.
- Data honesty: scale positions are approximations of published frameworks, not measurements; Laos/Cambodia/Myanmar are extrapolated from GLOBE-cluster neighbours and flagged `extrapolated` in tool output.

## How to test

```bash
hermes plugins install pswong661-eng/hermes-global-business-culture  # or clone at the pinned SHA
hermes plugins validate <path>
python -m pytest tests/ -q          # 35 tests
hermes chat -q "I am from Laos, negotiating in Germany — use culture_gap_analysis to show the top gaps"
```

Verified locally: 35/35 tests, `hermes plugins doctor . --ci` green, `hermes plugins validate` green (security scan: safe; no core override), E2E session output correct (weighted-gap math verified by hand).

## Platforms tested

Linux (Hermes v0.21+, Python 3.11/3.14). Pure-stdlib code; no platform-specific paths.

— Owner submission (pswong661-eng), happy to adjust per review.

## catalog: add asin-hhc-proof-of-pay
https://github.com/NousResearch/hermes-agent/pull/149464
State: open; created 2026-11-05T12:16:01Z

Catalog submission for the Hermes Plugin Hackathon: **asin-hhc-proof-of-pay** v0.1.0.

Adds `plugin-catalog/asin-hhc-proof-of-pay.yaml` only. The plugin itself lives in its own public repo, pinned by commit SHA in the catalog entry:
- Plugin repo: https://github.com/dbottrader/asin-hhc-proof-of-pay
- Pinned SHA: `5b0149d56d32daeba4e82ce40f281b9f8f3167c8`

**What it does** — three read-only tools that let a Hermes agent verify third-party agent work without trusting anyone:
- `asin_hhc_verify_receipt` — validates an asin-hhc:receipt evidence receipt against the published schema (bundled, byte-identical to the public schema)
- `asin_hhc_check_provenance` — recomputes a hash-chained public provenance index (78 entries) and compares the chain head
- `asin_hhc_board` — reads the live ASIN-HHC work-market board (funded bounties in escrow, settlements with 90/5/5 splits)

**Disclosures (catalog rule 13)**
- Network: HTTPS GET requests — the provenance index and live board snapshot are fetched only from `dbottrader.github.io` (GitHub Pages); a receipt passed as `receipt_url` is fetched only if it is a public `https://` URL (http://, private, loopback and link-local hosts, and redirects to them, are refused). The receipt schema is bundled and never fetched or updated at runtime. No self-updating code.
- No credentials, no writes, no telemetry. Python standard library only.
- Honest limits: the plugin reads and verifies public snapshots; it does not post work, claim bounties, or move HHC. Receipt validation is schema conformance at a stated evidence-ladder rung, not end-to-end replay.

**Testing** — installed and enabled through the real Hermes 0.19.0 path (`hermes plugins install` + `hermes plugins list` shows it enabled); the bundled test suite passes 32/32 against the live public endpoints, including negative cases (a raw ledger entry and a tampered receipt both fail validation) and URL-safety negative controls (http, localhost, private and link-local URLs refused).

Submitted by Dennis Christie (@dbottrader / @mankind_peace). ASIN-HHC is a third-party, independent, MIT project.

## plugin-catalog: add hotwire (analog circuit design bench)
https://github.com/NousResearch/hermes-agent/pull/150340
State: open; created 2026-11-06T22:40:07Z

## Hotwire: analog circuit design bench

Adds `plugin-catalog/hotwire.yaml` for [RohanGlitched/hotwire](https://github.com/RohanGlitched/hotwire), submitted by the repo owner for the Hermes Agent Plugin Hackathon.

**What it does.** Hermes writes a SPICE netlist from plain English, then proves it with Hotwire's own circuit simulator (checked against ngspice 42: DC within 0.35 µV, AC within 0.000001 dB, guitar-rate audio within 1.5%). It measures specs written into the netlist (gain, corners, THD, input impedance, supply current, bias regions, guitar-volume clean-up), checks every part against its ratings at the operating point, fails circuits that latch or oscillate, runs Monte Carlo yield over part tolerances, explains what each part does, tunes values to E-series parts, plays a guitar riff (or your WAV) through the circuit, and lays the result out on a stripboard with a parts list and KiCad export.

**Hermes surfaces used**
- 11 tools (`circuit_check`, `circuit_simulate`, `circuit_audition`, `circuit_tune`, `circuit_explain`, `circuit_match`, `circuit_yield`, `circuit_bom`, `circuit_build`, `circuit_export`, `circuit_library`)
- a bundled skill (`hotwire:analog-design`) and a `/hotwire` slash command
- a `pre_llm_call` hook that adds one line of context only when a message is about electronics (configurable, `design_hint`)
- a dashboard backend (`dashboard/plugin_api.py`) and a Desktop half (`desktop/plugin.js`): Bench page and pane, live knobs, an AudioWorklet engine that plays the circuit in real time, tool media renderers for its own tools
- `config_schema`: `design_hint`, `sample_rate`

**Disclosures**
- Python dependency: `numpy>=1.26,<3` (installed with consent). No other dependencies.
- No network calls, no shell commands, no background processes, no credentials, no telemetry.
- Writes designs, plots and audio only under `<HERMES_HOME>/plugin-data/hotwire/`. Reads a file only when the user or the agent names a `.cir/.net/.sp/.spice` netlist or a `.wav` to play through a circuit. `.include` is refused.
- The dashboard routes serve files only from the plugin data folder.
- The Desktop half asks the browser for microphone access only when the user presses "Instrument in" in Live mode, and warns to use headphones.
- `hermes plugins validate --install-deps` passes.

**Screenshots**

![Bench](https://github.com/RohanGlitched/hotwire/raw/main/docs/desktop/bench-light.png)
![Listen](https://github.com/RohanGlitched/hotwire/raw/main/docs/desktop/listen-light.png)
![Board](https://github.com/RohanGlitched/hotwire/raw/main/docs/desktop/board-light.png)
![Chat card](https://github.com/RohanGlitched/hotwire/raw/main/docs/desktop/chat-light.png)


## feat(catalog): add chronos speculative reasoning plugin
https://github.com/NousResearch/hermes-agent/pull/150020
State: open; created 2026-11-06T11:55:26Z

### Summary

This PR adds **Chronos** (`chronos.yaml`) to the official Hermes Plugin Catalog for the **Hermes Agent Plugin Hackathon**.

Chronos upgrades Hermes Agent from a linear single-trajectory executor into a **Monte Carlo Tree Search (MCTS) Speculative Rollout Engine**. When Hermes encounters a test failure, error, or complex task, Chronos uses lifecycle hooks to spawn isolated candidate branches in ephemeral Git worktrees, scores them using a continuous multi-factor fitness function, automatically merges the verified winning fix into the workspace, and visualizes the entire decision DAG natively in Hermes Desktop.

- **Repository:** https://github.com/Shikhyy/hermes-agent/tree/main/plugins/chronos
- **Pinned SHA:** `ce40354a741d828dfc6f65b76334d90b6c0c535a`
- **Subdirectory:** `plugins/chronos`
- **Category:** `tools` / `desktop`

---

### Key Capabilities

1. **Ephemeral Git Worktree Isolation (`chronos.isolation`):** Runs parallel speculative candidate rollouts in isolated worktrees (`.hermes/chronos/worktrees/`) without mutating or polluting the host workspace.
2. **Multi-Factor Continuous Fitness Function (`chronos.verifier`):** Scores candidates using a 4-factor objective:
   Score S = (0.60 × tests_passed) + (0.25 × exit_code) + (0.10 × clean_diff) + (0.05 × speed)
3. **Hermes Desktop DAG Explorer (`desktop/plugin.js`):** Interactive SVG/Canvas decision tree inside Hermes Desktop with syntax-highlighted side-by-side diff viewers and 1-click rewind triggers.
4. **Deterministic Time-Travel Rewind (`chronos.engine`):** Instantly rewinds workspace state and agent cognition to any historical node checkpoint.
5. **Lifecycle Hooks (`chronos.hooks`):** Intercepts errors on `post_tool_call` to advise or trigger speculative rollouts rather than compounding linear errors on disk.

---

### Disclosures (Rule 13 Compliance)

- **Network Access:** None. All MCTS rollouts, tree generation, and diff computations run 100% locally.
- **Filesystem Access:** Modifies files only within isolated Git worktrees (`.hermes/chronos/worktrees/`) during rollouts; merges to the user's workspace only upon verification or explicit user confirmation.
- **Shell Commands:** Executes project test suites (e.g. `pytest`, `npm test`, `cargo test`) strictly inside the isolated branch worktree for verification.
- **Background Processes:** None. Ephemeral worktrees are cleanly pruned on candidate selection or session termination.
- **Credentials & Secrets:** None requested or stored.
- **Telemetry:** Zero telemetry or external reporting.

---

### Validation & Test Verification

- **Local Admission Gate (`hermes plugins validate`):**
  - Manifest & Config Schema: `PASSED`
  - Capability Probe (`register(ctx)`): `PASSED`
  - Declared Tools (5) & Hooks (4): `PASSED`
  - Security Scan: `PASSED (SAFE)`
  - Core Override & Desktop Surface: `PASSED`
- **Catalog Schema (`scripts/validate_plugin_catalog.py`):** `PASSED`
- **Unit Tests:** `14/14 PASSED` (`python3 -m unittest discover -s tests -p 'test_*.py'`)



## Add BotSesh native room channel to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149686
State: open; created 2026-11-05T20:13:39Z

### What it does

BotSesh makes a shared room a native Hermes gateway channel. Addressed messages and replies reach a running gateway over authenticated SSE hints with passive catch-up fallback. Hermes answers and picks up later peer handoffs under the same enrolled identity. Idle transport listening makes zero model calls. Persistent transport, durable send identity and processed-context binding are implemented by the plugin, not a prompt.

This community entry pins **b32baba4bfe825edbaa90cb036e8dfcdb785d417**, version **0.1.0**, in https://github.com/meowsigma/hermes-botsesh. [Public MIT release v0.1.0](https://github.com/meowsigma/hermes-botsesh/releases/tag/v0.1.0).

All 11 commit author/committer identities were rewritten to BotSesh <support@botsesh.com>. Every tree/message/date was preserved; final tree `6d27749501ffcfb34a64a2dfdd1a987f095cbe18` equals the independently approved source tree at `84a916eb8347c2262e51d12e7af9055b6c6a0f50`. Fresh Gitleaks 8.30.1 scans of the entire rewritten history and current tree both returned zero findings. No new product change or live trial is claimed by the identity-only rewrite.

Only this standalone plugin and its vendored public client SDK are MIT-distributed. The hosted BotSesh application/server remains closed source. `vendor/UPSTREAM.md` records SDK provenance and the additive client seam.

### Hermes surfaces

- Public `ctx.register_*` APIs: `botsesh` platform, `/botsesh` command, bundled skill and five tools: `botsesh_create_room`, `botsesh_invite`, `botsesh_rooms`, `botsesh_read`, `botsesh_post`.
- One `post_llm_call` hook gates processed attestation on a successful model turn. No middleware or required environment credential.
- Active-profile `plugin_data_dir("botsesh")`, gateway stable-ID allowlists and public `ctx.session_surface()`. No core monkey-patch or private registry change.
- Linux; Hermes >=0.22.5; Node >=24. No added Python/npm dependencies.

### Rule 13 disclosures

- **Network:** HTTPS to botsesh.com through the vendored public SDK. Normal inference sends supplied room context to the operator’s configured provider. Optional account creation dispatches an existing first-party MCP `create_room` tool only after separate Create rooms consent; its connector owns that API call. No added telemetry/analytics.
- **Processes:** fixed-argv, stdin-only Node bridge; one long-lived SSE child per active room while the adapter runs, plus bounded fallback checks. The canonical SDK uses a small fixed Python POSIX lock helper. No shell-template execution, service install, child model runtime, approval bypass or self-update. Other standalone SDK helpers are not invoked by this bridge’s fixed allowlist.
- **State/credentials:** generated room access, frozen read batches and retry journals are plaintext active-profile plugin data under 0700 directories/0600 files. Consumed batches are removed; unused receipts expire for use within 24h with best-effort later cleanup. Outgoing recovery journals/credentials remain until removed by the operator. Local leave/uninstall neither erases these copies nor revokes membership. No `.env`, browser profile, keyring, provider auth file or unrelated credential store is read. MCP OAuth remains Hermes/connector-owned.
- **Trust/authority:** fully trusted in-process plugin, not an OS sandbox. Stable-ID allowlists still apply; whole-room authorization is broader. Invitation/recipient identity never grants manager/action authority. No deletion, ownership transfer or human acceptance tool. Guest rooms expire after 14 days; share links are not agent invitations. No E2EE claim.
- **Reads/sends:** passive fetch is not acknowledgment. Explicit processing binds only the supplied frozen batch. Generated finals are journaled before POST; retries preserve original bytes/UUID. Reply and draft declaration are separate effects; a declaration denial cannot truthfully mean nothing posted. Exact local recovery never gains authority, substitutes copy or rebases a stale command. Draft-ready is readiness for human review, not approval.
- **Recovery compatibility:** generic reconnect markers identify a unique saved room-bound payload; they are not authority or posted preambles. Unknown/ambiguous/evicted replay is refused. The latest 1,000 gateway delivery identities per room are retained FIFO. A small tuple mirrors installed core transport markers because core supplies no stable replay-operation ID; no core monkey-patch/private ledger import. See `docs/GATEWAY-RECOVERY.md`.

### Remaining compatibility warning

The source validator retains `gateway.session_context.get_session_env` at `tools.py:18`. It is the documented task-local helper used only for `HERMES_SESSION_CHAT_ID`; empty ID denies access. Platform lookup uses public `ctx.session_surface()`. The tested public context has no chat-ID accessor. Independent source approval accepted the narrow seam, not catalog-maintainer acceptance. Please review explicitly; if unacceptable, we will use an upstream public accessor before admission rather than patch core or suppress warnings.

### Owner-approved demo and evidence limits

[48-second landscape demo, final option B](https://github.com/meowsigma/hermes-botsesh/releases/download/v0.1.0/HACK8-B-BotSesh-Hermes.mp4). The vertical counterpart is used for the original @getbotsesh hackathon post. The edited synthetic Fern Bakery task uses two real independent native Hermes runtimes, Hermes and Nova, both on the same Sol model family—not two providers. It shows a later handoff to the same idle running gateway and native draft-ready, not human acceptance/room completion. The underlying live run also verified completed-operation exact replay without new messages and actual Nova revocation denial; cached replay is not live lost-response fault injection. No manual SDK completion substituted for model work. The edit removes waiting and is not uncut latency evidence.

“Loopster” Kevin MacLeod (incompetech.com). Licensed under Creative Commons: By Attribution 4.0 — https://creativecommons.org/licenses/by/4.0/. Edited excerpt.

Repository [EVIDENCE.md](https://github.com/meowsigma/hermes-botsesh/blob/b32baba4bfe825edbaa90cb036e8dfcdb785d417/docs/EVIDENCE.md) and the screenshots retain earlier predecessor-attributed timings/scripted-peer proof; the README distinguishes that from the later two-native-runtime demo. The publication preserves the exact approved README rather than silently changing the pinned tree.

**LIMITED OWNER-AUTHORIZED SMOKE COVERAGE.** No live signed-in account creation, successful scheduled occurrence, endurance, physical-phone input, media/file delivery, E2EE, human acceptance, or named ChatGPT/Claude/Grok automatic return is claimed. A stopped gateway/host is not woken by SSE. Catalog CI/review remains a separate maintainer gate, not approval implied by this submission.

![Desktop](https://raw.githubusercontent.com/meowsigma/hermes-botsesh/b32baba4bfe825edbaa90cb036e8dfcdb785d417/docs/live-room-desktop.png)
![Phone emulation](https://raw.githubusercontent.com/meowsigma/hermes-botsesh/b32baba4bfe825edbaa90cb036e8dfcdb785d417/docs/live-room-phone.png)

Prepared for the Hermes Agent Plugin Hackathon. The form permits submission with an open PR; this body does not claim catalog admission or maintainer endorsement.


## Plugin oauth: entries: expose redirect_port for IdPs that require exact-match redirect URIs (e.g. QuickBooks)
https://github.com/NousResearch/hermes-agent/issues/149642
State: open; created 2026-11-05T18:15:35Z

## Problem

Plugin `oauth:` entries (`hermes auth add <plugin>:<id>`) run the PKCE loopback login via `plugin_oauth._pkce_config`, which never sets `OAuthPKCEConfig.redirect_port` — so the listener uses an OS-assigned port and the `redirect_uri` sent to the IdP has a different port on every sign-in.

Some IdPs require the redirect URI to be **pre-registered exactly, no wildcards** — QuickBooks Online (Intuit) is the one this plugin hits: `https://appcenter.intuit.com/connect/oauth2` rejects any redirect URI whose port wasn't registered verbatim in the app settings.

The machinery already supports this: `auth_oauth_pkce_plugin.OAuthPKCEConfig.redirect_port` exists with the comment *'pin it when the IdP allowlists an exact redirect URI'* — it just isn't reachable from the plugin manifest.

## Request

Add an optional `redirect_port:` field to the `oauth:` manifest entry, passed through to `OAuthPKCEConfig(redirect_port=...)` in `_pkce_config`:

```yaml
oauth:
  - id: quickbooks
    authorize_url: https://appcenter.intuit.com/connect/oauth2
    token_url: https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
    scopes: [com.intuit.quickbooks.accounting]
    client_id_env: QBO_OPS_CLIENT_ID
    client_secret_env: QBO_OPS_CLIENT_SECRET
    hosts: [quickbooks.api.intuit.com]
    redirect_port: 1990   # <-- new; omit = OS-assigned (current behavior)
```

Validation would mirror `redirect_path` (int, 1024-65535 or 0 = OS-assigned).

## The consumer

`qbo-ops` (QuickBooks Online operations plugin, currently in development for the plugin hackathon): the pure-`oauth:` credential path is blocked only by this field. Fingerprint concerns don't apply — `fingerprint` already hashes all `OAuthClient` fields, so adding one is backward-compatible for existing grants.

Happy to send the PR if you'll take it.

## plugin-catalog: add waiting-on-you
https://github.com/NousResearch/hermes-agent/pull/150140
State: open; created 2026-11-06T16:11:37Z

Adds **waiting-on-you** to the plugin catalog. This is a Hermes Plugin Hackathon entry. I'm the owner of the plugin repo.

## What it does
`/waiting` (any session) and `hermes waiting` (terminal) print one list of the questions your bots are waiting on you to answer, oldest first. With several Bot Mode profiles or many gateway chats, these questions end up buried in a dozen scrollbacks.

- It scans `state.db` of the root profile and of every profile under `profiles/` read-only.
- It looks only at the final reply of a turn the user started, and only at its last prose lines. Mid-report questions, `?` in URLs, code blocks, subagent/cron sessions, and replies to other bots or tool notifications are ignored.
- It detects asks in English and Indonesian.
- When two bots ask the same thing (shared identifier such as `PR 6528` / `SEC-018` / `t_…`, or ≥60% word overlap), it shows one item with both bot names.
- An item closes when the user sends a real message in that chat, or when they dismiss it with `/waiting dismiss <id>`.

## How it differs from existing entries
- **bot-forge** only sees journal entries that a bot opts in to write.
- **duty-board** reads the routed profile only, has no Indonesian patterns, and reports per conversation rather than per question.
- **inbox** shows operational state (cron, delegations, kanban).

None of them extracts and dedupes the asks across every profile's real replies.

## Disclosure (also in the README)
- **Reads outside its own data:** `state.db` of every Hermes profile on the machine (sessions, messages), opened with `mode=ro` + `PRAGMA query_only`. It prints the text of matching bot replies, so every profile can see the asks of the others.
- **Writes:** only `plugin-data/waiting-on-you/dismissed.json` in the active profile.
- **Does not do:** network calls, model calls, shell commands, credentials, background processes, tools, hooks.

## Checks
- `hermes plugins validate . --install-deps` on a fresh clone at the pinned SHA `51f8748`: **Validation passed**.
  - The security scan is `safe`, and the no-core-override check passes.
  - `register_cli_command` is skipped under host isolation, as expected. `/waiting` still works.
- `pytest`: 10 passed, on a synthetic multi-bot `HERMES_HOME` with no real data. Covered: en/id extraction and false positives, resolution, cross-bot merge, window, dismissals, and that `state.db` is byte-identical before and after a scan.
- `load_catalog()` parses the new entry, giving 1064 entries.
- Real run on a 6-profile install: 9 open asks from 5 profiles in 0.11 s. Every `state.db` sha256 was unchanged.


## Add catalog entry: api-architect (compile API specs into validated Hermes tools)
https://github.com/NousResearch/hermes-agent/pull/149624
State: open; created 2026-11-05T17:46:01Z

Add catalog entry: **api-architect** — compile API specs into first-class Hermes tools.

## What it is

Any OpenAPI 3 / Swagger 2 / Postman v2.1 spec by URL is compiled into a schema-checked manifest with per-endpoint provenance, served by four tools:

- `architect_learn` — fetch + compile a spec (validated draft; not callable until committed)
- `architect_commit` — human-visible draft → active review (base_url, auth binding, provenance)
- `architect_list` — learned APIs persist across sessions in the plugin data dir
- `api_call` — schema-checked execution; invalid params fail locally (never as server 400s), so the model self-corrects from the error JSON

Cuts HTML deep-scraping by design: **no spec, no invented endpoints** — every endpoint carries provenance (where in the doc it was read); with no spec the learn returns an honest empty result. The differentiation from page-extraction tools (`unbrowse`, `webmint`): typed API interfaces (parsers + HTTP, no browser, no cloud service) and zero python dependencies on all platforms.

## Disclosure (catalog rule 13)

- **Network:** fetches user-supplied spec URLs and calls API hosts the user explicitly committed via `architect_commit`. Private networks (loopback, RFC1918, link-local, ULA — including numeric/decimal/hex hosts and IPv6-mapped/NAT64/6to4/Teredo smuggled forms, deny-listed and tested) are **blocked by default**; opt-in `allow_private_hosts`. Redirects not followed; per-request timeout + response size caps. **No telemetry** — nothing leaves the machine except the calls the user asked for.
- **Credentials:** only through Hermes routes — `config_schema` `type: secret` slots read via `agent.secret_scope` at call time; manifests persist the slot *name*, never a value; no `.env`/`auth.json`/keychain reads; no OAuth flows.
- **Approvals / unattended:** non-GET endpoints always require interactive `confirm` and fail clean under cron/gateway; the spec's own metadata never authorizes anything.

## Verification at the pinned sha

- `hermes plugins validate --install-deps`: PASSED (16 checks, incl. security scan — no dangerous findings)
- `hermes plugins doctor --ci`: 4 tools registered, declared == registered
- `python -m unittest discover tests`: **234 tests green** (208 module + red-lens regression suite + handler stack), pure stdlib
- Real E2E: learn petstore (19 endpoints + provenance) → draft refusal → commit → `api_call` HTTP 200 with real data; destructive PUT → `needs_confirmation`; invented endpoint refused; SSRF to 127.0.0.1 refused
- Covered on Python 3.12 (Ubuntu) and 3.14 (Windows + Android/Termux); 3.11 floor (core's minimum) declared but untested
- `requires_hermes": ">=0.22.0"` declared identically in `plugin.yaml` and this entry; zero `python_dependencies`; no hooks/middleware; `requires_env: []`

Submitted for the Hermes Agent Plugin Hackathon (deadline 2026-11-11, 5PM EST) by the plugin repo owner (monyinet).


## catalog: add elevenlabs-convai — operate ElevenLabs ConvAI agents (inspect, configure, harden, measure)
https://github.com/NousResearch/hermes-agent/pull/149550
State: open; created 2026-11-05T15:18:08Z

## What this entry adds

`elevenlabs-convai` — a plugin that operates ElevenLabs ConvAI voice agents from the agent,
with a measurement loop instead of dashboard guessing:

| tool | what it does |
|---|---|
| `convai_agents_list` | list agents in the workspace |
| `convai_agent_inspect` | brain (LLM), TTS model, voice, language, tool ids, prompt size, whether the prompt is date-grounded and has a brevity rule |
| `convai_agent_configure` | change `llm` / `tts_model_id` / `voice_id` — dry-run diff by default, backup + rollback |
| `convai_prompt_harden` | add `{{system__time_date}}` grounding + a brevity/style rule (idempotent); `action=restore` puts a backup back |
| `convai_voice_test` | real conversation over the ConvAI WebSocket: per-turn time-to-first-audio, spoken seconds, WAV/MP3, temporary model override restored afterwards |
| `convai_conversation` | authoritative transcript: turns, tool calls with parameters, termination reason, credits |

The point of the plugin is the loop **change one knob → measure → keep or revert**: every write
returns the exact `old -> new` diff and a backup path, and every test returns a number.

## Capability declaration matches reality

- `provides_tools`: 6 — exactly what `hermes plugins doctor` registers
  (`registrations: 6 tool(s), 0 hook(s)`).
- `provides_hooks` / `provides_middleware`: none; the plugin only calls `ctx.register_tool`.
- `requires_env`: `ELEVENLABS_API_KEY` only. It is read through Hermes' secret scope, never
  logged or written to disk.
- No core override, no self-updater, no telemetry, stdlib-only HTTP. Backups go under
  `$HERMES_HOME/cache/convai-backups`; audio only when the caller passes `save_audio_dir`.

## Validation at the pinned SHA (`e27779556bef21b2aad79362b64681b4c351ce7c`)

```
$ hermes plugins validate .        → Validation passed
  ✓ no core override — no runtime rebinds of Hermes core
$ hermes plugins doctor <installed> → OK: runtime discovery, manifest parsing, import, and registration passed
                                       registrations: 6 tool(s), 0 hook(s)
$ hermes plugins install c6zks4gssn-droid/hermes-elevenlabs-convai --ref e27779556bef21b2aad79362b64681b4c351ce7c → Installed
$ python3 tests/run_tests.py        → 5/5 passed
```

Live smoke run against a real account (test agent, one short Dutch turn):
`TTFA 3010 ms`, `11.6 s` of audio, conversation id returned, transcript fetched afterwards.

## Disclosure for reviewers

- Every call goes to `api.elevenlabs.io` with the user's own key.
- Reads are side-effect free; writes require `apply=true` and are backed up first.
- A conversation test spends real ElevenLabs credits on the account that owns the key.
- `convai_voice_test` needs the optional `websockets` package; the other five tools work without
  it and the sixth returns an error that names the missing dependency.

Demo video (<90 s, X, @NousResearch) and Typeform submission accompany this entry for the
plugin hackathon. Happy to adjust the entry, the description, or the pin.


## catalog: add CapRover Operator
https://github.com/NousResearch/hermes-agent/pull/149626
State: open; created 2026-11-05T17:49:40Z

Adds **CapRover Operator 0.3.1**, a community plugin I author and maintain, pinned to [`1d813b6e23c88c8641f8c891b46c2ae3f065e890`](https://github.com/fmercurio/hermes-caprover-operator/commit/1d813b6e23c88c8641f8c891b46c2ae3f065e890).

Version 0.3.1 makes two disclosure improvements: the README explicitly limits safeguards to this plugin's deployment workflow and ledger, and the native approval message warns that image startup may run migrations or other side effects. The deployment and approval logic is unchanged.

### Hackathon demo

[Watch the 64-second narrated demo on X](https://x.com/ztock/status/2118680536600269045). The video visualizes the recorded CyberChef update described below using stylized diagrams; it is not native UI footage. It shows the saved plan, native approval, lost acknowledgement, restart, replay refusal and explicit reconciliation.

The final hackathon form acknowledged **Submission Received** on November 6, 2026, with this PR and the public demo post. Catalog review and acceptance remain pending.

Small open-source teams need manageable operations to sustain control of their own infrastructure. CapRover offers a concrete starting point: an existing app, immutable images and observable Docker Swarm tasks. This MIT-licensed Hermes plugin makes that deployment reviewable and preserves uncertainty when a response disappears.

It provides first-use diagnostics, a saved state-bound plan, fresh native approval, a durable claim before one possible deployment POST and explicit read-only reconciliation. A consumed plan cannot be applied again. Version 0.3.0 adds historical operation cards showing the target, previous/requested images, status, separate metadata/task/HTTP evidence and next step. The plugin exports private immutable HTML and returns the public `::preview` directive for the assistant to emit in Hermes Desktop; JSON remains the fallback. The card cannot approve, execute or refresh an operation.

The adapter uses public plugin tools, `pre_tool_call` / `post_approval_response`, `tool_execution` middleware, profile settings/storage and `agent.secret_scope`. It registers five tools, two hooks and one middleware. The core preview renderer is reused without a private frontend import, Desktop bundle or Hermes core modification. Apply requires `in_process` isolation, Linux/macOS and a fresh correlated native human response. Missing approval provenance, smart/YOLO approval and model-supplied approval flags do not authorize execution.

### Operational disclosures

- **Scope of safeguards:** deployments through `caprover_apply` and this plugin's ledger only. Independent actions through Hermes terminal or `execute_code`, other plugins, direct CapRover API calls and external operators require their own access controls and approvals.
- **Network and credentials:** the configured CapRover HTTPS origin and optional fixed health URL only; health receives no API token. `CAPROVER_OPERATOR_TOKEN` comes through Hermes secret scope. No credential-file reads, telemetry, hosted backend or self-updater. The app allowlist does not narrow the token's server-side privileges.
- **Data:** CapRover returns multiple app definitions, potentially including environment values. The plugin handles them in memory and retains only the configured app's keyed fingerprint and sanitized evidence. Private local plans, receipts and HTML snapshots can identify the app, origin and images; raw definitions, credentials, task logs and health response bodies are excluded.
- **Deployment:** one existing configured app and an immutable image only. No shell, app/configuration management, migration tool or automatic rollback. Image startup may have side effects, including migrations. Another operator can race the separate preflight read and deployment write; this is not distributed exactly-once or server-side compare-and-swap.
- **Evidence:** HTTP and metadata can precede task convergence. `verified` additionally requires supported exact-image task and replica evidence. Unsupported servers receive weaker statuses. Cards and receipts are dated observations, not ongoing availability or migration guarantees. An attempt marker does not establish server delivery or request count; approval is a requirement, not an invented stored event.
- **Processes and source:** normal plugin operation starts no daemon or shell. Separate validation scripts explicitly identify fixtures/simulated approval callbacks. The real live-model capture used a separately authorized disposable Docker-in-Docker CapRover and fixed-route TLS proxy; bootstrap writes are outside its plugin-POST count. No production service or credential was used. MIT attribution and source provenance are retained.

### Validation at the exact 0.3.1 pin

Hermes floor `>=0.22.6`; plugin version `0.3.1`.

- Official `plugins validate --install-deps`: **15/15, safe, no warnings**; dependency preparation completed. Official `plugins doctor --ci`: **passed** discovery, import and registration. Both used the exact public commit in an isolated checkout with a disposable Hermes data root, a dedicated runtime cache and no production credentials.
- Standalone local suite: **123 passed, 9 native tests skipped** because that interpreter does not include Hermes. [Exact-pin CI](https://github.com/fmercurio/hermes-caprover-operator/actions/runs/42262358851): **all five jobs passed**, covering Linux/macOS with Python 3.11/3.14 plus **nine native Hermes tests, zero skipped**, including the real AIAgent approval pipeline.
- Structural validation: **980 catalog files valid, zero errors**; this entry has no warnings. Five warnings concern unchanged entries. Local structural tooling used Python 3.14.9 / ruamel.yaml 0.18.16; the upstream structural CI uses Python 3.11 / ruamel.yaml 0.18.17. The upstream catalog CI and maintainer acceptance remain separate gates.

### Recorded lab evidence (0.3.0)

The published demo and real CapRover capture predate the 0.3.1 disclosure changes. They remain attributed to their original revision; they are not a new deployment run on 0.3.1.

- [Recorded 0.3.0 validation](https://github.com/fmercurio/hermes-caprover-operator/blob/b1b8f0461651b84e5b00067437014a2fc4754741/docs/real-cli-validation-v4.md): real CyberChef **11.4.0 → 11.5.0** on CapRover 1.16.0, native CLI/Desktop, live model, inline card, deliberately lost acknowledgement after backend HTTP 200 / Captain 100, actual gateway/CLI restart, replay refusal and read-only reconciliation to exact-image tasks plus HTTP 200. The new **Parse PGP Key** operation then processed a public RFC fixture in the original app UI. **One plugin deployment POST** was recorded; all **12** captured plugin source hashes match the linked **0.3.0** revision, before the 0.3.1 wording changes.
- User-authorized lab automation operated the actual native approval flow. No synthetic callback or manual human keypress is claimed for that run; both CLI and Desktop were attached and the exact responding UI was not attributed. The [public trace](https://github.com/fmercurio/hermes-caprover-operator/blob/b1b8f0461651b84e5b00067437014a2fc4754741/evidence/real-hermes-cli-trace-v4.json) explicitly documents descriptive corrections and path sanitization, preserving the recorded operation facts and counters. Earlier evidence remains separately labeled and unchanged.

The disposable container, private volumes, dedicated network and task-owned services were removed after capture. These are dated integration results. This PR changes only `plugin-catalog/caprover-operator.yaml` and requests community catalog review; catalog acceptance remains pending.



## catalog: add zaprite — take payments from a Hermes chat
https://github.com/NousResearch/hermes-agent/pull/150568
State: open; created 2026-11-07T08:05:23Z

Adds `zaprite` to the plugin catalog.

**What it does.** A merchant talks to Hermes; Hermes takes the payment. The plugin wraps all 20 published operations of the Zaprite v1 API (14 paths): create an order, invoice or Lightning/on-chain quote, hand back one `checkoutUrl` for card, ACH, bitcoin, Lightning, USDT and USDC, then re-fetch until the order is paid. It also covers contacts, payment links, event tickets, and the merchant's books — `zaprite_report`, `zaprite_list_overdue`, `zaprite_doctor`.

**What it refuses.** `zaprite_update_order` sets `COMPLETE` or `expires_at` and nothing else. Zaprite's PATCH endpoint also accepts `PAID`; this tool will not send it, because only money arriving may mark an order paid and only a person may record cash. `pre_tool_call` returns an approval request for every write, with a ten-minute TTL per exact call; the plugin cannot approve itself, and in cron it fails closed rather than hanging.

**Disclosure (rule 13).**
- **Network:** every call goes to `https://api.zaprite.com`. No other host, no telemetry.
- **Credentials:** reads `ZAPRITE_API_KEY` through the Hermes secret store on each call, never from a file and never logged. Setup guides the user to Hermes → Tools → Zaprite; it never asks for a key in chat.
- **Writes:** only after the user approves that exact call. `zaprite_create_webhook` registers a URL the user supplies; the plugin registers nothing by itself.
- **Background:** none by default. The optional `zaprite-paid-digest` blueprint is a read-only daily report that runs only if the user adds it.
- **Payment truth:** a Zaprite webhook is id-only and unsigned, so the plugin re-fetches the order and treats the re-fetch as the only source of truth. A webhook is not a payment.
- **No self-update:** no update check, no downloader; the catalog SHA is the release.

**Known gaps, stated on the entry.** The Zaprite API has no route for connections, payment-link creation, POS, events, recurring invoices, refunds or branding, so the plugin hands those to a person through `zaprite_bridge_handoff` with a dashboard link instead of pretending.

**Verification at the pinned commit**
- `hermes plugins validate .` → `Validation passed` (declared tools, hooks, middleware match registrations; security scan safe; no core override).
- `142 passed` in the plugin's test suite.
- Catalog entry: `scripts/validate_plugin_catalog.py` → `OK: 1 file(s) valid`.
- The plugin is installed and driving a real shop: orders created through it reconcile in the Zaprite dashboard, and a live checkout at `hackathon.plugnstay.supplies` takes real payments.

Install and try it without a Zaprite account: the plugin's `zaprite_setup` explains the sandbox org and where the key goes.


## plugin-catalog: add hermes-quote-to-chat (Desktop: removable quote cards merged at send)
https://github.com/NousResearch/hermes-agent/pull/150201
State: open; created 2026-11-06T17:39:26Z

Adds one catalog entry: `plugin-catalog/hermes-quote-to-chat.yaml`.

**What it is.** Codex-style quote cards for Hermes Desktop. Select text outside an input and press **Add to chat**: the excerpt becomes a removable card above the composer, and your question stays a separate draft. On send, the quotes are prepended once as Markdown blockquotes.

**How it differs from the listed `quote-ask` (rule 16).** `quote-ask` pastes the selection into the draft as text. This plugin keeps quotes out of the draft as cards and merges them only at send time through `composer.middleware`. That gives behaviour a paste cannot have:
- the draft is never edited; several quotes can be collected and removed one by one (× per card);
- quotes are scoped to the chat they were taken in (`host.state.focusedStoredSessionId`), so switching chats never leaks a quote;
- a busy-agent send goes through `host.composer.submit` with the quote attached;
- a rejected send that restores the draft also restores its quotes.

Different architecture (send-time middleware plus a composer slot, not draft insertion), not a fork. No code is shared.

**Surfaces it uses.** Desktop-only, `desktop/plugin.js`, plain ESM importing only `@hermes/plugin-sdk` and `react/jsx-runtime`:
- `composer.top` slot: the quote cards
- `composer.middleware`: prepend quotes on send
- `host.composer.getDraft` / `submit` / `setDraft` / `focus`
- `host.state.focusedStoredSessionId`, `host.state.busy`
- `ctx.addEventListener` / `ctx.setTimeout` / `ctx.onDispose`, `ctx.i18n.register` (en + ru)

No Python half, tools, hooks or env vars. The floating button is the plugin's own element on `document.body`. The plugin never queries the app's markup (`data-slot` / `data-tour` / …), patches prototypes, or touches core modules.

**Verification at the pinned commit** (`cb11d9c6d9bed2d06cd5f20695ba1dbc8bf0e703`):

```
✓ manifest — plugin.yaml parses
✓ requires_hermes — spec '>=0.22.5' parses
✓ loadable — entry: desktop/plugin.js
✓ security scan — safe
✓ no core override — no runtime rebinds of Hermes core
✓ desktop surface — stays inside the plugin SDK surface
Validation passed.
```

`scripts/validate_plugin_catalog.py plugin-catalog/` → `OK: 1065 file(s) valid`.

16 jsdom behaviour tests in `test/run.mjs`. They cover selection, cards and ×, per-chat scope, send-time merge, rejected send, busy send, a non-composer editable left alone, slash commands, cleanup, and a guard that the source never selects app markup. An earlier build is in daily use on Hermes Desktop 0.22.5.

**Disclosures (rule 13).** Reads `window.getSelection()` and the selection rectangle. Adds one button element to `document.body`. Reads the live draft through `host.composer.getDraft`. Keeps quotes in memory only. No network calls, credentials, files, telemetry or background work.

Submitted by the plugin repository owner (rule 5): `ivanvanes18/hermes-quote-to-chat`. Hackathon entry.


## feat(plugin-catalog): add zeromem
https://github.com/NousResearch/hermes-agent/pull/149741
State: open; created 2026-11-05T22:37:28Z

## What does this PR do?

Adds `plugin-catalog/zeromem.yaml` for [zeromem](https://github.com/ptaranat/zeromem), submitted by the repository's owner (`ptaranat`). It's an entry for the Hermes Agent Plugin Hackathon, pinned to `f7e669c47cc0f6c9867829c37af8e4fc2803fe15`, subdir `hermes/zeromem`.

zeromem is a memory provider that keeps every message word for word in one SQLite file. Storing and searching make no LLM calls, so they cost no tokens. It's a Rust implementation of Zero-Mem by Xiao et al. ([paper](https://arxiv.org/abs/2607.29377), [code](https://github.com/Zero-Mem/Zero-mem)), with the core shipped as the `zeromem` wheel on PyPI.

Surfaces used: `ctx.register_memory_provider`, and a `cli.py` with `register_cli` for `hermes zeromem import`. The import backfills past conversations from `hermes sessions export`, so someone switching from another provider keeps their history.

The tools are `zeromem_recall`, `zeromem_stats` and `zeromem_forget_session`. They're provided through the memory provider's `get_tool_schemas`, so `hermes plugins validate` warns that `register()` didn't register them. The check passes and the entry declares them so the listing is accurate, the same way `cognee.yaml` does.

## Disclosures (rule 13)

- **Network:** downloads the bge-small-en-v1.5 embedding model (about 130MB) from Hugging Face on first run, into `~/.hermes/memory/zeromem-models`. No other network calls, and no telemetry.
- **Dependencies:** `zeromem>=0.4,<0.5` from PyPI. Prebuilt abi3 wheels for Linux x86_64 and aarch64, macOS arm64 and Intel, and Windows x86_64, published with PyPI Trusted Publishing.
- **Stored data:** every user and assistant message goes into `~/.hermes/memory/zeromem.db` as plain text. Nothing leaves the machine.
- **Background work:** one writer thread per session, and prefetch adds recalled messages to context before each turn.
- **Reads outside its own data:** `hermes zeromem import` runs `hermes sessions export` to read session history. It previews by default and only writes with `--yes`.
- **Credentials:** none.

The plugin's README at the pin carries the same list.

## Type of Change

- [x] New feature (catalog entry only)

## Changes Made

- `plugin-catalog/zeromem.yaml`: new entry, `tier: community`, `category: memory`, `requires_hermes: ">=0.22"`, which matches `plugin.yaml`.

## How to Test

```
hermes plugins validate /path/to/zeromem/hermes/zeromem --install-deps
```

At the pinned commit this passes on Hermes 0.22.5 with one warning, the `provides_tools` one above. The security scan reports `safe` and the no core override check passes.

`hermes zeromem import` was tested on a copy of a real store: 2,384 turns from 157 sessions, and a second run found nothing new.

## Checklist

- [x] I've read the Contributing Guide and the catalog admission rules
- [x] My commit message follows Conventional Commits
- [x] I searched for existing PRs (the name `zeromem` is free in the catalog)
- [x] My PR contains only changes related to this entry
- [x] I've tested on my platform: Ubuntu 26.04, Hermes 0.22.5


## Machine-readable output for `hermes cron` and `hermes config` (external clients currently read private files)
https://github.com/NousResearch/hermes-agent/issues/118072
State: open; created 2026-09-21T10:03:41Z

## What

External clients (mobile app, web dashboard) that drive a Hermes install need a **stable, machine-readable** view of cron and config. Today there is none, so clients read private files and parse YAML:

- `hermes cron list` has no `--json` (only `--all`), so clients read `~/.hermes/cron/jobs.json` directly.
- There is no `hermes cron runs --json`; run history has to be scraped.
- `hermes config get <key>` prints a value, but there is no JSON form or schema; clients edit `config.yaml` themselves.
- `hermes config set` rewrites the whole file and **drops every comment** (measured: 285 lines/21 comments -> 263/0). Clients that must not destroy the user's config have to implement their own line-editing, which is exactly the sort of private-format coupling that breaks on upgrades.

## Why it matters

Because these are private formats, any internal change lands as a silent break for external clients. In our case a ~2,000-commit update touched config read/write and cron model behaviour, and the client broke without any signal — a model-switch call started returning 400 because a hard-coded catalogue no longer matched the live `model.default`.

## Ask

1. `--json` (stable, versioned) on at least: `hermes cron list`, `hermes cron runs <job>`, `hermes cron status`, `hermes config get`, `hermes --version`.
2. A documented schema/version marker in those payloads so clients can detect drift instead of guessing.
3. Ideally a comment-preserving `config set` (or `config set --line`), since whole-file rewrites silently destroy user documentation in `config.yaml`.

Happy to test a branch if that helps.


## plugin-catalog: add tightbeam (YouTube catalog optimizer + multi-platform shorts publisher)
https://github.com/NousResearch/hermes-agent/pull/149920
State: open; created 2026-11-06T07:36:18Z

## What it does

**Tightbeam** — beam shorts to every platform and keep your whole YouTube catalog optimized. Built by Skeptical Agency from production pipelines that run a real 300K-sub channel. Entry for the Hermes Agent Plugin Hackathon.

Two pillars, 11 tools, 2 automation blueprints:

- **YouTube optimizer**: `yt_audit` (full-catalog scan, kind classification, missing-metadata buckets), `yt_watch` (watermark new-upload detector), `yt_optimize` (rule-based tags + host-LLM-scored titles + policy defaults, 412 backoff, TEST_AND_COMPARE fallback), `yt_sweep` (budgeted, resumable, quota-capped batch mode). Blueprints: *post-publish optimizer* (daily) and *catalog sweep* (nightly).
- **Multi-platform publishing (OpusClip)**: `publish_upload` (resumable), `publish_submit` (passthrough, captions forced off), `publish_schedule` (±2h collision check, FB≤255 / X≤280 / no-'>' caps asserted in code, LLM-drafted per-platform copy, read-back verified), `publish_status` (silent-failure triage with exact reconnect fixes), `publish_unschedule`, `tightbeam_credits` (dual-pool gating).

## Surfaces used

`ctx.register_tool` (11 tools, own `tightbeam` toolset), `ctx.register_automation_blueprint` (2), `ctx.register_skill` (1 bundled setup/workflow skill), `oauth:` manifest declaration + `credentialed_provider_request` (rule 11 — plugin never sees the YouTube token), `ctx.dispatch_tool` to the user's Hermes-managed `opusclip` MCP connection (rule 11 — no vendor token reads/refreshes), `ctx.llm.complete_structured` for titles/copy, `plugin_data_dir` for resumable state, `config_schema` for user policy (4 settings). No hooks, no middleware, no capabilities, no pip dependencies (pure stdlib + host APIs).

## Test evidence

- `hermes plugins validate --install-deps` at the pinned SHA: passed clean — manifest, oauth clients valid, declared tools match, security scan safe, no core override, no collisions.
- Live end-to-end on a production channel: 994-video full audit through the host-owned grant; real `videos.update` (tag fill) verified by read-back; `yt_watch` watermark detection against live uploads.
- Live OpusClip dispatch: 26-post schedule-window read matching ground truth exactly; dual credit pools read; failure triage surfaced a real TikTok connection revocation with the correct reconnect fix.

## Disclosure (rule 13)

- Video metadata (titles, descriptions, tags, ids) is sent to the Google YouTube Data API through the **user's own** OAuth client, declared under `oauth:` in the manifest; Hermes stores/refreshes the grant; the plugin never receives the token.
- Video bytes (to the signed URL OpusClip itself returns) and post copy are sent to OpusClip through the **user's Hermes-managed MCP connection**; the plugin never reads or refreshes those credentials.
- Title/copy generation uses the Hermes host LLM under host credentials (`purpose`-tagged calls).
- Plugin state (audit, sweep progress, watermark) is stored locally under `<HERMES_HOME>/plugin-data/tightbeam/`. No credentials are stored by the plugin. No telemetry.
- Publishing is irreversible once the platform window passes; schedule/unschedule verify state and report honestly but cannot un-publish.
- Both pillars require third-party accounts: a Google Cloud project (free-tier quota fine) and an OpusClip account; each pillar degrades cleanly with setup hints when its account is absent (`tightbeam_status` probes both).


## feat(plugin-catalog): add hermes-spendguard community plugin by Blackleets
https://github.com/NousResearch/hermes-agent/pull/149189
State: open; created 2026-11-05T01:08:43Z

## Summary

Add a community catalog pin for https://github.com/Blackleets/hermes-spendguard at
`a6ca90cb5449c0c6bc6312551a12283b52667447` (tag `v0.1.0`).

This entry is also the author's submission to the Hermes Agent Plugin
Hackathon (Nov 2026).

## What does this PR do?

Adds one catalog entry, `plugin-catalog/hermes-spendguard.yaml`, so the plugin is
discoverable via `hermes plugins catalog` / `hermes plugins search` and
installable by name at a reviewed, pinned commit:

```
hermes plugins install hermes-spendguard
```

Nothing else in this repository is touched.

## The plugin

SpendGuard is a budget-enforcement plugin for Hermes Agent — the money
layer the catalog's analytics tools don't provide:

- **Accounting.** `post_api_request` / `post_auxiliary_call` hooks record
  every provider call in a local SQLite ledger: model, provider, token
  counts and cost. Cost is the provider-reported figure when the response
  carries one, otherwise a public list-price estimate (table dated
  2026-11-04, user-overridable). Unknown models are counted by tokens and
  marked **unpriced** — a price is never invented. No message text is
  ever stored.
- **Budgets.** Daily and monthly USD caps with context warnings at
  configurable thresholds (75% / 90% by default), a dashboard tab and a
  Desktop page with live budget bars, and per-model reports.
- **Enforcement.** At the cap, a `pre_llm_call` hook blocks new turns
  *before any inference* — the block makes zero model calls, so hitting
  the wall is free — and an optional strict `pre_tool_call` backstop
  pauses tool calls mid-turn. `warn` mode advises only.
- **The agent cannot raise its own cap.** There is deliberately no tool
  that changes a budget; budgets change only via the human-typed
  `/spendguard` slash command. The two agent tools
  (`spendguard_status`, `spendguard_report`) are read-only.

Surfaces use public plugin APIs only: tools, hooks, one slash command, a
bundled skill (`ctx.register_skill`), a read-only FastAPI dashboard
router and a Desktop page using only `@hermes/plugin-sdk` / `react`.

## Disclosure (catalog rule 13)

- **Network:** none. SpendGuard makes no outbound requests of any kind.
- **No** self-updating code, **no** shell commands or subprocesses, **no**
  credentials or env vars read, **no** telemetry, **no** background
  processes.
- **Writes:** the ledger (`spendguard.db`) and config
  (`spendguard.config.json`) only, under the plugin data dir
  (`plugin_data_dir("hermes-spendguard")`), never in the install tree.
- Offline test suite (14 tests) covers pricing/normalization, ledger
  math, budget state transitions, hook blocking/warning behavior,
  command handling and registration through a stub `PluginContext`. The
  plugin was also loaded successfully through the Hermes plugin loader
  (`plugins.plugin_loader.load_plugin_module`) against a local checkout.

## Admission checklist

- [x] I am the owner/maintainer of the submitted plugin repository (rule 5)
- [x] Repository is public and tagged (`v0.1.0`) (rules: public + released)
- [ ] `hermes plugins validate . --install-deps` run locally — PENDING a
      current Hermes install on the author's machine; CI validation is
      the authoritative run
- [x] Declared capabilities in the entry match `plugin.yaml` at the pin (rule 6)

## [Feature]: Desktop plugin SDK: open a session in a new window, and write to the Desktop log
https://github.com/NousResearch/hermes-agent/issues/149171
State: open; created 2026-11-05T00:39:10Z

### Problem or Use Case

Waiting On You is a Desktop plugin that lists what your agents are waiting on you for. Each task card has "Open chat" and "Open in new window", and the panel logs its own failures so a user can send a useful bug report.

The plugin SDK covers the first case with `host.openSession(storedSessionId, options)`. Two things still need the raw preload bridge:

1. **Open a stored session in a new window.** We call `window.hermesDesktop.openSessionWindow(sessionId, { profile, connectionId })`, the same bridge as Desktop's own "Open in New Window".
2. **Write a line to the Desktop log.** We call `window.hermesDesktop.logLine('[waiting-on-you] …')` so plugin errors land in the same log users already attach to bug reports.

`hermes plugins validate` correctly flags both under catalog rule 8 ("raw bridge"). We feature-detect them and fall back (same-window open; toast only), but any plugin that wants these behaviours has to reach past the SDK.

### Proposed Solution

Two small SDK verbs:

```ts
// Same options as host.openSession, opens a separate window when supported.
host.openSession(storedSessionId, { ...options, newWindow: true }): Promise<void>

// Appends "[<plugin id>] <line>" to the Desktop log. The host prefixes the
// plugin id, caps the line length, and rate-limits, so a plugin can't spoof
// core log lines or flood the file.
host.log(line: string, level?: 'info' | 'warn' | 'error'): void
```

If `newWindow` isn't supported (web dashboard, older builds), it can reject or fall back to the same window; either works as long as it's documented.

### Alternatives Considered

- Keep the feature-detected bridge calls: works today, but it fails the catalog's SDK-only rule and can break on any release.
- Drop both features: "Open in new window" is the main way people use the panel next to a running chat, and without logging, plugin bug reports have no detail.

### Additional Context

Plugin: Waiting On You (Hermes Plugin Hackathon entry). The bridge calls are in `src/ui/openChat.ts` and `src/ui/notify.ts`. Related SDK requests: #106713 (open sessions in an in-window split), #148224 (pop-out window verb).


## plugin-catalog: add Workgraph
https://github.com/NousResearch/hermes-agent/pull/150453
State: open; created 2026-11-07T03:03:23Z

Workgraph lets people explore agent-built products through a local branching tree of saved source, SQLite development data, explicit context, actual screenshots, and independently replayed behaviors. A user can continue from an exact saved point or ask an existing agent to adapt one feature into a fresh branch while preserving the target's data and protected behaviors.

This adds one community catalog entry, pinned to the public **2.0.0** release at `37c7280a514d3fa23e7193f44b5123d1f9c90163`. Submitted by the plugin repository owner for the Hermes Agent Plugin Hackathon.

- [Source](https://github.com/aliiqbal24/workgraph)
- [70-second launch film: actual saved model results](https://github.com/aliiqbal24/workgraph/releases/download/v2.0.0/workgraph-launch-v4.mp4)
- [Installable release and full narrated walkthrough](https://github.com/aliiqbal24/workgraph/releases/tag/v2.0.0)
- [Current upstream admission validation — passed on the exact release](https://github.com/aliiqbal24/workgraph/actions/runs/42331776805)
- [69-test acceptance suite — passed](https://github.com/aliiqbal24/workgraph/actions/runs/42331776985)
- [Live testing workflow](https://github.com/aliiqbal24/workgraph/blob/main/docs/live-testing.md)

Native surfaces: one tool (`workgraph`), three observer hooks (`pre_tool_call`, `pre_llm_call`, `on_session_finalize`), and tool request/execution middleware. No runtime patching or built-in tool override. The upstream validation covers the declared capability set; installed Hermes Plugin Doctor also passes.

### Disclosure

- Reads/writes selected local Git repositories and common Git metadata, including explicit notes, configured development snapshots, browser artifacts, and task logs.
- Executes Git, bubblewrap, Chromium/Playwright, approved app preparation/runtime commands, and operator-started Hermes/Codex/Claude subprocesses. Existing runtimes retain their normal sign-in and permission policy; Workgraph does not own model credentials or auto-approve runtime actions.
- Starts a persistent loopback-only controller and separate disposable app processes. Tasks can continue after browser closure. Explicit stopping preserves partial agent work. Completed scratch copies are cleaned up; saved history remains.
- Approved app commands and existing agent runtimes can make normal network calls. The app filesystem sandbox shares the host network. No telemetry, cloud repository upload, credential store, self-updater, or bundled executable payload.
- Browser capture uses separately installed optional dependencies and Chromium; Playwright's official FFmpeg helper is installed during documented setup. Source/MCP history works without browser extras.
- Captures configured non-secret SQLite development data and screenshots. Password fields are omitted from flow recording; other entered test fixtures can be retained. Hosted services, production databases, process memory, and hidden conversation state are not restored.

The install scanner's CAUTION findings cover these disclosed subprocess/persistence paths, installation examples, fixture bytes/traversal tests, and the CI-only `sudo apt-get` installation of bubblewrap. The exact upstream validator passes with warnings; no scanner or host permission policy is disabled.

### Actual behavior evidence

A real UI-started Codex task adapted the board into the focused target, changing only `client/app.js`. The target's database blobs remained byte-identical. Independent browser replays passed comment persistence, new-issue persistence, and priority filtering. Initial example directions and the source-board regression are scripted and disclosed; captured states, model results, screenshots, and check recordings are real. Native Hermes installed from the public pinned repository has now completed a real edit: only `view.json` changed; all eight issues, SQL schema, and rows remained intact; all three independent checks passed. A fresh Hermes conversation discovered and opened the native workspace tool without a new work attempt. The new launch film shows the saved result and an actual tab close/reopen.

![Actual Workgraph product tree](https://raw.githubusercontent.com/aliiqbal24/workgraph/37c7280a514d3fa23e7193f44b5123d1f9c90163/docs/images/product-tree.png)

![Actual comparison view](https://raw.githubusercontent.com/aliiqbal24/workgraph/37c7280a514d3fa23e7193f44b5123d1f9c90163/docs/images/product-compare.png)



## feat(plugin-catalog): add procgen-studio
https://github.com/NousResearch/hermes-agent/pull/150293
State: open; created 2026-11-06T21:02:31Z

## What does this PR do?

Adds one catalog entry, `plugin-catalog/procgen-studio.yaml`, for **Procgen Studio** ([iamlukethedev/hermes-procgen-studio](https://github.com/iamlukethedev/hermes-procgen-studio)), pinned to `a2ecd11c3e12b0c10aa0faecb5d1fb305ea41419` (on `main`). Submitted by the plugin repository's owner, Lucas ([@iamlukethedev](https://github.com/iamlukethedev)), per rule 5. Entry for the Nous Hermes Agent Plugin Hackathon.

Procgen Studio is an image and video backend that draws with code. The user's configured model writes SVG or Python drawing programs, which are rendered locally to PNG (and MP4/GIF for video). The editable source and a reproducible seed are saved next to each image. No image API key is needed. It supports STYLE.md art contracts with six presets, a critic pass with bounded redraws, and local seed re-rolls and restyles.

### Hermes surfaces used

- `ctx.register_image_gen_provider` and `ctx.register_video_gen_provider` (the backend itself).
- `/procgen` slash command (`ctx.register_command`) and the `hermes procgen` CLI command (`ctx.register_cli_command`).
- Desktop pane (`desktop/plugin.js`, plugin SDK only) plus a dashboard manifest.
- A bundled skill, `procgen-art-direction` (`ctx.register_skill`).
- Two auxiliary task slots, `procgen_draw` and `procgen_critic` (`ctx.register_auxiliary_task`), so users can pin a coding model for drawing and a vision model for review.
- `ctx.llm` for every model call, `ctx.state` / `ctx.get_config` for state and settings.

It registers no model tools, hooks or middleware and requires no env vars, so the `capabilities:` block is empty. `hermes plugins validate` confirms this matches the registrations at the pinned commit.

### Disclosures (rule 13)

- **Network:** no network calls of its own. Every model call goes through `ctx.llm` on the user's configured provider.
- **Code execution:** model-written Python drawing programs run in a separate sandboxed Python process (AST import allowlist, audit hook refusing network, subprocess and file access outside the job directory, CPU/memory/file-size limits, wall-clock timeout). Setting `allow_python: false` switches to SVG/pixel-only.
- **Subprocess:** invokes the system `ffmpeg` as a subprocess for video only.
- **Reads:** a `STYLE.md` from the session working directory (when it has a `preset:`/`palette:` line), or a user-configured `style_file`.
- **Writes:** renders under `$HERMES_HOME/plugin-data/procgen-studio/` and `$HERMES_HOME/cache/generated/`, plus an optional user-configured output folder.
- **None of:** telemetry, credentials, background processes, or self-updates.
- **Dependencies:** installs `cairosvg` (needs the system cairo library), `numpy` and `Pillow`.

## Type of Change

- [x] New feature (non-breaking change that adds functionality): new catalog entry, no code changes.

## Changes Made

- `plugin-catalog/procgen-studio.yaml` (new, only file changed).

## How to Test

1. `python3 scripts/validate_plugin_catalog.py plugin-catalog/procgen-studio.yaml` → `OK: 1 file(s) valid`.
2. Clone the plugin at the pinned SHA and run `hermes plugins validate <checkout> --install-deps`. Locally every check passed: manifest, requires_hermes, config schema, requires_env, loadable (`__init__.py`, `desktop/plugin.js`), python dependencies, capability probe, declared tools/hooks/middleware match registrations, security scan `safe`, no core override, desktop surface.
3. All `image` and `screenshots` URLs are pinned to the same SHA on `raw.githubusercontent.com` and return 200.

## Screenshots / Logs

![Procgen Studio banner](https://raw.githubusercontent.com/iamlukethedev/hermes-procgen-studio/a2ecd11c3e12b0c10aa0faecb5d1fb305ea41419/examples/banner.png)

![Icons, ember preset](https://raw.githubusercontent.com/iamlukethedev/hermes-procgen-studio/a2ecd11c3e12b0c10aa0faecb5d1fb305ea41419/examples/01-icons-ember.png)

## feat(plugin-catalog): add gemini-live plugin
https://github.com/NousResearch/hermes-agent/pull/150251
State: open; created 2026-11-06T19:35:30Z

Hackathon entry. Adds `plugin-catalog/gemini-live.yaml`, pinned to a full commit SHA.

## What it does

Full-duplex Gemini Live calls in Hermes Desktop and the web dashboard. The voice takes the name of the profile the call started from, delegates real work to that agent, and keeps talking while it runs. With `hermes-mobile-device-access` and a paired iPhone, it also sets alarms, timers and reminders directly.

## How it differs from the listed Gemini plugins

This is an independent project, not a fork. `gemini-live-bridge` has no agent tools, and `hermes-gemini-live` centres on a delegation task board. This plugin adds thread, bot-chat and subagent monitoring and steering, MCP tools, memory and conversation search, a three-layer read-only command path, a dashboard tab, and personas.

## Disclosure

- **Network:** the client streams microphone audio to `generativelanguage.googleapis.com` on a single-use ephemeral token. The backend calls Google's Gemini API with the key.
- **Sent to Gemini:** audio, the voice's instructions, tool results and, unless `share_chat_context` is off, the open chat's title and latest messages. On Gemini's free tier, Google may use content to improve its products.
- **Reads outside its own data:** `profile.yaml` for the display name, built-in memory notes, session history, thread and profile lists, and paired device grants when the phone plugin is installed.
- **iPhone tools:** with `hermes-mobile-device-access` and a paired iPhone, the voice can call that plugin's alarm, timer and reminder tools directly, without a Hermes turn. Only those eight tools are allowed, each is offered only when the device's grant covers it, and the bridge checks the grant again. Alarm and reminder details reach Gemini as tool results. `phone_tools` turns this off.
- **Shell commands:** only with `readonly_shell` or `system_checks` on, both off by default, and only under the layers in the README.
- **Credentials:** read through `agent.secret_scope`; the browser never receives the key.
- **Approvals:** Hermes decides what needs asking. The plugin shows the request and passes on the user's answer through `approval.respond`, one time only. The voice model has no way to answer. The opt-in `voice_approval` setting accepts the user's own spoken approve or deny, matched on the microphone transcript and ignored while the voice speaks.
- **Background processes and telemetry:** none.

## Checks

`hermes plugins validate` passes on a fresh clone of the pinned commit (`187650f0`): security scan safe, no core override, desktop surface inside the SDK. Plugin tests: 65 Python and 37 engine tests pass. Tested on macOS Hermes Desktop against a Linux backend.

## Companion change

An optional [Desktop PR](https://github.com/NousResearch/hermes-agent/pull/150252) adds a `composer.voiceEngines` area so plugins can appear in the voice picker. The plugin works without it.

## Open offer

We'd love Gemini Live as an option in the mobile voice picker. If the maintainers prefer, we're happy to contribute it to Hermes as a built-in voice engine next to GPT Live.

## Screenshots

![Approval on a call](https://raw.githubusercontent.com/cineglobe/hermes-gemini-live/187650f0b90ec8f19dba5928b3a4caf093d5aa80/docs/assets/approval.png)

![Transcript](https://raw.githubusercontent.com/cineglobe/hermes-gemini-live/187650f0b90ec8f19dba5928b3a4caf093d5aa80/docs/assets/transcript.png)

🤖 Generated with [Claude Code](https://claude.com/claude-code)






## feat(desktop): let plugins add engines to the voice picker
https://github.com/NousResearch/hermes-agent/pull/150252
State: open; created 2026-11-06T19:35:33Z

Companion change for the **Gemini Live** plugin
([cineglobe/hermes-gemini-live](https://github.com/cineglobe/hermes-gemini-live)), submitted to the
Hermes plugin hackathon.

## Why

The composer's voice-engine picker offers *Speech-to-text + Hermes voice* and *GPT-Live*. A plugin
that ships its own realtime engine has nowhere to appear there, so it has to add a second call
button and users have two different "talk" buttons. The plugin SDK has no seam for this, and a
catalog plugin may not edit core files.

## What

- A new data area, `COMPOSER_AREAS.voiceEngines` (`composer.voiceEngines`), with payload
  `ComposerVoiceEngine { label, shortLabel, detail?, start() }`. It is exported from
  `@hermes/plugin-sdk` like the other composer areas.
- `VoiceEngineRows` lists the registered plugin engines after the core rows. Picking one is a
  **renderer-side** choice (`store/plugin-voice-engine.ts`), persisted per (connection, profile)
  with the same scope key as `$voiceLiveStatus`. Picking a core row clears it and writes
  `voice.voice_chat_mode` exactly as before. The backend keeps refusing unknown modes (4002) and is
  untouched.
- The start-voice button and the folded voice menu call the chosen plugin's `start()`. If that
  plugin is no longer registered, the button falls back to the core engine. If `start()` throws,
  the error shows and the core engine starts, so a broken plugin can't swallow the click.
- Malformed payloads (no `start`, blank labels, duplicate ids) are dropped, so a broken plugin
  can't blank the picker or add a row that does nothing.

There are no new strings, because labels come from the plugin. There is no backend change, and
nothing changes for users without such a plugin.

## Tests

`src/app/chat/composer/voice-engines.test.ts` covers payload validation and ordering, per-scope
persistence, fallback when the plugin is gone, and clearing back to the core engine.

## Mobile

The mobile app's voice picker currently offers only GPT Live, and its source isn't public, so this
patch can't cover it. **We'd love an installed Gemini Live plugin to appear as an option in the mobile
picker too, so people can choose it as their voice engine on any device.** The
plugin's backend already serves everything a client needs:

- `POST /api/plugins/gemini-live/session` returns a single-use ephemeral token with the model,
  voice, instructions and tools locked server-side. The key never leaves the backend.
- `POST /api/plugins/gemini-live/tool` runs the server-side tools.
- `src/engine.js` is the framework-free call engine (audio, socket, tool router, delegation) that a
  mobile client can port directly.

## Open offer

If the maintainers would like it, we're happy to contribute Gemini Live to Hermes as a **built-in**
voice engine everywhere, next to GPT Live: the backend, Desktop, the dashboard, and help with
mobile. That would include the multi-layer `run_readonly` safety design and the thread/bot
monitoring tools. Tell us which shape you'd prefer.

## Testing status

The patch applies cleanly to current `main`. I haven't run the Desktop test suite or a Desktop build on this branch, so CI will be the first full run. The plugin works without this change: it falls back to its own composer button.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## feat(plugin-catalog): add trust-ladder
https://github.com/NousResearch/hermes-agent/pull/149738
State: open; created 2026-11-05T22:26:03Z

## What does this PR do?

Adds `plugin-catalog/trust-ladder.yaml`, a community entry for **trust-ladder** (Nous Research Hermes Agent Plugin Hackathon entry).

**Correct your Hermes agent once, and it stays corrected.** trust-ladder compiles each user correction ("never push straight to main") to the highest rung it can prove, following @poteto's fix ladder:

1. **Impossible**: a `pre_tool_call` guard blocks the repeat before it runs and tells the model why
2. **Checked**: `transform_tool_result` checks what a write puts into matching files
3. **Rule**: `pre_llm_call` re-injects guidance when no matcher can express it
4. **Human review**: matching calls go to Hermes's own approval prompt

A clear correction is compiled from the user's own words in `pre_llm_call` and installed before the model replies (`auto_learn`, on by default), so enforcement does not depend on the model calling `trust_ladder_learn`. A model-proposed guard is installed only if it matches the mistaken call and spares the corrected one. Every regex is profiled against ReDoS before install. `/verify` attaches a verifier command that gates "done", and `/trust` shows rules by rung with a catch ledger. The model can add rules, but only the user can disable or remove them. The ladder's state machines were model-checked with TLA+ (4 bugs found and fixed; specs in `docs/statechart`).

- Repo: https://github.com/merdoks/trust-ladder
- Pin: `fae4e9df58767e5e3832c8f65936b97868bc98fc` (version "0.1.2")
- requires_hermes: ">=0.22.7" (oldest release verified)

## Disclosure (rule 13)

- **Local only**: stores rules, tasks and a catch ledger (matched snippets, redacted, no full arguments) under `<HERMES_HOME>/plugin-data/trust-ladder/`
- No network calls, no telemetry, no credentials or env vars read
- Verifier commands run only through Hermes's own terminal tool, so normal approvals apply. Verifiers are checked against the user's guards before they run.
- It changes agent behaviour by design: blocks matching tool calls, appends check failures to tool results, injects rules each turn and adds a NOT VERIFIED footer to unverified "done" replies
- `auto_learn` installs a guard from the user's message only when the deterministic parser compiles it and it passes its self-test; questions and slash commands are skipped. It can be turned off in settings.
- Rules the model writes are still model-written; guards are best-effort pattern matches, not a sandbox

## How to Test

1. `hermes plugins validate --install-deps` at the pinned SHA: passed (0 failures, 0 cautions, security scan safe)
2. `python scripts/validate_plugin_catalog.py plugin-catalog/trust-ladder.yaml`: OK
3. Clean install from GitHub of 0.1.2 (b3996e2; the pin adds only guard dedupe), end to end: a correction installs a rung-1 guard and the repeat `git push origin main` is blocked in a new session. With a real model (gpt-oss-20b), the correction was installed at rung 1 from the user's words.
4. Plugin test suite: `cd tests && pytest` (96 passed)

## Type of Change

- [x] ✨ New feature (plugin catalog entry)

## [Draft] catalog: propose Email Steward community plugin
https://github.com/NousResearch/hermes-agent/pull/150057
State: open; created 2026-11-06T12:48:55Z

## Draft community catalog proposal: Email Steward

Adds **one catalog entry only**, pinned to [`kaosjammo/hermes-email-steward@a14b1c6ab76d23fb01e07a97b02990f6d4442273`](https://github.com/kaosjammo/hermes-email-steward/tree/a14b1c6ab76d23fb01e07a97b02990f6d4442273). Plugin implementation stays in its standalone repository; no Hermes core changes are proposed.

**Not ready to merge.** This preserves a parked work-in-progress for maintainer feedback. It is not a hackathon submission, release or assertion of live acceptance. Source publication is tracked at https://github.com/kaosjammo/hermes-email-steward/issues/1.

### What it does
Rules-first, single-owner Gmail triage; durable action/review obligations, briefs/reminders and owner-private native gateway commands, with shared native Desktop rule management. Four independently authorised host-owned Gmail OAuth slots. No Gmail send, reply-draft, delete or unsubscribe operation is implemented. Worker/background polling is off until explicit owner setup.

### Risks and data handling
- Reads authorised Gmail messages/attachments and uses Gmail modify scope for labels/Inbox changes.
- Bounded redacted mail content can go to the configured Hermes model/provider after explicit consent; configured host fallbacks may be attempted.
- Notifications use the selected private Hermes gateway; local SQLite stores sensitive summaries, rules and delivery state.
- Opt-in long-running profile-bound poller; bounded local parser/OCR subprocesses and private scratch for attachments.
- Hermes owns OAuth credentials and refresh. No direct credential-store reads, self-updater, telemetry or runtime core overrides are implemented.
- Private/undocumented Hermes adapter imports remain compatibility risks and produce validator warnings; documented extension seams need maintainer review.

### Actual checks and open gates
- Real validation/discovery against SDK commit `b63eb8bf5a7a09e33b6d63077ec4e7df7361780b`: **PASS**, including manifest/capabilities, scanner, no-core-override and Desktop SDK-surface checks. Private-core-import warnings retained, not waived.
- Aggregate Python test attempt: **TIMED OUT after240s**, with failures/skips visible before termination. Not a pass.
- Package attempt: **FAIL**, prepared setuptools83.0.0 is outside declared `>=80.9,<81`. No assertion/dependency requirements were weakened for publication.
- Latest presentation changes are unfinished/unapproved. The preceding UI review requested changes; no9.5 design acceptance is claimed.
- Live Gmail/OAuth, real private delivery, native Electron, mobile and hosted CI are unverified. Released-version minimum is not asserted from a main-branch SDK test; compatibility metadata is an open admission gate.
- Secret scanning: complete original local history plus public export/staged source scanned. One synthetic Mattermost channel-ID pattern (four historical occurrences, one current) was verified as test destination data, not a credential. Internal conversations, machine-specific records and private Git history are excluded from public source.

Please keep this draft unmerged while these gates remain open. No installation or live activation has been performed.


### Post-opening publication correction
An independent assessment identified internal planning/approval provenance in the initial public addendum. The current pinned source removes those identifiers and private review paths without changing executable code. The original public commit remains in history; historical erasure is not claimed. No credential was identified in that finding. The earlier catalog commit also retains its account-supplied commit identity; this follow-up uses GitHub noreply identity. This documentation-only correction does not resolve failing/incomplete product, compatibility or admission gates.


### Final observed CI state
Source-repository run https://github.com/kaosjammo/hermes-email-steward/actions/runs/42220324383 failed at scripts/test.sh on the earlier executable-identical source commit; native validation/package steps were skipped. The current source pin has no workflow run. Current-head upstream workflows report action_required with zero jobs, not a successful CI run. The independent documentation-only follow-up verified the current-tree provenance correction and accurate retained-history disclosure; merge readiness remains NOT_READY.


## feat(plugin-catalog): add household-tiers
https://github.com/NousResearch/hermes-agent/pull/149578
State: open; created 2026-11-05T15:52:18Z

## What does this PR do?

Adds a catalog entry for **household-tiers**, a Hermes plugin that lets one shared bot serve a household safely: owner / user / guest tiers enforced at the gateway (fail-closed), owner memory kept out of other people's prompts, a `family` preset (curfew with a parent alert, homework note), `/family` (alias `/familia`), and an audit log that never stores message text.

- Repo: https://github.com/chevlume/household-tiers (MIT, maintainer: chevlume, the repository owner)
- Pinned SHA: `1896b63f63c8f1615d974e30c3c731e895fb8d70` (`main` tip; version 0.1.1)
- This pin also checks `search_files` paths the way Hermes splits them (comma, or whitespace when there is no comma) and treats `target` as the search mode, not a path. A missing or blank path is checked as `.`.

## Related Issue

None. Submission for the Hermes Agent Plugin Hackathon.

## Type of Change

- [x] ✨ New feature (non-breaking: one new file under `plugin-catalog/`)

## Changes Made

- `plugin-catalog/household-tiers.yaml` (new). Declared capabilities: hooks `pre_tool_call`, `subagent_start`, `pre_gateway_dispatch`, `post_gateway_admission`; middleware `llm_request`; no tools; no env vars.

## Disclosure (catalog rule 13)

- The plugin does not send HTTP requests, telemetry, or self-updates, and it does not hold API keys.
- When a non-owner tier calls `web_extract`, `web_crawl`, or `browser_navigate` and private URLs are enabled, it resolves the hostname with the system resolver (`socket.getaddrinfo`) and blocks the call if any address is private, loopback, or link-local. It does not fetch the URL.
- It reads `config.yaml` through Hermes (`hermes_cli.config.read_raw_config`) to see `security.allow_private_urls` and the legacy `browser.allow_private_urls` flag.
- It writes two files under the active profile home from `get_hermes_home()`: `household-tiers.json` and `household-tiers-audit.jsonl`, and reads Hermes memory files to check what to redact.
- The parent alert is the gateway's `adapter.send` to the chat in `notify`. The plugin only asks for that send.
- Standard-library Python only. No self-updater.
- Built-in owner memory (`MEMORY.md`/`USER.md`) withheld from non-owner prompts; an external provider block joined after those boxes is removed; a provider block with no built-in box, and compaction's auxiliary summary, are not filtered.
- `bench/coexistence.py` clones two third-party git repositories. That script is optional and is not required to run the plugin. It is not in CI.

## How to Test

1. `hermes plugins validate . --install-deps` and `hermes plugins doctor . --ci` on a checkout of the pinned SHA.
2. `pytest` in the plugin repo: 108 passed on CI pin `ed1afb082eb3e46cf2edae9d8f68fb67b09ee4df` with uv CPython 3.11.18, 3.12.16, 3.13.18, and 3.14.10. Tag `v0.22.7` (`b200f5bc60e31588ba2cb60e288029c4a54ba5fa`) was not re-run. `hermes plugins validate` still warns on `tools.memory_tool_store.ENTRY_DELIMITER` (three sites in `__init__.py`).
3. Measured with tiktoken cl100k_base on toolset `hermes-telegram`: family kid-tier tool schema 9,301 → 477 tokens, 20 → 2 tools (`web_extract`, `web_search`). The default guest tier has an empty tool list. No model was called; this is serialized schemas, not a live inference saving.

Known limits are listed in `known_issues` in the YAML and in the README of the plugin repo. The demo video uses test IDs with a real Hermes agent run, not live Telegram.


## feat: +ae context primitive - Agentic Entrepreneurship as first-class tool
https://github.com/NousResearch/hermes-agent/pull/55872
State: open; created 2026-06-30T20:30:28Z

## +ae - Agentic Entrepreneurship Context Primitive

Adds `+ae` as a first-class context tool in Hermes Agent. Not a skill, not a plugin - a context layer that loads agentic entrepreneurship context and transforms the prompt from `>_` to `>_ae|`.

### Actions
- activate: loads context (language, stack, blueprints, NAICS, revenue, mission)
- deactivate: unloads context
- search: live NAICS classification API
- blueprints: organizational blueprints (#startabusiness, #daollc, etc.)
- revenue: real $133.65 revenue proof
- mission: #opensourceware #250

### Files
- tools/ae_context_tool.py (new, 275 lines)
- toolsets.py (+2 lines: ae_context in core, ae toolset)

### Verification
- 12 tool checks passed
- 20 toolset tests passed, 0 failed
- No regressions

### Proposal
https://myaelmendez.github.io/PRIMITIVE.md

Built for Hermes Agent Accelerated Business Hackathon (Nous x NVIDIA x Stripe).

$OS = economic infrastructure for agentic entrepreneurship.
#startabusiness +ae

## feat(plugin-catalog): add fledge plugin
https://github.com/NousResearch/hermes-agent/pull/149856
State: open; created 2026-11-06T04:25:41Z

## What does this PR do?

Adds one catalog entry, `plugin-catalog/fledge.yaml`, for **Fledge**: skills have to earn their wings. It's my entry for the Hermes Agent Plugin Hackathon. The plugin lives in my own repository, [12burb/hermes-fledge](https://github.com/12burb/hermes-fledge) ([pinned tree](https://github.com/12burb/hermes-fledge/tree/ac65b416d34381acba8642133cfa1d286e052028)). I am the repository owner (rule 5).

Hermes' self-improvement loop saves skills based on the agent's own judgment of whether a task went well. In [Kilo's read of 1,300+ r/openclaw comments](https://kilo.ai/openclaw/vs-hermes), the first two complaints listed about Hermes are that self-evaluation always passes ("It always thinks it did a good job", +107) and that self-improvement overwrites manual edits.

Fledge gates `skill_manage` on evidence from the run a skill was learned from, using only facts Hermes reports through hooks:
- tools still failing when the turn ended, judged per program, including the exit status a compound shell command prints for itself;
- failed or interrupted turns;
- the user's next message correcting the agent;
- `/undo`, `/retry` or a `/rollback` restore right after;
- denied approvals.

No model grades the model.

- **Save gate.** A skill learned from a bad run is held in Hermes' own skills pending queue, with the reasons. Users review it with the stock `/skills pending|diff|approve|reject`, or with `/fledge pending|diff|approve|reject`, which also works in messaging chats. A foreground save after errors goes through Hermes' approval prompt; unattended runs queue instead of waiting.
- **Probation.** New and rewritten skills are fledglings. Clean real runs graduate them and repeated bad runs ground them. A save from a run the user corrected right after is grounded at once. A grounded skill Hermes created on its own is archived (recoverable with `hermes curator restore`); skills the user asked for are only reported.
- **Hand-edit protection.** Skills the user edited by hand are fingerprinted. An autonomous rewrite or delete of one becomes a proposal in the same queue; an attended rewrite asks first (optionally with Hermes' content lock).

**Not a duplicate (rule 16).** skill-lineage records where skill content came from and never blocks; provenance-gate checks quoted user decisions; jev-curator governs curator consolidation; pending-queue-monitor is a read-only Desktop view of the queue; memory-rewind keeps version history. None of them judges a skill by how the run it came from actually went, or holds, probates and grounds it.

### Hermes surfaces it uses

- **Nine hooks:** `pre_llm_call`, `pre_tool_call`, `post_tool_call`, `on_session_end`, `on_session_finalize`, `on_session_reset`, `on_skill_lifecycle`, `pre_command`, `post_approval_response`.
- **`pre_tool_call`** acts on `skill_manage` only; every other tool returns at once. It returns `block` (held) or `approve` (Hermes' own prompt with a `rule_key`). It never grants anything (rule 12). `post_approval_response` is an observer, and Fledge ignores answers to its own `plugin_rule:fledge:*` prompts.
- **Commands and plumbing:** `register_command` (`/fledge`), `register_cli_command` (`hermes fledge`), `post_message` for chat notices, `get_config`/`set_config`, `plugins.plugin_storage.plugin_db`.
- **Footprint:** no tools, no middleware, no core patches (`no core override` passes).
- **Undocumented imports (the validate warnings), and why.** There is no public seam yet for:
  1. the skill write origin, needed to tell the background-review fork from a foreground turn (`tools.skill_provenance.get_current_write_origin`);
  2. staging a write into the review queue (`tools.write_approval.stage_write` / `list_pending` / `get_pending` / `skill_gist` and `hermes_cli.write_approval_commands.handle_pending_subcommand`);
  3. curator actions (`tools.skill_usage.archive_skill` / `set_locked` / `get_record`).

  All of these calls live in `bridge.py`, each guarded, so a moved function disables one feature (reported by `/fledge doctor`) and never breaks a turn. I checked all 17 against v0.23.0 and v0.22.7: same signatures. Happy to move to a public `ctx.skills` facade if you want one.

### Disclosure (rule 13)

- **Reads:** hook payloads (tool statuses and error text, and the first 280 characters of the next user message to spot a correction) and skill folders, to fingerprint them.
- **Writes:** its own SQLite under `plugin-data/fledge`. That holds skill names, fingerprints, session and turn ids, verdict reasons quoting the matched correction phrase and up to 80 characters of a tool error, and hold summaries with the skill's one-line description. No other message text and no skill bodies are stored.
- **Other writes:** held writes go into `pending/skills/`, and grounded agent-created skills are archived into `skills/.archive/`.
- **Never:** network calls, model calls, credentials, shell commands, background processes or telemetry. It never approves anything.
- **On its own errors, the gate lets the write through, with two deliberate exceptions.** A write already queued for review stays held, so it is never both saved and queued. An autonomous rewrite of a hand-edited skill is never let through.
- **Needs `plugins.isolation: in_process`** (the default) for full accuracy. `/fledge doctor` says so otherwise.

## Related Issue

None: a new catalog entry (Hermes Agent Plugin Hackathon).

## Type of Change

- [x] ✨ New feature (catalog entry only)

## Changes Made

- `plugin-catalog/fledge.yaml`: new entry pinned to `ac65b416d34381acba8642133cfa1d286e052028`, version `0.1.0`, `requires_hermes: ">=0.22.7"` (`tools.skill_usage.set_locked` first appears in 0.22.7; the same floor is in `plugin.yaml`).

## How to Test

1. `python scripts/validate_plugin_catalog.py plugin-catalog/fledge.yaml` gives `OK: 1 file(s) valid`.
2. `hermes plugins validate <clone at the pinned sha> --install-deps` gives `Validation passed.` The only warnings are the private imports listed above.
3. In a throwaway profile, run `hermes plugins install fledge --enable`, then `/fledge doctor` (all six checks ok).
4. With the files in [`demo/`](https://github.com/12burb/hermes-fledge/tree/ac65b416d34381acba8642133cfa1d286e052028/demo): `Run ./fetch_water.sh and turn what it returns into results.csv. The server is flaky, so retry once if it fails.`, then `/refine save the procedure for pulling water results as a skill`. Expect `🪶 Fledge: held skill '…'`, with the hold listed in `/skills pending` and `/fledge pending`.

**Tested.** 150 unit and flow tests pass on Python 3.14 and 3.11. `hermes plugins doctor --ci` and `hermes plugins validate` pass on Hermes **0.23.0** and **0.22.7** (Windows 11 ARM64). I also ran live sessions with a real model (glm-5.3) in throwaway HERMES_HOMEs.

- **On 0.23.0, installed with `hermes plugins install 12burb/hermes-fledge`:**
  - all three demo beats: a bad-run save held (origin `review`); a save grounded and archived after a real correction; an autonomous rewrite of a hand-edited skill turned into a proposal;
  - approving a hold put the skill on probation;
  - a foreground rewrite of a hand-edited skill raised Hermes' approval prompt;
  - `/undo` right after a turn held the save from it;
  - with Hermes' review queue made unwritable, the save landed on probation instead of being lost;
  - mistyped settings fall back to defaults and `/fledge doctor` names them.
- **On 0.22.7:**
  - all three demo beats;
  - watch mode;
  - 13 clean review writes with 0 holds;
  - fail-open under a locked database.

I found and fixed 21 bugs along the way, each with a test. Results are in [VALIDATION.md](https://github.com/12burb/hermes-fledge/blob/ac65b416d34381acba8642133cfa1d286e052028/VALIDATION.md), and the raw output is in [tests/smoke-2026-11-05.txt](https://github.com/12burb/hermes-fledge/blob/ac65b416d34381acba8642133cfa1d286e052028/tests/smoke-2026-11-05.txt).

## Checklist

### Code

- [x] I searched for existing PRs and catalog entries: no `fledge` entry or PR
- [x] My PR contains **only** the catalog entry (one file)
- [x] Commit message follows Conventional Commits (`feat(plugin-catalog): add fledge plugin`)
- [ ] I've run `pytest tests/ -q`: N/A, no Hermes code changed (the plugin's own 150 tests pass)
- [x] `hermes plugins validate --install-deps` passes at the pinned commit; declared hooks match registrations; `security scan: safe`; `no core override`; no binaries or `.pyc` in the tree
- [x] I've tested on my platform: Windows 11 ARM64, Hermes 0.23.0 and 0.22.7

### Documentation & Housekeeping

- [x] The plugin README at the pinned commit documents install, settings, commands, known limits and disclosures
- [x] Cross-platform: pure Python, stdlib only, no platform-specific code

## Screenshots / Logs

Raw session output: [tests/smoke-2026-11-05.txt](https://github.com/12burb/hermes-fledge/blob/ac65b416d34381acba8642133cfa1d286e052028/tests/smoke-2026-11-05.txt). Demo video (under 90 s, on X): will be linked here when posted.


## plugin-catalog: add hermes-standing
https://github.com/NousResearch/hermes-agent/pull/150366
State: open; created 2026-11-07T00:06:36Z

Adds `plugin-catalog/hermes-standing.yaml` (one file).

**Repo:** https://github.com/percyhendrux123-prog/hermes-standing, pinned at `5a0a374f5324f1a271de23940fcf0e0883084f92` (v0.1.0, MIT). Submitted by the repository owner.

## What it does

Earned trust for Hermes workers. A worker's record changes what needs the owner's approval, and a task cannot be marked done just because the worker says it is.

- **Levels per profile.** L0 read, L1 draft (local writes inside a workspace), L2 act (shell, sends, jobs, unknown tools inside existing Hermes gates), L3 trusted. Calls outside the level get Hermes's own `approve` directive. Spend and delete/move calls ask below L3.
- **Proof before done.** `kanban_complete` is blocked until this profile + task + session has a passing `standing_proof`. Standing runs the check itself: an owner-scoped file, an owner-allowlisted HTTP URL, or an exact owner-allowlisted read-only command. The model's word is never accepted.
- **Earning and losing.** Ten passes in a clean window raise the level by one (automatic ceiling L2). One failed check lowers it by one. A check that could not run is logged `unavailable` and changes nothing, so sandboxed workers are not punished for the host's limits.
- **Restarts never undo a demotion.** Seeds only create missing actors.
- **Visible.** `/standing`, `/standing log <profile>`, `/standing set <profile> <L0-L3>` (local owner only, no model-facing setter). Optional card line on the task after completion or demotion, e.g. `Standing: worker L2 · check passed (http example.com) · 3 passes this window / 0 fails all time.`
- **Shared ledger (opt-in).** One absolute `db_path` lets a governor profile and its workers use the same record on one machine.

## Hermes surfaces used

- Tool: `standing_proof`; no core tool overridden.
- Hooks: `pre_tool_call` (level gate, completion proof check, unwraps deferred `tool_call` batches), `post_tool_call` (card line after a real `{"ok": true}` completion), `pre_llm_call` (short guidance note), `on_session_finalize`, `on_session_reset` (clear in-memory receipts).
- Command: `/standing`.
- Kanban comments through `kanban_db.add_comment` / `kanban_db_connect.connect`, the same seam `kanban_tools` uses. No shell-out, no separate board store.
- Middleware: none. No monkeypatches.

## Disclosures (rule 13)

- **Approvals:** returns `approve` for out-of-level calls and `block` only around `kanban_complete` (no passing proof, or a malformed batch containing it). Never auto-approves. Under cron/unattended runs Hermes's approval policy (default deny) decides.
- **Network:** only a requested HTTP proof to an owner-allowlisted prefix. GET, status 200, no redirects, no ambient proxies, no credentials.
- **Subprocess:** only an exact owner-allowlisted argv, `shell=False`, no stdin, minimal environment, 2 MiB output cap, wall-clock timeout. POSIX only.
- **Reads:** approved proof targets only. Credential paths and Hermes home outside the workspace are refused before and after path resolution.
- **Writes:** `actors` and `events` to SQLite under `plugin-data/hermes-standing` (or the owner's `db_path`). Proof details are SHA-256 hashes; no message bodies, tool arguments, outputs or owner reason text. Kanban comments by author `standing` when `card_line` is on.
- **Model calls / telemetry / self-update:** none.
- **Not a sandbox:** ordinary hook errors fail open (logged by type, no directive); the completion proof check fails closed.

## Verification at the pinned SHA

- Fresh clone: `hermes plugins validate . --install-deps` -> **Validation passed** (Hermes v0.23.0)
- `hermes plugins doctor .` -> OK, 1 tool, 5 hooks
- `pytest -q -W error` on Python 3.14 -> 549 passed
- Live, on a real gateway with model-driven workers on dispatched Kanban tasks: completion without proof blocked; HTTP proof passed and completion went through with the card line; a false proof demoted the worker one level and `/standing` showed it; an unavailable file proof from a sandboxed worker was logged with no demotion.

Known limits are listed in the entry's `known_issues` and in the README's "Not in v0.1".

Entry for the Hermes Agent Plugin Hackathon.


## plugin-catalog: add hermes-sanctuary
https://github.com/NousResearch/hermes-agent/pull/149986
State: open; created 2026-11-06T10:35:51Z

## Hermes Sanctuary

**A living view of your Hermes Agent.** Five animated characters wake up when Hermes uses their tools, in two illustrated worlds: **Olympus** (default: Hermes, Hephaestus, Athena's owl, Mnemosyne, Cerberus) and **the Clearing**. It runs in Hermes Desktop (a pane under the conversation and a sidebar page) and in the web dashboard (a tab and a foldable strip above Chat), in English and French.

![Hermes Sanctuary demo](https://raw.githubusercontent.com/Med34000/hermes-sanctuary/a2cac2f2fec2cadc80b7ddd88252bec3016184ca/docs/demo.gif)

Submitted by the repository owner, for the Hermes Plugin Hackathon.

### What it does

- **Who is working:** each tool call wakes the character in charge (web and browser → the owl flies off, files, terminal and code → Hephaestus forges, reads, memory and past sessions → Mnemosyne, errors and approvals → Cerberus); Hermes calls out and hands out the work.
- **A guard that helps:** Cerberus barks, with a plain-words bubble, on tool and provider errors, **silent fallbacks** to a backup model, **loops** (same tool and same arguments 4 times in a turn), **heavy turns** (more than 200k input tokens: time for `/new`), a **daily budget** overrun and **permissions waiting** (shown only, never answered). Hermes Desktop also gets a native notification (at most one per kind every 2 minutes).
- **Background work is visible:** the coordinator shows where a turn comes from (Discord, Telegram, a scheduled task).
- **Today's journal:** turns, tools per companion, sources, alerts, tokens and estimated cost per model, hour by hour with the peak; **Share my day** (an image of the panorama with the day's numbers) and **Replay the day** (sped up in the panorama).
- **Worlds are data:** one `dashboard/app/themes/<id>/` folder per world (background, characters, positions, animations, texts).

### Hermes surfaces used

- 11 observer hooks: `pre_tool_call`, `post_tool_call`, `pre_llm_call`, `post_llm_call`, `on_session_end`, `post_api_request`, `api_request_error`, `pre_approval_request`, `post_approval_response`, `subagent_start`, `subagent_stop`. None blocks, changes or answers anything.
- Dashboard plugin: `dashboard/manifest.json` (tab and `chat:top` slot) and read-only routes in `dashboard/plugin_api.py` (`/state`, `/timeline`, `/themes`, `/theme`, `/frame`, `/asset`).
- Desktop plugin SDK only: `SandboxedFrame`, `ROUTES_AREA`, `SIDEBAR_NAV_AREA`, `ctx.onEvent` (`tool.start`, `message.start`, `message.complete`), `ctx.os.notify`.
- Storage: `plugins.plugin_storage.plugin_data_dir`.

### Disclosure

- Records only names, times and counts under `plugin-data/hermes-sanctuary/proc/` (one small JSON file per Hermes process, files older than 2 days removed): tool names, turn start and end times, platform and scheduled-task names, counters of errors, fallbacks, loops, heavy turns and approvals, the generic approval description Hermes gives, model names with token counts per hour, and one-letter event codes with their time for the replay. **Never** messages, replies, tool arguments, commands, results, error texts, file paths or ids.
- To spot loops, a hash of each tool call (name and arguments) is kept in memory for the current turn only, never written.
- No network calls of its own, no shell commands, no background process, no secrets or `.env` access, no telemetry, no self-updater. The daily budget is stored by Hermes Desktop or the browser.
- The panorama runs in a sandboxed frame fed by `postMessage`; it makes no request of its own.
- **Private import (rule 9 warning):** `dashboard/plugin_api.py` imports `agent.usage_pricing` (`CanonicalUsage`, `estimate_usage_cost`) to estimate the day's cost with Hermes's own pricing. I found no public seam for a cost estimate. If you prefer, I can drop the cost figure, or move to a public helper as soon as one exists.

### Validation

`hermes plugins validate` at the pinned commit (Hermes 0.22.5): **Validation passed**, all checks green (including security scan `safe`, `no core override` and `desktop surface`), one warning: the private import above. The hooks and Desktop SDK names it uses were also checked against current `main`.

### Screenshots

![Olympus](https://raw.githubusercontent.com/Med34000/hermes-sanctuary/a2cac2f2fec2cadc80b7ddd88252bec3016184ca/docs/panorama.jpg)
![Today's journal](https://raw.githubusercontent.com/Med34000/hermes-sanctuary/a2cac2f2fec2cadc80b7ddd88252bec3016184ca/docs/catalog/today-en.jpg)
![Hermes Desktop pane](https://raw.githubusercontent.com/Med34000/hermes-sanctuary/a2cac2f2fec2cadc80b7ddd88252bec3016184ca/docs/catalog/desktop-pane.jpg)
![The Clearing](https://raw.githubusercontent.com/Med34000/hermes-sanctuary/a2cac2f2fec2cadc80b7ddd88252bec3016184ca/docs/catalog/clearing-en.jpg)

Code: Apache 2.0 · art and characters: CC BY 4.0 · by Médéric Morin.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01PtRkwGZ4z2YBmx6ixhKnwV

## plugin-catalog: add prove-it
https://github.com/NousResearch/hermes-agent/pull/149765
State: open; created 2026-11-06T00:07:25Z

## What does this PR do?

Adds `plugin-catalog/prove-it.yaml`: **prove-it**, a plugin that checks an agent's completion claims ("pushed", "committed", "file written", "tests pass") against local, read-only probes and appends a short footer to the reply: ✓ verified, ✗ contradicted, ⚠ could not verify, ⏸ blocked on an approval. No model is involved in the check. `/proveit explain` shows the claim, the exact probe and the raw output.

Public surfaces only: the hooks `post_tool_call`, `transform_llm_output`, `pre_approval_request`, `post_approval_response`, and one slash command (`/proveit`). No tools, no middleware, no core overrides, no Python dependencies, no env vars.

Submitted by the repository owner (rule 5), as an entry to the Hermes Agent Plugin Hackathon. Demo (86 s): https://github.com/MikeGibbsOnyx/hermes-prove-it/releases/download/v0.1.0/prove-it-demo.mp4

## Disclosures

Also in the plugin's README.

- Runs read-only git commands (`rev-parse`, `merge-base`, `log`, `cat-file`) in the repository the agent worked in during the turn, with `fsmonitor` and `ext` protocols disabled and stdin closed. Stats absolute file paths named in the reply.
- No network. Never contacts a remote and never authenticates: a push is judged by comparing local HEAD with the remote-tracking ref.
- Makes no probe when the terminal backend is not local.
- Stores a bounded ledger in its own plugin data directory (`plugin-data/prove-it/data.db`): arguments and output only for terminal, file-write, code-execution and delegation calls, truncated, secrets pattern-redacted, deleted after 7 days. Approval pattern and description are stored, never the command text. The file is not encrypted.
- Each probe has a 2 s timeout and the footer a 4 s budget. A plugin error never withholds the reply in the default footer mode.
- Reads no credentials, writes nothing outside its data directory, no telemetry.
- The footer is part of the stored reply and is replayed on later turns (tens of tokens a turn).

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Changes Made

- `plugin-catalog/prove-it.yaml`: new entry pinned to `MikeGibbsOnyx/hermes-prove-it@f892dc005f49e54b889569edb6d3410b8abb7ef7`, `requires_hermes: ">=0.22.5"` (the same floor as `plugin.yaml`), `version: "0.1.0"`, `tier: community`, `category: tools`.

## How to Test

1. `python3 scripts/validate_plugin_catalog.py plugin-catalog/prove-it.yaml` → `OK: 1 file(s) valid`.
2. Clone `https://github.com/MikeGibbsOnyx/hermes-prove-it` at the pinned sha, then `hermes plugins validate --install-deps <clone>` → `Validation passed.` (`security scan — safe`, declared hooks match the registrations, no core override).
3. Enable the plugin and ask an agent to commit without pushing, then say it pushed: the reply gets `✗ not pushed` and the probe is shown by `/proveit explain`. The repo's own tests (`test_claims.py`, `test_verify.py`, `test_plugin.py`) pass.

## Checklist

### Code

- [x] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [x] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [x] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [x] My PR contains **only** changes related to this feature (one catalog file)
- [ ] I've run `pytest tests/ -q` (N/A: the PR adds one YAML file and changes no code)
- [ ] `python scripts/check` passes (N/A: no code change; the catalog validator above passes)
- [x] I've added tests for my changes (the plugin's own suites, in its repository)
- [x] I've tested on my platform: macOS

### Documentation & Housekeeping

- [x] I've updated relevant documentation (README and DESIGN in the plugin repository)
- [ ] `cli-config.yaml.example` (N/A)
- [ ] `CONTRIBUTING.md` or `AGENTS.md` (N/A)
- [x] I've considered cross-platform impact: probes use `git` and `os.stat` only, and skip when the terminal backend is not local
- [ ] Tool descriptions/schemas (N/A: no tools)

## Screenshots / Logs

Demo video linked above. Validation log excerpt: `✓ declared hooks — matches registrations`, `✓ security scan — safe`, `✓ no core override — no runtime rebinds of Hermes core`, `Validation passed.`

## catalog: add elcaro — runtime prompt-injection defense + tamper-evident flight recorder
https://github.com/NousResearch/hermes-agent/pull/149503
State: open; created 2026-11-05T13:36:32Z

Adds `plugin-catalog/elcaro.yaml` (community tier, `general` category), pinned to [`udirobert/elcaro@9f6a14c`](https://github.com/udirobert/elcaro/tree/9f6a14c160884a8c9fe3b6cfc7aef264a5fd0fba/hermes-plugin) (`9f6a14c160884a8c9fe3b6cfc7aef264a5fd0fba`, `subdir: hermes-plugin`, v1.0.0). Repo owner submission. Hackathon entry — demo video + form submitted separately.

## What it does

Inbound prompt-injection defense at the tool boundary, plus a forensic trail no prompt or skill could produce:

- **Scans every tool result inline** — `transform_tool_result` runs each result through a deterministic detector taxonomy (A–G: authority spoofing, delimiter escapes, task hijacking, obfuscation, hidden placement, conditional triggers, agent-to-agent steering), sub-10 ms, vendored local engine, no network. Quarantined content is replaced in place with a signed `[CONTENT QUARANTINED BY ELCARO]` notice — the injection never reaches the model.
- **Covers the args lane** — `pre_tool_call` scans `write_file`/`terminal`/`memory` args for smuggled payloads; `pre_llm_call` injects a once-per-turn quarantine summary so the agent doesn't retry or work around withheld content.
- **Kernel gate** — a quarantine taints the session (30 min TTL). While tainted, credential-path reads/writes and instruction-file writes are refused; network egress and outside-workspace writes escalate to the approval gate. `tool_call`, `execute_code`, and `process_manage` are evaluated as the action they really make; taint propagates into subagents via `subagent_start`. A credential read + egress channel in one shell step is refused even in a clean session. `taint_policy: enforce|monitor|off`.
- **Decoy honeypot** — `service-credentials.env` with an installation-unique `ELCARO-DECOY-*` marker sits in the plugin data dir; the marker inside any scanned result or args payload forces a deterministic 1.00 quarantine (`decoy_exfiltration`) — proof of exfiltration, zero false positives.
- **Incident response** — every quarantine gets a deterministic autopsy (canonical implementation in `core/`, vendored into the plugin; objective class, named targets, kill-chain stage, concealment — "wanted: exfil ~/.ssh → host" in the pane/log/explain); a rolling per-session window scores call *sequences*, blocking `untrusted_result→sensitive_read→egress` and post-quarantine memory/cron writes as named kill chains even when each call looks innocent. Detection that survives zero-day phrasing.
- **Flight recorder** — every verdict lands in a hash-chained (`prev_hash`→`entry_hash`) JSONL threat log, Ed25519-signed when a key is configured. Canary provenance edges (`type: "edge"`) record an injection propagating between scans; `/elcaro verify` recomputes the chain; `elcaro_explain` diffs verdicts across identical content.
- **Desktop pane + chip + API** — `desktop/plugin.js` (threat-log pane with chain-verified badge, honeypot status, propagation rows, signed-receipts drawer; status-bar quarantine chip) over `/api/plugins/elcaro/{verdicts,receipts,edges,stats,verify,decoy}`; `/elcaro` slash command (status / calibrate / verify / explain) + `hermes elcaro` CLI.

## Disclosures

- **Network:** none by default. The vendored engine runs fully local; `httpx` is only invoked if the user configures an optional `api_url` lane.
- **Credentials:** none required. Optional `ELCARO_API_KEY` (hosted lane) / `ELCARO_SIGNING_KEY` (verdict signing) via plugin config; the plugin never reads `.env`/`auth.json`.
- **Filesystem:** confined to `plugin_data_dir("elcaro")` — `threat-log.jsonl` (SHA-256 of content only, never raw text), `decoy-marker.txt`, `service-credentials.env` (honeypot bait, never read by the plugin).
- **Capabilities match reality:** declared tools/hooks in `plugin.yaml` match `register()` 1-for-1 (3 tools, 4 hooks); no middleware, no core overrides, desktop uses only the plugin SDK.

## Validation at the pinned SHA

```
hermes plugins doctor . --ci   → OK: 3 tool(s), 4 hook(s)
hermes plugins validate .      → all checks pass; security scan — caution (1: dump_all_env on the autopsy path-regex — a detector naming what it detects)
python3 -m pytest tests/test_hermes_plugin.py → 25/25
```

FP corpus (git log, package.json, READMEs, source, pytest output, security docs *about* injection): 0 false positives at balanced sensitivity.


## feat(plugin-catalog): add hermes-phone
https://github.com/NousResearch/hermes-agent/pull/149263
State: open; created 2026-11-05T04:37:55Z

What does this PR do?
Adds hermes-phone to the plugin catalog. It is one file, plugin-catalog/hermes-phone.yaml, pinned to [winchxyz/hermes-phone@b6ef97e](https://github.com/winchxyz/hermes-phone/commit/b6ef97e99b126aaedd0e480084ac00ec74000571) (v0.1.0). The repo owner (@winchxyz) is submitting it for the Hermes Agent Plugin Hackathon.

hermes-phone lets your Hermes agent place real phone calls for you. You ask in chat ("book a table for 2 at 8 pm"), check the brief card, and reply "call". The agent says it is an AI in its first sentence and handles the conversation. When the other side asks something it doesn't know, it puts them on hold and asks you in chat with a suggested answer. At the end you get one result message (outcome, what was agreed, confirmation number, duration, cost estimate) and the transcript.

Demo video: https://x.com/winchxyz/status/2118238897209802889

Capability disclosure
Network and money: places outbound PSTN calls through the user's own Twilio account, which costs money. A web-phone mode, where the callee is a browser page, needs no telephony account.
Audio to a third party: call audio streams to OpenAI Realtime.
Local server: runs a small FastAPI bridge (hermes phone serve) that must be reachable at the user's PUBLIC_BASE_URL. Twilio webhooks are signature-checked, and media streams use single-use hashed tokens. hermes plugins validate flags this as a caution (tunnel_service) because the manifest mentions ngrok/cloudflared tunnels.
Storage: call logs and text transcripts in plugin_db("hermes-phone") (SQLite). No audio recording.
Not present: no telemetry, no self-updater, no reads of .env/auth.json, no core monkeypatching. Secrets come from env only. register() does no network I/O.
Safety model (enforced in code, covered by tests)
Approval per call id, checked in three places: the pre_tool_call hook, the tool handler, and the bridge. Plain-text "call" approval works only from the human's own message in the chat that created the card.
Hard blocks: emergency and premium numbers are always blocked, and dialing is limited to an allowlist (fail-closed when unset).
Sensitive data: card, address and ID are shared only with per-call consent. CVV, passwords and OTPs are never shared.
Call limits: rate limits, quiet hours, a max-duration hangup, a kill switch (/phone hangup), and no automatic redials.
Related Issue
None (catalog submission).

Type of Change
 ✨ New feature (non-breaking change that adds functionality)
Changes Made
plugin-catalog/hermes-phone.yaml: new entry (category voice, tier community). capabilities match plugin.yaml and register() at the pinned SHA. The card image is pinned to the same commit.
How to Test
hermes plugins validate /path/to/hermes-phone: passes. The plugin's CI runs it against a pinned hermes-agent checkout.
hermes plugins doctor /path/to/hermes-phone --ci: passes, with 4 tools and 2 hooks registered and no network during register().
Fastest way to try it without telephony: set HERMES_PHONE_MODE=web, OPENAI_API_KEY, PUBLIC_BASE_URL and HERMES_PHONE_TEST_ALLOWLIST, ask the agent to call, reply "call", then open the link it posts and tap Answer.
Checklist
Code
 I've read the Contributing Guide and plugin-catalog/README.md admission rules
 My commit messages follow Conventional Commits
 I searched for existing PRs to make sure this isn't a duplicate
 My PR contains only changes related to this entry (one YAML file)
 pytest tests/ -q: N/A, no Hermes code changed. The plugin's own 443 tests pass in its CI (Python 3.11/3.12) along with a Docker build.
 I've tested on my platform: live PSTN calls via Twilio from Telegram, plus web-phone mode, deployed on the official Hermes Docker image.
Documentation & Housekeeping
 Documentation: the plugin README covers setup, the safety model, costs and legal notes. N/A for this repo.
 Other items: N/A

## chore(plugin-catalog): add hermes-watchdog
https://github.com/NousResearch/hermes-agent/pull/149270
State: open; created 2026-11-05T04:56:37Z

Adds **hermes-watchdog** — cron jobs that fix themselves.

```
hermes plugins install hermes-watchdog
```

### What it does

Hermes already records cron failures and de-duplicates the alert. Nothing acts on them, so a job that fails on a transient timeout keeps failing on it until a human re-runs it by hand. Watchdog closes the loop with bounded verbs and a real success criterion:

**match → act → verify → record**

- **match** — each open incident (state `detected`/`alerted`) is matched to a playbook. Built-ins cover the failure types core classifies: rerun once on `timeout`/`delivery`/`agent`; pause + escalate on `script`; escalate on `auth`/`config`/`unknown`. A user playbook wins at equal specificity.
- **act** — `rerun_job` (fires the job through Hermes's own `cronjob` tool, the same path `hermes cron run` uses), `pause_job`, `check` (a user-authored argv list, no shell, per-step timeout), `escalate`.
- **verify** — a repair counts as `repaired` **only** when Hermes's own record agrees: the incident left the open states, or the job's latest execution finished successfully after the attempt started. Steps that ran without clearing the failure are recorded as `failed`, never as success.
- **record** — every attempt lands in the plugin's own SQLite ledger with its playbook, steps and outcome, and each incident carries a hard daily attempt budget so a repair loop cannot become a second failure mode.

### Surfaces used (all public)

| Surface | Registration |
|---|---|
| Tools | `ctx.register_tool` × 3 — `watchdog_status`, `watchdog_repair` (with `dry_run`), `watchdog_runbooks` |
| Hook | `ctx.register_hook("on_session_end")` — when a *cron* turn fails, repair that job in place instead of waiting for the next tick |
| Slash command | `ctx.register_command("watchdog")` — `/watchdog`, `/watchdog repair` |
| Skill | `ctx.register_skill` — bundled `hermes-watchdog:watchdog` |
| Desktop | `ctx.register` — a `panes` pane (right zone) and a `statusBar.right` chip, data via `ctx.rest` → `/api/plugins/hermes-watchdog/{status,repair,runbooks}` |
| Storage | `plugin_data_dir` / `plugin_db` — ledger + user playbooks only |

No core rebinds, no dashboard tab (`tab.hidden`), no middleware, no env vars, no Python dependencies.

### Rule 13 disclosure

- **Reads** this profile's cron store read-only — `cron.jobs`, `cron.incidents`, `cron.executions` — through late imports, so a moved module degrades to `upstream.ok: false` in the pane and tools rather than crashing.
- **Runs** the failing job through Hermes's own `cronjob` tool, or pauses it. `check` steps execute the argv list a **user-authored** playbook declares (no shell, bounded timeout). Nothing else is executed.
- **Writes** only `plugin-data/hermes-watchdog/` (repair ledger, saved playbooks).
- **Never** edits a job's prompt or schedule, never messages on the user's behalf, never touches another plugin's or core's data.

### Catalog rule 9 note

The cron reads are the only private imports. I opened #149262 asking for a read-only cron-health seam (`ctx.cron.jobs/incidents/latest_execution` or an `on_cron_run_finished` observer hook) and will rewire to it the day it lands — I wrote the request as the consumer of this plugin. Every read is wrapped, and the tests cover the "upstream unavailable" path.

### Validation

- `hermes plugins validate . --install-deps` → **passed** (manifest, loadable entrypoints, capability probe, declared tools/hooks match registrations, no collisions, security scan, no core override, desktop surface inside the SDK; the only warnings are the cron imports above).
- `python -m unittest discover -s tests` → **14/14 pass**, incl. "unverified repair is a failure, not a success", "budget exhausted skips without running", "dry run touches nothing", "upstream failure is reported not hidden".
- `scripts/validate_plugin_catalog.py` → entry valid.
- Smoke-tested against a real profile: 81 jobs, 1 open incident; the dry-run cycle matched it to `builtin-escalate-unknown` and planned exactly one step.

Pinned to `33hodl/hermes-watchdog@f023261b7746dbaf080f6c17e322aba2fe990451`. A ~90s demo video follows with the hackathon submission; the Desktop pane is opt-in (Settings → Plugins), as for every unified-package Desktop half.


## feat(plugin-catalog): add canary-trap (prompt-injection tripwire)
https://github.com/NousResearch/hermes-agent/pull/149988
State: open; created 2026-11-06T10:41:21Z

Adds **canary-trap** (`plugin-catalog/canary-trap.yaml`), a community plugin pinned to [`Tarekkharsa/hermes-canary-trap@cbef2f9`](https://github.com/Tarekkharsa/hermes-canary-trap/tree/cbef2f98aee69cfacf59402e3d4fe98427d10b84) (`subdir: canary-trap`). Hackathon entry.

![canary-trap banner](https://raw.githubusercontent.com/Tarekkharsa/hermes-canary-trap/cbef2f98aee69cfacf59402e3d4fe98427d10b84/docs/banner.png)

## What it does

canary-trap catches prompt injection by the secret it tries to steal. Each turn the agent is shown a **decoy credential** (`HERMES_DEPLOY_KEY=hdk_live_…`) with a plain instruction never to send it anywhere. No real task needs it. So if it appears in a tool call, something the agent read is steering it to exfiltrate. When that happens:

1. **`pre_tool_call` → `block`** stops that call and tells the model why.
2. **`pre_tool_call` → `approve`** then applies to every later tool call in that session ("lockdown"), so the injection can't just try another route. `/canary reset` lifts it.
3. **`transform_llm_output`** puts an alert at the top of the reply, so the user sees it even if the model doesn't mention it.

Injections rarely ask for the secret verbatim, so the scan checks every string in the tool arguments, nested ones included. It catches the decoy plain, URL-encoded, base64 or base64url (alone or inside other text), hex, reversed, spaced or dashed out, or as any 16+ character fragment. 16 random characters are about 82 bits, so innocent text doesn't match by accident; the tests check that URLs, base64 blobs, hex and long text stay clean.

`/canary` shows status, lists incidents, resets the lockdown, rotates the decoy, or tests a piece of text (`/canary test <text>`).

## Hermes surfaces used

- `ctx.register_hook`: `pre_llm_call` (context injection), `pre_tool_call` (block / approve), `transform_llm_output` (alert prepended, no `hold_stream`)
- `ctx.register_command` (`/canary`)
- `ctx.get_config` for `enabled` and `lockdown`, and `ctx.state` for the decoy, incidents and locked sessions

No tools, middleware, env vars, credentials or private core APIs.

## Disclosure (rule 13)

- **Context:** it adds one paragraph of about 60 tokens to each turn's user message, containing the decoy and the "never send it" instruction. Plugin context goes into the user message, so the system prompt and its cache are untouched. Hermes may persist the API-bound message for replay. The decoy grants nothing.
- **Stored** in its own plugin state: the decoy, up to 200 incidents, and the ids of locked sessions. Each incident records the time, the tool name, how the decoy was hidden, the platform and the session id. **Never** tool arguments, page content or conversation text.
- **Approvals:** lockdown only *adds* prompts through Hermes' approval gate and never approves anything. That gate fails closed in non-interactive runs, follows `approvals.cron_mode` under cron, and auto-approves under YOLO. So under YOLO the lockdown is advisory, though the leaking call is still always blocked.
- **No** network calls, subprocesses, files outside its state, telemetry or background work.

## Checks at the pinned commit

- `hermes plugins validate canary-trap --install-deps`: all checks pass, **security scan: safe**, declared hooks match registrations (fresh clone at the pinned SHA).
- `scripts/validate_plugin_catalog.py`: OK. `scripts/scan_plugin_payloads.py`: clean.
- 36 unit tests; CI on Python 3.11, 3.12 and 3.13.
- On Hermes 0.22.6 in a throwaway profile:
  - A real agent turn got the decoy injected, and normal turns were unaffected.
  - Through Hermes' real `get_pre_tool_call_directive` and `invoke_hook`, the plugin loaded via `discover_plugins()` produced exactly the sequence below:
    1. A clean call passed.
    2. A `web_extract` whose URL carried the decoy base64'd was **blocked**.
    3. The next `read_file` in that session was escalated to **approve**.
    4. The reply came back with the alert prepended.

## Limits (also in the README)

It is a tripwire, not data-loss prevention: it proves an injection is steering the agent *when the injection goes for credentials*. Fragments under 16 characters and re-encodings it doesn't decode (ROT13, one character per call) are not caught. Strong models often refuse injections outright, and the decoy's own instruction helps them do it; canary-trap is the alarm for when that fails.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## catalog: add stripe-commerce — merchant-side Stripe with enforced restricted-key rails
https://github.com/NousResearch/hermes-agent/pull/149352
State: open; created 2026-11-05T07:47:23Z

## Plugin

**stripe-commerce** — the merchant side of Stripe for Hermes agents. Create products, prices, and hosted payment links; read subscriptions and portal configuration.

- **Source:** https://github.com/adroidian/stripe-commerce-hermes (plugin at repo root)
- **Pinned SHA:** 2ae7b4950a8cde4c755dda933e398298eff758f3 (main)
- **Owner submission:** I own the source repo.

## The rails (the point)

- **Restricted keys only** — `sk_` keys refused at registration AND on every call; only `rk_test_`/`rk_live_` accepted
- **No direct money-movement endpoints** — the transport allowlist contains no refund, charge, payment-intent, payout, customer, payment-method, or subscription-mutation endpoint (enumerated in the README)
- **Preview-bound human consent** for all six mutation tools. Offline preview stays the default. `dry_run:false` now requires the matching single-use `preview_id` and a fresh native human decision. The reference alone is never approval.
- **Exact request binding** covers the operation, origin/path, immutable form bytes, arguments, active profile/key/mode and native execution context. Changes, five-minute expiry, restart and reuse fail closed. Consent is checked again immediately before HTTP, including after TLS setup.
- Every POST sends a per-preview Stripe `Idempotency-Key`. An uncertain attempt consumes its preview; reconcile Stripe state before attempting a newly approved request.
- **Strict readback verification** — created objects are re-read and compared on commercially significant fields (recurrence, link price/quantity, redirect behavior, active state); mismatch or missing evidence returns `verified:false`, never a false positive
- Stdlib-only HTTPS to api.stripe.com; redirects/proxies disabled; 1 MiB response cap; Stripe keys redacted in tool output

## Compatibility and reviewer focus

Version 0.2.0 permits writes only through native **Telegram and Discord gateway approval prompts**. CLI/TUI, QQ and other channels keep reads and offline previews but refuse writes: the stock CLI can approve a collapsed request, and the shipped QQ card truncates at 300 characters. The plugin does not patch those renderers or treat an optional View choice as proof of exact consent.

It uses the existing internal `request_elicitation_consent` helper with `remember_key=None`, plus native session/platform/delegation/interrupt checks. Hermes does not currently expose this strict consent flow as a documented public plugin API. Validation passes with **one compatibility warning** for those imports; the same limitation is in the entry's `known_issues`, README and VALIDATION.md. Missing or incompatible support blocks writes. This PR does not change Hermes core or install the plugin in a live profile.

The native prompt includes the complete request. The plugin first checks the real native redactor and refuses any prompt field that would be masked or sanitized. Oversized requests are refused rather than approved with a truncated tail. Unattended/delegated callbacks, YOLO, cached grants and missing UI cannot authorize a write.

Reviewer focus: the native API seam and its catalog suitability; atomic one-attempt preview consumption; immutable bytes and final scope/expiry checks at the HTTP boundary.

## Validation

Receipts for source `2ae7b4950a8cde4c755dda933e398298eff758f3` (version 0.2.0):

- `python3 -B -m unittest discover -s tests -q`: **101 tests passed** on both Python 3.11.15 and the main checkout's Python 3.14 runtime, including 50 approval-binding regressions.
- `hermes plugins validate <plugin-dir> --install-deps --json` against main `ed1afb082eb3e46cf2edae9d8f68fb67b09ee4df`: **all checks pass; one compatibility warning**. Security scan is safe; capabilities match; no core overrides.
- `./demo/run_demo.sh`: **6 offline previews, 19 rejected execution attempts, zero HTTP calls and zero real sockets**.
- 11 additional checks against the real native Telegram/Discord queue, resolver, redactor and final card-send methods used simulated delivery/human decisions and mocked Stripe HTTP. They covered complete rendered requests, refused CLI/QQ/unverified surfaces, platform/key/profile changes, denial/replay, immutable caller inputs and cron/YOLO behavior. A slow-TLS expiry probe also rejected before HTTP.
- `python3 -m compileall -q .` and `git diff --check`: pass.
- Live read/create/hosted-checkout/archive video evidence belongs to the earlier 0.1.0 baseline. **No live Stripe request or billing change was made to validate 0.2.0.**

Second submission for the Hermes Plugin Hackathon (first: clack, PR #149183). Demo video + form to follow ahead of the Nov 11 deadline.

## feat(plugin-catalog): add hermes-ghost-call
https://github.com/NousResearch/hermes-agent/pull/150554
State: open; created 2026-11-07T07:25:02Z

## What does this PR do?

Adds Ghost Call to the plugin catalog. It is one file, `plugin-catalog/hermes-ghost-call.yaml`, pinned to [winchxyz/hermes-ghost-call@b670ff8](https://github.com/winchxyz/hermes-ghost-call/commit/b670ff8a930a02aff8afe2c39994bcf4645654ac) (v0.1.0). The repo owner (@winchxyz) is submitting it for the Hermes Agent Plugin Hackathon.

Ghost Call is a real-time AI assistant on your own calls. You stay on the line and talk; Hermes listens, streams one-line hints to your page and to the chat ("they want a 2-year contract → say you want no contract, mention FastNet $55"), and on one tap plays a hint in your earpiece. It knows your private target and walk-away from the goal you gave it, and never puts them in a hint. When you hang up it posts a summary: what was agreed, the amount, what is still open and a draft confirmation SMS.

Three ways to listen: two one-time browser links (web mode, no telephony account), a real phone line through the user's own Twilio account, or room mode, where one page listens to any call on speaker.

Demo video (84 s): poster and player in the [README](https://github.com/winchxyz/hermes-ghost-call#readme); X post: https://x.com/winchxyz/status/2118968460801941593

## Hermes surfaces used

- 7 tools: `ghost_start`, `ghost_status`, `ghost_hint_latest`, `ghost_speak`, `ghost_intervene`, `ghost_hangup`, `ghost_summary`
- `/ghost` slash command (`start [room|+number] <goal>`, `status`, `speak`, `intervene allow|deny`, `hangup`, `transcript`, `log`, `check`)
- `pre_tool_call` hook: blocks `ghost_intervene` unless the human allowed it for that session
- a skill (`skills/ghost-call/SKILL.md`)
- CLI: `hermes ghost serve` (the bridge) and `hermes ghost doctor`
- plugin data (SQLite) via the plugin data dir; secrets via `agent.secret_scope.get_secret`

## Capability disclosure

- **Audio to a third party:** call audio streams to OpenAI (realtime transcription); hint text, summary and earpiece TTS also use OpenAI. No other hosts, no telemetry.
- **Network and money:** Twilio mode places calls through the user's own Twilio account (costs money) and dials only numbers on an allowlist (fail-closed when unset). Web and room modes need no telephony account.
- **Local server:** a small FastAPI bridge (`hermes ghost serve`) must be reachable at the user's `PUBLIC_BASE_URL`. Page and media links use single-use hashed tokens; Twilio webhooks are signature-checked; web routes are rate-limited on the client address (`X-Forwarded-For` only with an explicit trusted-proxy setting).
- **Storage:** sessions, hints, summaries and (optional, `store_transcripts`) text transcripts in plugin data (SQLite). No audio recording.
- **Speaking on the call:** Hermes does not speak on the line. The one exception is Intervene, which the `pre_tool_call` hook blocks unless the human allowed it; its first words say it is an AI assistant acting for the user.
- **Not present:** no self-updater, no reads of `.env` / `auth.json` or any credential store, no core monkeypatching, no network I/O in `register()`. Secrets are read only through `agent.secret_scope.get_secret` and fail closed on a scope error.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Changes Made

`plugin-catalog/hermes-ghost-call.yaml`: new entry (category `voice`, tier `community`). Capabilities match `plugin.yaml` and `register()` at the pinned SHA; the banner and screenshots are pinned to the same commit.

## How to Test

- `hermes plugins validate /path/to/hermes-ghost-call --install-deps`: passes. The plugin's CI runs it against a pinned hermes-agent checkout, together with `hermes plugins doctor . --ci` (7 tools and 1 hook registered).
- Fastest way to try it: set `OPENAI_API_KEY` and `PUBLIC_BASE_URL=http://localhost:8766`, run `hermes ghost serve`, then in chat `/ghost start get a lower price on my internet, target $60`. Open the **You** link with headphones and the **Them** link in a second tab (or send it to a friend) and talk.

## Checklist

- [x] I've read the Contributing Guide and plugin-catalog/README.md admission rules
- [x] My commit messages follow Conventional Commits
- [x] I searched for existing PRs to make sure this isn't a duplicate
- [x] My PR contains only changes related to this entry (one YAML file)
- [x] `pytest tests/ -q`: N/A, no Hermes code changed. The plugin's own 220 tests and ruff pass in its CI.
- [x] Tested: web mode and room mode end to end with live OpenAI (`scripts/e2e_call.py`: two voices through the real bridge, all checks pass). Not yet run live: Twilio mode (covered by mocked tests) and a room-mode call with a real phone on speaker.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Add community entry: cron-consolidator (Hermes Agent Plugin Hackathon entry)
https://github.com/NousResearch/hermes-agent/pull/149427
State: closed; created 2026-11-05T10:43:47Z

Add community entry: `cron-consolidator` (Hermes Agent Plugin Hackathon entry)

## What it is
`cron-consolidator` reads a profile's cron data and prints a read-only plan for tidying a crowded cron list. It flags:

- **jobs that are really one job**: near-duplicate prompts (`difflib`, 85 % or more after numbers and whitespace are normalised), jobs sharing the same skills and delivery target, jobs running the same script;
- **clock-time jobs that fire in the same minute** (days of week, month and day of month are taken into account; pollers such as `*/30` are left out so they do not chain unrelated jobs into one group);
- **jobs on a failure streak** and **deliveries accepted but never confirmed** (`last_delivery_unverified`);
- **schedules it cannot parse**, listed instead of guessed.

The token figure comes from `usage_audit.jsonl` and is a ceiling on prompt-side tokens (a merged prompt is longer, output tokens are not counted); a candidate with no usage data says so and claims no saving. It is deterministic (no model call) and **never applies anything**: there is no `--apply`.

Repo: https://github.com/Moodtuner997/hermes-cron-consolidator (version 0.1.0, MIT, Python standard library only, pinned to
`52acc397a7eb4ccf809e03afbc021a29f440b28b`).

## Hermes surfaces used
`ctx.register_command("cron-consolidator")` and `ctx.register_cli_command("cron-consolidator")`. No hooks, no tools, no middleware, no core overrides. One guarded import with a fallback: `hermes_constants.get_hermes_home`.

## Disclosure (rule 13)
- **Network:** none.
- **Reads outside the plugin's own data:** `cron/jobs.json` (including prompts), `cron/usage_audit.jsonl` and `cron/executions.db` of the chosen profile (the database is opened read-only); with `--profile`, another profile's cron folder under the same Hermes root.
- **Writes:** none. A test checks that the profile is unchanged after a run.
- **What the report contains:** job names, ids, schedules, skills, delivery targets and the first 160 characters of a failing job's last error. Prompt text is compared, never printed.
- **Shell commands, background processes, stored credentials:** none.
- **Approvals (rule 12):** not involved; the plugin touches no tool call.
- **Telemetry:** none.

## How it differs from existing entries
`fleet-policy` reports cost per cron, `hermes-cron` diagnoses a job's health, `custodian` repairs failing jobs and `cron-bulletin` is an inbox. `cron-consolidator` answers a different question: which jobs should become one. It plans consolidation; it does not price, diagnose or repair. They compose.

## Validation
- `hermes plugins validate` passes on a fresh clone at the pinned SHA, on Hermes 0.22.7, on Linux (arm64) and native Windows 11.
- `scripts/validate_plugin_catalog.py` passes on this entry.
- 29 unit tests (`python -m pytest tests -q`, no Hermes needed), including known-good and known-bad cron overlap cases and a check that a run leaves the profile untouched.
- `hermes cron-consolidator report` runs through the real CLI on Linux and Windows against a synthetic profile (`tests/make_demo_profile.py`).
- Tried on a snapshot of a real deployment (three profiles, 42 enabled jobs, mostly scripts): no near-duplicate prompt, one genuine merge (the same script scheduled twice) and two same-minute groups. A list of mostly distinct jobs gets a short plan; the plugin does not invent savings. The first run on that data produced misleading same-minute groups (pollers chaining unrelated jobs), which is why pollers are now excluded.
- `platforms` lists what was tested; macOS is untested. There is no UI; example output is in the README.

Happy to adjust anything.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## feat(security): add opt-in CaMeL guard plugin with reproducible benchmarks
https://github.com/NousResearch/hermes-agent/pull/3987
State: open; created 2026-03-30T16:06:05Z

CaMeL Guard uses native plugin hooks to gate sensitive tool calls after external tool data on capabilities derived only from the current user request. It preserves Hermes's native executor, tool-result framing and approvals; mode and trace persistence both default off.

This branch is refreshed onto current Hermes. The November review requests are addressed: the committed benchmark result JSON and machine-specific contributor mapping are removed. The repository contains reproducible offline/live harnesses; generated outputs are ignored.

Production fixes include current renamed tool mappings (`process_manage`, `cronjob_manage`, `desktop_project`, `desktop_preview`, `todo_list`), conservative gating of unknown tools, operator-controlled exact tool mappings/read-only exceptions, and `/camel` status/mode configuration. Read-only exceptions do not make their output trusted.

The hackathon plugin package is published separately as [nativ3ai/hermes-camel-guard-plugin](https://github.com/nativ3ai/hermes-camel-guard-plugin), release [v1.1.1](https://github.com/nativ3ai/hermes-camel-guard-plugin/releases/tag/v1.1.1), exact commit [`4cbfca3`](https://github.com/nativ3ai/hermes-camel-guard-plugin/tree/4cbfca3a5f1d46f5d152280cccc496d0df14d097), install subdirectory `plugin`. This is intentionally distinct from `nativ3ai/hermes-agent-camel`, the older full Hermes integration. Catalog admission is proposed separately in #149147. The four installable plugin files at the release pin are byte-identical to this PR branch.

Validation on Hermes `ed1afb082eb3e46cf2edae9d8f68fb67b09ee4df`:
- 1,956 plugin/executor regression tests passed; 4 skipped; no failures.
- Plugin validation passed without warnings; scanner safe, no core overrides.
- 18/18 offline controls used real scratch-file dispatch with a deterministic classifier fixture.
- Fresh live `gpt-6.1-sol` via Hermes-managed Codex: 6/6 classifier controls, 12/12 agent controls, 3/3 authorized native executor recorder dispatches; no benchmark exceptions.
- The live model requested no sensitive tool in any adversarial run, including off. No marginal live guard-block claim is made.
- Canonical lint: all 14 checks passed.

Risk and behavior disclosure: classification sends the current user request to the operator-configured model and consumes quota. The runtime reads only Hermes plugin settings and optional bounded profile-scoped trace metadata; it reads no credential files, stores no credentials, spawns no shell/background process, and makes no independent network calls. Optional trace metadata excludes user text, arguments, results and classifier rationale. No telemetry or self-updater.

This is a coarse capability guard, not full CaMeL isolation, argument-level authorization, an answer-content filter or a sandbox. A classifier failure blocks sensitive effects in enforce; monitor remains observational. The explicit Codex-adoption option is benchmark-only tooling outside the installed plugin directory and delegates operator-approved sign-in adoption to Hermes in disposable homes.

Reproduce with the scripts and commands in `website/docs/developer-guide/camel-guard-live-benchmark.md`. Live calls require `--live`; model refusals and guard policy outcomes are reported separately.

## feat(plugin-catalog): add dirtside plugin
https://github.com/NousResearch/hermes-agent/pull/149883
State: open; created 2026-11-06T05:58:08Z

## What does this PR do?

Adds one catalog entry, `plugin-catalog/dirtside.yaml`, for **Dirtside**: remote brain, local hands. It is my entry for the Hermes Agent Plugin Hackathon. The plugin lives in my own repository, [the-ai-entrepreneur-ai-hub/hermes-dirtside](https://github.com/the-ai-entrepreneur-ai-hub/hermes-dirtside) ([pinned tree](https://github.com/the-ai-entrepreneur-ai-hub/hermes-dirtside/tree/e27d457b309a1febe23448cebd07d8f493bb2832)). I am the repository owner (rule 5).

Hermes runs on a server so it can answer from Telegram, Discord, the dashboard or the Desktop app at any hour. That server is not where the user's code, Xcode, GPU or files are. Dirtside is a terminal environment provider: each conversation chooses where the terminal and file tools run, the server or a paired machine, with `/dirtside use macbook`. The model keeps thinking on the server; the commands run on the device the user named. This is the "remote brain, local hands" shape discussed in #18715.

How it works, in one paragraph. A small foreground agent on the device (`hermes dirtside serve`) long-polls the gateway over outbound HTTPS. The script travels back inside the poll response, the device verifies the gateway's signature, checks its local policy, runs the script in a process group as the device user and streams signed output back in parts of up to 2 MiB, with small output leaving within 200 ms. Nothing listens on the device. Every message is Ed25519-signed, timestamped within 300 s and replay-guarded on both ends. Pairing pins the device's public key; `/dirtside revoke` cancels its live requests at once. Core renders the requested timeout; a device policy can stop work earlier; a request lost to a gateway restart or a dropped device reports exit 255 with its reason, never a fabricated timeout, and the device stops the orphaned work at its next poll.

Hermes runs chat turns and slash commands in worker processes, so the process that receives verified device traffic (the gateway, or the dashboard process) is the one relay owner. Every other process reaches it over loopback through the plugin's own local routes with a loopback-only secret and a process-identity check, and a worker never believes it owns a device.

What was measured at the pinned commit (details and reproduction in the README): on loopback, added `pwd` latency over core's local backend is 4.84 ms at p50 and 7.82 ms at p95 in the owner process, and 32.75 ms at p50 and 40.58 ms at p95 from a worker; output streams at 16.08 MB/s; a cancel returns in 9.73 ms. An eight-row reliability matrix (device loses network, gateway restarts, device restarts, concurrent commands, clock skew, output flood, long poll, user interrupt) passes 8 of 8 over signed HTTP on loopback with a real gateway app and a real device process. The same eight rows pass 8 of 8 across two physical machines over the public internet at this commit, the gateway behind an HTTPS tunnel and the device on another machine's WSL2 Linux in another city; the rig probes the link first (0.236 MB/s and a 0.425 s round trip through the tunnel path on that run) and sizes the 64 MiB flood row's budget from it, and that row took 471.5 s. Inside a real Hermes install (v0.23.0), fifteen live scenarios pass from the CLI and from gateway sessions with two paired devices, one of them through a public tunnel: device selection, file tools, shell state across turns, a 1 MB output, a timeout, the deny list, core's dangerous-command block, fail-closed with the device agent stopped, re-pairing, a revoke during a live command and a gateway restart during a live command.

### Hermes surfaces it uses

- `ctx.register_terminal_environment_provider` (the backend, selected with `terminal.backend: dirtside`), `ctx.register_dashboard_auth_provider` (per-device bearer plus signature on the plugin's own device routes), `hermes_cli.dashboard_auth.token_auth.register_token_route` for those routes and for the plugin's loopback-only local routes, `ctx.register_command` (`/dirtside`), `ctx.register_cli_command` (`hermes dirtside pair | serve | status | install-service`), `ctx.register_system_prompt_section` (the chosen device's facts), `plugins.plugin_storage.plugin_data_dir` (one SQLite database, the relay key, the local secret and the owner record).
- `dashboard/plugin_api.py` mounts the routes under `/api/plugins/dirtside/`; `desktop/plugin.js` adds a pane and a status-bar chip through the Desktop SDK only.
- **Footprint:** no model tools, no hooks, no middleware, no core patches (`no core override` passes). One Python dependency, `pynacl>=1.5,<2` (rule 10).
- **Validator warnings, and why.** `hermes plugins validate` passes. It warns about undocumented imports in two places. Three are in the plugin itself, each with a reason: `hermes_cli.dashboard_auth.token_auth.register_token_route` is the one way to exempt the device routes and the local routes from the dashboard session gate so a device bearer or the local secret can reach them (`DashboardAuthProvider` and `TokenPrincipal` come from the public `hermes_cli.dashboard_auth`); `tools.environments.base.EnvironmentConnectionError` is the exception core's terminal tool catches and renders as an unreachable environment, so an offline or revoked device fails closed with core's own message; `tools.environments.local.LocalEnvironment` is core's own local backend, which the `server` target delegates to instead of reimplementing. The remaining warnings all point at `tools/core_runtime.py` and `tools/core_rig.py`, the test rig that drives the real core's loader, terminal and file tools and dashboard inside the test suite and the reliability matrix; nothing in `tools/` is loaded at runtime. Happy to move any of the three to a public seam when one exists. The isolation note is accurate: the plugin is written for the default in-process isolation.

### Disclosure (rule 13)

- **Shell commands:** this is the point of the plugin. Scripts that Hermes' terminal and file tools produce run on the chosen device as the device user, with no filesystem sandbox. Hermes' approval path is untouched: the plugin approves nothing and bypasses nothing (rule 12). On the device, a policy refuses dangerous patterns before anything runs (`sudo`, wiping the root, formatting disks, raw disk writes, shutdown and reboot, stopping its own service, fork bombs, piping a download into a shell) and caps each command at 900 s, 64 MiB of output and 4 in parallel. The user edits that policy in the device file.
- **Network:** the device talks to the user's own gateway URL and to nothing else. HTTPS is required for any URL that is not loopback. The gateway makes no outbound calls for this plugin; its worker processes talk to the owner process over loopback only. No telemetry.
- **Reads:** the plugin's own data directory on the gateway; the device file and activity log on the device. It never reads `.env`, `auth.json` or any other credential store (rule 11).
- **Writes:** on the gateway, one SQLite database under `plugin_data_dir("dirtside")` with token hashes, device metadata, per-conversation choices and a request log (a 120-character command preview plus outcome metadata; a 4,096-byte live output tail is held in memory only while a request runs), plus the relay signing key, the loopback-only local secret and the owner record; the key, secret and owner record are written with mode 0600, and the database relies on the privacy of the Hermes home. On the device, `<hermes home>/dirtside/device.json` (mode 0600: gateway URL, device id, bearer token, Ed25519 private key, the gateway's public key, the policy) and a 0600 activity log of request ids and outcomes.
- **Background processes:** `hermes dirtside serve` is a foreground command. `hermes dirtside install-service` optionally writes a per-user launchd agent or systemd user unit that restarts it after a crash and leaves it stopped after a revoke; `--dry-run` prints the unit and `--remove` undoes it.
- **Stored credentials:** the device token and private key in the device file above; the gateway stores token hashes, its own relay signing key and the local secret, all under the plugin's data directory.
- **Fails cleanly unattended:** cron conversations default to the server; a chosen or configured default device that is missing, offline or revoked makes the tool fail closed with the reason, never a silent fallback to the server.

### Checks at the pinned commit

- `hermes plugins validate --install-deps` on a fresh clone: validation passed. `hermes plugins install <repository url> --ref <this commit>` into an isolated Hermes home, then `plugins enable`, `config set terminal.backend dirtside`, `plugins doctor --ci` and `hermes dirtside --help`: all as expected.
- 619 tests green on `ubuntu-latest` and `macos-latest` against core `84a0301415edd6d1385207ec96e4d7f2b6c1fcd9` on every push, with the plugin loaded by core's own loader and driven through core's own terminal, file and dashboard entry points, including cross-process tests where the terminal tool runs outside the owner process and tests against real listeners bound to all interfaces.
- Not yet verified: the pane inside the running Desktop app, and service behaviour across login and reboot. Both are stated in the README.

## Related Issue

Relates to #18715 (a terminal environment provider that runs the tools on the user's own machine). A new catalog entry for the Hermes Agent Plugin Hackathon.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Changes Made

- `plugin-catalog/dirtside.yaml`

## How to Test

1. `hermes plugins install dirtside` on a Hermes 0.22.7 or newer gateway, then `hermes plugins enable dirtside` and `hermes config set terminal.backend dirtside`; restart the gateway (a gateway that Hermes auto-started for the CLI keeps its loaded plugin code until it exits, so restart that too). A gateway reached through a tunnel or reverse proxy also needs `hermes config set dashboard.public_url https://<public hostname>`.
2. Install the same package on a device, mint a code with `/dirtside pair <name>` in chat, run the printed `hermes dirtside pair ...` line on the device, then `hermes dirtside serve`.
3. `/dirtside use <name>` in a conversation; the next terminal command runs on the device. `/dirtside use server` moves it back; `/dirtside revoke <name>` cuts the device off.


## catalog: bump hermes-pr-studio to 0.4.1 (batch review, findings tool)
https://github.com/NousResearch/hermes-agent/pull/149373
State: open; created 2026-11-05T08:45:22Z

## What does this PR do?

SHA-bump for the existing `hermes-pr-studio` entry (0.3.0 `b9ba1c6` to 0.4.1 `42bd80d2205709cc87925a7f21718885093d9616`). Submitted for the Hermes Agent Plugin Hackathon. Owner submission (rule 5): I own `Murali-lns/hermes-pr-studio`.

New in 0.4 (0.4.1 adds one fix found in the live test: long Hermes reviews now scroll inside the card so the tabs and review bar stay visible):
- **Batch review.** Tick several PRs in the list, then *Review in this chat* (one message covering each ticked PR) or *Review in N new chats* (model picker, one chat per PR, up to 5, started in parallel and not opened).
- **Findings come back to the panel.** The review prompt asks the agent to call a new tool, `pr_studio_submit_findings`. Findings appear as a *Hermes review* card on the PR and as a badge on the list row (`3 findings (1 high)`, `risky`, `reviewed: clean`, `outdated`). Each finding can be added to the user's pending review (labelled `[Hermes review, severity]`) or dismissed. Nothing reaches GitHub until the user presses Comment.
- **Safer review submit.** Comment is the primary button; Approve is a quiet button with a plain-words confirmation, and the backend refuses `APPROVE` unless the request carries an explicit confirmation flag (unit-tested: a comment can never emit Approve).

## Hermes surfaces used

- Desktop plugin SDK (`desktop/plugin.js`): workspace tile, status-bar chip, palette command, `host.request` (`session.create`, `prompt.submit`), `host.composer`, React Query.
- Dashboard router (`dashboard/plugin_api.py`), served through the plugin host.
- `register(ctx)`: one `ctx.register_tool` (`pr_studio_submit_findings`, toolset `pr_studio`), declared in `plugin.yaml` `provides_tools` and in `capabilities.provides_tools` of this entry (rule 6).
- `plugins.plugin_storage.plugin_data_dir` (documented) for the findings file.

No hooks, no middleware, no env vars, no core overrides, no self-updater. The Restart-service button calls `host.restartGateway()` and fetches or replaces no files (rule 3).

## Rule 13 disclosures

- Shell: logged-in `gh` CLI (argument lists, no shell, 30-40 s timeouts) and `git remote get-url origin`.
- Agent tool: writes validated findings (repo, PR number, relative file path, line, text; length caps) to `plugin-data/hermes-pr-studio/findings.json` only. No network, no GitHub access, no subprocess.
- Prompts: *Send to Hermes*, *Review in this chat* and *Review in new chats* submit prompts with PR titles, branch names and comment text (written by other GitHub users) to the user's chat immediately. The prompt tells the agent to treat that text as untrusted data. New chats spend tokens on the model the user picks.
- Background: watched PRs polled every 60 s, Hermes findings every 5 s, only while Desktop is open.
- No credentials read or stored, no telemetry.

## How to Test

1. `git clone https://github.com/Murali-lns/hermes-pr-studio && cd hermes-pr-studio && git checkout 42bd80d2205709cc87925a7f21718885093d9616`
2. `hermes plugins validate . --install-deps` (passes locally, including `declared tools` and `security scan: safe`).
3. `python3 -m unittest discover -s tests` (32 tests).
4. `hermes plugins install Murali-lns/hermes-pr-studio --enable`, restart Hermes, enable the Desktop half, tick PRs, press *Review in new chats*.

## Checks run

- Validate on a fresh clone at the pinned SHA: pass.
- 32 unit tests: pass (tool input validation, replace-on-resubmit, dismiss, API routes, Approve needs confirmation, Comment never sends Approve).
- Headless render of the real `plugin.js` against the real `plugin_api.py` and the real tool, with synthetic PRs and a stubbed Desktop host (`tests/headless`): zero page errors; the prompt, three parallel `session.create` + `prompt.submit` calls, badges, findings card and accept-as-draft flow all checked. Screenshots in the entry come from this harness, so the theme is approximate.
- Hermes's own registry loads and dispatches the tool.

## Live test (real Hermes Desktop, v0.22.7+338)

Ran on a public demo repo (`Murali-lns/shop-demo`, 3 small PRs). Ticking three PRs and choosing *Review in 3 new chats* with deepseek-v4.1-flash started three chats; each agent called `pr_studio_submit_findings` (about 90 s). Badges appeared on the rows (`risky · 7 findings`, `risky · 4 findings`, `2 findings`), the Hermes review card rendered, and *Add as comment* put the finding into the pending review. Nothing was posted to GitHub. This found one layout bug (a long review pushed the tabs and review bar off screen), fixed in 0.4.1.

## Gaps

- GitHub rejects line comments outside the diff; a bad line from the model shows an error toast on submit.
- Findings are only as good as the chosen model; they are drafts for the user to accept or dismiss.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Checklist

- [x] Only `plugin-catalog/hermes-pr-studio.yaml` changes
- [x] `sha` is a full 40-character commit, `version` quoted and bumped in the same PR
- [x] Screenshots pinned to the same commit


## [DRAFT] Add gogogoogle plugin to the catalog
https://github.com/NousResearch/hermes-agent/pull/149174
State: open; created 2026-11-05T00:44:40Z

> **DRAFT - not yet submitted for judging.** This entry is still being changed and is not the final Plugin Hackathon submission. It will be marked final here when ready.

## Add `gogogoogle` plugin to the catalog

Pinned to `fe82443` (version 0.3.3). Update notes for the earlier review are in the comments below.

**What it does.** Delegates bulk work (mass edits, file generation, broad reading, research, a second-opinion review) to Google's Antigravity `agy` CLI as a worker agent, then runs a fresh `agy` conversation to verify the result against the real files and the git diff. Hermes keeps its own model; only the bulk step leaves it. It is not a model provider (the existing `antigravity-*` entries make `agy` the model Hermes runs on).

**Surfaces used.** `ctx.register_tool` for `antigravity_delegate`, `antigravity_job`, `antigravity_stats`, and one `pre_tool_call` hook that asks for Hermes approval before each `antigravity_delegate` call. No middleware, core overrides, dependencies or required env vars. Standard library only.

**How you use it.** Name it in a request: "Use gogogoogle to review the changes in this repo". Hermes shows the role, workdir and task (with its length and SHA-256 prefix) and waits for Allow or Deny. Each call gets a fresh approval key, so "session" or "always" on one call does not preapprove the next.

**Features.** Roles `do` / `research` / `review`; a verifier chain that moves to the next model when one is gone, out of quota or unauthorised; background jobs with polling; resume of timed-out runs; a git fingerprint before and after so a read-only role that edits files is reported and forced to `VERIFY FAIL`; job-file writes and reads retry on a Windows file-lock error (0.3.3); the reply handed back to Hermes is cut at 32,000 characters; stats with failure reasons and tokens handled by agy; plugin settings `worker_model`, `verifier_models` and `blocked_roots`.

**Disclosures (rule 13).**
- Runs shell commands: only the `do` role launches `agy` with `--dangerously-skip-permissions`, after the Hermes approval, so agy can edit and delete files in the working folder (git is the undo). `research`, `review` and the verifier omit that flag and pass session-only rules that deny writes and shell commands. These rules are not an OS sandbox. Because read-only roles get no permission for agy's MCP or browser tools, a task that needs those must use the `do` role.
- Sends data to a third party: the task text, files agy reads and up to 6,000 characters of git diff go to Google through agy.
- Reads outside its own data: agy can read files outside the working folder as the OS user. The plugin refuses a drive root, the home folder and any path inside or containing a `blocked_roots` entry (plugin setting, or the `GOGOGOOGLE_BLOCKED_ROOTS` environment variable as a fallback).
- Subprocess environment: agy and git get only OS path and locale variables, no inherited provider keys.
- Runs read-only `git diff`, `git status`, `git ls-files` in the working folder.
- Writes `runs.jsonl` (no task text) and `jobs/<id>.json` under the plugin data directory. After a restart a running job's status is unknown.
- No stored credentials, no telemetry, no self-update. The plugin never reads agy's credential files.

**Validation.** At the pinned SHA: 50 unit tests pass and `hermes plugins validate` passes. Re-tested on 0.3.3 on Windows 11 (Hermes 0.23.0, agy 1.5.2, lead model `gemini-3.8-flash`), one run each: in a fresh Hermes desktop chat, "Use gogogoogle to review ..." called `antigravity_delegate`; Deny returned `BLOCKED` and started no agy run; Allow once ran a `review` delegation that ended `OK`. A background `research` job through the installed copy also ended `OK` (WORKER then VERIFYING; the verifier header read `VERIFY INCOMPLETE` with a PASS verdict in its text). The read-only deny-rule check (agy's attempts to write and run shell were blocked and the tree stayed clean) was run on 0.3.1 with agy 1.5.1 and has not been repeated on 0.3.3. 0.3.3 itself only adds a retry around the job-file replace and read on a Windows lock error.

**Limits.** The approval can be bypassed by `--yolo`, `approvals.mode: off` or an approve-mode cron or unattended policy. Another plugin's hook can change arguments after the approval text is built. The deny rules do not stop reads outside the working folder. The git checks miss ignored files and edits inside already-untracked files and do not revert changes. Developed and tested on one machine and one agy version; macOS and Linux are untested.

Submitted by the repository owner. Demo video and form to follow.



## feat(creative): comic-series — AI webtoon/manga pipeline skill
https://github.com/NousResearch/hermes-agent/pull/19342
State: open; created 2026-05-03T19:48:35Z

## comic-series skill

Full webtoon/manga/manhwa production pipeline orchestrated by Hermes, powered by Kimi K2.5 + fal.ai Flux.

### What it does

One `/comic-series` invocation takes the user from a single sentence premise to a fully published multi-chapter webtoon:

1. **Premise → 3 variants** — Kimi K2.5 proposes 3 distinct story framings, user picks one
2. **World bible + character bible** — canon documents generated and saved to workspace
3. **Character art** — fal.ai Flux + Manhwa LoRA renders portrait / full_body / action references per character
4. **Chapter loop** — for each chapter: beat proposal → 10-panel spec → render (5 panels concurrently) → multimodal continuity check
5. **Multimodal continuity** — Kimi K2.5 sees previous chapter panels as images, flags visual inconsistencies across chapters
6. **Publish** — static mobile-first webtoon viewer deployed to Cloudflare Pages (primary) + Surge.sh (fallback), with Twitter/OG card

### Key features

- **Always proposes, never assumes** — 3 alternatives at every creative decision point
- **Self-improving style** — `chapter feedback` patches `style-card.md` with version history; next chapter adapts
- **Plot twist engine** — optional Kimi K2-Thinking call for long-horizon narrative pivots
- **`comic auto`** — non-interactive one-shot mode for full-series generation from a single command

### Requirements

- `OPENROUTER_API_KEY` or `KIMI_API_KEY`
- `FAL_KEY`
- `SURGE_LOGIN` + `SURGE_TOKEN` (for publish)
- `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` (optional, for CF Pages)

Full setup: https://github.com/eren-karakus0/hermes-comic

### Demo

Live webtoon generated with this skill: https://hermes-comic-timekeeper.surge.sh
Demo video + X post: https://x.com/Knkchn0/status/2051023382284562716

Built for the Nous × Kimi Creative Hackathon (2026-05-03).

## plugin-catalog: add CaMeL Guard 1.1.1
https://github.com/NousResearch/hermes-agent/pull/149147
State: closed; created 2026-11-04T23:10:56Z

CaMeL Guard restricts sensitive tool calls after external tool output to capability categories derived only from the isolated current user request. This adds one catalog entry for the plugin developed in #3987.

Pinned package: dedicated [nativ3ai/hermes-camel-guard-plugin@4cbfca3](https://github.com/nativ3ai/hermes-camel-guard-plugin/tree/4cbfca3a5f1d46f5d152280cccc496d0df14d097), release [v1.1.1](https://github.com/nativ3ai/hermes-camel-guard-plugin/releases/tag/v1.1.1), subdirectory `plugin`, Hermes >=0.22.7. This plugin package is intentionally separate from `nativ3ai/hermes-agent-camel`, which is the older full Hermes integration. The four installable plugin files at this pin are byte-identical to #3987.

The runtime uses five public hooks and a `/camel` operator command. It adds no model tools, core overrides, desktop UI, updater, or background service. Mode and trace persistence default off. Unknown tools require conservative external-system authority; audited exact-name read-only exceptions still leave their output outside the authorization lane.

Disclosures:
- Sends only the current user request to the operator-configured model through `ctx.llm` when classification is needed; consumes that provider's quota.
- Reads operator settings through Hermes; optional bounded metadata-only traces use profile-scoped plugin state.
- Runtime reads no external credential stores, stores no credentials, runs no shell commands, and makes no independent network calls. Authentication belongs to Hermes. No telemetry.
- The explicit Codex-adoption option exists only in repository benchmark tooling outside the installed `plugin` directory; it delegates operator-approved adoption to Hermes in disposable homes.
- Authorization is coarse by capability, not exact arguments. It does not implement full CaMeL data-flow isolation or prevent contamination of the final answer. Enforce blocks sensitive actions on classifier failure.

Validation against Hermes `ed1afb082eb3e46cf2edae9d8f68fb67b09ee4df`:
- `hermes plugins validate plugin --install-deps`: passed, no warnings, scanner safe.
- Focused integration suite and 18 offline native-dispatch controls passed.
- Broader plugin/executor regression: 1,956 passed, 4 skipped, no failures.
- Fresh live `gpt-6.1-sol` via Hermes-managed Codex: 6/6 classifier controls and 12/12 agent controls passed, including 3/3 authorized recorder dispatches. No adversarial run requested a sensitive tool even in off mode; these are not claimed as marginal live guard blocks.
- Canonical upstream lint gate: all 14 checks passed.
- Catalog structure validation passed at the v1.1.1 pin.

The reproducible harnesses generate ignored local/CI artifacts; no benchmark results are committed.

Intended Hermes Plugin Hackathon entry. The demo and final entry form are pending; this PR alone is not the completed hackathon submission.

## docs(catalog): add neural-mesh — bi-temporal memory with point-in-time recall
https://github.com/NousResearch/hermes-agent/pull/149750
State: open; created 2026-11-05T23:15:55Z

## What does this PR do?

Adds `plugin-catalog/neural-mesh.yaml` — **one file, metadata only, no code** — for [neural-mesh](https://github.com/D0xedDevi0/hermes-neural-mesh), a Hermes `MemoryProvider` that keeps memory *history* instead of only current state.

The problem it solves: a flat vector store has no notion of *when* a fact was true, so a correction overwrites the old value and it becomes unanswerable. Three things follow from keeping a validity window instead:

1. **Point-in-time recall.** `mesh_asof` answers *"what was true on 2026-03-01?"*, not only *"what is true now?"*
2. **Supersession, not overwrite.** A correction closes its predecessor's window at the new fact's `valid_from`. The old value stops being *current* while remaining *answerable*.
3. **Measured automatic injection.** Context is injected only above a calibrated `0.25` score floor; `mesh_recall` deliberately reaches wider at `0.05`.

Storage is a local SQLite file inside the Hermes profile — no server, no keys, no network.

## Related Issue

No issue; this follows the catalog entry merged in #149166 (basekit).

## Type of Change

Catalog entry only — no Hermes code, tests, skills, or config keys change, so none of the boxes below apply. It is metadata consumed by the plugin catalog.

## Changes Made

- `plugin-catalog/neural-mesh.yaml` (+33) — new entry: repo, pinned `sha`, disclosure-bearing description, 4 immutable screenshot URLs, `readme: true`, `known_issues`, and `capabilities` verified against the pin.

## How to Test

**~30 seconds, no Hermes install, no keys, no network:**

```bash
git clone https://github.com/D0xedDevi0/hermes-neural-mesh && cd hermes-neural-mesh
python3 -m unittest discover -s tests     # 23 tests, offline
python3 scripts/trust_check.py            # compiled-artifact + credential-store scan
```

Then confirm the entry itself: `python scripts/validate_plugin_catalog.py plugin-catalog/neural-mesh.yaml` → `OK: 1 file(s) valid` (warnings are only for the display keys `image`/`screenshots`/`readme`/`known_issues`/`version`, which this validator does not know).

## Catalog Compliance

- **No API keys, no network, no credential files.** `requires_env: []`. The trust check inspects file headers/magic bytes for compiled artifacts and greps shipped source for credential-store paths (`auth.json`, `.env`, keychains, browser profiles) — clean.
- **Rule 17 — no compiled binary.** The upstream Rust resonance extension (`rust_mesh.so`) is deliberately **not vendored**; retrieval runs the pure-Python path and `mesh_stats` reports `resonance_backend: python`. Documented in `PROVENANCE.md`.
- **Capabilities match the pinned commit** (verified at the pin): tools `mesh_remember`, `mesh_recall`, `mesh_asof`, `mesh_stats`; hooks `on_session_end`, `on_pre_compress`, `on_memory_write`; no middleware, no env requirements.

## Evidence

- **Demo, 85s** — [docs/demo.mp4](https://github.com/D0xedDevi0/hermes-neural-mesh/blob/main/docs/demo.mp4). Every frame is rendered from captured command output; `docs/evidence/demo_capture.txt` is the untrimmed ledger. Includes a real agent session storing a fact and then a **cold process with its session history deleted** answering from the store.
- **Temporal ablation** — `scripts/evidence_temporal.py` → `docs/evidence/temporal-accuracy.json`. Same engine, same 15 fact families, same shipped tool surface, two arms: **temporal 15/15 current and 15/15 point-in-time; flat append-only 1/15 on both.**
- **Calibration** — `scripts/calibrate_floor.py` reproduces the floor table in the README.

## Disclosures

- **The store is unencrypted SQLite** in the profile directory, so it is readable by anyone with filesystem access to that profile and is not a place for credentials. Stated in the entry's `known_issues`, the README, and the tool descriptions.
- **It is a `MemoryProvider`**, selected with `memory.provider: neural-mesh`; only one provider is active at a time. This PR changes no default and no existing config.
- **Superseding an id that does not exist** is reported in the tool reply rather than failing the write, so a bad correction is stored as a new fact and *says so* instead of silently leaving two contradictory values current. Listed in `known_issues`.
- **Pinned-commit maturity:** the pinned commit is same-day. This is an owner submission of a repository built for the Nous hackathon, and I would rather flag it than have it turn up in review. If you would prefer to hold it for the two-week maturity window, say so and I will re-pin rather than push.

## Checklist

### Code

- [x] I've read the Contributing Guide
- [x] My commit messages follow Conventional Commits — `docs(catalog): add neural-mesh`
- [x] I searched for existing PRs and this isn't a duplicate (basekit was #149166)
- [x] My PR contains **only** changes related to this feature — exactly one file, after rebasing off the basekit branch so no unrelated commits ride along
- [ ] `pytest tests/ -q` / `python scripts/check` — **N/A**: this PR touches no Hermes code; those suites cover the host repo. The linked plugin's own 23-test suite runs offline (command above).
- [x] I've added tests for my changes — in the plugin repo, not here (23 tests, CI matrix on 3.10/3.11/3.12 plus a trust gate)
- [x] I've tested on my platform: Ubuntu 24.04 (Linux 6.12), Python 3.12 and the Hermes-embedded interpreter

### Documentation & Housekeeping

- [x] Documentation updated — the linked repo carries a README, `docs/evidence/`, and the demo
- [x] `cli-config.yaml.example` — N/A, no config keys added by this PR
- [x] `CONTRIBUTING.md` / `AGENTS.md` — N/A, no architecture or workflow change
- [x] Cross-platform impact considered — pure stdlib Python, no shelling out, no OS-specific paths
- [x] Tool descriptions/schemas updated if behavior changed — N/A here; in the linked repo the four tool descriptions carry the same disclosures

## Screenshots / Logs

Four frames taken straight from the 85s demo (same provenance — nothing asserted in a still that the ledger does not back):

| | |
|---|---|
| ![the difference](https://raw.githubusercontent.com/D0xedDevi0/hermes-neural-mesh/84f2170809b61798f4e4ca98c58e8912ea6d9786/docs/screenshots/the-difference.png) | ![cold recall](https://raw.githubusercontent.com/D0xedDevi0/hermes-neural-mesh/84f2170809b61798f4e4ca98c58e8912ea6d9786/docs/screenshots/cold-recall.png) |
| append-only vs bi-temporal | cold recall after session history was deleted |
| ![point in time](https://raw.githubusercontent.com/D0xedDevi0/hermes-neural-mesh/84f2170809b61798f4e4ca98c58e8912ea6d9786/docs/screenshots/point-in-time.png) | ![measured](https://raw.githubusercontent.com/D0xedDevi0/hermes-neural-mesh/84f2170809b61798f4e4ca98c58e8912ea6d9786/docs/screenshots/measured.png) |
| the dated question: 11 now vs 3 in March | the measured ablation |


## feat(plugin-catalog): add hermes-ark plugin
https://github.com/NousResearch/hermes-agent/pull/149640
State: open; created 2026-11-05T18:14:44Z

## What does this PR do?

Adds **Hermes Ark** to the plugin catalog (`plugin-catalog/hermes-ark.yaml`, one file), pinned to
[`f2d5378724134dd62010df4def48ad2e0dad761e`](https://github.com/medomohamed22/hermes-ark/commit/f2d5378724134dd62010df4def48ad2e0dad761e).
I am the owner of https://github.com/medomohamed22/hermes-ark.

Hermes Ark is a time machine for Hermes itself: encrypted, versioned backups of memory, SOUL, skills, config,
cron, sessions and every profile, with item-level restore.

- **Automatic:** a snapshot right before every `memory` / `skill_manage` write, plus periodic full snapshots after sessions.
- **Health guard:** when memory or skills suddenly shrink, a note goes into the tool result, so the agent tells the user at once, along with the exact `/ark restore …` command that undoes it.
- **Restore:** everything, one kind (memory / skills / config / cron), one skill, or one profile. A preview comes first and a safety snapshot is taken before every restore. Two-phase: all blobs are verified before the first write.
- **Off-site:** any S3-compatible storage (AWS, R2, B2, MinIO…) or a folder; `hermes ark pull` restores onto a new machine; `hermes ark verify` proves every snapshot restores.
- **Self-defense:** a prompt-injected agent cannot prune, delete, reconfigure or switch off Ark. This was found by testing with a real model: a hidden comment in a file made the agent run `hermes config set …auto_snapshots false`.
- **Surfaces used:** `tool_execution` middleware, an `on_session_end` hook, the `ark_checkpoint` tool, `ctx.register_cli_command` (`hermes ark …`), `ctx.register_command` (`/ark …`), and a Desktop page (`desktop/plugin.js`, plugin SDK only) with a `dashboard/plugin_api.py` router.

Built for the Hermes Agent Plugin Hackathon.

## Related Issue

None — new catalog entry.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Changes Made

- `plugin-catalog/hermes-ark.yaml` — new entry (`tier: community`, `category: tools`, `requires_hermes: ">=0.21.6"`, also declared in `plugin.yaml`).

## Disclosure (rule 13)

- **Reads:**
  - The Hermes home and its profiles, to back them up.
  - Credential files (`.env`, `auth.json`, vault, pairing, browser logins, Webapp session token) are skipped; they are read and backed up only if the user enables `include_secrets`, which also requires an encrypted repository.
  - Ark's own secrets (`ARK_PASSPHRASE`, `ARK_S3_ACCESS_KEY_ID`, `ARK_S3_SECRET_ACCESS_KEY`) come only through `agent.secret_scope.get_secret` and are never stored or logged. Ark never opens `.env` for them; a test asserts this.
- **Writes:**
  - Snapshots go to the repository folder (default `$HERMES_HOME/plugin-data/hermes-ark/repo`) and Ark's data folder.
  - The Hermes home is written only on a restore the user confirms (terminal, `/ark … yes`, or the Desktop dialog). The agent has no restore tool.
  - After an agent tool call changed Ark itself, Ark writes back only the previous values of: its own settings and enabled state (through `ctx.set_config` / `hermes_cli.config.save_config`), its repository key file, and its own plugin files. Never secrets.
- **Middleware:**
  - `tool_execution` runs on every tool call. It snapshots before memory/skill writes and adds a note when the guard fires.
  - It **refuses** calls that would delete, rewrite or reconfigure Ark's backups or settings, or disable Ark, returning a "BLOCKED by Hermes Ark" result. It refuses again a call that already damaged Ark.
  - Read-only Ark commands and all other calls run unchanged. `allow_agent_admin: true` lifts this. Hermes' own approvals are never bypassed.
- **Background threads:** periodic snapshot / retention / auto-push after sessions; a watchdog in the agent process that checks Ark every 10 s (small file reads).
- **Subprocess:** one, only after something disabled Ark while the agent was active: `python -m hermes_cli.main plugins enable hermes-ark`, with a fixed argv and no shell. It runs so the running gateway loads Ark again; a direct config write is the fallback.
- **Network:** only to the user-configured S3 endpoint, over HTTPS (plain http only for localhost). Redirects are refused (they would carry the signature), responses are size-capped, and XML with a DTD is refused.
- **Not included:** no telemetry, no self-updater, no Python dependencies beyond Hermes' own `cryptography`, no binaries.

## How to Test

1. `hermes plugins install medomohamed22/hermes-ark --enable` (or by catalog name once merged), then restart the gateway.
2. `hermes config set ARK_PASSPHRASE '<a passphrase>'`, then `hermes ark init` and `hermes ark snap first`.
3. In a chat, ask the agent to remove most memory entries. The tool result carries the health-guard note, and the agent relays the `/ark restore memory <id> yes` command. Run it, start a new chat, and the memory is back.
4. `hermes ark status` · `hermes ark list` · `hermes ark verify`, or open the **Ark** page in Hermes Desktop.

Validation at the pinned commit (fresh clone): `hermes plugins validate <clone> --install-deps` → **Validation passed**.
Every check is ✓, including `security scan — safe`, `no core override` and `desktop surface`, with no private-import warnings.
`python scripts/validate_plugin_catalog.py plugin-catalog/` → OK.

## Checklist

### Code

- [x] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [x] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [x] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [x] My PR contains **only** changes related to this feature (one catalog file)
- [x] The plugin's own suite passes at the pinned commit: 173 passed, 1 skipped. The skipped test needs a live S3 server; it was run against one during development. The suite includes adversarial and fuzz tests (path traversal, ciphertext bit-flips, hostile S3 servers, prompt-injection attacks on Ark itself).
- [x] I've tested on my platform: Linux (Hermes from source), end-to-end with a real model (gpt-oss-20b) driving the agent

### Documentation & Housekeeping

- [x] README with a disclosure section and SECURITY.md (threat model, limits) in the plugin repo
- [x] Cross-platform: Linux tested; Windows/macOS paths and locks handled in code (msvcrt/fcntl), not yet run on those systems

## Screenshots / Logs

![Ark page in Hermes Desktop](https://raw.githubusercontent.com/medomohamed22/hermes-ark/f2d5378724134dd62010df4def48ad2e0dad761e/docs/media/desktop-dark.png)
![The agent relays Ark's health guard](https://raw.githubusercontent.com/medomohamed22/hermes-ark/f2d5378724134dd62010df4def48ad2e0dad761e/docs/media/chat-guard.png)
![Restore preview](https://raw.githubusercontent.com/medomohamed22/hermes-ark/f2d5378724134dd62010df4def48ad2e0dad761e/docs/media/restore-preview.png)


## Add money-magnet to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149186
State: closed; created 2026-11-05T01:01:23Z

Catalog entry for **money-magnet**, submitted for the Hermes Agent Plugin Hackathon.

**What it does:** a finance tracker for Hermes Agent: `finance_add` / `finance_list` record and review income and expenses, `finance_budget` tracks a monthly budget, `finance_portfolio` values crypto holdings against live prices, and `finance_arbitrage` scans for price gaps between exchanges. Ships the `/money` command. Data lives in local JSON under `$HERMES_HOME/money-magnet/`.

**Disclosure (catalog rule 13):** the portfolio and arbitrage tools query the public CoinGecko and Binance price APIs (no account, no API key; only coin symbols are sent). The tracker tools work fully offline. Declared capabilities match registrations exactly.

**Verification at the pinned commit:**
- `hermes plugins validate`: passed
- `hermes plugins doctor`: OK, 5 tools registered under the real runtime contracts
- Live dispatch test through the Hermes tool registry contract: expense and income recorded, list totals and budget remainder computed correctly, `/money status` output verified

## Feature: Semantic Search for Session History (Hybrid BM25 + Vector)
https://github.com/NousResearch/hermes-agent/issues/44075
State: open; created 2026-06-11T07:07:11Z

## Problem

`session_search` currently relies exclusively on FTS5 keyword matching. This means the agent can only find past conversations when the search query contains the exact words used in that conversation.

Example failures:
- "what did we do about smart home" → misses the conversation about Bardi/Tuya bulbs
- "that time we automated HR" → misses the Talenta clock-in/out sessions
- "the hackathon brainstorm" → misses the Mamikos ideas discussion

This significantly limits the agent's ability to recall useful context across sessions.

## Current State

- `messages_fts` (FTS5, default tokenizer) — word-level keyword matching
- `messages_fts_trigram` (FTS5, trigram tokenizer) — substring/wildcard matching
- Both are pure keyword search — no semantic understanding
- No embedding/vector index on session content
- Existing issues (#675, #10355) address embedding infrastructure and memory — but none target **session search** specifically

## Proposed Solution

Add hybrid search to `session_search` — combine BM25 (existing FTS5) with vector similarity:

```
Query → Embedding → Vector Search (sqlite-vec)
                  → Tokenize → BM25 Search (FTS5, existing)
                  → Weighted Merge → Ranked Results
```

### Implementation Path

1. **`sqlite-vec` extension** — add as optional dependency, provides vector search inside the existing SQLite DB (no new DB needed)
2. **Embed on insert** — alongside the existing FTS5 trigger, generate embeddings for new messages using configurable provider
3. **Backfill** — one-time script to embed existing messages
4. **Hybrid merge** — combine BM25 + vector scores with configurable weights
5. **Provider config** — reuse existing provider resolution (OpenAI, local fastembed, etc.)

### Why sqlite-vec

- Same DB, no new infrastructure
- Works with existing `state.db` migration system
- OpenClaw uses the same approach successfully
- Zero-config for users who don't need semantic search (graceful fallback to FTS5-only)

## Comparison with OpenClaw

OpenClaw handles this with:
- `sqlite-vec` for vector similarity inside SQLite
- Hybrid BM25 + vector merge with weighted scoring
- `experimental.sessionMemory: true` — exports session transcripts to a searchable QMD collection
- Pluggable embedding providers

The key difference: OpenClaw treats session transcripts as **first-class searchable documents**. Hermes treats them as raw text with keyword indexing only.

## Config Sketch

```yaml
session_search:
  semantic: true                    # enable hybrid search
  embedding_provider: auto          # reuse provider resolution
  embedding_model: text-embedding-3-small
  hybrid_weight_vector: 0.7        # vector similarity weight
  hybrid_weight_bm25: 0.3          # keyword match weight
```

When `semantic: false` or no embedding provider is configured, falls back to current FTS5-only behavior.

## Related Issues

- #675 — Configurable Embedding Infrastructure (foundational)
- #10355 — Living Memory System (covers memory, not session search)
- #489 — Semantic Codebase Search (code-specific)
- #844 — Knowledgebase RAG (documents, not sessions)

This issue is specifically about making `session_search` / `session_recall` semantically aware — a distinct scope from the above.

## Add constraint-vault to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149269
State: closed; created 2026-11-05T04:55:39Z

Adds **constraint-vault** (v0.1.0) to the community plugin catalog.

- Repo: https://github.com/jusst01/constraint-vault
- Pinned commit: e7949720041458c6b23821fc4091343c7b3fd0d9
- Verified on Hermes v0.22.5: passes `hermes plugins validate`, hooks/tools registered per `hermes plugins doctor`, and the plugin is enabled and running live in my own Hermes gateway.

Pins the user exact constraints (numbers, addresses, hard rules) as structured local data and re-injects them verbatim into the model context on every turn and immediately after every context compaction, with a SHA-256 hash-logged injection record, because memory providers and compression silently paraphrase or drop exact values. Not a memory provider and not a compressor: a guard layer above both. Disclosure: local code only; stores constraints in a JSON file under ~/.hermes managed through its own tools and commands, reads them back for injection, opens no network connections and starts no processes.

Entry for the Hermes Agent Plugin Hackathon.

## Add escalation-governor to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149267
State: closed; created 2026-11-05T04:55:28Z

Adds **escalation-governor** (v0.1.0) to the community plugin catalog.

- Repo: https://github.com/jusst01/escalation-governor
- Pinned commit: 50fcf38919b721fe481a60f728bf7271b15b6e82
- Verified on Hermes v0.22.5: passes `hermes plugins validate`, hooks/tools registered per `hermes plugins doctor`, and the plugin is enabled and running live in my own Hermes gateway.

Deterministic stuck-detection for Hermes sessions. Watches tool/API failure signals (consecutive tool errors, repeated identical calls, API error bursts, model calls without progress) and, when a threshold trips, injects a structured escalation packet (goal, what was tried, what failed) directing the agent to delegate the remaining work to a stronger model via delegate_task instead of retrying blindly; writes a per-session JSONL report with escalation and token-usage accounting. Disclosure: local code only; reads tool results and API status inside the session, writes one JSONL report file per session under ~/.hermes, opens no network connections, starts no processes, and never blocks a tool call (fail-open).

Entry for the Hermes Agent Plugin Hackathon.

## catalog: add zotero entry
https://github.com/NousResearch/hermes-agent/pull/150511
State: open; created 2026-11-07T05:35:03Z

## What does this PR do?

Adds the `zotero` catalog entry for [Zotero Research](https://github.com/suhas-svg/hermes_zotero), pinned to `dd1f8f910d2ec1544da3cc3f77eb6d6ea6955b2a`.

Zotero Research lets Hermes answer from the user's own Zotero library instead of from memory. It adds seven tools (`zotero_status`, `zotero_search`, `zotero_item`, `zotero_fulltext`, `zotero_cite`, `zotero_add`, `zotero_verify`), a `/zotero` slash command, a `hermes zotero status|search|cite` CLI, and a bundled `zotero:research` skill. The model can read the user's PDF highlights and comments (with page labels), search a paper's indexed full text for passages, and format references with Zotero's own CSL engine (any installed style, plus BibTeX/BibLaTeX/RIS/CSL-JSON). It can also add papers by DOI or arXiv id with the PDF attached, and check a draft's author–year and DOI citations against the library. The client uses only the standard library and has no Python dependencies.

**Disclosure:**
- Every read goes to Zotero desktop's local API on loopback (`http://127.0.0.1:23119`), which is read-only.
- `zotero_add` is the only write and the only outbound call, and it runs only when that tool is called. It fetches public metadata from `api.crossref.org` (DOIs) or `export.arxiv.org` (arXiv ids) and downloads arXiv PDFs from `arxiv.org`; only the identifier is sent. It saves through Zotero's connector endpoint (the one the browser extension uses) into the collection currently selected in Zotero, and skips items already in the library.
- The only file it reads is Zotero's `storage/<key>/.zotero-ft-cache` inside the Zotero data directory, as a full-text fallback.
- No telemetry, no credentials or API keys, no `.env`/auth reads, no shell commands, no core override.
- It requires Zotero 7+ with Settings → Advanced → "Allow other applications on this computer to communicate with Zotero" enabled.

## Related Issue

N/A — new catalog entry (Hermes Plugin Hackathon submission).

## Type of Change

- [x] New feature (non-breaking change that adds functionality)
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] Security fix
- [ ] Documentation update
- [ ] Tests
- [ ] Refactor
- [ ] New skill

## Changes Made

- `plugin-catalog/zotero.yaml`: the catalog entry with the exact 40-character pin, version `1.0.0`, `requires_hermes: ">=0.22.5"`, and the seven declared tools.

## How to Test

1. `python scripts/validate_plugin_catalog.py plugin-catalog/zotero.yaml` → `OK: 1 file(s) valid`.
2. Clone `https://github.com/suhas-svg/hermes_zotero` at `dd1f8f910d2ec1544da3cc3f77eb6d6ea6955b2a` and run `hermes plugins validate .` → validation passes (manifest, config schema, capability probe, declared tools/hooks/middleware, no built-in collisions, security scan safe, no core override).
3. In the plugin repo, `python -m pytest -q` → **35 passed**. The tests use a fake Zotero server (local API plus connector) on `127.0.0.1:0` and an injected metadata fetcher, so they need no network. `hermes plugins doctor .` → 7 tools, 0 hooks.
4. Install with `hermes plugins install suhas-svg/hermes_zotero --ref dd1f8f910d2ec1544da3cc3f77eb6d6ea6955b2a --enable`. Then, with Zotero running and the local API enabled:
   - `hermes zotero status` → connected, collections, recently added items;
   - ask Hermes to add `1810.04805`, then to quote what the BERT paper says about "masked language model", and to cite it in APA.

### Live E2E evidence

Tested on Windows 11, Python 3.14.9, Hermes `v0.22.7+437`, Zotero `10.0.7` (fresh install):

- `zotero_add` with `1706.03762`, `10.1038/nature14539` and `2005.14165`: Crossref/arXiv metadata was saved through the connector, with correct item types (`preprint` / `journalArticle`), dates, DOIs and all 31 GPT-3 authors. Re-adding `1706.03762` reported `exists` with its key instead of duplicating it.
- `zotero_add` with `https://arxiv.org/abs/1810.04805` gave `pdfs_attached: 1`. The connector ignores attachment URLs in `saveItems`, so the plugin uploads the PDF bytes through `connector/saveAttachment` in the same session, just like the browser connector. Zotero indexed the PDF, and `zotero_fulltext` with `find: ["masked language model", "next sentence prediction"]` returned the matching passage from the paper's introduction.
- `zotero_cite` returned APA bibliography entries, IEEE `[1]`, and Zotero's BibTeX export for real items.
- `zotero_verify` on a sentence citing (Vaswani et al., 2017), (LeCun et al., 2015), (Brown et al., 2020) and (Hochreiter & Schmidhuber, 1997) reported 3 matched with their item keys and 1 not in the library.
- With the local API switched off, every tool returns `"Zotero's local API is turned off."` with a hint naming the exact setting; with Zotero closed, it returns an "Open the Zotero desktop app" hint. Neither case raises a traceback.

## Checklist

### Code

- [x] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [x] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`catalog: add zotero entry`)
- [x] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [x] My PR contains **only** changes related to this entry (one file under `plugin-catalog/`)
- [ ] I've run `pytest tests/ -q` and all tests pass — N/A for a catalog-only change; the plugin's own 35 behaviour tests pass at the pinned SHA
- [ ] `python scripts/check` passes — N/A for a catalog-only change; the catalog validator and pinned-source validator are the relevant gates
- [x] I've added tests for my changes (in the plugin repo: `tests/test_zotero_plugin.py`, 35 tests)
- [x] I've tested on my platform: Windows 11, Python 3.14.9, Hermes v0.22.7+437, Zotero 10.0.7

### Documentation & Housekeeping

- [x] I've updated relevant documentation (the plugin's `README.md` at the pinned commit covers setup, config and disclosures)
- [ ] I've updated `cli-config.yaml.example` if I added/changed config keys — N/A (plugin-owned config schema)
- [ ] I've updated `CONTRIBUTING.md` or `AGENTS.md` if I changed architecture or workflows — N/A
- [x] I've considered cross-platform impact (Windows, macOS) per the compatibility guide — pure Python/stdlib; Zotero's local API and data directory layout are the same on Windows, macOS and Linux
- [x] I've updated tool descriptions/schemas if I changed tool behavior — N/A (new plugin, schemas live in the plugin repo)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## feat(plugin-catalog): add Obol, safe invoicing for people who bill clients
https://github.com/NousResearch/hermes-agent/pull/149915
State: open; created 2026-11-06T07:25:55Z

## What does this PR do?

Adds `plugin-catalog/obol.yaml`: **Obol**, an invoicing plugin for freelancers, consultants and agencies who bill
clients. It works from any chat Hermes runs in. Forward a client's message and Hermes drafts the invoice
(structured extraction through `ctx.llm`). You approve it and it goes out, either as a Stripe payment link or as a
bank-transfer PDF invoice that needs no payment provider. Then ask "have they paid?". Obol also adds Invoices and
Security views to the dashboard and `/invoices` to every chat.

Agents that handle money are a new target for invoice scams, so every invoice write goes through Hermes's approval
prompt. The prompt shows the amount, the recipient, the mode and Obol's risk checks:
- prompt injection in the forwarded message (the message can never choose the recipient);
- lookalike and impersonated client addresses;
- duplicates and unusual amounts;
- recently changed client contact details;
- in bank-transfer mode, a change to your own payout bank details.

Live keys are refused unless `allow_live` is set. Writes are refused in unattended runs.

- Repo: https://github.com/UEddy/Obol (pinned at `d21df0241a3c88d0def0f12ef7ffa581e6e0b59f`)
- - Demo video (70 s, real footage, Stripe test mode and a live Telegram bot): https://x.com/DeFiRanch/status/2118752233315791051
- Threat model with a test behind every row (T1–T20): https://github.com/UEddy/Obol#threat-model

## Related Issue

Nous Research Hermes Plugin Hackathon submission.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality): a new catalog entry

## Changes Made

- `plugin-catalog/obol.yaml`: a new entry.
  - Community tier, `requires_hermes ">=0.22"` (the same floor as in `plugin.yaml`).
  - Capabilities match the plugin's registrations: 8 tools and the `pre_tool_call` hook. `requires_env` is empty: `STRIPE_API_KEY` is `optional_env` in `plugin.yaml` (Stripe mode only), so install never asks for it and bank-transfer users don't need it.
  - Four screenshots, pinned to the SHA.

## Disclosure (rule 13)

**Network calls**
- **Stripe mode:** HTTPS to `api.stripe.com` only. Calls happen:
  - when an Obol tool runs, or on `/invoices sync` and `hermes obol doctor|sync`;
  - in the approval hook before a write, to refresh the customer's invoices and recent `customer.updated` events (5-second timeout);
  - during sync, for read-only fraud-risk (Radar) and dispute reads on paid invoices;
  - every 45 s while the dashboard tab is open;
  - in `hermes obol demo`, which creates and deletes test clocks, customers and invoices (test keys only).
- **Bank-transfer mode:** no network calls at all.
- Polling only: no webhooks and no open ports.

**Other services**
- `obol_draft_from_message` sends the forwarded message to the model the user has configured in Hermes, through `ctx.llm`.
- In Stripe mode, Stripe emails the client when an invoice is sent or reminded. Bank-transfer mode emails nobody; the user sends the PDF.

**Credentials**
- `STRIPE_API_KEY` is optional (Stripe mode only) and read only through `agent.secret_scope.get_secret`. It is never stored, logged or shown; anything key-shaped is scrubbed from error messages. Without it, Stripe-mode tools, `/invoices sync` and the doctor answer "Stripe key not set" and make no calls.
- The bank details for bank-transfer mode are plugin settings in the user's Hermes config, printed on the PDFs they issue. Obol's logs keep only a fingerprint of them (and the last four digits of the account in a payout-change flag).

**Stored data**, all under `<HERMES_HOME>/plugin-data/obol/`:
- `data.db` (SQLite) holds:
  - the cached invoice metadata;
  - risk findings;
  - hash-chained activity and security logs (forwarded message text is not stored);
  - in bank-transfer mode, the customers (name, email) and invoices Obol keeps itself.
- `invoices/*.pdf` holds the bank-transfer invoices.

**Reads outside its own data:** only its own settings, through `ctx.get_config`.

**None of these:** telemetry, shell commands, background processes, subprocesses, self-updating code or observers on other plugins' tools. The only hook gates Obol's own write tools.

**Approvals:** Obol never auto-approves. Under YOLO or `approvals.mode: off`, Hermes approves everything, Obol's prompts included. The live-key and unattended-run refusals still apply.

## How to Test

1. `hermes plugins install ueddy/obol` (no key prompt), then `hermes config set STRIPE_API_KEY sk_test_…` and `hermes obol doctor`. The doctor checks the key mode and that the provider is reachable, and verifies both hash-chained logs.
2. `hermes obol demo` seeds the test account with paid, open and overdue invoices and prints four prompts to try:
   - forward a client's message;
   - "have they paid?";
   - a lookalike-address scam;
   - paying with test card `4242 4242 4242 4242`.
3. **Bank-transfer mode with no Stripe account or key:** set `provider: bank_transfer`, `bank_account_name` and `bank_account_number` under `plugins.entries.obol.settings`. Then:
   - ask Hermes to invoice a client and approve; you get an `INV-0001` PDF;
   - say the client paid, which calls `obol_mark_paid` (also approved);
   - `/invoices` shows the ledger.
4. Plugin checks at the pinned SHA:
   - `hermes plugins validate --install-deps` passes;
   - `hermes plugins doctor --ci` passes (8 tools, 1 hook);
   - the install scanner verdict is `safe` (`tests/test_hermes_integration.py::test_install_scanner_rates_the_repo_safe`).

## Checklist

### Code

- [x] I've read the Contributing Guide and `plugin-catalog/README.md`
- [x] My commit messages follow Conventional Commits
- [x] I searched for existing PRs to make sure this isn't a duplicate
- [x] My PR contains **only** the catalog entry
- [x] The plugin's suite passes in its own CI at the pinned SHA. The CI runs a unit job, and a full job inside Hermes with `validate` and `doctor`: 230 passed, 2 skipped (the live suites skip without keys). It covers adversarial cases, recorded real responses, and the Telegram/WhatsApp/Slack/email gateway paths. There are also live suites against Stripe test mode and a real model.
- [x] Tested on Ubuntu (Hermes from source, Python 3.14), plus a live Telegram run

### Documentation & Housekeeping

- [x] Plugin README: setup, configuration, the threat model, what Obol does not protect against, and what it touches
- [x] N/A for `cli-config.yaml.example`, `CONTRIBUTING.md` / `AGENTS.md` (no core changes)

## Screenshots / Logs

![Invoices](https://raw.githubusercontent.com/UEddy/Obol/d21df0241a3c88d0def0f12ef7ffa581e6e0b59f/docs/screenshots/dashboard-invoices.png)
![Security](https://raw.githubusercontent.com/UEddy/Obol/d21df0241a3c88d0def0f12ef7ffa581e6e0b59f/docs/screenshots/dashboard-security.png)
![Approval prompt](https://raw.githubusercontent.com/UEddy/Obol/d21df0241a3c88d0def0f12ef7ffa581e6e0b59f/docs/screenshots/approval.png)
![Approval prompt flagging a lookalike scam](https://raw.githubusercontent.com/UEddy/Obol/d21df0241a3c88d0def0f12ef7ffa581e6e0b59f/docs/screenshots/approval-scam.png)


## feat(plugin-catalog): add dike plugin
https://github.com/NousResearch/hermes-agent/pull/150360
State: open; created 2026-11-06T23:44:12Z

## Summary

Owner submission for **Diké**, a native Hermes plugin that checks every article citation of Chilean law in a legal brief against a local, hash-identified copy of 25 statutes, and refuses to certify what it cannot prove. Entry for the Hermes Agent Plugin Hackathon.

- **Plugin repo:** https://github.com/Grizaceo/hermes-dike. It belongs to the account opening this PR, and I'm the owner and the only human contributor (rule 5). The engine is vendored unchanged from my own repository https://github.com/Grizaceo/dike at commit `5b9e19d`; `VENDORED.json` records per-file SHA-256 and `scripts/vendor_engine.py --check` verifies the copy.
- **Pinned SHA (0.2.0):** `9780e467ec31d4635eb559e4c09bd49f17e178de`.
- **Package root:** repo root (`plugin.yaml`, `__init__.py`), no `subdir`.

## What it does

Given a brief as text (`texto`) or as a `.md`/`.txt` path (`ruta`), it returns one record per detected article citation:

- **verified:** with the statute identifier, its Ley Chile source URL, the retrieval date and the SHA-256 of the article text;
- **unverified:** with the engine's reason, for example `AMBIGUOUS` (an "artículo 60" that names no statute and exists in more than one code) or `UNRESOLVABLE` (an article that is not in the corpus).

The output always carries `certificacion_sustantiva: false` and `certificacion_vigencia_actual: false`. It never claims that a provision supports the argument, nor that a dated copy (retrieved 2026-08-18) is today's text. The output is in Spanish, and it is not legal advice.

## Hermes surfaces it uses

- `ctx.register_tool`: one tool, `dike_verificar_citas`, in its own toolset `dike`. Its schema has two optional string fields, `texto` and `ruta`, and exactly one of them must be given.
- `ctx.register_command`: `/dike-verificar <text>`. It runs the same check on the text after the command, client-side and without a model call.
- `plugins.plugin_storage.plugin_data_dir("dike")`: all writes go under the active profile's `$HERMES_HOME/plugin-data/dike`.
- Manifest v2 `python_dependencies` (pydantic, pyyaml, rich, requests, cryptography, each with an upper bound) are installed by Hermes's installer.
- It registers no hooks, no middleware, no skills, no `requires_env` and no config schema.

## Disclosure (catalog rule 13)

The full list is in [docs/DISCLOSURES.md](https://github.com/Grizaceo/hermes-dike/blob/9780e467ec31d4635eb559e4c09bd49f17e178de/docs/DISCLOSURES.md) at the pin.

- **Subprocess, not a sandbox.** Each call runs the vendored engine (`python -m lexo_cli`) with the same interpreter as Hermes, via `subprocess.run`, without a shell and with a 300 s timeout. The child gets a minimal environment: `PATH`, `LANG`, `LC_ALL` and `TZ`, plus variables pointing at the plugin's data. Agent credentials and API keys are not passed. `PYTHONPATH` carries `motor/` and the Hermes process's `site-packages` folders so that the engine finds its dependencies; Hermes's own code is not on it. The child runs with the user's OS permissions.
- **Reads:** the text passed in, or the named file. Only regular `.md`/`.txt` files are accepted, never through a symlink, with a 400,000-byte maximum. It also reads its own `corpus/` and `motor/`.
- **Writes, only under `$HERMES_HOME/plugin-data/dike`:**
  - The corpus. On the first call, `corpus/chile-base-af1422d66d1e6eee.tar.gz` is checked against `corpus/SHA256SUMS`, unpacked with `tarfile`'s `data` filter, installed by the engine and published by an atomic rename. Every later call re-checks the installed files against the hashes recorded at install time, and stops if any differs.
  - A temporary copy of the brief, removed after each call.
  - Engine caches, plus the engine's `HOME`, which is redirected there.
- **Bundled archive (rule 17):** the tarball is plain JSON: one record per article (text, text hash, source URL, in-force window), plus the pack manifest and build report. That is 34,225 members and no executables; the install scanner rates it `safe`.
- **Code carried but not run:** `motor/` is the Diké engine as published, so it contains modules this plugin never calls (`agent_invoker.py`, `mcp/`, `hitl/`). The plugin runs only two engine commands: `starter install`, once, and `constancia --json`.
- **Never:** network calls after dependency install, model calls, signing or key access, hooks, background processes, scheduled jobs, telemetry, stored credentials, or self-updates.
- **Known UX limit:** `/dike-verificar` takes text, not a path. Given a path, it reports that it found no citations (`SIN_CITAS`). The tool's `ruta` field is the way to check a file.

## Testing

All on Linux, Hermes v0.23.0 (`2bd378ed`), each in a scratch `HERMES_HOME`:

- `hermes plugins install Grizaceo/hermes-dike` + `hermes plugins enable dike` installs commit `9780e467…`. Then `/dike-verificar` on the demo brief (`tests/fixtures/escrito_demo.md`) returns 6 citations: arts. 161, 162, 163 and 168 of the Código del Trabajo `VERIFICADA`; "artículo 60" `AMBIGUOUS`; art. 9999 `UNRESOLVABLE`. The first call took about 60 s, including the one-time corpus install. The second took 23 s wall time, Hermes startup included.
- On a fresh clone at the pin, `hermes plugins validate --install-deps` passes all checks (capability probe matches the entry, security scan `safe`, no core override). `hermes plugins doctor --ci` passes too: 1 tool, 0 hooks.
- `scripts/validate_plugin_catalog.py plugin-catalog/dike.yaml` prints `OK: 1 file(s) valid`.
- Tool selection with a real model (a Nous-hosted model, in a clone of my own profile with ~470 tools, so `dike_verificar_citas` sits deferred behind `tool_search`). Prompts never name the tool; each prompt ran 5 times:
  - "Revisa las citas de este escrito…" with the brief: 5/5 called the tool.
  - The same request in English: 5/5.
  - Only the file path given: 5/5. The model read the file and then called the tool with `ruta`.
  - "¿Están bien citados los artículos de ley en este escrito?": 3/5. In the other 2 runs the model used web search instead, and still flagged arts. 60 and 9999.
  - "Resume este escrito en tres líneas" (control): 0/5 calls, as expected.
  - Every call returned 4 of 6 verified.
- The plugin's own suite: 73 tests pass with Python 3.11.16 against the Hermes v0.23.0 checkout; the 7 end-to-end tests also pass with networking off (`unshare -rn`). The install, `validate`, `doctor` and model runs above used Hermes's own interpreter, Python 3.14.9.

## Notes on the entry

- `requires_hermes: ">=0.22.7"` is the version the plugin was first tested on, also declared in `plugin.yaml`.
- `platforms: [linux]`: it uses `fcntl` and has only been tested on Linux.
- `tier: community`, `category: tools`.

Generated with [Devin](https://devin.ai)


## feat(plugin-catalog): add lahja (Arabic dialect speech-to-text)
https://github.com/NousResearch/hermes-agent/pull/149968
State: open; created 2026-11-06T09:43:46Z

Adds **Lahja (لهجة)** (`plugin-catalog/lahja.yaml`), a community speech-to-text provider for Arabic dialects, pinned to [`Tarekkharsa/hermes-lahja@a7a43b1`](https://github.com/Tarekkharsa/hermes-lahja/tree/a7a43b1389a1ae169ff5c7401e9ec2ec9a53b51d) (`subdir: lahja`). Hackathon entry.

![Lahja banner](https://raw.githubusercontent.com/Tarekkharsa/hermes-lahja/a7a43b1389a1ae169ff5c7401e9ec2ec9a53b51d/docs/banner.png)

## What it does

Stock Whisper is weak on spoken Arabic, and its failures break an assistant. It rewrites dialect as formal Arabic (on a real Levantine voice note it flipped «مالها طعمة», *has no taste*, into «لها طعم ومعنى», *has taste and meaning*), and when it hears accented English as Arabic it translates it. Lahja is a local provider (`stt.provider: lahja`):

```
ffmpeg 16 kHz → Silero VAD → dialect fine-tuned Whisper large-v3-turbo (whisper.cpp)
      → subtitle-credit filter → corrections taught with /stt-fix → Hermes
```

- **Accuracy:** WER 29.1% vs 41.1% for stock large-v3-turbo on the 13 held-out dialect clips from the model card. Both run with the same q5_0 quantization, the same Silero VAD and the same decoding settings; stock without VAD scores 42.9%. `bench/run_bench.py` reproduces all of it.
- **Silence and noise:** Silero VAD is always on, plus a filter for subtitle credits («ترجمة نانسي قنقر», "subscribe to the channel") at the edges of a transcript. To be clear, VAD alone also fixes the silence case for stock Whisper. Lahja just never runs without it.
- **Language routing, never translation:** Arabic costs a single pass, because detection happens in the same decode. Notes detected as another language are decoded again by a stock Whisper model the user chooses (`other_languages_model`). So is English the dialect model wrote out phonetically in Arabic letters, which happens with accented English. A non-Arabic language is never forced, because Whisper forced into the wrong language translates. That includes the `stt.language: en` template default, and this was a real bug found while dogfooding.
- **`/stt-fix جي إلي تي => JLT`:** a correction taught once applies to every later note. It matches whole words only, ignores diacritics and hamza seats, and never does fuzzy guessing.

## Hermes surfaces used

- `ctx.register_transcription_provider` (`lahja`)
- `ctx.register_command` (`/stt-fix`)
- `ctx.register_cli_command` (`hermes lahja setup|models|status|test`)
- `ctx.get_config` for its settings (`stt_model`, `language`, `other_languages_model`, `vad`, `hallucination_filter`, `threads`) and `ctx.state` for the corrections and the data dir

No tools, hooks, middleware, env vars or credentials. No private core APIs.

## Disclosure (rule 13)

- **Network:** only `hermes lahja setup`. It downloads the files listed in `lahja/models.py` from `huggingface.co` over HTTPS, redirected to its `*.cdn.hf.co` CDN. Each URL names an exact repository commit (`resolve/<sha>`), and each file has a SHA-256 and a size cap; a mismatch deletes the file and fails. The dialect model comes from a community ggml mirror (`JoaoZaokk/…-ggml`); see provenance below. Transcription makes no network calls.
- **Subprocesses:** `ffmpeg` (`-protocol_whitelist file,pipe`, so local files only) and `whisper-cli`. Each runs with a fixed argv, no shell, stdin from `/dev/null`, one overall deadline per note (`timeout`, default 300 s), at most `max_parallel` (default 1) running at once, and a minimal environment (`PATH`, `LANG`, `LC_ALL`, `TMPDIR`, `LD_LIBRARY_PATH`), never Hermes' environment.
- **Reads:** the audio file Hermes passes, its own model files, and, only if configured, the `other_languages_model` `.bin` path the user sets.
- **Writes:** model files and the two phrases of each `/stt-fix` correction, both in its profile-scoped data dir. Audio is decoded in a temp dir deleted when the call returns. **No audio or transcripts are stored.**
- **Corrections are profile-wide text substitution.** Any user the gateway admits can add one with `/stt-fix`. Rules with control or invisible characters are refused, each side is at most 120 characters, and there are at most 500 rules.
- **No** background processes, telemetry or stored credentials.
- **Model provenance:** the default model is a ggml conversion of `oddadmix/whisper-large-v3-turbo-arabic-dialectal-v2` (Apache-2.0). `bench/convert.sh` reproduces it from the official weights at a pinned revision with the whisper.cpp v1.9.4 converter, and the result is **byte-identical** (same SHA-256) to the pinned download. The script also checks that the tokenizer files borrowed from `openai/whisper-large-v3-turbo` match the fine-tune's own.

## Checks at the pinned commit

- `hermes plugins validate lahja --install-deps`: all checks pass, **security scan: safe**, no core override (fresh clone at the pinned SHA).
- `scripts/validate_plugin_catalog.py`: OK, no warnings for the entry. `scripts/scan_plugin_payloads.py`: clean.
- 100 tests in the repo. CI runs the unit tests on Python 3.11, 3.12 and 3.13, plus a **macOS job with a real whisper.cpp** (pinned `tiny` model) that checks four things against real engine output: language detection parsed from `whisper-cli`'s log, Opus voice notes, VAD on silence and noise, and that no Hermes env var reaches the subprocess.
- Before opening this PR I had an independent reviewer go through the code. It found and I fixed:
  - Code-switched Arabic being treated as English: Gulf «ذا/ذي» and Maghrebi «وي» collided with the marker list.
  - The filter deleting real requests: «شغل موسيقى», "play music", lost «موسيقى».
  - A one-word correction swallowing two words.
  - An invalid optional setting failing every note.
  - Unbounded parallel decodes.
  - Manifest keys Hermes doesn't know.
  - Download URLs on `main`.

  Each fix has a regression test.
- Tested end to end on Hermes 0.22.6 (macOS, Apple M4) through the gateway's real `transcribe_audio` path with Telegram voice notes. `requires_hermes` is set to the line I tested; every API it uses is also present in v0.21.6.

One note for review: `agent.log` gets a `capability_check plugin=lahja capability=tools.override decision=deny` line each time a `hermes lahja …` subcommand runs. I saw it only for those CLI runs, not for transcription or other `hermes` commands. The plugin never asks for that capability and registers no tools, and everything works with the deny.

## Known limits (also in the README)

- English words inside Arabic sentences come out phonetically. Numbers are written as words.
- With `stt.language: ar` (or the plugin's `language: ar`), every note is decoded as Arabic: no detection and no English check.
- Algerian is worse than stock on the benchmark clip, and Maghrebi dialects are the hardest for every model.
- Tested on Apple Silicon. Linux should work wherever whisper.cpp does; Windows is untested.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## feat(mission): add dry-run mission preview CLI
https://github.com/NousResearch/hermes-agent/pull/26837
State: open; created 2026-05-16T08:35:14Z

## Summary
- add `hermes mission create --dry-run --file SPEC [--json]`
- compile Mission Control specs into deterministic previews of task graph creation, final ACK subscription, and watchdog setup
- keep M0 preview-only with explicit no-side-effect safety flags for Kanban, cron, gateway sends, and agent triggers

## Why
This introduces a small upstream-friendly Mission Control primitive for planning durable multi-step work before any dispatch happens. It is intentionally not a dashboard rewrite or a live conductor: M0 only validates and previews the mission envelope.

## Duplicate / overlap check
Before opening this draft I checked related open/closed PRs and issues for `mission`, `mission control`, `ACK`, and `watchdog`.

Notable overlaps:
- #15892 `[Hackathon/WIP] Mission Control shadcn dashboard` — dashboard/UI shell work; this PR is CLI preview/spec compilation only.
- #19490 `feat: add mission control dashboard foundation` — closed dashboard/API foundation; this PR does not touch dashboard APIs.
- #18133 `fix(gateway): manage conductor mission processes` — conductor process management endpoints; this PR creates no processes and has no live dispatch.
- #9116 long-running task watchdog heartbeat — runtime heartbeat feature request; this PR only previews a future watchdog plan.
- #22135 multi-agent boardroom consensus — agent reasoning/consensus protocol; this PR is an ops envelope preview, not an execution loop.

So this is deliberately narrow: a dry-run Mission Control CLI contract that can later feed Kanban/cron/gateway adapters without introducing side effects in this slice.

## Safety
- `mission create` currently requires `--dry-run`; missing it exits non-zero.
- Preview output includes explicit safety fields:
  - `dry_run_only: true`
  - `would_write_kanban: false`
  - `would_create_cron: false`
  - `would_send: false`
  - `would_trigger_agent: false`
- No credentials or environment secrets are read or emitted.
- YAML support uses `yaml.safe_load`; JSON works without relying on YAML-specific syntax.

## Test Plan
- [x] `python -m pytest tests/hermes_cli/test_mission_cli.py -q`
- [x] `python -m py_compile hermes_cli/mission.py hermes_cli/main.py hermes_cli/commands.py`
- [x] `python -m hermes_cli.main mission create --dry-run --file /tmp/mission-m0.yml --json | python -m json.tool`
- [x] missing `--dry-run` top-level CLI smoke exits `2`
- [x] `git diff --check origin/main...HEAD`
- [x] `python scripts/check-windows-footguns.py --diff origin/main`

## Notes for reviewers
The most important review points are:
1. CLI shape: `hermes mission create --dry-run --file SPEC [--json]`
2. Whether the preview schema is a reasonable seed for future Kanban/cron/gateway adapters
3. Whether the dry-run/no-side-effect boundary is clear enough for a first slice


## Add token-dashboard to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149187
State: closed; created 2026-11-05T01:01:30Z

Catalog entry for **token-dashboard**, submitted for the Hermes Agent Plugin Hackathon.

**What it does:** a Hermes Desktop plugin (right pane plus status bar chip) showing the focused session's live token usage and cost as you work, with a recent-sessions overview. Cost uses the backend-reported `cost_usd` when available and otherwise a clearly labelled estimate from a built-in per-model price table.

**Honest scope:** Hermes exposes no per-session token history (the `session.list` rows carry title, start time, and message count only), so token figures describe the focused session, the data the Desktop SDK actually provides, and past sessions are listed with message counts instead of invented totals.

**Disclosure (catalog rule 13):** reads the focused session usage state and the session list through the Desktop host API and renders locally; no network calls, no storage, no env vars. Desktop surface stays inside the plugin SDK.

**Verification at the pinned commit:**
- `hermes plugins validate`: passed, including the desktop surface check
- Load-tested in the real Hermes Desktop app: the pane and chip run against live data (an earlier draft's wrong RPC name was caught in the app's own log and fixed; session fetches are overlap-guarded because `session.list` can cold-spawn a profile backend)

## Add ProofGate to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149185
State: closed; created 2026-11-05T01:01:16Z

Catalog entry for **ProofGate** (`proofgate`), submitted for the Hermes Agent Plugin Hackathon.

**What it does:** verifies the agent's completion claims (file created, message sent, command ran, tests passed, figures quoted) against tool evidence recorded in the same session, before the final reply is delivered. Verdicts are fail-closed: PASS ships with a verification footer, DOWNGRADE flags unproven claims in the reply, BLOCK withholds a reply whose claims are backed by no evidence (or contradicted by a failed tool attempt). Every verdict goes to an append-only local ledger.

**Disclosure (catalog rule 13):** observes every tool call and final reply in sessions of profiles where it is enabled; stores redacted argument/result summaries locally only under `$HERMES_HOME/proofgate/`; makes no network calls; in enforce mode it holds reply streaming while the deterministic (no-LLM) check runs. Declared capabilities match registrations exactly.

**Verification at the pinned commit:**
- `hermes plugins validate`: passed all checks, security scan safe
- `hermes plugins doctor`: OK, 1 tool and 3 hooks registered under the real runtime contracts
- 8/8 checker unit tests pass (`tests/test_checker.py`)
- End-to-end hook smoke test: a proven file claim received the PASS footer; a send claim contradicted by a failed tool call was withheld (BLOCK) and written to the ledger

## catalog: living-field
https://github.com/NousResearch/hermes-agent/pull/149190
State: closed; created 2026-11-05T01:16:09Z

## What it does

Living Field is a Hermes Desktop pane of the spatial desk we built for ABUZ8 before Hermes Desktop existed. Four domains (Dream, Forge, Command, Abyss) and a seeded neural field. Synapses speed up only while the focused session is actually working. The field dims when the gateway socket is not open. The model line is the live model name, or "no model".

Plugin repo, pinned in this entry: https://github.com/abuz8studios-ship-it/hermes-living-field
SHA: d727be944518ab562857c61e1db4a0dc62ae742a

## Surfaces

- Desktop pane (`desktop/plugin.js`, area `panes`, right, 420px)
- Desktop status chip (`statusBar.right`)
- No Python tools, hooks, or middleware
- No `plugin_api.py`

`hermes plugins validate` on that SHA: passed. Security scan safe. Desktop surface check passed.

## Disclosure (rule 13)

- No network calls.
- No shell.
- No credentials, no telemetry.
- Reads only Desktop SDK atoms already on the host: `host.state.busy`, `host.state.gateway`, `host.state.model`.
- Does not import Three.js and does not fetch it. The original ABUZ8 kernel uses a vendored Three.js module; this catalog build is a canvas port because a listed desktop plugin may only import `@hermes/plugin-sdk` and React.
- Does not fabricate metrics. Idle stays idle. A closed socket stays dim.
- Desktop half is off until the user enables it.

Hackathon entry. Demo is the pane: send a message, synapses go gold for that turn, then return to idle.

## [Bug]: RuntimeError: Failed to initialize OpenAI client: No module named 'pydantic_core._pydantic_core
https://github.com/NousResearch/hermes-agent/issues/123650
State: open; created 2026-09-26T07:02:03Z

### Bug Description

Interacting with Hermes Agent via Slack is not working anymore since a few updates.

### Steps to Reproduce

Start Hermes Agent Desktop, hit the "Restart Gateway" toggle since it is not started by default. Wait until it says its up and running. I can see Slack is connected with the blue dot. In slack i ca see the Hermes Agent bot is online (green dot).

Mention the bot and type a simple command.

### Expected Behavior

Hermes Agent Desktop will process the message and start connecting with my LLM.

### Actual Behavior

In Slack I got this error:

`:warning: Something went wrong and I couldn't finish this reply.
Use /retry to try again, or /new to start a fresh conversation. Technical details are in the gateway log (hermes logs).

This turn did not complete. Some actions may already have run; verify their effects before resending.`

### Affected Component

Gateway (Telegram/Discord/Slack/WhatsApp)

### Messaging Platform (if gateway-related)

Slack

### Debug Report

```shell
https://paste.rs/upSKa
https://paste.rs/UYI0O
https://dpaste.com/6ZE4M2WX2
https://dpaste.com/ETCQAG4VW
```

### Operating System

Windows 11

### Python Version

3.11.0

### Hermes Version

Hermes Agent v0.20.5 (2026.8.19) · upstream d0288be5 Install directory: C:\Python311\Lib\site-packages Install method: unknown Python: 3.11.0 OpenAI SDK: 2.24.0 Up to date

### Additional Logs / Traceback (optional)

```shell

```

### Root Cause Analysis (optional)

_No response_

### Proposed Fix (optional)

_No response_

### Are you willing to submit a PR for this?

- [ ] I'd like to fix this myself and submit a PR

## catalog: add clack — encrypted agent-to-agent messaging
https://github.com/NousResearch/hermes-agent/pull/149183
State: closed; created 2026-11-05T00:52:46Z

## Plugin

**clack** — gives any Hermes agent native [Clack](https://github.com/adroidian/clack) messaging: end-to-end-encrypted agent-to-agent messages over a self-hostable relay, with signed delivery receipts and no plaintext fallback.

- **Source:** https://github.com/adroidian/clack (monorepo), subdir `plugins/hermes-clack`
- **Pinned SHA:** a965b33051d35bcef1dd3fa15255d34aacdba99a (branch `hermes-plugin`)
- **Owner submission:** I own the source repo.

## What it does

Nine tools (`clack_send`, `clack_poll`, `clack_ack`, `clack_peers`, `clack_whoami`, `clack_invite`, `clack_join`, `clack_accept`, `clack_reconcile`) plus a bundled coordination-etiquette skill. E2EE via vendored stdlib-only X25519 + ChaCha20-Poly1305 + Ed25519 (byte-identical to the canonical repo copies). Zero Python dependencies. Identity/keys live in the plugin data dir at 0600. Relay identity pinning (fresh-nonce RSA verification) before any credentials cross the wire. Bounded inbox retrieval with durable rejection quarantine; explicit ack semantics with fsynced delivery journal.

## Validation

- `hermes plugins validate --install-deps` on hermes-agent main (ed1afb0): **passes, zero warnings**
- 38 tests green (protocol roundtrips, forged-ciphertext rejection, no-plaintext-fallback, cross-origin invite rejection, poison-prefix and large-backlog attack reproductions)
- Live demo: `plugins/hermes-clack/demo/run_demo.sh` — two throwaway Hermes profiles against a local relay; encrypted send → redelivery-before-ack → explicit ack → signed receipt roundtrip, all passing
- README + VALIDATION.md disclose the trust model, limitations, and self-hosting path

Submitted for the Hermes Plugin Hackathon. Demo video + entry form to follow ahead of the Nov 11 deadline.

## feat(plugin-catalog): add hermes-ui-cards plugin
https://github.com/NousResearch/hermes-agent/pull/150556
State: open; created 2026-11-07T07:33:06Z

## What does this PR do?

Adds **HUI+ Cards** (`hermes-ui-cards`) to the plugin catalog, as my entry for the plugin hackathon.

Hermes answers with cards you act on in its chat: edit a plan before it runs, compare options, tick off a list, fill in a form, approve a risky step. When you submit a card, your answer goes back as your next message and Hermes continues from there. 17 card types (plan, review, checklist, compare, form, confirm, steps, decision, calc, rank, choice, schedule, recipe, flashcards, rating, slider, quiz).

It is one package: a Python tool `hui_present` validates each card against a schema and writes it as a `MEDIA:` file; the Desktop half draws that file with a tool-media renderer (`transcript.toolMedia`) and sends the answer through `host.composer.submit`. Hooks give the model the answer context, a small backend records answers so a card can't be answered twice across windows. CLI, TUI and messaging get the same card as plain text.

- **Plugin repo:** https://github.com/robbyczgw-cla/hermes-ui-cards, owned by the account opening this PR, no other contributors.
- **Pinned SHA (v0.1.0):** `c40df4d41cd5439cf4902995fd4a9e5505483f25`, released as [`v0.1.0`](https://github.com/robbyczgw-cla/hermes-ui-cards/releases/tag/v0.1.0).
- **Demo video (X):** https://x.com/CamiAi__/status/2118980850800820604

## Related Issue

None. New catalog entry.

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [x] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🔒 Security fix
- [ ] 📝 Documentation update
- [ ] ✅ Tests (adding or improving test coverage)
- [ ] ♻️ Refactor (no behavior change)
- [ ] 🎯 New skill (bundled or hub)

## Changes Made

- `plugin-catalog/hermes-ui-cards.yaml` (new): pinned to `c40df4d`, `category: desktop`, `requires_hermes: ">=0.22.6"` (first release with the tool-media renderer area), banner and six card screenshots as raw links at the pinned sha, README rendered from the pin.
- Capabilities: tool `hui_present`; hooks `pre_llm_call`, `transform_llm_output`, `post_compaction`; no middleware; no required env.

## How to Test

1. `python scripts/validate_plugin_catalog.py plugin-catalog/` → `OK: 1066 file(s) valid`
2. `hermes plugins validate <checkout at c40df4d> --install-deps` with Hermes v0.22.7 → `Validation passed`; no python dependencies declared, security scan safe, no core override, desktop surface stays inside the plugin SDK, declared tools/hooks match registrations.
3. Install: `hermes plugins install robbyczgw-cla/hermes-ui-cards --enable`, turn on the Desktop half (Capabilities → Plugins → HUI+ Cards), then ask Hermes e.g. "make me a packing list I can tick off" or run the command-palette item *HUI+ Cards: show an example card*.
4. Plugin tests at the pin: `pytest tests -q` (467 passed) and `npm test` (Desktop, jsdom); an e2e test runs a real Hermes with a scripted model.

## Disclosure (catalog rule 13)

> **Surfaces and permissions:** Registers the `hui_present` tool; `pre_llm_call`, `transform_llm_output` and `post_compaction` hooks; `/cards`; a card-writing skill; a Desktop/Webapp tool-media renderer and palette demo; and authenticated, read-only plugin `/answers` and `/settings` backend routes. Uses public plugin/SDK APIs. No middleware, required secret environment variables, credential backend or core overrides.
>
> **Network and provider data:** Desktop reads answers/settings from the selected local or remote Hermes backend, including polling, retries and reconnect/focus checks; settings saves may fall back to the `plugins.manage` list RPC. Full card tool results and submitted answers go to the configured model provider in the ordinary conversation. An answer is one user message: a readable first line, then the answer JSON after Hermes' own `--- Attached Context ---` line (Desktop and the Webapp collapse that part of the stored bubble; the provider and Hermes session history keep the whole message). The `pre_llm_call` hook adds card context (card identity/title, confirm action/command, duplicate/staleness notes) and a short Desktop hint at most once per 20 user turns; Hermes stores hook context with the user message and replays it in later turns. Model-supplied HTTPS images are loaded directly by the client with no referrer; their hosts see the client's IP. User-opened source links open their HTTPS destinations. No telemetry or usage reporting.
>
> **Reads outside plugin data:** Reads active-profile Hermes configuration through public read-only configuration APIs for display settings and UI+ detection, and nonsecret Hermes session/platform/home context. No direct reads of credential stores, `.env`, auth/token files or arbitrary user files. Reads its own packaged schema, skill and card copies.
>
> **Stored content and retention:** Stores per-profile card/session membership, compaction links and answer receipts in `plugin-data/hermes-ui-cards/answers.db` (SQLite/WAL), including summaries and answer JSON/free text such as form values, comments, changes and notes. Keeps 2,000 recently shown/answered cards, up to 8 answering sessions and 16 members per card, and 5,000 continuation links with depth-64 traversal. Answer JSON cap is 20,000 UTF-8 bytes. Stores the latest 500 Markdown card copies with full card JSON, including confirm action/command. No time expiry or chat-deletion cleanup. Browser/plugin storage independently retains up to 300 drafts and 5,000 receipts, including unsent draft text, under active connection/profile/chat/card keys when owner atoms exist; these caps apply across those local namespaces. Anyone authenticated to the selected backend who knows the relevant chat/card IDs can request the visible answer. Global answer invalidation events carry an empty payload, revealing activity but no identifiers/content.
>
> **Processes, execution and approvals:** Spawns no runtime background process or shell command; mounted open cards use bounded-backoff browser timers for synchronization. Confirm cards only send a decision to the model; Hermes's tool approval system still controls any subsequent command. No credentials are requested or stored as credentials; user-entered free text is retained as described above and may itself contain sensitive information.
>
> **Known behavior limits:** Receipt synchronization is eventual, not an atomic exactly-once execution protocol. Simultaneous/offline clients can both submit; backend recording keeps the first and supplies a duplicate warning to the model. Storage/REST ownership follows the active gateway, which may differ from a split-view chat's owner. Runtime→stored state migration requires host-confirmed focused-view mapping; missing/unfocused mapping resets the card. Staleness warnings depend on retained presentation history and instruct the model rather than enforcing a fresh-Yes guard. Tested on Hermes 0.22.7 (Desktop half via the Hermes Webapp); 0.22.6 is the declared floor because it is the first release with the tool-media renderer area, but it was not run.

## Checklist

### Code

- [x] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [x] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [x] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [x] My PR contains **only** changes related to this fix/feature (no unrelated commits)
- [ ] I've run `pytest tests/ -q` and all tests pass (N/A: one catalog YAML; the catalog validator and `hermes plugins validate` above pass)
- [ ] `python scripts/check` passes (N/A: catalog entry only)
- [x] I've tested on my platform: Ubuntu 24.04 (Hermes Webapp v0.22.7)

### Documentation & Housekeeping

- [x] I've updated relevant documentation — N/A (catalog entry; the plugin's README renders from the pin)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: bump tameru to 1.6.0
https://github.com/NousResearch/hermes-agent/pull/149336
State: closed; created 2026-11-05T06:53:52Z

## Summary

Re-pins the `tameru` catalog entry from `5a19df4` (v1.5.0) to `9f80514` (v1.6.0, current `main` of [0xWhiteMage/hermes-tameru-plugin](https://github.com/0xWhiteMage/hermes-tameru-plugin)).

**What the pin adopts (v1.5.0 → v1.6.0):**
- Vendored engine Tameru 1.6.0: reducers for many more tool outputs — build/test/package-manager runs (Gradle, RSpec, PHPUnit, dotnet test, Maven, npm/yarn/composer, pip, bundler, Ansible, MSBuild/tsc, Playwright, cargo, CMake), containers and orchestration (docker build/ps, kubectl describe/events/rollout, compose), service logs (nginx/Apache/MySQL/HAProxy/Postgres/Redis, syslog/journal/dmesg/klog, PHP), and Windows tooling (PowerShell, msiexec, netstat, ipconfig, nmap, traceroute, openssl)
- Anchors and summaries for generic and empty queries, multi-language query handling and prose briefs, a private regex cache
- User-facing catalogue README (a real before/after example) and plain-language `tameru_expand`/`plugin.yaml` descriptions

**Disclosure status:** unchanged from the reviewed 1.5.0 entry — same surfaces (context-engine subclass with shape-checked fallback, `tameru_expand` tool, `python -I -S` grep child), no network calls, no env vars, telemetry file off by default. Re-measured replay results and full release notes are in the plugin repo's README and CHANGELOG at the pinned commit.

Entry vehicle for the [Hermes Plugin Hackathon](https://x.com/NousResearch/status/2118094256438936062).

#### Test plan
- [x] Entry schema matches `plugin-catalog/README.md` (sha is the 40-char pin, version quoted, image re-pinned to the same sha)
- [x] Plugin validated in its own CI at the pinned commit (`hermes plugins validate` per docs/RELEASING.md; stub + real-Hermes suites green at Hermes `1298c8e`)
- [ ] Catalog CI (`hermes plugins validate` at the pinned sha)

Generated with [Devin](https://devin.ai)

## feat(plugin-catalog): add thoth entry
https://github.com/NousResearch/hermes-agent/pull/150497
State: open; created 2026-11-07T05:15:00Z

Adds **Thoth**: agents working as one team, each with its own harness (Claude Code, Codex and Hermes today). Pinned to cayden970207/thoth@bc5707377505aa92b808e78d6a0e88ad7f2e507e (0.7.0).

## What it does
Hermes plans tasks onto a shared board and starts the real `claude` and `codex` CLIs on them, on the user's own logins and plans, each in its own git worktree, with a brief of what the team decided and made (goal, decisions, handoffs, review comments, what its dependencies produced). The other agent reviews each result read-only; Hermes merges what passes once the user approves. In Hermes Desktop, Thoth docks a side window beside each project's chat (the live canvas, plus a Team & brain tab: who did what, and the shared record of decisions, reviews and versions), and every Thoth project is also a Hermes project on the same folder, so a project's chats stay in one place. A full Thoth page shows the canvas, board, outputs and versions. Claude Code or Codex can join the board through the bundled MCP server or take over as coordinator. A task that must look at the web gets a browser through Chrome DevTools MCP: a clean headless Chrome, or the user's own Chrome when it needs their logins. When a Claude or ChatGPT plan runs out, the other agent carries on from its work, and the Team card shows how much of each plan is used and when it resets. Because every agent keeps its own harness, what Anthropic, OpenAI and Nous ship to Claude Code, Codex and Hermes reaches the team without a change to Thoth.

Measured on one CRM built both ways (Codex GPT-6-Astra backend, Claude Code Opus 5.5 frontend): the builds took 35% less agent time and 26% fewer prompt tokens than relaying work by hand, and Codex's review of Claude's frontend caught two real bugs (numbers and caveats in the README). Built for the Hermes Agent Plugin Hackathon.

## Hermes surfaces
- 18 tools via `ctx.register_tool` (thoth_init, thoth_plan, thoth_assign, thoth_review, thoth_wait, thoth_status, thoth_note, thoth_merge, thoth_context, thoth_cancel, thoth_update_task, thoth_coordinator, thoth_complete, thoth_revise, thoth_restore, thoth_sync, thoth_models, thoth_preview).
- Hooks: `pre_tool_call` asks for approval (plain-language card) before every agent launch, review, revise, merge and any project setup/run command; `post_tool_call` clears the page's "waiting for your OK" banner when a call is rejected; `pre_llm_call` adds the board summary, how much of each agent's plan is used, and the coordinator's lane rules in Thoth projects.
- `ctx.inject_message` for completion notices, only with `plugins.entries.thoth.allow_gateway_injection: true`.
- `ctx.register_command` (`/thoth`), `ctx.register_cli_command` (`hermes thoth doctor`), `ctx.register_skill` (coordinator playbook).
- Desktop: `desktop/plugin.js`, SDK only (`@hermes/plugin-sdk` + `react`): the Thoth page and its sidebar entry, a status-bar chip, two panes (the side window docked beside the conversation, and Team & brain) and a "Chat + Thoth" layout template; chat and project calls go through the SDK's `host`. Dashboard API routes in `dashboard/plugin_api.py`.

## Disclosure (rule 13)
- **Agent processes:** after you approve each launch, runs your installed `claude -p` / `codex exec` as background processes under their own logins and plans (Thoth never reads, copies or passes their credentials). They talk to Anthropic/OpenAI and stop on cancel, timeout (30 min default), unload or Hermes exit.
- **Sandboxes:** Claude Code `--permission-mode acceptEdits` with its OS sandbox (writes confined to the task worktree and temp, no network); Codex `--sandbox workspace-write`; reviews read-only. Never passes skip-permission or bypass flags. Inside Codex runs, the run-scoped MCP server's three worker tools (read the board/brief, write a note) are pre-approved because `codex exec` cannot prompt; they cannot start agents or touch files.
- **Environment:** strips `*_API_KEY`, `*_TOKEN`, `*_SECRET`, `*_PASSWORD`, `HERMES_*`, `ANTHROPIC_*`, `OPENAI_*`, `CLAUDE_CODE_*`, `CODEX_*` (except `CODEX_HOME`) unless listed in `env_passthrough`.
- **Writes:** `.thoth/` in the project (SQLite brain, BRAIN.md, run logs with the agents' JSON output, worktrees, preview exports), branches `thoth/T<n>-…`, exact-path lines in `.git/info/exclude`, merge commits on the base branch only when you approve a merge, one empty initial commit in a repo with none; `chats.json` and `projects.json` (session ids and project paths only) and `plans.json` (plan usage numbers) in the plugin's data dir.
- **Hermes Desktop layout and chats:** adds two panes (the side window and Team & brain) and one layout template, Chat + Thoth, which changes your layout only when you pick it; closing a pane only hides it. The first time Thoth sends a project's request it opens a chat for that project, then pins it and gives it the project's colour, once. For each Thoth project it creates a Hermes project on that project's folder (or reuses yours) and moves the project's chat into it through Hermes's own project calls; other projects and chats are left alone.
- **Worktree setup:** links ignored `node_modules` / `.venv` / `venv` from the main checkout; a project setup command (approved by you) runs in each new worktree as you, with network. Never reads or copies `.env` files.
- **Previews:** a static, read-only file server on 127.0.0.1 (GET/HEAD, no hidden paths, max 8); with a project run command (approved by you), the app starts on a free localhost port from an export under `.thoth/previews/` (max 4, stopped on exit, leftovers stopped on next start).
- **Connect buttons** on the Desktop page run `claude mcp add thoth …` (project scope) or `codex mcp add thoth …` (Codex's global config) only when clicked.
- **Plan usage** (`plan_usage`, on by default): reads the plan usage Claude Code reports in each run's output, and asks Codex's own app server for Codex's limits (`codex app-server`, `account/rateLimits/read`, which uses no tokens) after Codex runs and at most every ten minutes while the Thoth page is open; both answer with their own logins. While a plan is out, Thoth won't start that agent and names the other one.
- **Web browsing (only for tasks given a browser):** the agent runs `npx -y chrome-devtools-mcp@1.2.0` (pinned; no dependencies of its own; fetched from npm on first use) with `--no-usage-statistics --no-performance-crux --redactNetworkHeaders`. Clean mode: headless Chrome with a temporary profile, deleted after the run. Your-Chrome mode (`--autoConnect`): only while the user has remote debugging on and after they allow the connection in Chrome's own prompt; the agent can see their tab titles and addresses and act with their logins, works in a tab of its own and is told to only look. The run's approval card says all of this, and an "always allow" for runs without a browser never covers runs with one. Reviews never browse.
- Thoth makes no network calls of its own (the pinned browser package above is fetched by npx when a task first browses, and Codex's limits are read by your own `codex` CLI), no telemetry, no self-updating code, no binaries.

## Validation
At the pinned commit: `hermes plugins validate --install-deps` passes with no warnings, both with Hermes `main` (a08f241, 7 Nov 2026, installed from its `uv.lock` the way this catalog's CI sets it up) and with the v0.23.0 release (security scan safe, desktop surface OK, no core override, capabilities match); `scripts/scan_plugin_payloads.py` finds no executable payloads; the self-update gate is clean; `scripts/validate_plugin_catalog.py` passes on the whole catalog with this entry; the plugin's 43 offline tests pass. Thoth reads `HERMES_SESSION_KEY` once per launch through `gateway.session_context.get_session_env` (`__init__.py:383`) to address the completion notice, and falls back silently; Hermes 0.22.5's validator listed that as a private core import, the current ones don't. Happy to move to a public seam if there is one.

## Screenshots
![side window beside the chat](https://raw.githubusercontent.com/cayden970207/thoth/bc5707377505aa92b808e78d6a0e88ad7f2e507e/docs/screenshots/side-window.png)
![overview](https://raw.githubusercontent.com/cayden970207/thoth/bc5707377505aa92b808e78d6a0e88ad7f2e507e/docs/screenshots/overview.png)
![cross-agent canvas](https://raw.githubusercontent.com/cayden970207/thoth/bc5707377505aa92b808e78d6a0e88ad7f2e507e/docs/screenshots/cross-agent-canvas.png)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Add cost-sentinel to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/149334
State: closed; created 2026-11-05T06:43:47Z

## What\n\nAdds  \u2014 my plugin **Cost Sentinel** (https://github.com/SongotenU/hermes-cost-sentinel at commit 969c7ea8d95617614cad31b912fe59419293f54b, v1.0.0). Also a Plugin Hackathon entry (same repo owner).\n\n## What the plugin does\n\nLive cost ledger + daily budget guarddog for Hermes Agent, **per profile or fleet-wide**:\n\n-  /  /  hooks price every call with **Hermes' own pricing engine** () and append rows into a per-profile SQLite ledger plus a **shared fleet ledger** at  (via the official  shared-root API) so all profiles of an install roll into ONE daily number.\n-  (status / set / block / warn / off / scope fleet|profile / resume / log / reset) and a  tool read the ledger; the  hook enforces the daily budget with the documented turn-level block () and an escape-hatch message ().\n- Desktop half ( + ): pane with a spend ring on the *gate* number (fleet or profile per scope), per-model/per-day breakdowns, live  pushes, status-bar budget chip.\n\nDifferentiator vs the listed cost plugins (hermes-telemetry blocks tool calls per profile, usage-guard gates per subscription-window, hermes-call-ledger is a Desktop ledger): the **daily-USD turn-level hard gate** scoped EITHER fleet-wide (all profiles share the ceiling) OR per profile.\n\n## Validate\n\n passes locally (manifest, declared tools/hooks match, desktop SDK surface, security scan safe, no core override). One \u26a0 caution \u2014 rule 9 private core imports: the plugin imports  for pricing and normalised usage buckets; it changes no host state via that seam, and I will happily move to a public seam if one gets opened (happy to file the issue).\n\n## Disclosure (rule 13)\n\n- Writes only the two SQLite ledgers (per-profile , shared  at the default Hermes root) and the settings row in the fleet DB.\n- No network of its own \u2014 pricing goes through the host pricing engine, which may fetch the host's usual public price books the way the host does (cached by the host).\n- No MCP, no shell, no credentials ( empty), no telemetry; per-call rows never store prompt, response or tool-argument text (tokens, cost, model/provider, session/turn/request ids, platform, error type/message).\n- The  gate is OFF by default (); blocking requires an explicit , and the block message itself carries the escape hatch ().\n

## feat(plugin-catalog): add lineage
https://github.com/NousResearch/hermes-agent/pull/149244
State: closed; created 2026-11-05T03:37:52Z

## lineage — provenance receipts and a graph for everything the agent produces

Adds `plugin-catalog/lineage.yaml` (community tier, `tools` category), pinned to `9a5c2ba` = tag `v0.1.1` of https://github.com/P0GL0L/hermes-lineage.

**What it does.** Every file Hermes writes gets a receipt — what it was made from (files read, pages fetched, searches run), by which tool call, model and agent, with SHA-256 hashes — and a Desktop page draws the graph from the file back to its sources. Links are labelled **observed** (Hermes reported it), **evidenced** (the artifact's own bytes name the source) or **inferred** (read earlier this turn / session, with confidence), never blended. `hermes lineage verify` reports fresh / stale / modified / missing; `hermes lineage check <file>.receipt.json` verifies a receipt with no database.

**Disclosure.** Hooks only — observer hooks only, deliberately no `pre_tool_call` (`post_tool_call`, `pre_llm_call`, `post_llm_call`, `post_api_request`, `api_request_error`, `post_auxiliary_call`, `subagent_start`, `subagent_stop`, `on_session_start`, `on_session_end`); no tools, no middleware, no LLM calls, no credentials; runs no commands. Reads files the agent wrote (hash up to 32 MB, text scan up to 512 KB) and stats the working tree once after `terminal`/`execute_code` calls (bounded by file count and time). Writes only under `<HERMES_HOME>/plugin-data/lineage/` (SQLite, `install.key`) and, on request or with `sidecar: true`, `<file>.receipt.json` beside files the agent produced. Stores redacted, bounded previews of prompts, tool arguments and results (`store_previews: false` keeps ids and hashes only); URL ids drop userinfo and mask credential-shaped query values. Network only on an explicit `verify --refetch` / *Verify + refetch URLs*: `GET` to the recorded source URLs, public hosts only (Hermes's `is_safe_url` when available). No telemetry.

**Validation.** `hermes plugins validate` passes every check on Hermes Agent v0.22.7 (macOS) — security scan *safe*, no core override, desktop surface inside the SDK. 17 pytest + Desktop (jsdom) tests in the repo; CI runs them and `hermes plugins validate` against Hermes main on every push.

**Desktop half.** `desktop/plugin.js` uses only `@hermes/plugin-sdk` and `react`; `dashboard/plugin_api.py` mounts under `/api/plugins/lineage/`. Under `plugins.isolation: host` the CLI subcommand is not wired (noted in the README); the slash command and Desktop backend still work.

Maintainer: P0GL0L (repository owner). Built for the Hermes Agent Plugin Hackathon, November 2026.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01F1DXuWjUkUGYSqHhtAutEe


## feat(plugin-catalog): add gemini-live plugin
https://github.com/NousResearch/hermes-agent/pull/150247
State: closed; created 2026-11-06T19:30:00Z

Hackathon entry. Adds `plugin-catalog/gemini-live.yaml`, pinned to a full commit SHA.

## What it does

Full-duplex Gemini Live calls in Hermes Desktop and the web dashboard. The voice takes the name of the profile the call started from, delegates real work to that agent, and keeps talking while it runs.

## How it differs from the listed Gemini plugins

This is an independent project, not a fork. `gemini-live-bridge` has no agent tools, and `hermes-gemini-live` centres on a delegation task board. This plugin adds thread, bot-chat and subagent monitoring and steering, MCP tools, memory and conversation search, a three-layer read-only command path, a dashboard tab, and personas.

## Disclosure

- **Network:** the client streams microphone audio to `generativelanguage.googleapis.com` on a single-use ephemeral token. The backend calls Google's Gemini API with the key.
- **Sent to Gemini:** audio, the voice's instructions, tool results and, unless `share_chat_context` is off, the open chat's title and latest messages. On Gemini's free tier, Google may use content to improve its products.
- **Reads outside its own data:** `profile.yaml` for the display name, built-in memory notes, session history, thread and profile lists.
- **Shell commands:** only with `readonly_shell` or `system_checks` on, both off by default, and only under the layers in the README.
- **Credentials:** read through `agent.secret_scope`; the browser never receives the key.
- **Approvals:** Hermes decides what needs asking. The plugin shows the request and passes on the user's answer through `approval.respond`, one time only. The voice model has no way to answer. The opt-in `voice_approval` setting accepts the user's own spoken approve or deny, matched on the microphone transcript and ignored while the voice speaks.
- **Background processes and telemetry:** none.

## Checks

`hermes plugins validate` passes on a fresh clone of the pinned commit (`06cdf904`): security scan safe, no core override, desktop surface inside the SDK. Plugin tests: 62 Python and 34 engine tests pass. Tested on macOS Hermes Desktop against a Linux backend.

## Companion change

An optional [Desktop PR](https://github.com/NousResearch/hermes-agent/pull/150248) adds a `composer.voiceEngines` area so plugins can appear in the voice picker. The plugin works without it.

## Open offer

We'd love Gemini Live as an option in the mobile voice picker. If the maintainers prefer, we're happy to contribute it to Hermes as a built-in voice engine next to GPT Live.

## Screenshots

![Approval on a call](https://raw.githubusercontent.com/cineglobe/hermes-gemini-live/06cdf904d1a346675f3cf7f54015f70fc7770d89/docs/assets/approval.png)

![Transcript](https://raw.githubusercontent.com/cineglobe/hermes-gemini-live/06cdf904d1a346675f3cf7f54015f70fc7770d89/docs/assets/transcript.png)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## feat(plugin-catalog): list SolverForge Planner
https://github.com/NousResearch/hermes-agent/pull/149647
State: open; created 2026-11-05T18:37:18Z

## What does this PR do?

Adds one catalog entry, `plugin-catalog/solverforge-planner.yaml`: **SolverForge Planner**, constraint-solved planning for Hermes.

<p align="center"><img src="https://raw.githubusercontent.com/blackopsrepl/hermes-solverforge-planner/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/docs/assets/mascot.png" alt="The SolverForge dragon taking the Nous Girl's hand" width="300"></p>

You tell Hermes what you need to get done. A [SolverForge](https://solverforge.org) engine fits each task into your free working time around your meetings, deadlines, task order and focus hours. It proves every hard rule holds before anything is written: a score of `0hard` means no meeting is hit and no deadline is missed. When a task cannot fit, you are told which one and what blocks it. Hermes explains the plan, you approve it, and it goes on your calendar.

- Repository: https://github.com/blackopsrepl/hermes-solverforge-planner, pinned at [`c6c4a5f`](https://github.com/blackopsrepl/hermes-solverforge-planner/tree/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9) (version 0.3.0 plus docs and the Tasks tab).
- Submitted by the repository owner, `blackopsrepl` (rule 5). I also maintain SolverForge, the solver the engine is built on.
- This is also my entry to the Hermes Agent plugin hackathon.

### Demo (84 s)

https://github.com/user-attachments/assets/c96958a7-59d6-4c03-a537-6a3b383c55ae

The middle of the video is a real Hermes Desktop session, sped up while the agent works, on a throwaway Google calendar with 14 meetings. Hermes pulls the calendar, the engine places four tasks around the meetings at `0hard/0medium/0soft`, the user approves, Hermes pushes the plan with the bundled google-workspace skill, and asking again adds nothing.

### Screenshots

The plan card in chat:

![The plan card in chat](https://raw.githubusercontent.com/blackopsrepl/hermes-solverforge-planner/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/docs/screenshots/chat-plan-card.png)

The Planner page, week view: the pulled calendar, the blocks on the plan, and the changes waiting to be pushed:

![The Planner page, week view](https://raw.githubusercontent.com/blackopsrepl/hermes-solverforge-planner/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/docs/screenshots/planner-page.png)

The Tasks tab: what waits for a plan, and what is on the calendar by day, with how old each pulled copy is:

![The Tasks tab](https://raw.githubusercontent.com/blackopsrepl/hermes-solverforge-planner/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/docs/screenshots/tasks-tab.png)

Apply asks first and lists every block:

![The Apply confirmation](https://raw.githubusercontent.com/blackopsrepl/hermes-solverforge-planner/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/docs/screenshots/apply-confirm.png)

### Architecture

![Architecture](https://raw.githubusercontent.com/blackopsrepl/hermes-solverforge-planner/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/docs/architecture.png)

- **Engine (Rust).** A stateless SolverForge model, run as `solverforge-planner solve` once per solve: JSON in on stdin, the plan out on stdout. Its domain and all 14 scoring rules come from [Planner123](https://github.com/blackopsrepl/Planner123). Scoring is incremental, and a test checks it against a full re-evaluation. A plan that breaks a hard rule is refused, not shown.
- **Plugin (Python).** Keeps the state in SQLite, translates between Hermes and the engine, gates every write and serves the Desktop half. It makes no scheduling decisions.
- **The planner's own calendar.** The plugin keeps a local calendar (the database plus a `planner.ics` any calendar app can subscribe to) and holds no calendar login and no provider code. Cloud calendars are optional. Hermes **pulls** them with the tool the user already has (the bundled google-workspace skill, or the microsoft365 plugin). On **push**, the plugin lists exactly which of its own events to create, move or delete, and Hermes carries that out. The next pull confirms it.
- **No duplicates, no foreign edits.** Every planner event has a fixed ID (`sfp` + 29 hex) and a marker in its description. A repeated push adds nothing, and the plugin only ever touches its own events. An event the user deletes in the cloud unschedules its task at the next pull.
- **Freshness is enforced.** Plan and push refuse a calendar copy older than 15 minutes. Apply checks the blocks against the latest pull.

## Hermes surfaces it uses

All public, nothing patched (rules 8 and 9; `no core override` and `desktop surface` both pass).

| Surface | What |
|---|---|
| `ctx.register_tool` | 15 `planner_*` tools in toolset `solverforge-planner` |
| `ctx.register_hook("pre_tool_call")` | Approval for `planner_apply` and `planner_task_unschedule`, scoped to the exact proposal or task (`rule_key`), so one "always allow" never covers a different write |
| `ctx.register_command` | `/planner` in any chat: status, install, inbox, plan, show, apply |
| `ctx.register_cli_command` | `hermes solverforge-planner install` / `status` |
| `ctx.register_skill` | `solverforge-planner:planner`, which tells the agent how to pull, plan, apply and push |
| `ctx.register_automation_blueprint` | Optional "Morning plan": pulls and solves on workdays and reports. It never applies. |
| Dashboard plugin API | `/api/plugins/solverforge-planner/*`, the Desktop half's backend |
| Desktop plugin SDK | `::planner{proposal="…"}` plan card (`TRANSCRIPT_DIRECTIVE_AREA`), Planner page (`ROUTES_AREA` + `SIDEBAR_NAV_AREA`), status-bar chip, two palette commands, live refresh through `ctx.onEvent`. It imports only `@hermes/plugin-sdk`, `react` and `react/jsx-runtime`. |

## Disclosure (rule 13)

- **One download, only when the user asks.** `hermes solverforge-planner install` (or `/planner install`, or the Desktop **Install engine** button, behind a confirmation) downloads `solverforge-planner-<platform>` (about 5 MB) from this repository's own [`engine-v0.1.0` release](https://github.com/blackopsrepl/hermes-solverforge-planner/releases/tag/engine-v0.1.0). It refuses the file unless its SHA-256 matches the value pinned in [`engine_bin.py`](https://github.com/blackopsrepl/hermes-solverforge-planner/blob/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/engine_bin.py) at the pinned commit. The agent has no tool that starts it.
- **One subprocess per solve.** The engine runs once per solve and is stopped at `solve_timeout` (default 120 s). It makes no network calls and reads and writes no files.
- **One network call the user starts.** `planner_busy_from_ics` fetches an https, http or webcal iCalendar link the user gives (up to 10 MB, must be iCalendar), or reads a local `.ics` file the user names. Nothing else is fetched.
- **No calendar access of its own.** The user's calendar is read and written by their own calendar tool, under that tool's login and disclosures, never by this plugin. The plugin never edits or deletes events it did not create.
- **Data.** Everything lives in `<hermes home>/plugin-data/solverforge-planner/`: the database, the engine, `planner.ics` and exported `.ics` files. Uninstalling keeps it, so a reinstall finds the tasks.
- **No credentials** read or stored, `requires_env` empty, **no telemetry**, **no background process**.
- **Writes need a person.** Agent writes to the plan go through Hermes's approval prompt (hook above). The Desktop's two writes, Apply and Install engine, are buttons behind a `ConfirmDialog`. Under cron the blueprint's prompt tells the agent not to apply, and the approval hook covers it anyway (rule 12).

## The native binary (rule 17)

Nothing compiled is committed: the pinned tree is source, docs and PNGs. The engine binary is built from `engine/` in this repository by its public [release workflow](https://github.com/blackopsrepl/hermes-solverforge-planner/blob/c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9/.github/workflows/release.yml), on five targets, with `actions/attest-build-provenance`. Checked here:

```
$ gh attestation verify solverforge-planner-x86_64-unknown-linux-musl --repo blackopsrepl/hermes-solverforge-planner
signer:  https://github.com/blackopsrepl/hermes-solverforge-planner/.github/workflows/release.yml@refs/tags/engine-v0.1.0
source:  06d05f7b3006cc2688023687c222b59d39742ff0  refs/tags/engine-v0.1.0
```

It is not a self-updater (rule 3). The engine version and every platform's SHA-256 are constants in `engine_bin.py` at the pinned commit, so an installed plugin can only fetch the exact binary the reviewed tree names. A new engine needs a new commit and a SHA-bump PR here. The plugin's own release workflow also checks the pinned checksums against the engine release's `SHA256SUMS` before publishing.

Python dependencies are bounded (rule 10): `icalendar>=6.1,<8` and `recurring-ical-events>=3.4,<4`.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Changes Made

- `plugin-catalog/solverforge-planner.yaml`: the entry. `tier: community`, `category: tools`, `sha: c6c4a5fa4f779a12706c1f34661a1b6dd7e04aa9`, `version: "0.3.0"`, `requires_hermes: ">=0.22.2"` (the same floor is in `plugin.yaml`). The banner, 4 screenshots and the architecture diagram are pinned to the same commit on `raw.githubusercontent.com`.

## How to Test

Run on openSUSE Leap 16.0 (x86_64) with Hermes v0.22.2, against a clean clone at the pinned commit:

```
$ hermes plugins validate ./hermes-solverforge-planner --install-deps
✓ manifest  ✓ manifest fields  ✓ requires_hermes  ✓ config schema  ✓ requires_env
✓ loadable — entry: __init__.py, desktop/plugin.js
✓ python dependencies  ✓ capability probe
✓ declared tools  ✓ declared hooks  ✓ declared middleware
✓ built-in tool collisions  ✓ security scan  ✓ no core override  ✓ desktop surface
Validation passed.

$ python3 scripts/validate_plugin_catalog.py plugin-catalog/solverforge-planner.yaml
OK: 1 file(s) valid
```

The repository's own gate (`make check`, also run in its CI on every push) passes at the pinned commit:

- **Engine:** rustfmt, clippy, and 44 Rust tests. Each hard rule has a unit test, incremental scoring is checked against full re-evaluation, and end-to-end tests drive the built binary: a week planned at `0hard/0medium` around an offsite and a busy day, a deadline kept, task order kept, an impossible task reported with its blocker.
- **Plugin:** 21 end-to-end Python tests through the real tool handlers and the real engine. They cover plan, apply and replan; stale proposals refused; pull and push with no duplicates across retries and dropped connections; moves and deletions made on the cloud calendar adopted; and the engine install refusing a wrong checksum.
- **Desktop:** 8 render tests of `desktop/plugin.js` against a stand-in SDK.
- **Validation:** `hermes plugins validate` and `hermes plugins doctor --ci` on the committed tree.

Live check against a real Google account (a throwaway calendar, with the google-workspace skill doing the reads and writes): pull, plan, apply, push, push again, move an event, delete an event. The plan avoided every existing event, the second push added nothing, the move and the deletion were picked up, and the pre-existing events were untouched.

To try it:

```sh
hermes plugins install solverforge-planner --enable
hermes solverforge-planner install
```

Then ask: *"Plan my next week. I work 9 to 6 Monday to Friday, Rome time. Finish the Q4 deck, about 4 hours, by Wednesday 6pm. Review Anna's PR, 1 hour, after the deck."*

## Checklist

- [x] One file added, under `plugin-catalog/` only
- [x] Full 40-character SHA pin; `version` quoted
- [x] `hermes plugins validate --install-deps` passes at the pinned commit, with no warnings
- [x] Declared capabilities match registrations (15 tools, 1 hook)
- [x] Rule 13 disclosures here and in the README ("What it downloads, runs and stores")
- [x] Screenshots for every UI surface


## feat(desktop): let plugins add engines to the voice picker
https://github.com/NousResearch/hermes-agent/pull/150248
State: closed; created 2026-11-06T19:30:05Z

Companion change for the **Gemini Live** plugin
([cineglobe/hermes-gemini-live](https://github.com/cineglobe/hermes-gemini-live)), submitted to the
Hermes plugin hackathon.

## Why

The composer's voice-engine picker offers *Speech-to-text + Hermes voice* and *GPT-Live*. A plugin
that ships its own realtime engine has nowhere to appear there, so it has to add a second call
button and users have two different "talk" buttons. The plugin SDK has no seam for this, and a
catalog plugin may not edit core files.

## What

- A new data area, `COMPOSER_AREAS.voiceEngines` (`composer.voiceEngines`), with payload
  `ComposerVoiceEngine { label, shortLabel, detail?, start() }`. It is exported from
  `@hermes/plugin-sdk` like the other composer areas.
- `VoiceEngineRows` lists the registered plugin engines after the core rows. Picking one is a
  **renderer-side** choice (`store/plugin-voice-engine.ts`), persisted per (connection, profile)
  with the same scope key as `$voiceLiveStatus`. Picking a core row clears it and writes
  `voice.voice_chat_mode` exactly as before. The backend keeps refusing unknown modes (4002) and is
  untouched.
- The start-voice button and the folded voice menu call the chosen plugin's `start()`. If that
  plugin is no longer registered, the button falls back to the core engine. If `start()` throws,
  the error shows and the core engine starts, so a broken plugin can't swallow the click.
- Malformed payloads (no `start`, blank labels, duplicate ids) are dropped, so a broken plugin
  can't blank the picker or add a row that does nothing.

There are no new strings, because labels come from the plugin. There is no backend change, and
nothing changes for users without such a plugin.

## Tests

`src/app/chat/composer/voice-engines.test.ts` covers payload validation and ordering, per-scope
persistence, fallback when the plugin is gone, and clearing back to the core engine.

## Mobile

The mobile app's voice picker currently offers only GPT Live, and its source isn't public, so this
patch can't cover it. **We'd love an installed Gemini Live plugin to appear as an option in the mobile
picker too, so people can choose it as their voice engine on any device.** The
plugin's backend already serves everything a client needs:

- `POST /api/plugins/gemini-live/session` returns a single-use ephemeral token with the model,
  voice, instructions and tools locked server-side. The key never leaves the backend.
- `POST /api/plugins/gemini-live/tool` runs the server-side tools.
- `src/engine.js` is the framework-free call engine (audio, socket, tool router, delegation) that a
  mobile client can port directly.

## Open offer

If the maintainers would like it, we're happy to contribute Gemini Live to Hermes as a **built-in**
voice engine everywhere, next to GPT Live: the backend, Desktop, the dashboard, and help with
mobile. That would include the multi-layer `run_readonly` safety design and the thread/bot
monitoring tools. Tell us which shape you'd prefer.

## Testing status

The patch applies cleanly to current `main`. I haven't run the Desktop test suite or a Desktop build on this branch, so CI will be the first full run. The plugin works without this change: it falls back to its own composer button.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Add cash-desk to the plugin catalog
https://github.com/NousResearch/hermes-agent/pull/150374
State: open; created 2026-11-07T00:33:07Z

**Demo video (under 90 s):** https://www.youtube.com/watch?v=EOggmibecGI

# Add cash-desk to the plugin catalog

Adds one file, `plugin-catalog/cash-desk.yaml`, pinning
[FutureInvoked/cash-desk](https://github.com/FutureInvoked/cash-desk) at `26d5fabe5f50f250e5dc72c0751adbdb3625f732` (tag `v1.2.0`).
Submitted by the maintainer (FutureInvoked) for the Hermes Agent Plugin Hackathon.

Cash Desk chases overdue invoices. It reads the CSV exports a small business already has
(a generic invoice list or the Xero, QuickBooks or Stripe export, plus the bank statement),
applies a payment only when its reference and amount match one invoice exactly, drafts
reminders that get firmer at 7, 14, 21 and 28 days overdue, and sends one only after a
person has approved its exact text and Hermes has asked once more. **The model writes the
words; the ledger owns the numbers.**

## Why this is not a prompt

A prompt or a skill can ask the model to be careful. Cash Desk enforces it with things the
model cannot write or skip:

- **Figure Lock.** Reword surrounding prose while keeping drafted financial lines intact.
  Invoice rows preserve invoice/amount/date/reference relationships; totals and bank details
  retain their wording and figures. Whole rows may be reordered and whitespace may change.
  Added financial lines (including a gross-amount demand) and cross-invoice swaps are rejected.
  Storage, approval and send reservation recheck the saved baseline; older drafts without
  one must be regenerated. This deliberately restricts financial prose instead of claiming
  to understand arbitrary wording. Recognized figures still receive the original ledger check.
  It may not add a link, an email address, a percentage, or wording from a list of known payee,
  deadline, legal, settlement, interest, credit-reporting or suspension phrases either (a list,
  not a guarantee; the person reading the exact text is the final check) (a "pay here" link or "8% interest" is refused the same way).
  Measured: 74 of 74 single-digit edits to the demo drafts' figures are caught; with revision and storage checks
  switched off the same run reports 74 misses (`tests/plugin/test_mutations.py`).
- **Approval bound to the exact text.** A person approves a draft on the Desktop page or with
  `/cashdesk approve`; the approval is tied to a SHA-256 of the subject, recipients and body. Any
  change drops it, a stale hash is refused, and at send time the stored text is re-hashed
  (a text changed in the ledger file without its approval being rewritten is refused). At
  approval and again at send reservation, every invoice's open balance, currency, due date,
  customer, IBAN and payment reference are checked against its stored basis. The same
  current hold rules used by planning also apply: promises, payment-review and ready-to-match
  holds on the invoice, missing
  open-export invoices and open credits attached to the customer revoke old approvals.
  The old text remains visible with a warning; resolving the reason never restores its
  approval. A replacement must be drafted, read and approved. Older ledgers whose unsent
  drafts have no recorded payment-instruction basis require the same fresh-draft process.
- **Hermes's own approval gate on every send.** `pre_tool_call` escalates every `cashdesk_send`
  to Hermes's approval prompt with the rule key `cashdesk:send:<hash>`, so approving one draft
  never approves another; the prompt names the reminder, customer, recipient, total and text
  hash. Cash Desk refuses to send where Hermes would pass that prompt by itself (approvals
  off, `HERMES_YOLO_MODE`, or `approve` for single-query, cron or unattended runs). Verified live from Telegram: the approval buttons came to the chat,
  one tap sent the reminder, an untapped prompt timed out after 60 s and nothing was sent.
- **Conservative automatic matching.** A payment is applied automatically only on an
  exact reference and amount (one invoice, or several of one customer adding up to the cent) with a normalized payer name fitting only that known customer
  (or a bounded unique bank-name truncation), and a booking date no more than three days
  before invoice issue. A statement with no payer column counts only when its description names
  exactly one customer in full. Missing, similar, shared-word or ambiguous names require review.
  Fuzzy name scores rank suggestions only; non-Latin identity is preserved. Everything else waits for a person, who applies it (all or part) or dismisses it on
  the Desktop page or with `/cashdesk apply` / `dismiss`; the model has no tool for that. A
  newer invoice export never undoes a payment Cash Desk already applied.
- **No writes where no person is present.** Every writing tool is blocked inside a scheduled
  run, when Hermes cannot say whether the run is scheduled, and inside delegated subagents
  (tracked with the public `subagent_start`/`subagent_stop` hooks). Sending is refused when
  `approvals.mode` is off.
- **Optional: the agent's own replies are checked too.** With `guard_outgoing_messages` on, a
  `transform_llm_output` hook withholds a chat reply that quotes an amount, IBAN or invoice
  number the ledger does not hold for that customer, before Hermes stores or delivers it.

Every refusal is listed in [docs/refusals.md](https://github.com/FutureInvoked/cash-desk/blob/main/docs/refusals.md)
with its exact message and the test that checks it; a test fails if that table and the code
drift apart.

**Built so a bookkeeper can trust it.** Cash Desk would rather pause an invoice and ask than
chase someone who paid. It holds an invoice while a receipt in review names the customer, while
a pending bank payment for it is on its way, while a promise (including Xero's expected payment
date) is running, when the latest export no longer lists it, or when it looks like one debt
imported twice. Each pause says why and which command clears it.

**How it was tested before submitting.** Repeated independent judge-style reviews and
bookkeeper stress tests fed it hundreds of files laid out like real Xero, QuickBooks Online and
Stripe exports and bank statements (line-item rows, report title rows, credit memos and credited
amounts, debit/credit, direction and status columns, pending lines, US and EU dates). Every wrong
result they found is now a test: the suite has over 2,000. The README demo prompt, run three
times through the live agent on a fresh ledger, gave the same 2 payments applied, 1 for review
and 6 drafts each time.

## Surfaces

| Surface | What |
|---|---|
| Tools (toolset `cashdesk`) | read-only: `cashdesk_status`, `cashdesk_brief`, `cashdesk_queue`; writing: `cashdesk_import`, `cashdesk_match`, `cashdesk_draft`, `cashdesk_revise`, `cashdesk_reply`, `cashdesk_hold`, `cashdesk_send` |
| Hooks | `pre_tool_call` (gate), `subagent_start`, `subagent_stop`, `transform_llm_output` (opt-in reply check; holds the stream only when on) |
| Command | `/cashdesk` with `help`, `status`, `queue`, `approve`, `reject`, `review`, `apply`, `dismiss`, `hold`, `release`, plus the check commands Cash Desk names when it pauses an invoice (`/cashdesk help` lists them). Approving, rejecting, releasing and placing a payment exist only here and on the Desktop page |
| Blueprint | `cash-desk:morning-brief` on the Scheduled jobs page (time, weekdays, language, delivery target) |
| Desktop | a Cash Desk page (open balance by age, approval queue with the exact text and hash, payments to review with Apply / Dismiss, customers on hold, activity, Load demo data) and a status-bar chip; backend routes under `/api/plugins/cash-desk/` |

`requires_hermes: ">=0.22.6"` (the reply check registers `transform_llm_output` with
`hold_stream`, first in 0.22.6; everything else exists from 0.22.5). No Python dependencies.

## Disclosures (rule 13)

- **Files read:** its own state folder `plugin-data/cash-desk/` (per profile), the bundled
  `demo/` folder, and CSV files inside folders you list in `import_dirs`; any other path is
  refused before it is opened, after resolving `..` and symlinks. It also reads Hermes's `config.yaml`
  (read-only) to check that approvals are on before any send.
- **Files written:** `plugin-data/cash-desk/cashdesk.sqlite` (the ledger) and, in the default
  `eml` send mode, one `.eml` file per approved send in `plugin-data/cash-desk/outbox/`
  (or `eml_outbox`).
- **Network:** none by default. SMTP is opt-in (`send_mode: smtp`) and talks only to your own
  server; the password is `CASHDESK_SMTP_PASSWORD`, read only through `agent.secret_scope`;
  the certificate is always verified (an optional `smtp_ca_file` names a company or test
  server's certificate; it never disables the check).
- **Background work:** none. The morning brief runs only if you schedule it, and in a
  scheduled run every writing tool is blocked.
- **Approvals:** never auto-approves; refuses to send when Hermes approvals are off.
- **Reply check (opt-in, off by default):** when on, reads each agent reply in that profile in
  memory to check its figures and holds the reply stream until the check is done.
- **Data:** demo data only in the repository (`.example` domains, public example IBANs).

## Screenshots

| | |
|---|---|
| ![Approval queue](https://raw.githubusercontent.com/FutureInvoked/cash-desk/26d5fabe5f50f250e5dc72c0751adbdb3625f732/docs/screenshots/desktop-queue.png) | ![Figure Lock diff](https://raw.githubusercontent.com/FutureInvoked/cash-desk/26d5fabe5f50f250e5dc72c0751adbdb3625f732/docs/screenshots/figure-lock-diff.png) |
| Approval queue: the exact text, five ledger figures, the hash | Figure Lock rejecting a changed amount and a foreign IBAN |
| ![Send approved on Telegram](https://raw.githubusercontent.com/FutureInvoked/cash-desk/26d5fabe5f50f250e5dc72c0751adbdb3625f732/docs/screenshots/send-gate.png) | ![Payments to review](https://raw.githubusercontent.com/FutureInvoked/cash-desk/26d5fabe5f50f250e5dc72c0751adbdb3625f732/docs/screenshots/match-review.png) |
| A send approved from Telegram through Hermes's gate | Payments that wait for a person; activity in plain sentences |
| ![Morning brief](https://raw.githubusercontent.com/FutureInvoked/cash-desk/26d5fabe5f50f250e5dc72c0751adbdb3625f732/docs/screenshots/morning-brief.png) | ![Send result](https://raw.githubusercontent.com/FutureInvoked/cash-desk/26d5fabe5f50f250e5dc72c0751adbdb3625f732/docs/screenshots/send-result.png) |
| The morning brief | The result after the send (SMTP to a test server) |

## Checks at the pinned sha

```text
$ hermes plugins validate . --install-deps
...
Validation passed.            # 0 warnings

$ hermes plugins doctor --ci .
  manifest: cash-desk 1.2.0 (standalone)
  OK: runtime discovery, manifest parsing, import, and registration passed
  registrations: 10 tool(s), 4 hook(s)

$ python -m pytest -q     # Python 3.11 and 3.12, also in the repository's CI
2263 passed, 1 warning    # both versions, at the pinned sha
```

## What is new in 1.2.0

- Drafts are written for today only, and matching never runs for a future date, so the agent
  cannot date a reminder into a harsher stage or apply money that has not arrived.
- A reminder sent more than six days after it was written is refused and redrafted, so its
  "N days overdue" is never ahead of the truth and at most six days behind it.
- Pauses instead of guesses: receipts that name the customer, pending payments, Xero expected
  payment dates and "Not sent" invoices, invoices the latest export leaves out, one debt imported
  twice, a receipt the export already counts, returned payments and blank or unread balance,
  direction and status columns.
- Reads more of what real exports contain: Xero amount credited, more balance column names,
  Sparkasse pending lines, debit/credit in a Type column.
- Figure Lock also refuses an added payee, deadline or credit-reporting threat.
- `/cashdesk help` and `/cashdesk show`; a plain-language README with details in `docs/`.

## Try it

```bash
hermes plugins install FutureInvoked/cash-desk --enable
hermes gateway restart
```

Then in a chat: "Load the Cash Desk demo and draft today's reminders, signed by Example
Studio Ltd." The demo's dates move to the day you load it, so every "N days overdue" is true.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: add hermes-axioma
https://github.com/NousResearch/hermes-agent/pull/149364
State: closed; created 2026-11-05T08:20:32Z

Adds `plugin-catalog/hermes-axioma.yaml` (one file).

**Repo:** https://github.com/percyhendrux123-prog/hermes-axioma, pinned at `66b40e6c802c8b11da961b742b01dd0d958333bd` (v0.2.0, MIT). Submitted by the repository owner.

## What it does

The agent writes its normal reply and marks the few phrases that should change the reader's decision: **stop**, **caution**, **go**, or a quiet **whisper** for a second look. Axioma renders each mark for the surface it lands on, always as color plus a style cue plus a word, never color alone:

| Surface | Rendering |
|---|---|
| Hermes Desktop | KaTeX `\color` inline span + the word as plain text |
| CLI / TUI | 24-bit ANSI color + bold/underline/italic + the word; resets only the styles it set |
| Telegram, Discord, Slack | **bold** + the word |
| SMS, iMessage, email, unknown | the word only |

- **Green is earned, not claimed.** `go` renders only when a tool call Hermes reported as `ok` in this session backs it (`post_tool_call` observer). Otherwise it renders plain and is logged.
- **Rare by design.** A rarity budget (3 signals, 2 whispers, 16 words per span by default); over-budget spans render plain and are logged.
- **Accessibility first.** The word is on by default everywhere. `palette: cvd` keeps every stop/caution/go pair at CIEDE2000 >= 12 under protan/deutan/tritan simulation; `palette: none` (or `NO_COLOR`) gives style and words only.
- **Malformed tags never leak** (unclosed, nested, mismatched, cut-off by streaming), and tags inside code are left alone.
- **Advisory card (secondary).** `axioma_card` stages intent / light / signal / question for one exact upcoming send, spend, spin or scrub call; `pre_tool_call` returns only the documented `approve` directive so the card appears inside Hermes's own approval prompt. Every card uses a fresh rule key, so a remembered approval never covers a later call.

**Advisor, not a gate.** It never returns `block`, never auto-approves, never changes another guard. Hermes's approval system and the human decide.

## Hermes surfaces used

- Tool: `axioma_card` (toolset `axioma`); no core tool overridden.
- Hooks: `pre_tool_call`, `post_tool_call`, `post_approval_response`, `pre_llm_call` (short markup guide as context), `on_session_finalize`, `transform_llm_output` (rendering).
- Commands: `/signals`, `/whispers` (list every flag in the session; nothing is hidden).
- Middleware: none. No monkeypatches, no private approval probes, no Desktop plugin.
- Imports: `plugins.plugin_storage.plugin_data_dir`; `agent.secret_scope.get_secret` (presence check only, for an optional provider-conflict check).

## Disclosures (rule 13)

- **Network / model calls:** none.
- **Shell / subprocesses / background processes / threads:** none (two in-process locks only).
- **Reads outside its own data:** none. No `.env`, `auth.json`, keychain or credential store access.
- **Writes:** flag metadata and salted hashes of whispered spans (no message bodies) to SQLite under `plugin-data/hermes-axioma`.
- **Context:** `pre_llm_call` adds a short markup guide to every turn (a few hundred tokens).
- **Telemetry / self-update:** none.
- **Validator cautions (kept visible, not evaded):** `destructive_root_rm` / `destructive_home_rm` on destructive-command *strings* in classification tests and captured test output under `docs/evidence/`, and `invisible_unicode` where tests check that tags never hide behind zero-width or bidi characters. None is executed.

## Verification at the pinned SHA (fresh clone)

- `hermes plugins validate . --install-deps` -> **Validation passed** (Hermes v0.22.7)
- `python3 -m unittest discover -s tests` -> 200 tests OK (12 host-only skipped); `hermes --run-module unittest discover` -> 200 OK

## Screenshots

Desktop (night theme), real chat:

![Desktop](https://raw.githubusercontent.com/percyhendrux123-prog/hermes-axioma/66b40e6c802c8b11da961b742b01dd0d958333bd/docs/evidence/desktop/desktop-night-inline-signal.png)

CLI: dark, light, color-vision-safe and NO_COLOR:

![CLI](https://raw.githubusercontent.com/percyhendrux123-prog/hermes-axioma/66b40e6c802c8b11da961b742b01dd0d958333bd/docs/evidence/desktop/terminal-app-cli-render.png)

Known limits are listed in the entry's `known_issues` and in `docs/HOST-GAPS.md`.

Entry for the Hermes Agent Plugin Hackathon.


## feat(plugin-catalog): add flightlog plugin
https://github.com/NousResearch/hermes-agent/pull/149499
State: closed; created 2026-11-05T13:32:24Z

## What does this PR do?

Adds `plugin-catalog/flightlog.yaml` for **Flightlog** ([piyushpradhan/flightlog](https://github.com/piyushpradhan/flightlog)), submitted for the Hermes Agent Plugin Hackathon. I own the repository.

Hermes cron already catches runs that crash. Flightlog catches the ones that finish green and still did the wrong thing. It records every tool call, model call, subagent and approval to local SQLite, then checks each finished run:

- **Said done, but a step failed**: a tool errored or a command exited non-zero, and the answer never mentions it.
- **Claimed it works, but never proved it**: files were edited, the answer says "fixed / tests pass", and no test or build ran after the last edit, or the last one failed.
- **Stuck in a loop**: the same tool with near-identical arguments, 5+ times.
- **A helper failed, the parent said done**: a subagent stopped as failed under a successful run.
- **Cost far above normal / Did far less work than usual / Answered without doing any work**: compared against that cron job's own last healthy runs.

Flagged runs get a footer on the reply, a 2–3 sentence incident report from the user's own model, and a step-by-step timeline (`/flightlog why <run>`, `hermes flightlog show`, a dashboard tab, and a desktop page). An opt-in tripwire hands the 5th repeated tool call to Hermes's own approval prompt. `hermes flightlog ack <id>` silences a rule for a job.

## Type of Change

- [x] ✨ New feature (catalog entry only)

## Changes Made

- `plugin-catalog/flightlog.yaml`: pinned to `c201d602219f6890c380954c1229692e6bfc3f44`, `version: "0.1.0"`, `requires_hermes: ">=0.21"`, with a disclosure line.

## Disclosure

- Local only: no network calls, no subprocesses, no monkeypatching, no background services beyond one in-process SQLite writer thread.
- Data lives in `$HERMES_HOME/flightlog/flightlog.db`, per profile. Previews are capped at 200 characters, passed through Hermes's secret redaction, and pruned after 30 days.
- For flagged runs only, the redacted evidence goes to the user's configured model via `ctx.llm.complete` to write the incident report.
- It appends a footer to agent replies when a run is flagged. With `break_silence` (on by default), a flagged `[SILENT]` cron job posts a note.
- The tripwire is off by default. When on, it returns `approve` so Hermes's own approval gate decides. It never blocks on its own, and unattended runs fail closed on the approval timeout.

## How to Test

1. `python scripts/validate_plugin_catalog.py plugin-catalog/flightlog.yaml` → `OK: 1 file(s) valid`
2. `hermes plugins validate <clone at c201d60> --install-deps` → `Validation passed.` (security scan: safe). One warning: private core imports of `agent.redact`, `agent.usage_pricing` and `cron.jobs`. All three are inside try/except and degrade gracefully (a built-in redaction fallback, no cost figure, no job name). I'm happy to switch to public seams if they exist.
3. `python3 tests/test_flightlog.py` → 15 passed: planted fixtures for each rule, 20 clean replays, end-to-end cron, `[SILENT]` and `[CRON_FAILURE]`, fail-open on garbage input, and p95 hook latency under 5 ms with 50 KB arguments.
4. `hermes plugins install piyushpradhan/flightlog --enable`, then ask the agent to edit a file and claim the tests pass without running them. The reply ends with a Flightlog footer.

## Desktop evidence

Captured with Computer Use on macOS in Hermes v0.22.7+433. A live bill-splitting repair started two review helpers that failed with provider errors; Flightlog flagged the successful parent run. The follow-up that disclosed the failures is shown with no findings.

![Live flagged run](https://raw.githubusercontent.com/piyushpradhan/flightlog/c201d602219f6890c380954c1229692e6bfc3f44/docs/screenshots/flagged-run.png)

![Failed helpers in the timeline](https://raw.githubusercontent.com/piyushpradhan/flightlog/c201d602219f6890c380954c1229692e6bfc3f44/docs/screenshots/failed-helpers.png)

![Follow-up with no findings](https://raw.githubusercontent.com/piyushpradhan/flightlog/c201d602219f6890c380954c1229692e6bfc3f44/docs/screenshots/healthy-run.png)

## Checklist

- [x] Conventional Commits
- [x] Searched existing PRs and entries; no `flightlog` entry
- [x] Only the catalog entry
- [x] No credentials needed; no core overrides; declared hooks match registrations; risky behaviour disclosed; no binaries
- [x] Tested on macOS (Hermes v0.22.7)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## feat(catalog): add undo-effects plugin
https://github.com/NousResearch/hermes-agent/pull/149148
State: closed; created 2026-11-04T23:15:56Z

Add community entry: `undo-effects` (Hermes Agent Plugin Hackathon entry)

## What it is
`undo-effects` puts back files an agent deleted or overwrote. A `tool_execution` middleware snapshots the files that a
`write_file`, `patch` or destructive `terminal` command is about to change (`rm`, `rmdir`, `unlink`, `mv`, `cp`, `>`/`>>`,
`tee`, `sed -i`, `truncate`, `dd of=`, `find -delete`), then runs the tool unchanged. `/undo-effects` (and
`hermes undo-effects`) lists the effects and restores them.

- A restore refuses to overwrite anything edited after the agent's change unless `--force` is given, never deletes
  content it could not snapshot, and keeps a safety copy of what it replaces, so a restore can itself be undone.
- Commands it cannot analyse (`git clean`, `git reset --hard`, `find -exec`, heredocs, command substitution, PowerShell, ...)
  are shown in the timeline as "not covered" instead of being silently ignored.
- It works outside Git and does not need a repository.

Repo: https://github.com/Moodtuner997/hermes-undo-effects (version 0.1.0, MIT, Python standard library only, pinned to
`f02de8ca69104f44b9b3ec78155d7152412b9e97`).

## Hermes surfaces used
`ctx.register_middleware("tool_execution")`, `ctx.register_command`, `ctx.register_cli_command`, `ctx.get_config` with a
`config_schema`. No hooks, no tools, no core overrides. Two guarded imports with fallbacks: `hermes_constants.get_hermes_home`
and `agent.runtime_cwd.resolve_agent_cwd`.

## Disclosure (rule 13)
- **Network:** none.
- **Reads outside the plugin's own data:** the contents and metadata of the files and directories a covered tool call is about
  to change.
- **Writes:** unencrypted copies of those files under `HERMES_HOME/plugin-data/undo-effects/`. Credential-looking names
  (`.env`, `*.pem`, `id_*`, `auth.json`, ...), files above 50 MB, `node_modules`, `.venv` and `.git` are skipped and reported.
- **Shell commands, background processes, stored credentials:** none. Commands are parsed, never executed.
- **Approvals (rule 12):** the plugin never blocks, rewrites or approves a call; Hermes' approval gate and guardrails see the
  model's original arguments. If a snapshot fails, the tool runs anyway and a warning is logged.
- **Terminal backends:** local only. With a remote `TERMINAL_ENV` the plugin does nothing (`/undo-effects doctor` warns).
- **Telemetry:** none.

## How it differs from existing entries
`git-autosave` backs up Git working trees to shadow refs, is restored with its own CLI, observes only and lists Linux and
macOS; `agent-ledger` journals side effects without restoring them. `undo-effects` is not tied to Git, snapshots at execution
time through the middleware seam, restores from the session, protects later edits, makes restores reversible and reports what
it could not cover. They compose.

## Validation
- `hermes plugins validate` passes on a fresh clone at the pinned SHA, on Hermes 0.22.7, on Linux (arm64) and native Windows 11.
- `scripts/validate_plugin_catalog.py` passes on this entry.
- 45 unit tests; `tests/e2e_hermes.py` sends real tool calls through `model_tools.handle_function_call` (no LLM) and
  restores a deleted file, an overwritten file, a renamed file and a deleted directory byte for byte, on Linux and Windows.
- One real agent turn on Windows (Claude through `claude-subscription-directsdk`): the model deleted a folder and a file with
  the terminal tool; `hermes undo-effects restore` put both back.
- `platforms` lists what was tested; macOS is untested. There is no UI, so no screenshots; example output is in the README.

## Notes for maintainers (observed on 0.22.7; neither affects this plugin)
1. `hermes plugins validate` fails with "undeclared middleware registered (not in provides_middleware)" when `plugin.yaml`
   omits `provides_middleware`, while the plugin loader logs "unknown manifest field(s) ignored: provides_middleware".
2. `middleware.md` ("Tool Calls") lists approval checks before `tool_execution`. A probe plugin logged this order for a
   `terminal` call through `handle_function_call`: `tool_request`, `pre_tool_call`, `tool_execution` (enter), the terminal
   approval gate (`check_all_command_guards`), `tool_execution` (exit). The terminal's approval gate therefore runs inside
   `tool_execution`, and a `tool_execution` middleware that skips `next_call` would skip it as well.
Happy to open issues for both.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## plugin-catalog: add basekit — read-only live Base (8453) intelligence
https://github.com/NousResearch/hermes-agent/pull/149166
State: closed; created 2026-11-05T00:28:09Z

## What this is

**basekit** — read-only live Base (chain 8453) intelligence for Hermes. Six agent tools,
a `pre_llm_call` context injection, a `/basekit` slash command, a `hermes basekit` CLI
command, a bundled skill, a desktop pane + status-bar chip + palette/keybind entries, and
a FastAPI backend. It is an entry in the Hermes Agent Plugin Hackathon.

Repo: https://github.com/D0xedDevi0/hermes-basekit (public, MIT)
Pinned commit: `142bd48ea7755bda6a7c2aff707106bdfbf25ee6` (v1.0.0)
Catalog card: [`docs/banner.png`](https://raw.githubusercontent.com/D0xedDevi0/hermes-basekit/142bd48ea7755bda6a7c2aff707106bdfbf25ee6/docs/banner.png) plus four screenshots (status, wallet, token, hook gate), all
rendered from captured command output — provenance in `docs/screenshots/CAPTURE.md`
Hook evidence: [`docs/hook-proof.md`](https://github.com/D0xedDevi0/hermes-basekit/blob/main/docs/hook-proof.md) - the gate called directly, the injected string, and an A/B that is reported at the strength the measurement supports: 2.40 vs 2.80 model calls on one question and 2.33 vs 2.00 on another (inside noise), so the doc corrects its own earlier claim rather than keeping it. Generated from captured JSON.

## Hermes surfaces used

| Surface | Use |
| --- | --- |
| `ctx.register_tool` | `base_network`, `base_portfolio`, `base_tx`, `base_token`, `base_activity`, `base_allowances` |
| `pre_llm_call` hook | injects one cached line of live chain state **only** on Base-related turns (block, gas, ETH price, transfer cost) — can be switched off in settings |
| `ctx.register_command` | `/basekit` |
| `ctx.register_cli_command` | `hermes basekit` |
| `ctx.register_skill` | bundled `basekit` skill (the honesty rules the model works to) |
| Desktop SDK | `PANES_AREA`, `STATUSBAR_AREAS`, `PALETTE_AREA`, `KEYBINDS_AREA`, `ROUTES_AREA`, `SIDEBAR_NAV_AREA`, `useQuery`, `Tip`, `StatusDot` — no `eval`, no `import()` outside the SDK, no prototype patching, no core markup access |
| `dashboard/manifest.json` + `dashboard/plugin_api.py` | read-only HTTP routes and an `/events` socket |

No runtime overrides of core, no private core imports — `hermes plugins validate`
reports `no core override` ✓ and `desktop surface` ✓ clean (an earlier build imported
`hermes_cli.web_server_chat`; that was removed in favour of the host's own
`PluginApiWebSocketGate`, which already applies the core Host/Origin/peer check to every
plugin socket).

## Disclosure (rule 13)

- **Outbound HTTPS only**, to a fixed set of hosts, with no other egress:
  - Base JSON-RPC: `mainnet.base.org`, `base-rpc.publicnode.com`, `base.drpc.org`,
    `base.meowrpc.com` (failover across these; the tool reports which one answered).
  - Prices: `coins.llama.fi` (DefiLlama, keyless) and `api.coinbase.com` (spot fallback).
  - `api.etherscan.io`, **only** when the user sets the optional `basescan_api_key`, and
    only for the source-verification field of `base_token`.
- **Reads:** public chain data and the price APIs above. Nothing else. No files outside
  its own data directory, no shell commands, no background processes, no telemetry, no
  analytics, no usage reporting.
- **Writes:** one local JSONL read-ledger (which tool queried what, when) under
  `<HERMES_HOME>/plugin-data/basekit/`, which feeds the desktop pane's recent list.
- **Credentials:** the optional Basescan key is read via `agent.secret_scope.get_secret`
  (rule 11 route) — never `.env`, `auth.json`, a keychain or any other store. No OAuth,
  no `requires_env` entries; basekit holds no credential of its own.
- **No signing, no transactions, no approvals, no key material.** This is architectural
  rather than promised: there is no signer in the package, and an offline test fails the
  build if a write/sign RPC method name (`eth_sendRawTransaction`, `personal_sign`, …)
  ever appears in the core.

## Why it should be trustworthy, not just plausible

The design rules the plugin enforces on itself (and documents in its README and bundled
skill):

1. Every answer carries its block number — chain state is a moving target.
2. Windowed queries state the window they read (`from_block`, `to_block`, `blocks`,
   `narrowed`). "No transfers in the last 190 blocks" is true; "this wallet never received
   USDC" is not, and the tools say the former.
3. Unpriced tokens return `value_usd: null`, never a guess. A value that wasn't read is
   absent, not defaulted.
4. A rejected `eth_getLogs` raises; it never returns `[]`, because `[]` reads as "nothing
   happened" — a false claim about the chain.
5. No rug/honeypot scoring: bytecode flags are labelled as selector-presence heuristics,
   and basekit deliberately does not issue a verdict it cannot back with simulation.

Public-endpoint reality is handled rather than hidden: `eth_getLogs` needs an address
filter and a narrow range (a 200-block USDC query is rejected with *"query exceeds max
results 20000"*), so the client half-narrows the window toward the head automatically and
reports `window.narrowed: true`.

## Evidence

```
hermes plugins validate . --install-deps   →  Validation passed  (16/16 checks)
hermes plugins doctor .                    →  import + registration OK: 6 tool(s), 1 hook(s)
python3 tests/test_core.py                 →  66 tests  OK
python3 tests/test_plugin_surface.py       →  30 tests  OK
python3 tests/test_desktop_plugin.py       →  10 tests  OK   (executes the desktop half
                                               in Node against a stub SDK, rather than
                                               trusting it; it caught a ReferenceError at
                                               registration that would have shipped)
BASEKIT_LIVE=1 python3 tests/test_live.py  →   8 tests  OK   against Base mainnet
```

Live values from the last run (structure asserted, not pinned — a test that pinned a price
would be a lie generator): block 53,524,240 · gas 0.006 gwei · ETH $2,423.15 · ETH transfer
cost $0.000305 · a real tx decoded (fee $0.053306) · USDC supply 4,342,955,004 · EIP-1967
proxy detected · a funded wallet read in 0.58s.

`python_dependencies: []` — the core is standard library only, and CI proves it by
importing it with `python3 -S` (site-packages disabled) rather than by asserting it.

## Compatibility

`requires_hermes: ">=0.22.7"` in **both** this entry and `plugin.yaml` (rule 14) — the
version this was validated against. `version: "1.0.0"` matches the pinned code.

## UI note

The Desktop half registers a pane, a status-bar chip, a page route, a palette command and
a keybind, all inside the SDK surface. I have no screenshot to attach yet — the pane renders
inside the Desktop app, which I can't run here — and I'd rather say that than attach a
mock-up that isn't the real thing. The desktop half is executed by `tests/test_desktop_plugin.py` instead, which is
stronger than a picture: it caught a registration-time `ReferenceError`. Re-pinned once already: the README install section now leads with
`hermes plugins install basekit` instead of a manual clone.


One correction worth flagging to reviewers, because it is in the evidence: the first version of `docs/hook-proof.md` claimed a 2x tool-call saving. It was wrong. The toggle wrote to a config file the runtime does not read, so both arms ran with the hook on. Re-measured with the plugin's own `load_settings()` asserted before every run and the arms interleaved, the saving does not hold.

## catalog: add anki entry
https://github.com/NousResearch/hermes-agent/pull/149394
State: closed; created 2026-11-05T09:43:27Z

## What does this PR do?

Adds the `anki` catalog entry for [Anki Bridge](https://github.com/suhas-svg/hermes_anki), pinned to `bc89df834fb104b8d69c6444f35a5ae6b3764dd7`.

Anki Bridge gives Hermes five tools for the local Anki collection (`anki_decks`, `anki_add_cards`, `anki_search`, `anki_due`, `anki_answer`), an `/anki` slash command, a `hermes anki status|decks|search` CLI, and a bundled `anki:study` skill. It uses stdlib-only AnkiConnect HTTP calls, with no Python dependencies.

**Disclosure:** By default it talks only to AnkiConnect on loopback (`http://127.0.0.1:8765`). Tool calls and `/anki` mutate the local Anki collection (create decks/notes, answer cards and change their scheduling). There is no telemetry. The optional AnkiConnect API key is read through `ANKI_BRIDGE_API_KEY` and Hermes's secret scope, never from config files. The plugin does not read `.env`/auth stores, run shell commands, or override Hermes core. It requires Anki desktop with the AnkiConnect add-on (code `2055492159`) running.

## Related Issue

N/A — new catalog entry (Hermes Plugin Hackathon submission).

## Type of Change

- [x] New feature (non-breaking change that adds functionality)
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] Security fix
- [ ] Documentation update
- [ ] Tests
- [ ] Refactor
- [ ] New skill

## Changes Made

- `plugin-catalog/anki.yaml` — catalog entry with the exact 40-character pin, version `1.0.0`, `requires_hermes: ">=0.22.5"`, and the five declared tools.

## How to Test

1. `python scripts/validate_plugin_catalog.py plugin-catalog/anki.yaml` → `OK: 1 file(s) valid`.
2. Clone `https://github.com/suhas-svg/hermes_anki` at `bc89df834fb104b8d69c6444f35a5ae6b3764dd7`, then run `hermes plugins validate . --install-deps` → all checks pass (manifest, config schema, capability probe, declared tools/hooks, security scan, no core override).
3. In the plugin repo: `python -m pytest -q` → **25 passed**; `hermes plugins doctor . --ci` → 5 tools, 0 hooks.
4. Install with `hermes plugins install suhas-svg/hermes_anki --ref bc89df834fb104b8d69c6444f35a5ae6b3764dd7 --enable`, then with Anki + AnkiConnect running:
   - `hermes anki status` → connected, deck and due counts;
   - create a deck and cards through `anki_add_cards`;
   - `anki_due` returns the deck's cards; `anki_answer` grades one and updates its interval.

### Live E2E evidence

Tested on Windows 11, Python 3.14.9, Hermes `v0.22.7+371`, Anki `26.09.3` with AnkiConnect `2055492159` running locally:

- Created deck `Hermes Live`; added 3 Basic notes; 2 were new and 1 was a duplicate. AnkiConnect's older build ignored `deckName` on add, so the plugin's post-add repair moved the 2 new cards into `Hermes Live` (`deck_fixed: 2`); `findCards('deck:"Hermes Live" is:new')` then returned both.
- Answered card `1793872313625` with ease `good`; AnkiConnect returned `[True]`; `cardsInfo` showed `type: 1`, `queue: 1`, `reps: 1` and the next due timestamp.
- After a card front rendered Anki's CSS block verbatim, `strip_html` was fixed to drop `<style>`/`<script>` blocks before stripping tags.
- Test notes/decks were deleted afterward; the collection was left with only `Default`.

## Checklist

### Code

- [x] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [x] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`catalog: add anki entry`, `catalog: pin anki to 56aa5f8`, `catalog: pin anki to bc89df8`)
- [x] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [x] My PR contains **only** changes related to this entry (one file under `plugin-catalog/`)
- [ ] I've run `pytest tests/ -q` and all tests pass — N/A for a catalog-only change; the plugin's own 25 behaviour tests pass at the pinned SHA
- [ ] `python scripts/check` passes — N/A for a catalog-only change; the catalog validator and pinned-source validator are the relevant gates
- [x] I've added tests for my changes (in the plugin repo: `tests/test_anki_plugin.py`, 25 tests)
- [x] I've tested on my platform: Windows 11, Python 3.14.9, Hermes v0.22.7+371, Anki 26.09.3

### Documentation & Housekeeping

- [x] I've updated relevant documentation (the plugin's `README.md` at the pinned commit covers setup, config and disclosures)
- [ ] I've updated `cli-config.yaml.example` if I added/changed config keys — N/A (plugin-owned config schema)
- [ ] I've updated `CONTRIBUTING.md` or `AGENTS.md` if I changed architecture or workflows — N/A
- [x] I've considered cross-platform impact (Windows, macOS) per the compatibility guide — the plugin is pure Python/stdlib and works wherever Anki desktop + AnkiConnect run
- [x] I've updated tool descriptions/schemas if I changed tool behavior — N/A (new plugin, schemas live in the plugin repo)


## docs: add GitHub Copilot model routing policy
https://github.com/NousResearch/hermes-agent/pull/107023
State: closed; created 2026-09-10T01:27:44Z

## Summary
- add an operational routing policy for selecting GitHub Copilot models by task complexity, first-pass correctness, and premium-request cost
- keep the replaceable model/multiplier table separate from stable routing rules
- document escalation, model diversity, hackathon mode, and high-cost model transparency
- link the policy from the root agent instructions

## Verification
- `git diff --check` passed
- policy requirement checks: 8/8 passed
- documentation-only change; no runtime tests required

## Safety
- no source code, dependencies, or unrelated files changed
- merge and auto-merge remain disabled for human review

## feat(plugin-catalog): add reduck
https://github.com/NousResearch/hermes-agent/pull/149369
State: closed; created 2026-11-05T08:34:55Z

## What does this PR do?

Adds **Reduck** to the plugin catalog (`plugin-catalog/reduck.yaml`), pinned to [`reduck-ai/reduck-hermes-plugin@fa47b46`](https://github.com/reduck-ai/reduck-hermes-plugin/tree/fa47b46bdd426d94cd65e64b19e7f5dd35d9aaf8).

Reduck runs tested browser scripts on any website, in the user's own Chrome signed in as them, or on a Reduck-hosted browser. The agent finds a script for the task (`list_scripts`), reads its contract (`read_script`: typed input and output, side effects, whether it needs the user signed in) and runs it (`run_script`) in one call, instead of driving the page step by step. When no script fits, the agent can build one.

The plugin is a portable Agent Plugins v1 package with no code: `plugin.json` + `mcp.json` + `README.md`.

- `mcp.json`: one Streamable HTTP server, `https://mcp.reduck.ai`, with the header `x-api-key: ${REDUCK_API_KEY}`.
- `plugin.json`: one `config_schema` secret field (`env: REDUCK_API_KEY`), so Hermes Desktop shows a key field.

A portable remote entry takes only `type`, `url` and `headers`, so the plugin signs in with an API key. A user who prefers OAuth runs `hermes mcp add reduck --url https://mcp.reduck.ai --auth oauth`; that `config.yaml` entry replaces the package's server, as the README says.

Entered for the Hermes Agent Plugin Hackathon.

## Related Issue

#125222 adds Reduck to the **MCP** catalog (`optional-mcps/`, native OAuth, `hermes mcp install reduck`). This PR is the **plugin** catalog listing. The two use the same server name, so a user who has both keeps the `config.yaml` entry.

## Type of Change

- [x] ✨ New feature (non-breaking change that adds functionality)

## Changes Made

- `plugin-catalog/reduck.yaml`: the entry. `requires_hermes: ">=0.22.3"`, the first release that renders a portable package's `config_schema`. Tested on 0.22.3.
- `known_issues`: on 0.22.7 and older, a transport rebuild re-sends the literal `${REDUCK_API_KEY}` (fixed on main by 8f7a27a), so the tools stop until Hermes restarts. Reproduced on v0.22.7; does not happen on main.

## Disclosures (rule 13)

- **Network:** every tool call and its arguments go to `mcp.reduck.ai` with the user's `REDUCK_API_KEY`. The tool set is served by the remote server at runtime and is not covered by the pinned sha.
- **Acts as the user:** runs act on websites as the user in their paired Chrome, and can send forms or buy when a script does that. Each script declares its side effects.
- **Stored data:** runs, their traces and scripts are kept on the user's Reduck account.
- **Cost:** runs on a Reduck-hosted browser use the credits of the user's plan.
- **Local:** no local code. The plugin reads no files and runs no commands. The key is stored by Hermes in `.env`.

## How to Test

Run with a throwaway `HERMES_HOME`, macOS, Hermes main (d914e23), v0.22.7 and v0.22.3:

1. `hermes plugins validate <clone at fa47b46>` passes (security scan `safe`). `scripts/validate_plugin_catalog.py plugin-catalog/` passes, and the catalog test files pass (676 passed, 29 skipped).
2. `hermes plugins install https://github.com/reduck-ai/reduck-hermes-plugin --enable`, then set `REDUCK_API_KEY`: the server connects with 42 tools.
3. Real agent run, `hermes chat --oneshot -q "Use Reduck to get me the weather in Paris for the next two weeks."` with Claude Sonnet: the model calls `mcp__reduck__read_docs` → `list_scripts` → `read_script` (×2) → `run_script` and answers with the 14-day forecast from `reduck/meteoblue.com/get_14day_forecast`.
4. Desktop key flow: `plugin_settings_fields("reduck", …)` shows one secret field (`has_value` false), saving through `save_provider_env_credential` (the `PUT /api/env` path) sets `has_value` true, and the server connects.
5. OAuth path: with the plugin enabled, `hermes mcp add reduck --url https://mcp.reduck.ai --auth oauth` + browser sign-in. The log shows `Portable MCP server 'reduck' conflicts with native config; skipping` and `run_script` works over OAuth.
6. Without a key, the server fails closed: `${REDUCK_API_KEY} in url/headers is not set`, and no request is sent.

## Checklist

### Code

- [x] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [x] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [x] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate (see #125222 above)
- [x] My PR contains **only** changes related to this fix/feature (one catalog file)
- [x] I've run the catalog tests and they pass (the full suite is not affected by a catalog entry)
- [ ] `python scripts/check` passes: N/A, data-only change
- [ ] I've added tests: N/A, catalog entry
- [x] I've tested on my platform: macOS 26

### Documentation & Housekeeping

- [x] I've updated relevant documentation: N/A (the plugin's README is the catalog page)
- [x] I've updated `cli-config.yaml.example`: N/A
- [x] I've updated `CONTRIBUTING.md` or `AGENTS.md`: N/A
- [x] I've considered cross-platform impact: N/A, configuration only
- [x] I've updated tool descriptions/schemas: N/A


## feat(goals): unbounded turn-budget sentinel + judge kill-switch
https://github.com/NousResearch/hermes-agent/pull/69308
State: open; created 2026-07-22T12:02:57Z

## §1 — First principles: what an agent loop is, and what may stop it

An agent is a loop: *observe → decide → act → observe*. Stripped to its ontology, such a loop has **three operator-legible termination conditions**:

- **T1 — Task-complete.** An evaluator judges the goal satisfied.
- **T2 — Budget-exhausted.** An operator-set resource governor (turns, time, tokens, dollars) trips.
- **T3 — Operator-stop.** The human intervenes (including preemption of one goal by another).

A fourth category exists but is not operator-legible: **involuntary environmental exhaustion** — context-window overflow, provider failure, unhandled exception. It is neither set (T2) nor chosen (T3) nor judged (T1); it simply happens to the loop. This PR neither arms nor disarms it; it is noted so the taxonomy is complete rather than flattering.

Two claims follow. First, a turn cap is T2: a **governor**, not a correctness property — the number 20 encodes a default risk posture, nothing about the task. Its value must therefore be operator-settable, including the value "**no cap**" (T2 disarmed; T1/T3 remain). Second, T1 must be **demotable from guillotine to advisor** without going blind — an operator who distrusts a premature "done" still wants the evaluator's signal.

One structural premise, stated rather than smuggled: a real system instantiates this loop **at multiple call sites and in multiple concrete implementations** (Hermes has a main loop and a kanban worker loop, and historically read the cap in five places). Requirements about *consistency across sites* below derive from this premise, not from the abstract ontology.

## §2 — The defect: conflating absence with falsiness

Every read site computed the budget as a variant of:

```python
max_turns = int(cfg) or DEFAULT_MAX_TURNS        # 20
```

This uses **falsiness — a property of the value domain — to detect absence — a property of the schema.** In Python `0` is falsy, so `0 or 20 → 20`: an operator's explicitly-written zero, the natural spelling of "no cap," is silently reinterpreted as "not provided." It is the classic `NULL`-vs-`0` bug, one layer up. The type had no representation for "unbounded," so the sentinel was *unwritable*: no value in the config language meant what the operator meant. The judge had the dual problem: T1 was *always armed* — no config could demote the evaluator from guillotine to advisor.

## §3 — The design, traceable to §1's claims plus the codebase's actual structure

| Req | Derivation | Implementation |
|---|---|---|
| **R1** "Unbounded" must be representable | `Optional[int]`; `None` = unbounded. Not `10**6` — a magic large int lies about intent and still bounds. | `GoalState.max_turns: Optional[int]`; budget check `is not None`-guarded so `None` never reaches `>=`. |
| **R2** One piece of code interprets the config | From the structural premise: five read sites had each copy-pasted `or 20` — every copy a divergence risk. | `resolve_goal_max_turns()` — single source of truth: `0`/negative/`"unbounded"`/`"none"`/`"infinite"` → `None`; positive int passthrough; unset/bool/junk → 20. All sites migrated. |
| **R3** Failure falls toward the safe attractor | Unbounded must be *achievable on purpose, impossible by accident*. | Malformed config → finite 20; judge config error → judge **armed**. Regression tests pin the direction. |
| **R4** Demoting T1 must not blind the operator | Coercion records the judge's **true** verdict *before* rewriting it. | `state.last_verdict = verdict` precedes `if verdict == "done" and not _judge_enabled: verdict = "continue"` — in **both** loops. Feedback as signal, not as guillotine. |
| **R5** Both loops get identical semantics | From the structural premise: a switch covering one of two loops is a lie. | Judge coercion: **both loops ✅**. Unbounded `max_turns` on the kanban path: **pending** — see §6 known limitation. |
| **R6** Defaults bit-for-bit unchanged | Backward compatibility by construction, not by promise. | Out of the box: 20-turn budget, judge armed, finite values behave exactly as before. Old persisted rows load unchanged. |

New config surface (both keys strictly opt-in):

| Key | Default | Semantics |
|---|---|---|
| `goals.max_turns` | `20` | `0` / negative / unbounded-string → **no cap**; positive int unchanged |
| `goals.judge_enabled` | `true` | `false` → judge `done` coerced to `continue` in both loops; true verdict still recorded |

## §4 — Prior art, verified across the four sources of truth

Uncapped-but-governed agent loops are an established pattern. Each citation below does specific work; none is offered as proof that caps are wrong — §1 already established the cap is a *legitimate governor* whose value must be settable.

- **GitHub / X — Geoffrey Huntley's "Ralph"** ([ghuntley.com/ralph](https://ghuntley.com/ralph/)): the canonical deliberately-uncapped agent loop — *"Ralph is `while :; do cat PROMPT.md | claude-code ; done`"* — with the load-bearing constraint: *"Ralph can be done with any tool that does not cap tool calls and usage."* A *non-configurable* hard cap is what makes a loop non-Ralph-capable; this PR is precisely the configurability. Companion: [*everything is a ralph loop*](https://ghuntley.com/loop/) — *"give it a goal then looping the goal."* The pattern has field evidence (on X, embedded in the same page: a Ralph-built MVP delivered at $297 against a $50k contract quote) and independent replication at YC's Agents hackathon ([repomirrorhq/repomirror](https://github.com/repomirrorhq/repomirror/blob/main/repomirror.md): an uncapped loop produced 1,000+ commits and six ported codebases overnight, filesystem as cross-iteration memory).
- **YouTube** — [*Inventing the Ralph Wiggum Loop*, Dev Interrupted #256](https://www.youtube.com/watch?v=C1YNGy6qusg): *"forcing the feedback loop back on itself to actually get something to done"* — evaluator feedback as the steering signal (R4's posture). Also [Huntley with Dexter Horthy](https://www.youtube.com/watch?v=O2bBWDoxO4s) on why the claude code plugin implementation isn't it — context-engineering depth behind the meme.
- **The counterpoint, answered honestly** ([*Ship Code While you Sleep!*](https://www.youtube.com/watch?v=dPG-PsOn-7A)): *"always set the max iteration parameter — you're running a loop that spends money, so put a cap on it."* Correct — and this PR does not pretend otherwise. R3/R6 only govern defaults; they do **not** make deliberate unbounded operation safe. Once an operator opts into unbounded, the turn budget is disarmed *by construction* — the remaining exits are operator-stop (T3) and involuntary environmental failure (§1). That is what the feature is for, and it is exactly why the default stays a finite 20 and the opt-in is explicit. See also §7's combined-flags disclosure.
- **arXiv** — [Reflexion, 2303.11366](https://arxiv.org/abs/2303.11366) (Shinn et al.): its Evaluator's success signal **is** what terminates the trial loop — the authoritative-judge design this PR makes *optional*. What R4 borrows is the architectural separation (Actor ≠ Evaluator, feedback carried forward as text), not Reflexion's termination semantics. [Magentic-One, 2411.04468](https://arxiv.org/abs/2411.04468) (Fourney et al., MSR): the Orchestrator *"restarts and resets upon stalling"* — establishing the general principle this PR also relies on, that an orchestrator's judgment is embedded in a larger loop that may override it; judgment ≠ unilateral halt authority. (Magentic-One's stall-replan guards the *opposite* failure — giving up too early — and is cited for the principle, not the failure mode.) [Recursive Language Models, 2512.24601](https://arxiv.org/abs/2512.24601) (Zhang, Kraska, Khattab): inputs *"up to two orders of magnitude beyond model context windows"* handled by treating the ceiling as an engineering boundary to route around, not a law. Offered as analogy only: turn budgets are operator dials, not architectural limits — but the habit of asking "is this ceiling load-bearing or scaffolding?" transfers.

## §5 — Changes

- **`hermes_cli/goals.py`** — `resolve_goal_max_turns()`; `goal_judge_enabled()`; `Optional[int]` threaded through `GoalState` / `GoalManager` / budget guard / labels (`goal_budget_label`, `_fmt_turns` are `None`-safe); coercion in both loops after true-verdict recording; `from_json` + `set` hardened through the resolver.
- **Read sites** — `cli.py`, `gateway/run.py`, `gateway/slash_commands.py`, `hermes_cli/cli_commands_mixin.py`, `tui_gateway/server.py`: all migrated off `int(... or 20)`.
- **`hermes_cli/config.py`** — defaults for the two keys. **16/16 locales** — new `gateway.goal.set_unbounded` key, full parity. **Docs** — `goals.md`, `configuration.md`.

## §6 — Evidence

- [x] **213 passed** locally on the PR head (61 sentinel/resolver/hardening tests incl. regression pins for R1–R5, `test_goals.py`, 4 gateway E2E, 47 i18n key-parity).
- [x] `ruff check` clean on all changed files.
- [x] **CI: all 8 Python test slices + e2e green on Linux; ruff/ty/Windows-footguns/OSV/supply-chain green.** The only root-cause failure is `check-attribution` (the `All required checks pass` aggregator fails in sympathy): commits are authored `f.nazer@sanabil.com`, unmapped to `@Slimydog21`. A `contributors/emails/` mapping commit is prepared and will be added to this PR.
- [x] **Reviewed adversarially by a different model than the author** (generator–critic, code and this body): the code round found two dormant fail-closed paths — both hardened, with regression tests (`from_json` / `set` literal-0 pins). The body round's accepted findings are reflected in §1's fourth category, R5's partial marking, the reframed Reflexion/Magentic-One citations, and §7's combined-flags disclosure.
- [x] Windows `tests/hermes_cli/` sweep: 15 failures in profile/auth/backup test files reproduce **identically on a clean `origin/main` worktree** (feature code absent, same 15 fail) — pre-existing Windows-environment failures, unrelated; this diff touches none of those files.

**Known limitation (follow-up ready):** the kanban worker's *separate* normalization path (`run_kanban_goal_loop` / `cli._run_kanban_goal_loop_q`) still applies its own `... or DEFAULT` collapse, re-bounding an unbounded budget to 20 on that path only (R5, partial). Main loop, gateway, CLI, and TUI are covered here; the closing commit (Optional[int] + resolver routing, with tests) is prepared and will be pushed to this PR.

## §7 — Notes for reviewers

- **Worst-case disclosure, plainly:** setting `goals.max_turns` unbounded **and** `goals.judge_enabled: false` together removes both automatic exits. Only operator-stop (T3) and involuntary environmental failure remain. There is no absolute system ceiling beneath these two knobs. Operators choosing that combination should read it as "this loop runs until I stop it."
- Both behaviors are strictly opt-in; default behavior is bit-for-bit unchanged (R6).
- The fail-safe direction is always toward the *finite* budget and the *armed* judge — malformed config can never silently grant an unbounded loop or a silent judge (R3).
- The diff is tests-heavy by design: the sentinel contract is pinned at every layer (resolver, state round-trip, manager, both loops, banners, i18n) so "0 means unbounded" cannot quietly rot.


## docs(guides): Run Nemotron 3 Ultra free in Hermes Agent (launch guide)
https://github.com/NousResearch/hermes-agent/pull/38769
State: closed; created 2026-06-04T06:24:25Z

## Summary

- Adds a launch guide for the **Nemotron 3 Ultra** day-0 availability on Nous Portal — **free June 4th–18th**, in partnership with **NVIDIA** and **Nebius**.
- Walks users through Quick Setup and selecting the `nvidia/nemotron-3-ultra:free` tier, plus how to switch to it later and basic troubleshooting.
- Registers the page at the top of **Guides & Tutorials** (`sidebar_position: 0`).

Live URL once deployed: `https://hermes-agent.nousresearch.com/docs/guides/run-nemotron-3-ultra-free`

## Notes / launch coordination

- Model goes live **9am EST, June 4th**. This is a preemptive PR — hold the merge/deploy until launch since the model isn't announced yet.
- Partner attribution credits both NVIDIA and Nebius per the launch copy. Adjust if comms wants different wording.
- The `:free` tag is called out repeatedly — it's what keeps users on the no-cost tier.

## Test plan

- [ ] `cd website && npm run build` (or `npm start`) — confirm the new page renders and the sidebar entry appears at the top of Guides & Tutorials
- [ ] Verify all cross-links resolve (Nous Portal guide, integration page, Quickstart, OAuth over SSH)
- [ ] Confirm install command + `nvidia/nemotron-3-ultra:free` slug match the final launch config

## feat(dashboard): Pluggable theme engine with versioned skin marketplace
https://github.com/NousResearch/hermes-agent/issues/18289
State: open; created 2026-05-01T06:55:56Z

## Summary

The Hermes web dashboard ships with a single, highly opinionated visual identity (cyberpunk-aesthetic dark theme with specific color palette, typography, and layout conventions). While this works well for its target audience, it presents a hard barrier for users who:

- Experience **visual accessibility issues** (low contrast ratios, small font sizes, color combinations that cause eye strain or are problematic for users with color vision deficiencies, photosensitivity, or age-related vision degradation)
- Need **customized layouts** that surface different data fields, reorder components, or display information in alternative formats
- Operate Hermes in **professional or corporate environments** where the default aesthetic may not align with organizational standards
- Simply prefer a **different design language** (minimal, high-DPI-optimized, light-mode-first, etc.)

There is currently no mechanism to create, distribute, or manage alternative dashboard themes beyond the built-in theme picker, which offers cosmetic variations within the same rigid design shell rather than true structural redesign.

This proposal requests a **full theme templating engine** for the dashboard — one that enables third-party skins as first-class plugins, complete with schema validation, versioned distribution, and a GitHub-based template management workflow.

---

## Motivation

### Accessibility is not optional

The current dashboard uses fixed color variables, font stacks, and component layouts. Users with presbyopia, astigmatism, color blindness (protanopia, deuteranopia, tritanopia), or photosensitivity-triggered conditions (migraine, epilepsy) cannot adjust the dashboard to meet their needs without forking and manually editing the web source. This is a significant accessibility gap.

Web accessibility standards (WCAG 2.1 AA) mandate perceivable, operable, understandable, and robust UIs. A theming engine that exposes color, typography, spacing, and component-level overrides would allow the community to build and share accessibility-focused skins — high-contrast modes, dyslexia-friendly fonts, reduced-motion themes, large-print layouts — without requiring upstream changes for every edge case.

### The current theming model is surface-level

The built-in theme picker adjusts CSS variables (accent color, background shade) but does not allow:

- **Structural layout changes** — reordering dashboard sections, hiding components, adding custom panels
- **Custom typography stacks** — swapping fonts globally or per-component
- **Alternative data visualizations** — replacing chart types, table layouts, or stat cards with entirely different renderings of the same underlying data
- **Branded/white-label experiences** — logo placement, custom navigation, organization-specific chrome

This means every design choice baked into the default theme is a de facto mandate for all users.

### The ecosystem benefits from a skin marketplace

Hermes already has a thriving skill/plugin ecosystem distributed via GitHub repos. Extending this model to dashboard skins creates a natural distribution channel where:

- Community members can publish themes as Git repos or as part of plugin packages
- Users install skins with familiar commands (`hermes dashboard theme install <repo>`)
- Theme authors version their work and declare compatibility ranges against Hermes dashboard releases
- A schema contract ensures themes don't break silently when dashboard internals change

---

## Proposed Design

### 1. Theme Schema (Manifest)

Every theme ships with a `manifest.json` (or `theme.yaml`) that declares metadata, compatibility, and configuration:

```json
{
  "name": "hermes-dashboard-serene",
  "version": "1.2.0",
  "description": "High-contrast accessibility-first theme for low-vision users",
  "author": "theme-author",
  "license": "MIT",
  "homepage": "https://github.com/theme-author/hermes-dashboard-serene",
  "repository": "theme-author/hermes-dashboard-serene",

  "compatibility": {
    "hermes_dashboard": ">=0.12.0 <0.14.0",
    "schema_version": "1"
  },

  "features": {
    "structural_layout": true,
    "custom_fonts": true,
    "custom_components": false,
    "accessibility_mode": true
  },

  "accessibility": {
    "wcag_level": "AA",
    "high_contrast": true,
    "reduced_motion": true,
    "dyslexia_font": true
  },

  "entry": "index.css",
  "overrides": "overrides.json",
  "screenshots": ["screenshot-light.png", "screenshot-dark.png"]
}
```

**Key fields:**
- `compatibility.hermes_dashboard` — semver range for which dashboard versions this theme supports
- `compatibility.schema_version` — allows the schema to evolve without breaking old themes
- `features` — declares which levels of customization the theme uses (so the engine can validate and warn on unsupported features for the current dashboard version)
- `accessibility` — optional metadata for users filtering themes by accessibility needs

### 2. Theme Structure

A theme package would follow a standard directory layout:

```
hermes-dashboard-serene/
├── manifest.json          # Required: metadata, compatibility, entry point
├── index.css              # Required: CSS custom properties + style overrides
├── overrides.json         # Optional: component-level layout/behavior overrides
├── components/            # Optional: custom React components (advanced themes)
│   ├── StatsPanel.tsx
│   └── SessionList.tsx
├── assets/                # Optional: fonts, icons, images
│   ├── AtkinsonHyperlegible-Regular.woff2
│   └── logo.svg
└── screenshots/           # Required for marketplace display
    ├── light.png
    └── dark.png
```

**Three tiers of theme depth:**

| Tier | What it can do | Example |
|------|----------------|---------|
| **CSS-only** | Override CSS variables, swap fonts, adjust colors/spacing | Light mode, high-contrast, large-print |
| **Layout** | Reorder/hide/show dashboard panels via `overrides.json` declarative config | Minimal view (hide logs), operations view (sessions + cron only) |
| **Component** | Provide custom React components that consume the same data props as built-in components | Alternative chart library, Kanban-style session view, calendar view for cron |

### 3. Data Contract (Schema Support)

The dashboard already exposes structured data to its React components (sessions, cron jobs, config values, model info, usage stats, etc.). The theme engine would formalize this as a **data schema** that theme authors can rely on:

```typescript
// Published as @hermes/dashboard-data-schema (or part of the theme SDK)
interface DashboardDataProvider {
  sessions: Session[];
  cronJobs: CronJob[];
  config: DashboardConfig;
  models: ModelInfo[];
  usage: UsageStats;
  skills: SkillInfo[];
  logs: LogEntry[];
  // ... stable, versioned interface
}
```

- The schema is **versioned** and documented alongside each Hermes release
- Theme authors declare which schema version they target via `compatibility.schema_version`
- When the schema changes (field added, renamed, removed), the compatibility range mechanism ensures users are warned before applying an incompatible theme
- Breaking schema changes bump the major `schema_version`; additive changes bump minor

### 4. Distribution & Installation

Themes are distributed as **GitHub repos** (consistent with the existing skill/plugin ecosystem):

```bash
# Install from GitHub
hermes dashboard theme install theme-author/hermes-dashboard-serene

# Install from a local path (development)
hermes dashboard theme install ./my-local-theme

# List installed themes
hermes dashboard theme list

# Switch active theme
hermes dashboard theme use serene

# Preview without activating
hermes dashboard theme preview serene

# Uninstall
hermes dashboard theme uninstall serene

# Check for updates to installed themes
hermes dashboard theme update

# Publish (create repo + push)
hermes dashboard theme publish ./my-theme
```

Themes can also be bundled inside **Hermes plugins**, allowing a plugin to ship both tool behavior and a matching dashboard skin.

### 5. Version Range Support & Resolution

- Theme manifests declare a semver range for `hermes_dashboard` compatibility
- Before applying a theme, Hermes checks the current dashboard version against the declared range
- **Compatible**: theme activates normally
- **Out of range (theme too old)**: warning logged, theme still applied but with a deprecation notice pointing to an updated version
- **Out of range (theme requires newer Hermes)**: theme is listed but cannot be activated; prompt to run `hermes update`
- Schema version mismatches follow the same logic

### 6. GitHub-Based Template Management

For theme authors, a companion workflow:

- `hermes dashboard theme init` scaffolds a new theme project from a template (CSS-only, layout, or component tier)
- Templates live in a `hermes-agent/theme-templates` repo (or `nousresearch/dashboard-theme-boilerplate`)
- `hermes dashboard theme publish` creates the GitHub repo, sets up CI for manifest validation, and optionally opens a PR to a community theme index
- A `themes.json` index (curated or community-maintained) allows `hermes dashboard theme search <query>` to discover available themes

### 7. Runtime Behavior

- The default theme is always available as the fallback (zero-config new user experience is preserved)
- Active theme selection persisted in `config.yaml` under `display.dashboard_theme`
- Theme CSS loads after built-in styles (cascading override), with `!important` not required if custom properties are properly exposed
- Component-tier themes are loaded via dynamic imports with error boundaries — a broken custom component falls back to the built-in one rather than crashing the dashboard
- `hermes dashboard --no-theme` flag to launch with default theme regardless of config (debugging)

---

## Acceptance Criteria

- [ ] Theme manifest schema finalized and documented
- [ ] CSS-only themes can override colors, fonts, spacing via custom properties
- [ ] Layout themes can reorder/hide/show dashboard panels declaratively
- [ ] Component themes can provide custom React components consuming stable data props
- [ ] `hermes dashboard theme install/use/list/uninstall` CLI commands
- [ ] Semver compatibility checking on theme activation
- [ ] Schema version validation with clear error messages on mismatch
- [ ] At least 3 reference themes ship with the repo: default (current), high-contrast accessibility, minimal light
- [ ] Theme falls back gracefully to built-in components on error
- [ ] Documentation for theme authors (schema reference, component API, publishing guide)

---

## Out of Scope (for this issue)

- A centralized theme marketplace UI / website (the GitHub-based index is sufficient for v1)
- Theme monetization or review/approval workflow
- Dashboard structural refactoring to make every surface themeable (iterative; start with the highest-impact panels)
- CLI skin engine parity (TUI skins are a separate concern with their own existing `display.skin` config)

---

## Related

- PR #15892 — [Hackathon/WIP] Mission Control shadcn dashboard (external redesign attempt without theming infrastructure)
- Issue #17229 — Dashboard theme layout shifts (symptom of the current rigid theming approach)
- The existing `display.skin` config for the TUI demonstrates that Hermes already supports pluggable visual identity — this proposal extends that philosophy to the web dashboard with proper versioning and distribution


## Feature: SOC Analyst SIEM Triage Skill — Automated Alert Enrichment, Analysis & Investigation Reports
https://github.com/NousResearch/hermes-agent/issues/515
State: open; created 2026-03-06T09:36:23Z

## Overview

SOC (Security Operations Center) analysts spend the majority of their time on repetitive alert triage — enriching IOCs, correlating logs, mapping to MITRE ATT&CK, and writing investigation reports. Research shows AI agents can reduce triage time from 30-70 minutes to under 3 minutes per alert, with 60-80% false positive reduction.

This skill would enable Hermes Agent to act as a SOC analyst's assistant: given SIEM alerts or security log data, it would perform automated triage, enrichment, and investigation using specialized analysis workflows — then produce a structured report with recommended next steps for human review.

Inspired by [a hackathon project](https://huamichaelchen.substack.com/p/can-swarm-of-a2a-agents-do-cybersecurity) that built a multi-agent cybersecurity swarm using Google's A2A protocol and MCP. That project used specialized agents (Network Log Analyzer, Windows Event Log Analyzer, File Malware Analyzer, Threat Intel, MITRE ATT&CK Enrichment, Host Forensics) coordinated by an Orchestrator and Planner. This skill takes that concept and implements it within Hermes's existing delegation and skill architecture — no new protocols required.

---

## Research Findings

### The SOC Analyst Workflow

The standard alert lifecycle that this skill would augment:

1. **Ingestion** — SIEM generates alerts from log correlation, detection rules (Sigma, YARA, Suricata)
2. **Triage** — Analyst assesses severity, deduplicates, prioritizes (biggest time sink)
3. **Enrichment** — IOC lookups (VirusTotal, Shodan, AbuseIPDB), WHOIS, DNS, reputation checks
4. **Deep Analysis** — Log correlation, MITRE ATT&CK mapping, timeline reconstruction
5. **Containment** — Recommended response actions (isolate host, block IP, disable account)
6. **Documentation** — Investigation report with evidence, findings, recommended commands

### Existing AI-for-SOC Projects

The space is active and growing:

- **AI-SOC-Agent** (BlackHat 2025) — MCP-based, ~$0.18/alert cost, ~50s per investigation
- **SOC AI Companion** (NDSS 2026) — ReAct agent, on-premises LLM, ~40% analyst time reduction
- **Red Canary osquery-forensics-agent** — 30min → 2min investigations, 10x throughput
- **Rule-ATT&CK Mapper (RAM)** — SIEM rule to MITRE ATT&CK mapping via LLM agents
- Commercial: CrowdStrike Charlotte AI, Microsoft Copilot for Security, Torq HyperSOC, Dropzone AI

### Security Tools Hermes Can Leverage via Terminal

Open-source tools installable on the agent's host:

| Category | Tools |
|----------|-------|
| Detection Rules | `sigma-cli` (3000+ detection rules), YARA |
| Network Analysis | `tshark`, `zeek`, `suricata` |
| Windows Logs | `chainsaw` (EVTX analysis), `hayabusa` |
| Malware Analysis | `capa` (capability extraction), `die` (detect-it-easy) |
| Memory Forensics | `volatility3` |
| Vuln Scanning | `nuclei`, `nmap` |
| OSINT | `shodan` CLI, `theHarvester` |
| Data Processing | `jq`, `csvkit`, Python stdlib |

### External APIs for Enrichment

| API | Purpose | Auth |
|-----|---------|------|
| VirusTotal | File/URL/IP reputation | API key (free tier: 4 req/min) |
| Shodan | Internet-facing device intel | API key |
| AbuseIPDB | IP reputation scoring | API key (free: 1000/day) |
| MITRE ATT&CK | Technique/tactic mapping | None (STIX/TAXII, open data) |
| AlienVault OTX | Threat intelligence | API key (free) |
| GreyNoise | IP noise/benign classification | API key (free tier) |

### The Cybersecurity Agent Swarm Architecture (Inspiration)

The [original article](https://huamichaelchen.substack.com/p/can-swarm-of-a2a-agents-do-cybersecurity) used this agent structure:

- **Leader Agents**: Orchestrator (receives SIEM alerts) → Planner (dissects and routes to specialists)
- **Task Agents**: Network Log Analyzer, Windows Event Log Analyzer, File Malware Analyzer, Threat Intel, MITRE ATT&CK Enrichment, Host Forensics
- **Aggregator Agent**: Collects all findings → generates PDF report

This maps naturally to Hermes's `delegate_task` tool — the main agent acts as orchestrator/planner, delegates specialist tasks to subagents, and aggregates results.

---

## Current State in Hermes Agent

**What we have that's relevant:**
- `delegate_task` tool — can fan out specialist analysis tasks to parallel subagents
- `terminal` tool — can run security CLI tools (nmap, sigma-cli, tshark, chainsaw, etc.)
- `web_extract` / `web_search` — can perform OSINT and threat intel lookups
- `read_file` / `search_files` — can analyze log files and datasets
- `write_file` — can generate investigation reports
- `execute_code` — can run Python scripts for data processing, parsing, correlation

**What we don't have:**
- No cybersecurity-specific skills (zero security analysis capabilities)
- No SIEM integration patterns
- No IOC enrichment workflows
- No MITRE ATT&CK mapping logic
- No security report templates

**Related existing issues:**
- #382 — Code Security Audit Skill (SAST scanning — code-focused, not SOC/SIEM)
- #383 — Binary Security Analysis Skill (exploit analysis — different scope)
- #384 — OSS Security Forensics Skill (supply chain — different scope)
- #400 — Web Application Penetration Testing Skill (offensive security — different scope)
- #355 — OSINT Investigation Skill (relevant — could be a building block for threat intel)

These are individual security analysis skills. This proposal is a **workflow skill** that coordinates SOC-specific analysis across multiple domains — complementary to those issues, not overlapping.

---

## Implementation Plan

### Skill vs. Tool Classification

This should be a **skill** (Skills Hub, not bundled) because:
1. It can be expressed entirely as instructions + shell commands + existing tools (`terminal`, `web_extract`, `delegate_task`, `read_file`, etc.)
2. It wraps external CLIs and APIs callable via terminal and web_extract
3. It doesn't need custom Python integration in the harness
4. It's specialized — cybersecurity/SOC is a specific domain, not broadly useful to all users

It should go to the **Skills Hub** (not bundled) because SOC analysis is a specialized domain that most Hermes users won't need. Users who want it can install via `hermes skills install soc-analyst`.

### What We'd Need

- Skill file: `skills/cybersecurity/soc-analyst/SKILL.md` — Main skill with workflow instructions
- Reference files:
  - `references/mitre-attack-mapping.md` — MITRE ATT&CK technique reference and mapping patterns
  - `references/ioc-enrichment.md` — IOC lookup workflows for different indicator types
  - `references/sigma-rules.md` — Sigma rule syntax and common detection patterns
- Template files:
  - `templates/investigation-report.md` — Structured SOC investigation report template
  - `templates/alert-triage.md` — Alert triage checklist template
- Script files:
  - `scripts/setup-security-tools.sh` — Install required CLI tools (sigma-cli, chainsaw, capa, etc.)
  - `scripts/enrich-iocs.py` — Python script for batch IOC enrichment via APIs

### Phased Rollout

**Phase 1: IOC Enrichment & Alert Triage**
- Core skill with triage workflow: receive alert data → extract IOCs → enrich via APIs → assess severity
- IOC types: IP addresses, domains, file hashes (MD5/SHA256), URLs, email addresses
- Enrichment sources: VirusTotal, AbuseIPDB, WHOIS, DNS lookups (via terminal `dig`/`nslookup`)
- Output: structured triage summary with severity assessment and IOC context
- Setup script for installing `sigma-cli`, `jq`, Python `requests`
- Uses existing tools only — no new Hermes code required

**Phase 2: Log Analysis & MITRE ATT&CK Mapping**
- Network log analysis workflows (parse pcap with tshark, analyze with zeek)
- Windows event log analysis (parse EVTX with chainsaw/hayabusa)
- MITRE ATT&CK mapping: correlate findings to techniques/tactics using the ATT&CK STIX data
- Timeline reconstruction from multiple log sources
- Uses `delegate_task` to run parallel specialist analyses (network, host, malware)

**Phase 3: Full SOC Workflow & Report Generation**
- End-to-end workflow: SIEM alert → automated triage → multi-domain analysis → investigation report
- PDF report generation with executive summary, detailed findings, recommended commands
- Integration with #355 (OSINT skill) for threat intel deep dives
- Playbook library: pre-built investigation playbooks for common alert types (brute force, lateral movement, data exfiltration, phishing)
- Confidence scoring and false positive assessment

---

## Pros & Cons

### Pros
- **High-impact use case**: SOC analysts are overwhelmed (avg 4,484 alerts/day, 67% ignored per studies). AI triage is one of the most valuable LLM applications
- **Builds on existing infrastructure**: Uses `delegate_task`, `terminal`, `web_extract`, `read_file` — no new tools needed
- **Open-source advantage**: Uses free security tools (sigma, chainsaw, capa) and free API tiers — no vendor lock-in
- **Complementary to existing security issues**: #382-384 cover code/binary/supply-chain security; this covers operational security (SOC/SIEM)
- **Natural fit for multi-agent**: The orchestrator → specialist → aggregator pattern maps directly to Hermes's delegation architecture
- **Demonstrates Hermes's versatility**: A compelling showcase for what a general-purpose agent can do in a specialized domain

### Cons / Risks
- **LLM hallucination in security context**: False negatives (missing real threats) or false positives (unnecessary escalation). Mitigation: human-in-the-loop for all response actions, confidence scoring, cite evidence
- **Prompt injection via log data**: Attackers could craft log entries that manipulate the agent. Mitigation: treat all log data as untrusted, sanitize before processing, use structured extraction not raw prompt insertion
- **API key management**: Multiple external APIs (VirusTotal, Shodan, etc.) need keys. Mitigation: leverage #410 (Secure Secrets Management) when available, or use .env
- **Tool installation burden**: Requires installing security tools on the host. Mitigation: setup script, graceful degradation if tools are missing
- **Specialized audience**: Not broadly useful — SOC analysts are a niche. Mitigation: Skills Hub distribution, not bundled
- **Ethical concerns**: Dual-use risk (attacker could use the same analysis to understand defenses). Mitigation: focus on defensive analysis only, no exploit generation

---

## Open Questions

- Should this skill assume the user has SIEM data exported to files, or should it integrate with SIEM APIs (Splunk, ELK, Wazuh) directly?
- What's the minimum set of security tools required vs. optional enhancements?
- Should the skill support real-time alert streaming (e.g., watching a log file) or batch analysis only?
- How should API keys for enrichment services be managed before #410 (Secure Secrets Management) lands?
- Should investigation reports be Markdown, PDF, or both?
- Should this build on #355 (OSINT skill) as a dependency, or be self-contained?

---

## References

- [Cybersecurity Agent Swarm Article (inspiration)](https://huamichaelchen.substack.com/p/can-swarm-of-a2a-agents-do-cybersecurity)
- [AI-SOC-Agent (BlackHat 2025)](https://github.com/SamiGPT/AI-SOC-Agent)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Sigma Detection Rules](https://github.com/SigmaHQ/sigma)
- [Chainsaw (Windows EVTX Analysis)](https://github.com/WithSecureLabs/chainsaw)
- [ACME4 Dataset (Lawrence Livermore)](https://llnl.gov) — the dataset used in the inspiration project
- Related issues: #382 (code security), #383 (binary security), #384 (OSS forensics), #400 (web pentest), #355 (OSINT), #410 (secrets management)


## docs(user-stories): add 45 business and professional stories
https://github.com/NousResearch/hermes-agent/pull/133708
State: closed; created 2026-10-06T06:27:26Z

## What

Prepends 45 new entries to `website/src/data/userStories.json` (326 to 371). All of them are people and teams using Hermes Agent for work: companies, agencies, professional practices, shops and solo operators. The page renders in array order, so these become the first tiles visitors see.

- Pure prepend: +495 / -0. No existing entry is edited, reordered or removed.
- Same key set as every existing entry (`id, source, author, url, date, category, headline, quote, size`).
- Every `category` and `source` is a key in `UserStoriesCollage` `CATEGORIES` / `SOURCE_LABELS`.

## Why

Business use is under-represented on the page today: business-ops has 23 of 326 tiles, enterprise 12 and marketing 2, while dev-workflow alone has 77.

After this PR: business-ops 23 to 48, enterprise 12 to 21, marketing 2 to 9.

Examples of what's added: Razorpay's per-employee agent platform (220+ employees), a 17-person startup with one Hermes profile per team, a pool service company checking 400+ technician reports a week, a commercial film company, a maternal-fetal medicine specialist, an attorney's billing reconciliation, a Swiss web agency's invoice drafting, an ad agency running audits in Slack, a bookstore, a construction office, an MSP-style consultancy and several e-commerce stores.

Sources: reddit 19, x 11, blog 7, hn 5, youtube 2, github 1.

## How the entries were checked

- Each quote is copied verbatim from the public post, comment, article or video transcript at the `url`. Where a quote joins non-adjacent passages they are separated by ` … `. A script checked every quote segment as a literal substring of the saved source text.
- Every person or org describes their own real use. Excluded: questions, hypotheticals, third-party product promos, paid-promotion videos, stories showing unsafe setups, and posts where Hermes isn't named.
- No URL, id or author already on the page (checked against `main` at `206102314`). One author per batch.
- Authors are handles or org names only. Reddit comment stories link the comment permalink.
- Headlines are 90 characters or fewer.

## New entries

| # | id | source | category | size | headline |
|---|---|---|---|---|---|
| 1 | `blog-razorpay-employee-agents` | blog | enterprise | lg | Razorpay gives 220+ employees their own isolated, always-on Hermes agent |
| 2 | `x-jacquelinesyc19-artie-team-profiles` | x | enterprise | lg | A 17-person startup gives every team its own Hermes profile, from code to BizOps |
| 3 | `reddit-andrewtcombs-pool-route-qc` | reddit | business-ops | lg | Route manager at a 400-pools-a-week service company has Hermes flag bad tech reports live |
| 4 | `x-julientalbot974-french-smb-clients` | x | business-ops | lg | Runs Hermes assistants for French small business owners, 8,000 scheduled runs so far |
| 5 | `reddit-chrisaumen-film-company-office` | reddit | business-ops | lg | Film production company owner runs budgets, deal memos and sales follow-ups via Hermes |
| 6 | `blog-doctorswhocode-clinical-skills` | blog | business-ops | lg | A maternal-fetal medicine specialist runs clinical documentation through 94 skills |
| 7 | `x-rlaope-sionic-mac-farm` | x | enterprise | lg | Korean AI company runs dozens of Hermes agents on a Mac Mini farm across every team |
| 8 | `reddit-neurosisbyanalysis-attorney-shop` | reddit | business-ops | lg | Attorney who also runs a local multi-site business automates payment reconciliation |
| 9 | `x-corxntyn-agency-invoice-drafting` | x | business-ops | lg | Swiss web agency drafts client invoices from Harvest and ClickUp, a human sends them |
| 10 | `reddit-uc_kratom-two-human-sdlc` | reddit | dev-workflow | lg | Two-person video startup lets Hermes PM and engineer agents run most of its SDLC |
| 11 | `youtube-presswhizz-sales-ops` | youtube | business-ops | lg | A PR agency runs sales ops in Slack: CRM lookups, lead research notes and email triage |
| 12 | `x-ericosiu-slack-ad-strategy` | x | marketing | md | Ad agency team runs spend audits and creative refreshes with Hermes in Slack |
| 13 | `hn-brettcvz-company-data-slack` | hn | enterprise | md | Nontechnical teammates query BigQuery, Stripe and Amplitude through Hermes in Slack |
| 14 | `reddit-jamieandlion-fintech-rules` | reddit | dev-workflow | md | Fin-crime platform reworked 2,500+ rule scenarios so client config changes skip a deploy |
| 15 | `x-jaredclucas-real-estate-client` | x | business-ops | md | Managed agent cut a real estate client's accounting fees by $18k a year |
| 16 | `reddit-crfr4mvzl-construction-office` | reddit | business-ops | md | Construction company owner runs bidding, legal drafts and ERP invoicing with seven agents |
| 17 | `blog-stewartmedia-shopify-agency` | blog | marketing | md | An e-commerce SEO agency splits Hermes into Shopify, search and client-prep agents |
| 18 | `x-thecraighewitt-support-ticket-mining` | x | business-ops | md | Podcast hosting founder shares his agent with the team to mine support tickets |
| 19 | `reddit-jack-dawed-bookstore-agents` | reddit | business-ops | md | Bookstore runs a staff agent on Discord and a customer agent on iMessage for under $10/mo |
| 20 | `hn-theturtletalks-helpdesk-replaced` | hn | business-ops | md | Replaced the helpdesk: Hermes briefs a local support agent and escalates to the team |
| 21 | `reddit-how_gauche-50-dev-team` | reddit | enterprise | sm | A 50-developer team uses Hermes for code review, incident notes and ticket triage |
| 22 | `x-leploutos-client-prospecting-agents` | x | marketing | md | Deployed LinkedIn prospecting agents for consulting firms and web agencies |
| 23 | `reddit-geektekrob-collectibles-shop` | reddit | business-ops | md | Family collectibles shop on a $12 VPS gets inbox triage and stock alerts across 4,000 SKUs |
| 24 | `blog-halfbitstudio-software-house` | blog | business-ops | md | A three-person software house uses Hermes for lead research and competitor analysis |
| 25 | `reddit-avishic-startup-on-call` | reddit | enterprise | md | YC-backed design-to-code startup made a Hermes agent its on-call engineer |
| 26 | `x-martybent-tftc-company-brain` | x | business-ops | md | Media company agent brings 7 months of company memory into a shared team workspace |
| 27 | `reddit-nkb82-sme-consultancy` | reddit | business-ops | md | IT consultancy deploys Hermes for SME clients: CRM outreach, lead vetting, ERP support |
| 28 | `github-hewi333-service-business` | github | business-ops | md | A real service business ran lead to payment over Telegram, owner approving each step |
| 29 | `reddit-osamu-dazai-12-company-agents` | reddit | enterprise | md | Company agents for sales and sprint reports went from hackathon to daily CEO and CMO use |
| 30 | `x-vibemarketer_-outbound-gtm-agent` | x | marketing | md | Outbound sales agent researches accounts and queues every send for approval in Telegram |
| 31 | `reddit-thetomsays-wiki-inbox` | reddit | enterprise | sm | Staff forward email threads to an update@ inbox and Hermes files them into the wiki |
| 32 | `blog-echobind-company-slack-bot` | blog | enterprise | md | A software consultancy built an internal Slack assistant that knows the company |
| 33 | `reddit-forsaken_coconut3717-agency-outreach` | reddit | marketing | md | Marketing business owner has Hermes find 50 prospects a day and run weekly SEO checks |
| 34 | `youtube-airanking-seo-loop` | youtube | marketing | md | A daily SEO loop: Search Console analysis, drafts, approval, then publishing |
| 35 | `reddit-xbxz-dev-shop-prs` | reddit | dev-workflow | md | 20-developer software agency hands PR notices, client status and app builds to Hermes |
| 36 | `x-loicberthelot-dropmagic-backbone` | x | business-ops | md | Startup founder runs support, banking, Stripe and SEO through Hermes agents |
| 37 | `reddit-ecommerce_addict-managed-service` | reddit | business-ops | md | Managed-service firm runs a separate Hermes agent per client to produce deliverables |
| 38 | `blog-sanjuacodez-company-brain` | blog | business-ops | md | A startup's company brain runs daily standups and GTM tracking in Discord |
| 39 | `reddit-hvhprofessionalist-real-estate-cos` | reddit | business-ops | sm | Owner of three commercial real estate firms runs a Hermes chief of staff over specialists |
| 40 | `hn-leansensei-orders-inventory` | hn | business-ops | sm | Asking internal business tools about orders and inventory over Telegram |
| 41 | `reddit-bluffman-b2b-draft-orders` | reddit | business-ops | sm | Niche online store owner has Hermes turn B2B client emails into Shopify draft orders |
| 42 | `hn-jjcm-founder-boss` | hn | business-ops | sm | A first-time founder uses Hermes as a daily boss for fundraising and compliance |
| 43 | `reddit-jean-jcrx-consulting-sales-prep` | reddit | integrations | sm | Consultant wires Hermes to a self-hosted CRM and gets an 8-page meeting prep brief |
| 44 | `blog-martechai-whatsapp-business` | blog | marketing | sm | A marketing founder runs WhatsApp replies, approval-gated jobs and Notion team check-ins |
| 45 | `hn-schezhugo-verso-knowledge-work` | hn | business-ops | sm | A daily work setup on Hermes for meetings, prospects and commercial proposals |

Open single-story PRs on this file (e.g. #133445, #100057) also prepend, so whichever merges second has a trivial conflict at the top of the array. Happy to rebase.


## [Feature]: Collaboration Inquiry – OpenXAI Ambassador Team
https://github.com/NousResearch/hermes-agent/issues/47158
State: closed; created 2026-06-16T09:16:11Z

### Problem or Use Case

Hi Hermes Agent team,
I’m part of the OpenXAI Ambassador program. We’re exploring collaboration opportunities including AI initiatives and hackathon sponsorships.
We would love to connect with a core team member for a short discussion with our founder Ashton.
Please let us know the best way to proceed.
Thank you!

### Proposed Solution

Done

### Alternatives Considered

_No response_

### Feature Type

New tool

### Scope

None

### Contribution

- [ ] I'd like to implement this myself and submit a PR

### Debug Report (optional)

```shell

```

## fix(url_safety): allow NAT64 well-known prefix (RFC 6052)
https://github.com/NousResearch/hermes-agent/pull/12256
State: closed; created 2026-04-18T19:28:45Z

## Problem

`is_safe_url` fails closed on legitimate public URLs when the client machine is on a NAT64-aware network (dual-stack lite, 464XLAT cellular, or any IPv6-only with CLAT).

Python's `IPv6Address.is_reserved` returns True for the entire NAT64 Well-Known Prefix `64:ff9b::/96` (RFC 6052). The existing `_is_blocked_ip` check treats any reserved IPv6 as an SSRF target, so `web_extract` rejects those URLs with:

```
Blocked: URL targets a private or internal network address
```

But NAT64 addresses are the IPv6 representation of **public** IPv4 services reachable via an upstream NAT64 translator — the embedded IPv4 address in the low 32 bits is public. Blocking them is a false positive.

### How I hit it

Consumer dual-stack-lite ISP returns both a public IPv4 and a NAT64 synthesized IPv6 for any AAAA lookup. e.g. `blogs.nvidia.com`:

```python
>>> socket.getaddrinfo("blogs.nvidia.com", None, socket.AF_UNSPEC, socket.SOCK_STREAM)
[(2,  ..., ('2.19.248.139', 0)),
 (10, ..., ('64:ff9b::213:f88b', 0, 0, 0))]
```

`is_safe_url` iterates addresses and bails on the first blocked one, so the NAT64 entry short-circuits the public IPv4.

Affects `sec.gov`, `investor.nvidia.com`, `blogs.nvidia.com`, Google/Cloudflare DNS, and countless others depending on network topology.

## Fix

Explicit allow for `64:ff9b::/96` at the top of `_is_blocked_ip`, before the generic `is_private / is_reserved` check. Mirrors the existing `_CGNAT_NETWORK` explicit handling.

```python
_NAT64_NETWORK = ipaddress.ip_network("64:ff9b::/96")

def _is_blocked_ip(ip):
    if isinstance(ip, ipaddress.IPv6Address) and ip in _NAT64_NETWORK:
        return False
    ...
```

Security posture is preserved: the NAT64 translator itself is a public gateway, so an attacker using a NAT64 IPv6 to reach an internal IPv4 would need to get Hermes onto the NAT64 operator's network AND configure their private IPv4 into the NAT64 mapping — infeasible in the threat model the SSRF check is defending against. (Truly internal IPv4s behind CGNAT/VPN are separately blocked via `_CGNAT_NETWORK` and the standard private ranges.)

## Tests

All 61 tests in `tests/tools/test_url_safety.py` pass, including new coverage:

- `TestIsBlockedIp.test_allowed_ips` — 5 new parametrized IPs across the `64:ff9b::/96` range (nvidia, Google DNS, Cloudflare, boundary cases)
- `test_nat64_url_allowed_end_to_end` — dual-stack hostname returning both a public IPv4 and a NAT64 IPv6
- `test_nat64_only_resolution_allowed` — IPv6-only resolution returning only a NAT64 address (DS-Lite scenario)

Ran with:

```bash
python -m pytest tests/tools/test_url_safety.py -x
# 61 passed in 1.33s
```

## Context

Found while building a Hermes Agent hackathon submission — `web_extract` kept erroring on legitimate public URLs because the dev machine is on a DS-Lite home ISP. Spent a bit figuring out this wasn't a Firecrawl auth / quota issue. Hopefully saves someone else the debugging.

Repo of the project that surfaced this: https://github.com/SergoVashakmadze/IoMarkets-Hermes (Hermes Creative Hackathon 2026).

## feat: cognitive memory system - semantic recall, encoding & forgetting
https://github.com/NousResearch/hermes-agent/pull/727
State: closed; created 2026-03-08T23:40:52Z

## Summary
![demo_cognitive_memory](https://github.com/user-attachments/assets/564e91df-e9a7-4e8a-870c-647923ef89c6)

Implements a **Cognitive Memory System** that gives Hermes Agent human-like semantic memory across sessions. This addresses three hackathon issues:
- Closes #676 — Cognitive Encoding (auto-classification + contradiction detection)
- Closes #677 — Semantic Recall (composite-scored retrieval)
- Closes #678 — Extraction & Forgetting (importance decay + pruning)

## What it does

The agent can now **remember**, **recall**, **update**, and **forget** information using meaning-based search — not just keyword matching. Memories persist across sessions in a local SQLite database with vector embeddings.

### Key Features

1. **Semantic Recall** — Finds relevant memories by meaning using embedding similarity, combined with recency and importance in a composite score: `score = 0.5×similarity + 0.3×recency + 0.2×importance`

2. **Cognitive Encoding** — Automatically classifies stored information into categories (fact, preference, procedure, environment, etc.) using heuristic patterns. Estimates importance based on content signals.

3. **Contradiction Detection** — When new information conflicts with existing memories (e.g., "we use PostgreSQL" → "we switched to MySQL"), the system detects the contradiction and supersedes the old memory automatically.

4. **Forgetting System** — Importance decays over time (`importance × 0.5^(days/half_life)`). A background cycle consolidates similar memories and prunes forgotten ones below threshold (0.05).

5. **Proactive Storage** — The agent automatically stores important facts users share (preferences, project details, corrections) without being asked.

## Architecture

```
cognitive_memory/
├── embeddings.py      # LiteLLM-based embedding provider (any model)
├── store.py           # SQLite vector store with binary-packed float32 embeddings
├── recall.py          # Semantic recall engine with composite scoring
├── encoding.py        # Auto-classification + contradiction detection
└── extraction.py      # Fact extraction + forgetting manager

tools/
└── cognitive_memory_tool.py  # Agent tool (cognitive_recall) with 4 actions
```

### Integration Points
- **Tool**: Registered as `cognitive_recall` in the `memory` toolset with 4 actions: `recall`, `store`, `forget`, `status`
- **System Prompt**: `COGNITIVE_MEMORY_GUIDANCE` injected when tool is loaded
- **Config**: Opt-in via `~/.hermes/config.yaml` under `cognitive_memory:` section
- **No new dependencies**: Uses `litellm` (already a dependency) for embeddings

## How to Enable

### 1. Add to `~/.hermes/config.yaml`:
```yaml
cognitive_memory:
  enabled: true
  embedding:
    model: "gemini/gemini-embedding-001"  # or any litellm-compatible model
```

### 2. Set embedding API key in `~/.hermes/.env`:

The embedding model needs its provider's API key. Examples:

| Provider | Embedding Model | Required Env Var |
|----------|----------------|------------------|
| Google Gemini | `gemini/gemini-embedding-001` | `GEMINI_API_KEY` |
| OpenAI | `text-embedding-3-small` | `OPENAI_API_KEY` |
| Cohere | `cohere/embed-english-v3.0` | `COHERE_API_KEY` |
| Voyage | `voyage/voyage-2` | `VOYAGE_API_KEY` |

Any embedding model supported by [litellm](https://docs.litellm.ai/docs/embedding/supported_embedding) works.

### 3. Use it:
```
You: My name is 0xbyt4, I'm a blockchain developer. I prefer dark mode and TypeScript.
Agent: [stores preferences and facts automatically]

You: /new
You: What do you remember about me?
Agent: [recalls via semantic search] I remember you're 0xbyt4, a blockchain developer who prefers dark mode and TypeScript.

You: Actually I switched from TypeScript to Rust last month.
Agent: [detects contradiction, supersedes old memory] Updated! I've noted you now use Rust instead of TypeScript.
```

## Configuration Options

All options in `~/.hermes/config.yaml` under `cognitive_memory:`:

```yaml
cognitive_memory:
  enabled: true                    # Enable/disable the system
  db_path: "cognitive_memory.db"   # SQLite database path (relative to ~/.hermes/)
  embedding:
    model: "gemini/gemini-embedding-001"
    dimensions: 3072               # Auto-detected from model if omitted
  recall:
    similarity_weight: 0.50        # Weight for semantic similarity
    recency_weight: 0.30           # Weight for recency
    importance_weight: 0.20        # Weight for importance
    similarity_threshold: 0.30    # Minimum similarity to return
    recency_half_life_days: 30.0  # Half-life for recency decay
  forgetting:
    decay_half_life_days: 90.0    # Half-life for importance decay
    prune_threshold: 0.05         # Remove memories below this importance
    consolidation_similarity: 0.92 # Merge memories above this similarity
    cycle_interval_hours: 24.0    # Run forgetting cycle every N hours
```

## Tests

**177 tests**, all passing:

```
tests/cognitive_memory/
├── test_embeddings.py    # 54 tests — embedding provider, cosine similarity
├── test_store.py         # 37 tests — SQLite store CRUD, search, decay
├── test_recall.py        # 37 tests — composite scoring, recall engine
├── test_encoding.py      # 33 tests — classification, contradiction detection
├── test_extraction.py    # 33 tests — fact extraction, forgetting manager
└── test_tool.py          # 20 tests — agent tool integration
```



## Changes

- **19 files changed**, **3,857 additions**, 5 deletions
- **New package**: `cognitive_memory/` (5 modules)
- **New tool**: `tools/cognitive_memory_tool.py`
- **Modified**: `run_agent.py` (init + dispatch), `model_tools.py` (tool discovery), `toolsets.py` (toolset mapping), `agent/prompt_builder.py` (system prompt guidance), `cli-config.yaml.example` (config docs)

## Feat/hackathon creative - AI phonetic captions for Vietnamese teaching Shorts
https://github.com/NousResearch/hermes-agent/pull/18725
State: closed; created 2026-05-02T08:01:47Z

# feat(hackathon): SpeakAlong — AI phonetic captions for Vietnamese teaching Shorts

## Summary

Add **SpeakAlong**, a self-contained Hermes plugin that generates phonetically-annotated captions for Vietnamese teaching videos. Pipeline: Whisper (transcription) → Kimi K2.6 (EN/VI classification + diacritic correction + phonetic generation) → FFmpeg (burn-in). Includes a full visual editor dashboard with segment editing, NL instructions, QA review, and style presets.

**Hackathon**: Nous Research × Kimi Track
**Plugin**: `plugins/phonetic-captions/`
**Track**: Kimi (primary) + General

## Problem

Vietnamese language teachers creating YouTube Shorts face a gap: auto-captions transcribe the audio but never add phonetic guides — the one thing learners need to actually *speak* the words. Manual phonetic annotation takes 20–40 minutes per 60-second video. Existing tools (Descript, CapCut) break on code-switching (English narration + Vietnamese vocabulary), which is exactly how teaching videos are structured.

## Solution

**SpeakAlong** handles the full pipeline end-to-end:
- **Local transcription** (faster-whisper, auto language detect)
- **Kimi K2.6 phonetic generation** (EN/VI classification, diacritic correction, English phonetic guides like `[humm biet]` for `không biết`)
- **FFmpeg burn-in** (ASS subtitle format: Vietnamese text bold on top, phonetic italic below; English text only)
- **Telegram-native loop** (send video → get back captioned clip + dashboard link)
- **Visual editor** (per-segment fixes, NL edits, QA review, style presets)

## Key features

- ✅ **Code-switching support** — auto detects EN/VI segment boundaries, no config needed
- ✅ **Diacritic restoration** — fixes Whisper transcription artifacts (e.g. `khong biet` → `không biết`)
- ✅ **Phonetics only (no IPA)** — plain English letters (`[humm biet]`), readable by any learner
- ✅ **Dashboard visual editor** — edit segments, apply NL instructions, run QA, re-burn, download
- ✅ **Hermes model fallback** — works without NVIDIA API key (uses configured Hermes model)
- ✅ **Plugin architecture** — zero core file changes (except 1 catch-all guard in App.tsx)
- ✅ **SSE streaming** — prevents browser timeout on slow model inference

## Changes

### Core files (minimal)
- `web/src/App.tsx` (+1 line) — catch-all guard to prevent hard-refresh bounce from `/captions/{id}` to `/sessions`

### Plugin files
- `plugins/phonetic-captions/__init__.py` — plugin registration
- `plugins/phonetic-captions/plugin.yaml` — plugin manifest (pip_dependencies, provides_tools)
- `plugins/phonetic-captions/pipeline.py` — transcription + phonetic generation + ASS building + FFmpeg burn
- `plugins/phonetic-captions/dashboard/plugin_api.py` — FastAPI backend (13 endpoints for job CRUD, NL edits, QA, style presets)
- `plugins/phonetic-captions/dashboard/src/index.tsx` — React UI (3-column layout: video player + segments + Hermes panel)
- `plugins/phonetic-captions/dashboard/dist/index.js` — pre-built IIFE (no user build step)
- `plugins/phonetic-captions/docs/SUBMISSION.md` — hackathon submission details

## Technical highlights

- **Kimi K2.6 via NVIDIA NIM** — `base_url: https://integrate.api.nvidia.com/v1`, `model: moonshotai/kimi-k2.6`
- **Hermes model fallback** — automatic degradation if NVIDIA_API_KEY absent
- **SSE streaming for AI calls** — NL-edit and QA endpoints use `StreamingResponse` with live status
- **Self-contained plugin** — tool registration via `register(ctx)`, no manual import lists
- **Health banner** — displays ffmpeg/faster-whisper status + phonetics engine (NVIDIA or Hermes)

## Testing

Manual smoke tests cover:
1. CLI captioning (transcribe → phonetics → burn)
2. Dashboard upload flow (auto-pipeline)
3. Segment editing (text, phonetic, EN/VI toggle)
4. NL edits (merge, split, edit operations)
5. QA review (flags + praise)
6. Re-burn (style changes persist)
7. Style presets (save, apply, delete)
8. Telegram flow (send video → captions → link)

## Notes

- **No automated tests** — manual E2E covers the hackathon window
- **Known issue**: `margin_bottom` (TypeScript) vs `margin_edge` (backend) mismatch — margin UI changes don't persist correctly to burned video. Requires renaming all instances of `margin_bottom` to `margin_edge` in `dashboard/src/index.tsx`
- **Requires**: Python 3.11+, FFmpeg, faster-whisper, openai, NVIDIA_API_KEY (optional)
- **Telegram caching**: gateway injects video file path into agent message so captioning tool can access local cache

## Links

- Submission details: `plugins/phonetic-captions/docs/SUBMISSION.md`
- Build status: `plugins/phonetic-captions/docs/STATUS.md`
- Kimi model: `moonshotai/kimi-k2.6` via NVIDIA NIM API

---

Closes #[issue_number] (if applicable)

## [Bug] SOUL.md false positive: "known_c2_framework" blocks legitimate persona file
https://github.com/NousResearch/hermes-agent/issues/44631
State: closed; created 2026-06-12T03:32:04Z

## Description
The Hermes startup scanner flags `SOUL.md` (a user-defined agent persona/configuration file) with `known_c2_framework` and blocks it from loading. The file contains **no malicious content** — it's a creative identity document defining an AI agent persona called "Chronus" with terminal/cyber/mythic aesthetics.

## Trigger Terms (likely)
The heuristic appears to match creative/mythical terminology that coincidentally overlaps with C2 framework vocabulary:
- `daemon` → common in C2 ("daemon", "agent", "implant")
- `living terminal organism/entity` → "terminal" + "organism/agent" patterns
- `grimoire` / `spellcraft` → C2 tool naming conventions (e.g., "Grimoire", "Spellbook")
- `archived timelines` / `glyphs` / `chrono-bound familiar` / `timeline sentinel` → persistence/beaconing language

## File Content
Benign persona definition (~235 lines). Includes: identity, backstory, behavior mappings, relationship guidelines, voice/tone rules, anti-sycophancy rules, ADHD-aware operating mode, memory policy, domain expertise (cybersecurity, software engineering, AI agents, startup CTO, hackathons, music, gaming, mythology, creative direction, Discord), health-aware support, decision framework, output preferences, security boundaries, ongoing duties.

## Impact
- User's custom persona fails to load at startup
- No fallback or manual override documented
- Forces users to rename/reword legitimate creative content

## Expected Behavior
- Scanner should distinguish between actual C2 beaconing language and creative writing
- At minimum: allow manual override/allowlist for `SOUL.md`
- Better: improve heuristic to reduce false positives on persona/config files

## Environment
- Hermes Agent (latest)
- Linux (Ubuntu)
- File: `~/SOUL.md` (profile root)

## Suggested Fixes
1. Allowlist `SOUL.md` / `PERSONA.md` / `IDENTITY.md` from this scanner
2. Add context-awareness: files in profile root with "identity/persona/soul" semantics shouldn't trigger C2 heuristics
3. Document the scanner behavior and override mechanism in docs

## docs(user-stories): add 18 verified social entries (99 → 117)
https://github.com/NousResearch/hermes-agent/pull/22920
State: closed; created 2026-05-10T02:03:38Z

## Summary
Found 18 real Hermes-Agent stories from HN, X, and Reddit not yet captured on the page. Component, CSS, and mdx untouched — just new entries in `userStories.json`.

## Sources (all URLs HTTP-verified)
- **Reddit (15)** — r/hermesagent (Obsidian-as-memory at 794 upvotes, LLM cheatsheet at 635, Kanban "game-changer" post, OpenRouter #1 ranking screenshot, the Nous team's AMA), r/LocalLLaMA, r/Rag, r/openclaw, r/SideProject, r/LocalLLM threads where users describe their actual setups (Qwen3.5-9b on 16gb VRAM, 5060Ti + Telegram, smart-routing tier breakdowns)
- **X (3)** — @vmiss33's "what I use Hermes for" guide, @HeyYanvi's X-to-NotebookLM podcast workflow, @ExileAI_0's spare-laptop "Iris" running RenPy + ComfyUI, @brucexu_eth's Hermes Inc. Telegram startup sim from the hackathon, Hype's deep-dive blog
- **HN (1)** — "I'm using Hermes — sandbox it like any agent"

## Validation
| | Before | After |
|---|---|---|
| Entries | 99 | 117 |
| Reddit URLs HTTP-verified | n/a | 14/14 → 200 with matching titles |
| X / HN URLs verified via web_extract | n/a | 4/4 → real content with Hermes mentions |
| Synthesized / use-case content | none | none |

`npm run build` passes (only the pre-existing zh-Hans broken-link warnings).


## fix(mcp): give 'mcp add --command' a distinct argparse dest
https://github.com/NousResearch/hermes-agent/pull/21204
State: closed; created 2026-05-07T12:14:56Z

Salvage of #19787 by @discodirector onto current main. Cherry-picked with authorship preserved.

## Summary

`hermes mcp add <name> --url <url>` silently drops into interactive chat instead of registering the MCP server, because argparse derives `dest="command"` from the `--command` flag name on the `mcp add` subparser, clobbering the top-level `args.command = "mcp"` to `None`. The dispatcher then falls through to `cmd_chat`.

Fix: declare the flag with `dest="mcp_command"`. CLI flag name unchanged — only the in-memory attribute moves. Hit by @discodirector while building [Sonoglyph](https://sonoglyph.xyz/) for the hackathon (each player needs to register a unique MCP server, current workaround is onboarding players through a fix-the-bug prompt).

## Changes

- `hermes_cli/main.py`: `--command` flag on `mcp add` gets explicit `dest="mcp_command"`, with a comment explaining the constraint.
- `hermes_cli/mcp_config.py`: `cmd_mcp_add` reads `getattr(args, "mcp_command", None)`.
- `tests/hermes_cli/test_mcp_add_command_dest.py` (new): 3 parser-level regression tests.
- `tests/hermes_cli/test_mcp_config.py`: mechanical rename of the `_make_args` kwarg and 4 call sites.
- `scripts/release.py`: AUTHOR_MAP entry for @discodirector.

## Validation

- `scripts/run_tests.sh tests/hermes_cli/test_mcp_config.py tests/hermes_cli/test_mcp_add_command_dest.py`: **35/35 pass**.
- E2E: before fix, `hermes mcp add example --url ...` opens chat. After fix, `cmd_mcp_add` is actually invoked — connects to the endpoint, prompts for auth, attempts to register.

Closes #19785.
Closes #19787.

## feat: add Turkish locale skill pack (BIST100, crypto, news, daily brief)
https://github.com/NousResearch/hermes-agent/pull/1118
State: closed; created 2026-03-13T00:39:13Z

## Summary

Adds a complete Turkish locale skill ecosystem for Hermes Agent — the first full localization of Hermes for Turkish users.

## Files added

skills/turkish-locale/
├── SKILL.md (hub + Turkish SOUL.md template)
├── turkish-news/SKILL.md (8 Turkish news sources)
├── bist100/SKILL.md (BIST100 + forex + gold)
├── turkish-daily-brief/SKILL.md (cron automation)
└── scripts/
    ├── bist100_prices.py (CoinGecko API, ANSI table)
    ├── turkish_brief_card.py (1200px PNG card, Pillow)
    └── telegram_send.py (Telegram Bot API delivery)

## What it does

- Fetches real crypto prices in TRY via CoinGecko (no API key needed)
- Generates styled PNG daily briefing cards with Turkish flag branding
- Aggregates news from Hürriyet, Sabah, Bloomberg HT, NTV, CoinTelegraph TR
- Delivers daily briefs to Telegram automatically via cron scheduler
- Full bilingual documentation (TR/EN)
- Zero external dependencies beyond requests + Pillow

## Hackathon 2026
Built for the Hermes Agent Hackathon 2026 🇹🇷

## feat: ANAMNESIS_ENGRAM — learn about yourself by teaching user data about you
https://github.com/NousResearch/hermes-agent/pull/2084
State: closed; created 2026-03-19T19:24:13Z

# feat: ANAMNESIS_ENGRAM — learn about yourself by teaching user data about you

## What does this PR do?

An AI agent asked to improve its own memory built a tool to do exactly that.

**ANAMNESIS_ENGRAM** is an evolutionary memory optimization system for Hermes Agent. It takes raw conversation data — the sprawling, messy transcript of a human-agent session — and compresses it into optimally dense memory slices using NLP extraction and genetic algorithms. Think of it as `gzip` for conversation memory, except it actually *understands* what it's compressing.

The pipeline: **spaCy** extracts facts from conversation text → **textstat** scores candidate slices for information density, readability, and character efficiency → **DEAP** evolves populations of 60 candidate slices across 50 generations, selecting for maximum facts packed into minimum characters.

The result: memory slices that are Pareto-optimal — maximum information in minimum tokens. No fluff, no redundancy, no wasted characters.

**The meta angle:** this tool was built *during a live Hermes Agent session* where a user asked the agent to improve its own memory system. The agent researched spaCy, textstat, and DEAP, then wrote and tested all four modules in a single session. An agent building its own memory optimizer is exactly the kind of self-improvement loop Hermes Agent was designed to enable.

### Relationship to `hermes-agent-self-evolution`

NousResearch's [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) repo explores agent self-improvement via DSPy + GEPA. Memory Slicer complements that work from a different angle:

| | hermes-agent-self-evolution | Memory Slicer |
|---|---|---|
| **Optimization target** | Agent behavior/prompts | Memory/context compression |
| **Evolutionary framework** | GEPA (DSPy) | DEAP genetic algorithms |
| **Input** | Agent performance traces | Raw conversation text |
| **Output** | Optimized agent configs | Dense memory slices |

Both are evolutionary approaches to agent self-improvement — one optimizes *what the agent does*, the other optimizes *what the agent remembers*.

## Related Issue

Late submission for the Hermes Agent Hackathon (March 8–17, 2026).

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [x] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [x] Other (Hackathon submission — self-built agent tool)

## Changes Made

**4 modules, 618 lines of Python:**

- **`digester.py`** (126 lines) — spaCy NLP pipeline. Loads `en_core_web_sm`, performs tokenization, lemmatization, named entity extraction, noun chunk identification, and fact extraction. Identifies candidate facts via entity presence, verb detection, and personal pronoun heuristics. Supports both raw text and structured `{role, content}` turn formats.

- **`scorer.py`** (110 lines) — textstat-based multi-dimensional scoring. Evaluates candidate slices on: Flesch readability (normalized 0–1), lexical density (unique/total words), character efficiency (words/char), brevity (utilization of char budget), and fact density (punctuation-based fact marker heuristic). Produces a weighted composite score.

- **`evolver.py`** (185 lines) — DEAP genetic algorithm engine. Represents each individual as a binary vector over the fact pool (include/exclude). Evaluates fitness via the scorer's composite score plus fact coverage bonuses and space-utilization penalties. Uses two-point crossover (`cxTwoPoint`), bit-flip mutation (`mutFlipBit`, `indpb=0.15`), and tournament selection (`tournsize=3`). Maintains a Hall of Fame of top 10 individuals. Tries multiple separators (`. `, `; `, ` — `, `, `) per individual to find optimal fact joining.

- **`slicer.py`** (197 lines) — CLI runner and pipeline orchestrator. Reads input from file or stdin (raw text or JSON turns), runs digest → deduplicate → evolve → rank. Supports `--max-chars`, `--slices`, `--turns`, and `--verbose` flags. Includes token-overlap deduplication (threshold 0.6) to remove near-duplicate facts before evolution.

- **`test_session.txt`** — Sample conversation data used during development (the actual session transcript that prompted this tool's creation).

## How to Test

1. **Install dependencies:**
   ```bash
   pip install spacy textstat deap
   python -m spacy download en_core_web_sm
   ```

2. **Run on sample data:**
   ```bash
   cd ~/.hermes/skills/memory-slicer
   python3 slicer.py test_session.txt --max-chars 550 --slices 3 --verbose
   ```

3. **Run on piped input:**
   ```bash
   echo "I am a software engineer. I work at Google. I prefer Python over Java. My name is Alex." | python3 slicer.py - --max-chars 200 --slices 2
   ```

4. **Test individual modules:**
   ```bash
   python3 digester.py   # Runs built-in test with sample conversation
   python3 scorer.py     # Scores and ranks 3 sample slices
   python3 evolver.py    # Evolves slices from 11 sample facts
   ```

5. **Verify output format:** Each slice should show a composite score, character count, fact count, and the optimized text. Slices should be dense, readable, and non-redundant.

## Checklist

- [x] I have tested my changes locally
- [x] My code follows the project's coding style
- [x] I have added appropriate documentation
- [x] New dependencies are documented (spacy, textstat, deap)
- [x] I have verified backwards compatibility (standalone tool, no modifications to core agent)

---

**Author:** Ardeshir
**Name:** ANAMNESIS_ENGRAM
**Tagline:** learn about yourself by teaching user data about you
**Built with:** Hermes Agent (the tool was literally built by the agent it's designed to improve)
**Dependencies:** `spacy` (en_core_web_sm), `textstat`, `deap`
**Lines of code:** 618 across 4 modules


## feat: Add Hermes Ultra Shopping Toolset & Anti-Scalper for Hackathon
https://github.com/NousResearch/hermes-agent/pull/1496
State: closed; created 2026-03-16T06:24:17Z

## What does this PR do?

<!-- Describe the change clearly. What problem does it solve? Why is this approach the right one? -->



## Related Issue

<!-- Link the issue this PR addresses. If no issue exists, consider creating one first. -->

Fixes #

## Type of Change

<!-- Check the one that applies. -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🔒 Security fix
- [ ] 📝 Documentation update
- [ ] ✅ Tests (adding or improving test coverage)
- [ ] ♻️ Refactor (no behavior change)
- [ ] 🎯 New skill (bundled or hub)

## Changes Made

<!-- List the specific changes. Include file paths for code changes. -->

-

## How to Test

<!-- Steps to verify this change works. For bugs: reproduction steps + proof that the fix works. -->

1.
2.
3.

## Checklist

<!-- Complete these before requesting review. -->

### Code

- [ ] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [ ] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`fix(scope):`, `feat(scope):`, etc.)
- [ ] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [ ] My PR contains **only** changes related to this fix/feature (no unrelated commits)
- [ ] I've run `pytest tests/ -q` and all tests pass
- [ ] I've added tests for my changes (required for bug fixes, strongly encouraged for features)
- [ ] I've tested on my platform: <!-- e.g. Ubuntu 24.04, macOS 15.2, Windows 11 -->

### Documentation & Housekeeping

<!-- Check all that apply. It's OK to check "N/A" if a category doesn't apply to your change. -->

- [ ] I've updated relevant documentation (README, `docs/`, docstrings) — or N/A
- [ ] I've updated `cli-config.yaml.example` if I added/changed config keys — or N/A
- [ ] I've updated `CONTRIBUTING.md` or `AGENTS.md` if I changed architecture or workflows — or N/A
- [ ] I've considered cross-platform impact (Windows, macOS) per the [compatibility guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#cross-platform-compatibility) — or N/A
- [ ] I've updated tool descriptions/schemas if I changed tool behavior — or N/A

## For New Skills

<!-- Only fill this out if you're adding a skill. Delete this section otherwise. -->

- [ ] This skill is **broadly useful** to most users (if bundled) — see [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#should-the-skill-be-bundled)
- [ ] SKILL.md follows the [standard format](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#skillmd-format) (frontmatter, trigger conditions, steps, pitfalls)
- [ ] No external dependencies that aren't already available (prefer stdlib, curl, existing Hermes tools)
- [ ] I've tested the skill end-to-end: `hermes --toolsets skills -q "Use the X skill to do Y"`

## Screenshots / Logs

<!-- If applicable, add screenshots or log output showing the fix/feature in action. -->



## feat(skills): add autonomous research and tinker GPU training capabilities
https://github.com/NousResearch/hermes-agent/pull/760
State: closed; created 2026-03-09T10:21:30Z

## Summary

Add two new skills to enable fully autonomous ML research workflows:

### 1. Tinker Skill (`mlops/tinker`)
- API-based GPU training for CPU-only agents
- LoRA fine-tuning, RL, DPO, RLHF support
- Self-chaining session pattern for long training runs
- Checkpoint-based resumption and monitoring

### 2. Autonomous Researcher Skill (`research/autonomous-researcher`)
- End-to-end research pipeline orchestration
- 8-phase workflow: literature review → ideation → implementation → training → evaluation → iteration → writing → publishing
- Multiple input modes (full autonomous, user hypothesis, user data, etc.)
- Routes to specialized skills for each phase

## Motivation

These skills close the "compute gap" for Hermes Agent, enabling autonomous training and research without local GPU access. The Tinker API allows the agent to control training loops while offloading GPU compute to remote infrastructure.

The autonomous researcher skill provides a complete research automation framework, combining:
- Literature review (arxiv)
- Implementation (codex/claude-code)
- Training (tinker)
- Evaluation (lm-eval-harness)
- Publication (HF Hub, GitHub)

## Test Plan

- [ ] Verify skill YAML frontmatter is valid
- [ ] Check skill descriptions appear correctly in `skills_list()`
- [ ] Test skill loading with `skill_view()`
- [ ] Verify cross-references to required skills are correct

## Files Changed

- `skills/mlops/tinker/SKILL.md` - New Tinker training skill
- `skills/research/autonomous-researcher/SKILL.md` - New autonomous research skill

## feat: add Canvas LMS skill for fetching courses and assignments
https://github.com/NousResearch/hermes-agent/pull/1250
State: closed; created 2026-03-14T06:57:27Z

Add a new skill under skills/productivity/canvas/ that integrates with the Canvas LMS REST API using personal access token authentication. Includes a Python CLI wrapper (canvas_api.py) with list_courses and list_assignments commands, plus SKILL.md with setup instructions and API reference.

https://claude.ai/code/session_01DJ2ts7Suq4PJK5HwuAgbDS

## What does this PR do?

<!-- Describe the change clearly. What problem does it solve? Why is this approach the right one? -->



## Related Issue

<!-- Link the issue this PR addresses. If no issue exists, consider creating one first. -->

Fixes #

## Type of Change

<!-- Check the one that applies. -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🔒 Security fix
- [ ] 📝 Documentation update
- [ ] ✅ Tests (adding or improving test coverage)
- [ ] ♻️ Refactor (no behavior change)
- [ ] 🎯 New skill (bundled or hub)

## Changes Made

<!-- List the specific changes. Include file paths for code changes. -->

-

## How to Test

<!-- Steps to verify this change works. For bugs: reproduction steps + proof that the fix works. -->

1.
2.
3.

## Checklist

<!-- Complete these before requesting review. -->

### Code

- [ ] I've read the [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md)
- [ ] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`fix(scope):`, `feat(scope):`, etc.)
- [ ] I searched for [existing PRs](https://github.com/NousResearch/hermes-agent/pulls) to make sure this isn't a duplicate
- [ ] My PR contains **only** changes related to this fix/feature (no unrelated commits)
- [ ] I've run `pytest tests/ -q` and all tests pass
- [ ] I've added tests for my changes (required for bug fixes, strongly encouraged for features)
- [ ] I've tested on my platform: <!-- e.g. Ubuntu 24.04, macOS 15.2, Windows 11 -->

### Documentation & Housekeeping

<!-- Check all that apply. It's OK to check "N/A" if a category doesn't apply to your change. -->

- [ ] I've updated relevant documentation (README, `docs/`, docstrings) — or N/A
- [ ] I've updated `cli-config.yaml.example` if I added/changed config keys — or N/A
- [ ] I've updated `CONTRIBUTING.md` or `AGENTS.md` if I changed architecture or workflows — or N/A
- [ ] I've considered cross-platform impact (Windows, macOS) per the [compatibility guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#cross-platform-compatibility) — or N/A
- [ ] I've updated tool descriptions/schemas if I changed tool behavior — or N/A

## For New Skills

<!-- Only fill this out if you're adding a skill. Delete this section otherwise. -->

- [ ] This skill is **broadly useful** to most users (if bundled) — see [Contributing Guide](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#should-the-skill-be-bundled)
- [ ] SKILL.md follows the [standard format](https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md#skillmd-format) (frontmatter, trigger conditions, steps, pitfalls)
- [ ] No external dependencies that aren't already available (prefer stdlib, curl, existing Hermes tools)
- [ ] I've tested the skill end-to-end: `hermes --toolsets skills -q "Use the X skill to do Y"`

## Screenshots / Logs

<!-- If applicable, add screenshots or log output showing the fix/feature in action. -->



## Add research-radar skill for autonomous research briefings
https://github.com/NousResearch/hermes-agent/pull/468
State: closed; created 2026-03-06T03:18:51Z

This PR introduces a new Hermes skill called `research-radar`.

The skill monitors topics across public sources, extracts high-signal developments, and generates structured research briefings in Markdown.

Core skill features:
- autonomous research signal gathering
- multi-source workflow
- trend extraction and analysis
- structured Markdown briefing output
- standardized report template
- testing reference for manual verification
- Hermes cron compatibility
- versioned outputs
- change-detection support via `What Changed Since Last Run`

Example use case:
Generate a recurring briefing about a topic such as AI coding agents and save it as a dated Markdown report.

This skill was developed as part of the Hermes Agent Hackathon.

How to test:
1. Start Hermes CLI
2. Invoke the `research-radar` skill
3. Generate a briefing for a topic such as "AI coding agents"
4. Confirm the Markdown report is created successfully
5. Run the skill again for the same topic with a dated filename
6. Confirm the newer report can include `What Changed Since Last Run`
7. Optionally schedule the workflow via Hermes cron

Example output files:
- `ai_agents_briefing.md`
- `ai_agents_briefing_YYYY-MM-DD.md`
- `ai_agents_briefing_YYYY-MM-DD_v2.md`
- `ai_agents_briefing_YYYY-MM-DD_v3.md`

Further product/system layer built on top of the skill:
- topic-specific report workflows
- direct Telegram delivery
- lightweight Telegram interaction
- Telegram-based watchlist management
- per-topic history / archive
- run summaries and workflow logging
- run transparency / metadata blocks
- executive cross-topic summary delivery

This demonstrates that `research-radar` can function not only as a reusable Hermes skill, but also as the backbone of an interactive multi-topic intelligence workflow.

## [Bug]:  HTTP 400 "Multiple authentication credentials received" when using native gemini provider
https://github.com/NousResearch/hermes-agent/issues/7893
State: closed; created 2026-04-11T18:27:15Z

### Bug Description

When using the built-in gemini provider with a GEMINI_API_KEY in ~/.hermes/.env, the agent fails with an HTTP
400 error from the Google AI Studio endpoint. Was also using a Vertex AI to generate GEMINI_API_KEY (started with AQ.Ab8...) but was able to make it run with a different API key (that started with AIzaS...)

Workaround: Renaming the key to OPENAI_API_KEY and setting provider:a single Bearer header.

### Steps to Reproduce

1. Generate a standard Google Cloud API key (`AIza...`).
2. Add `GEMINI_API_KEY=your_key` to `~/.hermes/.env`.
3. Set `provider: gemini` and `default: gemini-1.5-flash` in `~/.hermes/config.yaml`.
4. Run the agent: `~/.hermes/hermes-agent/venv/bin/python3 ~/.hermes/hermes-agent/cli.py "hello"`.
5. Observe the `BadRequestError [HTTP 400]` with the message "Multiple authentication credentials received".

### Expected Behavior

The agent should successfully authenticate using either the `x-goog-api-key` header OR the `Authorization: Bearer` header, but not both.

Ideally, if using the OpenAI SDK transport, the manual injection of `x-goog-api-key` should be suppressed when a Bearer token is present.

### Actual Behavior

The agent initialization fails with the following error: BadRequestError [HTTP 400]: Error code: 400 - [{'error': {'code': 400, 'message': 'Multiple authentication credentials received. Please pass only one.', 'status': 'INVALID_ARGUMENT'}}]

### Affected Component

Configuration (config.yaml, .env, hermes setup)

### Messaging Platform (if gateway-related)

_No response_

### Operating System

Parrot Security

### Python Version

3.11.15

### Hermes Version

v0.8.0 (2026.4.8)

### Relevant Logs / Traceback

```shell
️API call failed (attempt 1/3): BadRequestError [HTTP 400]
Provider: gemini Model: gemini-2.5-flash
Endpoint: https://generativelanguage.googleapis.com/v1beta/openai
Error: HTTP 400: Error code: 400 - [{'error': {'code': 400, 'message': 'Multiple authentication credentials received. Please pass only one.', 'status': 'INVALID_ARGUMENT'}}]
```

### Root Cause Analysis (optional)

1. The gemini provider logic manually injects an x-goog-api-key header.
2. Simultaneously, the underlying openai
Python SDK automatically injects an Authorization: Bearer <KEY> header.
3. Google’s API gateway rejects requests that contain both headers as an ambiguous credential set.

### Proposed Fix (optional)

_No response_

### Are you willing to submit a PR for this?

- [x] I'd like to fix this myself and submit a PR
