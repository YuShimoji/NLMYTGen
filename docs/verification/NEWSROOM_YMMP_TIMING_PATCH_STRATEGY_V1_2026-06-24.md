# Newsroom YMM4 Timing Patch Strategy v1

artifact_id: newsroom_ymmp_timing_patch_strategy_v1_2026_06_24
strategy_id: newsroom_ymmp_timing_patch_strategy_v1_2026_06_24
schema_version: newsroom_ymmp_timing_patch_strategy.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
strategy_status: recommended_for_probe
diagnostic_only: true


## Source

- strategy_id: newsroom_ymmp_timing_patch_strategy_v1_2026_06_24
- source_audio_observation_readback_path: samples/_probe/newsroom_handoff/audio_observation_and_timing_patch_readiness_v1.json
- source_audio_observation_readback_id: newsroom_audio_observation_and_timing_patch_readiness_v1_2026_06_24
- source_native_audio_path_proof_path: samples/_probe/newsroom_handoff/yym4_native_audio_path_proof_v1.json
- source_native_audio_path_proof_id: newsroom_yym4_native_audio_path_proof_v1_2026_06_24
- source_tiny_render_result_path: samples/_probe/newsroom_handoff/tiny_render_smoke_result_readback_v1.json
- source_tiny_render_result_id: newsroom_tiny_render_smoke_result_readback_v1_2026_06_23
- source_ymmp_structure_readback_path: samples/_probe/newsroom_handoff/diagnostic_ymmp_structure_readback_v1.json
- source_ymmp_structure_readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
- source_neutral_timeline_path: samples/_probe/newsroom_handoff/neutral_timeline_import_proof_v1.json
- source_neutral_timeline_id: newsroom_neutral_timeline_import_proof_v1_2026_06_22
- source_prior_timing_gap_strategy_path: samples/_probe/newsroom_handoff/yym4_timing_gap_strategy_v1.json
- source_prior_timing_gap_strategy_id: newsroom_yym4_timing_gap_strategy_v1_2026_06_23
- production_status: diagnostic_only
- strategy_status: recommended_for_probe

## Source Validation

- status: passed
- audio_observation_readback_id: newsroom_audio_observation_and_timing_patch_readiness_v1_2026_06_24
- native_audio_path_proof_id: newsroom_yym4_native_audio_path_proof_v1_2026_06_24
- tiny_render_result_id: newsroom_tiny_render_smoke_result_readback_v1_2026_06_23
- ymmp_structure_readback_id: newsroom_diagnostic_ymmp_structure_readback_v1_2026_06_23
- neutral_timeline_id: newsroom_neutral_timeline_import_proof_v1_2026_06_22
- prior_timing_gap_strategy_id: newsroom_yym4_timing_gap_strategy_v1_2026_06_23
- canonical_speaker: ゆっくり霊夢
- canonical_speaker_unicode_escape: \u3086\u3063\u304f\u308a\u970a\u5922
- tiny_render_duration_sec: 8
- natural_duration_frames: 509.0
- neutral_timeline_total_sec: 68
- timing_gap_status: unresolved
- errors: []

## Known Current Timing State

- tiny_render_duration_sec: 8
- tiny_render_duration_qualifier: approx
- yym4_timebase_fps: 60
- natural_duration_frames: 509
- natural_duration_sec: 8.483333
- neutral_timeline_total_sec: 68
- neutral_timeline_total_frames_at_60fps: 4080
- timing_gap_sec: 59.516667
- timing_gap_status: unresolved
- audio_path_status: diagnostic_pass
- voice_path: YMM4_native_yukkuri_japanese
- external_TTS_status: closed
- canonical_speaker: ゆっくり霊夢

## Strategy Candidate Comparison

