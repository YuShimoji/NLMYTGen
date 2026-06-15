# G-28 Map / Evidence YMM4 Diagnostic Carrier Probe

Probe artifact: `g28_map_evidence_carrier_ymmp_probe_v1`
Source artifact: `g28_map_evidence_carrier_skeleton_v1`

This is a self-contained YMM4-compatible diagnostic carrier candidate for human review. It is not a render, production carrier approval, creative final acceptance, rights approval, source-footage intake, image intake, or slot-fill.

## Generated Files

- YMM4 probe: `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`
- readback JSON: `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_readback.json`
- report: `samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe_report.md`

## Why This Artifact

- The game_mechanics YMM4 diagnostic carrier remains reviewable but is now recorded as layout_system_debt.
- Same-screen tuning stays stopped.
- This slice advances a separate G-28 reviewable artifact, speed-first, before a later cross-screen layout-normalization audit.

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
- `real_map_or_satellite_image_intake`: `false`
- `external_material_intake`: `false`
- `audio_or_tts`: `false`
- `image_or_url_or_raw_reference`: `false`
- `game_mechanics_same_screen_tuning`: `false`
- `common_foundation_work`: `false`

## Readback Rollup

- status: `passed`
- classification: `pass_map_evidence_ymmp_diagnostic_carrier_created`
- carrier kind: `map_evidence_carrier`
- variant: `map_evidence`
- frame: 1920x1080 / 16:9
- bottom caption reserve: clear=`true`, y=810, h=216
- evidence surface: in_main_canvas=`true`
- annotation slots: 3
- source note: `出典確認済み`, bounded=`true`
- host role: `non_focal_lower_corner_decoration_emotional_anchor`
- visible text: 2 items / 15 chars

## Checks

- `diagnostic_only`: `true`
- `production_candidate_false`: `true`
- `carrier_kind_expected`: `true`
- `variant_expected`: `true`
- `self_contained_ymmp_probe_created`: `true`
- `frame_16_9_1920_1080`: `true`
- `caption_reserve_bottom_20pct`: `true`
- `caption_reserve_clear`: `true`
- `evidence_area_in_main_canvas`: `true`
- `annotation_slot_count_2_to_4`: `true`
- `source_note_area_exists`: `true`
- `source_note_text_budget_bounded`: `true`
- `host_role_non_focal`: `true`
- `dense_table_false`: `true`
- `indexed_whiteboard_false`: `true`
- `tiny_text_false_or_bounded`: `true`
- `primitive_item_count_bounded`: `true`
- `shape_item_count_expected`: `true`
- `text_item_count_expected`: `true`
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

## Next Review Inputs Required

- carrier path
- preview screenshot
- timeline screenshot
- item/layer confirmation
- caption reserve visual confirmation
- human decision: accept / accept_with_caveats / revise_once / layout_system_debt / redesign_required

## Known Caveats

- This is a self-contained YMM4 diagnostic carrier candidate, not a production carrier.
- The evidence surface is abstract and uses no real map, satellite image, image path, URL, or raw reference.
- Annotation slots are empty placeholders until a later scoped slot-fill slice exists.
- No render, video, audio, source footage, external image, rights automation, or creative final acceptance is included.
- Game-mechanics same-screen micro-tuning remains stopped; this advances a separate reviewable artifact.
