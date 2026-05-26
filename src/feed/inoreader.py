"""Read-only Inoreader adapter for feed sources and entries."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from urllib.parse import urlencode, quote
import urllib.request

from src.contracts.feed_entry import FeedEntry
from src.contracts.feed_source import FeedSource


INOREADER_BASE_URL = "https://www.inoreader.com"
INOREADER_TOKEN_ENV = "NLMYTGEN_INOREADER_ACCESS_TOKEN"
_USER_AGENT = "NLMYTGen/1.0"


def load_inoreader_sources(access_token: str | None = None) -> list[FeedSource]:
    """Load the logged-in user's feed subscriptions from Inoreader."""
    payload = _get_json(
        "/reader/api/0/subscription/list",
        access_token=_require_access_token(access_token),
    )
    return parse_inoreader_subscriptions(payload)


def fetch_inoreader_entries(
    *,
    access_token: str | None = None,
    sources: list[FeedSource] | None = None,
    stream_id: str = "user/-/state/com.google/reading-list",
    limit: int = 20,
) -> list[FeedEntry]:
    """Fetch recent entries from an Inoreader stream."""
    path = f"/reader/api/0/stream/contents/{quote(stream_id, safe='')}"
    payload = _get_json(
        path,
        access_token=_require_access_token(access_token),
        params={"n": str(limit)},
    )
    return parse_inoreader_stream(payload, sources=sources)


def parse_inoreader_subscriptions(payload: dict) -> list[FeedSource]:
    """Map Inoreader subscription/list JSON to `FeedSource` records."""
    subscriptions = payload.get("subscriptions", [])
    if not isinstance(subscriptions, list):
        raise ValueError("Inoreader subscription/list response must contain subscriptions[]")

    sources: list[FeedSource] = []
    for subscription in subscriptions:
        if not isinstance(subscription, dict):
            continue
        feed_url = _string_or_none(subscription.get("url"))
        if not feed_url:
            continue
        sources.append(
            FeedSource(
                feed_url=feed_url,
                title=_string_or_none(subscription.get("title")),
                html_url=_string_or_none(subscription.get("htmlUrl")),
                categories=_category_labels(subscription.get("categories")),
                reader="inoreader",
                reader_feed_id=_string_or_none(subscription.get("id")),
                icon_url=_string_or_none(subscription.get("iconUrl")),
            )
        )
    return sources


def parse_inoreader_stream(
    payload: dict,
    *,
    sources: list[FeedSource] | None = None,
) -> list[FeedEntry]:
    """Map Inoreader stream/contents JSON to `FeedEntry` records."""
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Inoreader stream/contents response must contain items[]")

    source_by_id, source_by_url = _source_indexes(sources or [])
    entries: list[FeedEntry] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = _string_or_none(item.get("title"))
        if not title:
            continue

        origin = item.get("origin") if isinstance(item.get("origin"), dict) else {}
        stream_id = _string_or_none(origin.get("streamId"))
        origin_feed_url = _feed_url_from_stream_id(stream_id)
        source = source_by_id.get(stream_id or "") or source_by_url.get(origin_feed_url or "")

        entries.append(
            FeedEntry(
                title=title,
                published=_published_date(item),
                source_url=source.feed_url if source else origin_feed_url,
                url=_href_from_links(item.get("canonical")) or _href_from_links(item.get("alternate")),
                summary=_summary_content(item.get("summary")),
                source_title=source.title if source else _string_or_none(origin.get("title")),
                source_categories=source.categories if source else (),
            )
        )
    return entries


def _get_json(path: str, *, access_token: str, params: dict[str, str] | None = None) -> dict:
    query = f"?{urlencode(params)}" if params else ""
    url = f"{INOREADER_BASE_URL}{path}{query}"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": _USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Inoreader response must be a JSON object")
    return data


def _require_access_token(access_token: str | None) -> str:
    token = access_token or os.environ.get(INOREADER_TOKEN_ENV)
    if not token:
        raise ValueError(f"Missing Inoreader token. Set {INOREADER_TOKEN_ENV}.")
    return token


def _source_indexes(sources: list[FeedSource]) -> tuple[dict[str, FeedSource], dict[str, FeedSource]]:
    by_id = {source.reader_feed_id: source for source in sources if source.reader_feed_id}
    by_url = {source.feed_url: source for source in sources}
    return by_id, by_url


def _category_labels(raw: object) -> tuple[str, ...]:
    if not isinstance(raw, list):
        return ()
    labels: list[str] = []
    for category in raw:
        if not isinstance(category, dict):
            continue
        label = _string_or_none(category.get("label"))
        if label:
            labels.append(label)
    return tuple(labels)


def _href_from_links(raw: object) -> str | None:
    if not isinstance(raw, list):
        return None
    for link in raw:
        if not isinstance(link, dict):
            continue
        href = _string_or_none(link.get("href"))
        if href:
            return href
    return None


def _summary_content(raw: object) -> str | None:
    if not isinstance(raw, dict):
        return None
    return _string_or_none(raw.get("content"))


def _published_date(item: dict) -> str | None:
    for key, divisor in (("published", 1), ("crawlTimeMsec", 1000), ("timestampUsec", 1_000_000)):
        value = item.get(key)
        if not isinstance(value, (int, float)):
            continue
        try:
            return datetime.fromtimestamp(value / divisor, tz=timezone.utc).date().isoformat()
        except (OSError, OverflowError, ValueError):
            continue
    return None


def _feed_url_from_stream_id(stream_id: str | None) -> str | None:
    if stream_id and stream_id.startswith("feed/"):
        return stream_id.removeprefix("feed/")
    return None


def _string_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
