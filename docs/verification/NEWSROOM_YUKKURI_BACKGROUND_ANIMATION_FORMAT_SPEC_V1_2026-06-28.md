# Newsroom Yukkuri Background Animation Format Spec v1

artifact_id: newsroom_yukkuri_background_animation_format_spec_v1_2026_06_28
schema_version: newsroom_yukkuri_background_animation_format_spec.v1
production_status: diagnostic_only
next_recommended_slice: newsroom-yukkuri-animation-primitive-proof-v1


## User Correction Normalized

- base_video_format: yukkuri_explainer
- background_style_layer: yukkuri_chaban_style_reenactment_pv
- goal: visual_engagement_through_lightweight_animation
- rejected_interpretation: chaban_style_dialogue_script_as_the_main_format
- rejected_path: line_count_density_and_card_only_visual_optimization
- missing_core: background_animation_layer_and_scene_beat_automation
- animation_primitives_expected: ["head_body_separated_character_motion", "nodding_or_head_movement", "expression_changes", "character_movement", "speech_balloons", "light_interaction_consistency"]

## Layer Model

| layer_id | role | primary_job | must_not_do |
|---|---|---|---|
| narration_subtitle_layer | primary_explanation | carry the yukkuri explainer logic and subtitle-safe narration | be replaced by unsourced chaban dialogue |
| background_animation_layer | supportive_reenactment_pv | provide simple actions, reactions, and continuity behind the explanation | become the main script format or production-quality animation claim |
| card_overlay_layer | bounded_information_support | show point, proof, warning, or next-action cues only when useful | turn the video back into card-only slides |
| source_boundary_layer | diagnostic_limits | keep fake/private/source/rights/publication boundaries visible | imply real source approval or public readiness |

## Background Animation Role

| role_id | purpose |
|---|---|
| prevent_card_fatigue | avoid a PowerPoint-like card-only rhythm |
| visual_continuity | make each narration segment feel connected |
| light_reenactment | show simple situations without copying external footage |
| externalize_reactions | show questions or doubt as character reactions |
| attention_without_overload | add motion while keeping explanation readable |

## Scene Beat Schema

- required_fields: ["beat_id", "narration_line_id", "scene_function", "character", "expression", "motion", "prop_or_background", "card_overlay", "timing_range", "fallback_if_animation_missing"]
- scene_function_values: ["hook", "reaction", "explanation", "proof", "warning", "next_action"]
- policy: {"animation_supports_explanation": true, "fallback_must_preserve_meaning": true, "no_public_reference_copying": true, "one_beat_one_visible_job": true}

## Scene Beat Examples

| beat_id | narration_line_id | scene_function | character | expression | motion | prop_or_background | card_overlay | timing_range | fallback_if_animation_missing |
|---|---|---|---|---|---|---|---|---|---|
| beat_001 | dense_v2_line_001 | hook | reimu | concerned | small_head_tilt | plain room / blank process demo card | none | 0-6 sec | static character plus subtitle |
| beat_002 | dense_v2_line_002 | explanation | reimu | neutral | nod | idea-to-video arrows | point card optional | 6-11 sec | card-only cue with no motion |
| beat_003 | dense_v2_line_006 | explanation | reimu | confident | small_position_move | reviewable draft board | flow card optional | 26-31 sec | static board and subtitle |
| beat_004 | dense_v2_line_010 | warning | reimu | serious | head_shake | rights/source warning sign | boundary note | 48-54 sec | warning card only |
| beat_005 | dense_v2_line_012 | next_action | reimu | easy | speech_balloon | YMM4 import/save checklist | next card optional | 58-63 sec | subtitle plus small next-action card |

## Reference Grammar Plan

- external_fetch_or_copy_in_this_slice: false
- later_reference_pack_should_extract: ["number_of_characters", "scene_transition_frequency", "typical_reaction_beats", "subtitle_and_balloon_relationship", "card_overlay_tolerance", "how_background_action_supports_explanation"]
- allowed_later_method: abstract grammar only; no visual copying
- blocked_until: reference use is explicitly allowed and rights boundaries are recorded

## Business Goal Evaluation

| gate | status | evidence | decision |
|---|---|---|---|
| problem_clear | pass | cards alone are identified as causing card fatigue and weak visual continuity | shift axis to background animation layer |
| offer_clear | pass | animation layer adds reactions, simple situations, and continuity while narration explains | define as supportive layer |
| proof_clear | pass | prior YMM4 mechanics are separated from unproven newsroom animation automation | probe primitives next |
| boundary_clear | pass | production quality, render proof, public reference copying, and audience acceptance remain false | keep diagnostic only |
| next_action_clear | pass | newsroom-yukkuri-animation-primitive-proof-v1 | newsroom-yukkuri-animation-primitive-proof-v1 |
| visual_supports_explanation | pass | scene beat schema requires fallback and narration-line anchoring | avoid decoration-only motion |

## Completion Matrix

| gate | status |
|---|---|
| repo_state_verified | true |
| user_correction_normalized | true |
| animation_layer_format_spec_created | true |
| primitive_inventory_created | true |
| prior_asset_recovery_audit_created | true |
| next_animation_specific_axis_selected | newsroom-yukkuri-animation-primitive-proof-v1 |
| commit_and_push_if_push_gate_passes | ready_for_git_followthrough |

## Artifact Readiness

| gate | status |
|---|---|
| spec_json_exists | true |
| human_doc_exists | true |
| primitive_inventory_exists | true |
| recovery_audit_exists | true |
| no_production_public_claim | true |
| downstream_next_use_described | true |

## Access Readiness

| gate | status |
|---|---|
| found_asset_paths_include_access_state | true |
| missing_assets_classified_honestly | true |
| no_user_work_emitted_without_verified_access | true |

## Render Gate Hygiene

| gate | status |
|---|---|
| no_render_performed_by_agent | true |
| no_YMM4_launch | true |
| no_ymmp_edit | true |
| no_audio_or_tts_generation | true |
| L0_no_render_gate_preserved | true |

## Human Burden Hygiene

| gate | status |
|---|---|
| user_input | none_required_for_this_slice |
| fixed_form_requested | false |
| schema_owner | agent |
| future_user_work_waits_for_verified_artifact | true |

## Inertia Check

| gate | status |
|---|---|
| no_text_density_loop | true |
| no_visual_card_polish_loop | true |
| no_render_automation_rabbit_hole | true |
| animation_layer_restored_as_core_product_axis | true |
| next_concrete_animation_milestone_named | newsroom-yukkuri-animation-primitive-proof-v1 |

## Not Accepted Scope

- render_proof: false
- ymmp_mutation: false
- production_animation_quality: false
- public_upload_or_public_readiness: false
- real_rss_or_news_integration: false
- external_reference_video_fetch: false
- copied_external_visuals: false
- actual_order_or_audience_acceptance: false

## Boundaries

- YMM4_launched_by_agent: false
- render_performed_by_agent: false
- ymmp_edited_or_committed: false
- audio_tts_generated: false
- cards_regenerated: false
- real_rss_or_news_fetched: false
- external_reference_videos_fetched: false
- production_public_readiness_claimed: false
- actual_audience_acceptance_claimed: false

## Boundary Note

This spec does not render, launch YMM4, edit `.ymmp`, create audio/TTS, fetch public reference videos, copy external visuals, or claim production quality.
