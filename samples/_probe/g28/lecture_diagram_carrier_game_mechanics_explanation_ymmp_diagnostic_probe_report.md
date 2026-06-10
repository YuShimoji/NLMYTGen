# G-28 Game Mechanics YMM4 Diagnostic Carrier Probe

Probe artifact: `g28_lecture_diagram_carrier_game_mechanics_explanation_ymmp_probe_v1`
Source artifact: `g28_lecture_diagram_carrier_game_mechanics_explanation_v1`
Variant id: `g28_ldc_game_mechanics_explanation`

This is a self-contained YMM4-compatible diagnostic carrier candidate for human review. It is not a render, production carrier approval, creative final acceptance, rights approval, source-footage intake, gameplay screenshot intake, or slot-fill.

## Generated Files

- YMM4 probe: `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
- readback JSON: `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe_readback.json`
- report: `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe_report.md`

## Relationship To HTML/Readback Precedent

- Source precedent: `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*`.
- The existing HTML/readback diagnostic surface was accepted for reviewability only.
- This probe turns that diagnostic shape into a YMM4-openable, ShapeItem/TextItem-only carrier candidate so the next human review can inspect YMM4 preview/timeline evidence.
- The middle node is visible as `内部ルール / 判定` to carry the semantics-note emphasis; this is diagnostic review text, not production copy approval.

## Boundary

- `diagnostic_only`: `true`
- `production_candidate`: `false`
- `self_contained_ymmp_probe`: `true`
- `production_render`: `false`
- `render_output`: `false`
- `creative_final_acceptance`: `false`
- `production_carrier_approval`: `false`
- `rights_approval`: `false`
- `slot_fill`: `false`
- `source_footage_intake`: `false`
- `gameplay_screenshot_intake`: `false`
- `external_material_intake`: `false`
- `audio_or_tts`: `false`
- `image_or_url_or_raw_reference`: `false`
- `real_estate_reopened`: `false`
- `newsroom_handoff_processed`: `false`
- `g27_revival`: `false`
- `rss_or_notebooklm_work`: `false`

## Readback Rollup

- status: `passed`
- classification: `pass_game_mechanics_ymmp_diagnostic_carrier_created`
- carrier kind: `lecture_diagram_carrier`
- variant: `game_mechanics_explanation`
- frame: 1920x1080 / 16:9
- bottom caption reserve: clear=`true`, y=810, h=216
- focal chain labels: 入力操作 -> 内部ルール / 判定 -> 画面上の結果
- callout labels: 操作感 / 判定 / 当たり判定 / リスクとリターン
- host role: `non_focal_lower_corner_decoration_emotional_anchor`
- visible text: 7 items / 49 chars

## Checks

- `diagnostic_only`: `true`
- `production_candidate_false`: `true`
- `carrier_kind_expected`: `true`
- `variant_expected`: `true`
- `source_artifact_id_expected`: `true`
- `variant_id_expected`: `true`
- `self_contained_ymmp_probe_created`: `true`
- `frame_16_9_1920_1080`: `true`
- `focal_chain_count_3`: `true`
- `focal_chain_labels_expected`: `true`
- `callout_count_3`: `true`
- `callout_labels_expected`: `true`
- `bottom_caption_reserve_clear`: `true`
- `focal_area_in_main_canvas`: `true`
- `host_role_non_focal`: `true`
- `diagnostic_text_budget_bounded`: `true`
- `dense_table_false`: `true`
- `indexed_whiteboard_false`: `true`
- `external_image_count_zero`: `true`
- `external_url_count_zero`: `true`
- `source_footage_count_zero`: `true`
- `audio_item_count_zero`: `true`
- `tts_or_voice_item_count_zero`: `true`
- `render_output_false`: `true`
- `production_approval_false`: `true`
- `creative_final_acceptance_false`: `true`
- `rights_approval_false`: `true`
- `token_like_pattern_count_zero`: `true`
- `carrier_not_modified_in_place`: `true`

## YMM4 Human Review Intake

- Open the probe in YMM4 and confirm the project opens without error.
- Capture a preview screenshot showing the carrier surface.
- Capture a timeline screenshot showing title, focal chain, callouts, hosts, and caption reserve items/layers.
- Confirm the chain reads `入力操作 -> 内部ルール / 判定 -> 画面上の結果`.
- Confirm the callouts read `操作感`, `判定 / 当たり判定`, and `リスクとリターン` without becoming a dense table.
- Confirm the hosts stay non-focal lower-corner decoration.
- Confirm the bottom caption reserve is visually clear.

## Next Review Inputs Required

- carrier path
- preview screenshot
- timeline screenshot
- item/layer confirmation
- bottom caption safe-area evidence

## Known Caveats

- This is a self-contained YMM4 diagnostic carrier candidate, not a production carrier.
- It has not been visually accepted in the YMM4 GUI; human preview and timeline screenshots are still required.
- Visible node and callout labels are review aids and do not approve production slot-fill or final copy.
- No render, video, audio, source footage, gameplay screenshot, external image, URL, raw reference, rights automation, or creative final acceptance is included.
