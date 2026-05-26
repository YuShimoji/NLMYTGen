"""Inoreader read-only adapter tests."""

from src.feed.inoreader import (
    INOREADER_TOKEN_ENV,
    fetch_inoreader_entries,
    load_inoreader_sources,
    parse_inoreader_stream,
    parse_inoreader_subscriptions,
)


SUBSCRIPTION_PAYLOAD = {
    "subscriptions": [
        {
            "id": "feed/https://example.com/feed.xml",
            "title": "Example Feed",
            "categories": [{"label": "Tech"}],
            "url": "https://example.com/feed.xml",
            "htmlUrl": "https://example.com/",
            "iconUrl": "https://example.com/icon.png",
        }
    ]
}


def test_parse_inoreader_subscriptions_maps_feed_source_fields():
    sources = parse_inoreader_subscriptions(SUBSCRIPTION_PAYLOAD)
    source = sources[0]

    assert source.feed_url == "https://example.com/feed.xml"
    assert source.title == "Example Feed"
    assert source.html_url == "https://example.com/"
    assert source.categories == ("Tech",)
    assert source.reader == "inoreader"
    assert source.reader_feed_id == "feed/https://example.com/feed.xml"
    assert source.icon_url == "https://example.com/icon.png"


def test_parse_inoreader_stream_maps_entry_fields_from_source_lookup():
    sources = parse_inoreader_subscriptions(SUBSCRIPTION_PAYLOAD)
    payload = {
        "items": [
            {
                "title": "Example Article",
                "published": 1779753600,
                "canonical": [{"href": "https://example.com/article"}],
                "summary": {"content": "<p>Article summary</p>"},
                "origin": {
                    "streamId": "feed/https://example.com/feed.xml",
                    "title": "Fallback Feed",
                    "htmlUrl": "https://example.com/",
                },
            }
        ]
    }

    entries = parse_inoreader_stream(payload, sources=sources)
    entry = entries[0]

    assert entry.title == "Example Article"
    assert entry.published == "2026-05-26"
    assert entry.source_url == "https://example.com/feed.xml"
    assert entry.url == "https://example.com/article"
    assert entry.summary == "<p>Article summary</p>"
    assert entry.source_title == "Example Feed"
    assert entry.source_categories == ("Tech",)


def test_parse_inoreader_stream_handles_feed_stream_without_optional_fields():
    payload = {
        "items": [
            {
                "title": "Feed Stream Article",
                "timestampUsec": 1779753600000000,
                "alternate": [{"href": "https://example.com/fallback"}],
                "origin": {
                    "streamId": "feed/https://example.com/feed.xml",
                    "title": "Origin Feed",
                },
            }
        ]
    }

    entry = parse_inoreader_stream(payload)[0]

    assert entry.published == "2026-05-26"
    assert entry.source_url == "https://example.com/feed.xml"
    assert entry.url == "https://example.com/fallback"
    assert entry.summary is None
    assert entry.source_title == "Origin Feed"
    assert entry.source_categories == ()


def test_inoreader_live_helpers_require_token(monkeypatch):
    monkeypatch.delenv(INOREADER_TOKEN_ENV, raising=False)

    for call in (load_inoreader_sources, fetch_inoreader_entries):
        try:
            call()
        except ValueError as exc:
            assert INOREADER_TOKEN_ENV in str(exc)
        else:
            raise AssertionError("expected missing-token error")
