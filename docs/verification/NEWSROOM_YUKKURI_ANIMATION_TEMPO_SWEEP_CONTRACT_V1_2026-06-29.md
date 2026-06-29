# Newsroom Yukkuri Animation Tempo Sweep Contract v1

artifact_id: newsroom_yukkuri_animation_tempo_sweep_contract_v1_2026_06_29
schema_version: newsroom_yukkuri_animation_tempo_sweep_contract.v1
production_status: diagnostic_only
render_gate: L0_no_render
v4_materialization_status: materialized_ignored_local_probe
selected_next_axis: newsroom-yukkuri-animation-tempo-sweep-preview-operator-instruction-v1


## Source Context

```json
{
  "source_v3_probe_path": "_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp",
  "source_v3_observation_path": "samples/_probe/newsroom_handoff/yukkuri_animation_v3_preview_observation_v1.json",
  "source_tempo_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_tempo_contract_v1.json",
  "source_motion_contract_path": "samples/_probe/newsroom_handoff/yukkuri_animation_motion_contract_v1.json",
  "source_nod_head_ymmp_path": "samples/nod_head.ymmp",
  "v3_materialization_basis": "existing tracked v3 tempo contract materializer"
}
```


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


## V3 Issue Summary

```json
[
  "v3 is shorter than v2",
  "v3 is still floaty and too slow",
  "user suggested starting around 1 second",
  "single-value fast/slow loops are inefficient",
  "render/export remains unnecessary for this stage"
]
```


## Tempo Bands

| band_id | frame_span | seconds_at_60fps | expected_feel | primitives_included | continuity_policy | anchor_policy | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tempo_band_030f_0_5s | 30 | 0.5 | very snappy lower bound; likely useful for reaction-only motion | ["head_nod", "small_position_move", "character_entrance_exit", "expression_swap"] | carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries | do not reintroduce X jump; each nudge starts and ends on the shared anchor | Fastest comparison band; expression readability may need a longer hold in scene integration. |
| tempo_band_045f_0_75s | 45 | 0.75 | quick but still readable; candidate if 1.0 second remains floaty | ["head_nod", "small_position_move", "character_entrance_exit", "expression_swap"] | carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries | keep bounded entry/exit and return-to-anchor nudges | Middle-fast comparison band for lightweight reenactment beats. |
| tempo_band_060f_1_0s | 60 | 1.0 | primary default candidate based on the user suggestion to start around 1 second | ["head_nod", "small_position_move", "character_entrance_exit", "expression_swap"] | carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries | keep head nod as a short reaction and movement as bounded cue | Expected default candidate unless preview shows it is still slow or too abrupt. |
| tempo_band_090f_1_5s | 90 | 1.5 | upper comparison band; should reveal whether longer movement still reads floaty | ["head_nod", "small_position_move", "character_entrance_exit", "expression_swap"] | carry forward v2/v3 X=-96 shared anchor at adjacent beat boundaries | bounded movement only; no slow centerward drift | Kept as a contrast band rather than a likely default after the v3 observation. |


## Primitive Coverage Per Band

| band_id | frame_span | primitive_ids | beat_count | section_timing_range |
| --- | --- | --- | --- | --- |
| tempo_band_030f_0_5s | 30 | ["character_entrance_exit", "expression_swap", "head_nod", "small_position_move"] | 5 | 0.00-2.50 sec |
| tempo_band_045f_0_75s | 45 | ["character_entrance_exit", "expression_swap", "head_nod", "small_position_move"] | 5 | 2.50-6.25 sec |
| tempo_band_060f_1_0s | 60 | ["character_entrance_exit", "expression_swap", "head_nod", "small_position_move"] | 5 | 6.25-11.25 sec |
| tempo_band_090f_1_5s | 90 | ["character_entrance_exit", "expression_swap", "head_nod", "small_position_move"] | 5 | 11.25-18.75 sec |


## Anchor Continuity Carry Forward

```json
{
  "source_policy": "v2/v3 shared anchor",
  "shared_anchor_x": -96.0,
  "no_x_jump_regression": true,
  "entry_exit_policy": "bounded side travel only",
  "small_move_policy": "start and end at X=-96",
  "head_nod_policy": "0 -> negative -> 0 neutral return"
}
```


## Expected Default Candidate

```json
{
  "band_id": "tempo_band_060f_1_0s",
  "frame_span": 60,
  "seconds_at_60fps": 1.0,
  "reason": "The user suggested starting around 1 second; 0.75 and 0.5 seconds are comparison lower bounds."
}
```


## Review Instruction For Next Preview

