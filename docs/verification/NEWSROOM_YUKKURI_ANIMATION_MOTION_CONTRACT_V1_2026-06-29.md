# Newsroom Yukkuri Animation Motion Contract v1

artifact_id: newsroom_yukkuri_animation_motion_contract_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_motion_contract.v1
production_status: diagnostic_only
render_gate: L0_no_render
v2_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-yukkuri-animation-primitive-v2-preview-operator-instruction-v1


## Source Context

```json
{
  "source_primitive_proof_path": "samples/_probe/newsroom_handoff/yukkuri_animation_primitive_proof_v1.json",
  "source_v1_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
  "source_v1_observation_path": "samples/_probe/newsroom_handoff/yukkuri_animation_primitive_preview_observation_v1.json",
  "source_nod_head_ymmp_path": "samples/nod_head.ymmp"
}
```


## Motion Contract

| primitive_id | current_status | observed_issue | intended_motion | start_anchor_policy | end_anchor_policy | facing_policy | duration_policy | easing_policy | continuity_policy | expression_span_policy | fallback_if_not_supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| head_nod | pass_with_timing_warning | visible but too slow; read as one vertical nod | short acknowledgement nod that returns to neutral | head rotation starts at 0 degrees | head rotation ends at 0 degrees | no facing change; keep body orientation neutral | one nod must fit inside a 6 second beat with key motion concentrated near the beat middle | linear route is acceptable for v2; avoid long hold at the tilted state | head neutral at beat boundaries so adjacent primitives do not inherit a tilt | expression remains stable during the nod beat | hold neutral head and rely on expression_swap for reaction |
| expression_swap | pass | expressions switched, but random-feeling timing would weaken the animation layer | beat-aligned expression state change | expression starts at the beat file path | expression remains stable until the next beat boundary | no facing change from expression alone | one expression per 6 second beat in v2 | instant image source swap is acceptable for this structural probe | do not change expression mid-beat unless a later visual pass asks for it | panic/easy/anger/panic/easy map to the five v2 beats | use easy expression for all beats |
| character_entrance_exit | pass_with_facing_warning | broad X travel looked like backward movement toward screen center | bounded side entry/exit cue without implying a wrong facing direction | entry starts near the left-side staging anchor, not far offscreen | entry ends at the shared review anchor; exit starts from that same anchor | avoid flip/orientation claims in v2; use neutral lateral travel only | entry/exit cue each fits within one 6 second beat | linear route is acceptable; avoid slow center drift | adjacent beat start/end X values must match the shared anchor unless a cut is explicit | entry uses panic; exit uses easy | static character hold at the shared review anchor |
| small_position_move | pass_with_anchor_continuity_warning | segment-to-segment X discontinuity caused jumpy disconnected movement | small nudge around a stable review anchor | start every nudge at the previous beat end anchor | return every nudge to the same shared anchor | no facing change; movement must not read as walking backward | small nudge fits within a 6 second beat | linear out-and-back route is acceptable for v2 | remove sudden jumps by making each adjacent beat boundary share X=-96 | expression remains stable while the nudge happens | drop the nudge and keep the shared review anchor |


## V1 Issue Summary

```json
[
  "motion too slow",
  "head nod too slow and perceived as a single vertical nod",
  "broad X travel looked like backward movement toward screen center",
  "facing/orientation intent was underspecified",
  "X anchor changed between adjacent segments and created jumps",
  "expression changes passed but need beat-aligned spans"
]
```


## V2 Correction Plan

```json
{
  "head_nod": [
    "shorten beat length from 12 seconds to 6 seconds",
    "use 0 -> negative rotation -> 0 so the head returns to neutral"
  ],
  "facing_orientation": [
    "do not claim or perform facing flip in v2",
    "replace broad centerward travel with bounded neutral lateral movement"
  ],
  "anchor_continuity": [
    "use X=-96 as the shared review anchor",
    "every adjacent beat boundary carries that anchor unless the exit beat intentionally leaves it"
  ],
  "expression_timing": [
    "one expression state per beat",
    "panic/easy/anger/panic/easy sequence follows scene role instead of random switching"
  ],
  "render_boundary": "no render/export proof in this slice"
}
```


## V2 Beat Plan

| beat_id | timing_range | scene_function | primitive_ids | parent_x_values | head_rotation_values |
| --- | --- | --- | --- | --- | --- |
| v2_beat_01_enter_question | 0-6 sec | viewer_question_reaction | ["character_entrance_exit", "expression_swap"] | [-144.0, -96.0] | [0.0] |
| v2_beat_02_nod_response | 6-12 sec | explanation_response | ["head_nod", "small_position_move"] | [-96.0, -84.0, -96.0] | [0.0, -10.0, 0.0] |
| v2_beat_03_emphasis_nudge | 12-18 sec | proof_emphasis | ["expression_swap", "small_position_move"] | [-96.0, -116.0, -96.0] | [0.0] |
| v2_beat_04_boundary_warning | 18-24 sec | boundary_warning | ["expression_swap", "small_position_move"] | [-96.0, -86.0, -96.0] | [0.0] |
| v2_beat_05_exit_close | 24-30 sec | next_action_close | ["character_entrance_exit", "head_nod"] | [-96.0, -144.0] | [0.0, -8.0, 0.0] |


