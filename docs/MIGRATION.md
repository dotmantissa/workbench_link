# Workspace migration — November 7, 2026

New standalone project: `/home/dotmantissa/hackathons/workbench_link`. Initialized an independent Git repository; nothing staged or committed.

Moved from `../hermes-plugin-hackathon`:

- `DIRECTION_DECISION.md`: active Workbench Link direction and judge-oriented boundaries.
- `SOURCES.md`: source/evidence register, including historical research context.
- Complete `research/`: collector, marketplace/entrant metadata and ignored raw source snapshots.

There were no plugin implementation files to move. `research/collect.py` is a research collector, not plugin runtime code. New module names in the architecture are planned files.

The previous `RESEARCH.md`, `BUILD_PLAN.md` and `JUDGE_REVIEW.md` remain in the old folder as explicitly superseded Data Clinic history. Their active-document links now point to this project. The migrated source register may cite historical filenames; those refer to that archive, not a second current build plan.

Relevant task/decision/verification history was migrated into the new project's ignored root TASKS.md. The old root checklist is an archive pointer. Each root has one canonical local recovery checklist; neither is staged/committed. Raw source snapshots stay ignored and were not executed.

The user's subsequent clarification is binding: one local test machine is available, and the plugin needs no frontend. The architecture therefore uses a local isolated test topology, CLI/native commands, and no Desktop/dashboard implementation.
