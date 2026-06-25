# Newsroom YMM4 Card Asset Placement Probe v1

artifact_id: newsroom_yym4_card_asset_placement_probe_v1_2026_06_25
probe_id: newsroom_yym4_card_asset_placement_probe_v1_2026_06_25
schema_version: newsroom_yym4_card_asset_placement_probe.v1
review_status: ready_for_supervisor_review
production_status: diagnostic_only
probe_status: placed_structurally
diagnostic_only: true

## Identity

- probe_id: newsroom_yym4_card_asset_placement_probe_v1_2026_06_25
- source_visual_card_bridge_path: samples/_probe/newsroom_handoff/visual_card_asset_bridge_v1.json
- source_render_smoke_result_path: samples/_probe/newsroom_handoff/ymmp_timing_patch_render_smoke_result_readback_v1.json
- source_timing_patch_probe_path: samples/_probe/newsroom_handoff/ymmp_timing_patch_probe_v1.json
- source_ymmp_local_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_timing_patch_v1.ymmp
- patched_ymmp_local_path: _tmp/newsroom_manual_probe/diagnostic_bound_speaker_probe_card_placement_v1.ymmp
- production_status: diagnostic_only
- probe_status: placed_structurally
- observation_source: repo_structural_probe_without_yym4_launch

## Source Validation

- status: passed
- errors: []
- source_visual_card_bridge_id: newsroom_visual_card_asset_bridge_v1_2026_06_25
- source_render_smoke_result_id: newsroom_ymmp_timing_patch_render_smoke_result_readback_v1_2026_06_25
- source_timing_patch_probe_id: newsroom_ymmp_timing_patch_probe_v1_2026_06_24
- render_smoke_result: pass
- duration_sec: 68
- native_audio_present: true
- source_ymmp_exists: true
- patched_ymmp_exists: true
- source_dialogue_item_count: 4
- patched_dialogue_item_count: 4
- source_card_asset_count: 4
- png_file_count: 4
- image_item_schema_source: existing_repo_overlay_builder_and_tracked_ymmp_samples
- canonical_speaker: yukkuri_reimu
- canonical_speaker_unicode_escape: \u3086\u3063\u304f\u308a\u970a\u5922

## Source Assets

| card_id | timing | dialogue | svg | png |
|---|---:|---|---|---|
| visual_card_cap_beat_fake_intro_001_01_v1 | 0-12s | Fake topic, review only. | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_01_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_01_v1.png |
| visual_card_cap_beat_fake_intro_001_02_v1 | 12-24s | Review-only handoff stays. | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_02_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_intro_001_02_v1.png |
| visual_card_cap_beat_fake_claim_001_01_v1 | 24-46s | A fake claim is shown. | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_01_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_01_v1.png |
| visual_card_cap_beat_fake_claim_001_02_v1 | 46-68s | Fake source checks are noted. | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_02_v1.svg | samples/_probe/newsroom_handoff/visual_cards_v1/visual_card_cap_beat_fake_claim_001_02_v1.png |

## Raster Export

- png_export_status: generated
- rasterization_method: existing_toolchain
- deterministic_export: true
- png_files_generated_in_this_slice: true
- png_file_count: 4
- expected_png_file_count: 4
- asset_dimensions: 1920x1080
- source_format: svg
- target_format: png
- external_fetch_performed: false
- real_media_dependency: false
- errors: []

## Placement Operations

| operation_id | frame | length | target | applied |
|---|---:|---:|---|---|
| add_image_item_visual_card_cap_beat_fake_intro_001_01_v1 | 0 | 720 | Layer 2 / ImageItem | true |
| add_image_item_visual_card_cap_beat_fake_intro_001_02_v1 | 720 | 720 | Layer 2 / ImageItem | true |
| add_image_item_visual_card_cap_beat_fake_claim_001_01_v1 | 1440 | 1320 | Layer 2 / ImageItem | true |
| add_image_item_visual_card_cap_beat_fake_claim_001_02_v1 | 2760 | 1320 | Layer 2 / ImageItem | true |

## Preservation Checks

- timeline_duration_preserved: true
- dialogue_items_preserved: true
- native_audio_fields_preserved: true
- speaker_preserved: true
- source_dialogue_item_count: 4
- patched_dialogue_item_count: 4
- direct_yym4_card_object_graph: false
- yym4_text_shape_reconstruction: false
- external_TTS_introduced: false
- render_created: false
- media_committed: false

## Structural Result

- patched_ymmp_created_locally: true
- patched_ymmp_committed: false
- visual_assets_committed: true
- card_item_count_added_or_planned: 4
- card_image_item_count_observed: 4
- placement_structural_readback_status: pass
- next_render_trigger: newsroom-card-placement-render-smoke-v1

## Accepted Scope

- external_visual_card_assets_are_placement_mapped: true
- cards_are_placed_into_ignored_yym4_diagnostic_copy: true
- direct_yym4_card_object_graph_construction_avoided: true
- native_audio_timing_proofs_preserved: true
- png_card_assets_generated_from_existing_svg: true
- timing_patch_duration_preserved: true

## Not Accepted Scope

- production_visual_quality: false
- final_design_system: false
- post_card_render_proof: false
- public_video_readiness: false
- real_newsroom_visuals: false
- real_content_readiness: false
- production_approval: false

## Readiness Separation

