from pathlib import Path

import typer
from pydantic import ValidationError

from wolf_prowl.config import load_config
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
    try:
        app_config = load_config(config)
    except (FileNotFoundError, ValidationError) as error:
        raise typer.BadParameter(str(error), param_hint="--config") from error

    candidates = discover_sources(app_config.enabled_sources)
    store = CandidateStore(app_config.database.path)
    inserted, updated = store.upsert_candidates(candidates)

    typer.echo(
        f"Discovered {len(candidates)} candidates from {len(app_config.enabled_sources)} sources. "
        f"Inserted {inserted}, updated {updated}."
    )


@app.command()
def run(config: Path = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c")) -> None:
    """Run the manual discovery and digest workflow."""
    discover(config=config)
