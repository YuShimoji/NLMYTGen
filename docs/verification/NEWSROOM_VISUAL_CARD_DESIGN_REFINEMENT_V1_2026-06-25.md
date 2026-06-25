# Newsroom Visual Card Design Refinement v1

artifact_id: newsroom_visual_card_design_refinement_v1_2026_06_25
refinement_id: newsroom_visual_card_design_refinement_v1_2026_06_25
schema_version: newsroom_visual_card_design_refinement.v1
refinement_status: assets_regenerated
production_status: diagnostic_only

## Identity

- refinement_id: newsroom_visual_card_design_refinement_v1_2026_06_25
- source_internal_review_result_readback_path: samples/_probe/newsroom_handoff/internal_review_v0_1_result_readback_v1.json
- source_internal_review_result_readback_id: newsroom_internal_review_v0_1_result_readback_v1_2026_06_25
- source_visual_card_bridge_path: samples/_probe/newsroom_handoff/visual_card_asset_bridge_v1.json
- source_cards_dir: samples/_probe/newsroom_handoff/visual_cards_v1
- output_cards_dir: samples/_probe/newsroom_handoff/visual_cards_v1
- source_card_render_result_path: samples/_probe/newsroom_handoff/card_placement_render_smoke_result_readback_v1.json
- source_card_render_result_id: newsroom_card_placement_render_smoke_result_readback_v1_2026_06_25
- production_status: diagnostic_only

## Design Token Constraints

- canvas_size: {"height": 1080, "width": 1920}
- safe_margin: 96
- title_font_size: 46
- headline_font_size: 54
- body_font_size: 34
- chip_font_size: 28
- meta_font_size: 30
- minimum_font_size: 28
- maximum_font_size: 54
- max_title_lines: 2
- max_headline_lines: 2
- body_max_lines: 3
- body_wrap_width: 940
- subtitle_safe_reserve: {"height": 116, "width": 1696, "x": 112, "y": 812}
- footer_debug_treatment: removed_from_review_surface
- real_brand_or_url_present: false
- production_claim_present: false
- text_wrapping_required: true
- source_metadata_wrap_required: true
- card_variation_required: role_specific_layout_motif

## Card Changes

| card | role | motif | wrap | clipping guard | svg | png |
|---|---|---|---|---|---|---|
| visual_card_cap_beat_fake_intro_001_01_v1 | intro_summary | summary_stack | true | true | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_01_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_01_v1.png |
| visual_card_cap_beat_fake_intro_001_02_v1 | handoff_process | process_ladder | true | true | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_02_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_02_v1.png |
| visual_card_cap_beat_fake_claim_001_01_v1 | claim_check | check_matrix | true | true | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_01_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_01_v1.png |
| visual_card_cap_beat_fake_claim_001_02_v1 | source_status_next_action | status_panel | true | true | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_02_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_02_v1.png |

## Accepted Scope

- review_findings_captured: true
- external_card_assets_refined: true
- text_clipping_reduced_by_generator_rules: true
- wrapping_clamping_rules_introduced: true
- card_variation_increased: true
- assets_ready_for_later_yym4_placement_render_smoke: true

## Not Accepted Scope

- production_visual_quality: false
- final_design_system: false
- YMM4_placement_proof_after_refinement: false
- post_refinement_render_proof: false
- public_video_readiness: false
- real_newsroom_visuals: false
- real_content_readiness: false
- production_approval: false

## Next Recommended Slice

- slice: newsroom-card-placement-post-refinement-render-smoke-v1
- reason: asset paths are stable and PNGs were regenerated, so the next milestone is a post-refinement render-smoke observation

## Recommended Next Slices

| slice | timing | reason |
|---|---|---|
| newsroom-card-placement-post-refinement-render-smoke-v1 | recommended_next_default | stable SVG/PNG asset paths are regenerated; the existing ignored placement project should now reference the improved PNGs |
| newsroom-yym4-card-asset-placement-refresh-v1 | only_if_existing_placement_paths_are_not_stable | refresh ImageItem placement only if stable PNG paths cannot be reused |
| newsroom-internal-review-v0.1-prep | after_post_refinement_smoke | internal review is meaningful after the changed visual surface is observed |
| newsroom-rss-dry-run-integration-plan-v1 | later_not_immediate | real packet integration should wait until the visual baseline is accepted |

## Goal Stack

| level | goal | success signal | contribution |
|---|---|---|---|
| Immediate | Convert internal review into actionable visual refinement | review readback and refined assets exist | avoids a vague review loop |
| Short-term | Improve card readability and variation | no obvious clipping, better type scale, differentiated cards | makes next render review meaningful |
| Mid-term | Prepare post-refinement render smoke | stable PNG assets can be reused by placement .ymmp | moves toward internal review acceptance |
| Long-term | Establish reusable card design baseline | future packets can use readable card templates | supports automation |

## Completion Matrix

| item | status |
|---|---|
| current_repo_state_verified | true |
| internal_review_observation_normalized | true |
| current_card_issues_inspected | true |
| refined_card_assets_generated | true |
| preview_contact_sheet_updated | true |
| narrow_commit_created_and_pushed_if_push_gate_passes | pending_until_git_gate |

## Artifact Readiness

| item | status |
|---|---|
| review_result_readback | present |
| visual_refinement_json | present |
| human_docs | present |
| refined_svg_png_assets | present |
| contact_sheet_preview | present |
| downstream_next_use | present |

## Visual Readiness

| item | status |
|---|---|
| visual_card_concept_selected | true |
| external_card_assets_generated | true |
| preview_contact_sheet_available | true |
| assets_mapped_to_timeline_caption_units | true |
| yym4_placement_contract_defined | true |
| yym4_placement_proof_observed | true |
| post_refinement_render_reviewed | false |

## Render Gate Hygiene

| item | status |
|---|---|
| render_performed_in_this_slice | false |
| existing_render_review_evidence_reused | true |
| render_treated_as_milestone_gated | true |
| next_render_tied_to_visual_card_design_surface_change | true |
| no_render_for_docs_readback_changes | true |
| repeated_timing_audio_review_avoided | true |

## Human Burden Hygiene

| item | status |
|---|---|
| user_input | freeform |
| template_required | false |
| schema_owner | Agent |
| user_side_work_for_this_slice | none |
| negative_confirmation_checklist | false |
| fixed_form_relapse | false |
| repeated_review_request | false |

## Review Non-Redundancy

| item | status |
|---|---|
| prior_internal_review_observation_consumed_once | true |
| prior_render_evidence_reused | true |
| next_axis_stated_as_visual_refinement | true |
| not_accepted_scope_preserved | true |
| repeated_user_review_requested | false |
| mechanics_re_review_requested | false |

## Inertia Check

| item | status |
|---|---|
| packet_for_packet_drift | false |
| readback_only_stall | false |
| repeated_render_request | false |
| readiness_separated_from_slice_completion | true |
| next_concrete_milestone | newsroom-card-placement-post-refinement-render-smoke-v1 |

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

The assets are improved diagnostic cards only. The stable PNG paths make a later post-refinement smoke meaningful, but production visual quality, final design, real content, and public readiness stay closed.
