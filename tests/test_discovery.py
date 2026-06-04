from time import gmtime

from feedparser.util import FeedParserDict

from wolf_prowl.config import SourceConfig
from wolf_prowl.discovery import discover_feed


def test_discover_feed_normalizes_entries(monkeypatch) -> None:
    source = SourceConfig(
        name="Example feed",
        type="rss",
        url="https://example.com/feed.xml",
        topics=["general"],
        enabled=True,
    )

    def parse_feed(url: str) -> FeedParserDict:
        assert url == "https://example.com/feed.xml"
        return FeedParserDict(
            entries=[
                FeedParserDict(
                    title="Contest title",
                    link="https://example.com/contest",
                    summary="Contest summary",
                    published_parsed=gmtime(0),
                ),
                FeedParserDict(title="Missing link"),
            ]
        )

    monkeypatch.setattr("wolf_prowl.discovery.feedparser.parse", parse_feed)

    candidates = discover_feed(source)

    assert len(candidates) == 1
    assert candidates[0].title == "Contest title"
    assert candidates[0].url == "https://example.com/contest"
    assert candidates[0].source == "Example feed"
    assert candidates[0].topics == ("general",)
    assert candidates[0].description == "Contest summary"
    assert candidates[0].dedupe_key == "https://example.com/contest"
    assert candidates[0].published_at is not None
