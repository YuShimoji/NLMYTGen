# Newsroom YMM4 Timing Gap Strategy v1

artifact_id: newsroom_yym4_timing_gap_strategy_v1_2026_06_23
strategy_id: newsroom_yym4_timing_gap_strategy_v1_2026_06_23
schema_version: newsroom_yym4_timing_gap_strategy.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
strategy_status: accepted_for_next_tiny_render_smoke
diagnostic_only: true

## Source

- source_structure_readback_path: samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json
- source_structure_readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
- source_manual_result_readback_path: samples/_probe/newsroom_handoff/diagnostic_ymmp_manual_result_readback_v1.json
- source_manual_result_id: newsroom_diagnostic_ymmp_manual_result_readback_v1_2026_06_23

## Source Validation

- status: passed
- errors: []
- canonical_speaker_value: ゆっくり霊夢
- canonical_speaker_unicode_escape: \u3086\u3063\u304f\u308a\u970a\u5922
- accepted_speaker_value_must_not_equal_mojibake: true

## Timing Facts

- neutral_timeline_total_sec: 68
- ymmp_fps: 60
- ymmp_total_frames: 509
- ymmp_total_duration_sec: 8.483333
- timing_gap_sec: 59.516667
- timing_imported_by_csv: false
- timing_patch_applied: false
- item_frames: [0, 130, 255, 369]
- item_lengths: [130, 125, 114, 140]

## Strategy Options

| option | role | enables | defers | main risk |
|---|---|---|---|---|
| accept_yym4_natural_duration_for_first_smoke | viable_but_too_short_as_final_strategy | first tiny render smoke boundary; tool-chain viability check | neutral 68 second timing proof; audio/narration alignment | can be mistaken for production timing if not fenced; does not test the 68 second neutral pacing plan |
| patch_ymmp_to_neutral_68s_before_render | deferred_not_default | neutral duration patch planning; later production-like timing proof | smallest render smoke isolation; current diagnostic natural-duration proof reuse | mixes timing patch behavior with first render smoke; requires a separate .ymmp patch boundary before evidence exists |
| hybrid_natural_first_then_patch_later | recommended_default | newsroom-tiny-render-smoke-boundary-v1; newsroom-ymmp-timing-patch-strategy-v1 | 68 second .ymmp patch in this slice; TTS readiness claims; production approval | requires two evidence steps instead of one; natural timing must stay clearly marked diagnostic-only |
| keep_timing_external_until_render_path | too_passive_after_structure_readback | docs-only planning; future timing comparison | tiny render smoke boundary; timing patch strategy | does not reduce the render smoke decision bottleneck; can leave natural versus neutral timing unresolved too long |

## Recommended Default

- choice: hybrid_natural_first_then_patch_later
- next_recommended_slice: newsroom-tiny-render-smoke-boundary-v1
- after_that: newsroom-ymmp-timing-patch-strategy-v1
- reasoning:
  - The first tiny render smoke should isolate YMM4/render tool-chain viability.
  - Timing patch mechanics should not be mixed with the first render proof.
  - The neutral 68 second metadata remains valid as production-like planning data.
  - The saved YMM4 natural duration is valid only for diagnostic smoke evidence.
- what_it_enables_next:
  - prepare a tiny render smoke boundary using the saved natural duration
  - defer neutral-timing stretch into a separate patch strategy
  - keep audio/TTS readiness outside the render smoke decision
- what_it_defers:
  - production-like 68 second .ymmp timing
  - audio and narration timing alignment
  - public video readiness

## Next Path

- if_hybrid_chosen: newsroom-tiny-render-smoke-boundary-v1 -> newsroom-ymmp-timing-patch-strategy-v1
- if_timing_patch_first_chosen: newsroom-ymmp-timing-patch-planning-v1
- if_blocked_missing_evidence: []

## Boundary

- ymmp_patched_in_this_slice: false
- ymmp_created_in_this_slice: false
- ymmp_staged_or_committed: false
- ymmp_committed: false
- agent_launched_yym4: false
- render_created: false
- TTS_generated: false
- real_media_imported: false
- external_fetch_performed: false
- real_newsroom_ingest_performed: false
- dashboard_governance_freshness_changed: false
- production_approval: false
- public_video_ready: false

## Human Burden Hygiene

- user_input: freeform
- template_required: false
- schema_owner: Agent
- max_required_points: 0
- screenshot_optional: true
- negative_confirmations_required_from_user: false
- fixed_form_result_template: false
- operator_observation_card: none
- user_side_work_this_slice: none

## Review Memory

- prior_user_review_count: {'manual_import_behavior': 1, 'bound_speaker_behavior': 1, 'diagnostic_ymmp_manual_observation': 1, 'ymmp_structure_readback': 1, 'timing_gap_strategy': 0}
- next_nonredundant_axis: ['newsroom-tiny-render-smoke-boundary-v1', 'newsroom-ymmp-timing-patch-strategy-v1', 'newsroom-audio-tts-boundary-v1']
- repeated_general_review_allowed: false

## Boundary Note

This strategy records a diagnostic timing decision only. It does not patch `.ymmp`, stage or commit `.ymmp`, launch YMM4, render, generate TTS/audio, import real media, approve production, or prepare a public video.
