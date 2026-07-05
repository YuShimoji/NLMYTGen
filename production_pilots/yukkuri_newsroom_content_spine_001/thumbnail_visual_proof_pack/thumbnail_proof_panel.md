# Thumbnail Visual Proof Pack

- artifact_id: thumbnail_visual_proof_pack_001
- selected_candidate_id: sports_pitch_sequence_p05
- selected_title: Why a 155 km/h fastball followed by a 140 km/h slider changes the at-bat
- primary_visual_proof: `thumbnail_layout_proof.svg`
- rights_status: sample_only_no_publication
- transcript_status: sample_fixture_not_real

## Status Palette

ready, partial, sample_fixture_not_real, draft_offline, blocked_by_real_input, blocked_by_true_gate, deferred, missing, unknown

## Title / Text Candidates

- primary: 155 -> 140 km/h (draft_offline)
- primary: Why a 155 km/h fastball followed by a 140 km/h slider changes the at-bat (draft_offline)
- short: 15km/hの罠 (draft_offline)
- short: 速球のあとが怖い (draft_offline)
- short: 外低めスライダー (draft_offline)

## Concepts

- speed_drop_scoreboard: ready - 15km/hの罠
- low_outer_zone_focus: draft_offline - 速球のあとが怖い
- yukkuri_reaction_data_card: draft_offline - 外低めスライダー

## Visual Constraints

- proof_status: static_proof_only_not_final_thumbnail
- visual_motif: Original scoreboard strip plus two pitch cards connected by a speed-drop arrow.
- no_external_media: true

## Readiness Grid

| capability | state | review_ready | path | note |
|---|---|---:|---|---|
| content_spine | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/MANIFEST.json` | current local/offline episode package |
| thumbnail_brief | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_brief_001.md` | text-only direction brief, not an image |
| episode_candidate | draft_offline | true | `production_pilots/yukkuri_newsroom_content_spine_001/episode_candidate_001.md` | episode hook and beat outline are available |
| thumbnail_layout_proof | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/thumbnail_layout_proof.svg` | abstract SVG proof generated locally |
| transcript_source | sample_fixture_not_real | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/transcript_source_probe.json` | current transcript still uses sample fixture |
| real_transcript_input | blocked_by_real_input | false | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/real_input` | verified real transcript remains required before production |
| dashboard_readiness_ingest | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/readiness_summary.json` | read-only readiness summary exists |
| gui_dashboard_panel | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/gui_dashboard_panel/gui_dashboard_adapter.json` | static dashboard panel exists |
| ymm4_import_preview | ready | true | `production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/import_readiness_summary.json` | import preview exists but no actual YMM4 import was run |
| source_rights_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/topic_candidates.json` | sample_only_no_publication |
| external_media_download | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_brief_001.md` | no image, logo, screenshot, or sports media download is allowed here |
| public_upload_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/readiness_summary.json` | no YouTube upload, scheduling, visibility, or public-ready claim |
| thumbnail_image_generation | deferred | false | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_output` | static proof only; no PNG/JPG final output generated |
| production_thumbnail_output | missing | false | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_output/final_thumbnail.png` | no production image output exists |
| timing_audio_status | unknown | false | `production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/import_readiness_summary.json` | timing=no_audio_or_yymm4_timing; audio=no_audio_generated_or_imported |
| ymm4_gui_render_status | blocked_by_true_gate | false | `production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/import_readiness_summary.json` | no YMM4 GUI launch, import, or render in this proof |
| visual_polish | partial | true | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/thumbnail_proof_panel.html` | composition reviewable, final taste and template transfer still pending |

## Boundary Status

| boundary | status |
|---|---|
| source_status | offline_fixture_not_live |
| rights_status | sample_only_no_publication |
| transcript_status | sample_fixture_not_real |
| sample_fixture_status | sample_fixture_not_real |
| real_transcript_status | blocked_by_real_input |
| thumbnail_proof_status | ready |
| thumbnail_image_status | deferred |
| external_media_status | blocked_by_true_gate |
| public_upload_status | blocked_by_true_gate |
| yymm4_gui_import_render_status | blocked_by_true_gate |
| production_status | blocked_by_true_gate |

## Next Safe Local Action

Open thumbnail_proof_panel.html or thumbnail_layout_proof.svg for offline composition review; then choose accept_direction, revise_copy, revise_layout, or hold before any real-source, YMM4, or final thumbnail work.
