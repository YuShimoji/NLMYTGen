# RSS Live Smoke Evidence

- input kind: OPML export
- raw input location: not committed (_local/rss/feeds.opml.xml)
- source count: 147
- category count: 7
- source-list match: manual_required
- fetch status counts: fetched=116, empty=0, error=31, listed=0
- representative entry fields: url=present, summary=present, source_title=present, source_categories=absent
- notable fixes needed: one or more feeds failed to fetch
- after: -
- limit: 20
- next move: clean failed feeds or rerun after confirming network/token access

## Manual Hands-On

1. Export OPML from the human RSS reader into _local/rss/feeds.opml.xml.
2. Compare source_count/category_count and spot-check feed titles/categories against the reader UI.
3. Commit only this sanitized evidence, not the raw OPML or full article bodies.
