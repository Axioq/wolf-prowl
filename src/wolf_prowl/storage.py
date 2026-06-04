from datetime import datetime
from pathlib import Path

import duckdb

from wolf_prowl.discovery import Candidate


class CandidateStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                create table if not exists candidates (
                    id uuid primary key default uuid(),
                    title varchar not null,
                    url varchar not null,
                    source varchar not null,
                    source_url varchar not null,
                    topics varchar[] not null,
                    description varchar,
                    published_at timestamp,
                    discovered_at timestamp not null,
                    last_seen_at timestamp not null,
                    dedupe_key varchar not null unique,
                    status varchar not null default 'new'
                )
                """
            )

    def upsert_candidates(self, candidates: list[Candidate]) -> tuple[int, int]:
        inserted = 0
        updated = 0
        self.initialize()

        with self._connect() as connection:
            for candidate in candidates:
                existing = connection.execute(
                    "select id from candidates where dedupe_key = ?",
                    [candidate.dedupe_key],
                ).fetchone()

                if existing:
                    connection.execute(
                        """
                        update candidates
                        set last_seen_at = ?, title = ?, url = ?, source = ?, source_url = ?,
                            topics = ?, description = ?, published_at = ?
                        where dedupe_key = ?
                        """,
                        [
                            _strip_tz(candidate.discovered_at),
                            candidate.title,
                            candidate.url,
                            candidate.source,
                            candidate.source_url,
                            list(candidate.topics),
                            candidate.description,
                            _strip_tz(candidate.published_at),
                            candidate.dedupe_key,
                        ],
                    )
                    updated += 1
                    continue

                connection.execute(
                    """
                    insert into candidates (
                        title, url, source, source_url, topics, description, published_at,
                        discovered_at, last_seen_at, dedupe_key
                    ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        candidate.title,
                        candidate.url,
                        candidate.source,
                        candidate.source_url,
                        list(candidate.topics),
                        candidate.description,
                        _strip_tz(candidate.published_at),
                        _strip_tz(candidate.discovered_at),
                        _strip_tz(candidate.discovered_at),
                        candidate.dedupe_key,
                    ],
                )
                inserted += 1

        return inserted, updated

    def count_candidates(self) -> int:
        self.initialize()
        with self._connect() as connection:
            result = connection.execute("select count(*) from candidates").fetchone()
        return int(result[0])

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.path))


def _strip_tz(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value.replace(tzinfo=None)
