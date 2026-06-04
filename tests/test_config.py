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


def test_load_config_generates_sources_from_topic_templates(tmp_path: Path) -> None:
    config_path = tmp_path / "wolf-prowl.yaml"
    config_path.write_text(
        """
topics:
  - name: cycling
    keywords:
      - cycling
      - mountain bike
    opportunity_terms:
      - giveaway
      - contest
    excluded_terms:
      - expired
source_templates:
  - name: Reddit search
    type: rss
    url_template: https://www.reddit.com/search.rss?q={query}&sort=new
    topics: [cycling]
    enabled: true
    max_queries_per_topic: 3
""".strip(),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert [source.name for source in config.generated_sources] == [
        "Reddit search: cycling: cycling giveaway",
        "Reddit search: cycling: cycling contest",
        "Reddit search: cycling: mountain bike giveaway",
    ]
    assert [str(source.url) for source in config.generated_sources] == [
        "https://www.reddit.com/search.rss?q=cycling+giveaway&sort=new",
        "https://www.reddit.com/search.rss?q=cycling+contest&sort=new",
        "https://www.reddit.com/search.rss?q=mountain+bike+giveaway&sort=new",
    ]
    assert [source.topics for source in config.generated_sources] == [["cycling"]] * 3


def test_disabled_source_templates_do_not_generate_sources(tmp_path: Path) -> None:
    config_path = tmp_path / "wolf-prowl.yaml"
    config_path.write_text(
        """
topics:
  - name: cycling
    keywords: [cycling]
    opportunity_terms: [giveaway]
source_templates:
  - name: Disabled search
    type: rss
    url_template: https://www.reddit.com/search.rss?q={query}&sort=new
    topics: [cycling]
    enabled: false
""".strip(),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.generated_sources == []
    assert config.enabled_sources == []
