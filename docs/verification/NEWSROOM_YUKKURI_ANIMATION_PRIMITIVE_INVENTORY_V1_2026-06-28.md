# Newsroom Yukkuri Animation Primitive Inventory v1

artifact_id: newsroom_yukkuri_animation_primitive_inventory_v1_2026_06_28
schema_version: newsroom_yukkuri_animation_primitive_inventory.v1
primitive_count: 11
first_probe_candidate_count: 5


## Candidate Primitives

| primitive_id | purpose | likely_yym4_representation | required_assets | source_asset_status | automation_risk | first_probe_candidate |
|---|---|---|---|---|---|---|
| head_nod | confirm or acknowledge a narration point | GroupItem or TachieItem transform keyframes; prior nod template evidence | ["nod_head_probe", "skit_group_template_source"] | present | medium | true |
| head_shake | show denial, caution, or disagreement | GroupItem X-axis shake / deny template family | ["skit_group_registry", "group_motion_map"] | present | medium | false |
| expression_swap | externalize reaction without adding dialogue | face map or image source swap | ["reimu_expression_easy", "reimu_expression_anger", "reimu_expression_panic", "face_map_extracted"] | present | low | true |
| mouth_eye_change_if_feasible | small face-part change where YMM4 route supports it | TachieFaceParameter or face-map bundle route | ["face_map_bundle_default", "face_map_bundle_haitatsuin"] | present | medium | false |
| character_entrance_exit | give a scene beginning and ending | skit_group GroupItem template enter/exit | ["skit_group_template_source", "skit_group_registry"] | present | medium | true |
| small_position_move | keep the background layer alive without overloading the viewer | GroupItem X/Y/Zoom relative motion | ["group_motion_map"] | present | low | true |
| scale_rotation_emphasis | brief emphasis or surprise | GroupItem Zoom/Rotation or motion recipe | ["motion_recipe_brief", "group_motion_map"] | present | medium | false |
| speech_balloon | show a question or short reaction without changing main narration | ShapeItem/TextItem or overlay route; dedicated proof not yet present | [] | unknown | low | true |
| reaction_mark | visual punctuation such as question or warning mark | ShapeItem/TextItem or overlay PNG route; dedicated asset not present | [] | missing | low | false |
| prop_object_cue | make a situation readable through a simple object | ImageItem/ShapeItem prop proxy | ["background_skit_blueprint_example"] | present | medium | false |
| background_pan_or_simple_camera | create continuity between beats | bg_anim X/Y/Zoom route | ["primitive_visibility_readback"] | present | medium | false |

## Probe Readiness Summary

- minimum_viable_probe: ["head_nod", "expression_swap", "small_position_move", "speech_balloon"]
- enough_for_first_probe: true
- blocking_gap: null
- notes: ["speech_balloon has no dedicated prior proof, but can be probed as ShapeItem/TextItem without external media", "production animation quality remains unaccepted"]

## Not Accepted Scope

- render_proof: false
- ymmp_mutation: false
- production_animation_quality: false
- public_upload_or_public_readiness: false
- real_rss_or_news_integration: false
- external_reference_video_fetch: false
- copied_external_visuals: false
- actual_order_or_audience_acceptance: false

## Boundaries

- YMM4_launched_by_agent: false
- render_performed_by_agent: false
- ymmp_edited_or_committed: false
- audio_tts_generated: false
- cards_regenerated: false
- real_rss_or_news_fetched: false
- external_reference_videos_fetched: false
- production_public_readiness_claimed: false
- actual_audience_acceptance_claimed: false
