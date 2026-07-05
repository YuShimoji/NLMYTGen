# Dashboard Readiness Review Checklist

## Check Now

- Confirm the dashboard preview matches the current pilot package.
- Confirm sample_fixture_not_real is visible before any transcript rerun.
- Confirm draft_yymm4_csv is treated as a preview, not YMM4 import proof.
- Confirm no rights, legal, public-ready, render, upload, or payment gate is crossed.

## Reviewable Artifacts

- content_spine: `production_pilots/yukkuri_newsroom_content_spine_001/MANIFEST.json`
- ir_bridge: `production_pilots/yukkuri_newsroom_content_spine_001/ir_bridge/bridge_manifest.json`
- transcript_substitution: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/substitution_manifest.json`
- writer_ir: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_writer_ir_candidate.json`
- cue_packet: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_cue_packet_candidate.json`
- draft_yymm4_csv: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv`
- dashboard_ingest: `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest`
- project_cockpit: `docs/PROJECT_COCKPIT.md`
- project_pipeline_mermaid: `docs/PROJECT_PIPELINE.mmd`

## Next Move

Review dashboard_preview.md and readiness_summary.json, then supply a real transcript or rerun build-transcript-substitution with --transcript before YMM4 import preview work.
