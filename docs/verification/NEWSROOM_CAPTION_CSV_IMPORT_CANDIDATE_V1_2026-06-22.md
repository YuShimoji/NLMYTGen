# Newsroom Caption CSV Import Candidate v1

artifact_id: newsroom_caption_csv_import_candidate_v1_2026_06_22
schema_version: newsroom_caption_csv_import_candidate.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
caption_csv_import_status: passed
diagnostic_only: true

## Source

- source_csv_path: samples/_probe/newsroom_handoff/caption_import_candidate_v1.csv
- source_neutral_timeline_path: samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json
- source_episode_id: episode_fake_nlmytgen_delta_v1
- source_commit_or_status: worktree_verified_before_generation

## Review Memory

- prior_user_review_count: 0
- current_axis: caption_csv_import_candidate_schema
- repeated_general_review_allowed: false

## Schema

- required_columns_present: true
- column_order_matches_required: true
- required_YMM4_columns: none
- extra_columns_blocking: false

## Row Validation

- row_count: 4
- expected_row_count: 4
- all_rows_valid: true

| caption_id | beat_id | timing | flags |
|---|---|---|---|
| cap_beat_fake_intro_001_01 | beat_fake_intro_001 | 0.0-12.0s | diagnostic_only=true, production_ready=false |
| cap_beat_fake_intro_001_02 | beat_fake_intro_001 | 12.0-24.0s | diagnostic_only=true, production_ready=false |
| cap_beat_fake_claim_001_01 | beat_fake_claim_001 | 24.0-46.0s | diagnostic_only=true, production_ready=false |
| cap_beat_fake_claim_001_02 | beat_fake_claim_001 | 46.0-68.0s | diagnostic_only=true, production_ready=false |

## Neutral Timeline Consistency

- every_csv_caption_id_exists: true
- timing_matches: true
- text_matches: true
- missing_caption_rows: none
- extra_caption_rows: none

## Diagnostic Safety

- real_urls: false
- real_media_paths: false
- TTS_generated: false
- render_created: false
- ymmp_created: false
- production_approval: false

## Next Use

- recommended_next_slice: newsroom-script-import-candidate-v1
- allowed_next_artifacts:
  - script import candidate
  - neutral timeline consumer proof
  - YMM4-adjacent no-media proof
- prohibited_next_artifacts:
  - production .ymmp
  - render output
  - TTS output
  - real media

## Review Card

Review Card: none. This checker validates the caption CSV import candidate schema without asking for repeated timing, caption, copy, blocker, or neutral timeline review.

## Boundary

This readback is diagnostic-only and caption-only. It does not create `.ymmp`, YMM4 carriers, renders, TTS/audio, real packet ingestion, external fetches, real source access, media files, production approvals, rights approvals, public-use approvals, or publishing output.
