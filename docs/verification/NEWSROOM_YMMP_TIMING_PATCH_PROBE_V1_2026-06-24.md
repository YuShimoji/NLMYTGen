# Newsroom YMM4 Timing Patch Probe v1

artifact_id: newsroom_ymmp_timing_patch_probe_v1_2026_06_24
probe_id: newsroom_ymmp_timing_patch_probe_v1_2026_06_24
schema_version: newsroom_ymmp_timing_patch_probe.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
probe_status: applied_to_ignored_local_copy_after_validation
readback_id: newsroom_ymmp_timing_patch_probe_readback_v1_2026_06_24
readback_status: structural_pass
diagnostic_only: true


## Source

- probe_id: newsroom_ymmp_timing_patch_probe_v1_2026_06_24
- source_strategy_path: samples/_probe/newsroom_handoff/ymmp_timing_patch_strategy_v1.json
- source_strategy_id: newsroom_ymmp_timing_patch_strategy_v1_2026_06_24
- source_neutral_timeline_path: samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json
- source_neutral_timeline_id: newsroom_neutral_timeline_import_proof_v1_2026_06_22
- source_structure_readback_path: samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json
- source_structure_readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
- source_audio_observation_path: samples/_probe/newsroom_handoff/audio_observation_and_timing_patch_readiness_v1.json
- source_audio_observation_id: newsroom_audio_observation_and_timing_patch_readiness_v1_2026_06_24
- source_native_audio_path_proof_path: samples/_probe/newsroom_handoff/yym4_native_audio_path_proof_v1.json
- source_native_audio_path_proof_id: newsroom_yym4_native_audio_path_proof_v1_2026_06_24
- source_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp
- patched_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- production_status: diagnostic_only

## Source Validation

- status: passed
- strategy_id: newsroom_ymmp_timing_patch_strategy_v1_2026_06_24
- neutral_timeline_id: newsroom_neutral_timeline_import_proof_v1_2026_06_22
- structure_readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
- audio_observation_id: newsroom_audio_observation_and_timing_patch_readiness_v1_2026_06_24
- native_audio_path_proof_id: newsroom_yym4_native_audio_path_proof_v1_2026_06_24
- canonical_speaker: ゆっくり霊夢
- canonical_speaker_unicode_escape: \u3086\u3063\u304f\u308a\u970a\u5922
- source_fps: 60
- source_total_frames: 509
- target_total_frames: 4080
- source_voice_item_count: 4
- neutral_caption_count: 4
- mapping_method: text_and_order
- errors: []

## Selected Patch Method

- choice: neutral_timeline_skeleton_patch_with_native_voice_preserved
- source_strategy_choice: neutral_timeline_skeleton_patch_with_native_voice_preserved
- strategy_slice: newsroom-ymmp-timing-patch-probe-v1
- why_safe_for_this_probe: ['the four VoiceItem rows match the four neutral caption rows by text and order', 'actual .ymmp timing fields are Frame, Length, and timeline Length', 'speaker, text, VoiceCache, VoiceParameter, Pronounce, Hatsuon, VoiceLength, and AudioEffects are not modified']
- why_diagnostic_only: ['long sparse spans are timing mechanics, not final pacing', 'post-patch render has not been run in this slice', 'visual layout and production narration remain unaccepted']

## Dialogue Mapping

| index | text | source frame/length | target frame/length | method |
|---|---|---|---|---|
| 0 | Fake topic, review only. | 0 / 130 | 0 / 720 | text_and_order |
| 1 | Review-only handoff stays. | 130 / 125 | 720 / 720 | text_and_order |
| 2 | A fake claim is shown. | 255 / 114 | 1440 / 1320 | text_and_order |
| 3 | Fake source checks are noted. | 369 / 140 | 2760 / 1320 | text_and_order |

## Patch Operations

