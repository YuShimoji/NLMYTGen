# Newsroom Yukkuri Animation Tempo Contract v1

artifact_id: newsroom_yukkuri_animation_tempo_contract_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_tempo_contract.v1
production_status: diagnostic_only
render_gate: L0_no_render
v3_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1


## Source Context

```json
{
  "source_v2_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp",
  "source_v2_observation_path": "samples/_probe/newsroom_handoff/yukkuri_animation_v2_preview_observation_v1.json",
  "source_motion_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_motion_contract_v1.json",
  "source_nod_head_ymmp_path": "samples/nod_head.ymmp"
}
```


## Tempo Contract

| primitive_id | v2_status | observed_issue | intended_tempo | current_duration_or_frame_span_if_available | proposed_duration_or_frame_span | speed_change_ratio_if_available | easing_policy | continuity_policy | natural_pause_policy | fallback_if_not_supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| head_nod | pass_with_tempo_warning | visible and connected, but still too slow | short reaction nod that reads within a compact 3 second beat | 360 frames / 6 seconds | 180 frames / 3 seconds | 0.5x duration / 2.0x tempo | keep linear route for structural probe; concentrate the tilt near the middle keyframe | preserve 0 -> negative -> 0 rotation so no tilt leaks across beat boundaries | no long pause at the tilted state; neutral can hold at the end of the beat | use v2 nod timing but mark tempo unresolved |
| expression_swap | pass | no regression; must remain readable after tempo increase | one readable expression state per 3 second beat | 360 frames / 6 seconds per expression beat | 180 frames / 3 seconds per expression beat | 0.5x duration / 2.0x tempo | instant image swap remains acceptable; no mid-beat flicker | expression changes only at beat boundaries | hold expression for the full 3 second beat | keep v2 expression beat length and continue tempo work on motion only |
| character_entrance_exit | pass_with_tempo_warning | connected movement still feels slow | intentional bounded cue rather than slow drift | 360 frames / 6 seconds | 180 frames / 3 seconds | 0.5x duration / 2.0x tempo | linear route is acceptable; avoid slow centerward drift | preserve v2 shared anchor X=-96 at adjacent beat boundaries | entry/exit ends on a stable anchor instead of continuing to drift | hold at X=-96 with no entrance/exit travel |
| small_position_move | pass_with_tempo_warning | anchor continuity improved but small movement remains slow | quick bounded nudge that returns to the shared anchor | 360 frames / 6 seconds | 180 frames / 3 seconds | 0.5x duration / 2.0x tempo | linear out-and-back is acceptable for this tempo pass | start and end every nudge at X=-96 | no lingering drift after the nudge returns to anchor | drop the nudge and keep the shared anchor |


## V2 Issue Summary

```json
[
  "anchor continuity improved",
  "segment connection passed",
  "X jump regression was not reported",
  "motion remains very slow",
  "render/export is still not required for this stage"
]
```


## V3 Correction Plan

```json
{
  "tempo": [
    "halve each v2 beat from 360 frames / 6 seconds to 180 frames / 3 seconds",
    "keep the five-beat structure but shorten the total probe from 30 seconds to 15 seconds"
  ],
  "anchor_continuity": [
    "preserve X=-96 shared anchor at adjacent beat boundaries",
    "do not reintroduce v1 X jumps"
  ],
  "head_nod": [
    "preserve 0 -> negative rotation -> 0 neutral return",
    "make the nod read inside a short reaction beat"
  ],
  "expression_timing": [
    "keep one expression per 3 second beat",
    "do not flicker mid-beat"
  ],
  "render_boundary": "no render/export proof in this slice"
}
```


## V3 Beat Plan

