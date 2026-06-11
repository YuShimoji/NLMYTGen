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

## One-pass Targeted Layout Fix

- This update is a one-pass targeted layout fix for the current YMM4 diagnostic carrier candidate.
- It does not change the carrier variant, focal-chain meaning, callout meaning, host role, bottom caption reserve, or diagnostic-only boundary.
- Right focal label fix: `画面上の結果` keeps the same text and node, but the inherited rightward nudge was removed and the right-label font size was reduced from 42 to 38.
- Lower callout fix: all callout labels now use one common centered rule with font size 28 and zero horizontal offset.
- Do not continue same-screen micro-tuning. The next human review is only the two targeted fit/alignment checks below.

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
- classification: `pass_game_mechanics_ymmp_label_layout_fixed`
- carrier kind: `lecture_diagram_carrier`
- variant: `game_mechanics_explanation`
- frame: 1920x1080 / 16:9
- bottom caption reserve: clear=`true`, y=810, h=216
- focal chain labels: 入力操作 -> 内部ルール / 判定 -> 画面上の結果
- callout labels: 操作感 / 判定 / 当たり判定 / リスクとリターン
- host role: `non_focal_lower_corner_decoration_emotional_anchor`
- visible text: 7 items / 49 chars
- one-pass targeted fix: `true`
- no further micro-tuning recommended: `true`
- next decision gate: `accept_with_layout_caveat`

## Layout Fix Readback

- right focal label fit: `fits_after_one_pass_targeted_fix`
  - G28_LDC_Node_Right_Label: font=38, margin_each_side=16px, center_delta=(0, -4), fits=true
- callout label alignment: `common_centering_rule_applied`
  - G28_LDC_CalloutSlot_1_Label: font=28, margin_each_side=108px, center_delta=(0, -3), fits=true
  - G28_LDC_CalloutSlot_2_Label: font=28, margin_each_side=29px, center_delta=(0, -3), fits=true
  - G28_LDC_CalloutSlot_3_Label: font=28, margin_each_side=38px, center_delta=(0, -3), fits=true
- label overflow check: `true`

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
- `right_focal_label_fit`: `true`
- `callout_label_alignment`: `true`
- `label_overflow_absent`: `true`

## YMM4 Human Review Intake

- Open the probe in YMM4 and confirm the project opens without error.
- Capture a preview screenshot showing the carrier surface.
- Capture a timeline screenshot showing title, focal chain, callouts, hosts, and caption reserve items/layers.
- Confirm the chain reads `入力操作 -> 内部ルール / 判定 -> 画面上の結果`.
- Confirm the callouts read `操作感`, `判定 / 当たり判定`, and `リスクとリターン` without becoming a dense table.
- Confirm the hosts stay non-focal lower-corner decoration.
- Confirm the bottom caption reserve is visually clear.
- Targeted recheck only: confirm `画面上の結果` is inside the right node.
- Targeted recheck only: confirm `判定 / 当たり判定` and `リスクとリターン` look centered in their callout boxes.

## Next Review Inputs Required

- carrier path
- preview screenshot
- timeline screenshot
- item/layer confirmation
- bottom caption safe-area evidence

## Known Caveats

- This is a self-contained YMM4 diagnostic carrier candidate, not a production carrier.
- The one-pass targeted layout fix is verified by builder/readback geometry; final YMM4 visual recheck remains human-owned.
- Visible node and callout labels are review aids and do not approve production slot-fill or final copy.
- No render, video, audio, source footage, gameplay screenshot, external image, URL, raw reference, rights automation, or creative final acceptance is included.
- Do not continue same-screen micro-tuning. If the two targeted labels still fail visually, classify the remaining problem as layout_system_debt or redesign_required.
