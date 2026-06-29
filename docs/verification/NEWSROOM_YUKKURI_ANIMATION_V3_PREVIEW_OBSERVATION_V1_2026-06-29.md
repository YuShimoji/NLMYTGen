# Newsroom Yukkuri Animation V3 Preview Observation v1

artifact_id: newsroom_yukkuri_animation_v3_preview_observation_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_v3_preview_observation.v1
production_status: diagnostic_only
render_gate: L0_no_render


## Source V3 Probe Access

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


## Normalized User Observation

```json
{
  "source_observation_role": "user_opened_local_v3_ymmp_preview",
  "source_v3_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp",
  "yym4_opened": true,
  "v3_preview_observed": true,
  "motion_speed": "still_too_slow",
  "floatiness": "high",
  "v3_tempo_improved_but_insufficient": true,
  "single_value_iteration_risk": true,
  "recommended_method": "tempo_sweep",
  "render_export_checked": false,
  "render_export_required_now": false,
  "next_axis": "tempo_sweep_calibration"
}
```


## Current Issue

```json
{
  "motion_speed": "still_too_slow",
  "floatiness": "high",
  "v3_tempo_improved_but_insufficient": true,
  "next_axis": "tempo_sweep_calibration"
}
```


## Single Value Iteration Risk

```json
{
  "risk": true,
  "reason": "The user already distinguished shorter from usable. More one-value speed changes would keep asking the operator for fast/slow feedback instead of choosing a default band.",
  "replacement_method": "compare 0.5, 0.75, 1.0, and 1.5 second bands in one ignored local probe"
}
```


## Render Deferral

```json
{
  "render_export_checked": false,
  "render_export_required_now": false
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

This readback normalizes a user-side v3 preview observation only. It does not render, launch YMM4 from the agent, stage media, or accept production/public quality.
