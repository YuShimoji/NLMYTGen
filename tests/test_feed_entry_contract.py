"""FeedEntry data contract tests."""

from src.contracts.feed_entry import FeedEntry


def test_feedentry_creation():
    entry = FeedEntry(
        title="Test Title",
        published="2026-03-30",
        source_url="https://example.com/feed",
        url="https://example.com/article",
        summary="Summary",
        source_title="Example Feed",
        source_categories=("News",),
    )
    assert entry.title == "Test Title"
    assert entry.published == "2026-03-30"
    assert entry.source_url == "https://example.com/feed"
    assert entry.url == "https://example.com/article"
    assert entry.summary == "Summary"
    assert entry.source_title == "Example Feed"
    assert entry.source_categories == ("News",)


def test_feedentry_defaults():
    entry = FeedEntry(title="Minimal")
    assert entry.title == "Minimal"
    assert entry.published is None
    assert entry.source_url is None
    assert entry.url is None
    assert entry.summary is None
    assert entry.source_title is None
    assert entry.source_categories == ()


def test_feedentry_is_frozen():
    entry = FeedEntry(title="Frozen")
    try:
        entry.title = "Changed"
        assert False, "Should not be able to set attributes on frozen dataclass"
    except AttributeError:
        pass


def test_feedentry_equality():
    a = FeedEntry(title="Same", published="2026-01-01")
    b = FeedEntry(title="Same", published="2026-01-01")
    assert a == b
