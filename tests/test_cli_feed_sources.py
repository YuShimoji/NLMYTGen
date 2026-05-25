"""CLI tests for OPML-backed RSS source listing and fetching."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from src.cli.main import main


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
