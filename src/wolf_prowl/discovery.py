from dataclasses import dataclass
from datetime import UTC, datetime
from time import struct_time
from typing import Any

import feedparser

from wolf_prowl.config import SourceConfig


@dataclass(frozen=True)
class Candidate:
    title: str
    url: str
    source: str
    source_url: str
    topics: tuple[str, ...]
    description: str | None
    published_at: datetime | None
    discovered_at: datetime
    dedupe_key: str


def discover_feed(source: SourceConfig) -> list[Candidate]:
    feed = feedparser.parse(str(source.url))
    discovered_at = datetime.now(UTC)

    candidates: list[Candidate] = []
    for entry in feed.entries:
        url = _entry_url(entry)
        if not url:
            continue

        title = _entry_text(entry, "title") or url
        description = _entry_text(entry, "summary") or _entry_text(entry, "description")
        candidates.append(
            Candidate(
                title=title,
                url=url,
                source=source.name,
                source_url=str(source.url),
                topics=tuple(source.topics),
                description=description,
                published_at=_entry_published_at(entry),
                discovered_at=discovered_at,
                dedupe_key=_canonical_url(url),
            )
        )

    return candidates


def discover_sources(sources: list[SourceConfig]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for source in sources:
        candidates.extend(discover_feed(source))
    return candidates


def _entry_url(entry: dict[str, Any]) -> str | None:
    link = _entry_text(entry, "link")
    if link:
        return link

    links = entry.get("links") or []
    for candidate_link in links:
        href = candidate_link.get("href")
        if href:
            return str(href)

    return None


def _entry_text(entry: dict[str, Any], key: str) -> str | None:
    value = entry.get(key)
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _entry_published_at(entry: dict[str, Any]) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return None
    if isinstance(parsed, struct_time):
        return datetime(*parsed[:6], tzinfo=UTC)
    return None


def _canonical_url(url: str) -> str:
    return url.strip()
