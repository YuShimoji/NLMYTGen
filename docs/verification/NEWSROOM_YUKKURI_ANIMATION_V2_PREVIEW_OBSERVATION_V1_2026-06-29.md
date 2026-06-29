# Newsroom Yukkuri Animation V2 Preview Observation v1

artifact_id: newsroom_yukkuri_animation_v2_preview_observation_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_v2_preview_observation.v1
production_status: diagnostic_only
render_gate: L0_no_render
next_axis: motion_tempo_calibration


## Source V2 Probe Access

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


## Normalized User Observation

```json
{
  "source_observation_role": "user_opened_local_v2_ymmp_preview",
  "source_v2_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v2_motion_fix.ymmp",
  "yym4_opened": true,
  "v2_preview_observed": true,
  "anchor_continuity": "improved",
  "segment_connection": "pass",
  "x_jump_regression": "not_reported",
  "motion_speed": "too_slow",
  "tempo_status": "fail_or_warning",
  "major_visual_breakage": false,
  "render_export_checked": false,
  "render_export_required_now": false,
  "next_axis": "motion_tempo_calibration"
}
```


## Primitive Tempo Classification

| primitive_id | classification | v2_status | observed_issue | decision |
| --- | --- | --- | --- | --- |
| head_nod | pass_with_tempo_warning | anchor/neutral-return improved | nod still reads too slowly for a short reaction beat | halve the beat span while preserving 0 -> tilt -> 0 return |
| expression_swap | pass | beat-aligned and readable | no expression regression reported | keep one expression per faster beat; do not flicker mid-beat |
| character_entrance_exit | pass_with_tempo_warning | bounded neutral movement improved connection | movement still feels slow and drifting | halve the bounded travel span while preserving shared anchors |
| small_position_move | pass_with_tempo_warning | anchor continuity improved and X jump not reported | small movement still feels too slow | halve the nudge span and keep return to X=-96 |


## Render Deferral

```json
{
  "render_export_checked": false,
  "render_export_required_now": false,
  "render_deferred_reason": "The user-side v2 preview confirmed smooth segment connection, so the remaining bottleneck is tempo calibration rather than render/export proof."
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


## Boundary Note

This readback normalizes a user-side v2 preview observation only. It does not render, launch YMM4 from the agent, stage media, or accept production/public quality.
