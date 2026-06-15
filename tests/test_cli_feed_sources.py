"""CLI tests for OPML-backed RSS source listing and fetching."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from src.cli.main import main
from src.contracts.feed_entry import FeedEntry
from src.contracts.feed_source import FeedSource


def _rss_data_url() -> str:
    xml = (
        '<rss version="2.0"><channel>'
        '<item><title>Smoke Topic</title>'
        '<link>https://example.com/smoke</link>'
        '<description>Smoke summary</description>'
        '<pubDate>Mon, 25 May 2026 09:00:00 +0900</pubDate>'
        '</item></channel></rss>'
    )
    return "data:application/rss+xml," + quote(xml, safe="")


def _empty_rss_data_url() -> str:
    xml = '<rss version="2.0"><channel><title>Empty</title></channel></rss>'
    return "data:application/rss+xml," + quote(xml, safe="")


def _invalid_feed_data_url() -> str:
    xml = "<notfeed />"
    return "data:application/xml," + quote(xml, safe="")


def _write_opml(tmp_path: Path) -> Path:
    opml = tmp_path / "feeds.opml"
    opml.write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <body>
    <outline text="News">
      <outline text="Smoke Feed" xmlUrl="{_rss_data_url()}" htmlUrl="https://example.com/feed" />
    </outline>
  </body>
</opml>
""",
        encoding="utf-8",
    )
    return opml


def _write_mixed_opml(tmp_path: Path) -> Path:
    opml = tmp_path / "mixed.opml"
    opml.write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <body>
    <outline text="News">
      <outline text="Smoke Feed" xmlUrl="{_rss_data_url()}" />
      <outline text="Empty Feed" xmlUrl="{_empty_rss_data_url()}" />
      <outline text="Broken Feed" xmlUrl="{_invalid_feed_data_url()}" />
    </outline>
  </body>
</opml>
""",
        encoding="utf-8",
    )
    return opml


def _write_empty_opml(tmp_path: Path) -> Path:
    opml = tmp_path / "empty.opml"
    opml.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <body>
    <outline text="Empty Folder">
      <outline text="No Feed Here" />
    </outline>
  </body>
</opml>
""",
        encoding="utf-8",
    )
    return opml


def test_cli_list_feed_sources_json(tmp_path, capsys):
    opml = _write_opml(tmp_path)

    code = main(["list-feed-sources", "--opml", str(opml), "--format", "json"])

    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["title"] == "Smoke Feed"
    assert data[0]["categories"] == ["News"]
    assert data[0]["reader"] == "opml"


def test_cli_list_feed_sources_markdown(tmp_path, capsys):
    opml = _write_opml(tmp_path)

    code = main(["list-feed-sources", "--opml", str(opml), "--format", "markdown"])

    assert code == 0
    out = capsys.readouterr().out
    assert "| categories | title | feed_url | html_url | reader |" in out
    assert "Smoke Feed" in out
    assert "News" in out


def test_cli_fetch_topics_from_opml_json(tmp_path, capsys):
    opml = _write_opml(tmp_path)

    code = main(["fetch-topics", "--opml", str(opml), "--format", "json"])

    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["title"] == "Smoke Topic"
    assert data[0]["url"] == "https://example.com/smoke"
    assert data[0]["summary"] == "Smoke summary"
    assert data[0]["source_title"] == "Smoke Feed"
    assert data[0]["source_categories"] == ["News"]


def test_cli_fetch_topics_with_fetch_report_json(tmp_path, capsys):
    opml = _write_mixed_opml(tmp_path)

    code = main(["fetch-topics", "--opml", str(opml), "--format", "json", "--with-fetch-report"])

    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    reports = {report["title"]: report for report in data["sources"]}
    assert data["entries"][0]["title"] == "Smoke Topic"
    assert reports["Smoke Feed"]["status"] == "fetched"
    assert reports["Smoke Feed"]["entry_count"] == 1
    assert reports["Smoke Feed"]["shown_count"] == 1
    assert reports["Empty Feed"]["status"] == "empty"
    assert reports["Broken Feed"]["status"] == "error"
    assert reports["Broken Feed"]["error"]
    assert "Error fetching" in captured.err


