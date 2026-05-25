"""Data contract for RSS/Atom feed source subscriptions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeedSource:
    """A feed subscription shared by a human RSS reader and NLMYTGen."""

    feed_url: str
    title: str | None = None
    html_url: str | None = None
    categories: tuple[str, ...] = ()
    reader: str = "opml"
    reader_feed_id: str | None = None
    icon_url: str | None = None
