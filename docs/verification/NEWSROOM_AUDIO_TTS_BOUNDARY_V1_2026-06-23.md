# Newsroom Audio / TTS Boundary v1

artifact_id: newsroom_audio_tts_boundary_v1_2026_06_23
boundary_id: newsroom_audio_tts_boundary_v1_2026_06_23
schema_version: newsroom_audio_tts_boundary.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
boundary_status: accepted_for_next_audio_observation
diagnostic_only: true

## Source

- source_render_smoke_result_path: samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json
- source_render_smoke_result_id: newsroom_tiny_render_smoke_result_readback_v1_2026_06_23
- source_ymmp_structure_readback_path: samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json
- source_ymmp_structure_readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
- source_timing_strategy_path: samples/_probe/newsroom_handoff/yym4_timing_gap_strategy_v1.json
- source_timing_strategy_id: newsroom_yym4_timing_gap_strategy_v1_2026_06_23

## Source Validation

- status: passed
- errors: []
- canonical_speaker_value: ゆっくり霊夢

## Known Render Result

- tiny_render_smoke_result: pass
- output_video_observed: true
- approximate_duration_sec: 8
- four_dialogue_lines_visible: true
- timing_mode: YMM4 natural duration
- neutral_68_sec_timing_patch_applied: false
- render_output_path_if_known: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.mp4
- render_output_committed: false
- render_output_staged: false

## Known / Unknown Audio State

- VoiceCache_or_voice_fields_present_in_ymmp: true
- voice_audio_related_fields_present: ['VoiceLength', 'VoiceCache', 'VoiceParameter', 'Pronounce', 'Hatsuon', 'AudioEffects']
- voice_item_count: 4
- voice_cache_item_count: 4
- character_voice_apis: ['AquesTalk']
- TTS_generated_by_agent: false
- explicit_operator_TTS_generation: false
- audio_presence_in_render: unknown
- audio_quality_accepted: false
- TTS_ready: false
- voice_binding_ready: partial
- speaker_binding_status: ゆっくり霊夢 accepted for diagnostic import
- speaker_unicode_escape: \u3086\u3063\u304f\u308a\u970a\u5922
- known_unknown_note: Render success and VoiceCache presence do not establish audio presence or audio quality in the output.

## Responsibility Split

| path | role | enables | defers | main risk |
|---|---|---|---|---|
| yym4_native_voice_audio_path | recommended_next_diagnostic_path | small audio presence observation; native voice path proof | external TTS integration; production voice readiness | audio presence in the current render is not yet observed; VoiceCache presence can be overread as audio quality |
| external_tts_path | closed_for_now | future external narration experiments; future voice replacement design | current diagnostic render follow-through; neutral timing patch strategy | adds timing drift before the native path is understood; adds credential/tooling and file-retention questions |
| metadata_only_voice_profile_path | planning_only | voice profile bookkeeping; future path comparison | audio presence proof; TTS quality acceptance | does not prove audible output; can be mistaken for voice readiness |
| no_audio_diagnostic_render_path | fallback_if_audio_remains_unneeded | continued non-audio diagnostic render checks; retention-policy decisions for silent outputs | voice readiness; production render readiness | not representative of a public video; cannot validate voice timing or speaker quality |

## Recommended Default

- choice: keep_yym4_native_voice_audio_path_for_next_diagnostic
- reasoning:
  - The current .ymmp already records YMM4 voice fields and VoiceCache.
  - The tiny render smoke proves diagnostic render viability, not audio quality.
  - External TTS would add a second timing and integration variable too early.
  - Audio/TTS choice should be understood before neutral 68 second timing patch work.
- do_now:
  - keep YMM4 native voice/audio path as the next diagnostic path
  - record audio presence in render as unknown until a small observation is needed
  - keep external TTS closed
- defer:
  - external TTS generation
  - audio quality acceptance
  - production voice readiness
  - neutral 68 second timing patch

## Operator Observation Card If Needed

- status: proposed_if_needed
- target: tiny render audio presence observation
- why: Audio presence in the render is unknown; use only if audio becomes the next bottleneck.
- action: Play the existing diagnostic tiny render and answer in freeform.
- answer_style: freeform
- look_for:
  - whether any audio is present
  - whether the voice sounds like the expected YMM4 speaker
  - whether there is obvious silence, cutoff, or mismatch
- not_needed:
  - fixed form
  - production quality review
  - timing patch
  - new render
  - external TTS

## Timing Interaction

- first_render_smoke_used_natural_duration: true
- first_smoke_duration_sec: 8
- first_smoke_duration_qualifier: approx
- prior_ymmp_natural_duration_sec: 8.483333
- neutral_68_sec_timing_patch_remains_deferred: true
- audio_tts_choice_may_affect_timing_duration: true
- do_not_patch_timing_before_audio_tts_boundary_understood: true
- timing_patch_applied: false

## Next Recommended Slices

- if_audio_presence_is_sufficient_from_existing_evidence: newsroom-ymmp-timing-patch-strategy-v1
- if_audio_presence_is_unknown_and_needed: newsroom-tiny-render-audio-observation-card-v1
- if_audio_path_should_be_defined_first: newsroom-yym4-native-audio-path-proof-v1
- do_not_recommend: production_render_immediately

## Boundary Status

- render_created_by_agent: false
- audio_generated_by_agent: false
- TTS_generated_by_agent: false
- real_media_imported: false
- production_approval: false
- public_video_ready: false
- output_retention_required_now: false
- dashboard_governance_freshness_changed: false

## Human Burden Hygiene

- user_input: freeform
- template_required: false
- schema_owner: Agent
- user_side_work_this_slice: none
- future_observation_max_required_points: 3
- screenshot_optional: true
- negative_confirmations_required_from_user: false
- fixed_form_result_template: false

## Review Memory

- prior_user_review_count: {'manual_import_behavior': 1, 'bound_speaker_behavior': 1, 'diagnostic_ymmp_manual_observation': 1, 'ymmp_structure_readback': 1, 'timing_gap_strategy': 1, 'tiny_render_smoke_boundary': 1, 'tiny_render_smoke_result': 1, 'audio_tts_boundary': 0}
- next_nonredundant_axis: ['newsroom-tiny-render-audio-observation-card-v1', 'newsroom-yym4-native-audio-path-proof-v1', 'newsroom-ymmp-timing-patch-strategy-v1']
- repeated_general_review_allowed: false

## Boundary Note

This boundary defines audio/TTS responsibility only. It does not launch YMM4, render, generate audio/TTS, import real media, patch or commit `.ymmp`, approve production, prepare public video, or change dashboard/governance/freshness work.
