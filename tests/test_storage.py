from datetime import UTC, datetime
from pathlib import Path

from wolf_prowl.discovery import Candidate
from wolf_prowl.storage import CandidateStore


def test_candidate_store_dedupes_by_key(tmp_path: Path) -> None:
    store = CandidateStore(tmp_path / "wolf_prowl.duckdb")
    candidate = Candidate(
        title="Original title",
        url="https://example.com/contest",
        source="Example feed",
        source_url="https://example.com/feed.xml",
        topics=("general",),
        description="Original summary",
        published_at=None,
        discovered_at=datetime(2026, 1, 1, tzinfo=UTC),
        dedupe_key="https://example.com/contest",
    )
    updated_candidate = Candidate(
        title="Updated title",
        url="https://example.com/contest",
        source="Example feed",
        source_url="https://example.com/feed.xml",
        topics=("general",),
        description="Updated summary",
        published_at=None,
        discovered_at=datetime(2026, 1, 2, tzinfo=UTC),
        dedupe_key="https://example.com/contest",
    )

    assert store.upsert_candidates([candidate]) == (1, 0)
    assert store.upsert_candidates([updated_candidate]) == (0, 1)
    assert store.count_candidates() == 1
