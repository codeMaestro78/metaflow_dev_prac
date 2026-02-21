# Codebase Contribution Guide

This repository is the Metaflow framework: a Python-first system for authoring, running, and operating ML/data workflows from local development to production orchestration.

## High-level map

- **`metaflow/`**: Main Python package (runtime, CLI, plugins, client APIs, decorators, datastore, metadata, runners).
- **`test/`**: Unit, integration/core, and data-layer tests.
- **`R/`**: R package bindings and docs.
- **`docs/`**: Architecture and feature docs/images.
- **Root packaging files** (`setup.py`, `MANIFEST.in`, `setup.cfg`): distribution and installation metadata.

## Runtime architecture (most critical paths)

The project explicitly treats the following as the most sensitive paths for correctness and regression risk:

1. **Execution engine**: `metaflow/runtime.py`, `metaflow/task.py`, `metaflow/flowspec.py`.
2. **CLI plumbing**: `metaflow/cli.py`, `metaflow/cli_components/`.
3. **Datastore and metadata internals**: `metaflow/datastore/`, `metaflow/plugins/datastores/`, `metaflow/metadata_provider/`.
4. **Decorators and graph semantics**: `metaflow/decorators.py`, `metaflow/graph.py`, parameter/config modules.
5. **Orchestration plugins**: Argo, Step Functions, Kubernetes, Batch integrations under `metaflow/plugins/`.

## Recommended contribution priorities

If you want high-impact contributions with clear user value, prioritize:

1. **Tests in `test/core/tests/` and `test/unit/`**
   - Improve coverage for edge cases in foreach/switch/resume/retry and card behavior.
   - Add regression tests for reported issues before touching core runtime.

2. **Core runtime bug fixes with strong reproductions**
   - Fixes in `runtime.py` / `task.py` / `flowspec.py` are impactful, but require minimal reproducible tests due to high blast radius.

3. **Plugin reliability and cloud parity**
   - Datastore and orchestrator plugin fixes are practical contributions for production users.

4. **Developer UX improvements**
   - CLI ergonomics and error messaging in `metaflow/cli.py` and `metaflow/cli_components/`.

5. **Docs and examples**
   - Tutorial updates and architecture docs to reduce onboarding time.

## File-by-file reading strategy for new contributors

Given the repository size, read in this order:

1. `README.md` and `CONTRIBUTING.md` for purpose and contribution bar.
2. `metaflow/__init__.py` to understand public API surface.
3. `metaflow/cli.py` + `metaflow/cli_components/` for command entry and UX.
4. `metaflow/flowspec.py`, `metaflow/runtime.py`, `metaflow/task.py` for execution semantics.
5. `metaflow/plugins/__init__.py` to see extension points and plugin registry.
6. `test/README.md`, then `test/core/tests/` and `test/unit/` for expected behavior.

## Practical “first PR” ideas

- Add/strengthen a regression test in `test/core/tests/` for a known edge case.
- Improve a user-facing error message in CLI for invalid input or configuration mismatch.
- Add a focused unit test around a plugin parser/utility with low runtime coupling.
- Improve docs for an existing decorator or orchestration path.


## What should I do right now? (concrete next steps)

If you are asking "what should I do?", use this 7-step path:

1. Pick **one** small issue (bug or UX pain), ideally one that can be validated locally.
2. Reproduce it in the smallest possible flow or unit test.
3. Add a failing test first in `test/unit/` or `test/core/tests/`.
4. Implement the minimal fix (avoid mixing refactors).
5. Run targeted tests locally and capture exact commands + outputs.
6. Write a PR description with:
   - problem statement,
   - root cause,
   - why the fix is correct,
   - what edge cases were tested.
7. If your change touches core runtime files (`runtime.py`, `task.py`, `flowspec.py`), include an issue link and a clear reproduction before requesting review.

### Best first contribution options

- Add a regression test for an edge case in foreach/switch/resume behavior.
- Improve a confusing CLI error message and add a test for that message.
- Fix a plugin/datastore bug with a focused, well-scoped test.

### What to avoid for your first PR

- Large refactors across runtime + plugins in one change.
- Behavior changes without tests.
- "cleanup-only" PRs that don’t solve a user-visible problem.
