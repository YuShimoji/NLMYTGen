# RSS Reader Sync Spec

## Position

A-04 is still an L1 input-acquisition helper. It does not replace
NotebookLM, write scripts, call an LLM, or produce video artifacts.

The 2026-05-25 RSS Reader Sync v1 slice makes an OPML subscription export the
shared source of truth between the human RSS reader view and NLMYTGen's AI-side
feed fetch. The existing direct-URL `fetch-topics` path remains supported.

The 2026-05-26 follow-up keeps that OPML-first base, adds fetch coverage
reporting for many-feed runs, and adds an Inoreader read-only adapter. The
adapter uses only an access token supplied by environment variable and does not
store refresh tokens or reader state.

## Current Behavior

- `fetch-topics URL...` fetches RSS 2.0 / Atom 1.0 feeds directly.
- `fetch-topics --opml feeds.opml` loads all feed subscriptions from OPML and
  fetches them in OPML order.
- `fetch-topics --opml feeds.opml --with-fetch-report --format json` returns
  `{entries, sources}` so the operator can see which feeds fetched, returned no
  entries, or failed.
- `fetch-topics --reader inoreader` loads Inoreader subscriptions and recent
  reading-list contents through the read-only adapter.
- `rss-smoke --opml feeds.opml` or `rss-smoke --reader inoreader` runs the
  source/fetch smoke and emits sanitized evidence that is safe to commit after
  review.
- `list-feed-sources --opml feeds.opml` prints the feed list NLMYTGen will use,
  so the operator can compare it with the RSS reader export before article
  fetching.
- `list-feed-sources --reader inoreader` prints the feed list visible through
  the Inoreader API.
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

Fetch OPML articles with per-feed coverage:

```bash
python -m src.cli.main fetch-topics --opml feeds.opml --format json --with-fetch-report
```

Review Inoreader sources or fetch recent Inoreader reading-list entries:

```bash
set NLMYTGEN_INOREADER_ACCESS_TOKEN=...
python -m src.cli.main list-feed-sources --reader inoreader --format markdown
python -m src.cli.main fetch-topics --reader inoreader --format json --with-fetch-report
```

Generate sanitized live-smoke evidence:

```bash
python -m src.cli.main rss-smoke --opml feeds.opml --format markdown -o docs/verification/RSS-LIVE-SMOKE-EVIDENCE-YYYY-MM-DD.md
```

For the next live-smoke entry point, use
[RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md](verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md).
It fixes where to place raw OPML/token inputs, which commands to run, what
counts as success, and what sanitized evidence is safe to commit.

## Fetch Report

`--with-fetch-report` is opt-in. Without it, `fetch-topics --format json`
continues to emit the backward-compatible list of entries.

With `--with-fetch-report`, JSON output is:

```json
{
  "entries": [],
  "sources": [
    {
      "feed_url": "https://example.com/feed.xml",
      "title": "Example Feed",
      "categories": ["Tech"],
      "reader": "opml",
      "reader_feed_id": null,
      "status": "fetched",
      "entry_count": 3,
      "matched_count": 2,
      "shown_count": 2,
      "error": null
    }
  ]
}
```

`status` is `fetched`, `empty`, `error`, or `listed`. `entry_count` is the
number of entries returned by that source before date filtering, `matched_count`
is after `--after`, and `shown_count` is after the global `--limit`.

## Reader Options

| option | fit for v1 | notes |
|---|---|---|
| OPML export | best first step | Keeps the human reader list and AI fetch list aligned without auth, DB, or external API contracts. |
| Inoreader API | read-only adapter | Uses `subscription/list` for `FeedSource` and `stream/contents` for `FeedEntry`. Requires an access token in `NLMYTGEN_INOREADER_ACCESS_TOKEN`; OAuth app registration and token refresh are outside this repo slice. Candidate official endpoints: [OAuth](https://www.inoreader.com/uk/developers/oauth), [Feeds list](https://www.inoreader.com/developers/subscription-list), [Stream contents](https://www.inoreader.com/developers/stream-contents), [Rate limiting](https://www.inoreader.com/developers/rate-limiting). |
| Miniflux | later alternative | Good if self-hosting is acceptable and an API token flow is preferred. Reference: [Miniflux API](https://miniflux.app/docs/api.html). |
| FreshRSS | later alternative | Good if a self-hosted Google Reader API-compatible reader is preferred. Reference: [FreshRSS Google Reader API](https://freshrss.github.io/FreshRSS/en/developers/06_GoogleReader_API.html). |

## Boundaries

This slice does not implement Inoreader OAuth, refresh-token persistence,
unread/read state, subscription mutation, database storage, background polling,
or GUI sync. Those require a separate feature decision because they introduce
auth or long-lived state.

The next Inoreader move is a live smoke only when the operator supplies a token:
retrieve subscriptions, retrieve recent stream contents, compare
`list-feed-sources --reader inoreader` with the human Inoreader view, and keep
only sanitized counts / field-presence evidence in repo.
