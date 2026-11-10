# Workbench Link

Workbench Link routes Hermes's native file tools and foreground terminal commands to one explicitly selected project on a Linux Docker worker. The worker connects outbound to a profile-owned broker; Hermes never selects a new local directory remotely.

**Experimental implementation checkpoint.** Native `read_file`, `patch`, `write_file`, `search_files` and foreground `terminal` are tested with Hermes v0.23.0. `execute_code` and background terminal jobs are explicitly refused: Hermes's persistent remote kernel needs background processes and concurrent file RPC that this implementation does not support yet. Full release gates remain open.

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

Plain HTTP requires explicit `--local-test` on both processes and loopback addresses. For a remote broker, use `https://` with a trusted certificate: `serve` accepts `--tls-cert` and `--tls-key`, and the worker accepts `--ca-file`. This remote TLS topology has not yet been exercised in the integration suite.

## State and limitations

The broker keeps durable grants, output chunks, cancellation intentions and receipts. Duplicate delivery uses the same operation identity. Known shell exit failures stay shell failures. Missing termination evidence becomes `OUTCOME_UNKNOWN` and fences the binding; a new operation ID cannot bypass it. Cancellation does not undo project edits.

Stop the foreground worker and broker with Ctrl-C. The in-container watchdog stops remaining children after lease loss. Timeout/cancellation can destroy scratch and shell state; the native adapter reports that loss. After an uncertain operation, inspect `status --json` and preserve the state directories. Human resolution/reset commands are not implemented yet; reconnecting or restarting does not clear a fence. `doctor` currently reports the same connection/binding status as `status`.

Project contents, command scripts, stdin and returned output are disclosed to Hermes and stored in private worker/broker state. Secrets already inside the selected project remain readable by commands. The watchdog is a failure-control mechanism for trusted project execution, not an isolation guarantee against hostile code running as the same container user.

Gateway concurrency, delegated/multiple environments, persistent `execute_code`, background jobs, automatic file sync, Windows/macOS workers, output-quota exhaustion and operator fence resolution remain release gates. The repository is not yet published in the Hermes catalog.

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
```

This development harness expects the source/runtime under this checkout's ignored `dev/` tree. It runs Hermes in a separate container with a server decoy, profile and private control socket, and no selected-project mount or Docker socket. The broker and project worker run outside it on the same local machine. It checks native routing, approval denial, file extraction, shell state, explicit unsupported calls and disconnected refusal. This is not a physical two-machine reliability test.

See [runtime evidence](docs/RUNTIME_EVIDENCE.md), [architecture](ARCHITECTURE.md), [implementation/release gates](docs/IMPLEMENTATION.md), [protocol](docs/PROTOCOL.md) and [product scope](PRODUCT.md). [Operations](docs/OPERATIONS.md) preserves the broader intended interface; commands beyond those shown here remain planned. [Direction and demand](DIRECTION_DECISION.md) and [sources](SOURCES.md) record the research behind the project.
