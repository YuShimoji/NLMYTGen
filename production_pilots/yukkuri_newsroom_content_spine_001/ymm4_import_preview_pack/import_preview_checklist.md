# YMM4 Import Preview Checklist

## Check Now

- Confirm the copied CSV is the intended draft import handoff file.
- Confirm `sample_fixture_not_real` is visible before any real transcript rerun.
- Confirm headerless CSV state is understood: headers are documented, not present in the import CSV.
- Confirm cue packet and Writer IR are candidates only.
- Confirm YMM4 GUI, import, render, production `.ymmp`, rights, public upload, OAuth, and payment gates remain closed.

## Reviewable Artifacts

- draft_yymm4_csv: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv`
- csv_row_contract: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv`
- csv_header_contract: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv`
- cue_packet: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_cue_packet_candidate.json`
- writer_ir: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_writer_ir_candidate.json`
- transcript_source: `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/transcript_source_probe.json`
- dashboard_readiness_ingest: `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/readiness_summary.json`
- gui_dashboard_panel: `production_pilots/yukkuri_newsroom_content_spine_001/gui_dashboard_panel/gui_dashboard_adapter.json`

## Next Move

Open import_preview_panel.md or import_preview_panel.html for offline review; then provide a verified real transcript via transcript_substitution_readiness/real_input/ or rerun build-transcript-substitution with --transcript before any actual YMM4 import.
