"""fetch-topics CLI tests with no network access."""

from __future__ import annotations

import json

from src.cli import main as cli_main
from src.contracts.feed_entry import FeedEntry
import src.feed.fetch as feed_fetch


def test_fetch_topics_json_outputs_topic_candidates_only(monkeypatch, capsys):
    def fake_fetch(url: str, *, timeout: int = 10) -> list[FeedEntry]:
        assert timeout == 3
        return [
            FeedEntry(title="AI Market Update", published="2026-05-20", source_url=url),
            FeedEntry(title="Old Entry", published="2026-05-10", source_url=url),
        ]

    monkeypatch.setattr(feed_fetch, "fetch_feed", fake_fetch)

    code = cli_main.main(
        [
            "fetch-topics",
            "https://example.com/feed.xml",
            "--format",
            "json",
            "--after",
            "2026-05-15",
            "--timeout",
            "3",
        ]
    )

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == [
        {
            "title": "AI Market Update",
            "published": "2026-05-20",
            "source": "https://example.com/feed.xml",
            "url": None,
            "summary": None,
            "source_title": None,
            "source_categories": [],
        }
    ]
    assert {"title", "published", "source"}.issubset(payload[0])


def test_fetch_topics_text_groups_titles_by_feed_source(monkeypatch, capsys):
    def fake_fetch(url: str, *, timeout: int = 10) -> list[FeedEntry]:
        return [
            FeedEntry(title=f"First from {url}", published=None, source_url=url),
            FeedEntry(title=f"Second from {url}", published=None, source_url=url),
        ]

    monkeypatch.setattr(feed_fetch, "fetch_feed", fake_fetch)

    code = cli_main.main(
        [
            "fetch-topics",
            "https://example.com/a.xml",
            "https://example.com/b.xml",
            "--format",
            "text",
            "--limit",
            "3",
        ]
    )

    assert code == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("# Source: https://example.com/a.xml (")
    assert lines[1] == "First from https://example.com/a.xml"
    assert lines[2] == "Second from https://example.com/a.xml"
    assert lines[3].startswith("# Source: https://example.com/b.xml (")
    assert lines[4] == "First from https://example.com/b.xml"


def test_fetch_topics_rejects_nonpositive_limit_before_fetch(monkeypatch, capsys):
    def fake_fetch(url: str, *, timeout: int = 10) -> list[FeedEntry]:
        raise AssertionError("fetch_feed should not run for invalid --limit")

    monkeypatch.setattr(feed_fetch, "fetch_feed", fake_fetch)

    code = cli_main.main(["fetch-topics", "https://example.com/feed.xml", "--limit", "0"])

    captured = capsys.readouterr()
    assert code == 1
    assert "--limit must be a positive integer" in captured.err


def test_fetch_topics_rejects_nonpositive_timeout_before_fetch(monkeypatch, capsys):
    def fake_fetch(url: str, *, timeout: int = 10) -> list[FeedEntry]:
        raise AssertionError("fetch_feed should not run for invalid --timeout")

    monkeypatch.setattr(feed_fetch, "fetch_feed", fake_fetch)

    code = cli_main.main(["fetch-topics", "https://example.com/feed.xml", "--timeout", "0"])

    captured = capsys.readouterr()
    assert code == 1
    assert "--timeout must be a positive integer" in captured.err
