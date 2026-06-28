# Newsroom Visual Density Simplification Spec v1

artifact_id: newsroom_visual_density_simplification_spec_v1_2026_06_26
spec_id: newsroom_visual_density_simplification_spec_v1_2026_06_26
schema_version: newsroom_visual_density_simplification_spec.v1
spec_status: defined
production_status: diagnostic_only

## Outcome

This spec turns the recorded density/cognitive-load finding into bounded simplification criteria for the next visual refinement. It does not redesign cards, regenerate assets, launch YMM4, render video, edit .ymmp files, or claim production/public/audience acceptance.

## Identity

- spec_id: newsroom_visual_density_simplification_spec_v1_2026_06_26
- source_density_gate_path: samples/_probe/newsroom_handoff/post_benchmarked_visual_observation_density_gate_v1.json
- source_density_gate_id: newsroom_post_benchmarked_visual_observation_density_gate_v1_2026_06_26
- source_benchmark_evaluation_path: samples/_probe/newsroom_handoff/audience_fit_benchmark_evaluation_v1.json
- source_benchmark_evaluation_id: newsroom_audience_fit_benchmark_evaluation_v1_2026_06_26
- source_visual_benchmark_path: samples/_probe/newsroom_handoff/visual_audience_fit_benchmark_v1.json
- source_visual_benchmark_id: newsroom_visual_audience_fit_benchmark_v1_2026_06_26
- source_benchmarked_refinement_path: samples/_probe/newsroom_handoff/visual_card_benchmarked_refinement_v1.json
- source_benchmarked_refinement_id: newsroom_visual_card_benchmarked_refinement_v1_2026_06_26
- source_cards_dir: samples/_probe/newsroom_handoff/visual_cards_v1
- production_status: diagnostic_only
- visual_work_class: audience_fit
- spec_status: defined
- actual_audience_acceptance_claimed: False

## Problem Statement

- mechanics_status_pass: True
- visual_density_issue: True
- cognitive_load_high: True
- format_attention_over_content: True
- text_fit_tight_warning: True
- pacing_density_issue_for_68_sec_video: True
- production_quality_accepted: False
- public_video_ready: False

## Density Budget

- dominant_message_per_card: exactly_one
- headline_budget: maximum_1_headline
- primary_sentence_budget: maximum_1_primary_sentence
- supporting_note_or_diagram_budget: maximum_1
- meaningful_label_budget: maximum_2_to_3_labels
- essential_meaning_in_tiny_metadata: False
- debug_or_source_text_policy: shorten_demote_or_hide_from_main_viewing_path
- subtitle_reserve_policy: simple_and_non_competing
- minimum_meaningful_font_size_policy: preserve_or_increase
- box_count_policy: reduce_or_merge_before_adding

## Simplification Operations

| operation | rule | future use |
|---|---|---|
| remove_nonessential_microcopy | delete text that explains diagnostic scaffolding but does not change the viewer's takeaway | reduce reading paths before changing style |
| merge_repeated_labels | combine repeated role/status labels into one visible boundary or cue | keep the diagnostic boundary without label clutter |
| demote_diagnostic_source_metadata | move source/debug detail out of the primary viewing path or shorten it to a tiny nonessential cue | prevent source/subtitle areas from competing with the card message |
| replace_small_text_with_visual_markers | use icons, numbers, or color-coded markers when the text only signals role/state | remove tiny reading obligations without losing role variation |
| increase_whitespace_around_essential_text | give the headline and primary sentence more breathing room before adding any explanatory box | make the dominant message visible within three seconds |
| split_overloaded_roles_only_if_necessary | split a card role only when removal/merge/demotion cannot preserve the essential message | avoid expanding the four-card structure casually |
| preserve_fake_review_boundary_with_fewer_labels | retain review-only/fake/diagnostic meaning through one compact boundary signal | keep publication safety while reducing surface noise |
| preserve_card_role_variation | keep point, flow, check, and next/source roles distinct after simplification | prevent simplification from flattening the explainer structure |

