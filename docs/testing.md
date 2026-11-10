# Development and testing

Use Linux, Python 3.11+ and Docker with access granted to the current user. Unit tests use the standard library and OpenSSL. Integration tests select only generated fixtures; they need no model credentials or paid inference.

## Unit and packaging checks

```sh
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/python -W error::ResourceWarning -m unittest discover -s tests/unit -v
.venv/bin/python -m pip check
.venv/bin/python -m pip wheel --no-deps --wheel-dir dist .
```

The tests cover schemas and HMAC, actual private/TLS sockets, cancellation/grant races, output integrity, restart fences, migration, disk/quota failures and operator resolution. A wheel supplies the standalone worker/library. The source distribution also includes the root plugin entrypoint, manifest, Docker build files, documentation and tests.

## Docker integration

```sh
docker build -t workbench-link-worker:test .
WBL_IMAGE_ID="$(docker image inspect workbench-link-worker:test --format '{{.Id}}')"
.venv/bin/python tests/integration/worker_smoke.py --image "$WBL_IMAGE_ID"
.venv/bin/python tests/integration/worker_faults.py --image "$WBL_IMAGE_ID"
```

The smoke suite checks exact bytes, selected-mount policy, duplicate delivery, lost terminal HTTP acknowledgements and operator recovery. The fault suite checks foreground/session output, quotas, inherited-pipe capture, cancel/timeout, worker/runner death and broker restart, including detached jobs after a completed launch. Use `--scenario runner_death` to run an individual case.

The [CI workflow](../.github/workflows/ci.yml) runs unit and wheel checks on Python 3.11 and 3.14, plus Docker smoke/fault checks on Python 3.14. It uses read-only repository permissions and pinned GitHub Actions. It does not publish packages or images.

## Native Hermes and installation checks

The native harness runs real Hermes discovery and native tool dispatch in a separate container with a server decoy. That container has no selected-project mount, Docker socket or network. The worker and broker run outside it. The harness checks approvals, file/code tools, kernel RPC, shell state, background lifecycle, profile refusal and cleanup.

Prepare an isolated Hermes checkout under `dev/hermes` and use its supported package manager:

```sh
mkdir -p dev/runtime/hermes-home
git clone --branch v0.23.0 --depth 1 https://github.com/NousResearch/hermes-agent.git dev/hermes
git -C dev/hermes rev-parse HEAD
# Expected: 2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19

export HERMES_HOME="$PWD/dev/runtime/hermes-home"
export HERMES_RUNTIME_DIR="$HERMES_HOME"
dev/hermes/scripts/run-in-hermes-env python --version

dev/hermes/scripts/run-in-hermes-env python tests/integration/native_smoke.py \
  --hermes-source dev/hermes --image "$WBL_IMAGE_ID"
dev/hermes/scripts/run-in-hermes-env python tests/integration/install_smoke.py \
  --hermes-source dev/hermes
```

The installation harness creates a clean named profile using the installed disposable Hermes runtime. It checks enablement, Doctor, CLI help/status, missing-key refusal and unsupported host isolation. It removes its own profile afterward. First-time Hermes dependency/tool downloads are a separate prerequisite and may take longer than plugin installation.

Validate a clean plugin checkout through the supported runtime:

```sh
hermes plugins doctor /absolute/path/to/workbench-link --ci
hermes plugins validate /absolute/path/to/workbench-link --install-deps
```

Keep the disposable Hermes runtime outside a directory passed to Doctor or catalog validation; their staging must not recursively copy runtime/state. For source development with `dev/` inside this checkout, stage only the root entrypoint, manifest, package metadata, README, license and `workbench_link/` into a separate clean directory before validation.

## Reporting results

Record the source revision, Hermes/Python/Docker versions, inspected image ID, topology and observed failures with each integration result. [Verification](verification.md) records the current release coverage. Local isolated testing does not establish WAN/NAT, other-platform or live-model behavior. Command output and state can contain project data; share only reviewed fixture results.
