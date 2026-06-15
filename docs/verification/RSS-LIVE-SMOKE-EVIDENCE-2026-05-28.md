# RSS Live Smoke Evidence

- input kind: OPML export
- diagnostic base HEAD: 9487396
- raw input location: not committed (_local/rss/feeds.opml.xml)
- source count: 147
- category count: 7
- source-list match: manual_required
- fetch status counts: fetched=115, empty=0, error=32, listed=0
- representative entry fields: url=present, summary=present, source_title=present, source_categories=absent
- fetch error breakdown: http_403=5, http_404=8, parse_or_non_feed=15, ssl_error=2, timeout=2
- fetch error count note: live reruns varied around the prior 31-error baseline; this evidence records the current failing set without raw feed URLs
- duplicate source summary: feed_url_duplicates=0, title_duplicates=1, handling=manual_review
- source_categories propagation: source_records_with_categories=106, source_records_without_categories=41, fetched_sources_with_categories=82, matched_entries_from_categorized_sources=5355, shown_entries_from_categorized_sources=0, diagnosis=representative_sample_from_uncategorized_sources
- leakage check: no hits for the configured URL, token, raw OPML, or feed filename marker set
- manual_required: RSS reader UI count/category/title spot-check before treating OPML as operational source of truth
- notable fixes needed: one or more feeds failed to fetch
- after: -
- limit: 20
- next move: clean failed feeds or rerun after confirming network/token access

## Manual Hands-On

1. Export OPML from the human RSS reader into an ignored path such as _local/rss/feeds.opml.xml.
2. Compare source_count/category_count and spot-check feed titles/categories against the reader UI.
3. Commit only this sanitized evidence, not the raw OPML or full article bodies.
