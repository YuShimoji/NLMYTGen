# G-28 Real Estate Information Gap YMM4 Diagnostic Probe

Probe artifact: `g28_lecture_diagram_carrier_real_estate_information_gap_ymmp_probe_v1`
Source artifact: `g28_lecture_diagram_carrier_real_estate_information_gap_v1`
Variant id: `g28_ldc_real_estate_information_gap`

This is a self-contained YMM4-compatible diagnostic probe. It is not a render, production carrier approval, creative final acceptance, rights approval, source-footage intake, or slot-fill.

## Polish Revision

- revision id: `g28_real_estate_information_gap_ymmp_polish_v1`
- source human decision: `revise_probe`
- bounded scope: `yellow connector alignment`, `rectangle text centering`, `callout spacing`, `small visual offsets`
- boundary note: Diagnostic-only polish revision; no production approval, render, slot-fill, image, URL, audio, TTS, or source footage.

## Layout Contract Revision

- revision id: `g28_real_estate_information_gap_layout_contract_v1`
- classification: `pass_layout_contract_implemented`
- next decision: `ready_for_human_gui_recheck_before_review_console_ingest`
- scope: derived connector geometry, registered text offsets, callout row rule, and tolerance readback metrics.
- boundary: diagnostic-only implementation improvement; not production approval, render approval, rights approval, creative final acceptance, or slot-fill.

## Right Node Alignment Revision

- revision id: `g28_real_estate_information_gap_right_node_alignment_v1`
- source human decision: `revise_probe_again_narrow_right_node_text_alignment`
- classification: `pass_right_node_alignment_fixed`
- target label: `G28_LDC_Node_Right_Label`
- observed issue: Human GUI recheck saw only the right node label as visually off-center inside its rectangle.
- cause classification: `right_node_registered_optical_offset_needed`
- formula change: No common text-centering formula change; the right node label gets a bounded x-axis optical offset.
- boundary note: Diagnostic-only right-node alignment fix; no render, production approval, slot-fill, image, URL, audio, TTS, or source footage.

## Callout Label Alignment Revision

- revision id: `g28_real_estate_information_gap_callout_label_alignment_v1`
- source human decision: `revise_probe_again_narrow_callout_label_alignment`
- classification: `pass_callout_label_alignment_fixed`
- target label: `G28_LDC_CalloutSlot_3_Label`
- observed issue: Human GUI correction identified the lower-right callout label as the actual off-center target, not the right node label.
- target correction: Previous right-node alignment fix is retained; the corrected target is the third callout label.
- cause classification: `callout_label_registered_optical_offset_needed`
- formula change: No common callout formula change; the third callout label gets a bounded x-axis optical offset.
- boundary note: Diagnostic-only callout label alignment fix; no render, production approval, slot-fill, image, URL, audio, TTS, or source footage.

## Callout Label Human Calibration

- revision id: `g28_real_estate_information_gap_callout_label_human_calibration_v1`
- source human decision: `apply_one_time_human_calibrated_callout_x_and_record_layout_debt`
- classification: `pass_callout_label_human_calibrated`
- target label: `G28_LDC_CalloutSlot_3_Label`
- observed issue: Human GUI recheck still saw the lower-right callout label as left-shifted after the bounded offset fix.
- computed x before human calibration: 289
- previous polished x: 289
- human calibrated x: 313
- calibration delta x: 24
- cause classification: `callout_text_layout_model_debt`
- formula change: No formula success claim; the existing formula output is overridden once with the human-calibrated YMM4 X value.
- reuse risk: `high_do_not_generalize`
- boundary note: Diagnostic-only human calibration; no render, production approval, Review Console ingest, slot-fill, image, URL, audio, TTS, or source footage.
- no more pixel tuning boundary: If this remains visually off, stop individual offset changes and redesign the callout text layout system.

## Generated Files

