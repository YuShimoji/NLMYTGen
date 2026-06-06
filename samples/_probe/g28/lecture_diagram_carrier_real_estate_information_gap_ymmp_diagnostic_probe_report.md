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
- classification: `pass_probe_polished`
- frame: 1920x1080 / 16:9
- caption reserve: y=810, h=216, clear=`true`
- focal chain labels: 元付情報 -> ポータル掲載 -> 借主判断
- callout labels: 情報遅延 / 掲載粒度の欠落 / 仲介インセンティブ
- host role: `non_focal_lower_corner_decoration_emotional_anchor`
- visible text: 7 items / 42 chars

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
