# Dashboard Readiness Ingest Preview

- artifact_id: content_spine_002_dashboard_readiness_ingest_v1
- selected_candidate_id: factory_seed_dry_run_002
- transcript_status: sample_fixture_not_real
- next_action: Review dashboard_preview.md and readiness_summary.json, then supply a verified local real transcript in the real_input drop-zone for a future replacement slice before YMM4 import preview work.

## Capability Grid

| capability | state | review_ready | path | note |
|---|---|---:|---|---|
| content_spine_002 | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_002/MANIFEST.json` | offline content/package is reviewable; source remains local fixture |
| ir_bridge_002 | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_002/ir_bridge/bridge_manifest.json` | draft Writer IR, cue packet, and CSV bridge exist; not production timing |
| transcript_substitution_002 | sample_fixture_not_real | true | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/substitution_manifest.json` | sample fixture is used until a real transcript is supplied |
| writer_ir | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_writer_ir_candidate.json` | candidate only; validate-ir/apply-production inputs are not accepted |
| cue_packet | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_cue_packet_candidate.json` | candidate not sent to external LLM or production operator |
| draft_yymm4_csv | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv` | CSV preview only; no YMM4 import, VoiceItem timing, or render proof |
| real_transcript_input | blocked_by_real_input | false | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/real_input` | drop a real NotebookLM/human-reviewed transcript here for a future replacement slice |
| dashboard_ingest | ready | true | `production_pilots/yukkuri_newsroom_content_spine_002/dashboard_readiness_ingest` | read-only status package generated for local review and later GUI adapter work |
| project_cockpit | ready | true | `docs/PROJECT_COCKPIT.md` | navigation doc; not a production gate |
| project_pipeline_mermaid | ready | true | `docs/PROJECT_PIPELINE.mmd` | navigation diagram; dashboard node should be visible |
| yymm4_import_preview | deferred | false | `production_pilots/yukkuri_newsroom_content_spine_002/yymm4_import_preview` | future slice; no YMM4 GUI/import/render in this ingest |
| thumbnail_visual_proof | deferred | false | `production_pilots/yukkuri_newsroom_content_spine_002/thumbnail_visual_proof` | future slice; no thumbnail image generation or public-ready proof |

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

## Ready For Review

- content_spine_002
- ir_bridge_002
- transcript_substitution_002
- writer_ir
- cue_packet
- draft_yymm4_csv
- dashboard_ingest
- project_cockpit
- project_pipeline_mermaid

## Needs Real Input

- real_transcript_input
