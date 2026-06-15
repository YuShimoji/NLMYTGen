"""RSS/Atom feed parsing tests (no network required)."""

from src.feed.fetch import parse_feed_xml
from src.contracts.feed_entry import FeedEntry

RSS_SAMPLE = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Tech News</title>
    <item>
      <title>AI\xe3\x81\x8c\xe5\xa4\x89\xe3\x81\x88\xe3\x82\x8b\xe6\x9c\xaa\xe6\x9d\xa5</title>
      <link>https://example.com/ai-future</link>
      <description>AI summary</description>
      <pubDate>Mon, 28 Mar 2026 09:00:00 +0900</pubDate>
    </item>
    <item>
      <title>Quantum Computing Update</title>
      <pubDate>Sun, 27 Mar 2026 12:00:00 +0000</pubDate>
    </item>
    <item>
      <title>Space Exploration</title>
    </item>
  </channel>
</rss>
"""

ATOM_SAMPLE = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Science Blog</title>
  <entry>
    <title>Dark Matter Research</title>
    <link href="https://example.com/dark-matter" rel="alternate" />
    <summary>Dark matter summary</summary>
    <published>2026-03-29T10:00:00Z</published>
  </entry>
  <entry>
    <title>Climate Change Report</title>
    <updated>2026-03-25T08:00:00Z</updated>
  </entry>
  <entry>
    <title>  </title>
  </entry>
</feed>
"""


def test_parse_rss_titles():
    entries = parse_feed_xml(RSS_SAMPLE, source_url="https://example.com/rss")
    assert len(entries) == 3
    assert entries[0].title == "AIが変える未来"
    assert entries[1].title == "Quantum Computing Update"
    assert entries[2].title == "Space Exploration"


def test_parse_rss_dates():
    entries = parse_feed_xml(RSS_SAMPLE)
    assert entries[0].published == "2026-03-28"
    assert entries[1].published == "2026-03-27"
    assert entries[2].published is None


def test_parse_rss_source_url():
    entries = parse_feed_xml(RSS_SAMPLE, source_url="https://example.com/rss")
    assert all(e.source_url == "https://example.com/rss" for e in entries)


def test_parse_rss_nested_title_text():
    xml = b"""\
<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Example</title>
    <item>
      <title>Sports <b>Market</b> Update</title>
      <pubDate>not a date</pubDate>
    </item>
  </channel>
</rss>
"""
    entries = parse_feed_xml(xml)
    assert entries == [FeedEntry(title="Sports Market Update", published=None, source_url=None)]


def test_parse_rss_article_url_and_summary():
    entries = parse_feed_xml(RSS_SAMPLE)
    assert entries[0].url == "https://example.com/ai-future"
    assert entries[0].summary == "AI summary"


def test_parse_source_metadata():
    entries = parse_feed_xml(
        RSS_SAMPLE,
        source_url="https://example.com/rss",
        source_title="Tech News",
        source_categories=("Tech", "AI"),
    )
    assert entries[0].source_title == "Tech News"
    assert entries[0].source_categories == ("Tech", "AI")


def test_parse_atom_titles():
    entries = parse_feed_xml(ATOM_SAMPLE, source_url="https://example.com/atom")
    assert len(entries) == 2
    assert entries[0].title == "Dark Matter Research"
    assert entries[1].title == "Climate Change Report"


def test_parse_atom_dates():
    entries = parse_feed_xml(ATOM_SAMPLE)
    assert entries[0].published == "2026-03-29"
    assert entries[1].published == "2026-03-25"


def test_parse_atom_article_url_and_summary():
    entries = parse_feed_xml(ATOM_SAMPLE)
    assert entries[0].url == "https://example.com/dark-matter"
    assert entries[0].summary == "Dark matter summary"


def test_parse_atom_skips_blank_titles():
    entries = parse_feed_xml(ATOM_SAMPLE)
    titles = [e.title for e in entries]
    assert "  " not in titles
    assert len(entries) == 2


def test_parse_atom_invalid_date_returns_none():
    xml = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example</title>
  <entry>
    <title>Bad Date</title>
    <published>not-a-date-value</published>
  </entry>
</feed>
"""
    entries = parse_feed_xml(xml)
    assert entries == [FeedEntry(title="Bad Date", published=None, source_url=None)]


def test_parse_empty_rss():
    xml = b"""\
<?xml version="1.0"?>
<rss version="2.0"><channel><title>Empty</title></channel></rss>
"""
    entries = parse_feed_xml(xml)
    assert entries == []


def test_parse_empty_atom():
    xml = b"""\
<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Empty</title></feed>
"""
    entries = parse_feed_xml(xml)
    assert entries == []


def test_unrecognised_format():
    xml = b"<html><body>Not a feed</body></html>"
    try:
        parse_feed_xml(xml)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Unrecognised feed format" in str(e)


def test_malformed_xml_raises_value_error():
    xml = b"<rss><channel><item><title>Broken</title></item></channel>"
    try:
        parse_feed_xml(xml)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Invalid feed XML" in str(e)


def test_date_filtering():
    entries = parse_feed_xml(RSS_SAMPLE)
    after = "2026-03-28"
    filtered = [e for e in entries if e.published and e.published >= after]
    assert len(filtered) == 1
    assert filtered[0].title == "AIが変える未来"


def test_limit():
    entries = parse_feed_xml(RSS_SAMPLE)
    limited = entries[:1]
    assert len(limited) == 1
    assert limited[0].title == "AIが変える未来"
