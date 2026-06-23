# Newsroom Minimal .ymmp Boundary Decision v1

artifact_id: newsroom_minimal_ymmp_boundary_decision_v1_2026_06_23
decision_id: newsroom_minimal_ymmp_boundary_decision_v1_2026_06_23
schema_version: newsroom_minimal_ymmp_boundary_decision.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
decision_status: approved_for_next_probe_packet
diagnostic_only: true

## Source

- source_bound_speaker_readiness_path: samples/_probe/newsroom_handoff/yym4_bound_speaker_import_readiness_v1.json
- source_bound_speaker_readiness_id: newsroom_yym4_bound_speaker_import_readiness_v1_2026_06_23
- source_bound_csv_path: samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv
- source_commit_or_status: worktree_verified_before_generation

## Accepted Inputs

- bound_CSV_accepted_in_current_environment: true
- speaker_value: ゆっくり霊夢
- row_count: 4
- text_visible: true
- speaker_prompt_shown: false
- accepted_for: diagnostic_yym4_script_import_in_current_environment

## .ymmp Boundary

- current_ymmp_status: not_created
- agent_may_create_ymmp_now: false
- user_manual_ymmp_probe_may_be_prepared_next: true
- production_ymmp_allowed: false
- render_allowed: false
- TTS_generation_allowed: false
- real_media_allowed: false

## Recommended Next Path

- choice: prepare_manual_diagnostic_ymmp_probe_packet
- next_recommended_slice: newsroom-diagnostic-ymmp-probe-packet-v1
- reason: Bound speaker CSV import is accepted in the current diagnostic environment, but the CSV path does not carry the 68 second neutral timing plan. The narrow next move is to prepare, not execute, a manual diagnostic .ymmp probe packet that keeps render, TTS, real media, and production closed.

## Timing Gap Policy

- neutral_timeline_total_sec: 68
- observed_yym4_import_approx_sec: 8.48
- timing_imported_by_csv: false
- recommended_default: accept YMM4 natural duration for first diagnostic .ymmp
- reason: The next probe should isolate the save/readback boundary first. Using YMM4 natural dialogue duration avoids mixing manual timing adjustment with the first diagnostic .ymmp evidence.
- options:
  - accept YMM4 natural duration for first diagnostic .ymmp
  - patch timing after import
  - keep timing metadata external until render path

## Evidence Policy

- input_mode: freeform
- template_required: false
- schema_owner: Agent
- screenshot_optional: true
- sufficient_freeform_evidence:
  - whether a diagnostic .ymmp was saved
  - whether 4 imported dialogue rows still exist
  - whether timing stayed short or was manually adjusted

## Operator Observation Card

- status: for_next_probe_packet_only
- target: manual diagnostic .ymmp probe after a future packet is written
- why: Confirm only the save/readback and timing-boundary behavior for a diagnostic project, without render, TTS, real media, or production.
- action: If a later packet authorizes it, save a diagnostic project from the bound CSV import and answer in freeform.
- answer_style: freeform
- look_for:
  - .ymmp saved or not saved
  - 4 dialogue rows still present
  - timing stayed short or was adjusted
- not_needed:
  - fixed result form
  - render confirmation
  - TTS/audio confirmation
  - production approval

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

## Review Card

Review Card: none. This is an agent-owned boundary decision and does not ask for repeated prior review or a fixed result template.

## Boundary

This decision does not create `.ymmp`, launch YMM4, render, generate TTS/audio, import real media, fetch external sources, approve production, or prepare a public video.
