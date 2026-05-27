# RSS Live Smoke Runbook (2026-05-26)

This runbook is the next-action entry point for the A-04 RSS lane after RSS
Reader Sync v1.1. It does not take over the G-27 mainline and does not touch
YMM4, production artifacts, DB state, OAuth storage, subscription mutation, or
background polling.

## Purpose

Prove, with real operator data, that the human RSS reader list and the AI-side
feed list match, then confirm article fetching is understandable across many
feeds.

Raw OPML exports and access tokens must not be committed. The repo ignores
`*.opml`, `*.opml.xml`, and `_local/rss/`; use those for live smoke inputs and
scratch output.

## Restart From Another Terminal

Use the latest-master integration branch and fast-forward it before running
live smoke:

```powershell
cd C:\Users\PLANNER007\NLMYTGen
git fetch --all --prune
git checkout codex/rss-reader-sync-master-integrate
git pull --ff-only
```

The integration branch is pushed to
`origin/codex/rss-reader-sync-master-integrate`. If the main worktree is not
available on the machine, clone or add a worktree for that remote branch, then
use this runbook as the entry point. The only expected manual input is a real
OPML export or a temporary Inoreader access token.

## OPML Smoke

Place the exported OPML somewhere ignored, for example:

```powershell
New-Item -ItemType Directory -Force _local/rss
$opml = "_local/rss/feeds.opml"
```

Generate sanitized evidence in one command:

```powershell
python -m src.cli.main rss-smoke --opml $opml --format markdown -o docs/verification/RSS-LIVE-SMOKE-EVIDENCE-YYYY-MM-DD.md
```

Review the source list that NLMYTGen will use:

```powershell
python -m src.cli.main list-feed-sources --opml $opml --format markdown
python -m src.cli.main list-feed-sources --opml $opml --format json > _tmp/rss_sources.json
```

Fetch article candidates with coverage:

```powershell
python -m src.cli.main fetch-topics --opml $opml --format markdown --with-fetch-report > _tmp/rss_fetch_report.md
python -m src.cli.main fetch-topics --opml $opml --format json --with-fetch-report > _tmp/rss_fetch_report.json
```

Success signal:

- `list-feed-sources` count, categories, feed titles, and feed URLs match the
  human RSS reader export well enough to trust OPML as the shared source.
- `fetch-topics --with-fetch-report` clearly separates `fetched`, `empty`, and
  `error` feeds.
- Representative entries include `url`, `summary`, `source_title`, and
  `source_categories`.

## Inoreader Smoke

Run this only when the operator has a temporary Inoreader access token. The
token is supplied by environment variable and is not persisted by NLMYTGen.

```powershell
$env:NLMYTGEN_INOREADER_ACCESS_TOKEN = "..."
python -m src.cli.main rss-smoke --reader inoreader --format markdown -o docs/verification/RSS-INOREADER-SMOKE-EVIDENCE-YYYY-MM-DD.md
python -m src.cli.main list-feed-sources --reader inoreader --format markdown
python -m src.cli.main list-feed-sources --reader inoreader --format json > _tmp/rss_inoreader_sources.json
python -m src.cli.main fetch-topics --reader inoreader --format json --with-fetch-report > _tmp/rss_inoreader_fetch_report.json
Remove-Item Env:\NLMYTGEN_INOREADER_ACCESS_TOKEN
```

Success signal:

- `list-feed-sources --reader inoreader` matches the human Inoreader
  subscription view closely enough to trust the read-only adapter.
- `fetch-topics --reader inoreader --with-fetch-report` returns entries with
  article URL, summary when provided by Inoreader, source title, and source
  categories.
- The run stays within read-only behavior: no refresh-token storage, unread/read
  sync, subscription add/delete, DB write, or polling.

## Sanitized Evidence Template

`rss-smoke` emits this shape directly. When recording the smoke result in repo,
do not paste raw OPML, tokens, private feed URLs, or full article bodies. Commit
only the generated sanitized evidence after checking that it contains counts and
field-presence signals rather than raw subscription data:

```markdown
# RSS Live Smoke Evidence (YYYY-MM-DD)

- input kind: OPML export / Inoreader read-only
- raw input location: not committed (`_local/rss/...` or environment token)
- source count: N
- category count: N
- source-list match: manual_required / needs_fix
- fetch status counts: fetched=N, empty=N, error=N, listed=N
- representative entry fields: url=present, summary=present/partial, source_title=present, source_categories=present
- notable fixes needed: feed URL mismatch / duplicate category / dead feed / token scope / rate limit / none
- next move: keep OPML as source of truth / clean feed list / run Inoreader smoke / defer Inoreader
```

## Next Decision

| Result | Recommended next move |
|---|---|
| OPML list matches and fetch report is readable | Use OPML as the operational RSS source and feed markdown/json output into topic selection. |
| OPML has dead or duplicated feeds | Clean the human RSS reader list, re-export OPML, rerun this runbook. |
| OPML works but manual export is too much friction | Run the Inoreader smoke and compare the read-only API list against the human view. |
| Inoreader token or rate limit blocks smoke | Keep OPML as v1 source; revisit Inoreader only after API eligibility and token policy are settled. |
