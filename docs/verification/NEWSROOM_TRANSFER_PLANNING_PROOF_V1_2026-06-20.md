# Newsroom Transfer Planning Proof

status: blocked
transfer_status: blocked
validator_status: passed
slot_linkage_status: passed_with_warnings
review_console_visibility_status: documented_read_only
packet_path: samples/_probe/newsroom_handoff/minimal_episode_packet.json
slot_linkage_path: samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json
review_console_doc_path: docs/verification/NEWSROOM_REVIEW_CONSOLE_CONSUMER_V1_2026-06-20.md
artifact_id: newsroom_handoff_minimal_episode_packet_v1
episode_id: fake-newsroom-episode-0001
title: Placeholder Policy Explainer Episode
contract_version: newsroom-to-nlmytgen-handoff-v1.11

## Transfer Candidate Summary

Not a transfer candidate yet: transfer remains blocked until rights, media/source availability, review approval, visual readiness, and downstream/YMM4 readiness blockers are cleared.

## Input Counts
- g28_slot_hints: 4
- review_warnings: 2
- script_beats: 3
- slot_linkage_rows: 4
- source_notes: 2
- visual_plan: 2
- visual_slot_gaps: 2

## Transfer Blockers
### rights/provenance
- rights_clearance_not_cleared: rights_summary.clearance_state=synthetic_fixture_only (rights_summary.clearance_state)
- rights_summary_blocks_ymm4_transfer: rights_summary.blocked_uses includes YMM4_transfer (rights_summary.blocked_uses)
- rights_risk_flags_present: rights_summary.risk_flags=not_publishable,no_approved_media_assets (rights_summary.risk_flags)
### media/source availability
- raw_source_material_not_included: provenance.raw_source_material_included is false or missing (provenance.raw_source_material_included)
- placeholder_source_notes_only: placeholder source notes: src_fake_001,src_fake_002 (source_notes)
### review approval
- review_warning_blocks_transfer:rw_001: Synthetic fixture rights block publication, render, and YMM4 transfer. (review_warnings.rw_001)
- review_warning_blocks_transfer:rw_002: Visuals are placeholders and require approved media or abstract replacements before transfer planning. (review_warnings.rw_002)
- review_console_is_read_only: review_console_visibility_status=documented_read_only (docs/verification/NEWSROOM_REVIEW_CONSOLE_CONSUMER_V1_2026-06-20.md)
### visual readiness
- visual_assets_placeholder_only: placeholder visuals: vis_001,vis_002 (visual_plan.asset_policy)
- visual_slot_gaps_present: visuals with unhinted slots: vis_001,vis_002 (g28_slot_linkage_readback.visual_slot_gaps)
### downstream/YMM4 readiness
- validator_transfer_status_blocked: validator transfer_status=blocked (validator.transfer_status)
- slot_linkage_transfer_status_blocked: slot-linkage transfer_status=blocked (g28_slot_linkage_readback.transfer_status)
- ymm4_transfer_ready_false: downstream_readiness.ymm4_transfer_ready=false (downstream_readiness.ymm4_transfer_ready)
- downstream_blocking_reasons_present: blocking_reasons=synthetic_fixture_not_publishable,rights_summary_blocks_transfer,no_approved_media_assets (downstream_readiness.blocking_reasons)

