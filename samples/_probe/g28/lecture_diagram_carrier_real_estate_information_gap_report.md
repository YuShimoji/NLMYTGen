# G-28 Lecture Diagram Carrier g28_ldc_real_estate_information_gap Variant Report

- artifact: g28_lecture_diagram_carrier_real_estate_information_gap_v1
- status: passed
- diagnostic_only: true
- production_candidate: false
- ymmp_generation: not_generated_boundary
- primitive_item_count: 14
- semantic_group_count: 5
- semantic_element_count: 8
- callout_slot_count: 3
- caption_reserve_clear: true
- failures: none

## Boundary

This is a diagnostic skeleton/readback artifact, not a production carrier. It
does not copy or transform reference images, does not use external image assets,
does not record image paths or URLs, does not generate a YMM4 project file, does
not render, and does not claim creative final acceptance.

## Layer Order

- L1: G28_LDC_BG_Stage (ShapeItem, decoration, group=G28_LDC_Stage)
- L2: G28_LDC_TitleBand_BG (ShapeItem, label, group=G28_LDC_TitleBand)
- L3: G28_LDC_Title_Text (TextItem, label, group=G28_LDC_TitleBand)
- L4: G28_LDC_Focal_Core (ShapeItem, focal_anchor, group=G28_LDC_FocalGroup)
- L5: G28_LDC_Focal_Label (TextItem, label, group=G28_LDC_FocalGroup)
- L6: G28_LDC_Node_Left (ShapeItem, internal_node, group=G28_LDC_FocalGroup)
- L6: G28_LDC_Node_Right (ShapeItem, internal_node, group=G28_LDC_FocalGroup)
- L7: G28_LDC_Connector_Left (ShapeItem, connector, group=G28_LDC_FocalGroup)
- L7: G28_LDC_Connector_Right (ShapeItem, connector, group=G28_LDC_FocalGroup)
- L8: G28_LDC_CalloutSlot_1 (ShapeItem, supporting, group=G28_LDC_CalloutSlots)
- L8: G28_LDC_CalloutSlot_2 (ShapeItem, supporting, group=G28_LDC_CalloutSlots)
- L8: G28_LDC_CalloutSlot_3 (ShapeItem, supporting, group=G28_LDC_CalloutSlots)
- L9: G28_LDC_Host_Left (ShapeItem, decoration, group=G28_LDC_Hosts)
- L9: G28_LDC_Host_Right (ShapeItem, decoration, group=G28_LDC_Hosts)

## Readback

- caption reserve: y=810, h=216, clear=true
- focal area: {"x":560,"y":240,"width":800,"height":360}
- host role: lower-corner decoration / emotional anchor, not focal
- callout slots: G28_LDC_CalloutSlot_1, G28_LDC_CalloutSlot_2, G28_LDC_CalloutSlot_3

## Variant Semantics

- variant_id: g28_ldc_real_estate_information_gap
- composition_type: center-focal
- focal_chain: 元付情報 -> ポータル掲載 -> 借主判断
- callouts: 情報遅延, 掲載粒度の欠落, 仲介インセンティブ
- host_role: non-focal lower-corner decoration
- failure_modes: dense_table, indexed_whiteboard, host_as_focal, subtitle_collision, source_over_decoration
- dense_table: false
- indexed_whiteboard: false
- source_footage_carrier: false
- external_image_count: 0
- external_url_count: 0
- token_like_pattern_count: 0
- text_budget_dense: false

## Limitations

- No YMM4 .ymmp file generated in this slice because G-28 v0.1 still excludes zero-generation.
- HTML is visualization-only and not a render or creative final acceptance.
- Callout slots are empty placeholders until a theme-specific slot-fill slice exists.
