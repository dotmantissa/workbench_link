# Workbench Link

Workbench Link routes Hermes's native file, terminal and code tools to one explicitly selected project on a Linux Docker worker. The worker connects outbound to a profile-owned broker; Hermes never selects a new local directory remotely.

**Version 0.1.0, verified with Hermes v0.23.0.** Native read/edit/test, persistent `execute_code` with tool RPC, and tracked background jobs run in the selected worker container. Receipts, process ownership and confirmed cleanup are tested in an isolated local topology. See the [measured evidence](docs/RUNTIME_EVIDENCE.md) for the tested scope.

There is no frontend or replacement shell/file toolset. Management uses `hermes workbench-link`; `/workbench-link` shows the current profile binding. Registration starts no services.

## Local setup

Use a dedicated Hermes profile with one foreground CLI session, Hermes v0.23.x and `plugins.isolation: in_process`. The worker requires Python 3.11+ and authorized Docker daemon access; use Hermes's supported runtime on its host. The package has no third-party runtime dependencies.

Install the directory plugin through Hermes's normal plugin discovery: place a clean checkout at your selected profile's `plugins/workbench-link`, then run `hermes plugins enable workbench-link`. Keep disposable development runtimes outside an installed plugin directory. Validate it with:

```sh
hermes plugins doctor /absolute/path/to/workbench-link --ci
hermes plugins validate /absolute/path/to/workbench-link --install-deps
```

Create one random shared key of 32–128 bytes, encoded as lowercase hexadecimal. Supply it deliberately to both processes through `WORKBENCH_LINK_TOKEN`, or use the plugin's secret setting on Hermes and the worker's hidden prompt. Do not put the key in command arguments or URLs. For an environment-based setup, read it without echo in each launch shell:

```sh
read -rsp 'Workbench key: ' WORKBENCH_LINK_TOKEN
export WORKBENCH_LINK_TOKEN
```

In the dedicated profile's `config.yaml`, merge these settings with existing configuration:

```yaml
plugins:
  isolation: in_process
  enabled: [workbench-link]
  entries:
    workbench-link:
      settings:
        worker_id: local-dev
        project_alias: project
        # Optional: an absolute private directory, useful for long Unix socket paths.
        control_dir: /absolute/private/short/control
terminal:
  backend: workbench_link
  cwd: /workspace
```

Start the broker explicitly in one Hermes host shell:

```sh
hermes workbench-link serve --listen 127.0.0.1 --port 8765 --local-test
```

Build the worker image from this source checkout and inspect its immutable image ID:

```sh
docker build -t workbench-link-worker:dev .
docker image inspect workbench-link-worker:dev --format '{{.Id}}'
```

In another shell on the project machine, run the worker from this checkout, supplying the printed full `sha256:…` image ID:

```sh
python -m workbench_link.worker \
  --broker http://127.0.0.1:8765 \
  --worker-id local-dev --alias project \
  --project /absolute/path/to/selected-project \
  --image sha256:YOUR_INSPECTED_IMAGE_ID \
  --state-dir /absolute/private/worker-state \
  --local-test
```

The selected directory must be owned and writable by the worker user. New state directories are created with mode 0700. The worker prints the exact project, instance and image identities; it mounts that project at `/workspace` with write access. The container runs as the worker user's UID/GID with no network, Docker socket or host-home mount, a read-only root, dropped capabilities and bounded resources.

Inspect and accept the printed identities on the Hermes host:

```sh
hermes workbench-link status --json
hermes workbench-link bind \
  --instance-id PRINTED_INSTANCE_UUID \
  --project-id PRINTED_PROJECT_UUID \
  --image sha256:YOUR_INSPECTED_IMAGE_ID
hermes workbench-link status
```

Start a new Hermes session in that profile. Use its native tools to read a file, patch a bug and run project tests with a foreground command such as `python test_project.py`. Normal Hermes approvals still apply. A denial creates no worker operation.

Plain HTTP requires explicit `--local-test` on both processes and loopback addresses. For a remote broker, use `https://` with a trusted certificate: `serve` accepts `--tls-cert` and `--tls-key`, and the worker accepts `--ca-file`. Certificate trust, hostname checks and handshake capacity are tested locally. Physical two-machine deployment and WAN behavior remain unmeasured.