## Unlock Requirements
- [rights/provenance] Record cleared rights or an explicit limited-use clearance before any transfer candidate review. (current: rights_summary.clearance_state=synthetic_fixture_only; fields: rights_summary.clearance_state)
- [rights/provenance] Remove YMM4_transfer from blocked uses only after rights/provenance review permits a limited downstream handoff. (current: rights_summary.blocked_uses includes YMM4_transfer; fields: rights_summary.blocked_uses)
- [rights/provenance] Resolve or explicitly waive rights risk flags before transfer planning. (current: rights_summary.risk_flags=not_publishable,no_approved_media_assets; fields: rights_summary.risk_flags)
- [media/source availability] Provide approved source media metadata or approved abstract replacement evidence before limited transfer can be considered. (current: provenance.raw_source_material_included is false or missing; fields: provenance.raw_source_material_included)
- [media/source availability] Replace placeholder-only source notes with approved, sanitized packet metadata from the upstream newsroom export. (current: placeholder source notes: src_fake_001,src_fake_002; fields: source_notes)
- [review approval] Resolve the blocking review warning and record a freeform human review outcome before transfer-candidate review. (current: Synthetic fixture rights block publication, render, and YMM4 transfer.; fields: review_warnings.rw_001)
- [review approval] Resolve the blocking review warning and record a freeform human review outcome before transfer-candidate review. (current: Visuals are placeholders and require approved media or abstract replacements before transfer planning.; fields: review_warnings.rw_002)
- [review approval] Add a separate planning approval/readiness outcome; the current Review Console consumer is visibility only. (current: review_console_visibility_status=documented_read_only; fields: docs/verification/NEWSROOM_REVIEW_CONSOLE_CONSUMER_V1_2026-06-20.md)
- [visual readiness] Replace placeholder-only visual plans with approved media, approved abstract replacements, or an explicit no-media visual route. (current: placeholder visuals: vis_001,vis_002; fields: visual_plan.asset_policy)
- [visual readiness] Close or explicitly defer unhinted visual content slots before transfer-candidate review. (current: visuals with unhinted slots: vis_001,vis_002; fields: g28_slot_linkage_readback.visual_slot_gaps)
- [downstream/YMM4 readiness] Clear validator blockers before any limited transfer can be considered. (current: validator transfer_status=blocked; fields: validator.transfer_status)
- [downstream/YMM4 readiness] Clear slot-linkage blockers and warnings before transfer-candidate review. (current: slot-linkage transfer_status=blocked; fields: g28_slot_linkage_readback.transfer_status)
- [downstream/YMM4 readiness] Keep YMM4 transfer closed until all upstream rights, media, review, visual, and slot-linkage blockers are resolved. (current: downstream_readiness.ymm4_transfer_ready=false; fields: downstream_readiness.ymm4_transfer_ready)
- [downstream/YMM4 readiness] Remove downstream blocking reasons only after their source blockers are resolved. (current: blocking_reasons=synthetic_fixture_not_publishable,rights_summary_blocks_transfer,no_approved_media_assets; fields: downstream_readiness.blocking_reasons)

## Contradiction Checks
- transfer_ready_with_blockers: pass / info - No ready transfer claim conflicts with current blockers.
- rights_media_missing_but_readiness_claims_true: warn / warning - Readiness fields true while rights/media blockers remain: g28_slot_mapping_ready,notebooklm_seed_ready,review_surface_ready,scriptir_mapping_ready,visualir_mapping_ready
- review_approval_absent_but_production_transfer_implied: pass / info - No production transfer approval is implied.
- slot_linkage_readback_required: pass / info - Slot-linkage readback exposes status, transfer status, and rows.

## Prohibited Next Actions
- .ymmp generation
- YMM4 carrier generation
- render generation
- external fetch
- production approval
- rights approval
- public-use approval

## Allowed Next Actions
- Review Console planning panel
- real packet readiness checklist
- fixture/schema refinement
- rights/provenance field review
- approved media or abstract replacement planning

## Errors
- none

## Warnings
- MISSING_G28_SLOT_HINT: vis_001->callout_box,caption_reserve
- MISSING_G28_SLOT_HINT: vis_002->label_chip,source_note
- READINESS_TRUE_WITH_RIGHTS_OR_MEDIA_BLOCKERS

## Boundary

This proof is diagnostic planning only. It does not generate `.ymmp`, YMM4 carriers, renders, external fetches, production approvals, rights approvals, or publication outputs.

next_use: Use this proof as a non-YMM4 planning gate before a future read-only Review Console planning panel or real-packet readiness checklist.

## Validation Readback

- JSON parse: `samples/_probe/newsroom_handoff/minimal_episode_packet.json`, `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json`, and `samples/_probe/newsroom_handoff/transfer_planning_readback.json`
- Validator: `uv run python -m src.cli.main validate-newsroom-handoff samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Slot-linkage proof: `uv run python -m src.cli.main prove-newsroom-g28-slot-linkage samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Transfer-planning proof: `uv run python -m src.cli.main plan-newsroom-transfer samples/_probe/newsroom_handoff/minimal_episode_packet.json --slot-linkage samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json --format json`
- Focused tests: `uv run --with pytest pytest tests/test_newsroom_handoff_validator.py`
- Expected focused test result: `19 passed`
- Expected transfer-planning result: `status=blocked`, `transfer_status=blocked`, `errors=0`
