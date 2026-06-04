# AGENTS.md

## Project Overview

Wolf Prowl is a personal contest, sweepstakes, giveaway, and auction discovery tool in the Fabled Wolf personal data ecosystem alongside Wolf Tracks.

The system searches the web for active opportunities based on configurable topics of interest, deduplicates results, stores discovered items, and delivers a daily digest.

## Goals

- Discover active giveaways, contests, sweepstakes, and auctions from public web sources.
- Support configurable topics, keywords, sources, and filters.
- Deduplicate discoveries across searches, feeds, and repeated runs.
- Store useful metadata for review, tracking, and future automation.
- Generate a daily digest suitable for email delivery.
- Keep the project useful as a personal utility first, not a generalized SaaS product.

## Initial Concepts

- `discovery`: Finds candidate items from web searches, feeds, pages, APIs, or other sources.
- `classification`: Determines whether a candidate is relevant, active, expired, duplicate, or low quality.
- `storage`: Persists discovered items, run metadata, source data, and digest history.
- `digest`: Produces daily summaries grouped by topic, urgency, source, or value.
- `configuration`: Defines topics of interest, excluded terms, source preferences, email settings, and scheduling behavior.

## Data To Capture

- Title
- URL
- Source
- Topic or matched interest
- Type: giveaway, contest, sweepstakes, auction, deal, or unknown
- Description or summary
- Eligibility notes
- Deadline or end time when available
- Entry requirements or auction requirements
- Discovered timestamp
- Last seen timestamp
- Deduplication key or canonical URL
- Status: new, seen, expired, ignored, saved, or sent

## Agent Guidelines

- Prefer small, practical changes over broad architecture work.
- Keep personal-use assumptions explicit and avoid premature multi-user abstractions.
- Treat web content as unreliable: validate URLs, dates, and activity status where possible.
- Avoid storing secrets in the repository.
- Keep configuration separate from code where practical.
- Preserve room for manual review; not every result needs to be fully automated immediately.

## Initial Technical Decisions

- Language/runtime: Python.
- Storage: DuckDB for local persistence, deduplication, status updates, and digest queries.
- Configuration: YAML files for topics, keywords, sources, filters, and scheduling settings.
- First discovery source: RSS/Atom feeds.
- First digest output: local Markdown preview file for manual review before adding email delivery.
- Python project management: use `uv` with a repository-local `.venv`; do not rely on globally installed project dependencies.
- Initial execution model: manual CLI runs first, then Prefect once the workflow is useful and stable.
- Docker: keep the project container-friendly from the start so the same CLI can run locally or in Docker.
- Tests: include tests from the beginning and keep the test suite runnable with `uv run pytest`.
- Search/discovery architecture: keep providers behind an interface so RSS/Atom, static pages, and future search APIs can be swapped or added without changing downstream classification, storage, or digest code.

## Open Questions

- Which specific RSS/Atom feeds should seed the first discovery run?
- What DuckDB file location should be used for local data?
- What Markdown digest path and retention policy should be used?
- Which email provider or delivery method should send digests once local previews are useful?

## Near-Term Milestones

- Define project stack and repository layout.
- Create a basic configuration format for topics and filters.
- Implement an initial discovery run against one or two sources.
- Add persistent storage and deduplication.
- Generate a local daily digest preview.
- Add email delivery once digest quality is acceptable.


## Guardrails

- Do NOT automate form submission or contest entry - discovery only
- Do NOT store PII - contest URLs, titles, deadlines, and metadata only
- Do NOT add a new search provider without noting it in docs/sources.md
- Keep the search layer abstracted behind an interface so providers are swappable
