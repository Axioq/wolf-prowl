from datetime import UTC, datetime
from pathlib import Path

from typer.testing import CliRunner

from wolf_prowl.cli import app
from wolf_prowl.discovery import Candidate


def test_discover_command_loads_config_and_persists_candidates(
    monkeypatch,
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "wolf_prowl.duckdb"
    config_path = tmp_path / "wolf-prowl.yaml"
    config_path.write_text(
        f"""
database:
  path: {database_path}
sources:
  - name: Enabled feed
    type: rss
    url: https://example.com/feed.xml
    topics: [general]
    enabled: true
""".strip(),
        encoding="utf-8",
    )

    def discover_fake_sources(sources):
        assert len(sources) == 1
        return [
            Candidate(
                title="Contest title",
                url="https://example.com/contest",
                source="Enabled feed",
                source_url="https://example.com/feed.xml",
                topics=("general",),
                description="Contest summary",
                published_at=None,
                discovered_at=datetime.now(UTC),
                dedupe_key="https://example.com/contest",
            )
        ]

    monkeypatch.setattr("wolf_prowl.cli.discover_sources", discover_fake_sources)

    result = CliRunner().invoke(app, ["discover", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "Discovered 1 candidates from 1 sources. Inserted 1, updated 0." in result.stdout
    assert database_path.exists()


def test_digest_command_writes_markdown(tmp_path: Path) -> None:
    database_path = tmp_path / "wolf_prowl.duckdb"
    digest_dir = tmp_path / "digests"
    config_path = tmp_path / "wolf-prowl.yaml"
    config_path.write_text(
        f"""
database:
  path: {database_path}
digest:
  output_dir: {digest_dir}
  filename_template: "{{date}}.md"
""".strip(),
        encoding="utf-8",
    )

    result = CliRunner().invoke(app, ["digest", "--config", str(config_path), "--date", "2026-06-04"])

    assert result.exit_code == 0
    assert "Wrote digest with 0 new discoveries" in result.stdout
    assert (digest_dir / "2026-06-04.md").exists()
