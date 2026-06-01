"""Fetch and parse RSS 2.0 / Atom 1.0 feeds using stdlib only."""

from __future__ import annotations

import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime
from email.utils import parsedate_to_datetime

from src.contracts.feed_entry import FeedEntry
from src.contracts.feed_source import FeedSource

_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_USER_AGENT = "NLMYTGen/1.0"
_ISO_DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:$|[T\s])")


def fetch_feed(
    url: str,
    *,
    timeout: int = 10,
    source: FeedSource | None = None,
) -> list[FeedEntry]:
    """Fetch a feed from *url* and return parsed entries."""
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        xml_bytes: bytes = resp.read()
    return parse_feed_xml(
        xml_bytes,
        source_url=source.feed_url if source else url,
        source_title=source.title if source else None,
        source_categories=source.categories if source else (),
    )


def parse_feed_xml(
    xml_bytes: bytes,
    *,
    source_url: str | None = None,
    source_title: str | None = None,
    source_categories: tuple[str, ...] = (),
) -> list[FeedEntry]:
    """Parse RSS 2.0 or Atom 1.0 XML bytes into a list of `FeedEntry`."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid feed XML: {exc}") from exc

    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag == "rss":
        return _parse_rss(root, source_url, source_title, source_categories)
    if tag == "feed":
        return _parse_atom(root, source_url, source_title, source_categories)
    raise ValueError(f"Unrecognised feed format: root element <{root.tag}>")


def _parse_rss(
    root: ET.Element,
    source_url: str | None,
    source_title: str | None,
    source_categories: tuple[str, ...],
) -> list[FeedEntry]:
    entries: list[FeedEntry] = []
    channel = root.find("channel")
    items = channel.findall("item") if channel is not None else root.findall("item")
    for item in items:
        title = _child_text(item, "title")
        if not title:
            continue
        pub_value = _child_text(item, "pubDate")
        published = _parse_rfc822(pub_value) if pub_value else None
        entries.append(FeedEntry(
            title=title,
            published=published,
            source_url=source_url,
            url=_child_text(item, "link"),
            summary=_child_text(item, "description"),
            source_title=source_title,
            source_categories=source_categories,
        ))
    return entries


def _parse_atom(
    root: ET.Element,
    source_url: str | None,
    source_title: str | None,
    source_categories: tuple[str, ...],
) -> list[FeedEntry]:
    entries: list[FeedEntry] = []
    for entry in root.findall(f"{_ATOM_NS}entry"):
        title = _child_text(entry, "title")
        if not title:
            continue
        pub_value = _child_text(entry, "published")
        if pub_value is None:
            pub_value = _child_text(entry, "updated")
        published = _parse_iso8601_date(pub_value) if pub_value else None
        entries.append(FeedEntry(
            title=title,
            published=published,
            source_url=source_url,
            url=_atom_link(entry),
            summary=_child_text(entry, "summary") or _child_text(entry, "content"),
            source_title=source_title,
            source_categories=source_categories,
        ))
    return entries


def _child_text(parent: ET.Element, child_name: str) -> str | None:
    for child in list(parent):
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag != child_name:
            continue
        text = " ".join(part.strip() for part in child.itertext() if part and part.strip())
        return text or None
    return None


def _atom_link(entry: ET.Element) -> str | None:
    fallback: str | None = None
    for link in entry.findall(f"{_ATOM_NS}link"):
        href = (link.attrib.get("href") or "").strip()
        if not href:
            continue
        rel = (link.attrib.get("rel") or "alternate").strip()
        if rel == "alternate":
            return href
        if fallback is None:
            fallback = href
    return fallback


def _parse_rfc822(value: str) -> str | None:
    """Parse RFC 822 date to ISO 8601 date string (YYYY-MM-DD)."""
    try:
        dt = parsedate_to_datetime(value)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def _parse_iso8601_date(value: str) -> str | None:
    """Extract YYYY-MM-DD from an ISO 8601 datetime string."""
    value = value.strip()
    if not _ISO_DATE_PREFIX_RE.match(value):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        try:
            return date.fromisoformat(value[:10]).isoformat()
        except ValueError:
            return None
