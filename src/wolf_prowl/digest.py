from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


@dataclass(frozen=True)
class DigestItem:
    title: str
    url: str
    source: str
    topics: tuple[str, ...]
    description: str | None
    published_at: datetime | None
    discovered_at: datetime


def write_digest(
    items: list[DigestItem],
    output_dir: Path,
    filename_template: str,
    digest_date: date,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename_template.format(date=digest_date.isoformat())
    output_path.write_text(render_digest(items, digest_date), encoding="utf-8")
    return output_path


def render_digest(items: list[DigestItem], digest_date: date) -> str:
    lines = [f"# Wolf Prowl Digest - {digest_date.isoformat()}", "", "## New Discoveries", ""]

    if not items:
        lines.append("No new discoveries.")
        lines.append("")
        return "\n".join(lines)

    for item in items:
        lines.extend(_render_item(item))

    return "\n".join(lines)


def _render_item(item: DigestItem) -> list[str]:
    lines = [f"### {item.title}", ""]
    lines.append(f"- Source: {item.source}")
    lines.append(f"- Topics: {_format_topics(item.topics)}")
    lines.append(f"- URL: {item.url}")
    lines.append(f"- Published: {_format_datetime(item.published_at)}")
    lines.append(f"- Discovered: {_format_datetime(item.discovered_at)}")
    lines.append("")

    if item.description:
        lines.append(item.description.strip())
        lines.append("")

    return lines


def _format_topics(topics: tuple[str, ...]) -> str:
    if not topics:
        return "unknown"
    return ", ".join(topics)


def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return "unknown"
    return value.date().isoformat()
