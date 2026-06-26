# Newsroom Visual Audience-Fit Benchmark v1

artifact_id: newsroom_visual_audience_fit_benchmark_v1_2026_06_26
benchmark_id: newsroom_visual_audience_fit_benchmark_v1_2026_06_26
schema_version: newsroom_visual_audience_fit_benchmark.v1
benchmark_status: draft_proxy_benchmark_defined
production_status: diagnostic_only

## Purpose

This benchmark prevents additional ad hoc visual tweaking. It defines proxy criteria for whether the current fake/review-only newsroom cards are understandable for a general explanatory YouTube viewer. It is not a card redesign, YMM4 render, .ymmp edit, production approval, public-readiness claim, real newsroom intake, external reference scrape, or audience acceptance proof.

## Target Audience Assumption

- assumed_audience: general YouTube viewers for explanatory/newsroom-style content, non-expert, low patience, expects familiar visual grammar
- viewing_context: normal video playback, likely desktop/mobile, not frame-by-frame inspection
- attention_level: must understand the dominant card message quickly
- device_screen_assumption: 1080p baseline, readable after video compression

## Visual Job-To-Be-Done

- helps_viewer: understand what each fake/review-only card is doing, follow a simple diagnostic structure without reading tiny metadata
- dominant_message: one clear point per card
- non_goals: final production design, real news design, public-ready branding, audience acceptance proof

## Evidence Level

- current_level: L1_user_freeform_direction
- evidence: user freeform review, YMM4 screenshots, local diagnostic render observations, current diagnostic SVG/PNG card assets
- evidence_not_yet: L2_reference_pack, L3_proxy_metric_pass, L4_target_viewer_feedback, L5_actual_analytics
- unknowns: actual target viewer preference, retention or CTR, target viewer comprehension outside the project, production visual quality

## Reference / Benchmark Abstraction

- reference_pack_status: needed_or_deferred
- no_copy_policy: do not copy reference images, logos, brands, screenshots, or current YouTube-specific material
- candidate_reference_types: Japanese explainer video card, TV info-board style, YouTube news commentary simple panel, educational slide-like callout
- extracted_grammar_hypotheses: large headline or role label before detail, one dominant visual motif per card, simple block hierarchy over dense dashboard chips, diagnostic/fake boundary visible without footnote reading
- hypotheses_not_market_proof: True

## Proxy Metrics

| metric | pass | fail | unknown |
|---|---|---|---|
| readability_at_a_glance | card role and dominant message are understandable in about 3 seconds | viewer must pause, inspect tiny text, or infer from metadata | no benchmark evaluation has been run against current cards yet |
| text_clipping_wrapping | no meaningful text is clipped and wrapping preserves readable phrases | meaningful label, headline, or body text is clipped or awkwardly wrapped | render compression and final placement are not benchmarked here |
| minimum_meaningful_font_size | essential meaning uses the current 34px or larger card text floor | essential meaning depends on text below the 34px floor or footer microcopy | apparent size after video compression still needs evaluation |
| one_dominant_message_per_card | each card has one primary point before secondary labels | multiple equal-weight messages compete for attention | viewer comprehension outside the project is not measured |
| familiar_explainer_tv_youtube_grammar | layout resembles large-block explainer, TV info-board, or simple YouTube panel grammar | layout reads mainly as SaaS dashboard, audit UI, or dense internal tool | reference pack is needed before calling this market-proven |
| no_tiny_metadata_dependency | small metadata is decorative or diagnostic, not required for core meaning | role, claim, fake boundary, or next action depends on tiny metadata | requires card-by-card benchmark evaluation |
| card_to_card_role_variation | cards have visibly different roles, motifs, and reading order | cards feel like repeated panels with swapped text | variation has not yet been judged against this benchmark |
| pacing_density_68_sec | density can be understood during normal 68 sec playback | viewer must frame-step or pause because density exceeds pacing | current benchmark is not a new render or playback review |
| diagnostic_boundary_visibility | fake/review-only boundary is visible without reading tiny footnotes | card could be mistaken for real news, source proof, or public claim | needs evaluation on current cards and any future render surface |
| no_real_brand_url_public_claim | no real brand, URL, real screenshot, or public-readiness claim is present | real external identity or production/public claim appears | none for the current committed card assets; recheck future edits |

## Acceptance Criteria

- must: no clipped meaningful text, no tiny metadata carrying essential meaning, one dominant message per card, card role understood within about 3 seconds, diagnostic/fake boundary visible
- should: familiar large-block layout, visible role variation, simple labels, limited decorative noise
- must_not: claim production/public readiness, claim actual audience acceptance, use real brand, URL, or news screenshot, use render as vague visual exploration

