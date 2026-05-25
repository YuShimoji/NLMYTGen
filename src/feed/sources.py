"""OPML feed-source parsing helpers."""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

from src.contracts.feed_source import FeedSource


def load_opml_sources(path: str | Path) -> list[FeedSource]:
    """Load feed subscriptions from an OPML file."""
    return parse_opml_sources(Path(path).read_bytes())


def parse_opml_sources(xml_bytes: bytes) -> list[FeedSource]:
    """Parse OPML XML into de-duplicated `FeedSource` records."""
    root = ET.fromstring(xml_bytes)
    tag = _local_name(root.tag).lower()
    if tag != "opml":
        raise ValueError(f"Unrecognised OPML format: root element <{root.tag}>")

    sources: list[FeedSource] = []
    seen_urls: set[str] = set()

    def walk(node: ET.Element, category_stack: tuple[str, ...]) -> None:
        for child in list(node):
            if _local_name(child.tag).lower() != "outline":
                walk(child, category_stack)
                continue

            feed_url = _attr(child, "xmlUrl")
            label = _outline_label(child)
            next_categories = category_stack

            if feed_url:
                feed_url = feed_url.strip()
                if feed_url and feed_url not in seen_urls:
                    seen_urls.add(feed_url)
                    sources.append(
                        FeedSource(
                            feed_url=feed_url,
                            title=label,
                            html_url=_attr(child, "htmlUrl"),
                            categories=category_stack,
                            reader="opml",
                            reader_feed_id=_attr(child, "id"),
                            icon_url=_attr(child, "iconUrl") or _attr(child, "icon"),
                        )
                    )
            elif label:
                next_categories = (*category_stack, label)

            walk(child, next_categories)

    walk(root, ())
    return sources


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _attr(node: ET.Element, name: str) -> str | None:
    value = node.attrib.get(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def _outline_label(node: ET.Element) -> str | None:
    return _attr(node, "title") or _attr(node, "text")