| beat_id | timing_range | scene_function | primitive_ids | parent_x_values | head_rotation_values |
| --- | --- | --- | --- | --- | --- |
| v3_beat_01_enter_question | 0-3 sec | viewer_question_reaction | ["character_entrance_exit", "expression_swap"] | [-144.0, -96.0] | [0.0] |
| v3_beat_02_nod_response | 3-6 sec | explanation_response | ["head_nod", "small_position_move"] | [-96.0, -84.0, -96.0] | [0.0, -10.0, 0.0] |
| v3_beat_03_emphasis_nudge | 6-9 sec | proof_emphasis | ["expression_swap", "small_position_move"] | [-96.0, -116.0, -96.0] | [0.0] |
| v3_beat_04_boundary_warning | 9-12 sec | boundary_warning | ["expression_swap", "small_position_move"] | [-96.0, -86.0, -96.0] | [0.0] |
| v3_beat_05_exit_close | 12-15 sec | next_action_close | ["character_entrance_exit", "head_nod"] | [-96.0, -144.0] | [0.0, -8.0, 0.0] |


## V3 Local Probe

```json
{
  "artifact_id": "local_ignored_v3_tempo_fix_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp",
  "folder_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 261241
}
```


## V3 Probe Readback

```json
{
  "readback_status": "structural_pass",
  "target_exists": true,
  "file_sha256": "a1daddfa7563482d8f380ccf1a3af20f5aed6e504c9e576b3556502f22fb8ffb",
  "file_size_bytes": 261241,
  "timeline": {
    "fps": 60,
    "length_frames": 900,
    "length_sec": 15.0,
    "item_count": 20,
    "item_type_counts": {
      "GroupItem": 10,
      "ImageItem": 10
    },
    "unexpected_item_types": []
  },
  "beat_readback": [
    {
      "beat_id": "v3_beat_01_enter_question",
      "scene_function": "viewer_question_reaction",
      "timing_range": "0-3 sec",
      "frame": 0,
      "length": 180,
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
      "face_file_path": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_panic.png",
      "status": "pass"
    },
    {
      "beat_id": "v3_beat_02_nod_response",
      "scene_function": "explanation_response",
      "timing_range": "3-6 sec",
      "frame": 180,
      "length": 180,
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
      "face_file_path": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_easy.png",
      "status": "pass"
    },
    {
      "beat_id": "v3_beat_03_emphasis_nudge",
      "scene_function": "proof_emphasis",
      "timing_range": "6-9 sec",
      "frame": 360,
      "length": 180,
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
      "face_file_path": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_anger.png",
      "status": "pass"
    },
    {
      "beat_id": "v3_beat_04_boundary_warning",
      "scene_function": "boundary_warning",
      "timing_range": "9-12 sec",
      "frame": 540,
      "length": 180,
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
      "face_file_path": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_panic.png",
      "status": "pass"
    },
    {
      "beat_id": "v3_beat_05_exit_close",
      "scene_function": "next_action_close",
      "timing_range": "12-15 sec",
      "frame": 720,
      "length": 180,
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
      "face_file_path": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_easy.png",
      "status": "pass"
    }
  ],
  "primitive_status": [
    {
      "primitive_id": "head_nod",
      "status": "pass",
      "evidence": "head nod keeps 0 -> non-zero -> 0 and beat length is 180 frames"
    },
    {
      "primitive_id": "expression_swap",
      "status": "pass",
      "evidence": [
        "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_anger.png",
        "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_easy.png",
        "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\samples\\characterAnimSample\\reimu_panic.png"
      ]
    },
    {
      "primitive_id": "character_entrance_exit",
      "status": "pass",
      "evidence": "bounded entry/exit travel is preserved at 180 frames per beat"
    },
    {
      "primitive_id": "small_position_move",
      "status": "pass",
      "evidence": "nudges still return to X=-96 and run in 180-frame beats"
    }
  ],
  "tempo_change": {
    "v2_beat_length_frames": 360,
    "v3_beat_length_frames": 180,
    "duration_ratio": 0.5,
    "tempo_multiplier": 2.0
  },
  "anchor_continuity": {
    "shared_anchor_x": -96.0,
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
  "selected": "newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1",
  "reason": "ignored local v3 probe exists, is git-ignored, preserves v2 anchor continuity, and halves beat duration from 6 seconds to 3 seconds",
  "prerequisites": [
    "keep v3 .ymmp ignored and unstaged",
    "use preview-only operator observation before any render request",
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
| tempo_contract_targets_reported_visual_issue | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1 |


## Boundary Note

The v3 probe is an ignored local diagnostic artifact. It is not rendered, not staged, not committed, and not production/public acceptance.
