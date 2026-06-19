# Newsroom Handoff Validator v1 - 2026-06-20

Artifact id: `newsroom_handoff_validator_v1_2026_06_20`

This readback records the first lightweight validator for the
`newsroom-yt-pipeline -> NLMYTGen` handoff contract.

## Scope

The validator checks a portable packet boundary only. It does not fetch
sources, scrape pages, call external APIs, open the Newsroom repository, copy
real news material, generate `.ymmp`, create render outputs, approve rights, or
mark YMM4 transfer ready.

## Implemented Artifacts

| Artifact | Path | Purpose |
| --- | --- | --- |
| validator module | `src/pipeline/newsroom_handoff_validator.py` | Fail-closed structure and reference checks for a newsroom handoff packet. |
| CLI command | `python -m src.cli.main validate-newsroom-handoff [packet.json] [--format text\|json]` | Human-readable or machine-readable readback. |
| focused tests | `tests/test_newsroom_handoff_validator.py` | Fixture pass, missing-field failure, unknown G-28 slot failure, broken reference failure, contradictory readiness failure, and CLI behavior. |
| fixture | `samples/_probe/newsroom_handoff/minimal_episode_packet.json` | Synthetic non-fetching packet used by this slice. |

## Validation Coverage

The validator currently checks:

- top-level identity and required packet fields
- non-empty `source_notes`, `script_beats`, `visual_plan`,
  `g28_slot_hints`, and `review_warnings`
- `notebooklm_packet` seed presence
- source ids, beat ids, visual ids, and G-28 slot hint ids
- script beat evidence refs resolve to known source ids
- visual plan beat refs resolve to known beat ids
- visual content slots and G-28 object catalog slots use the known G-28 slot set
- G-28 hint visual refs and source refs resolve
- provenance and rights summary fields needed for transfer gating
- blocking `review_warnings`
- `downstream_readiness.ymm4_transfer_ready`
- contradiction where YMM4 transfer is marked ready while blockers exist
- fail-closed transfer status when required packet structure is invalid

## G-28 Slot Set

The allowed slot set mirrors the G-28 object catalog:

`image_slot`, `screenshot_slot`, `footage_slot`, `highlight_box`, `arrow`,
`leader_line`, `label_chip`, `callout_box`, `lower_third_telop`,
`source_note`, `quote_card`, `comparison_panel`, `table_row`,
`host_placeholder`, and `caption_reserve`.

## Fixture Readback

Command:

`uv run python -m src.cli.main validate-newsroom-handoff samples/_probe/newsroom_handoff/minimal_episode_packet.json --format json`

Result summary:

- validator status: `passed`
- transfer status: `blocked`
- source notes: 2
- script beats: 3
- visual plans: 2
- G-28 slot hints: 4
- review warnings: 2
- observed slots: `caption_reserve`, `quote_card`, `screenshot_slot`, `source_note`
- YMM4 transfer ready: `false`

The fixture passes structure validation but stays blocked for YMM4 transfer
because it is synthetic-only, has no approved media assets, carries blocking
review warnings, and explicitly lists transfer blockers in
`downstream_readiness.blocking_reasons`.

## Test Readback

Command:

`uv run pytest tests/test_newsroom_handoff_validator.py`

Result:

`8 passed`

## Downstream Next Use

Use this command as a pre-ingest structure gate before any later ScriptIR-like,
VisualIR, G-28 linkage, or YMM4 transfer planning slice:

`uv run python -m src.cli.main validate-newsroom-handoff --format text`

This validator is intentionally not a full production ingest adapter. A future
slice can expand from this into a deeper G-28 linkage proof or Review Console
surface while keeping real source intake upstream.

## Boundary Confirmation

This slice adds a validator, tests, and docs only. It does not modify
`newsroom-yt-pipeline`, fetch sources, include real URLs or copyrighted article
text, touch `.ymmp` files, create media/render outputs, regenerate YMM4
carriers, approve rights, or change production state.
