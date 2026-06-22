# Newsroom Tiny Importable Proof v1

artifact_id: newsroom_tiny_importable_proof_v1_2026_06_22
proof_id: newsroom_tiny_importable_proof_v1_2026_06_22
schema_version: newsroom_tiny_importable_proof.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
tiny_importable_status: passed_with_warnings
diagnostic_only: true

## Source

- source_yym4_adjacent_shape_path: samples/_probe/newsroom_handoff/yym4_adjacent_no_media_import_shape_v1.json
- source_script_candidate_path: samples/_probe/newsroom_handoff/script_import_candidate_v1.json
- import_artifact_path: samples/_probe/newsroom_handoff/tiny_script_import_candidate_v1.csv
- import_artifact_type: tool_adjacent_csv
- source_episode_id: episode_fake_nlmytgen_delta_v1
- source_commit_or_status: worktree_verified_before_generation

## Review Memory

- prior_user_review_count: 0
- current_axis: tiny_importable_artifact_shape
- repeated_general_review_allowed: false

## Tiny Importable Summary

- columns: speaker, text
- has_header: false
- encoding: utf-8-sig
- row_count: 4
- timing_columns_in_csv: false
- production_ready_flags_in_csv: false

## Source Mapping Summary

| csv_row | source_row_id | source_line_id | source_caption_id | speaker | text | timing metadata |
|---|---|---|---|---|---|---|
| 1 | yym4_adjacent_row_01 | line_01_cap_beat_fake_intro_001_01 | cap_beat_fake_intro_001_01 | synthetic_newsroom_placeholder | Fake topic, review only. | 0-12s / 12s |
| 2 | yym4_adjacent_row_02 | line_02_cap_beat_fake_intro_001_02 | cap_beat_fake_intro_001_02 | synthetic_newsroom_placeholder | Review-only handoff stays. | 12-24s / 12s |
| 3 | yym4_adjacent_row_03 | line_03_cap_beat_fake_claim_001_01 | cap_beat_fake_claim_001_01 | synthetic_newsroom_placeholder | A fake claim is shown. | 24-46s / 22s |
| 4 | yym4_adjacent_row_04 | line_04_cap_beat_fake_claim_001_02 | cap_beat_fake_claim_001_02 | synthetic_newsroom_placeholder | Fake source checks are noted. | 46-68s / 22s |

## Row Validation

- row_count: 4
- expected_row_count: 4
- every_row_maps_exactly_one_source_row: true
- all_rows_valid: true
- no_real_names_detected: true

## Boundary Summary

- ymmp_created: false
- YMM4_launched: false
- YMM4_carrier_created: false
- YMM4_approval: false
- TTS_generated: false
- render_created: false
- public_video_ready: false

## Diagnostic Safety

- real_urls: false
- real_media_paths: false
- production_approval: false

## Next Use

- tiny_importable_status: passed_with_warnings
- warnings:
  - not_YMM4_verified
  - timing_metadata_not_imported
  - no_audio
  - no_media
  - synthetic_speaker_not_bound_to_YMM4_character
- recommended_next_slice: newsroom-import-readiness-review-surface-v1
- prohibited_next_artifacts:
  - production .ymmp
  - render output
  - TTS output
  - real media

## Review Card

Review Card: none. This checker validates the tiny importable artifact without asking for repeated timing, caption copy, blocker, neutral timeline, CSV, script, YMM4-adjacent proof, YMM4, TTS, media, render, or production review.

## Boundary

This readback is diagnostic-only and tool-adjacent. It creates only a tiny script CSV plus proof metadata. It does not create `.ymmp`, YMM4 carriers, renders, TTS/audio, real packet ingestion, external fetches, real source access, media files, production approvals, rights approvals, public-use approvals, or publishing output.
