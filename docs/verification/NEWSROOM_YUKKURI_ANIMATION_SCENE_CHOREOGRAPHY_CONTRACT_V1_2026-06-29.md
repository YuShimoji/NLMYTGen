# Newsroom Yukkuri Animation Scene Choreography Contract v1

artifact_id: newsroom_yukkuri_animation_scene_choreography_contract_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_scene_choreography_contract.v1
production_status: diagnostic_only
render_gate: L0_no_render
scene_probe_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-yukkuri-animation-scene-choreography-preview-operator-instruction-v1


## Source Context

```json
{
  "source_v4_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
  "source_v4_observation_path": "samples/_probe/newsroom_handoff/yukkuri_animation_v4_tempo_sweep_observation_v1.json",
  "source_tempo_sweep_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_tempo_sweep_contract_v1.json",
  "source_motion_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_motion_contract_v1.json",
  "source_nod_head_ymmp_path": "samples/nod_head.ymmp"
}
```


## Provisional Tempo Policy

```json
{
  "active_reaction_motion": "30-60 frames",
  "nod_reaction": "30-45 frames",
  "small_nudge": "30-60 frames",
  "entrance_or_larger_move": "45-75 frames",
  "expression_change": "instantaneous or near-instantaneous switch with a readable hold",
  "scene_beat_duration": "roughly 3-6 seconds",
  "hold_policy": "most scene time should hold readable poses instead of drifting",
  "status": "provisional_default_until_scene_preview"
}
```


## Choreography Rules

```json
[
  "every motion must have a scene function",
  "do not cycle expressions mechanically",
  "expression changes must be tied to a beat reason",
  "do not repeat nodding unless the scene calls for repeated acknowledgement",
  "do not use body forward/back movement unless it expresses a clear action",
  "prefer short active motion plus readable hold",
  "preserve anchor continuity",
  "avoid floaty drifting",
  "avoid cheap-looking tilt loops by limiting nod count and using neutral return",
  "treat cards and overlays as optional support, not the animation target"
]
```


## Anti Patterns Observed In V4

| anti_pattern_id | observed_in_v4 | replacement_rule |
| --- | --- | --- |
| repeated_nod_playback | True | use one acknowledgement nod only when the beat needs acknowledgement |
| mechanical_expression_cycle | True | bind every expression change to a reason in the scene beat |
| meaningless_forward_back_body_motion | True | use at most one small intentional nudge around the shared anchor |
| floaty_drift | True | limit active motion to 30-60 frames and hold the pose afterward |


## Scene Beat Mapping

| beat_id | scene_function | viewer_information_goal | motion_reason | primitive_used | expression_reason | active_motion_span | hold_span | forbidden_motion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beat_a_neutral_listening_pose | establish_readable_listening_state | show the character is present and listening before the reaction starts | no movement; this beat prevents immediate primitive playback | ["stable_hold"] | calm listening state before the question cue | 0 | 180 | ["nod_loop", "body_forward_back", "expression_cycle"] |
| beat_b_question_reaction_cue | question_reaction_cue | mark that a question or concern has appeared | expression change carries the reaction; body stays anchored | ["expression_swap"] | concerned reaction to the question cue | 0 | 180 | ["extra_nod", "body_forward_back", "expression_cycle"] |
| beat_c_one_short_ack_nod | single_acknowledgement | show a single acknowledgement before explanation continues | one nod acknowledges the question; it is not repeated | ["head_nod"] | return to explanation-ready confidence after the question cue | 45 | 135 | ["second_nod", "body_forward_back", "expression_cycle"] |
| beat_d_reasoned_expression_shift | risk_emphasis_expression | mark the moment where the explanation turns to risk or caution | expression change carries emphasis; no extra body motion is needed | ["expression_swap"] | risk/caution emphasis rather than mechanical sequence | 0 | 180 | ["nod_loop", "body_forward_back", "random_expression_swap"] |
| beat_e_one_small_intentional_nudge | intentional_small_emphasis_move | show one small emphasis move tied to the caution point | small nudge underlines emphasis, then returns to the shared anchor | ["small_position_move"] | same caution expression holds while the body makes one intentional nudge | 60 | 120 | ["body_forward_back", "long_drift", "second_nudge"] |
| beat_f_stable_explanation_pose | return_to_stable_explanation_pose | settle the scene back into a stable explanation pose | no movement; the beat closes the mini-scene cleanly | ["expression_swap", "stable_hold"] | return from caution to explanation-ready tone | 0 | 180 | ["closing_nod_loop", "body_forward_back", "extra_expression_cycle"] |


## V1 Scene Probe Plan

```json
{
  "scene_id": "yukkuri_scene_choreography_probe_v1",
  "duration_frames": 1080,
  "duration_sec_at_60fps": 18.0,
  "beat_count": 6,
  "structure": [
    "Beat A: neutral listening pose",
    "Beat B: question/reaction cue",
    "Beat C: one short nod or acknowledgement",
    "Beat D: expression changes for reason",
    "Beat E: one small intentional nudge",
    "Beat F: return to stable explanation pose"
  ],
  "demonstrates": [
    "one meaningful nod",
    "one reasoned expression change sequence",
    "one small intentional move",
    "stable anchor continuity",
    "no mechanical expression cycling",
    "no meaningless forward/back drift",
    "no production claim"
  ],
  "local_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp"
}
```


## Scene Probe Access

```json
{
  "artifact_id": "local_ignored_scene_choreography_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_scene_choreography_probe_v1.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_scene_choreography_probe_v1.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_scene_choreography_probe_v1.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 370078
}
```


## Scene Probe Readback Summary

```json
{
  "status": "structural_pass",
  "timeline_length_frames": 1080,
  "timeline_length_sec": 18.0,
  "item_type_counts": {
    "GroupItem": 16,
    "ImageItem": 16
  },
  "segment_count": 8,
  "semantic_status": "pass"
}
```


## Next Recommended Axis

```json
{
  "selected": "newsroom-yukkuri-animation-scene-choreography-preview-operator-instruction-v1",
  "reason": "ignored local scene choreography probe exists, is git-ignored, uses one meaningful nod, one small intentional nudge, reasoned expression changes, and stable anchor continuity",
  "prerequisites": [
    "keep scene choreography .ymmp ignored and unstaged",
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
| tempo_only_loop_exited | True |
| no_card_polish_loop | True |
| no_render_export_loop | True |
| choreography_replaces_primitive_collage | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-scene-choreography-preview-operator-instruction-v1 |


## Boundary Note

The scene choreography probe is an ignored local diagnostic artifact. It is not rendered, not staged, not committed, and not production/public acceptance.
