# G-28 Map / Evidence Carrier Skeleton Report

- artifact: g28_map_evidence_carrier_skeleton_v1
- status: passed
- diagnostic_only: true
- production_candidate: false
- ymmp_generation: not_generated_boundary
- composition_type: center-focal
- primitive_item_count: 14
- semantic_group_count: 6
- semantic_element_count: 11
- annotation_slot_count: 3
- source_note_exists: true
- source_note_bounded: true
- caption_reserve_clear: true
- dense_table: false
- indexed_whiteboard: false
- tiny_text: false
- external_image_count: 0
- external_url_count: 0
- token_like_pattern_count: 0
- failures: none

## Boundary

This is a diagnostic skeleton/readback artifact, not a production carrier. It
does not use a real map, satellite image, image asset, image path, URL, raw
reference, YMM4 project generation, render, production timing, or creative final
acceptance.

## SCS Mapping

- archetype: Map / Evidence Carrier
- composition_type: center-focal
- rationale: A single map/evidence surface is the focal argument surface; annotation slots support it without becoming equal-weight cards.
- reading_order: G28_MEC_Title_Text -> G28_MEC_EvidenceSurface -> G28_MEC_LabelAnchor_1 -> G28_MEC_LabelAnchor_2 -> G28_MEC_AnnotationSlot_1 -> G28_MEC_AnnotationSlot_2 -> G28_MEC_AnnotationSlot_3 -> G28_MEC_SourceNote_Text

## Layer Order

- L1: G28_MEC_BG_Stage (ShapeItem, decoration, group=G28_MEC_Stage)
- L2: G28_MEC_TitleBand_BG (ShapeItem, label, group=G28_MEC_TitleBand)
- L3: G28_MEC_Title_Text (TextItem, label, group=G28_MEC_TitleBand)
- L4: G28_MEC_EvidenceSurface (ShapeItem, focal_anchor, group=G28_MEC_EvidenceSurface)
- L5: G28_MEC_LabelAnchor_1 (ShapeItem, connector, group=G28_MEC_Annotations)
- L5: G28_MEC_LabelAnchor_2 (ShapeItem, connector, group=G28_MEC_Annotations)
- L6: G28_MEC_LeaderLine_1 (ShapeItem, connector, group=G28_MEC_Annotations)
- L7: G28_MEC_AnnotationSlot_1 (ShapeItem, supporting, group=G28_MEC_Annotations)
- L7: G28_MEC_AnnotationSlot_2 (ShapeItem, supporting, group=G28_MEC_Annotations)
- L7: G28_MEC_AnnotationSlot_3 (ShapeItem, supporting, group=G28_MEC_Annotations)
- L8: G28_MEC_SourceNote_BG (ShapeItem, supporting, group=G28_MEC_SourceNote)
- L9: G28_MEC_SourceNote_Text (TextItem, label, group=G28_MEC_SourceNote)
- L10: G28_MEC_Host_Left (ShapeItem, decoration, group=G28_MEC_Hosts)
- L10: G28_MEC_Host_Right (ShapeItem, decoration, group=G28_MEC_Hosts)

## Readback

- evidence area: {"x":240,"y":180,"width":1440,"height":500}, in_main_canvas=true
- annotation slots: G28_MEC_AnnotationSlot_1, G28_MEC_AnnotationSlot_2, G28_MEC_AnnotationSlot_3
- source note: text=出典確認済み, chars=6, font_size=32
- host role: lower-corner decoration / emotional anchor, not focal
- caption reserve: y=810, h=216, clear=true
- failure modes: map_label_overload, source_note_overload, indexed_whiteboard, tiny_text, subtitle_collision, decorative_map_without_argument

## Limitations

- No real map, satellite image, image path, or URL is used in this diagnostic skeleton.
- HTML is visualization-only and not a render or creative final acceptance.
- Annotation slots are empty placeholders until a later scoped slot-fill slice exists.
- No YMM4 .ymmp file is generated in this slice.