- slice_completion: pass_for_this_placement_probe
- video_readiness_progress: 6/7
- video_readiness_current: card_assets_structurally_placed_in_ignored_yym4_copy
- video_readiness_next_missing_gate: post-placement render smoke and internal review milestone
- visual_readiness_progress: 6/7
- visual_readiness_current: YMM4 image placement proof exists structurally
- production_readiness: low_diagnostic_only
- production_readiness_reason: The probe uses fake PNG card assets and an ignored local YMM4 copy; it does not prove post-card render output or production quality.
- next_default_slice: newsroom-card-placement-render-smoke-v1

## Recommended Next Slices

| slice | timing | reason |
|---|---|---|
| newsroom-card-placement-render-smoke-v1 | recommended_next_default | structural placement passed, so the next meaningful gate is a milestone render smoke of the changed video surface |
| newsroom-visual-card-raster-export-v1 | only_if_png_export_missing | use only when compatible raster assets are unavailable |
| newsroom-yym4-image-item-schema-audit-v1 | only_if_image_item_schema_becomes_unsafe | audit ImageItem fields before mutating any YMM4 copy |
| newsroom-internal-review-v0.1-prep | later_after_card_placement_render_smoke | prepare v0.1 review once the rendered visual surface is observed |

## Goal Stack

| level | goal | success signal | contribution |
|---|---|---|---|
| Immediate | Place or prepare external card assets for YMM4 image placement | placement probe JSON/readback shows card assets mapped without direct object graph reconstruction | moves visual axis from asset-only to YMM4-placement-ready |
| Short-term | Prepare post-card render smoke | ignored .ymmp copy structurally includes card images | makes the next render milestone meaningful |
| Mid-term | Reach internal review v0.1 | 68sec video has native audio, timing, and visible cards | enables useful human review |
| Long-term | Stabilize Newsroom-to-video pipeline | content packet can drive script, audio, timing, and visual assets repeatably | reduces manual assembly |

## Completion Matrix

| item | status |
|---|---|
| current_repo_state_verified | true |
| visual_card_assets_inspected | true |
| raster_export_readiness_determined | true |
| placement_plan_probe_created | true |
| structural_readback_or_clean_block_recorded | true |
| narrow_commit_created_and_pushed_if_push_gate_passes | pending_until_git_gate |

## Artifact Readiness

| item | status |
|---|---|
| placement_probe_json | present |
| human_readback | present |
| asset_mapping | present |
| placement_operations_or_clean_block | applied |
| preservation_checks | present |
| downstream_next_use | present |

## Video Readiness

| item | status |
|---|---|
| source_input_path_proven | true |
| target_yym4_import_path_proven | true |
| audio_path_proven | true |
| timing_duration_strategy_defined | true |
| tiny_smoke_render_observed | true |
| targeted_regression_render_observed | true |
| internal_review_milestone_reached | false |

## Visual Readiness

| item | status |
|---|---|
| visual_card_concept_selected | true |
| external_card_assets_generated | true |
| preview_contact_sheet_available | true |
| assets_mapped_to_timeline_caption_units | true |
| yym4_placement_contract_defined | true |
| yym4_placement_proof_observed | true |
| post_placement_render_reviewed | false |

## Render Gate Hygiene

| item | status |
|---|---|
| video_render_performed_in_this_slice | false |
| existing_render_evidence_reused | true |
| render_treated_as_milestone_gated | true |
| next_render_tied_to_successful_card_placement | true |
| no_render_for_docs_readback_changes | true |
| repeated_timing_audio_render_check_avoided | true |

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
| prior_timing_proof_reused | true |
| prior_audio_evidence_reused | true |
| prior_render_smoke_result_reused | true |
| next_axis_stated_as_visual_placement | true |
| not_accepted_scope_preserved | true |
| repeated_timing_audio_render_review_requested | false |

## Inertia Check

| item | status |
|---|---|
| packet_for_packet_drift | false |
| readback_only_stall | false |
| repeated_render_request | false |
| product_video_visual_readiness_separated_from_slice_completion | true |
| next_concrete_milestone | newsroom-card-placement-render-smoke-v1 |

## Placement Contract

- placement_mode: image_asset_import
- yym4_item_type: ImageItem
- card_asset_format: png
- source_card_format: svg
- target_layer: 2
- direct_yym4_card_object_graph: false
- yym4_text_shape_reconstruction: false
- preserves_native_audio_path: true
- preserves_existing_timing_strategy: true
- render_required_in_this_slice: false
- YMM4_launch_required_in_this_slice: false
- ymmp_mutation_boundary: ignored local diagnostic copy only
- next_render_should_be_milestone_gated: true
- no_render_for_docs_readback_policy_only_changes: true

## Boundary

- YMM4_launched_by_agent: false
- video_render_created_by_agent: false
- audio_generated_by_agent: false
- TTS_generated_by_agent: false
- external_TTS_introduced: false
- real_media_imported: false
- external_source_fetch_performed: false
- real_urls_or_real_brands_used: false
- production_ymmp_edited_or_committed: false
- ignored_ymmp_staged_or_committed: false
- render_output_staged_or_committed: false
- production_approval: false
- public_video_ready: false
- dashboard_governance_freshness_changed: false

## Boundary Note

This probe proves structural image-asset placement in the ignored diagnostic YMM4 copy only. It preserves the prior native audio and 68 second timing evidence, avoids direct YMM4 text/shape card reconstruction, and leaves post-placement render smoke, internal review, real newsroom visuals, and production approval to later milestones.
