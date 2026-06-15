# RSS Failed Feed Cleanup Summary (2026-05-28)

This is a sanitized summary for the RSS OPML failed-feed cleanup audit. The
raw OPML and detailed failed-feed list stay local-only under `_local/` and
`_tmp/`.

- branch: `master`
- audit base HEAD: `1666f3c`
- input kind: OPML export
- OPML operational status: accepted as the current operational source of truth after RSS UI source/category count match
- total sources: 147
- categories: 7
- duplicate feed URL count: 0
- duplicate title count: 1
- duplicate title handling: manual_review; do not auto-merge or auto-delete from title alone
- current local audit status counts: fetched=121, empty=0, error=26, listed=0
- current local audit error breakdown: http_403=4, http_404=2, parse_or_non_feed=15, ssl_error=2, timeout=3
- prior smoke baseline: fetch error count varied around the previous 31/32-error diagnostic evidence
- failed feed cleanup policy: delete-first
- default delete classes: http_404, parse_or_non_feed, ssl_error, timeout, http_403
- rescue / replacement research: not part of this cleanup pass
- http_403 handling: delete or exclude from direct-fetch operation unless explicitly protected; do not add bot-bypass or header-tuning work
- exceptions: explicitly protected feeds or category coverage risk only
- cleanup priority: http_404 -> parse_or_non_feed -> ssl_error -> timeout -> http_403
- local-only detailed markdown: `_tmp/rss_failed_feed_cleanup_candidates.md`
- local-only detailed json: `_tmp/rss_failed_feed_cleanup_candidates.json`
- local-only delete-first checklist: `_tmp/rss_delete_first_cleanup_checklist.md`
- Inoreader API: not run
- subscription changes: none
- source_categories note: prior diagnosis still holds; OPML parser has categories and representative sample selection caused absent shown categories
- next human action: delete failed-feed candidates in the Inoreader UI unless explicitly protected, leave the duplicate title for manual_review, export a fresh OPML, then rerun post-cleanup smoke

No feed URLs, private URLs, tokens, raw OPML fragments, article titles, or
article bodies are included in this committed summary.
