# Newsroom Yukkuri Animation V4 Tempo Sweep Observation v1

artifact_id: newsroom_yukkuri_animation_v4_tempo_sweep_observation_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_v4_tempo_sweep_observation.v1
production_status: diagnostic_only
render_gate: L0_no_render


## Source V4 Probe Access

```json
{
  "artifact_id": "local_ignored_v4_tempo_sweep_probe",
  "repo_relative_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
  "folder_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe",
  "file_full_path_current_host": "C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
  "launcher_or_open_command": "Invoke-Item -LiteralPath \"C:\\Users\\thank\\Storage\\Media Contents Projects\\NLMYTGen-mainline-slot-linkage\\_tmp\\newsroom_manual_probe\\yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp\"",
  "target_exists": true,
  "access_state": "verified_present",
  "access_evidence_level": "L3_VERIFIED_PRESENT",
  "artifact_scope": "ignored_local_only",
  "evidence_source": "current_host_filesystem_plus_git_check_ignore",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
    "stderr": "",
    "ignored": true
  },
  "size": 811331
}
```


## Normalized User Observation

```json
{
  "source_observation_role": "user_opened_local_v4_tempo_sweep_preview",
  "source_v4_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
  "yym4_opened": true,
  "v4_preview_observed": true,
  "default_tempo_band": "0.75s",
  "default_frame_span_at_60fps": 45,
  "scene_dependency": true,
  "one_second_status": "acceptable_variant_for_slower_explanatory_or_readability_heavy_moments",
  "half_second_status": "acceptable_variant_for_quick_reaction_punch_or_small_emphasis",
  "one_point_five_second_status": "not_selected_as_default_upper_comparison_or_special_slow_case_only",
  "tempo_loop_exit": true,
  "primitive_only_loop_exit": true,
  "next_axis": "newsroom-yukkuri-animation-scene-beat-integration-v1",
  "render_export_checked": false,
  "render_export_required_now": false,
  "production_public_render_approval_given": false
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


## Tempo Only Loop Exit

```json
{
  "exit": true,
  "reason": "The v4 sweep has selected a default timing policy: 0.75s / 45 frames is the most natural default, while 0.5s and 1.0s remain acceptable by scene. The next bottleneck is applying that policy inside scene beats, not another primitive-only fast/slow loop.",
  "next_axis": "newsroom-yukkuri-animation-scene-beat-integration-v1"
}
```


## Primitive Feasibility Judgment

```json
{
  "status": "not_reopened",
  "reason": "this readback records tempo selection only; production animation quality remains unapproved"
}
```


## Motion Coherence Warning

```json
{
  "status": "deferred_to_scene_beat_integration",
  "issues": [
    "duration choice depends on scene function",
    "primitive timing should be evaluated inside a scene-beat structure"
  ]
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

This readback normalizes a user-side v4 preview observation only. It does not render, launch YMM4 from the agent, stage media, or accept production/public quality.
