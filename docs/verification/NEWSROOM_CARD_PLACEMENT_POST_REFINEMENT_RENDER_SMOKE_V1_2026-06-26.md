# Newsroom Card Placement Post-Refinement Render Smoke v1

artifact_id: newsroom_card_placement_post_refinement_render_smoke_v1_2026_06_26
smoke_id: newsroom_card_placement_post_refinement_render_smoke_v1_2026_06_26
schema_version: newsroom_card_placement_post_refinement_render_smoke.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
smoke_status: prepared_not_run
package_status: ready_for_manual_milestone_render_smoke
diagnostic_only: true

## Source

- smoke_id: newsroom_card_placement_post_refinement_render_smoke_v1_2026_06_26
- source_refinement_path: samples/_probe/newsroom_handoff/visual_card_design_refinement_v1.json
- source_refinement_id: newsroom_visual_card_design_refinement_v1_2026_06_25
- source_placement_probe_path: samples/_probe/newsroom_handoff/yym4_card_asset_placement_probe_v1.json
- source_placement_probe_id: newsroom_yym4_card_asset_placement_probe_v1_2026_06_25
- source_prior_render_result_path: samples/_probe/newsroom_handoff/card_placement_render_smoke_result_readback_v1.json
- source_prior_render_result_id: newsroom_card_placement_render_smoke_result_readback_v1_2026_06_25
- target_card_placement_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp
- post_refinement_render_output_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_post_refinement_v1.mp4
- production_status: diagnostic_only
- render_smoke_status: not_run

## Source Validation

- status: passed
- errors: []
- source_refinement_id: newsroom_visual_card_design_refinement_v1_2026_06_25
- source_refinement_status: assets_regenerated
- source_placement_probe_id: newsroom_yym4_card_asset_placement_probe_v1_2026_06_25
- source_placement_probe_status: placed_structurally
- source_prior_render_result_id: newsroom_card_placement_render_smoke_result_readback_v1_2026_06_25
- source_prior_render_result: pass
- prior_render_duration_sec: 68
- prior_render_card_count_visible: 4
- refined_card_count: 4
- refined_png_paths: samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_01_v1.png, samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_02_v1.png, samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_01_v1.png, samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_02_v1.png
- target_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp
- target_ymmp_found_at_generation: true
- target_ymmp_card_image_item_count: 4
- target_ymmp_reuses_refined_png_paths: true
- target_ymmp_ignored: true
- target_ymmp_committed: false
- target_ymmp_staged: false

## Target

- target_card_placement_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp
- target_ymmp_path_status: discoverable_local_file_at_generation_time
- git_tracking_policy: ignored_under_tmp_do_not_stage_or_commit
- ymmp_file_newly_modified_in_this_slice: false
- post_refinement_render_output_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_post_refinement_v1.mp4
- post_refinement_output_exists_at_generation: false
- render_output_commit_allowed: false
- expected_duration_sec: 68
- expected_card_count: 4
- expected_dialogue_item_count: 4
- render_objective: {"confirm_dialogue_and_native_audio_preserved": true, "confirm_output_duration_about_68_sec": true, "confirm_project_opens": true, "confirm_refined_cards_visible_and_readable": true, "confirm_render_completes": true, "production": false, "public_video": false}

| card | role | png | ymmp path reused |
|---|---|---|---|
| visual_card_cap_beat_fake_intro_001_01_v1 | intro_summary | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_01_v1.png | true |
| visual_card_cap_beat_fake_intro_001_02_v1 | handoff_process | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_02_v1.png | true |
| visual_card_cap_beat_fake_claim_001_01_v1 | claim_check | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_01_v1.png | true |
| visual_card_cap_beat_fake_claim_001_02_v1 | source_status_next_action | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_02_v1.png | true |

## Milestone Render Gate

- gate_type: milestone_gated_verification
- milestone: newsroom-card-placement-post-refinement-render-smoke-v1
- render_performed_in_this_slice: false
- YMM4_launched_by_agent: false
- manual_render_allowed_next: true
- manual_render_count: 1
- render_reason: Refined card PNGs replaced the prior visual surface at stable paths, so one observation can confirm YMM4 sees the updated assets.
- timing_strategy_change_allowed: false
- external_TTS_allowed: false
- render_output_commit_allowed: false
- ymmp_commit_allowed: false

## Operator Observation Card

- status: required_next_milestone
- target: post-refinement card-placement diagnostic render smoke
- target_ymmp_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp
- output_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_post_refinement_v1.mp4
- why: Confirm the existing card-placement project reads the regenerated refined PNG assets.
- action: Open the ignored card-placement .ymmp in YMM4 and render once to the separate post-refinement output path without changing timing, voice, media, or card placement.
- answer_style: freeform
- answer_hint: opened and rendered; about 68 sec; four refined cards visible without obvious clipping; dialogue and native voice remained
- look_for:
  - card-placement diagnostic project opens
  - render completes to a separate post-refinement output
  - output duration is approximately 68 seconds
  - four refined PNG cards are visible and have no obvious text clipping
  - dialogue timeline and native YMM4/Yukkuri audio remain present
- not_needed:
  - fixed form
  - another review of the old card design
  - detailed sound quality judgement
  - production quality approval
  - committing .ymmp or media output

## Result Normalization Schema

- schema_owner: Agent
- user_must_fill_schema: false
- duration_tolerance_sec: 2