- YMM4 probe: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp`
- readback JSON: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json`
- report: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md`

## Boundary

- `diagnostic_only`: `true`
- `production_candidate`: `false`
- `self_contained_ymmp_probe`: `true`
- `production_render`: `false`
- `render_output`: `false`
- `creative_final_acceptance`: `false`
- `production_carrier_approval`: `false`
- `slot_fill`: `false`
- `source_footage_intake`: `false`
- `audio_or_tts`: `false`
- `image_or_url_or_raw_reference`: `false`
- `g27_revival`: `false`
- `rss_or_notebooklm_work`: `false`

## Readback Rollup

- status: `passed`
- classification: `pass_callout_label_human_calibrated`
- frame: 1920x1080 / 16:9
- caption reserve: y=810, h=216, clear=`true`
- focal chain labels: 元付情報 -> ポータル掲載 -> 借主判断
- callout labels: 情報遅延 / 掲載粒度の欠落 / 仲介インセンティブ
- host role: `non_focal_lower_corner_decoration_emotional_anchor`
- visible text: 7 items / 42 chars

## Layout Contract Readback

- text_center_error_px: 0 (threshold 1)
- registered_optical_offset_max_px: 5.657 (threshold 6)
- connector_alignment_error_px: 0 (threshold 2)
- caption_reserve_overlap_px: 0
- callout_density: width=0.818, height=0.333
- host_focality_risk: `low`
- formula: top_left = center(target_box) + registered_visual_offset - estimated_text_bbox / 2
- metric scope: Measures implementation placement against the registered offset and estimated text box; it is not a rendered YMM4 glyph optical-center measurement.
- right node applied offset: x=4, y=-4
- right node caveat: text_center_error_px=0 means the label was placed exactly at the registered offset; the human GUI recheck is the authority for rendered optical centering.
- callout label applied offset: x=4, y=-3
- callout label caveat: text_center_error_px=0 means the callout label was placed exactly at the registered offset; the human GUI correction is the authority for rendered optical centering.
- callout human calibrated override: `true`
- callout human calibrated x: computed=289, previous=289, human=313, delta=24
- callout human calibration caveat: This pass records a one-time human-calibrated YMM4 X override. It is not a proof that the callout text formula is reusable.
- layout system debt: g28_callout_text_layout_model_debt_v1
- connector rule: connector spans from source edge to target edge, with y centered on the adjacent side node and fixed thickness.
- callout supported counts: 2, 3
- 4-callout handling: fail fast or change layout; do not squeeze into the current 3-slot row.

## Checks

- `diagnostic_only`: `true`
- `production_candidate_false`: `true`
- `source_artifact_id_expected`: `true`
- `variant_id_expected`: `true`
- `self_contained_ymmp_probe_created`: `true`
- `frame_16_9_1920_1080`: `true`
- `caption_reserve_bottom_20pct`: `true`
- `caption_reserve_clear`: `true`
- `focal_area_in_main_canvas`: `true`
- `focal_chain_nodes_3`: `true`
- `focal_chain_labels_expected`: `true`
- `callout_count_3`: `true`
- `callout_labels_expected`: `true`
- `host_role_non_focal`: `true`
- `layer_order_matches_contract`: `true`
- `diagnostic_text_budget_bounded`: `true`
- `dense_table_false`: `true`
- `indexed_whiteboard_false`: `true`
- `external_image_count_zero`: `true`
- `external_url_count_zero`: `true`
- `source_footage_count_zero`: `true`
- `audio_item_count_zero`: `true`
- `tts_or_voice_item_count_zero`: `true`
- `render_output_false`: `true`
- `creative_final_acceptance_false`: `true`
- `production_approval_false`: `true`
- `token_like_pattern_count_zero`: `true`
- `carrier_not_modified_in_place`: `true`
- `polish_revision_bounded`: `true`
- `layout_contract_metrics_present`: `true`
- `layout_contract_tolerances_pass`: `true`
- `right_node_alignment_fix_recorded`: `true`
- `callout_label_alignment_fix_recorded`: `true`
- `callout_label_human_calibration_recorded`: `true`

## YMM4 Mapping

- `G28_LDC_Stage`: `G28_LDC_BG_Stage`
- `G28_LDC_TitleBand`: `G28_LDC_TitleBand_BG`, `G28_LDC_Title_Text`
- `G28_LDC_FocalGroup`: `G28_LDC_Focal_Core`, `G28_LDC_Node_Left`, `G28_LDC_Node_Right`, `G28_LDC_Connector_Left`, `G28_LDC_Connector_Right`, `G28_LDC_Node_Left_Label`, `G28_LDC_Node_Center_Label`, `G28_LDC_Node_Right_Label`
- `G28_LDC_CalloutSlots`: `G28_LDC_CalloutSlot_1`, `G28_LDC_CalloutSlot_2`, `G28_LDC_CalloutSlot_3`, `G28_LDC_CalloutSlot_1_Label`, `G28_LDC_CalloutSlot_2_Label`, `G28_LDC_CalloutSlot_3_Label`
- `G28_LDC_Hosts`: `G28_LDC_Host_Left`, `G28_LDC_Host_Right`

## Human GUI Check

- Open the probe in YMM4 and confirm the project opens without error.
- Confirm the focal chain reads as `元付情報 -> ポータル掲載 -> 借主判断`.
- Confirm the bottom caption reserve remains visually clear.
- Confirm the three callouts are readable without becoming a table.
- Confirm the hosts stay lower-corner, non-focal, and non-evidence-like.
- Confirm the surface does not imply a real listing, real portal, real property, render approval, rights approval, or production use.

## Limitations

- This is a self-contained diagnostic probe, not production carrier approval.
- This revision addresses bounded human-review polish only after revise_probe; it does not change the diagnostic-only boundary.
- It uses visible node/callout labels for GUI review; this does not approve production text density.
- No render, video, audio, source footage, external image, URL, raw reference, rights automation, or slot-fill is included.