| target | before | after | applied |
|---|---:|---:|---|
| Timelines[0].Length | 509 | 4080 | true |
| Timelines[0].Items[0].Frame | 0 | 0 | true |
| Timelines[0].Items[0].Length | 130 | 720 | true |
| Timelines[0].Items[1].Frame | 130 | 720 | true |
| Timelines[0].Items[1].Length | 125 | 720 | true |
| Timelines[0].Items[2].Frame | 255 | 1440 | true |
| Timelines[0].Items[2].Length | 114 | 1320 | true |
| Timelines[0].Items[3].Frame | 369 | 2760 | true |
| Timelines[0].Items[3].Length | 140 | 1320 | true |

## Patch Application

- patch_method: neutral_timeline_skeleton_patch_with_native_voice_preserved
- operation_count: 9
- operations_applied: true
- timeline_length_operation_applied: true
- voice_item_timing_operations_applied: 8
- fallback_carrier_used: false

## Before / After Timing

- fps: 60
- source_total_frames: 509
- source_total_sec: 8.483333
- patched_total_frames: 4080
- patched_total_sec: 68.0
- target_total_frames: 4080
- target_total_sec: 68
- source_item_timings: [{'voice_index': 0, 'item_index': 0, 'text': 'Fake topic, review only.', 'frame': 0, 'length_frames': 130, 'end_frame': 130, 'start_sec': 0.0, 'duration_sec': 2.166667, 'end_sec': 2.166667, 'voice_length': '00:00:01.8590000'}, {'voice_index': 1, 'item_index': 1, 'text': 'Review-only handoff stays.', 'frame': 130, 'length_frames': 125, 'end_frame': 255, 'start_sec': 2.166667, 'duration_sec': 2.083333, 'end_sec': 4.25, 'voice_length': '00:00:01.7895000'}, {'voice_index': 2, 'item_index': 2, 'text': 'A fake claim is shown.', 'frame': 255, 'length_frames': 114, 'end_frame': 369, 'start_sec': 4.25, 'duration_sec': 1.9, 'end_sec': 6.15, 'voice_length': '00:00:01.5995000'}, {'voice_index': 3, 'item_index': 3, 'text': 'Fake source checks are noted.', 'frame': 369, 'length_frames': 140, 'end_frame': 509, 'start_sec': 6.15, 'duration_sec': 2.333333, 'end_sec': 8.483333, 'voice_length': '00:00:02.0270000'}]
- patched_item_timings: [{'voice_index': 0, 'item_index': 0, 'text': 'Fake topic, review only.', 'frame': 0, 'length_frames': 720, 'end_frame': 720, 'start_sec': 0.0, 'duration_sec': 12.0, 'end_sec': 12.0, 'voice_length': '00:00:01.8590000'}, {'voice_index': 1, 'item_index': 1, 'text': 'Review-only handoff stays.', 'frame': 720, 'length_frames': 720, 'end_frame': 1440, 'start_sec': 12.0, 'duration_sec': 12.0, 'end_sec': 24.0, 'voice_length': '00:00:01.7895000'}, {'voice_index': 2, 'item_index': 2, 'text': 'A fake claim is shown.', 'frame': 1440, 'length_frames': 1320, 'end_frame': 2760, 'start_sec': 24.0, 'duration_sec': 22.0, 'end_sec': 46.0, 'voice_length': '00:00:01.5995000'}, {'voice_index': 3, 'item_index': 3, 'text': 'Fake source checks are noted.', 'frame': 2760, 'length_frames': 1320, 'end_frame': 4080, 'start_sec': 46.0, 'duration_sec': 22.0, 'end_sec': 68.0, 'voice_length': '00:00:02.0270000'}]
- patched_item_end_frames: [720, 1440, 2760, 4080]
- target_68_sec_reached_structurally: true

## Field Preservation Readback

