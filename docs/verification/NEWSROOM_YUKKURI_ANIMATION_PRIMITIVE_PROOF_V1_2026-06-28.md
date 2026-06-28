# Newsroom Yukkuri Animation Primitive Proof v1

artifact_id: newsroom_yukkuri_animation_primitive_proof_v1_2026_06_28
schema_version: newsroom_yukkuri_animation_primitive_proof.v1
production_status: diagnostic_only
render_gate: L0_no_render
next_recommended_axis: newsroom-yukkuri-animation-primitive-render-smoke-v1


## Proof Summary

```json
{
  "selected_count": 5,
  "pass_count": 4,
  "partial_count": 1,
  "blocked_count": 0,
  "structurally_provable_count": 4,
  "enough_for_next_render_smoke_axis": true,
  "local_ignored_probe_created": false
}
```


## Primitive Proofs

| primitive_id | intended_scene_function | required_assets | asset_access_state | ymm4_representation_candidate | can_prove_without_render | proof_status | risk | fallback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| head_nod | confirmation_or_agreement_reaction | ["nod_head_probe", "motion_recipe_brief", "motion_recipe_code"] | [{"access_state": "tracked_repo_artifact_exists", "artifact_id": "nod_head_probe", "artifact_kind": "proof", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "motion_recipe_brief", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "motion_recipe_code", "artifact_kind": "tracked", "target_exists": true}] | GroupItem native template with head rotation keyframes | True | pass | medium | static expression_swap if nod route is visually rejected |
| expression_swap | externalize_question_or_confidence_without_dialogue | ["reimu_expression_easy", "reimu_expression_anger", "reimu_expression_panic", "character_body_source", "face_map_extracted", "face_map_bundle_default"] | [{"access_state": "tracked_repo_artifact_exists", "artifact_id": "reimu_expression_easy", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "reimu_expression_anger", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "reimu_expression_panic", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "character_body_source", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "face_map_extracted", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "face_map_bundle_default", "artifact_kind": "tracked", "target_exists": true}] | ImageItem face/expression source switch | True | pass | low | single neutral face if expression palette fails |
| character_entrance_exit | open_or_close_a_background_reenactment_beat | ["skit_group_template_source", "skit_group_registry", "skit_group_placement_code"] | [{"access_state": "tracked_repo_artifact_exists", "artifact_id": "skit_group_template_source", "artifact_kind": "template", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "skit_group_registry", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "skit_group_placement_code", "artifact_kind": "tracked", "target_exists": true}] | GroupItem skit template registry entry | True | pass | medium | static character hold with no entrance motion |
| small_position_move | keep_background_layer_alive_without_decorative_overload | ["group_motion_map", "motion_recipe_code"] | [{"access_state": "tracked_repo_artifact_exists", "artifact_id": "group_motion_map", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "motion_recipe_code", "artifact_kind": "tracked", "target_exists": true}] | ImageItem or GroupItem X/Y/Zoom transform | True | pass | low | static pose plus subtitle-only explanation |
| speech_balloon | show_short_question_or_reaction_as_supportive_overlay | ["scene_composition_schema", "production_ir_spec"] | [{"access_state": "tracked_repo_artifact_exists", "artifact_id": "scene_composition_schema", "artifact_kind": "tracked", "target_exists": true}, {"access_state": "tracked_repo_artifact_exists", "artifact_id": "production_ir_spec", "artifact_kind": "tracked", "target_exists": true}] | ShapeItem/TextItem balloon overlay candidate | True | partial | medium | caption-only reaction note if balloon styling is rejected |


## Asset Access State

| artifact_id | repo_relative_path | folder_full_path_current_host | file_full_path_current_host | target_exists | access_state | access_evidence_level | evidence_source | artifact_kind |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nod_head_probe | samples/nod_head.ymmp | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\nod_head.ymmp | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | proof |
| motion_recipe_brief | samples/recipe_briefs/g26_nod_head_v1_brief.v2.json | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\recipe_briefs | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\recipe_briefs\g26_nod_head_v1_brief.v2.json | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| motion_recipe_code | src/pipeline/motion_recipe.py | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\src\pipeline | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\src\pipeline\motion_recipe.py | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| reimu_expression_easy | samples/characterAnimSample/reimu_easy.png | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample\reimu_easy.png | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| reimu_expression_anger | samples/characterAnimSample/reimu_anger.png | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample\reimu_anger.png | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| reimu_expression_panic | samples/characterAnimSample/reimu_panic.png | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample\reimu_panic.png | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| character_body_source | samples/characterAnimSample/Gemini_Generated_Image_kfezhpkfezhpkfez-removebg-preview.png | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample\Gemini_Generated_Image_kfezhpkfezhpkfez-removebg-preview.png | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| face_map_extracted | samples/characterAnimSample/face_map_extracted.json | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\characterAnimSample\face_map_extracted.json | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| face_map_bundle_default | samples/face_map_bundles/default.json | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\face_map_bundles | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\face_map_bundles\default.json | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| skit_group_template_source | samples/templates/skit_group/delivery_v1_templates.ymmp | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\templates\skit_group | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\templates\skit_group\delivery_v1_templates.ymmp | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | template |
| skit_group_registry | samples/registry_template/skit_group_registry.template.json | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\registry_template | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\registry_template\skit_group_registry.template.json | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| skit_group_placement_code | src/pipeline/skit_group_placement.py | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\src\pipeline | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\src\pipeline\skit_group_placement.py | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| group_motion_map | samples/group_motion_map.example.json | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\samples\group_motion_map.example.json | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| scene_composition_schema | docs/SCENE_COMPOSITION_SCHEMA.md | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\docs | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\docs\SCENE_COMPOSITION_SCHEMA.md | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |
| production_ir_spec | docs/PRODUCTION_IR_SPEC.md | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\docs | C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage\docs\PRODUCTION_IR_SPEC.md | True | tracked_repo_artifact_exists | repo_tracked_current_host | git ls-files + filesystem exists | tracked |


