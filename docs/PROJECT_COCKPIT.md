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
| Episode 002 GUI dashboard panel | ready | `production_pilots/yukkuri_newsroom_content_spine_002/gui_dashboard_panel/` | one-surface local HTML/JSON review; validation noise is nonblocking |
| Episode 002 YMM4 import preview pack | ready_context_synced | `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/` | local/offline import-prep inventory; not imported to YMM4; thumbnail proof is context only |
| Episode 002 thumbnail visual proof pack | ready_context | `production_pilots/yukkuri_newsroom_content_spine_002/thumbnail_visual_proof_pack/` | static/local SVG+HTML proof; contextual only for import preview; not production thumbnail approval |
| Validation drift triage | nonblocking | `docs/verification/VALIDATION_DRIFT_VELOCITY_RECOVERY_V1_2026-07-06.md` | full-suite drift is classified; product work can continue |
| Real transcript replacement | blocked_by_real_input | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/real_input/` | requires verified local transcript input |

## Symbolic Bars

- content_spine_002: `[#####--]` local draft package exists.
- ir_bridge_002: `[#####--]` draft IR/CSV bridge exists.
- transcript_substitution_002: `[####---]` sample fixture readiness exists, real transcript missing.
- dashboard_ingest_002: `[######-]` read-only ingest generated and validated.
- gui_dashboard_panel_002: `[######-]` static HTML/JSON panel generated and validated.
- yymm4_import_preview_pack_002: `[######-]` CSV/cue/Writer IR import-prep inventory generated and thumbnail context synced; YMM4 not launched/imported/rendered.
- thumbnail_visual_proof_002: `[######-]` 3 static SVG variants plus HTML/contact sheet generated and validated.
- validation_drift_triage: `[#####--]` current drift classified as nonblocking for episode 002 product work.
- real_transcript_input: `[#------]` drop-zone exists, real input absent.

## Product Return Path

Completed/current slice: episode 002 YMM4 import preview pack context sync.
The import preview is the active review surface; the thumbnail proof exists
only as a context input inside `thumbnail_proof_context`. Preferred next slice
is surface alignment across GUI dashboard, import preview, and thumbnail proof,
so reviewers can decide whether the three local surfaces tell the same
dry-run story before any real transcript or YMM4 import lane. The validation
drift is currently classified as older newsroom generated-artifact noise,
host/path drift, stale metadata, and fixture snapshot drift rather than a
blocker for the episode 002 dashboard/import-preview/thumbnail-proof line.

## Regeneration

```bash
python -m src.cli.main build-dashboard-readiness-ingest --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_dashboard_readiness_ingest_v1
python -m src.cli.main build-gui-dashboard-panel --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_gui_dashboard_panel_v1
python -m src.cli.main build-yymm4-import-preview-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_yymm4_import_preview_pack_v1
python -m src.cli.main build-thumbnail-visual-proof-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_thumbnail_visual_proof_v1
```

Primary machine readback:

```text
production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/validation_readback.json
```

Primary human review file:

```text
production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/import_preview_panel.md
```

## Closed Gates

- No YouTube upload, publication, scheduling, or visibility change.
- No OAuth, API keys, payment, or paid service use.
- No rights/legal/public-ready acceptance.
- No live scraping, RSS fetch, external image/media download, or embedded copyrighted media.
- No YMM4 GUI launch, import, render, production `.ymmp`, audio generation, or timing acceptance.
- Baseball hash residue is outside this import-preview context-sync slice.