- all_required_fields_preserved: true
- preserved_field_names: ['CharacterName', 'Serif', 'VoiceCache', 'VoiceParameter', 'Pronounce', 'Hatsuon', 'VoiceLength', 'AudioEffects']
- per_item: [{'voice_index': 0, 'item_index': 0, 'text': 'Fake topic, review only.', 'fields': {'CharacterName': True, 'Serif': True, 'VoiceCache': True, 'VoiceParameter': True, 'Pronounce': True, 'Hatsuon': True, 'VoiceLength': True, 'AudioEffects': True}, 'all_required_fields_preserved': True}, {'voice_index': 1, 'item_index': 1, 'text': 'Review-only handoff stays.', 'fields': {'CharacterName': True, 'Serif': True, 'VoiceCache': True, 'VoiceParameter': True, 'Pronounce': True, 'Hatsuon': True, 'VoiceLength': True, 'AudioEffects': True}, 'all_required_fields_preserved': True}, {'voice_index': 2, 'item_index': 2, 'text': 'A fake claim is shown.', 'fields': {'CharacterName': True, 'Serif': True, 'VoiceCache': True, 'VoiceParameter': True, 'Pronounce': True, 'Hatsuon': True, 'VoiceLength': True, 'AudioEffects': True}, 'all_required_fields_preserved': True}, {'voice_index': 3, 'item_index': 3, 'text': 'Fake source checks are noted.', 'fields': {'CharacterName': True, 'Serif': True, 'VoiceCache': True, 'VoiceParameter': True, 'Pronounce': True, 'Hatsuon': True, 'VoiceLength': True, 'AudioEffects': True}, 'all_required_fields_preserved': True}]
- characters_block_preserved: true
- character_voice_apis_preserved: true
- external_TTS_introduced: false
- voice_regenerated: false
- voice_stretched_or_replaced: false
- voice_cache_rewritten: false

## Structural Result

- structural_readback_status: pass
- source_total_frames: 509
- source_total_sec: 8.483333
- patched_total_frames: 4080
- patched_total_sec: 68.0
- target_total_frames: 4080
- target_total_sec: 68
- fps: 60
- patched_voice_item_count: 4
- patched_frames: [0, 720, 1440, 2760]
- patched_lengths: [720, 720, 1320, 1320]
- patched_end_frames: [720, 1440, 2760, 4080]
- target_68_sec_reached_structurally: true
- fallback_carrier_used: false
- render_required_before_video_acceptance: true

## Local File Status

- source_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_v1.ymmp
- source_ymmp_found_at_generation: true
- patched_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- patched_ymmp_created_or_updated_by_generation: true
- patched_copy_under_tmp: true
- expected_git_ignore_rule: _tmp/
- ymmp_committed: false
- ymmp_or_media_staged: false
- media_output_created: false

## Render Gate

- render_performed_in_this_slice: false
- YMM4_launched_by_agent: false
- render_deferred_until_structural_readback_passes: true
- next_render_trigger: patched copy structurally reaches 68 sec and preserves native voice fields
- next_recommended_slice: newsroom-ymmp-timing-patch-render-smoke-v1
- repeated_audio_check_requested: false

## Not Accepted Scope

- production_render_readiness: false
- public_video_readiness: false
- production_narration_quality: false
- final_script_narration_quality: false
- visual_layout_readiness: false
- real_content_readiness: false
- production_approval: false
- external_TTS_adoption: false
- post_patch_render_smoke: false
- neutral_68_sec_video_acceptance: false

## Boundaries

- YMM4_launched_by_agent: false
- render_created_by_agent: false
- audio_generated_by_agent: false
- TTS_generated_by_agent: false
- real_media_imported: false
- external_fetch_performed: false
- source_ymmp_modified: false
- patched_ymmp_copy_created_under_ignored_tmp: true
- ymmp_or_media_staged_or_committed: false
- production_approval: false
- public_video_ready: false
- dashboard_governance_freshness_changed: false

## Boundary Note

The patched `.ymmp` is an ignored local diagnostic copy only. This probe changes timeline length plus VoiceItem Frame/Length fields, preserves speaker/text/native voice fields, and keeps render deferred to the next milestone.