## State and limitations

The broker keeps durable grants, output chunks, cancellation intentions and receipts. Duplicate delivery uses the same operation identity. Known shell exit failures stay shell failures. Missing termination evidence becomes `OUTCOME_UNKNOWN` and fences the binding; a new operation ID cannot bypass it. Cancellation does not undo project edits.

Use `hermes workbench-link stop` to request environment cleanup; keep the broker and worker running until stopped evidence arrives. `reset` requires stopped environments and reconciled outcomes, then creates a new generation. Start a new Hermes session after reset or container loss. Ctrl-C shuts down each foreground service; the container watchdog stops children on lease loss. Cancellation does not undo project edits.

Inspect uncertainty with `operations --json`, `inspect OPERATION_UUID --json` and `recover --json`. Recover reads receipts and never replays a command or clears a fence. For an irreducible `UNKNOWN`, restart the same worker state to stop recorded containers, inspect the project locally, then run `resolve OPERATION_UUID --note 'Your inspection findings'` from a human terminal. It requires typing the complete operation ID and preserves unknown history. After reconciliation, run `reset`; if the worker restarted, bind its new printed instance. `inspect OPERATION_UUID --output` explicitly writes retained output bytes to stdout.

Project contents, command scripts, stdin and returned output are disclosed to Hermes and stored in private worker/broker state. Secrets already inside the selected project remain readable by commands. The watchdog is a failure-control mechanism for trusted project execution, not an isolation guarantee against hostile code running as the same container user.

Supported scope is one foreground CLI session and environment per profile. Additional environments are refused. Gateway multiplexing, delegated workspace isolation, PTY/interactive background stdin, jobs that outlive environment closure (`persist_on_release`), automatic file sync and Windows/macOS workers are outside this release. Native background log/poll/wait/kill work through Hermes's existing process tools. Output is capped at 16 MiB per operation; incomplete output fails instead of becoming successful file data. Private spools have a 512 MiB quota and are retained until operator maintenance; automatic timed deletion is not implemented. Preserve unresolved state. The repository is not yet listed in the Hermes catalog.

## Reproduce the checks

```sh
python -m unittest discover -s tests/unit -v
python tests/integration/worker_smoke.py --image sha256:YOUR_INSPECTED_IMAGE_ID
python tests/integration/worker_faults.py --image sha256:YOUR_INSPECTED_IMAGE_ID
```

For real native routing, prepare a disposable pinned Hermes v0.23.0 source/runtime using its supported workflow, then run:

```sh
HERMES_HOME="$PWD/dev/runtime/hermes-home" \
HERMES_RUNTIME_DIR="$PWD/dev/runtime/hermes-home" \
  "$PWD/dev/hermes/scripts/run-in-hermes-env" python \
  tests/integration/native_smoke.py \
  --hermes-source "$PWD/dev/hermes" \
  --image sha256:YOUR_INSPECTED_IMAGE_ID

HERMES_HOME="$PWD/dev/runtime/hermes-home" \
HERMES_RUNTIME_DIR="$PWD/dev/runtime/hermes-home" \
  "$PWD/dev/hermes/scripts/run-in-hermes-env" python \
  tests/integration/install_smoke.py --hermes-source "$PWD/dev/hermes"
```

This development harness expects the source/runtime under this checkout's ignored `dev/` tree. It runs Hermes in a separate container with a server decoy, profile and private control socket, and no selected-project mount or Docker socket. The broker and project worker run outside it on the same local machine. It checks native routing, approval denial, file extraction, shell state, persistent kernels, background lifecycle, profile refusal, confirmed cleanup and disconnected refusal. The install harness checks a fresh dedicated profile using the already installed disposable Hermes runtime. This is not a physical two-machine reliability test.

See [runtime evidence](docs/RUNTIME_EVIDENCE.md), [architecture](ARCHITECTURE.md), [implementation/release gates](docs/IMPLEMENTATION.md), [protocol](docs/PROTOCOL.md) and [product scope](PRODUCT.md). [Operations](docs/OPERATIONS.md) documents the implemented management and recovery commands. [Direction and demand](DIRECTION_DECISION.md) and [sources](SOURCES.md) record the research behind the project.
