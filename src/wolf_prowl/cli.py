import typer

app = typer.Typer(help="Discover and review contest, giveaway, sweepstakes, and auction leads.")


@app.callback()
def main() -> None:
    """Wolf Prowl command line interface."""


@app.command()
def run() -> None:
    """Run the manual discovery and digest workflow."""
    typer.echo("Wolf Prowl workflow is not implemented yet.")
