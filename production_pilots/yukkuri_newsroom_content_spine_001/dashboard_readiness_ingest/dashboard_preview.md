# Dashboard Readiness Ingest Preview

- artifact_id: dashboard_readiness_ingest_001
- selected_candidate_id: sports_pitch_sequence_p05
- transcript_status: sample_fixture_not_real
- next_action: Review dashboard_preview.md and readiness_summary.json, then supply a real transcript or rerun build-transcript-substitution with --transcript before YMM4 import preview work.

## Capability Grid

| capability | state | review_ready | path | note |
|---|---|---:|---|---|
| content_spine | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/MANIFEST.json` | offline content/package is reviewable; source remains local fixture |
| ir_bridge | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/ir_bridge/bridge_manifest.json` | draft Writer IR, cue packet, and CSV bridge exist; not production timing |
| transcript_substitution | sample_fixture_not_real | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/substitution_manifest.json` | sample fixture is used until a real transcript is supplied |
| writer_ir | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_writer_ir_candidate.json` | candidate only; validate-ir/apply-production inputs are not accepted |
| cue_packet | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_cue_packet_candidate.json` | candidate not sent to external LLM or production operator |
| draft_yymm4_csv | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/regenerated_draft_yymm4.csv` | CSV preview only; no YMM4 import, VoiceItem timing, or render proof |
| real_transcript_input | blocked_by_real_input | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/real_input` | drop a real NotebookLM/human-reviewed transcript here or rerun with --transcript |
| dashboard_ingest | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest` | read-only status package generated for local review and later GUI adapter work |
| project_cockpit | ready | true | `docs/PROJECT_COCKPIT.md` | navigation doc; not a production gate |
| project_pipeline_mermaid | ready | true | `docs/PROJECT_PIPELINE.mmd` | navigation diagram; dashboard node should be visible |
| yymm4_import_preview | deferred | false | `production_pilots/yukkuri_newsroom_content_spine_001/yymm4_import_preview` | future slice; no YMM4 GUI/import/render in this ingest |
| thumbnail_visual_proof | deferred | false | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof` | future slice; no thumbnail image generation or public-ready proof |

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

## Ready For Review

- content_spine
- ir_bridge
- transcript_substitution
- writer_ir
- cue_packet
- draft_yymm4_csv
- dashboard_ingest
- project_cockpit
- project_pipeline_mermaid

## Needs Real Input

- real_transcript_input
