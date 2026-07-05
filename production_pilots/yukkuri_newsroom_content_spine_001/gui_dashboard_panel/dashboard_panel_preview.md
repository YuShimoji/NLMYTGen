# GUI Dashboard Panel Preview

- artifact_id: gui_dashboard_panel_ingest_001
- selected_candidate_id: sports_pitch_sequence_p05
- headline_status: sample fixture visible; real input blocked
- transcript_status: sample_fixture_not_real

## Capability Status

| capability | state | path |
|---|---|---|
| content_spine | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_001/MANIFEST.json` |
| ir_bridge | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_001/ir_bridge/bridge_manifest.json` |
| transcript_substitution | sample_fixture_not_real | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/substitution_manifest.json` |
| writer_ir | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_writer_ir_candidate.json` |
| cue_packet | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_cue_packet_candidate.json` |
| draft_yymm4_csv | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv` |
| real_transcript_input | blocked_by_real_input | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/real_input` |
| dashboard_ingest | ready | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest` |
| project_cockpit | ready | `docs/PROJECT_COCKPIT.md` |
| project_pipeline_mermaid | ready | `docs/PROJECT_PIPELINE.mmd` |
| yymm4_import_preview | deferred | `production_pilots/yukkuri_newsroom_content_spine_001/yymm4_import_preview` |
| thumbnail_visual_proof | deferred | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof` |

## Boundary Status

| boundary | status |
|---|---|
| source_status | offline_fixture_not_live |
| transcript_status | sample_fixture_not_real |
| timing_status | no_audio_or_yymm4_timing |
| audio_status | no_audio_generated_or_imported |
| rights_status | sample_only_no_publication |
| production_status | blocked_until_transcript_timing_and_human_review |
| public_upload_status | blocked_by_true_gate |
| ymm4_render_status | blocked_by_true_gate |

## Next Safe Action

Open dashboard_panel_preview.html for the one-surface read-only view; then review dashboard_preview.md and readiness_summary.json, then supply a real transcript or rerun build-transcript-substitution with --transcript before YMM4 import preview work.
