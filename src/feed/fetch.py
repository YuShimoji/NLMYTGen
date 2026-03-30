"""Fetch and parse RSS 2.0 / Atom 1.0 feeds using stdlib only."""

from __future__ import annotations

import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from src.contracts.feed_entry import FeedEntry

_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_USER_AGENT = "NLMYTGen/1.0"


def fetch_feed(url: str, *, timeout: int = 10) -> list[FeedEntry]:
    """Fetch a feed from *url* and return parsed entries."""
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        xml_bytes: bytes = resp.read()
    return parse_feed_xml(xml_bytes, source_url=url)


def parse_feed_xml(xml_bytes: bytes, *, source_url: str | None = None) -> list[FeedEntry]:
    """Parse RSS 2.0 or Atom 1.0 XML bytes into a list of `FeedEntry`."""
    root = ET.fromstring(xml_bytes)

    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag == "rss":
        return _parse_rss(root, source_url)
    if tag == "feed":
        return _parse_atom(root, source_url)
    raise ValueError(f"Unrecognised feed format: root element <{root.tag}>")


def _parse_rss(root: ET.Element, source_url: str | None) -> list[FeedEntry]:
    entries: list[FeedEntry] = []
    for item in root.iter("item"):
        title_el = item.find("title")
        if title_el is None or not (title_el.text or "").strip():
            continue
        pub_el = item.find("pubDate")
        published = _parse_rfc822(pub_el.text) if pub_el is not None and pub_el.text else None
        entries.append(FeedEntry(
            title=title_el.text.strip(),
            published=published,
            source_url=source_url,
        ))
    return entries


def _parse_atom(root: ET.Element, source_url: str | None) -> list[FeedEntry]:
    entries: list[FeedEntry] = []
    for entry in root.findall(f"{_ATOM_NS}entry"):
        title_el = entry.find(f"{_ATOM_NS}title")
        if title_el is None or not (title_el.text or "").strip():
            continue
        pub_el = entry.find(f"{_ATOM_NS}published")
        if pub_el is None:
            pub_el = entry.find(f"{_ATOM_NS}updated")
        published = _parse_iso8601_date(pub_el.text) if pub_el is not None and pub_el.text else None
        entries.append(FeedEntry(
            title=title_el.text.strip(),
            published=published,
            source_url=source_url,
        ))
    return entries


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
    if len(value) >= 10:
        return value[:10]
    return None
