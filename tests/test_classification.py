from datetime import UTC, datetime

from wolf_prowl.classification import filter_relevant_candidates
from wolf_prowl.config import TopicConfig
from wolf_prowl.discovery import Candidate


def test_filter_relevant_candidates_keeps_keyword_matches() -> None:
    candidates = [
        _candidate(title="Win a camera giveaway", description="Enter today"),
        _candidate(title="Unrelated post", description="Nothing useful here"),
    ]
    topics = [TopicConfig(name="giveaways", keywords=["giveaway"], excluded_terms=[])]

    result = filter_relevant_candidates(candidates, topics)

    assert result.candidates == [candidates[0]]
    assert result.filtered_count == 1


def test_filter_relevant_candidates_drops_excluded_terms() -> None:
    candidates = [_candidate(title="Camera giveaway", description="This contest is expired")]
    topics = [TopicConfig(name="giveaways", keywords=["giveaway"], excluded_terms=["expired"])]

    result = filter_relevant_candidates(candidates, topics)

    assert result.candidates == []
    assert result.filtered_count == 1


def test_filter_relevant_candidates_keeps_unknown_topics() -> None:
    candidate = _candidate(title="Unknown topic item", description=None, topics=("missing",))

    result = filter_relevant_candidates([candidate], [])

    assert result.candidates == [candidate]
    assert result.filtered_count == 0


def _candidate(
    title: str,
    description: str | None,
    topics: tuple[str, ...] = ("giveaways",),
) -> Candidate:
    return Candidate(
        title=title,
        url="https://example.com/item",
        source="Example feed",
        source_url="https://example.com/feed.xml",
        topics=topics,
        description=description,
        published_at=None,
        discovered_at=datetime.now(UTC),
        dedupe_key="https://example.com/item",
    )