## Hard Constraints

- do_not_reduce_minimum_meaningful_font_size: True
- do_not_solve_density_by_shrinking_text: True
- do_not_add_more_boxes_to_explain_existing_boxes: True
- do_not_introduce_real_brands_urls_or_real_news_visuals: True
- do_not_convert_cards_into_complex_yym4_object_graphs: True
- do_not_claim_production_visual_quality: True
- do_not_claim_audience_acceptance: True

## Card-Specific Preliminary Diagnosis

| card | likely density problem | essential message | remove/demote | must stay | future direction |
|---|---|---|---|---|---|
| visual_card_cap_beat_fake_intro_001_01_v1 | intro card carries headline, summary, number motif, point panel, no-real-claim chip, and source band at once | fake topic is review-only and the card is a plain point summary | secondary POINT mini panel, no-real-news-claim chip if boundary is preserved elsewhere, extra diagnostic badge repetition | review-only/fake boundary, dominant fake-topic headline, card order cue | make one large point message with one compact diagnostic boundary and more whitespace |
| visual_card_cap_beat_fake_intro_001_02_v1 | flow card repeats step numbers, labels, and simple-flow badge while also asking the viewer to read body copy | handoff stays review-only through three simple steps | simple-flow badge, repeated explanatory body text, extra box outlines around every step | three-step flow, review-only boundary, role difference from point/check/source cards | use three large step markers with short labels and remove secondary explanation |
| visual_card_cap_beat_fake_claim_001_01_v1 | check card uses four small status boxes plus left body text, creating multiple reading paths | a fake claim is shown and the viewer should understand it is check/review-only | RESULT box, STATUS box, duplicate check/caution microcopy | fake claim boundary, check/caution role, large readable primary message | collapse status boxes into one check/caution visual cue and keep one primary sentence |
| visual_card_cap_beat_fake_claim_001_02_v1 | next/source card stacks source, status, next panels and a next bubble, so metadata competes with the main next action | fake source checks are noted and the next action remains diagnostic | separate SOURCE/STATUS/NEXT panel headings, next bubble, source microcopy in the main reading path | source-check awareness, next-action role, diagnostic/fake boundary | merge source/status/next into one short next-action block with demoted source detail |

## Evaluation Criteria For Next Refinement

| criterion | target |
|---|---|
| dominant_message_visible_within_3_seconds | viewer can identify the card's single point without reading secondary metadata |
| no_more_than_one_primary_reading_path | headline and one primary sentence or diagram carry the main meaning |
| meaningful_text_fits_without_crowding | no essential text sits close to box edges or depends on unexpected wrap behavior |
| source_subtitle_debug_area_does_not_compete | source/subtitle/debug cues are visibly secondary to main content |
| role_difference_remains_clear | point, flow, check, and next/source roles remain distinguishable |
| diagnostic_fake_boundary_remains_visible | review-only/fake status remains clear with fewer labels |
| surface_feels_simpler_than_previous_density_gate | less broadcast/presentation-like concentration burden than the benchmarked cards |

## Next Slice Recommendation

- default_slice: newsroom-visual-card-density-benchmarked-refinement-v1
- reason: density/cognitive-load issue now has a spec and can be addressed with a bounded card update
- user_side_work: none_for_this_slice

## Recommended Next Slices

| slice | timing | reason |
|---|---|---|
| newsroom-visual-card-density-benchmarked-refinement-v1 | default_next | apply remove/merge/demote/whitespace rules to the current card assets |
| newsroom-visual-information-density-benchmark-v1 | only_if_current_spec_cannot_define_adequate_criteria | upgrade metrics before refinement only if these spec criteria are insufficient |
| newsroom-internal-review-v0.1-operator-review-card | only_if_supervisor_accepts_current_density_for_diagnostic_v0_1 | skip additional visual change only with an explicit supervisor decision |
| newsroom-visual-card-source-band-simplification-v1 | if_source_subtitle_band_is_dominant_actionable_issue | narrow to source/subtitle band if the next diagnosis says that is the main burden |

