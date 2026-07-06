# Project Cockpit

This navigation sheet records the current local/offline episode 002 readiness
surface. It is not a production gate, a prompt, or a source of product rules.

## Current Route

| Checkpoint | State | Review path | Boundary |
|---|---|---|---|
| Episode 002 content spine | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/` | dry-run fixture, not real/source-reviewed content |
| Episode 002 IR/CSV bridge | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/ir_bridge/` | Writer IR, cue packet, and CSV are draft candidates only |
| Episode 002 transcript readiness | sample_fixture_not_real | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/` | no real transcript; sample fixture is explicit |
| Episode 002 dashboard readiness ingest | ready | `production_pilots/yukkuri_newsroom_content_spine_002/dashboard_readiness_ingest/` | read-only status package; no YMM4 import/render or public gate crossed |
| Validation drift triage | nonblocking | `docs/verification/VALIDATION_DRIFT_VELOCITY_RECOVERY_V1_2026-07-06.md` | full-suite drift is classified; product work can continue |
| Real transcript replacement | blocked_by_real_input | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/real_input/` | requires verified local transcript input |
| YMM4 import preview | deferred | not generated here | future slice after real transcript/source review |
| Thumbnail visual proof | deferred | not generated here | future static proof only; no external media or public-ready claim |

## Symbolic Bars

- content_spine_002: `[#####--]` local draft package exists.
- ir_bridge_002: `[#####--]` draft IR/CSV bridge exists.
- transcript_substitution_002: `[####---]` sample fixture readiness exists, real transcript missing.
- dashboard_ingest_002: `[######-]` read-only ingest generated and validated.
- validation_drift_triage: `[#####--]` current drift classified as nonblocking for episode 002 product work.
- real_transcript_input: `[#------]` drop-zone exists, real input absent.

## Product Return Path

Preferred next slice: episode 002 GUI dashboard panel. The validation drift is
currently classified as older newsroom generated-artifact noise, host/path
drift, stale metadata, and fixture snapshot drift rather than a blocker for the
episode 002 dashboard line.

## Regeneration

```bash
python -m src.cli.main build-dashboard-readiness-ingest --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_dashboard_readiness_ingest_v1
```

Primary machine readback:

```text
production_pilots/yukkuri_newsroom_content_spine_002/dashboard_readiness_ingest/validation_readback.json
```

Primary human review file:

```text
production_pilots/yukkuri_newsroom_content_spine_002/dashboard_readiness_ingest/dashboard_preview.md
```

## Closed Gates

- No YouTube upload, publication, scheduling, or visibility change.
- No OAuth, API keys, payment, or paid service use.
- No rights/legal/public-ready acceptance.
- No live scraping, RSS fetch, external image/media download, or embedded copyrighted media.
- No YMM4 GUI launch, import, render, production `.ymmp`, audio generation, or timing acceptance.
- Baseball hash residue is outside this dashboard-readiness slice.
