# YMM4 Import Preview Pack

- artifact_id: ymm4_import_preview_pack_001
- selected_candidate_id: sports_pitch_sequence_p05
- transcript_status: sample_fixture_not_real
- csv_rows: 10
- copied_csv: `production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/draft_yymm4_import_preview.csv`

## Status Palette

ready, partial, sample_fixture_not_real, draft_offline, blocked_by_real_input, blocked_by_true_gate, deferred, missing, unknown

## Readiness Grid

| capability | state | review_ready | path | note |
|---|---|---:|---|---|
| draft_yymm4_csv | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv` | copied into the preview package; no YMM4 import has been run |
| csv_row_contract | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv` | 10 data rows; column_count_ok=True |
| csv_header_contract | partial | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv` | YMM4 import CSV is headerless; speaker/text headers are documented but absent by design |
| cue_packet | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_cue_packet_candidate.json` | candidate only; external LLM and production operator steps were not run |
| writer_ir | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_writer_ir_candidate.json` | candidate only; row ranges, timing, maps, and validate/apply remain gated |
| transcript_source | sample_fixture_not_real | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/transcript_source_probe.json` | sample fixture is not a real NotebookLM/human-reviewed transcript |
| real_transcript_input | blocked_by_real_input | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/real_input` | supply a verified local transcript before production import review |
| dashboard_readiness_ingest | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/readiness_summary.json` | read-only status ingest is available to cross-check import state |
| gui_dashboard_panel | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/gui_dashboard_panel/gui_dashboard_adapter.json` | static read-only panel exists; no GUI runtime or YMM4 launch implied |
| timing_audio_status | unknown | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/transcript_source_probe.json` | timing=no_audio_or_yymm4_timing; audio=no_audio_generated_or_imported |
| source_rights_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/transcript_source_probe.json` | sample_only_no_publication |
| production_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/transcript_source_probe.json` | blocked until real transcript, timing, source review, and human acceptance exist |
| public_upload_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/readiness_summary.json` | no YouTube upload, scheduling, visibility, or public-ready claim |
| ymm4_gui_import_status | deferred | false | `production_pilots/yukkuri_newsroom_content_spine_001/manual_yymm4_import` | YMM4 was not launched; import is a future manual/verified gate |
| ymm4_render_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/render` | no render or video output was generated |
| production_ymmp | missing | false | `production_pilots/yukkuri_newsroom_content_spine_001/production.ymmp` | not created in this slice; zero-generation remains out of scope |

## CSV Contract

- header_mode: headerless_yymm4_csv
- required_headers: speaker, text
- missing_headers: speaker, text
- missing_headers_block_import: false
- column_count_ok: true

## Boundary Status

| boundary | status |
|---|---|
| source_status | offline_fixture_not_live |
| transcript_status | sample_fixture_not_real |
| timing_status | no_audio_or_yymm4_timing |
| audio_status | no_audio_generated_or_imported |
| rights_status | sample_only_no_publication |
| production_status | blocked_by_true_gate |
| public_upload_status | blocked_by_true_gate |
| ymm4_gui_status | blocked_by_true_gate |
| ymm4_import_status | deferred |
| ymm4_render_status | blocked_by_true_gate |

## Next Safe Local Action

Open import_preview_panel.md or import_preview_panel.html for offline review; then provide a verified real transcript via transcript_substitution_readiness/real_input/ or rerun build-transcript-substitution with --transcript before any actual YMM4 import.
