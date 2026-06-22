# Newsroom Script Import Candidate v1

artifact_id: newsroom_script_import_candidate_v1_2026_06_22
script_candidate_id: newsroom_script_import_candidate_v1_2026_06_22
schema_version: newsroom_script_import_candidate.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
import_status: candidate_with_placeholders
script_import_status: passed
diagnostic_only: true

## Source

- source_csv_path: samples/_probe/newsroom_handoff/caption_import_candidate_v1.csv
- source_neutral_timeline_path: samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json
- source_caption_csv_readback_path: samples/_probe/newsroom_handoff/caption_csv_import_candidate_readback_v1.json
- source_episode_id: episode_fake_nlmytgen_delta_v1
- source_commit_or_status: worktree_verified_before_generation

## Review Memory

- prior_user_review_count: 0
- current_axis: script_import_candidate_schema
- repeated_general_review_allowed: false

## Script Import Candidate Summary

- script_lines_array_present: true
- line_count: 4
- expected_line_count: 4
- required_line_fields_present: true
- speaker_assignment_policy: single_synthetic_placeholder
- voice_profile_policy: placeholder_not_generated_no_tts

## CSV-to-Script Mapping Summary

- every_line_maps_exactly_one_csv_caption_row: true
- every_csv_row_mapped: true
- source_caption_ids_are_unique: true
- timing_matches: true
- text_matches: true
- missing_csv_caption_rows: none
- extra_script_lines: none

## Script Lines

| line_id | source_caption_id | beat_id | timing | speaker | voice | flags |
|---|---|---|---|---|---|---|
| line_01_cap_beat_fake_intro_001_01 | cap_beat_fake_intro_001_01 | beat_fake_intro_001 | 0-12s | synthetic_newsroom_placeholder | voice_status=placeholder_not_generated | diagnostic_only=true, production_ready=false, tts_ready=false |
| line_02_cap_beat_fake_intro_001_02 | cap_beat_fake_intro_001_02 | beat_fake_intro_001 | 12-24s | synthetic_newsroom_placeholder | voice_status=placeholder_not_generated | diagnostic_only=true, production_ready=false, tts_ready=false |
| line_03_cap_beat_fake_claim_001_01 | cap_beat_fake_claim_001_01 | beat_fake_claim_001 | 24-46s | synthetic_newsroom_placeholder | voice_status=placeholder_not_generated | diagnostic_only=true, production_ready=false, tts_ready=false |
| line_04_cap_beat_fake_claim_001_02 | cap_beat_fake_claim_001_02 | beat_fake_claim_001 | 46-68s | synthetic_newsroom_placeholder | voice_status=placeholder_not_generated | diagnostic_only=true, production_ready=false, tts_ready=false |

## Line Validation

- line_count: 4
- expected_line_count: 4
- all_lines_valid: true
- all_lines_diagnostic_only: true
- all_lines_production_not_ready: true
- all_lines_tts_not_ready: true

## Diagnostic Safety

- real_urls: false
- real_media_paths: false
- TTS_generated: false
- render_created: false
- ymmp_created: false
- production_approval: false

## Next Use

- script_import_status: passed
- allowed_next_artifacts:
  - YMM4-adjacent no-media proof
  - script import mapping proof
  - tiny importable proof after another gate
- prohibited_next_artifacts:
  - production .ymmp
  - render output
  - TTS output
  - real media

## Review Card

Review Card: none. This checker validates the script import candidate without asking for repeated timing, caption copy, blocker, neutral timeline, YMM4, TTS, media, or production review.

## Boundary

This readback is diagnostic-only. It does not create `.ymmp`, YMM4 carriers, renders, TTS/audio, real packet ingestion, external fetches, real source access, media files, production approvals, rights approvals, public-use approvals, or publishing output.
