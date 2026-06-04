from datetime import date
from pathlib import Path

import typer
from pydantic import ValidationError

from wolf_prowl.classification import filter_relevant_candidates
from wolf_prowl.config import load_config
from wolf_prowl.digest import write_digest
from wolf_prowl.discovery import discover_sources
from wolf_prowl.storage import CandidateStore

app = typer.Typer(help="Discover and review contest, giveaway, sweepstakes, and auction leads.")
DEFAULT_CONFIG_PATH = Path("config/wolf-prowl.yaml")


@app.callback()
def main() -> None:
    """Wolf Prowl command line interface."""


@app.command()
def discover(config: Path = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c")) -> None:
    """Discover candidates from enabled RSS/Atom sources."""
    inserted, updated, candidate_count, source_count, filtered_count, errors = _discover(config)

    typer.echo(
        f"Discovered {candidate_count} candidates from {source_count} sources. "
        f"Filtered {filtered_count}. Inserted {inserted}, updated {updated}."
    )
    _echo_source_errors(errors)


@app.command()
def digest(
    config: Path = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c"),
    digest_date: str | None = typer.Option(None, "--date"),
) -> None:
    """Generate a local Markdown digest preview."""
    output_path, item_count = _digest(config, _parse_digest_date(digest_date))

    typer.echo(f"Wrote digest with {item_count} new discoveries to {output_path}.")


@app.command()
def run(
    config: Path = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c"),
    digest_date: str | None = typer.Option(None, "--date"),
) -> None:
    """Run the manual discovery and digest workflow."""
    inserted, updated, candidate_count, source_count, filtered_count, errors = _discover(config)
    output_path, item_count = _digest(config, _parse_digest_date(digest_date))

    typer.echo(
        f"Discovered {candidate_count} candidates from {source_count} sources. "
        f"Filtered {filtered_count}. Inserted {inserted}, updated {updated}."
    )
    _echo_source_errors(errors)
    typer.echo(f"Wrote digest with {item_count} new discoveries to {output_path}.")


def _discover(config: Path) -> tuple[int, int, int, int, int, list[str]]:
    try:
        app_config = load_config(config)
    except (FileNotFoundError, ValidationError) as error:
        raise typer.BadParameter(str(error), param_hint="--config") from error

    discovery_run = discover_sources(app_config.enabled_sources)
    filter_result = filter_relevant_candidates(discovery_run.candidates, app_config.topics)
    store = CandidateStore(app_config.database.path)
    inserted, updated = store.upsert_candidates(filter_result.candidates)

    errors = [f"{error.source}: {error.message}" for error in discovery_run.errors]
    return (
        inserted,
        updated,
        len(discovery_run.candidates),
        discovery_run.source_count,
        filter_result.filtered_count,
        errors,
    )


def _digest(config: Path, digest_date: date) -> tuple[Path, int]:
    try:
        app_config = load_config(config)
    except (FileNotFoundError, ValidationError) as error:
        raise typer.BadParameter(str(error), param_hint="--config") from error

    store = CandidateStore(app_config.database.path)
    items = store.list_new_digest_items()
    output_path = write_digest(
        items,
        app_config.digest.output_dir,
        app_config.digest.filename_template,
        digest_date,
    )
    return output_path, len(items)


def _parse_digest_date(value: str | None) -> date:
    if value is None:
        return date.today()
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise typer.BadParameter("Use YYYY-MM-DD format", param_hint="--date") from error


def _echo_source_errors(errors: list[str]) -> None:
    for error in errors:
        typer.echo(f"Source error: {error}", err=True)
