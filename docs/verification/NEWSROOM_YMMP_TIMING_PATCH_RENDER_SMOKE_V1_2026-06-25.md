# Newsroom YMM4 Timing Patch Render Smoke v1

artifact_id: newsroom_ymmp_timing_patch_render_smoke_v1_2026_06_25
smoke_id: newsroom_ymmp_timing_patch_render_smoke_v1_2026_06_25
schema_version: newsroom_ymmp_timing_patch_render_smoke.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
smoke_status: prepared_not_run
package_status: ready_for_manual_milestone_render_smoke
diagnostic_only: true

## Source

- smoke_id: newsroom_ymmp_timing_patch_render_smoke_v1_2026_06_25
- source_probe_path: samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json
- source_probe_id: newsroom_ymmp_timing_patch_probe_v1_2026_06_24
- source_probe_readback_path: samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_readback_v1.json
- source_probe_readback_id: newsroom_ymmp_timing_patch_probe_readback_v1_2026_06_24
- source_native_audio_path_proof_path: samples/_probe/newsroom_handoff/yym4_native_audio_path_proof_v1.json
- source_native_audio_path_proof_id: newsroom_yym4_native_audio_path_proof_v1_2026_06_24
- source_audio_observation_path: samples/_probe/newsroom_handoff/audio_observation_and_timing_patch_readiness_v1.json
- source_audio_observation_id: newsroom_audio_observation_and_timing_patch_readiness_v1_2026_06_24
- patched_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- production_status: diagnostic_only
- render_smoke_status: not_run

## Source Validation

- status: passed
- probe_id: newsroom_ymmp_timing_patch_probe_v1_2026_06_24
- probe_readback_id: newsroom_ymmp_timing_patch_probe_readback_v1_2026_06_24
- patch_method: neutral_timeline_skeleton_patch_with_native_voice_preserved
- patched_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- patched_ymmp_found_at_generation: true
- patched_total_sec: 68.0
- patched_total_frames: 4080
- patched_dialogue_item_count: 4
- native_voice_path_preserved: true
- external_TTS_introduced: false
- render_already_performed: false
- errors: []

## Target

- patched_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- patched_ymmp_path_status: discoverable_local_file_at_generation_time
- git_tracking_policy: ignored_under_tmp_do_not_stage_or_commit
- expected_duration_sec: 68.0
- expected_total_frames: 4080
- expected_dialogue_item_count: 4
- expected_item_frames: [0, 720, 1440, 2760]
- expected_item_lengths: [720, 720, 1320, 1320]

## Milestone Render Gate

- gate_type: milestone_gated_verification
- milestone: newsroom-ymmp-timing-patch-render-smoke-v1
- render_performed_in_this_slice: false
- YMM4_launched_by_agent: false
- manual_render_allowed_next: true
- manual_render_count: 1
- render_reason: structural timing patch reached 68 sec and needs real YMM4 open/render confirmation
- timing_strategy_change_allowed: false
- external_TTS_allowed: false
- render_output_commit_allowed: false
- ymmp_commit_allowed: false

## Operator Observation Card

- status: required_next_milestone
- target: patched diagnostic .ymmp render smoke
- patched_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- why: Confirm YMM4 accepts the 68 sec structural patch on the real open/render surface.
- action: Open the patched diagnostic .ymmp in YMM4 and render once without changing timing, voice, or media.
- answer_style: freeform
- answer_hint: opened and rendered; about 68 sec; four dialogue items and native voice remained
- look_for:
  - patched project opens successfully
  - render completes
  - output duration is approximately 68 seconds
  - four dialogue items remain present
  - native YMM4/Yukkuri audio remains present
- not_needed:
  - fixed form
  - detailed sound quality review
  - production quality judgement
  - screenshots unless useful
  - committing .ymmp or media output

## Result Normalization Schema

- schema_owner: Agent
- user_must_fill_schema: false
- duration_tolerance_sec: 2

| field | type | normalization |
|---|---|---|
| patched_project_opened | boolean_or_unknown | true only when the patched .ymmp opens in YMM4 |
| render_completed | boolean_or_unknown | true only when YMM4 export finishes |
| output_duration_observed_sec | number_or_null | observed media duration in seconds when known |
| duration_approximately_68_sec | boolean_or_unknown | true when duration is within the configured 68 sec tolerance |
| dialogue_items_preserved | boolean_or_unknown | true when the four expected dialogue items remain present |
| dialogue_item_count_observed | integer_or_null | observed dialogue item count if the operator reports it |
| native_audio_present | boolean_or_unknown | true when native YMM4/Yukkuri audio is still audible |
| operator_notes | string_or_null | freeform notes retained without making the user fill a form |
| error_message | string_or_null | YMM4 or export error text when reported |
| confidence | string | agent confidence in the normalized observation |
| unknowns | array | required targets the observation did not settle |
| classification | enum | classification from the success/failure matrix |
| result | enum | pass, fail, or blocked_by_operator_uncertainty |

## Success / Failure Classification Matrix

| classification | trigger | result | next slice |
|---|---|---|---|
| post_patch_render_smoke_pass | all five observation targets are true | pass | newsroom-ymmp-timing-patch-render-smoke-result-readback-v1 |
| patched_project_open_failure | patched project does not open | fail | newsroom-ymmp-timing-patch-render-failure-classification-v1 |
| patched_render_execution_failure | project opens but render does not complete | fail | newsroom-ymmp-timing-patch-render-failure-classification-v1 |
| patched_duration_mismatch | render completes but output is not approximately 68 sec | fail | newsroom-ymmp-timing-patch-render-failure-classification-v1 |
| dialogue_preservation_regression | render completes but dialogue items are missing or altered | fail | newsroom-ymmp-timing-patch-render-failure-classification-v1 |
| native_audio_preservation_regression | render completes and dialogue remains, but native audio is absent | fail | newsroom-ymmp-timing-patch-render-failure-classification-v1 |
| operator_observation_uncertain | one or more required observation targets remain unknown | blocked_by_operator_uncertainty | newsroom-ymmp-timing-patch-render-smoke-operator-uncertainty-v1 |

## Render Readback Builder

- builder_id: newsroom_ymmp_timing_patch_render_smoke_result_readback_builder_v1
- module: src.pipeline.newsroom_ymmp_timing_patch_render_smoke
- function: build_newsroom_ymmp_timing_patch_render_smoke_result_readback
- input_package: samples/_probe/newsroom_handoff/ymmp_timing_patch_render_smoke_v1.json
- input_observation: future freeform operator observation normalized by Agent
- output_schema_version: newsroom_ymmp_timing_patch_render_smoke_result_readback.v1
- writes_artifact_in_this_slice: false
- requires_committed_media: false
- requires_committed_ymmp: false
- classification_function: classify_render_smoke_observation

## Boundaries

- YMM4_launched_by_agent: false
- render_created_by_agent: false
- audio_generated_by_agent: false
- TTS_generated_by_agent: false
- external_TTS_introduced: false
- real_media_imported: false
- external_fetch_performed: false
- ymmp_created_or_modified_by_agent: false
- ymmp_or_media_staged_or_committed: false
- render_output_staged_or_committed: false
- timing_strategy_changed: false
- production_approval: false
- public_video_ready: false
- dashboard_governance_freshness_changed: false

## Boundary Note

This packet prepares the next manual milestone render smoke only. The agent did not launch YMM4, render, modify the patched `.ymmp`, generate or replace audio, stage media, or change the timing strategy. A later freeform observation should be normalized by the builder in this module before any production-readiness claim.
