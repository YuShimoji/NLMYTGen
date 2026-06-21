# Newsroom Episode Production Capsule v1

artifact_id: newsroom_episode_production_capsule_v1_2026_06_22
schema_version: newsroom_episode_production_capsule.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
diagnostic_only: true

## Purpose

This capsule is the first diagnostic bridge from the adapted fake newsroom packet toward one video structure. It organizes ScriptIR-like beats, VisualIR concepts, G-28 slot hints, caption reserve state, provisional timing, and transfer blockers without accepting production, public, or YMM4 readiness.

## Episode Capsule Summary

- episode_id: episode_fake_nlmytgen_delta_v1
- title: Fake upstream export delta for NLMYTGen
- source: synthetic/adapted packet
- script_beats: 2
- visual_units: 2
- total_approx_duration_seconds: 68
- transfer_status: blocked
- blocker_count: 13
- unlock_requirement_count: 13

## Video Readiness Matrix

| area | status | note |
|---|---|---|
| script structure | diagnostic_capsule_ready | beats are mapped from adapted packet only |
| visual structure | diagnostic_capsule_ready | visual units remain schematic/template-only |
| caption reserve | mapped_with_unhinted_slot_warnings | semantic reserve exists but slot warnings remain |
| timing | provisional | rough sequence timing only |
| audio/voice | not_started | no TTS, narration, or audio file exists |
| transfer | blocked | YMM4 transfer is false and blockers remain |

## Script Structure

- 1. beat_fake_intro_001: intro (24s; review=fake_only)
  placeholder: Introduce the fake topic and promise a review-safe handoff.
  source_note_refs: none; visual_refs: visual_fake_title_card_001
- 2. beat_fake_claim_001: claim (44s; review=hold_for_review)
  placeholder: Present a fake claim with fake primary and fake critical source coverage.
  source_note_refs: source_fake_primary_001, source_fake_critical_001; visual_refs: visual_fake_evidence_card_001

## Visual Structure

- visual_fake_title_card_001: title_card / title_card (slots=caption_reserve; unhinted=lower_third_telop)
  caption_reserve: present; warning: Schematic/template-only visual; no screenshot, footage, or approved media is included.
- visual_fake_evidence_card_001: article_quote_card / article_quote_card (slots=source_note; unhinted=caption_reserve, quote_card)
  caption_reserve: present; warning: Schematic/template-only visual; no screenshot, footage, or approved media is included.

## Transfer And Review Debt

validator_status: passed
slot_linkage_status: passed_with_warnings
transfer_planning_status: blocked
transfer_status: blocked

Remaining gaps before importable proof:
- rights and provenance are not cleared
- approved source media or approved abstract replacements are absent
- human review and production approval are absent
- audio voice, TTS, and narration timing are not started
- caption timing is only provisionally reserved
- YMM4 transfer remains blocked
- visual G-28 slot warnings remain before transfer-candidate review
- 13 unlock requirements remain open

Prohibited steps:
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
- Review Console episode preview
- caption/timing refinement
- YMM4 transfer candidate proof only after blockers are resolved

## Boundary

This readback is diagnostic-only. It does not create `.ymmp`, YMM4 carriers, renders, TTS/audio, external fetches, real source access, media downloads, production approvals, rights approvals, public-use approvals, or publishing output.
