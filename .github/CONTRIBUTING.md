# Contributing

Workbench Link is a native Hermes execution backend with a standalone project worker. Start with the [architecture](../docs/architecture.md), [protocol](../docs/protocol.md) and [development instructions](../docs/testing.md).

Keep changes focused on a concrete behavior. Include reproduction steps for bugs and explain the resulting behavior in pull requests, with the checks you ran. Runtime changes should include tests for the affected failure path, especially operation identity, grants, output integrity or process ownership.

Maintain the Hermes directory-plugin entrypoint and the worker's independent imports. Use the public Hermes provider/environment interfaces; keep native tool approvals intact. Recovery must preserve unknown history and must not replay uncertain commands or clear fences automatically.

Run the unit suite for code changes. Changes to runner, transport, lifecycle or packaging also need the relevant Docker, native Hermes or clean-installation checks described in the testing guide. Keep documentation aligned with implemented behavior and record the tested source/runtime versions.
