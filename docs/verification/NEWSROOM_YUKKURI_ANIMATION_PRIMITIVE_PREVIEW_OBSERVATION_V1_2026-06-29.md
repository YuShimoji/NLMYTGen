# Newsroom Yukkuri Animation Primitive Preview Observation v1

artifact_id: newsroom_yukkuri_animation_primitive_preview_observation_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_primitive_preview_observation.v1
production_status: diagnostic_only
render_gate: L0_no_render
next_axis: motion_timing_facing_anchor_continuity_fix


## Source V1 Probe Access

```json
{
  "artifact_id": "local_ignored_primitive_probe_v1",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
  "folder_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v1.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v1.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 261441
}
```


## Normalized User Observation

```json
{
  "source_observation_role": "user_opened_local_ymmp_preview",
  "source_v1_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v1.ymmp",
  "yym4_opened": true,
  "character_visible": true,
  "head_body_attachment": "pass",
  "expression_swap": "pass",
  "character_motion_visible": "pass_with_warning",
  "entrance_exit": "pass_with_facing_warning",
  "small_position_move": "pass_with_anchor_continuity_warning",
  "head_nod": "pass_with_timing_warning",
  "major_visual_breakage": false,
  "render_export_checked": false,
  "render_export_required_now": false,
  "next_axis": "motion_timing_facing_anchor_continuity_fix"
}
```


## Primitive Classification

| primitive_id | classification | observed_issue | decision |
| --- | --- | --- | --- |
| head_nod | pass_with_timing_warning | nod was visible but excessively slow and read as one slow vertical nod | keep primitive, shorten beat timing, require return-to-neutral |
| expression_swap | pass | several expressions switched; no major breakage reported | keep expression swap but bind each expression to a beat span |
| character_entrance_exit | pass_with_facing_warning | movement appeared backward toward screen center, suggesting missing facing/orientation intent | avoid broad facing-dependent travel in v2; use neutral bounded side entry/exit |
| small_position_move | pass_with_anchor_continuity_warning | X position changed between animation segments and produced jumpy disconnected movement | carry X anchors across adjacent beats unless a cut is explicit |


## Render Deferral

```json
{
  "render_export_checked": false,
  "render_export_required_now": false,
  "render_deferred_reason": "User-side preview opened the .ymmp and confirmed the current stage: the remaining problem is motion timing, facing, and anchor continuity, not render/export mechanics."
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

This readback normalizes a user-side preview observation only. It does not render, launch YMM4 from the agent, stage media, or accept production/public quality.
