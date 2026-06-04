from datetime import date, datetime
from pathlib import Path

from wolf_prowl.digest import DigestItem, render_digest, write_digest


def test_render_digest_includes_new_discoveries() -> None:
    markdown = render_digest(
        [
            DigestItem(
                title="Contest title",
                url="https://example.com/contest",
                source="Example feed",
                topics=("general",),
                description="Contest summary",
                published_at=datetime(2026, 1, 1),
                discovered_at=datetime(2026, 1, 2),
            )
        ],
        date(2026, 6, 4),
    )

    assert "# Wolf Prowl Digest - 2026-06-04" in markdown
    assert "### Contest title" in markdown
    assert "- Source: Example feed" in markdown
    assert "- Topics: general" in markdown
    assert "- URL: https://example.com/contest" in markdown
    assert "- Published: 2026-01-01" in markdown
    assert "Contest summary" in markdown


def test_write_digest_creates_markdown_file(tmp_path: Path) -> None:
    output_path = write_digest([], tmp_path / "digests", "{date}.md", date(2026, 6, 4))

    assert output_path == tmp_path / "digests" / "2026-06-04.md"
    assert output_path.read_text(encoding="utf-8") == (
        "# Wolf Prowl Digest - 2026-06-04\n\n"
        "## New Discoveries\n\n"
        "No new discoveries.\n"
    )
