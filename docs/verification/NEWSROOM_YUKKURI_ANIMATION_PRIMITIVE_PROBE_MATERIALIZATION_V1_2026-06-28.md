# Newsroom Yukkuri Animation Primitive Probe Materialization v1

artifact_id: newsroom_yukkuri_animation_primitive_probe_materialization_v1_2026_06_28
schema_version: newsroom_yukkuri_animation_primitive_probe_materialization.v1
production_status: diagnostic_only
materialization_status: materialized_ignored_local_probe
render_gate: L0_no_render
next_recommended_axis: newsroom-yukkuri-animation-primitive-render-smoke-v1


## Source Context

```json
{
  "source_primitive_proof_path": "samples/_probe/newsroom_handoff/yukkuri_animation_primitive_proof_v1.json",
  "source_primitive_proof_id": "newsroom_yukkuri_animation_primitive_proof_v1_2026_06_28",
  "source_primitive_proof_doc_path": "docs/verification/NEWSROOM_YUKKURI_ANIMATION_PRIMITIVE_PROOF_V1_2026-06-28.md",
  "source_scene_beat_probe_path": "samples/_probe/newsroom_handoff/yukkuri_animation_scene_beat_probe_v1.json",
  "source_scene_beat_probe_id": "newsroom_yukkuri_animation_scene_beat_probe_v1_2026_06_28",
  "source_scene_beat_probe_doc_path": "docs/verification/NEWSROOM_YUKKURI_ANIMATION_SCENE_BEAT_PROBE_V1_2026-06-28.md",
  "source_nod_head_ymmp_path": "samples/nod_head.ymmp",
  "source_context_role": "verified_repo_filesystem_not_agent_report_claim"
}
```


## Local Probe

```json
{
  "artifact_id": "local_ignored_primitive_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v1.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v1.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present_ignored_local_artifact",
  "access_evidence_level": "current_host_filesystem_plus_git_ignore",
  "evidence_source": "Path.exists + git check-ignore -v",
  "git_state": "ignored",
  "git_check_ignore": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
    "stderr": "",
    "ignored": true
  }
}
```


## Probe Plan

| beat_id | timing_range | scene_function | primitive_ids | expression | motion_label |
| --- | --- | --- | --- | --- | --- |
| probe_beat_01_enter_question | 0-12 sec | viewer_question_reaction | ["character_entrance_exit", "expression_swap"] | panic | enter_from_left |
| probe_beat_02_nod_response | 12-24 sec | explanation_response | ["head_nod", "small_position_move"] | easy | small_nudge_right |
| probe_beat_03_emphasis_nudge | 24-36 sec | proof_emphasis | ["expression_swap", "small_position_move"] | anger | small_nudge_left |
| probe_beat_04_boundary_warning | 36-48 sec | boundary_warning | ["expression_swap", "small_position_move"] | panic | small_nudge_center |
| probe_beat_05_exit_close | 48-60 sec | next_action_close | ["character_entrance_exit", "head_nod"] | easy | exit_left |


## Probe YMM4 Readback

```json
{
  "readback_status": "structural_pass",
  "target_exists": true,
  "file_sha256": "182c2bf0d3de4f2c634c3840915697c7281c0ed0c211722620af3a2fc7e75fc7",
  "file_size_bytes": 260880,
  "timeline": {
    "fps": 60,
    "length_frames": 3600,
    "length_sec": 60.0,
    "item_count": 20,
    "item_type_counts": {
      "GroupItem": 10,
      "ImageItem": 10
    },
    "unexpected_item_types": []
  },
  "beat_readback": [
    {
      "beat_id": "probe_beat_01_enter_question",
      "scene_function": "viewer_question_reaction",
      "timing_range": "0-12 sec",
      "frame": 0,
      "length": 720,
      "primitive_ids": [
        "character_entrance_exit",
        "expression_swap"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -520.0,
        -120.0,
        -80.0
      ],
      "head_rotation_values": [
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_panic.png",
      "status": "pass"
    },
    {
      "beat_id": "probe_beat_02_nod_response",
      "scene_function": "explanation_response",
      "timing_range": "12-24 sec",
      "frame": 720,
      "length": 720,
      "primitive_ids": [
        "head_nod",
        "small_position_move"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -80.0,
        -48.0,
        -80.0
      ],
      "head_rotation_values": [
        0.0,
        -8.0,
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_easy.png",
      "status": "pass"
    },
    {
      "beat_id": "probe_beat_03_emphasis_nudge",
      "scene_function": "proof_emphasis",
      "timing_range": "24-36 sec",
      "frame": 1440,
      "length": 720,
      "primitive_ids": [
        "expression_swap",
        "small_position_move"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -80.0,
        -116.0,
        -80.0
      ],
      "head_rotation_values": [
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_anger.png",
      "status": "pass"
    },
    {
      "beat_id": "probe_beat_04_boundary_warning",
      "scene_function": "boundary_warning",
      "timing_range": "36-48 sec",
      "frame": 2160,
      "length": 720,
      "primitive_ids": [
        "expression_swap",
        "small_position_move"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -80.0,
        -60.0,
        -80.0
      ],
      "head_rotation_values": [
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_panic.png",
      "status": "pass"
    },
    {
      "beat_id": "probe_beat_05_exit_close",
      "scene_function": "next_action_close",
      "timing_range": "48-60 sec",
      "frame": 2880,
      "length": 720,
      "primitive_ids": [
        "character_entrance_exit",
        "head_nod"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -80.0,
        -120.0,
        -520.0
      ],
      "head_rotation_values": [
        0.0,
        -6.0,
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_easy.png",
      "status": "pass"
    }
  ],
  "primitive_status": [
    {
      "primitive_id": "head_nod",
      "status": "pass",
      "evidence": "head GroupItem Rotation route contains non-zero keyframes"
    },
    {
      "primitive_id": "expression_swap",
      "status": "pass",
      "evidence": [
        "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_anger.png",
        "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_easy.png",
        "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_panic.png"
      ]
    },
    {
      "primitive_id": "character_entrance_exit",
      "status": "pass",
      "evidence": "parent GroupItem X route moves between off-screen and review position"
    },
    {
      "primitive_id": "small_position_move",
      "status": "pass",
      "evidence": "parent GroupItem X route uses small bounded nudges"
    },
    {
      "primitive_id": "speech_balloon",
      "status": "omitted_partial",
      "evidence": "omitted from the local .ymmp because the previous proof classified it as partial: ShapeItem/TextItem routes exist, but no dedicated balloon template or visual pass exists yet"
    }
  ],
  "source_ymmp_copy_basis": "samples/nod_head.ymmp",
  "local_probe_access_state": "verified_present_ignored_local_artifact",
  "YMM4_launch_status": "not_launched",
  "render_status": "not_rendered",
  "audio_tts_status": "not_created"
}
```


