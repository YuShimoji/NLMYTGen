# RSS read-only adapter preflight (2026-05-26)

This preflight describes what must be decided before adding an Inoreader-style
API adapter. It does not implement OAuth, token storage, API calls, or database
state.

## Verified external API shape

Official Inoreader docs checked on 2026-05-26:

- OAuth 2.0 uses `https://www.inoreader.com/oauth2/auth` and
  `https://www.inoreader.com/oauth2/token`; the consent flow can request
  `read` scope, and Zone 2 requires read/write permissions.
- Feeds list is available at
  `https://www.inoreader.com/reader/api/0/subscription/list`, returning feed
  identifiers, titles, categories, feed URLs, site URLs, and icons.
- Stream contents is available at
  `https://www.inoreader.com/reader/api/0/stream/contents/[streamId]`, returning
  JSON article items with title, timestamps, canonical/alternate links, summary,
  origin, categories, and continuation.
- Rate limiting groups subscription list and stream contents in Zone 1; the
  public docs currently describe default daily limits and usage headers.

References:

- https://www.inoreader.com/uk/developers/oauth
- https://www.inoreader.com/developers/subscription-list
- https://www.inoreader.com/developers/stream-contents
- https://www.inoreader.com/developers/rate-limiting

## Minimum adapter contract

| Need | Default for first adapter |
| --- | --- |
| Scope | read-only only |
| Source contract | map subscription records into `FeedSource` |
| Entry contract | map stream items into `FeedEntry` |
| State | no DB and no unread/read mutation |
| Token handling | blocked until repo-local secret storage rules are selected |
| Rate-limit handling | fail closed with response headers in the error payload |
| Subscription mutation | out of scope |

The first adapter should prove two read-only calls only: subscriptions and
recent stream contents. It should then compare adapter-derived `FeedSource`
records with OPML-derived `FeedSource` records before any operator workflow
switches away from OPML.

## Mapping notes

| Inoreader field | NLMYTGen field |
| --- | --- |
| subscription `url` | `FeedSource.feed_url` |
| subscription `title` | `FeedSource.title` |
| subscription `htmlUrl` | `FeedSource.html_url` |
| subscription category labels | `FeedSource.categories` |
| subscription `id` | `FeedSource.reader_feed_id` |
| subscription `iconUrl` | `FeedSource.icon_url` |
| item `title` | `FeedEntry.title` |
| item canonical or alternate href | `FeedEntry.url` |
| item `published` | `FeedEntry.published` after timestamp conversion |
| item `summary.content` | `FeedEntry.summary` after HTML/text policy is selected |
| item `origin.title` | `FeedEntry.source_title` |
| item origin stream/feed | `FeedEntry.source_url` when feed URL is available |

## Blockers before implementation

- Choose secret storage rules for client secret, access token, and refresh token.
- Decide whether a local-only OAuth callback is acceptable.
- Decide how to expose rate-limit and refresh failures in CLI output.
- Decide whether HTML summaries are stripped, preserved, or truncated before
  being passed to downstream AI review.
- Confirm the user actually wants API parity beyond OPML export.

Until those decisions are made, OPML remains the recommended operational path.