## Structural Evidence

```json
{
  "head_nod": {
    "status": "pass",
    "source": "samples/nod_head.ymmp",
    "group_item_count": 2,
    "image_item_count": 2,
    "rotation_routes": [
      [
        0.0
      ],
      [
        0.0,
        -10.0,
        0.0
      ]
    ],
    "native_template_remark": "nod_head_v1"
  },
  "expression_swap": {
    "status": "pass",
    "tracked_asset_count": 6,
    "required_asset_count": 6,
    "expression_files": [
      "samples/characterAnimSample/reimu_easy.png",
      "samples/characterAnimSample/reimu_anger.png",
      "samples/characterAnimSample/reimu_panic.png"
    ],
    "representation": "face image source switch over a stable body image"
  },
  "character_entrance_exit": {
    "status": "pass",
    "template_names": [
      "delivery_deny_oneshot_v1",
      "delivery_enter_from_left_v1",
      "delivery_exit_left_v1",
      "delivery_nod_v1",
      "delivery_surprise_oneshot_v1"
    ],
    "required_templates": [
      "delivery_enter_from_left_v1",
      "delivery_exit_left_v1"
    ],
    "validation_warnings": [],
    "analysis_warnings": [],
    "has_template_analysis": true
  },
  "small_position_move": {
    "status": "pass",
    "source": "samples/group_motion_map.example.json",
    "required_motion_ids": [
      "approach",
      "nudge_left",
      "nudge_right",
      "retreat"
    ],
    "available_motion_ids": [
      "approach",
      "aside_left",
      "aside_right",
      "center_stage",
      "nudge_down",
      "nudge_left",
      "nudge_right",
      "nudge_up",
      "reset_center",
      "retreat",
      "slide_left",
      "slide_right",
      "zoom_focus",
      "zoom_in_relative",
      "zoom_out_relative"
    ],
    "relative_motion_ids": [
      "approach",
      "nudge_left",
      "nudge_right",
      "retreat"
    ]
  },
  "speech_balloon": {
    "status": "partial",
    "reason": "ShapeItem/TextItem routes are documented, but no dedicated speech balloon template or YMM4 visual pass exists in this slice",
    "scene_composition_schema_exists": true,
    "production_ir_spec_exists": true,
    "dedicated_balloon_template_found": false
  }
}
```


## Business Goal Evaluation

| gate | status | evidence | decision |
| --- | --- | --- | --- |
| problem_clear | pass | primitive proof targets card-only fatigue | keep animation axis |
| offer_clear | pass | proof shows nod, expression, movement, entrance/exit, and partial balloon value | support explainer |
| proof_clear | pass | structural proof is separated from render and production quality | no render claim |
| boundary_clear | pass | diagnostic status and no public/production flags stay explicit | keep L0_no_render |
| next_action_clear | pass | newsroom-yukkuri-animation-primitive-render-smoke-v1 | newsroom-yukkuri-animation-primitive-render-smoke-v1 |
| visual_supports_explanation | pass | scene beats bind primitives to narration roles | avoid decoration-only motion |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| animation_format_artifacts_inspected | True |
| safe_primitive_subset_selected | ["head_nod", "expression_swap", "character_entrance_exit", "small_position_move", "speech_balloon"] |
| primitive_proof_json_doc_created | True |
| scene_beat_probe_json_doc_created | True |
| access_states_recorded | True |
| next_axis_selected | newsroom-yukkuri-animation-primitive-render-smoke-v1 |
| commit_and_push_if_push_gate_passes | ready_for_git_followthrough |


## Access Readiness

| gate | status |
| --- | --- |
| selected_assets_have_access_state | True |
| missing_assets_classified_honestly | True |
| local_ignored_ymmp_is_ignored_or_absent | True |
| no_user_work_emitted_unless_access_verified | True |


## Inertia Check

| gate | status |
| --- | --- |
| no_text_density_loop | True |
| no_card_polish_loop | True |
| no_render_automation_rabbit_hole | True |
| animation_layer_remains_product_axis | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-primitive-render-smoke-v1 |


## Local Ignored Output

```json
{
  "artifact_id": "local_ignored_primitive_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v1.ymmp",
  "target_exists": false,
  "access_state": "ignored_local_artifact_missing",
  "access_evidence_level": "local_ignored",
  "evidence_source": "git ls-files + filesystem exists",
  "git_state": "ignored",
  "artifact_kind": "proof",
  "created_in_this_slice": false,
  "reason": "not created; this slice is a structural proof package and keeps the optional ignored .ymmp target for the next render-smoke gate"
}
```


## Not Accepted Scope

```json
{
  "render_proof": false,
  "ymmp_committed": false,
  "production_animation_quality": false,
  "public_upload_or_public_readiness": false,
  "real_rss_or_news_integration": false,
  "external_reference_video_fetch": false,
  "copied_external_visuals": false,
  "actual_order_or_audience_acceptance": false
}
```


## Boundaries

```json
{
  "YMM4_launched_by_agent": false,
  "render_performed_by_agent": false,
  "source_ymmp_edited_by_hand": false,
  "ymmp_staged_or_committed": false,
  "audio_tts_generated": false,
  "cards_modified": false,
  "real_rss_or_news_fetched": false,
  "external_reference_videos_fetched": false,
  "production_public_readiness_claimed": false,
  "actual_audience_acceptance_claimed": false
}
```


## Boundary Note

This proof does not render, launch YMM4, edit source `.ymmp`, create audio/TTS, fetch real news, fetch external reference videos, modify card assets, or claim production quality.
