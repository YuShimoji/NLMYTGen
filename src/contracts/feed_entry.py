"""Data contract for RSS/Atom feed entries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeedEntry:
    """A single entry extracted from an RSS or Atom feed."""

    title: str
    published: str | None = None
    source_url: str | None = None
    url: str | None = None
    summary: str | None = None
    source_title: str | None = None
    source_categories: tuple[str, ...] = ()
