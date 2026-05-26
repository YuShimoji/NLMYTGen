# RSS OPML operational verification (2026-05-26)

This note keeps A-04 OPML sync operational without expanding into OAuth,
database storage, unread/read sync, or background polling.

## Position

RSS Reader Sync v1 makes an OPML export the shared source of truth between the
human RSS reader and NLMYTGen's `fetch-topics` command. The verification target
is list parity and article candidate review, not automated ingestion into a
production script.

Do not commit a personal OPML file unless it has been intentionally sanitized.
Use a local path such as `_local/feeds.opml` or `_tmp/rss/feeds.opml` for
operator-owned exports.

## Operator flow

| Step | Command | Success signal |
| --- | --- | --- |
| Inspect the AI-side subscription list | `uv run python -m src.cli.main list-feed-sources --opml <feeds.opml> --format markdown` | Feed titles, URLs, and categories match the human RSS reader export closely enough to review. |
| Capture machine-readable source list | `uv run python -m src.cli.main list-feed-sources --opml <feeds.opml> --format json > _tmp/rss_sources.json` | JSON records carry `feed_url`, optional `title`, `html_url`, `categories`, and `reader="opml"`. |
| Fetch topic candidates | `uv run python -m src.cli.main fetch-topics --opml <feeds.opml> --after 2026-05-01 --format markdown -o _tmp/rss_topics.md` | Candidate rows include feed/source context and article URLs for human selection. |
| Produce AI-friendly candidate JSON | `uv run python -m src.cli.main fetch-topics --opml <feeds.opml> --after 2026-05-01 --format json -o _tmp/rss_topics.json` | Downstream review can consume `FeedEntry` fields without scraping text output. |

Use `--after` as the first noise control. Use `-n` only after confirming that
feed ordering and source coverage are correct, because early limits can hide
feeds later in the OPML list.

## Expected mismatch classes

| Mismatch | Likely cause | Response |
| --- | --- | --- |
| Missing folder/category | Reader exported a flat OPML or category nesting differs | Accept if feed URLs match; category parity is useful but not the source of truth. |
| Duplicate feed collapsed | OPML contains the same `xmlUrl` in more than one folder | Current parser de-duplicates by feed URL; record this before relying on category counts. |
| Feed has no candidates | Feed is unreachable, empty, or filtered by `--after` | Re-run direct `fetch-topics <feed-url>` or relax the date filter before treating it as a source gap. |
| Reader item count differs | Reader may cache or enrich articles beyond RSS/Atom feed output | Keep OPML v1 as acquisition parity only; do not infer reader unread/read state. |

## Acceptance

The v1 operational check is passed when an operator can compare the OPML source
list with their RSS reader view, then generate reviewable topic candidates from
the same OPML without adding credentials or persistent state.

This does not authorize Inoreader API, OAuth, token persistence, subscription
mutation, unread/read state sync, polling, NotebookLM replacement, or video
artifact generation.
