from pathlib import Path

from wolf_prowl.config import load_config


def test_load_config_filters_enabled_sources(tmp_path: Path) -> None:
    config_path = tmp_path / "wolf-prowl.yaml"
    config_path.write_text(
        """
database:
  path: data/test.duckdb
sources:
  - name: Enabled feed
    type: rss
    url: https://example.com/enabled.xml
    topics: [general]
    enabled: true
  - name: Disabled feed
    type: atom
    url: https://example.com/disabled.atom
    topics: [general]
    enabled: false
""".strip(),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.database.path == Path("data/test.duckdb")
    assert [source.name for source in config.enabled_sources] == ["Enabled feed"]