```json
[
  "Open the v4 tempo sweep probe only; do not render.",
  "Review bands in the encoded order: 0.5 sec, 0.75 sec, 1.0 sec, 1.5 sec.",
  "Choose the default tempo band, or report that all bands are still too slow/too abrupt.",
  "After a usable band is chosen, stop the primitive tempo-only loop and move to scene-beat integration."
]
```


## Exit Criterion

```json
{
  "choose_default_tempo_band": true,
  "stop_primitive_tempo_only_loop": true,
  "move_to_scene_beat_integration_after_usable_band": true
}
```


## V4 Local Probe

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


## V4 Probe Readback

```json
{
  "readback_status": "structural_pass",
  "target_exists": true,
  "file_sha256": "664c6a0abe9774aa96e4c937694fec6371a0c5f6eb2ce8d6d4c18f118a9bdc19",
  "file_size_bytes": 811331,
  "timeline": {
    "fps": 60,
    "length_frames": 1125,
    "length_sec": 18.75,
    "item_count": 80,
    "item_type_counts": {
      "GroupItem": 40,
      "ImageItem": 40
    },
    "unexpected_item_types": []
  },
  "speed_band_order": [
    "tempo_band_030f_0_5s",
    "tempo_band_045f_0_75s",
    "tempo_band_060f_1_0s",
    "tempo_band_090f_1_5s"
  ],
  "band_readback": [
    {
      "band_id": "tempo_band_030f_0_5s",
      "frame_span": 30,
      "seconds_at_60fps": 0.5,
      "section_start_frame": 0,
      "section_end_frame": 150,
      "section_timing_range": "0.00-2.50 sec",
      "beat_count": 5,
      "primitive_ids": [
        "character_entrance_exit",
        "expression_swap",
        "head_nod",
        "small_position_move"
      ],
      "anchor_continuity": "pass",
      "status": "pass"
    },
    {
      "band_id": "tempo_band_045f_0_75s",
      "frame_span": 45,
      "seconds_at_60fps": 0.75,
      "section_start_frame": 150,
      "section_end_frame": 375,
      "section_timing_range": "2.50-6.25 sec",
      "beat_count": 5,
      "primitive_ids": [
        "character_entrance_exit",
        "expression_swap",
        "head_nod",
        "small_position_move"
      ],
      "anchor_continuity": "pass",
      "status": "pass"
    },
    {
      "band_id": "tempo_band_060f_1_0s",
      "frame_span": 60,
      "seconds_at_60fps": 1.0,
      "section_start_frame": 375,
      "section_end_frame": 675,
      "section_timing_range": "6.25-11.25 sec",
      "beat_count": 5,
      "primitive_ids": [
        "character_entrance_exit",
        "expression_swap",
        "head_nod",
        "small_position_move"
      ],
      "anchor_continuity": "pass",
      "status": "pass"
    },
    {
      "band_id": "tempo_band_090f_1_5s",
      "frame_span": 90,
      "seconds_at_60fps": 1.5,
      "section_start_frame": 675,
      "section_end_frame": 1125,
      "section_timing_range": "11.25-18.75 sec",
      "beat_count": 5,
      "primitive_ids": [
        "character_entrance_exit",
        "expression_swap",
        "head_nod",
        "small_position_move"
      ],
      "anchor_continuity": "pass",
      "status": "pass"
    }
  ],
  "tempo_sweep_summary": {
    "band_count": 4,
    "beat_count_per_band": 5,
    "total_beat_count": 20,
    "frame_spans": [
      30,
      45,
      60,
      90
    ],
    "seconds_at_60fps": [
      0.5,
      0.75,
      1.0,
      1.5
    ],
    "expected_default_candidate": "tempo_band_060f_1_0s"
  },
  "source_ymmp_copy_basis": "samples/nod_head.ymmp",
  "git_check_ignore_result": {
    "command": "git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
    "returncode": 0,
    "stdout": ".gitignore:37:_tmp/\t_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v4_tempo_sweep.ymmp",
    "stderr": "",
    "ignored": true
  },
  "local_probe_access_state": "verified_present",
  "YMM4_launch_status": "not_launched",
  "render_status": "not_rendered",
  "audio_tts_status": "not_created"
}
```


## Next Recommended Axis

```json
{
  "selected": "newsroom-yukkuri-animation-tempo-sweep-preview-operator-instruction-v1",
  "reason": "ignored local v4 tempo sweep probe exists, is git-ignored, covers all requested bands, and preserves the v2/v3 anchor rules",
  "prerequisites": [
    "keep v4 .ymmp ignored and unstaged",
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
| tempo_sweep_replaces_single_value_loop | True |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-tempo-sweep-preview-operator-instruction-v1 |


## Boundary Note

The v4 probe is an ignored local diagnostic artifact. It is not rendered, not staged, not committed, and not production/public acceptance.