## V2 Local Probe

```json
{
  "artifact_id": "local_ignored_v2_motion_fix_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp",
  "folder_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v2_motion_fix.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\PLANNER007\\NLMYTGen\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v2_motion_fix.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 260692
}
```


## V2 Probe Readback

```json
{
  "readback_status": "structural_pass",
  "target_exists": true,
  "file_sha256": "b92335826ab07d5cc4d3f29ace66861a9b3beb3771d7bc2b73f791eb8b8153ac",
  "file_size_bytes": 260692,
  "timeline": {
    "fps": 60,
    "length_frames": 1800,
    "length_sec": 30.0,
    "item_count": 20,
    "item_type_counts": {
      "GroupItem": 10,
      "ImageItem": 10
    },
    "unexpected_item_types": []
  },
  "beat_readback": [
    {
      "beat_id": "v2_beat_01_enter_question",
      "scene_function": "viewer_question_reaction",
      "timing_range": "0-6 sec",
      "frame": 0,
      "length": 360,
      "primitive_ids": [
        "character_entrance_exit",
        "expression_swap"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -144.0,
        -96.0
      ],
      "head_rotation_values": [
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_panic.png",
      "status": "pass"
    },
    {
      "beat_id": "v2_beat_02_nod_response",
      "scene_function": "explanation_response",
      "timing_range": "6-12 sec",
      "frame": 360,
      "length": 360,
      "primitive_ids": [
        "head_nod",
        "small_position_move"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -96.0,
        -84.0,
        -96.0
      ],
      "head_rotation_values": [
        0.0,
        -10.0,
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_easy.png",
      "status": "pass"
    },
    {
      "beat_id": "v2_beat_03_emphasis_nudge",
      "scene_function": "proof_emphasis",
      "timing_range": "12-18 sec",
      "frame": 720,
      "length": 360,
      "primitive_ids": [
        "expression_swap",
        "small_position_move"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -96.0,
        -116.0,
        -96.0
      ],
      "head_rotation_values": [
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_anger.png",
      "status": "pass"
    },
    {
      "beat_id": "v2_beat_04_boundary_warning",
      "scene_function": "boundary_warning",
      "timing_range": "18-24 sec",
      "frame": 1080,
      "length": 360,
      "primitive_ids": [
        "expression_swap",
        "small_position_move"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -96.0,
        -86.0,
        -96.0
      ],
      "head_rotation_values": [
        0.0
      ],
      "face_file_path": "C:\\Users\\PLANNER007\\NLMYTGen\\samples\\characterAnimSample\\reimu_panic.png",
      "status": "pass"
    },
    {
      "beat_id": "v2_beat_05_exit_close",
      "scene_function": "next_action_close",
      "timing_range": "24-30 sec",
      "frame": 1440,
      "length": 360,
      "primitive_ids": [
        "character_entrance_exit",
        "head_nod"
      ],
      "item_count": 4,
      "group_item_count": 2,
      "image_item_count": 2,
      "parent_x_values": [
        -96.0,
        -144.0
      ],
      "head_rotation_values": [
        0.0,
        -8.0,
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
      "evidence": "head Rotation route has 0 -> non-zero -> 0 within a 6 second beat"
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
      "evidence": "entry/exit uses bounded side travel instead of broad center drift"
    },
    {
      "primitive_id": "small_position_move",
      "status": "pass",
      "evidence": "adjacent beats share X=-96 and nudges return to that anchor"
    }
  ],
  "anchor_continuity": {
    "shared_anchor_x": -96.0,
    "beat_boundary_start_x_values": [
      -144.0,
      -96.0,
      -96.0,
      -96.0,
      -96.0
    ],
    "adjacent_boundaries_share_anchor": true
  },
  "source_ymmp_copy_basis": "samples/nod_head.ymmp",
  "local_probe_access_state": "verified_present",
  "YMM4_launch_status": "not_launched",
  "render_status": "not_rendered",
  "audio_tts_status": "not_created"
}
```


## Next Recommended Axis

```json
{
  "selected": "newsroom-yukkuri-animation-primitive-v2-preview-operator-instruction-v1",
  "reason": "ignored local v2 probe exists, is git-ignored, and structurally implements the motion timing/facing/anchor-continuity contract",
  "prerequisites": [
    "keep v2 .ymmp ignored and unstaged",
    "use a preview-only operator instruction before any render request",
    "do not claim production/public acceptance"
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


## Inertia Check

| gate | status |
| --- | --- |
| no_text_density_loop | True |
| no_card_polish_loop | True |
| no_render_export_loop | True |
| motion_contract_targets_reported_visual_issue | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-primitive-v2-preview-operator-instruction-v1 |


## Boundary Note

The v2 probe is an ignored local diagnostic artifact. It is not rendered, not staged, not committed, and not production/public acceptance.