## Not Accepted Scope

- actual_target_audience_acceptance: unknown
- ctr_retention_prediction: unknown
- production_visual_quality: False
- final_design_system: False
- real_newsroom_visual_acceptance: False
- public_readiness: False
- production_approval: False

## Goal Stack

| level | goal | success signal | contribution |
|---|---|---|---|
| Immediate | Define density simplification rules | spec JSON/doc exists | prevents another ad hoc visual tweak |
| Short-term | Enable bounded density refinement | next card change has explicit remove/merge/demote rules | reduces cognitive load |
| Mid-term | Resume internal review v0.1 | refined cards can be reviewed for pacing and content, not visual clutter | improves review utility |
| Long-term | Establish reusable density baseline | future RSS/content videos inherit simpler card rules | supports automation |

## Completion Matrix

| item | status |
|---|---|
| current_repo_state_verified | True |
| density_gate_inspected | True |
| density_budget_defined | True |
| simplification_operations_and_hard_constraints_defined | True |
| card_specific_preliminary_diagnosis_recorded | True |
| narrow_commit_created_and_pushed_if_push_gate_passes | agent_followthrough_after_validation |

## Artifact Readiness

| item | status |
|---|---|
| spec_json_exists | True |
| human_doc_exists | True |
| density_budget_present | True |
| simplification_operations_present | True |
| next_refinement_criteria_present | True |
| downstream_next_use_described | True |

## Visual Gate

| item | status |
|---|---|
| density_issue_preserved | True |
| cognitive_load_issue_preserved | True |
| no_redesign_performed | True |
| no_audience_acceptance_claimed | True |
| proxy_criteria_defined | True |
| next_iteration_bounded | True |
| unknowns_preserved | True |
| review_protocol_remains_freeform | True |

## Render Gate Hygiene

| item | status |
|---|---|
| no_render_performed_by_agent | True |
| no_render_for_spec_only_change | True |
| next_render_tied_to_material_density_linked_card_change | True |
| repeated_render_loop_avoided | True |
| existing_observation_consumed_once | True |
| output_first_principle_preserved | True |

## Human Burden Hygiene

| item | status |
|---|---|
| user_input_freeform | True |
| template_required_false | True |
| schema_owner_agent | True |
| user_side_work_none_for_this_slice | True |
| future_review_look_for_lte_3 | True |
| no_negative_confirmation_checklist | True |
| no_fixed_form_relapse | True |

## Review Non-Redundancy

| item | status |
|---|---|
| density_gate_reused | True |
| benchmark_evaluation_reused | True |
| next_axis_density_simplification_spec | True |
| not_accepted_scope_preserved | True |
| no_repeated_user_review_requested | True |
| no_mechanics_re_review_requested | True |

## Inertia Check

| item | status |
|---|---|
| no_ad_hoc_visual_iteration | True |
| no_broad_redesign | True |
| no_packet_for_packet_drift | True |
| readiness_separated_from_slice_completion | True |
| next_concrete_criteria_linked_milestone_named | True |

## Downstream Next Use

- default_next_slice: newsroom-visual-card-density-benchmarked-refinement-v1
- instruction: the next visual change must choose changes from this spec's remove/merge/demote/whitespace operations
- allowed_change_axis: density-benchmarked card refinement, source/subtitle band simplification if it is the dominant burden, benchmark upgrade only if this spec is inadequate
- disallowed_change_axis: broad redesign, style-only polish, text shrinking, more boxes explaining existing boxes, YMM4/render/audio/TTS work for this spec-only slice

## Boundaries

- diagnostic_only: True
- YMM4_launched_by_agent: False
- render_performed_by_agent: False
- ymmp_edited_or_committed: False
- svg_png_cards_regenerated: False
- audio_tts_or_voice_cache_created: False
- external_fetch_performed: False
- fixed_review_form_requested: False
- card_redesign_performed: False
- production_approval: False
- audience_acceptance_claimed: False
- public_video_ready: False