| field | type | normalization |
|---|---|---|
| placement_project_opened | boolean_or_unknown | true only when the target .ymmp opens in YMM4 |
| render_completed | boolean_or_unknown | true only when YMM4 export finishes |
| output_duration_observed_sec | number_or_null | observed media duration in seconds when known |
| duration_approximately_68_sec | boolean_or_unknown | true when duration is within the configured 68 sec tolerance |
| refined_card_assets_visible | boolean_or_unknown | true when all four refined PNG cards are visible |
| card_count_observed | integer_or_null | observed refined card count when reported |
| no_obvious_text_clipping_or_readability_breakage | boolean_or_unknown | true when the operator reports no obvious clipping or readability breakage |
| dialogue_items_preserved | boolean_or_unknown | true when the expected dialogue items remain present |
| dialogue_item_count_observed | integer_or_null | observed dialogue item count if reported |
| native_audio_present | boolean_or_unknown | true when native YMM4/Yukkuri audio is still audible |
| operator_notes | string_or_null | freeform notes retained without requiring a form |
| error_message | string_or_null | YMM4 or export error text when reported |
| confidence | string | agent confidence in the normalized observation |
| unknowns | array | required targets the observation did not settle |
| classification | enum | classification from the success/failure matrix |
| result | enum | pass, fail, or blocked_by_operator_uncertainty |

## Success / Failure Classification Matrix

| classification | trigger | result | next slice |
|---|---|---|---|
| post_refinement_render_smoke_pass | all post-refinement observation targets are true | pass | newsroom-card-placement-post-refinement-render-smoke-result-readback-v1 |
| post_refinement_project_open_failure | card-placement project does not open | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_render_execution_failure | project opens but render does not complete | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_duration_mismatch | render completes but output is not approximately 68 sec | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_card_visibility_regression | fewer than four refined cards are visible | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_readability_regression | cards render but still show obvious clipping or readability breakage | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_dialogue_preservation_regression | dialogue items are missing or altered | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_native_audio_regression | native audio is absent | fail | newsroom-card-placement-post-refinement-render-smoke-failure-classification-v1 |
| post_refinement_operator_observation_uncertain | one or more required observation targets remain unknown | blocked_by_operator_uncertainty | newsroom-card-placement-post-refinement-render-smoke-operator-uncertainty-v1 |

## Render Readback Builder

- builder_id: newsroom_card_placement_post_refinement_render_smoke_result_readback_builder_v1
- module: src.pipeline.newsroom_card_placement_post_refinement_render_smoke
- function: build_newsroom_card_placement_post_refinement_render_smoke_result_readback
- input_package: samples/_probe/newsroom_handoff/card_placement_post_refinement_render_smoke_v1.json
- input_observation: future freeform operator observation normalized by Agent
- output_schema_version: newsroom_card_placement_post_refinement_render_smoke_result_readback.v1
- writes_artifact_in_this_slice: false
- requires_committed_media: false
- requires_committed_ymmp: false
- classification_function: classify_render_smoke_observation

## Completion Matrix

| item | status |
|---|---|
| current_repo_state_verified | true |
| prior_visual_refinement_detected_as_complete | true |
| stable_png_paths_verified_in_ignored_ymmp | true |
| manual_render_smoke_package_created | true |
| future_readback_normalizer_defined | true |
| narrow_commit_created_and_pushed_if_push_gate_passes | pending_until_git_gate |

## Artifact Readiness

| item | status |
|---|---|
| render_smoke_package_json | present |
| human_render_smoke_doc | present |
| source_validation | ready_for_manual_milestone_render_smoke |
| operator_observation_card | present |
| result_normalization_schema | present |
| downstream_next_use | present |

## Visual Readiness

| item | status |
|---|---|
| visual_card_concept_selected | true |
| external_card_assets_generated | true |
| preview_contact_sheet_available | true |
| assets_mapped_to_timeline_caption_units | true |
| yym4_placement_contract_defined | true |
| yym4_placement_paths_reused_after_refinement | true |
| post_refinement_render_reviewed | false |

## Render Gate Hygiene

| item | status |
|---|---|
| render_performed_by_agent_in_this_slice | false |
| existing_render_evidence_reused | true |
| render_treated_as_milestone_gated | true |
| next_render_tied_to_visual_surface_change | true |
| no_render_for_docs_readback_changes | true |
| repeated_timing_audio_review_avoided | true |

## Human Burden Hygiene

| item | status |
|---|---|
| user_input | freeform |
| template_required | false |
| schema_owner | Agent |
| user_side_work_this_agent_slice | none |
| required_future_observation_target_count | 5 |
| negative_confirmation_checklist | false |
| fixed_form_relapse | false |

## Review Non-Redundancy

| item | status |
|---|---|
| prior_internal_review_observation_reused | true |
| prior_visual_refinement_reused | true |
| prior_card_placement_render_evidence_reused | true |
| next_axis_stated_as_post_refinement_render_smoke | true |
| not_accepted_scope_preserved | true |
| current_user_review_or_render_re_requested | false |

## Inertia Check

| item | status |
|---|---|
| packet_for_packet_drift | false |
| readback_only_stall | false |
| repeated_render_request_without_surface_change | false |
| readiness_separated_from_slice_completion | true |
| next_concrete_milestone | newsroom-card-placement-post-refinement-render-smoke-result-readback-v1 |

## Boundary

- YMM4_launched_by_agent: false
- video_render_created_by_agent: false
- audio_generated_by_agent: false
- TTS_generated_by_agent: false
- external_TTS_introduced: false
- real_media_imported: false
- external_source_fetch_performed: false
- real_brand_url_or_news_screenshot_used: false
- ymmp_edited_by_agent: false
- ymmp_or_media_staged_or_committed: false
- render_output_staged_or_committed: false
- production_visual_quality_accepted: false
- production_approval: false
- public_video_ready: false
- dashboard_governance_freshness_changed: false

## Boundary Note

This package prepares one milestone observation of the changed visual surface after the card assets were refined at stable paths. The agent did not launch YMM4, render, edit `.ymmp`, generate audio/TTS, stage media, or approve production/public use.
