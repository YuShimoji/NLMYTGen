# Newsroom Yukkuri Animation Scene Choreography Contract v1

artifact_id: newsroom_yukkuri_animation_scene_choreography_contract_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_scene_choreography_contract.v1
production_status: diagnostic_only
render_gate: L0_no_render
scene_probe_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-yukkuri-animation-scene-beat-integration-v1


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


## Tempo Default Policy

```json
{
  "policy_id": "newsroom_yukkuri_animation_v4_tempo_default_policy_v1_2026_06_29",
  "status": "active_for_scene_beat_integration",
  "scene_dependency": true,
  "default_tempo_band": "0.75s",
  "default_frame_span_at_60fps": 45,
  "default_use_case": "default light reenactment beat",
  "use_case_policy": [
    {
      "use_case": "default light reenactment beat",
      "tempo": "0.75s",
      "frames_at_60fps": 45,
      "note": "user-selected most natural"
    },
    {
      "use_case": "quick reaction / punch / short emphasis",
      "tempo": "0.5s",
      "frames_at_60fps": 30,
      "note": "acceptable but use selectively"
    },
    {
      "use_case": "explanatory / readable / calmer beat",
      "tempo": "1.0s",
      "frames_at_60fps": 60,
      "note": "acceptable, useful when readability matters"
    },
    {
      "use_case": "slow upper comparison",
      "tempo": "1.5s",
      "frames_at_60fps": 90,
      "note": "not default; contrast or special slow scene only"
    }
  ],
  "next_axis": "newsroom-yukkuri-animation-scene-beat-integration-v1",
  "source_user_observation": [
    "0.75s looks the most natural.",
    "However, the best duration depends on the scene.",
    "1.0s is also within acceptable range.",
    "0.5s is also within acceptable range.",
    "No production/public/render approval was given."
  ]
}
```


## Provisional Tempo Policy

```json
{
  "default_reaction_motion": "45 frames / 0.75s",
  "quick_reaction_or_punch": "30 frames / 0.5s",
  "readability_heavy_or_calm_explanation": "60 frames / 1.0s",
  "slow_upper_comparison": "90 frames / 1.5s",
  "scene_dependency": true,
  "status": "superseded_by_tempo_default_policy"
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
  "use 0.75s / 45 frames as the default light reenactment beat",
  "use 0.5s / 30 frames only for quick reaction, punch, or short emphasis",
  "use 1.0s / 60 frames for slower explanatory or readability-heavy moments",
  "keep 1.5s / 90 frames as a slow comparison or special-case upper bound",
  "prefer short active motion plus readable hold",
  "preserve anchor continuity",
  "avoid floaty drifting",
  "avoid cheap-looking tilt loops by limiting nod count and using neutral return",
  "treat cards and overlays as optional support, not the animation target"
]
```


## Scene Beat Integration Risks

| risk_id | status | mitigation |
| --- | --- | --- |
| primitive_only_tempo_loop | exited | use the tempo policy inside an actual scene/beat structure |
| scene_dependent_timing | active | select 0.5s, 0.75s, or 1.0s by beat function instead of forcing one global value |
| slow_upper_bound_overuse | guarded | do not use 1.5s as default; reserve it for contrast or a specific slow scene |


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
    "0.75s default active timing in a scene-beat structure",
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
  "selected": "newsroom-yukkuri-animation-scene-beat-integration-v1",
  "reason": "the v4 sweep selected 0.75s / 45 frames as the default tempo; the next proof should apply 0.5s, 0.75s, and 1.0s by scene-beat function instead of running another primitive-only tempo sweep",
  "prerequisites": [
    "keep scene choreography .ymmp ignored and unstaged",
    "use scene-beat integration before any render request",
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
| default_tempo_policy_selected | 0.75s / 45 frames |
| scene_dependent_variants_preserved | 0.5s and 1.0s |
| scene_beat_integration_replaces_primitive_loop | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-scene-beat-integration-v1 |


## Boundary Note

The scene choreography probe is an ignored local diagnostic artifact. It is not rendered, not staged, not committed, and not production/public acceptance.
