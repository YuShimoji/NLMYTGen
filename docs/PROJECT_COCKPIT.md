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
| Episode 002 surface alignment pack | ready | `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_pack/` | local/offline cross-surface review story; no YMM4 or production gates crossed |
| Episode 002 surface alignment reviewer packet | source_record | `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_review_packet/` | source record; label/next-action drift repaired at packet readback level; source surfaces unchanged |
| Episode 002 focused review brief | source_record | `production_pilots/yukkuri_newsroom_content_spine_002/focused_review_brief/focused_review_brief.html` | prior focused surface; preserved as secondary source record |
| Episode 002 compact review cockpit | ready | `production_pilots/yukkuri_newsroom_content_spine_002/review_cockpit_compact/review_cockpit.html` | primary human review cockpit; bounded dark HTML with state/layout readbacks |
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
- surface_alignment_002: `[######-]` GUI/import/thumbnail surfaces aligned into one review story; stale next-action labels recorded.
- surface_reviewer_packet_002: `[#####--]` prior 8 drift rows classified as 5 resolved and 3 accepted_nonblocking; now a source record for the focused brief.
- focused_review_brief_002: `[#####--]` prior dark-mode decision-first surface preserved as a source record.
- review_cockpit_compact_002: `[######-]` compact bounded dark review cockpit generated and validated as the current primary review surface.
- validation_drift_triage: `[#####--]` current drift classified as nonblocking for episode 002 product work.
- real_transcript_input: `[#------]` drop-zone exists, real input absent.

## Product Return Path

Completed/current slice: episode 002 compact review cockpit. The active human
review surface is now `review_cockpit_compact/review_cockpit.html`; the older
`focused_review_brief/focused_review_brief.html` and
`surface_alignment_review_packet/aligned_review_story.md` remain secondary
source records. The cockpit compresses the current GUI/import/thumbnail state
into a header strip, one primary decision card, three next-action choices,
three surface status cards, one closed-gate strip, and secondary details. Its
layout readback is bounded at 5 primary sections, 7 visible cards, 2 detail
sections, no top-level tables, and no ledger in the primary body. Proposed
next T+1 after human review is verified local real topic/source/transcript
replacement; actual YMM4 import observation without render/public claims is an
alternate later lane only if that gate is explicitly selected. The validation
drift is currently classified as older newsroom generated-artifact noise,
host/path drift, stale metadata, and fixture snapshot drift rather than a
blocker for the episode 002 review-cockpit line.

## Regeneration

```bash
python -m src.cli.main build-dashboard-readiness-ingest --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_dashboard_readiness_ingest_v1
python -m src.cli.main build-gui-dashboard-panel --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_gui_dashboard_panel_v1
python -m src.cli.main build-yymm4-import-preview-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_yymm4_import_preview_pack_v1
python -m src.cli.main build-thumbnail-visual-proof-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_thumbnail_visual_proof_v1
python -m src.cli.main build-surface-alignment-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_surface_alignment_across_gui_import_thumbnail_v1
python -m src.cli.main build-surface-reviewer-packet --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_surface_alignment_repair_and_reviewer_packet_v1
python -m src.cli.main build-focused-review-brief --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_focused_review_brief_dark_surface_v1
python -m src.cli.main build-review-cockpit-compact --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_review_cockpit_compact_v1
```

Primary machine readback:

```text
production_pilots/yukkuri_newsroom_content_spine_002/review_cockpit_compact/validation_readback.json
```

Primary human review file:

```text
production_pilots/yukkuri_newsroom_content_spine_002/review_cockpit_compact/review_cockpit.html
```

## Closed Gates

- No YouTube upload, publication, scheduling, or visibility change.
- No OAuth, API keys, payment, or paid service use.
- No rights/legal/public-ready acceptance.
- No live scraping, RSS fetch, external image/media download, or embedded copyrighted media.
- No YMM4 GUI launch, import, render, production `.ymmp`, audio generation, or timing acceptance.
- Baseball hash residue is outside this surface-alignment slice.