| candidate | suitability | benefits | risks | proves / enables | cannot prove / defers |
|---|---|---|---|---|---|
| A_keep_natural_8_sec_timing | deferred_not_default_after_audio_pass | preserves the tiny render project exactly as already observed; avoids any timing mutation risk | does not move toward the neutral 68 second design; can cause another readback-only stall after audio is already accepted | current diagnostic render/audio path remains intact | neutral 68 second timeline mechanics; post-patch render surface |
| B_global_scale_current_item_frames_to_68_sec | not_default_too_mechanical | simple mathematical bridge from 509 frames to 4080 frames; can expose whether YMM4 accepts stretched item timing | may stretch sparse dialogue gaps in a way that looks accidental; can imply voice/audio stretching even when voice should be preserved | rough duration proof if only total length matters | neutral beat alignment; creative density judgement |
| C_align_dialogue_start_end_to_neutral_timeline | recommended_default | connects the four dialogue rows to neutral 0-12-24-46-68 sec anchors; tests timing mechanics without introducing external TTS | long sparse gaps are diagnostic-only and not production quality; YMM4 voice item length semantics may need structural readback | 68 second project/timeline structural proof; newsroom-ymmp-timing-patch-probe-v1 | creative density improvement; visual layout acceptance; post-patch render observation |
| D_add_neutral_duration_tail_or_non_voice_carrier | fallback_if_voice_item_length_patch_is_unsafe | preserves current native voice timing exactly; can prove total timeline extension with minimal voice mutation | proves carrier duration more than dialogue alignment; may hide whether neutral caption/dialogue anchors can be patched | a YMM4 project can be extended toward 68 seconds | dialogue alignment to the neutral timeline; production pacing |
| E_defer_68_sec_patch_until_script_density_increases | not_default_creative_density_is_separate | avoids making a sparse diagnostic 68 second surface; keeps creative density concerns visible | blocks the next mechanical timing proof; keeps internal review video v0.1 from advancing | future richer script preparation | newsroom-ymmp-timing-patch-probe-v1; milestone-gated post-patch render smoke |

## Recommended Default

- choice: neutral_timeline_skeleton_patch_with_native_voice_preserved
- why_this_default: ['audio is now diagnostic-acceptable, so timing can be handled separately', 'the neutral timeline already defines 0-12-24-46-68 second anchors', 'native YMM4 voice fields should be preserved rather than stretched or regenerated', 'sparse long gaps are acceptable only as diagnostic timing mechanics']
- meaning: ['move toward a 68 sec project/timeline proof', 'preserve YMM4 native voice fields, VoiceCache, speaker, and text', 'do not introduce external TTS', 'do not stretch or regenerate voice audio', 'treat long gaps or sparse content as diagnostic-only', 'prove timing mechanics separately from creative density']
- next_probe: newsroom-ymmp-timing-patch-probe-v1
- not_recommended: ['global voice/audio stretch', 'production render immediately', 'external TTS adoption', 'creative/script density rewrite in this slice']

## Patch Probe Boundary

- next_slice: newsroom-ymmp-timing-patch-probe-v1
- may_create_ignored_local_patched_ymmp_copy: true
- ymmp_commit_allowed: false
- json_patch_plan_first: true
- probe_sequence: ['write a repo JSON/MD patch plan first', 'if the plan passes, create or update an ignored local .ymmp copy only', 'parse the patched copy and write structural readback JSON/MD', 'keep render deferred until structural patch readback passes']
- allowed_to_change: ['Frame', 'Length', 'timeline/project duration metadata if required', 'non-voice timing carrier fields if a carrier fallback is selected', 'diagnostic notes/metadata on the ignored copy only']
- must_preserve: ['CharacterName/speaker', 'Serif/text', 'VoiceCache', 'VoiceParameter', 'Pronounce', 'Hatsuon', 'VoiceLength unless readback proves a timing-only update needs otherwise', 'AudioEffects', 'native voice engine hints']
- readback_required: ['parse patched structure from ignored local .ymmp copy', 'compare original and patched frame/duration fields', 'verify speaker/text/native audio fields are preserved', 'verify no .ymmp/media output is staged or committed']
- render_deferred_until_structural_readback_passes: true

## Render Gate Carry-Forward

- render_gate_current: L0 No Render
- next_render_trigger: after timing patch probe changes timeline surface and structural readback passes
- render_after_patch_expected_level: ['L2 Tiny Smoke Render', 'L3 Targeted Regression Render']
- render_performed_in_this_slice: false
- repeated_audio_check: false
- do_not_render_for: ['strategy docs', 'readback JSON', 'policy-only updates']

## Readiness Separation

- slice_completion: {'status': 'strategy_ready_for_git_gate', 'expected_after_commit_and_push': '6/6'}
- video_readiness: {'status': 'incomplete', 'reason': 'timing strategy is defined, but timing patch probe and post-patch render remain outstanding'}
- production_readiness: {'status': 'low_not_accepted', 'reason': 'production narration, visual layout, real content, public use, and production approval remain outside this diagnostic slice'}

