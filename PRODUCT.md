# Workbench Link product brief

## Purpose

Let a user keep Hermes reasoning, memory and skills in one execution environment while the same native file, terminal and code tools operate on one explicitly selected local project. Make the execution target predictable across reading, editing and testing.

## Users and demand

The initial user is an individual developer who runs Hermes separately from the machine containing the project. This is a proposed target audience supported by concrete issue discussions, not measured adoption. The builder is solo and currently has one local machine for testing.

[Issue #18715](https://github.com/NousResearch/hermes-agent/issues/18715) explicitly requests a remote agent with local tools. Core SSH already covers reachable machines. Talaria already provides remote device tools; the inspected README says native Hermes terminal/file tools are not rerouted. Workbench Link must prove an advantage in the complete native read/edit/test workflow, rather than claim remote execution is new.

## Deliverable

A Python native terminal-environment plugin with a bundled worker and broker. No frontend, Desktop extension, dashboard, browser automation or separate agent framework. Management is through explicit CLI commands and a read-only in-session status command.

## Winning-quality outcome

An ordinary Hermes task reads a file, patches it and runs tests against the selected project using native tools. The server's corresponding fixture remains unchanged. A denied dangerous operation does not reach the worker. A disconnect produces an honest unavailable or uncertain state and never redirects execution or repeats an uncertain write.

The hackathon scores usefulness, reliability, polish and creativity; published weights are unknown. These outcomes support a competitive entry but do not imply a guaranteed placement.

## Confirmed constraints

- Solo builder collaborating with Codex; no blockchain.
- Local-only hardware currently available; no remote machine prerequisite for implementation.
- One Hermes host, one worker, one selected project, one active CLI session/profile binding initially.
- Native public provider API, normal Hermes approval handling, no core monkey-patching.
- Worker selects its own project path; server cannot request host mounts.
- Profile-scoped backend selection; separate profile for server-executed automation.
- No direct credential-store reads, self-updating source or automatic uncertain-command replay.

## Implemented engineering decisions

Linux/Docker first; Python standard library for transport and persistence; a separate broker process; private Unix control socket; worker-initiated authenticated HTTP polling; HTTPS for any non-loopback connection; full native environment lifecycle testing before release.

Verified on Linux/WSL Ubuntu-26.04 with Docker 29.1.3, standalone Python 3.11.17 and Hermes's supported Python 3.14.9 runtime. Native persistent kernels/background jobs and durable cleanup are implemented; measured evidence and limits are in docs/RUNTIME_EVIDENCE.md. Physical remote deployment and other operating systems require their own validation.
