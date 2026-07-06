# YMM4 Import Preview Panel

- artifact_id: episode_002_yymm4_import_preview_pack_v1
- selected_candidate_id: factory_seed_dry_run_002
- status: preview_ready_local_offline
- source_artifact_index: `source_artifact_index.json`
- preview_csv: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/draft_yymm4_preview.csv`

## Status Legend

| status | visible meaning |
|---|---|
| ready | import preview state marker |
| partial | import preview state marker |
| sample_fixture_not_real | import preview state marker |
| draft_offline | import preview state marker |
| blocked_by_real_input | import preview state marker |
| blocked_by_true_gate | import preview state marker |
| deferred | import preview state marker |
| missing | import preview state marker |
| unknown | import preview state marker |
| dry_run | import preview state marker |
| validation_noise_nonblocking | import preview state marker |

## CSV Inventory

| item | value |
|---|---|
| source_csv_path | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv` |
| copied_preview_csv_path | `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/draft_yymm4_preview.csv` |
| row_count | 9 |
| header_mode | headerless |
| required_fields | speaker, text |
| missing_required_fields | [] |
| not_imported_to_yymm4 | True |

## Cue / Writer IR

| surface | status | rows_or_sections |
|---|---|---|
| cue_packet | ready_for_local_review | transcript_rows=9; sections=3 |
| writer_ir | draft_offline | utterances=9; sections=3 |

## Boundary Status

| boundary | status |
|---|---|
| source_status | offline_fixture_not_live |
| transcript_status | sample_fixture_not_real |
| real_transcript_status | blocked_by_real_input |
| timing_status | no_audio_or_yymm4_timing |
| audio_status | no_audio_generated_or_imported |
| rights_status | sample_only_no_publication |
| rights_gate | blocked_by_true_gate |
| production_status | blocked_by_true_gate |
| public_upload_status | blocked_by_true_gate |
| yymm4_gui_status | blocked_by_true_gate |
| yymm4_import_status | blocked_by_true_gate |
| yymm4_import_observed_status | not_imported_to_yymm4 |
| bridge_yymm4_import_status | not_run |
| yymm4_render_status | blocked_by_true_gate |

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
| not_imported_to_yymm4 | True |
| no_yymm4_gui_launch | True |
| no_yymm4_render | True |
| no_production_ymmp | True |
| no_external_media_download | True |
| validation_noise_nonblocking | True |
| dashboard_flags_confirmed | True |

## Validation Drift

- status: validation_noise_nonblocking
- ledger_path: `samples/_probe/newsroom_handoff/validation_drift_velocity_recovery_v1.json`
- full_pytest_policy: not rerun in this slice
- recent_full_pytest_result: 22 failed, 1173 passed, 28 skipped

## Next Safe Local Action

Review import_preview_panel.md and draft_yymm4_preview.csv locally, then prepare the thumbnail visual proof pack or a separate human YMM4 import review; do not launch, import, render, or create a production .ymmp in this preview pack.
