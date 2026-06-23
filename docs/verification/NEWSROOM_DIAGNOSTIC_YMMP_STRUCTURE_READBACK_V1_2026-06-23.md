# Newsroom Diagnostic .ymmp Structure Readback v1

artifact_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
schema_version: newsroom_diagnostic_ymmp_structure_readback.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
ymmp_committed: false
diagnostic_only: true

## Source

- source_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp
- source_manual_result_readback_path: samples/_probe/newsroom_handoff/diagnostic_ymmp_manual_result_readback_v1.json

## Parse Status

- ymmp_found: true
- parse_status: parsed
- parse_method: python json utf-8-sig bounded structure read
- warnings: []

## Dialogue Structure

- dialogue_item_count: 4
- expected_dialogue_item_count: 4
- canonical_speaker_value: 繧・▲縺上ｊ髴雁､｢
- speaker_value_ui_observed: 繧・▲縺上ｊ髴雁､｢
- accepted_speaker_source: ['user_freeform_observation', 'supervisor_screenshot', 'bound_speaker_csv_observation']
- accepted_speaker_value_must_not_equal_mojibake: true
- raw_speaker_values: ['ゆっくり霊夢']
- raw_character_name_if_detected: ['ゆっくり霊夢']
- raw_character_name_decoding_status: decoded
- encoding_note: Raw .ymmp CharacterName values are recorded separately. Terminal or parser display mojibake must not be promoted into accepted canonical speaker fields.
- item_type_names: ['YukkuriMovieMaker.Project.Items.VoiceItem, YukkuriMovieMaker']
- items:
  - index=0 frame=0.0 length=130.0 text='Fake topic, review only.'
  - index=1 frame=130.0 length=125.0 text='Review-only handoff stays.'
  - index=2 frame=255.0 length=114.0 text='A fake claim is shown.'
  - index=3 frame=369.0 length=140.0 text='Fake source checks are noted.'

## Timing Structure

- observed_project_duration_sec: 8.483333
- observed_project_duration_frames: 509.0
- fps: 60.0
- item_start_duration_fields: ['Frame', 'Length', 'VoiceLength']
- item_timings: [{'index': 0, 'frame': 0.0, 'length_frames': 130.0, 'start_sec': 0.0, 'duration_sec': 2.166667, 'voice_length': '00:00:01.8590000'}, {'index': 1, 'frame': 130.0, 'length_frames': 125.0, 'start_sec': 2.166667, 'duration_sec': 2.083333, 'voice_length': '00:00:01.7895000'}, {'index': 2, 'frame': 255.0, 'length_frames': 114.0, 'start_sec': 4.25, 'duration_sec': 1.9, 'voice_length': '00:00:01.5995000'}, {'index': 3, 'frame': 369.0, 'length_frames': 140.0, 'start_sec': 6.15, 'duration_sec': 2.333333, 'voice_length': '00:00:02.0270000'}]
- timing_gap_status: unresolved
- neutral_timeline_total_sec: 68
- prior_observed_yym4_import_approx_sec: 8.48
- ymmp_natural_duration_observed: short_natural_duration
- timing_patch_applied: false

## Audio / TTS Structure

- voice_audio_related_fields_present: ['VoiceLength', 'VoiceCache', 'VoiceParameter', 'Pronounce', 'Hatsuon', 'AudioEffects']
- voice_item_count: 4
- voice_cache_item_count: 4
- audio_effect_total_count: 0
- character_voice_apis: ['AquesTalk']
- TTS_generated_by_agent: false
- explicit_operator_TTS_generation: false
- TTS_ready: false
- audio_boundary_note: Voice cache/voice fields are present in the saved diagnostic .ymmp, but this does not establish TTS readiness.

## Not Accepted Scope

- production_ymmp_ready: false
- render_readiness: false
- TTS_readiness: false
- timing_patch_strategy: false
- public_video_readiness: false

## Boundary

- render_created: false
- real_media_imported: false
- production_approval: false
- public_video_ready: false
- ymmp_staged_or_committed: false
- agent_launched_yym4: false
- agent_created_or_edited_ymmp: false
- TTS_generated_by_agent: false
- external_fetch_performed: false

## Human Burden Hygiene

- user_input: freeform
- template_required: false
- schema_owner: Agent
- max_required_points: 0
- screenshot_optional: true
- negative_confirmations_required_from_user: false
- fixed_form_result_template: false
- user_side_work_this_slice: none

## Next Recommended Axes

- newsroom-yym4-timing-gap-strategy-v1
- newsroom-audio-tts-boundary-v1
- newsroom-tiny-render-smoke-boundary-v1

## Boundary Note

This readback parses a local diagnostic `.ymmp` for structure only. It does not stage or commit `.ymmp`, launch YMM4, render, generate TTS/audio, import real media, approve production, or prepare a public video.
