# RSS Reader Sync Spec

## Position

A-04 is still an L1 input-acquisition helper. It does not replace
NotebookLM, write scripts, call an LLM, or produce video artifacts.

The 2026-05-25 RSS Reader Sync v1 slice makes an OPML subscription export the
shared source of truth between the human RSS reader view and NLMYTGen's AI-side
feed fetch. The existing direct-URL `fetch-topics` path remains supported.

## Current Behavior

- `fetch-topics URL...` fetches RSS 2.0 / Atom 1.0 feeds directly.
- `fetch-topics --opml feeds.opml` loads all feed subscriptions from OPML and
  fetches them in OPML order.
- `list-feed-sources --opml feeds.opml` prints the feed list NLMYTGen will use,
  so the operator can compare it with the RSS reader export before article
  fetching.
- `--format markdown` is intended for human review; `--format json` is intended
  for downstream AI or tooling.

## Contracts

`FeedSource` is the subscription-level contract:

```python
@dataclass(frozen=True)
class FeedSource:
    feed_url: str
    title: str | None = None
    html_url: str | None = None
    categories: tuple[str, ...] = ()
    reader: str = "opml"
    reader_feed_id: str | None = None
    icon_url: str | None = None
```

`FeedEntry` remains backward-compatible with the original `title`,
`published`, and `source_url` fields, and now also carries article and source
metadata:

```python
@dataclass(frozen=True)
class FeedEntry:
    title: str
    published: str | None = None
    source_url: str | None = None
    url: str | None = None
    summary: str | None = None
    source_title: str | None = None
    source_categories: tuple[str, ...] = ()
```

## CLI Examples

Direct URL fetching:

```bash
python -m src.cli.main fetch-topics https://example.com/feed.xml --format json
```

Review the OPML source list:

```bash
python -m src.cli.main list-feed-sources --opml feeds.opml --format markdown
```

Fetch articles from the same OPML source list:

```bash
python -m src.cli.main fetch-topics --opml feeds.opml --after 2026-05-01 --format markdown -o _tmp/rss_topics.md
```

## Reader Options

| option | fit for v1 | notes |
|---|---|---|
| OPML export | best first step | Keeps the human reader list and AI fetch list aligned without auth, DB, or external API contracts. |
| Inoreader API | later read-only adapter | Use only after confirming account/API eligibility, OAuth app setup, token storage rules, and rate-limit budget. Candidate official endpoints: [OAuth](https://www.inoreader.com/uk/developers/oauth), [Feeds list](https://www.inoreader.com/developers/subscription-list), [Stream contents](https://www.inoreader.com/developers/stream-contents), [Rate limiting](https://www.inoreader.com/developers/rate-limiting). |
| Miniflux | later alternative | Good if self-hosting is acceptable and an API token flow is preferred. Reference: [Miniflux API](https://miniflux.app/docs/api.html). |
| FreshRSS | later alternative | Good if a self-hosted Google Reader API-compatible reader is preferred. Reference: [FreshRSS Google Reader API](https://freshrss.github.io/FreshRSS/en/developers/06_GoogleReader_API.html). |

## Boundaries

This slice does not implement Inoreader OAuth, token persistence, unread/read
state, subscription mutation, database storage, background polling, or GUI
sync. Those require a separate feature decision because they introduce auth or
long-lived state.

The next Inoreader slice should be read-only and should start with a small
connectivity probe: retrieve subscriptions, retrieve recent stream contents,
map them into `FeedSource` / `FeedEntry`, and prove that the returned list
matches the human Inoreader view.