## Primitive Coverage

```json
{
  "covered_primitives": [
    "head_nod",
    "expression_swap",
    "character_entrance_exit",
    "small_position_move"
  ],
  "omitted_primitives": [
    "speech_balloon"
  ],
  "coverage": {
    "head_nod": [
      "probe_beat_02_nod_response",
      "probe_beat_05_exit_close"
    ],
    "expression_swap": [
      "probe_beat_01_enter_question",
      "probe_beat_03_emphasis_nudge",
      "probe_beat_04_boundary_warning"
    ],
    "character_entrance_exit": [
      "probe_beat_01_enter_question",
      "probe_beat_05_exit_close"
    ],
    "small_position_move": [
      "probe_beat_02_nod_response",
      "probe_beat_03_emphasis_nudge",
      "probe_beat_04_boundary_warning"
    ],
    "speech_balloon": []
  },
  "all_proven_primitives_covered": true,
  "speech_balloon_intentionally_omitted": true
}
```


## Access Readiness

| gate | status |
| --- | --- |
| target_path_emitted | True |
| folder_path_emitted | True |
| target_exists_stated | True |
| access_state_verified_present | True |
| access_evidence_level_stated | True |
| git_ignore_verified | True |


## Completion Matrix

| gate | status |
| --- | --- |
| repo_state_verified | True |
| primitive_proof_inspected | True |
| probe_subset_selected | ["head_nod", "expression_swap", "character_entrance_exit", "small_position_move"] |
| local_ignored_probe_created_or_blocked_recorded | True |
| access_state_recorded | True |
| readback_json_doc_created | True |
| next_axis_selected | newsroom-yukkuri-animation-primitive-render-smoke-v1 |
| commit_and_push_if_push_gate_passes | ready_for_git_followthrough |


## Expected Next User Action If Verified

```json
{
  "this_slice_user_action_required": false,
  "future_render_smoke_action": "use the verified ignored local probe as the target for a later operator-instructed YMM4 open/render-smoke slice",
  "open_command_recorded_not_requested": "Invoke-Item -LiteralPath \"C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v1.ymmp\""
}
```


## Next Recommended Axis

```json
{
  "selected": "newsroom-yukkuri-animation-primitive-render-smoke-v1",
  "reason": "local ignored .ymmp exists and structural readback covers the four proven primitives",
  "prerequisites": [
    "keep the local .ymmp ignored and unstaged",
    "create an operator instruction sheet before any render smoke",
    "keep production/public acceptance false"
  ]
}
```


## Not Accepted Scope

```json
{
  "render_proof": false,
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
  "source_ymmp_modified": false,
  "local_ignored_probe_created": true,
  "ymmp_or_media_staged_or_committed": false,
  "production_public_readiness_claimed": false
}
```


## Inertia Check

| gate | status |
| --- | --- |
| no_text_density_loop | True |
| no_card_polish_loop | True |
| no_render_automation_rabbit_hole | True |
| no_user_work_before_verified_target | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-primitive-render-smoke-v1 |


## Boundary Note

The local `.ymmp` is an ignored diagnostic probe only. It is not rendered, not staged, not committed, and not production/public acceptance. The speech balloon primitive remains omitted because it is still partial.
