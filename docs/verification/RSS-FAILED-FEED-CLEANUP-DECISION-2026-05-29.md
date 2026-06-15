# RSS Failed Feed Cleanup Decision (2026-05-29)

This is a sanitized decision record for the RSS failed-feed cleanup pass.
Detailed feed titles and feed URLs remain local-only under `_tmp/`, and the raw
OPML export remains local-only under `_local/`.

- branch: `master`
- decision base HEAD: `f6db81e`
- operational premise: RSS feed resources do not need to be perfect or strict; the current sample count is sufficient for the lane
- OPML operational status: accepted as the current operational source of truth after RSS UI source/category count match
- current source count: 147
- current category count: 7
- cleanup basis: local failed-feed cleanup audit from 2026-05-28
- failed feed cleanup policy: delete-first
- failed-feed audit status counts: fetched=121, empty=0, error=26, listed=0
- failed-feed audit breakdown: http_404=2, parse_or_non_feed=15, ssl_error=2, timeout=3, http_403=4
- default delete classes: http_404, parse_or_non_feed, ssl_error, timeout, http_403
- http_404 handling: delete; no replacement research
- parse_or_non_feed handling: delete; do not rescue broken or non-feed URLs
- ssl_error handling: delete unless explicitly protected
- timeout handling: delete unless explicitly protected
- http_403 handling: delete or exclude from direct-fetch operation unless explicitly protected; do not add bot-bypass or header-tuning work
- exceptions: explicitly protected feeds or category coverage risk only
- duplicate feed URL count: 0
- duplicate title count: 1
- duplicate title handling: manual_review; no automatic merge or deletion
- local-only delete-first checklist: `_tmp/rss_delete_first_cleanup_checklist.md`
- Inoreader-side changed count: unknown
- repo-side subscription mutation: none
- Inoreader API: not run
- token use: none
- fresh OPML export: required before post-cleanup smoke, because the current local OPML file has not been refreshed after this decision
- next human action: delete failed-feed candidates in the Inoreader UI, keep duplicate title as manual_review unless separately decided, export a fresh OPML, then rerun sanitized `list-feed-sources` and `rss-smoke`

No feed URLs, private URLs, tokens, raw OPML fragments, article titles, or
article bodies are included in this committed decision record.
