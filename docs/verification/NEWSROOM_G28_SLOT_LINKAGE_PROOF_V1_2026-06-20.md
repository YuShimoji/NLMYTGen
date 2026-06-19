# Newsroom G-28 Slot Linkage Proof

status: passed_with_warnings
validator_status: passed
transfer_status: blocked
packet_path: samples/_probe/newsroom_handoff/minimal_episode_packet.json
artifact_id: newsroom_handoff_minimal_episode_packet_v1
episode_id: fake-newsroom-episode-0001
contract_version: newsroom-to-nlmytgen-handoff-v1.11
readback_artifact: newsroom_g28_slot_linkage_proof_v1_2026_06_20

## Linkages

| Beat | Visual | Slot | Sources | Slot ok | Review surface | Transfer |
| --- | --- | --- | --- | --- | --- | --- |
| beat_001 | vis_001 | screenshot_slot | src_fake_001 | yes | samples/_probe/g28/reference_layout_prototypes/screenshot_callout.html | blocked |
| beat_001 | vis_001 | source_note | src_fake_001 | yes | samples/_probe/g28/reference_layout_prototypes/screenshot_callout.html | blocked |
| beat_002 | vis_002 | quote_card | src_fake_001, src_fake_002 | yes | samples/_probe/g28/reference_layout_prototypes/article_quote_card.html | blocked |
| beat_002 | vis_002 | caption_reserve | src_fake_001, src_fake_002 | yes | samples/_probe/g28/reference_layout_prototypes/article_quote_card.html | blocked |

## Visual Slot Gaps
- vis_001: missing hints for callout_box, caption_reserve
- vis_002: missing hints for label_chip, source_note

## Warnings
- MISSING_G28_SLOT_HINT: vis_001->callout_box,caption_reserve
- MISSING_G28_SLOT_HINT: vis_002->label_chip,source_note

## Errors
- none

## YMM4 Transfer Blockers
- downstream_blocking_reason:no_approved_media_assets
- downstream_blocking_reason:rights_summary_blocks_transfer
- downstream_blocking_reason:synthetic_fixture_not_publishable
- review_warning_blocks_ymm4:rw_001
- review_warning_blocks_ymm4:rw_002
- rights_clearance_not_cleared:synthetic_fixture_only
- rights_summary_blocks_ymm4_transfer

## Boundary

This is diagnostic/readback only. It does not implement Review Console UI, create YMM4 artifacts, approve production visuals, fetch sources, or change rights state.

next_use: Use this proof as a UI-independent readback before a future Review Console consumer or G-28 transfer-planning slice.

## Validation Readback

- JSON parse: `samples/_probe/newsroom_handoff/minimal_episode_packet.json` and `samples/_probe/newsroom_handoff/g28_slot_linkage_readback.json`
- Validator: `uv run python -m src.cli.main validate-newsroom-handoff samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Proof generation: `uv run python -m src.cli.main prove-newsroom-g28-slot-linkage samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`
- Focused tests: `uv run --with pytest pytest tests/test_newsroom_handoff_validator.py`
- Expected focused test result: `14 passed`
