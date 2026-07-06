# Episode 002 Focused Review Brief

Primary question: Which next path should episode 002 take after this local dry-run review?

## Current State

- Focused local review surface is ready.
- Source record remains `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_review_packet/aligned_review_story.md`.
- Production, YMM4 import/render, public, rights, and final thumbnail claims remain closed.

## Three-Line Summary

1. GUI, import preview, and thumbnail proof are aligned as local review evidence.
2. The package is still dry-run and sample-backed: no real transcript, YMM4 import, render, or production claim.
3. Reviewer should choose real input replacement, gated YMM4 import observation without render, or hold.

## Next Choices

- Real input replacement: Verified local real source/transcript material is available. Effect: Moves from sample fixture to production-relevant content without YMM4 or publication gates.
- YMM4 observation without render: Human explicitly chooses to inspect import behavior. Effect: Observes CSV/VoiceItem/timing behavior only; no render or production .ymmp claim.
- Hold / review later: The brief is insufficient, input is unavailable, or no YMM4 gate is selected. Effect: Keeps the current local/offline reviewer packet as the record.

## Evidence

- GUI dashboard panel: ready / GUI/dashboard state is already aligned and should be read as evidence, not as the current build target. Review: `production_pilots/yukkuri_newsroom_content_spine_002/gui_dashboard_panel/dashboard_panel_preview.html`
- YMM4 import preview pack: ready / CSV/import-prep package is locally reviewable; it has not been imported into YMM4. Review: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/import_preview_panel.md`
- Thumbnail visual proof pack: ready / Thumbnail proof is context only and is not final thumbnail approval. Review: `production_pilots/yukkuri_newsroom_content_spine_002/thumbnail_visual_proof_pack/thumbnail_visual_proof.html`

## Gates

dry_run, sample_fixture_not_real, no_real_transcript, rights_boundary, public_upload_closed, yymm4_render_closed, no_yymm4_import, thumbnail_context_only, validation_noise_nonblocking, not_production_ready

Primary machine readback:

`production_pilots/yukkuri_newsroom_content_spine_002/focused_review_brief/validation_readback.json`
