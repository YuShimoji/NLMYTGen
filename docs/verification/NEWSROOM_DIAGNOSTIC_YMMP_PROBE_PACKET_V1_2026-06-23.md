# Newsroom Diagnostic .ymmp Probe Packet v1

artifact_id: newsroom_diagnostic_ymmp_probe_packet_v1_2026_06_23
packet_id: newsroom_diagnostic_ymmp_probe_packet_v1_2026_06_23
schema_version: newsroom_diagnostic_ymmp_probe_packet.v1
review_status: ready_for_future_manual_probe
production_status: diagnostic_only
manual_probe_status: not_run
diagnostic_only: true

## Source

- source_boundary_decision_path: samples/_probe/newsroom_handoff/minimal_ymmp_boundary_decision_v1.json
- source_boundary_decision_id: newsroom_minimal_ymmp_boundary_decision_v1_2026_06_23
- source_bound_speaker_readiness_path: samples/_probe/newsroom_handoff/yym4_bound_speaker_import_readiness_v1.json
- source_bound_csv_path: samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv

## Target

- target_csv: samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv
- intended_YMM4_environment: manual/operator-run only
- expected_row_count: 4
- speaker_value: ゆっくり霊夢
- encoding: UTF-8 BOM
- header: false
- columns: speaker, text

## Expected Starting Point

- import_bound_speaker_csv: true
- confirm_4_rows_and_speaker: true
- save_minimal_diagnostic_ymmp_only_if_operator_comfortable: true
- do_not_render: true
- do_not_generate_TTS: true
- do_not_import_real_media: true
- timing_patch_in_this_probe: false

## Allowed Future Manual Action

- manual_YMM4_launch_by_user_operator: true
- manual_diagnostic_ymmp_save: true
- manual_diagnostic_ymmp_save_scope: diagnostic observation only
- recommended_save_location: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp
- recommended_save_location_created_by_agent: false
- committing_ymmp_allowed_now: false
- committing_ymmp_condition: not allowed unless a later explicit result-readback slice approves it

## Forbidden Actions

- Agent_YMM4_launch: false
- Agent_ymmp_creation: false
- render: false
- TTS_generation: false
- real_media_import: false
- production_approval: false
- public_video_claim: false
- external_fetch: false
- real_newsroom_ingest: false

## Operator Observation Card

- status: required_later
- target: diagnostic .ymmp probe from bound speaker CSV
- why: Confirm whether YMM4 can save the imported 4-line script as a project without render, TTS, real media, or production flow.
- action: Manually import the bound CSV in YMM4 and, only if comfortable, save a diagnostic .ymmp outside production flow.
- look_for:
  - 4 dialogue rows remain after save/reopen or save observation
  - speaker remains ゆっくり霊夢
  - timing stays natural short duration or changes unexpectedly
- answer_style: freeform
- answer_hint: One sentence is enough, for example: saved; 4 rows and speaker remained; timing stayed short.
- not_needed:
  - render
  - TTS
  - real media
  - production approval
  - fixed form
  - screenshot unless useful

## Agent Normalization Plan

- schema_owner: Agent
- exposed_as_user_form: false
- fields:
  - result
  - ymmp_saved
  - row_count_observed
  - speaker_preserved
  - timing_observation
  - render_created
  - TTS_generated
  - media_imported
  - confidence
  - unknowns

## Timing Policy

- neutral_timeline_total_sec: 68
- observed_yym4_import_approx_sec: 8.48
- first_probe_expected_timing: YMM4 natural duration
- timing_patch_in_this_probe: false
- next_timing_axis:
  - timing_gap_strategy
  - optional ymmp_patch_strategy after project structure is known

## Human Burden Hygiene

- user_input: freeform
- template_required: false
- schema_owner: Agent
- max_required_points: 3
- screenshot_optional: true
- negative_confirmations_required_from_user: false
- fixed_form_result_template: false

## Not Accepted Scope

- production_readiness: false
- render_readiness: false
- TTS_readiness: false
- public_video_readiness: false
- visual_layout_import: false
- portability_across_all_YMM4_installations: false
- timing_import_from_neutral_timeline_metadata: false
- committed_ymmp_artifact: false

## Next Recommended Slices

- newsroom-diagnostic-ymmp-manual-result-readback-v1
- newsroom-yym4-timing-gap-strategy-v1
- newsroom-ymmp-structure-readback-v1

## Review Card

Review Card: none. This packet prepares a later manual diagnostic probe and does not ask for repeated prior-artifact review.

## Boundary

This packet does not create `.ymmp`, launch YMM4, render, generate TTS/audio, import real media, fetch external sources, approve production, or prepare a public video.