## Next Visual Iteration Mapping

| future change | benchmark criteria |
|---|---|
| enlarge source/footer text | readability_at_a_glance, no_tiny_metadata_dependency |
| simplify card role labels | one_dominant_message_per_card |
| differentiate card composition | card_to_card_role_variation |
| reduce SaaS-like chips | familiar_explainer_tv_youtube_grammar |
| add simple visual motif | readability_at_a_glance, one_dominant_message_per_card |
| adjust pacing/density after review | pacing_density_68_sec |

## Review Protocol

- ask_user_after: benchmarked evaluation, material visual change
- look_for: Can the card role be understood within a few seconds?, Is any meaningful text too small or clipped?, Does the visual feel familiar enough for an explanatory YouTube video?
- answer_style: freeform
- schema_owner: Agent/Supervisor
- form_required: False

## Visual Benchmark Gate

- status: draft
- visual_work_class: audience_fit
- benchmark_status: defined_not_applied
- evidence_level: L1_user_freeform_direction
- proxy_metrics: 10 defined, current_cards_evaluated=False
- unknowns: actual audience preference, target viewer comprehension, production visual quality, retention or CTR
- next_iteration_allowed: True
- next_iteration_allowed_scope: newsroom-audience-fit-benchmark-evaluation-v1
- visual_refinement_allowed_before_evaluation: False

## Recommended Next Slice

- default: newsroom-audience-fit-benchmark-evaluation-v1
- reason: apply this benchmark to the current cards once before any further redesign

## Alternative Next Slices

| slice | condition |
|---|---|
| newsroom-visual-card-benchmarked-refinement-v1 | only if benchmark evaluation finds concrete failures |
| newsroom-reference-pack-visual-grammar-v1 | only if the benchmark cannot be completed without reference abstraction |
| newsroom-internal-review-v0.1-operator-review-card | only if benchmark evaluation says current cards are sufficient for diagnostic review |

## Completion Matrix

| item | status |
|---|---|
| current_repo_state_verified | True |
| audience_fit_incident_normalized | True |
| visual_benchmark_spec_created | True |
| proxy_metrics_and_unknowns_defined | True |
| next_benchmark_linked_slice_named | True |
| narrow_commit_created_and_pushed_if_push_gate_passes | pending_until_git_gate |

## Artifact Readiness

| item | status |
|---|---|
| benchmark_json_exists | True |
| human_doc_exists | True |
| proxy_metrics_present | True |
| unmeasurable_audience_acceptance_boundary_present | True |
| review_protocol_present | True |
| downstream_next_use_described | True |

## Render Gate Hygiene

| item | status |
|---|---|
| no_render_performed | True |
| render_not_used_for_vague_visual_guessing | True |
| next_render_tied_to_benchmark_linked_material_change | True |
| no_render_for_docs_benchmark_only_change | True |
| repeated_render_loop_avoided | True |
| output_first_principle_preserved | True |

## Human Burden Hygiene

| item | status |
|---|---|
| user_input | freeform |
| template_required | False |
| schema_owner | Agent/Supervisor |
| user_side_work_for_this_slice | none |
| future_review_look_for_count | 3 |
| negative_confirmation_checklist | False |
| fixed_form_relapse | False |

## Review Non-Redundancy

| item | status |
|---|---|
| latest_user_correction_consumed_once | True |
| prior_visual_reviews_reused | True |
| next_axis_stated_as_benchmark | True |
| not_accepted_scope_preserved | True |
| repeated_user_review_requested | False |
| mechanics_re_review_requested | False |

## Inertia Check

| item | status |
|---|---|
| ad_hoc_visual_iteration_stopped | True |
| packet_for_packet_drift | False |
| readback_only_stall | False |
| readiness_separated_from_slice_completion | True |
| next_concrete_benchmark_linked_milestone | newsroom-audience-fit-benchmark-evaluation-v1 |

## Boundary

- TTS_generated_by_agent: False
- YMM4_launched_by_agent: False
- actual_audience_acceptance_claimed: False
- audio_generated_by_agent: False
- cards_regenerated_in_this_slice: False
- external_fetch_performed: False
- production_visual_quality_accepted: False
- public_video_ready: False
- real_media_imported: False
- video_render_created_by_agent: False
- ymmp_edited_by_agent: False

## Downstream Next Use

- default_slice: newsroom-audience-fit-benchmark-evaluation-v1
- instruction: score the current cards against the proxy metrics before any further visual redesign
- evaluation_subject: current four diagnostic SVG/PNG cards
- refinement_gate: only concrete benchmark failures may drive a later benchmarked refinement
