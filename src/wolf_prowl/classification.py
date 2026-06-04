from dataclasses import dataclass

from wolf_prowl.config import TopicConfig
from wolf_prowl.discovery import Candidate


@dataclass(frozen=True)
class FilterResult:
    candidates: list[Candidate]
    filtered_count: int


def filter_relevant_candidates(
    candidates: list[Candidate],
    topics: list[TopicConfig],
) -> FilterResult:
    topic_by_name = {topic.name: topic for topic in topics}
    kept: list[Candidate] = []

    for candidate in candidates:
        if _is_relevant(candidate, topic_by_name):
            kept.append(candidate)

    return FilterResult(candidates=kept, filtered_count=len(candidates) - len(kept))


def _is_relevant(candidate: Candidate, topic_by_name: dict[str, TopicConfig]) -> bool:
    candidate_topics = [topic_by_name[name] for name in candidate.topics if name in topic_by_name]
    if not candidate_topics:
        return True

    haystack = _candidate_text(candidate)
    for topic in candidate_topics:
        if _contains_any(haystack, topic.excluded_terms):
            return False

    filtering_topics = [topic for topic in candidate_topics if topic.keywords or topic.opportunity_terms]
    if not filtering_topics:
        return True

    return any(_matches_topic(haystack, topic) for topic in filtering_topics)


def _candidate_text(candidate: Candidate) -> str:
    return " ".join(
        part.lower()
        for part in [candidate.title, candidate.description, candidate.url]
        if part
    )


def _contains_any(haystack: str, needles: list[str]) -> bool:
    return any(needle.lower() in haystack for needle in needles)


def _matches_topic(haystack: str, topic: TopicConfig) -> bool:
    keyword_match = not topic.keywords or _contains_any(haystack, topic.keywords)
    opportunity_match = not topic.opportunity_terms or _contains_any(
        haystack,
        topic.opportunity_terms,
    )
    return keyword_match and opportunity_match
