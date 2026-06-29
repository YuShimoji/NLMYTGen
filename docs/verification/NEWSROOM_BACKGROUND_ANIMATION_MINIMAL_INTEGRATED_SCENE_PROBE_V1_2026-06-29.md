# Newsroom Background Animation Minimal Integrated Scene Probe v1

artifact_id: newsroom_background_animation_minimal_integrated_scene_probe_v1_2026_06_29
schema_version: newsroom_background_animation_minimal_integrated_scene_probe.v1
production_status: diagnostic_only
render_gate: L0_no_render
scene_probe_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-background-animation-minimal-integrated-scene-preview-operator-instruction-v1


## Source Context

```json
{
  "source_mvp_policy_path": "samples/_probe/newsroom_handoff/background_animation_mvp_policy_v1.json",
  "source_integration_plan_path": "samples/_probe/newsroom_handoff/background_animation_integration_plan_v1.json",
  "source_nod_head_ymmp_path": "samples/nod_head.ymmp",
  "local_probe_path": "_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp",
  "repo_root": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage"
}
```


## Scene Description

```json
{
  "scene_id": "background_animation_minimal_integrated_scene_probe_v1",
  "duration_target_sec": 12.0,
  "explanation_beat": "A structural shift can create short-term friction while moving long-term leverage.",
  "narration_intent": "explain one structural-shift diagnostic point in a review-only beat",
  "viewer_information_goal": "the viewer should understand the caution point while the character accent reduces static-card fatigue",
  "animation_role": "small background accent supporting the explanation",
  "card_overlay_role": "none; existing minimal card or overlay context only",
  "source_boundary_role": "review-only diagnostic line; no real RSS/news source is used"
}
```


## Animation Plan Summary

```json
{
  "stable_start_pose": {
    "segment_id": "stable_start_pose",
    "frame": 0,
    "length": 240,
    "expression": "easy",
    "parent_x_values": [
      -96.0
    ],
    "head_rotation_values": [
      0.0
    ],
    "scene_reason": "let the explanation start from a readable neutral pose"
  },
  "expression_event": {
    "segment_id": "expression_event_key_phrase",
    "frame": 240,
    "length": 180,
    "expression": "panic",
    "parent_x_values": [
      -96.0
    ],
    "head_rotation_values": [
      0.0
    ],
    "scene_reason": "the key phrase introduces short-term friction"
  },
  "nod_or_reaction": {
    "segment_id": "one_short_nod_after_key_phrase",
    "frame": 420,
    "length": 45,
    "expression": "panic",
    "parent_x_values": [
      -96.0
    ],
    "head_rotation_values": [
      0.0,
      -8.0,
      0.0
    ],
    "scene_reason": "one short acknowledgement after the caution point"
  },
  "optional_lateral_emphasis": {
    "status": "omitted_not_needed",
    "reason": "the integrated beat can be represented without lateral movement"
  },
  "stable_end_pose": {
    "segment_id": "stable_end_pose",
    "frame": 465,
    "length": 255,
    "expression": "panic",
    "parent_x_values": [
      -96.0
    ],
    "head_rotation_values": [
      0.0
    ],
    "scene_reason": "end with neutral body/head pose so the accent does not keep acting"
  },
  "disabled_primitives": [
    "repeated_nods",
    "mechanical_expression_cycle",
    "body_forward_back",
    "complex_balloon"
  ]
}
```


## Integration Criteria

```json
{
  "animation_supports_explanation": {
    "target": true,
    "evidence": "expression and nod are tied to the explanation beat rather than isolated primitives"
  },
  "animation_does_not_distract": {
    "target": true,
    "evidence": "body X stays fixed and active motion is limited to one short head nod"
  },
  "no_primitive_collage": {
    "target": true,
    "evidence": "the scene has one explanation beat with stable start, one expression event, one nod, stable end"
  },
  "no_body_forward_back_default": {
    "target": true,
    "evidence": "all parent X routes stay at -96.0 and no Y/depth route is introduced"
  },
  "expression_has_scene_reason": {
    "target": true,
    "evidence": "panic expression marks the short-term friction phrase"
  },
  "nod_has_scene_reason": {
    "target": true,
    "evidence": "single nod acknowledges the explanation after the key phrase"
  },
  "return_to_stable_pose": {
    "target": true,
    "evidence": "final segment returns head rotation to 0.0 and holds X=-96.0"
  }
}
```


## Local Probe Access

```json
{
  "artifact_id": "local_ignored_minimal_integrated_scene_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\background_animation_minimal_integrated_scene_probe_v1.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\background_animation_minimal_integrated_scene_probe_v1.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/background_animation_minimal_integrated_scene_probe_v1.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 224108
}
```


## Local Probe Readback Summary

```json
{
  "status": "structural_pass",
  "timeline_length_frames": 720,
  "timeline_length_sec": 12.0,
  "item_type_counts": {
    "GroupItem": 8,
    "ImageItem": 8
  },
  "segment_count": 4,
  "semantic_status": "pass"
}
```


## Semantic Checks

```json
{
  "status": "pass",
  "checks": {
    "duration_10_to_20_sec": true,
    "one_expression_event": true,
    "one_short_nod_or_reaction": true,
    "no_body_forward_back_default": true,
    "no_primitive_collage": true,
    "expression_has_scene_reason": true,
    "nod_has_scene_reason": true,
    "return_to_stable_pose": true
  },
  "expression_event_segments": [
    "expression_event_key_phrase"
  ],
  "nod_or_reaction_segments": [
    "one_short_nod_after_key_phrase"
  ],
  "parent_x_values": [
    -96.0,
    -96.0,
    -96.0,
    -96.0
  ]
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
  "local_ignored_ymmp_created_in_this_slice": true,
  "ymmp_or_media_staged_or_committed": false,
  "production_public_readiness_claimed": false,
  "actual_order_or_audience_acceptance_claimed": false
}
```


## Boundary Note

The local probe is an ignored diagnostic .ymmp only. It is not rendered, not staged, not committed, and not production/public/audience acceptance.
