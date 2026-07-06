# GUI Dashboard Panel Preview

- artifact_id: content_spine_002_gui_dashboard_panel_v1
- selected_candidate_id: factory_seed_dry_run_002
- headline_status: sample fixture visible; validation drift nonblocking
- transcript_status: sample_fixture_not_real
- yymm4_import_status: blocked_by_true_gate
- validation_noise_status: validation_noise_nonblocking

## Capability Status

| capability | state | path |
|---|---|---|
| content_spine_002 | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/MANIFEST.json` |
| ir_bridge_002 | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/ir_bridge/bridge_manifest.json` |
| transcript_substitution_002 | sample_fixture_not_real | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/substitution_manifest.json` |
| writer_ir | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_writer_ir_candidate.json` |
| cue_packet | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_cue_packet_candidate.json` |
| draft_yymm4_csv | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv` |
| real_transcript_input | blocked_by_real_input | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/real_input` |
| dashboard_ingest | ready | `production_pilots/yukkuri_newsroom_content_spine_002/dashboard_readiness_ingest` |
| project_cockpit | ready | `docs/PROJECT_COCKPIT.md` |
| project_pipeline_mermaid | ready | `docs/PROJECT_PIPELINE.mmd` |
| yymm4_import_preview | deferred | `production_pilots/yukkuri_newsroom_content_spine_002/yymm4_import_preview` |
| thumbnail_visual_proof | deferred | `production_pilots/yukkuri_newsroom_content_spine_002/thumbnail_visual_proof` |
| validation_noise | validation_noise_nonblocking | `samples/_probe/newsroom_handoff/validation_drift_velocity_recovery_v1.json` |

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
| yymm4_import_status | blocked_by_true_gate |
| ymm4_render_status | blocked_by_true_gate |

## Boundary Flags

| flag | value |
|---|---|
| dry_run | True |
| sample_fixture_not_real | True |
| no_real_transcript | True |
| rights_boundary | True |
| public_upload_closed | True |
| yymm4_render_closed | True |
| no_yymm4_import | True |

## Validation Drift

- status: validation_noise_nonblocking
- ledger_path: `samples/_probe/newsroom_handoff/validation_drift_velocity_recovery_v1.json`
- recent_full_pytest_result: 22 failed, 1173 passed, 28 skipped
- full_pytest_policy: not rerun in this slice

## Next Safe Action

Open dashboard_panel_preview.html for GUI review, then use the confirmed status surface to prepare the episode 002 YMM4 import preview pack without launching, importing, or rendering in YMM4.
