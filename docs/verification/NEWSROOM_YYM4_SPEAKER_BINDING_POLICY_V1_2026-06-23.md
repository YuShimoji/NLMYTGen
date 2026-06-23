# Newsroom YMM4 Speaker Binding Policy v1

artifact_id: newsroom_yym4_speaker_binding_policy_v1_2026_06_23
policy_id: newsroom_yym4_speaker_binding_policy_v1_2026_06_23
schema_version: newsroom_yym4_speaker_binding_policy.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
policy_status: diagnostic_candidate
diagnostic_only: true

## Source

- source_manual_result_path: samples/_probe/newsroom_handoff/yym4_manual_import_result_readback_v1.json
- source_manual_result_id: newsroom_yym4_manual_import_result_readback_v1_2026_06_23
- source_tiny_csv_path: samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv
- source_commit_or_status: worktree_verified_before_generation

## Observed Binding

- source_placeholder_speaker: synthetic_newsroom_placeholder
- observed_manual_character: ゆっくり霊夢
- observed_behavior: manual_selection_required
- import_result: pass_with_warnings
- automatic_binding_observed: false
- observed_line_count: 4
- all_text_visible: true

## Binding Proposal

- proposed_binding_mode: emit_existing_yym4_character_name
- recommended_default: emit_existing_yym4_character_name
- candidate_speaker_name: ゆっくり霊夢
- fallback_behavior: manual selection remains allowed
- automatic_binding_claimed: false
- reason: The manual result showed that selecting the existing YMM4 character resolved the placeholder safely while all four diagnostic texts stayed visible. Emitting that existing character name in a separate candidate CSV reduces the next manual import friction without claiming automatic binding, TTS readiness, .ymmp readiness, or production approval.

## Bound CSV Candidate

- created: true
- path: samples/_probe/newsroom_handoff/tiny_script_import_candidate_yukkuri_reimu_v1.csv
- status: not_YMM4_verified, intended_for_next_manual_check
- encoding: utf-8-sig
- preserve_utf8_bom: true
- has_header: false
- timing_columns_in_csv: false
- production_ready_flags_in_csv: false

| csv_row | source speaker | bound speaker | text |
|---|---|---|---|
| 1 | synthetic_newsroom_placeholder | ゆっくり霊夢 | Fake topic, review only. |
| 2 | synthetic_newsroom_placeholder | ゆっくり霊夢 | Review-only handoff stays. |
| 3 | synthetic_newsroom_placeholder | ゆっくり霊夢 | A fake claim is shown. |
| 4 | synthetic_newsroom_placeholder | ゆっくり霊夢 | Fake source checks are noted. |

## Candidate Validation

- row_count: 4
- expected_row_count: 4
- all_text_preserved_exactly: true
- only_speaker_column_changed: true
- no_timing_columns: true
- no_media_paths: true

## Review Memory

- prior_user_review_count: 1
- repeated_general_review_allowed: false
- next_nonredundant_axis:
  - speaker_binding_policy
  - placeholder_to_yym4_character_mapping
  - bound_speaker_csv_candidate

## Not Accepted Scope

- automatic_speaker_binding: false
- TTS_ready_script: false
- ymmp: false
- render: false
- production_readiness: false
- public_video: false
- YMM4_approval: false

## Safety Boundary

- ymmp_created: false
- YMM4_launched_by_agent: false
- render_created: false
- TTS_generated: false
- real_media_imported: false
- production_approval: false
- public_video_ready: false

## Next Use

- recommended_next_slice: newsroom-yym4-bound-speaker-manual-check-packet-v1
- fallback_next_slice: newsroom-yym4-import-readiness-after-manual-result-v1
- if_bound_csv_candidate_is_used: Create a new manual check packet for the bound-speaker CSV and verify whether YMM4 accepts the explicit existing character name without asking the operator to bind it again.
- do_not_recommend_immediate:
  - production .ymmp
  - render
  - TTS/audio generation
  - real media import
  - production approval
  - public video

## Review Card

Review Card: none. The prior manual import result is already recorded, and this policy only defines the speaker-binding axis and a separate bound CSV candidate.

## Boundary

This policy is diagnostic-only. It does not prove automatic speaker binding, TTS readiness, `.ymmp` readiness, render readiness, production readiness, YMM4 approval, or public video readiness.