## Not Accepted Scope

- production_render_readiness: false
- public_video_readiness: false
- production_narration_quality: false
- final_script_narration_quality: false
- visual_layout_readiness: false
- real_content_readiness: false
- production_approval: false
- external_TTS_adoption: false
- neutral_68_sec_timing_proof: false

## Next Recommended Slices

| slice | purpose |
|---|---|
| newsroom-ymmp-timing-patch-probe-v1 | Create a JSON patch plan first, then use an ignored local .ymmp copy only if the plan passes preservation checks. |
| milestone-gated-post-patch-render-smoke | Render only after the timing patch probe changes the timeline surface and structural readback passes. |
| newsroom-visual-layout-bridge-v1 | Open later, after timing mechanics and post-patch smoke give a stable surface for visual layout review. |
| newsroom-render-output-retention-policy-v1 | Use only if a later render output must be retained as an artifact. |

## Goal Stack

| item | status |
|---|---|
| Immediate | strategy JSON/readback chooses a probe-ready path |
| Short-term | next slice has allowed fields and preservation rules |
| Mid-term | patch probe structurally proves duration/timing change |
| Long-term | timing/audio/render axes advance without repeated loops |

## Completion Matrix

| item | status |
|---|---|
| current_repo_state_verified | passed |
| source_timing_audio_render_artifacts_inspected | passed |
| timing_strategy_candidates_evaluated | passed |
| recommended_default_selected | neutral_timeline_skeleton_patch_with_native_voice_preserved |
| next_patch_probe_boundary_defined | passed |
| narrow_commit_and_push_if_gate_passes | pending_until_git_gate |

## Artifact Readiness

| item | status |
|---|---|
| strategy_json | present |
| human_readback | present |
| candidate_comparison | present |
| recommended_default | present |
| render_gate_carry_forward | present |
| downstream_next_use | present |

## Video Readiness

| item | status |
|---|---|
| source_input_path_proven | true |
| target_yym4_import_path_proven | true |
| audio_path_proven | true |
| timing_duration_strategy_defined | true |
| tiny_smoke_render_observed | true |
| targeted_regression_render_observed_if_required | false |
| internal_review_milestone_reached | false |

## Production Readiness

| item | status |
|---|---|
| diagnostic_render_exists | true |
| internal_review_accepted | false |
| quality_thresholds_met | false |
| rights_publication_boundary_cleared | false |
| production_export_settings_accepted | false |
| final_artifact_packaged | false |
| public_prod_use_explicitly_approved | false |

## Render Gate Hygiene

| item | status |
|---|---|
| render_performed_in_this_slice | false |
| existing_render_audio_evidence_reused | true |
| render_treated_as_milestone_gated | true |
| next_render_tied_to_timing_patch_probe_milestone | true |
| no_render_for_docs_readback_changes | true |
| repeated_audio_render_check_avoided | true |

## Human Burden Hygiene

| item | status |
|---|---|
| user_input | freeform |
| template_required | false |
| schema_owner | Agent |
| user_side_work | none |
| future_look_for_points_max | 3 |
| negative_confirmation_checklist | false |
| fixed_form_relapse | false |

## Review Non-Redundancy

| item | status |
|---|---|
| prior_render_evidence_reused | true |
| prior_audio_evidence_reused | true |
| prior_timing_gap_strategy_reused | true |
| next_axis_stated_as_timing | true |
| not_accepted_scope_preserved | true |
| repeated_audio_render_review_requested | false |

## Inertia Check

| item | status |
|---|---|
| packet_for_packet_drift | false |
| readback_only_stall | false |
| repeated_render_request | false |
| product_video_readiness_separated_from_slice_completion | true |
| next_concrete_milestone | newsroom-ymmp-timing-patch-probe-v1 |

## Boundaries

- YMM4_launched_by_agent: false
- render_created_by_agent: false
- audio_generated_by_agent: false
- TTS_generated_by_agent: false
- real_media_imported: false
- external_fetch_performed: false
- ymmp_created_or_modified_by_agent: false
- ymmp_or_media_staged_or_committed: false
- production_approval: false
- public_video_ready: false
- dashboard_governance_freshness_changed: false

## Boundary Note

This strategy chooses the next probe path only. It does not patch or commit `.ymmp`, launch YMM4, render, generate TTS/audio, import real media, accept production quality, or ask for another audio/render observation.
