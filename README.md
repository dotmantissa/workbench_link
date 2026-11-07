# Workbench Link

A native Hermes plugin that lets Hermes running in one environment inspect, edit and test a selected project in another environment through its existing terminal and file tools.

**Status: architecture and research complete enough to start the integration spike; plugin implementation has not started.** No runtime, network deployment, adoption or cancellation result is claimed yet.

There is no frontend. The deliverable is a standalone directory plugin, a command-line local worker, and a small connection broker. Setup and recovery use CLI commands; a read-only slash command identifies the selected target.

Start with [ARCHITECTURE.md](ARCHITECTURE.md), then follow [the implementation sequence](docs/IMPLEMENTATION.md). Supporting contracts:

- [Product and scope](PRODUCT.md)
- [Hermes API evidence and runtime gates](docs/API_CONTRACTS.md)
- [Wire protocol and durable state](docs/PROTOCOL.md)
- [Installation, commands and recovery](docs/OPERATIONS.md)
- [Validation and release gates](docs/VALIDATION.md)
- [Direction decision](DIRECTION_DECISION.md) and [sources](SOURCES.md)
- [Migration record](docs/MIGRATION.md)

The available test hardware is one local machine. Development will simulate the Hermes host in an isolated container while a local worker operates a separate project environment. This can establish execution isolation and lifecycle correctness; it does not establish performance or reliability over a real remote network.

The project targets Hermes v0.23.0 or later, initially Linux with Docker. Backend selection is profile-scoped. These are design targets pending the integration gate, not a current compatibility claim.
