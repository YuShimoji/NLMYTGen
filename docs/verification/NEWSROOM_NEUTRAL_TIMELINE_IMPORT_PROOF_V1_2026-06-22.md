# Newsroom Neutral Timeline Import Proof v1

timeline_id: newsroom_neutral_timeline_import_proof_v1_2026_06_22
schema_version: newsroom_neutral_timeline_import_proof.v1
review_status: ready_for_supervisor_review
source_episode_id: episode_fake_nlmytgen_delta_v1
production_status: diagnostic_only
import_status: diagnostic_candidate_with_placeholders
diagnostic_only: true

## Purpose

This artifact is the neutral, synthetic import-shaped timeline for the diagnostic newsroom episode. It is the source of truth for the optional caption CSV and keeps production/YMM4 transfer closed.

## Timing

- total_duration_sec: 68
- timebase: seconds
- fps_policy: not_required_for_neutral_timeline
- timing_confidence: provisional

## Track Summary

| track_id | track_kind | production_ready |
|---|---|---|
| track_captions_main | captions | false |
| track_visual_placeholders | visuals | false |
| track_markers | markers | false |
| track_audio_placeholder | audio_placeholder | false |

## Item Summary

| item_kind | count | diagnostic_import_allowed |
|---|---:|---|
| caption | 4 | true |
| visual_placeholder | 2 | true |
| marker | 2 | true |
| audio_placeholder | 1 | true |

## Caption Items

- cap_beat_fake_intro_001_01: 0-12s beat=beat_fake_intro_001 density=medium
  text: Fake topic, review only.
- cap_beat_fake_intro_001_02: 12-24s beat=beat_fake_intro_001 density=medium
  text: Review-only handoff stays.
- cap_beat_fake_claim_001_01: 24-46s beat=beat_fake_claim_001 density=low
  text: A fake claim is shown.
- cap_beat_fake_claim_001_02: 46-68s beat=beat_fake_claim_001 density=low
  text: Fake source checks are noted.

## Visual Placeholder Items

- visual_fake_title_card_001: 0-24s slot=caption_reserve layout=title_card
  caption_interference_note: low_semantic_reserve_present
  media_file_dependency: none
- visual_fake_evidence_card_001: 24-68s slot=source_note layout=article_quote_card
  caption_interference_note: medium_unhinted_caption_reserve
  media_file_dependency: none

## Audio Placeholder

- item_audio_placeholder_not_started: voice_status=not_started; TTS_generated=false; audio_required_for_this_proof=false

## Caption CSV

- status: created
- path: samples/_probe/newsroom_handoff/caption_import_candidate_v1.csv
- derived_from: items where item_kind=caption
- row_count: 4

## Blocker Carry-Forward

- production_transfer_status: blocked
- diagnostic_import_status: candidate_with_placeholders
- YMM4_candidate: false
- production_approval: false

## Next Mapping Policy

- recommended_next_slice: newsroom-caption-csv-import-candidate-v1
- allowed_next_artifacts:
  - neutral timeline JSON
  - caption CSV
  - script-import candidate
- prohibited_next_artifacts:
  - production .ymmp
  - render output
  - TTS output
  - real media
  - real packet ingest
  - external fetch

## Review Card

Review Card: none. This slice validates the neutral timeline import schema and does not ask for repeated timing, caption, copy, or blocker review.

## Boundary

neutral_timeline_json_is_source_of_truth: true
caption_csv_derived_from_json: true

This proof does not create `.ymmp`, YMM4 carriers, renders, TTS/audio, real packet ingestion, external fetches, real source access, media files, production approvals, rights approvals, public-use approvals, or publishing output.
