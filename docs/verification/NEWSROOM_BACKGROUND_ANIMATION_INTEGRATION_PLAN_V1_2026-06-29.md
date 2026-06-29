# Newsroom Background Animation Integration Plan v1

artifact_id: newsroom_background_animation_integration_plan_v1_2026_06_29
schema_version: newsroom_background_animation_integration_plan.v1
production_status: diagnostic_only
render_gate: L0_no_render
selected_next_axis: newsroom-background-animation-minimal-integrated-scene-probe-v1


## Source Context

```json
{
  "source_scene_preview_observation_path": "samples/_probe/newsroom_handoff/yukkuri_animation_scene_preview_observation_v1.json",
  "source_mvp_policy_path": "samples/_probe/newsroom_handoff/background_animation_mvp_policy_v1.json",
  "source_scene_choreography_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_scene_choreography_contract_v1.json",
  "repo_root": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage"
}
```


## Integrated Scene Probe Spec

```json
{
  "probe_id": "newsroom-background-animation-minimal-integrated-scene-probe-v1",
  "duration_sec_range": {
    "min": 10,
    "max": 20
  },
  "content_rule": "one actual explanation beat, not a primitive demo",
  "review_only_line": "A structural shift can create short-term friction while moving long-term leverage.",
  "line_status": "review_only_diagnostic_line",
  "animation_budget": {
    "stable_pose": "required",
    "expression_event_count": 1,
    "nod_or_reaction_count": 1,
    "body_forward_back_movement": "disabled_by_default",
    "small_lateral_emphasis": "optional_only_if_scene_justified",
    "speech_balloon": "deferred"
  },
  "card_overlay_policy": "minimal existing card or overlay only; no card asset redesign",
  "source_material_policy": "use a small existing diagnostic line or this review-only line",
  "output_policy": {
    "planning_slice_creates_ymmp": false,
    "later_slice_may_create_local_ignored_ymmp": "only if safe and necessary",
    "tracked_ymmp_allowed": false,
    "render_export_required": false
  },
  "preview_policy": {
    "user_review_mode": "one_freeform_preview_only",
    "do_not_request_repeated_render": true,
    "evaluation_focus": [
      "supports explanation",
      "does not distract",
      "reduces card fatigue",
      "introduces no confusion"
    ]
  }
}
```


## Success Signal

```json
{
  "status": "pending_user_freeform_preview",
  "required_readback": "animation supports explanation, does not distract, reduces card fatigue, and introduces no confusion"
}
```


## Failure Signal

```json
{
  "status": "defined",
  "if_user_reports_bad_integrated_feel": "freeze_animation_as_minimal_accent",
  "return_axis": "newsroom-rss-dry-run-integration-plan-v1"
}
```


## Not Accepted Scope

```json
{
  "render_proof": false,
  "render_export_required_now": false,
  "production_animation_quality": false,
  "public_upload_or_public_readiness": false,
  "real_rss_or_news_integration": false,
  "card_redesign_or_density_work": false,
  "dense_script_rewrite": false,
  "external_reference_video_fetch": false,
  "audio_or_tts_output": false,
  "actual_order_or_audience_acceptance": false,
  "speech_balloon_visual_acceptance": false
}
```


## Boundaries

```json
{
  "YMM4_launched_by_agent": false,
  "render_performed_by_agent": false,
  "audio_tts_generated": false,
  "real_media_imported": false,
  "external_fetch_performed": false,
  "card_assets_modified": false,
  "dense_script_modified": false,
  "local_ignored_ymmp_created_in_this_slice": false,
  "ymmp_or_media_staged_or_committed": false,
  "production_public_readiness_claimed": false
}
```


## Inertia Check

| gate | status |
| --- | --- |
| remote_parity_required_before_work | True |
| no_new_primitive_only_probe | True |
| no_repeated_visual_proof_request | True |
| integrated_scene_before_more_tuning | True |
| return_to_rss_story_integration_if_bad | newsroom-rss-dry-run-integration-plan-v1 |


## Boundary Note

This is a planning artifact for a later minimal integrated scene probe. It does not create a .ymmp file in this slice and does not request a render/export pass.
