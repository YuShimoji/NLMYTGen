"""OPML feed source parsing tests."""

from src.feed.sources import parse_opml_sources
from src.contracts.feed_source import FeedSource


OPML_SAMPLE = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <body>
    <outline text="Tech">
      <outline text="AI">
        <outline
          text="Example AI"
          xmlUrl="https://example.com/ai.xml"
          htmlUrl="https://example.com/ai"
          iconUrl="https://example.com/icon.png"
          id="feed/ai" />
      </outline>
      <outline text="No feed folder">
        <outline text="Ignored leaf without xmlUrl" />
      </outline>
    </outline>
    <outline text="Business">
      <outline title="Markets" xmlUrl="https://example.com/markets.xml" />
      <outline title="Duplicate AI" xmlUrl="https://example.com/ai.xml" />
    </outline>
  </body>
</opml>
"""


def test_feedsource_creation_defaults():
    source = FeedSource(feed_url="https://example.com/rss.xml")
    assert source.feed_url == "https://example.com/rss.xml"
    assert source.reader == "opml"
    assert source.categories == ()


def test_parse_opml_nested_categories_and_metadata():
    sources = parse_opml_sources(OPML_SAMPLE)
    first = sources[0]

    assert first.feed_url == "https://example.com/ai.xml"
    assert first.title == "Example AI"
    assert first.html_url == "https://example.com/ai"
    assert first.icon_url == "https://example.com/icon.png"
    assert first.reader_feed_id == "feed/ai"
    assert first.categories == ("Tech", "AI")


def test_parse_opml_ignores_missing_xml_url_and_deduplicates():
    sources = parse_opml_sources(OPML_SAMPLE)

    assert [s.feed_url for s in sources] == [
        "https://example.com/ai.xml",
        "https://example.com/markets.xml",
    ]
    assert sources[1].categories == ("Business",)
