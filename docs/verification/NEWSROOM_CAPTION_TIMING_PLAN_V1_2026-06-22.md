# Newsroom Caption / Timing Plan v1

artifact_id: newsroom_caption_timing_plan_v1_2026_06_22
schema_version: newsroom_caption_timing_plan.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_timing_plan_only
diagnostic_only: true

## Purpose

This plan refines the diagnostic episode capsule into a caption and timing planning layer. It keeps transfer blocked and does not create audio, media, YMM4 projects, renders, or production-ready video output.

## Episode Timing Summary

- episode_id: episode_fake_nlmytgen_delta_v1
- total_duration_sec: 68
- covered_range_sec: 68
- beat_count: 2
- caption_unit_count: 4
- visual_count: 2
- timing_confidence: low_provisional_from_capsule

## Video Readiness Matrix

| area | status | note |
|---|---|---|
| timing | provisional | capsule rough durations only |
| captions | placeholder_plan | copy and reading speed need review |
| visuals | mapped_to_beats | schematic VisualIR / G-28 references only |
| audio | not_started | no TTS or audio timing exists |
| transfer | blocked | YMM4_candidate=false |

## Beat Timing

- beat_fake_intro_001: 0-24s (24s)
  captions: cap_beat_fake_intro_001_01, cap_beat_fake_intro_001_02
  visuals: visual_fake_title_card_001
  sources: none
- beat_fake_claim_001: 24-68s (44s)
  captions: cap_beat_fake_claim_001_01, cap_beat_fake_claim_001_02
  visuals: visual_fake_evidence_card_001
  sources: source_fake_primary_001, source_fake_critical_001

## Caption Units

- cap_beat_fake_intro_001_01: 0-12s beat=beat_fake_intro_001 max_chars=34 lines=2
  placeholder: Introduce the fake topic.
  reserve: present_semantic_only
- cap_beat_fake_intro_001_02: 12-24s beat=beat_fake_intro_001 max_chars=34 lines=2
  placeholder: Promise a review-safe handoff.
  reserve: present_semantic_only
- cap_beat_fake_claim_001_01: 24-46s beat=beat_fake_claim_001 max_chars=34 lines=2
  placeholder: Present a fake claim.
  reserve: present_semantic_only
- cap_beat_fake_claim_001_02: 46-68s beat=beat_fake_claim_001 max_chars=34 lines=2
  placeholder: Fake primary and fake critical source coverage.
  reserve: present_semantic_only

## Visual Timing

- visual_fake_title_card_001: 0-24s beat=beat_fake_intro_001 slot=caption_reserve
  layout=title_card; caption risk=low_semantic_reserve_present
  review_surface_ref: samples/_probe/g28/reference_layout_prototypes/object_catalog.html
- visual_fake_evidence_card_001: 24-68s beat=beat_fake_claim_001 slot=source_note
  layout=article_quote_card; caption risk=medium_unhinted_caption_reserve
  review_surface_ref: samples/_probe/g28/reference_layout_prototypes/article_quote_card.html

## Transfer And Boundary

transfer_status: blocked
YMM4_candidate: false
TTS_generated: false

Prohibited next actions:
- real source fetch
- .ymmp generation
- YMM4 carrier generation
- render generation
- production approval
- publishing
- RSS/Inoreader operation
- real URL access
- media download
- external fetch
- rights approval
- public-use approval

Next allowed steps:
- Review Console timing panel or preview extension
- YMM4 transfer candidate proof only after blockers are resolved
- caption copy refinement
- synthetic voice placeholder planning without TTS generation

## Remaining Gaps

- rights and provenance are not cleared
- approved source media or approved abstract replacements are absent
- human review and production approval are absent
- audio voice, TTS, and narration timing are not started
- caption timing is only provisionally reserved
- YMM4 transfer remains blocked
- visual G-28 slot warnings remain before transfer-candidate review
- 13 unlock requirements remain open

## Boundary

This readback is diagnostic-only. It is a timing/caption planning layer, not public video, not an importable proof, and not a production approval.