def test_cli_rss_smoke_opml_json_is_sanitized(tmp_path, capsys):
    opml = _write_mixed_opml(tmp_path)

    code = main(["rss-smoke", "--opml", str(opml), "--format", "json"])

    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["input_kind"] == "OPML export"
    assert data["source_count"] == 3
    assert data["category_count"] == 1
    assert data["source_list_match"] == "manual_required"
    assert data["fetch_status_counts"] == {"fetched": 1, "empty": 1, "error": 1, "listed": 0}
    assert data["representative_entry_fields"]["url"] == "present"
    assert data["representative_entry_fields"]["summary"] == "present"
    assert data["representative_entry_fields"]["source_categories"] == "present"
    assert data["fetch_error_breakdown"] == {"parse_or_non_feed": 1}
    assert data["duplicate_source_summary"] == {
        "duplicate_feed_url_count": 0,
        "duplicate_title_count": 0,
        "handling": "none",
    }
    assert data["source_categories_propagation"] == {
        "source_records_with_categories": 3,
        "source_records_without_categories": 0,
        "fetched_sources_with_categories": 1,
        "matched_entries_from_categorized_sources": 1,
        "shown_entries_from_categorized_sources": 1,
        "diagnosis": "propagated_to_representative_entries",
    }
    assert "one or more feeds failed to fetch" in data["notable_fixes_needed"]
    assert "https://example.com/smoke" not in captured.out
    assert "Smoke Topic" not in captured.out


def test_cli_fetch_topics_from_opml_markdown(tmp_path, capsys):
    opml = _write_opml(tmp_path)

    code = main(["fetch-topics", "--opml", str(opml), "--format", "markdown"])

    assert code == 0
    out = capsys.readouterr().out
    assert "| categories | source | published | title | url |" in out
    assert "Smoke Feed" in out
    assert "Smoke Topic" in out
    assert "https://example.com/smoke" in out


def test_cli_fetch_topics_empty_opml_has_clear_message(tmp_path, capsys):
    opml = _write_empty_opml(tmp_path)

    code = main(["fetch-topics", "--opml", str(opml)])

    assert code == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "No feed sources found in OPML." in captured.err


def test_cli_list_feed_sources_from_inoreader_json(monkeypatch, capsys):
    import src.feed.inoreader as inoreader

    monkeypatch.setattr(
        inoreader,
        "load_inoreader_sources",
        lambda: [
            FeedSource(
                feed_url="https://example.com/feed.xml",
                title="Inoreader Feed",
                categories=("Tech",),
                reader="inoreader",
                reader_feed_id="feed/https://example.com/feed.xml",
            )
        ],
    )

    code = main(["list-feed-sources", "--reader", "inoreader", "--format", "json"])

    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["reader"] == "inoreader"
    assert data[0]["reader_feed_id"] == "feed/https://example.com/feed.xml"


def test_cli_fetch_topics_from_inoreader_with_report(monkeypatch, capsys):
    import src.feed.inoreader as inoreader

    source = FeedSource(
        feed_url="https://example.com/feed.xml",
        title="Inoreader Feed",
        categories=("Tech",),
        reader="inoreader",
        reader_feed_id="feed/https://example.com/feed.xml",
    )
    monkeypatch.setattr(inoreader, "load_inoreader_sources", lambda: [source])
    monkeypatch.setattr(
        inoreader,
        "fetch_inoreader_entries",
        lambda *, limit, sources: [
            FeedEntry(
                title="Inoreader Article",
                published="2026-05-26",
                source_url="https://example.com/feed.xml",
                url="https://example.com/article",
                summary="Summary",
                source_title="Inoreader Feed",
                source_categories=("Tech",),
            )
        ],
    )

    code = main(["fetch-topics", "--reader", "inoreader", "--format", "json", "--with-fetch-report"])

    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data["entries"][0]["source_title"] == "Inoreader Feed"
    assert data["sources"][0]["status"] == "fetched"
    assert data["sources"][0]["entry_count"] == 1


def test_cli_rss_smoke_inoreader_markdown(monkeypatch, capsys):
    import src.feed.inoreader as inoreader

    source = FeedSource(
        feed_url="https://example.com/feed.xml",
        title="Inoreader Feed",
        categories=("Tech",),
        reader="inoreader",
        reader_feed_id="feed/https://example.com/feed.xml",
    )
    monkeypatch.setattr(inoreader, "load_inoreader_sources", lambda: [source])
    monkeypatch.setattr(
        inoreader,
        "fetch_inoreader_entries",
        lambda *, limit, sources: [
            FeedEntry(
                title="Inoreader Article",
                published="2026-05-26",
                source_url="https://example.com/feed.xml",
                url="https://example.com/article",
                summary="Summary",
                source_title="Inoreader Feed",
                source_categories=("Tech",),
            )
        ],
    )

    code = main(["rss-smoke", "--reader", "inoreader", "--format", "markdown"])

    assert code == 0
    out = capsys.readouterr().out
    assert "# RSS Live Smoke Evidence" in out
    assert "input kind: Inoreader read-only" in out
    assert "source count: 1" in out
    assert "fetched=1" in out
    assert "fetch error breakdown: none" in out
    assert "source_categories propagation:" in out
    assert "Manual Hands-On" in out
    assert "Inoreader Article" not in out
