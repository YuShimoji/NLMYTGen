# Newsroom v0.1 Script Density Plan v1

artifact_id: newsroom_v0_1_script_density_plan_v1_2026_06_26
plan_id: newsroom_v0_1_script_density_plan_v1_2026_06_26
schema_version: newsroom_v0_1_script_density_plan.v1
production_status: diagnostic_only
plan_type: script_density_plan_only
diagnostic_only: true


## Target Density

- target_duration_sec: {"max": 75, "min": 60}
- target_narration_segments: 5
- suggested_line_count_range: {"max": 14, "min": 10}

## Current Script Density Reference

- current_dialogue_line_count: 4
- current_dialogue_lines: ["Fake topic, review only.", "Review-only handoff stays.", "A fake claim is shown.", "Fake source checks are noted."]
- current_duration_sec: 68
- current_seconds_per_dialogue_line: 17.0
- current_spoken_density: too_sparse_for_explanation
- silence_spacing_implication: four short lines over about 68 sec prove mechanics but leave the viewer to infer problem, offer, proof sequence, and next action
- four_lines_enough_for_explanation: false
- likely_needed_line_count_range: {"max": 14, "min": 10}
- likely_needed_segment_count: 5
- card_to_narration_alignment: cards can support structure but should not carry the full pitch
- what_should_be_spoken: ["what this diagnostic proves", "why CSV to YMM4 matters", "what evidence is now confirmed", "what remains diagnostic-only", "what the viewer should ask for next"]
- what_should_be_shown: ["card role", "simplified proof markers", "review-only boundary", "status/next-action hints"]

## Recommended Segment Structure

| segment | purpose | spoken_job | line_count_target |
|---|---|---|---|
| opening | what this proves | state that a diagnostic video can now be assembled from script import, native audio, timing, and card assets | 2-3 |
| mechanism | CSV to YMM4 | explain that tracked CSV/script input can recreate the YMM4 dialogue path while avoiding direct video generation claims | 2-3 |
| proof | audio/timing/cards/render | name the proof chain: native audio, 68 sec timing, four cards, render output | 3-4 |
| boundary | diagnostic only | say this is not production, public, or real-news acceptance | 1-2 |
| next_action | RSS dry run / real packet plan | direct the next decision toward an RSS dry run or real packet plan after review | 2 |

## Card To Narration Alignment

| card_index | card_role | spoken_job | shown_job |
|---|---|---|---|
| 1 | point / review-only overview | open with the diagnostic promise and what can now be built | keep the review-only boundary and point summary visible |
| 2 | flow / mechanism | explain CSV/script import into YMM4 as the controlled handoff | show the simple flow without narrating every label |
| 3 | check / proof | state what was proven: audio, timing, cards, render | support the proof with check/status markers |
| 4 | next / source-status | close with diagnostic boundary and next inquiry path | carry next-action/status hints |

## Implementation Policy

- plan_only: true
- script_implementation_in_this_slice: false
- YMM4_launch_or_render_in_this_slice: false
- cards_regenerated_in_this_slice: false

## Highest-Value Next Axis

- selected: newsroom-v0.1-script-density-implementation-plan-v1
- reason: script density should be planned before another render or RSS dry run

## Automation Note

- agent_can_prepare: ["CSV/script inputs", "card assets", "YMM4 patch/readback artifacts", "diagnostic verification docs"]
- user_yym4_side_remains_required_for: ["native YMM4 audio confirmation", "manual render/export", "GUI-only behavior until an official or tested automation path exists"]
- priority: do not prioritize full render automation before explanation/script density unless supervisor explicitly chooses it
- ai_direct_video_generation_via_ymmp: not_reliable_yet

## Not Accepted Scope

- production_readiness: false
- public_readiness: false
- actual_audience_or_order_acceptance: false
- real_rss_or_news_content: false
- rights_publication_clearance: false
- final_design_system: false
- automated_yym4_render_claim: false

## Completion Matrix

| gate | status |
|---|---|
| current_repo_state_verified | true |
| current_proven_capabilities_summarized | true |
| explanation_readiness_gates_evaluated | true |
| script_density_diagnosis_completed | true |
| highest_value_next_axis_selected | newsroom-v0.1-script-density-implementation-plan-v1 |
| narrow_commit_created_and_pushed_if_push_gate_passes | pending_until_git_gate |

## Artifact Readiness

| gate | status |
|---|---|
| explanation_readiness_json_exists | true |
| script_density_plan_json_exists | true |
| human_docs_exist | true |
| proven_capabilities_map_present | true |
| next_axis_decision_present | true |
| downstream_next_use_described | true |

## Render Gate Hygiene

| gate | status |
|---|---|
| no_render_performed_by_agent | true |
| existing_render_evidence_reused | true |
| no_render_for_docs_plan_only_change | true |
| next_render_tied_to_material_script_audio_card_change | true |
| repeated_render_loop_avoided | true |
| output_first_principle_preserved | true |

## Human Burden Hygiene

| gate | status |
|---|---|
| user_input | freeform |
| template_required | false |
| schema_owner | Agent |
| user_side_work | none_for_this_slice |
| future_review_look_for_count | <=3 |
| negative_confirmation_checklist | false |
| fixed_form_relapse | false |

## Inertia Check

| gate | status |
|---|---|
| no_ad_hoc_visual_iteration | true |
| no_automation_rabbit_hole | true |
| no_packet_for_packet_drift | true |
| business_explanation_goal_restored_above_visual_polish | true |
| next_concrete_milestone | newsroom-v0.1-script-density-implementation-plan-v1 |

## Downstream Next Use

- next_default_slice: newsroom-v0.1-script-density-implementation-plan-v1
- first_artifacts_to_reopen: ["samples/_probe/newsroom_handoff/v0_1_explanation_readiness_v1.json", "samples/_probe/newsroom_handoff/v0_1_script_density_plan_v1.json"]
- reason: script density is the next bottleneck after diagnostic render mechanics and density visuals passed

## Boundaries

- YMM4_launched_by_agent: false
- render_performed_by_agent: false
- ymmp_edited_or_committed: false
- audio_tts_generated: false
- cards_regenerated: false
- real_rss_or_news_fetched: false
- production_public_readiness_claimed: false
- actual_audience_acceptance_claimed: false

## Boundary Note

This plan defines density and segment structure only. It does not implement a denser script, regenerate YMM4 files, render, or approve public/production use.
