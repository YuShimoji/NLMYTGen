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
- failed-feed audit status counts: fetched=121, empty=0, error=26, listed=0
- failed-feed audit breakdown: http_404=2, parse_or_non_feed=15, ssl_error=2, timeout=3, http_403=4
- http_404 handling: delete
- parse_or_non_feed handling: delete
- ssl_error handling: delete
- timeout handling: delete
- http_403 handling: delete
- duplicate feed URL count: 0
- duplicate title count: 1
- duplicate title handling: manual_review; no automatic merge or deletion
- Inoreader-side changed count: unknown
- repo-side subscription mutation: none
- Inoreader API: not run
- token use: none
- fresh OPML export: required before post-cleanup smoke, because the current local OPML file has not been refreshed after this decision
- next validation: replace `_local/rss/feeds.opml.xml` with a fresh export, then rerun sanitized `list-feed-sources` and `rss-smoke`

No feed URLs, private URLs, tokens, raw OPML fragments, article titles, or
article bodies are included in this committed decision record.
