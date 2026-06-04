# Wolf Prowl

Wolf Prowl is a personal contest, sweepstakes, giveaway, and auction discovery utility in the Fabled Wolf ecosystem.

The first version will run manually, discover candidates from RSS/Atom feeds, store deduplicated results in DuckDB, and generate local Markdown digest previews for review.

## Initial Stack

- Python managed with `uv`
- DuckDB for local persistence
- YAML configuration
- RSS/Atom discovery first
- Local Markdown digest previews
- Manual CLI execution first
- Docker support during development and future scheduled runs
- Prefect later, after the manual workflow is reliable

## Local Setup

This project expects a local virtual environment at `.venv/`. The environment is created and managed with `uv`; project dependencies are not installed globally.

If `uv` is already available on your system, run:

```bash
uv venv
uv sync
```

If `uv` is not installed and you want to keep the binary repo-local, run:

```bash
./scripts/bootstrap-uv.sh
.local/bin/uv venv
.local/bin/uv sync
```

This installs the `uv` binary under `.local/bin/` and creates the project environment at `.venv/`. Both paths are ignored by git.

Activate the environment if you want shell access to installed tools:

```bash
source .venv/bin/activate
```

You can also run commands through `uv` without activating the environment:

```bash
uv run pytest
uv run wolf-prowl --help
```

With the repo-local binary, use:

```bash
.local/bin/uv run pytest
.local/bin/uv run wolf-prowl --help
```

## Planned Commands

The initial CLI should grow toward these commands:

```bash
wolf-prowl discover
wolf-prowl digest
wolf-prowl run
```

`discover` loads enabled RSS/Atom sources, normalizes feed entries, filters them with configured topic keywords and excluded terms, and persists them to DuckDB with URL-based deduplication.

`digest` generates a local Markdown preview from stored candidates with `status = 'new'`.

`run` performs the current end-to-end manual workflow: discover candidates, persist results, and generate a digest preview.

Use `--date YYYY-MM-DD` with `digest` or `run` when you want a deterministic output filename for testing or backfills.

## Configuration

Start from `config/wolf-prowl.example.yaml` and create a local config when the implementation needs real feeds.

Do not store secrets in config files committed to the repository.

For manual live-feed testing, copy `config/wolf-prowl.real-feeds.example.yaml` to `config/wolf-prowl.local.yaml`, enable one to three sources, and run with `--config config/wolf-prowl.local.yaml`. The local config is ignored by git.

For a topic-driven example, copy `config/wolf-prowl.cycling.example.yaml` to `config/wolf-prowl.local.yaml`. It uses `source_templates` to generate Reddit RSS searches for cycling giveaways, contests, and sweepstakes.

## Docker

Docker support is planned from the start so the same CLI can run locally or in a container. The first Docker image should run the manual CLI. Prefect orchestration can wrap the same command later.

## Automation

Automation is intentionally deferred until the manual workflow is useful and trustworthy. Prefect is the preferred scheduler/orchestrator once discovery, storage, and digest generation are stable.

## Development

Run tests with:

```bash
uv run pytest
```

Generated runtime data belongs in `data/` and generated digest previews belong in `digests/`. Both are ignored by git.
