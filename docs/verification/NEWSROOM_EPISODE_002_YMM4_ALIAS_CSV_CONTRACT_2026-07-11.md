# Episode 002 YMM4 alias / CSV responsibility correction — 2026-07-11

## Outcome

The assistant-owned correction is complete and the bounded GUI return is
blocked safely. Canonical speaker identities remain `れいむ` and `まりさ`.
An explicitly selected YMM4 `4.53.0.9` profile projects them to
`ゆっくり霊夢` and `ゆっくり魔理沙` with strict coverage and no silent
pass-through.

The derived CSV is ready for one clean re-observation, but it was not imported.
YMM4 restored an existing unsaved `無題*` project containing the prior nine-item,
2790-frame state. Starting a clean project required discarding or relocating
that existing state, so the Worker stopped without changing it and left YMM4
open.

## Artifact chain

| Artifact | Role | Evidence |
| --- | --- | --- |
| `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv` | Canonical identity CSV | 9 rows; SHA-256 `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`; byte-unchanged |
| `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_character_alias_profiles/ymm4_4_53_0_9_yukkuri_characters_v1.json` | Explicit environment profile | `strict_coverage=true`; no universal-default claim; prior receipt provenance pinned |
| `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv` | Primary YMM4 import CSV | 9 rows; text/order unchanged; speaker column only projected; SHA-256 `5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC` |
| `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/yymm4_character_alias_coverage_readback.json` | Machine derivation readback | strict coverage, row count, text/order, character projection, encoding, and canonical immutability pass |
| `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_receipt_2026-07-10.json` | Immutable historical v1 evidence | SHA-256 `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`; historical `partial` semantics retained |
| `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_alias_reobservation_blocker_2026-07-11.json` | Current GUI blocker receipt | Existing unsaved project preserved; no derived import, discard, save, render, or export |

## Versioned responsibility contract

- `edit_slice_to_ymm4_cue_map.v2` and `ymmp_adapter_plan.v2` remove the mixed
  `expected_yymm4_layer_or_track` / `expected_item_families` meaning.
- CSV import expects exactly `VoiceItem` plus linked subtitle.
- `ImageItem` plus independent `TextItem` placeholders belong to a separate
  diagnostic project with `not_authorized / not_attempted` state.
- Missing diagnostic items during CSV import are not a CSV-gate failure.
- The observation generator accepts immutable receipt v1 for historical
  readback and receipt v2 only for the corrected CSV-gate semantics.
- A successful receipt v2 advances to `supervisor_next_slice_decision`; it does
  not advance automatically to render or diagnostic `.ymmp` work.

## Validation

Modified Python compiled successfully. Focused validation completed with:

```powershell
uv run pytest tests/test_ymm4_character_alias_profile.py `
  tests/test_ymm4_import_ready_pack.py `
  tests/test_ymm4_observation_readback_pack.py `
  tests/test_pipeline_smoke.py `
  tests/test_local_edit_slice_execution_pack.py `
  tests/test_real_input_replacement_readiness_pack.py `
  tests/test_project_state_sync.py -q
```

Result: `72 passed`.

The import-ready and observation packs were regenerated twice from their CLI
entrypoints. All 18 generated files retained identical SHA-256 values on the
second pass. The explicit state checker passed for
`episode-002-ymm4-speaker-alias-ready-for-reobservation-v1`.

No full pytest run occurred. No unrelated tracked fixture changed.

## Exact GUI return

1. In the already-open YMM4 window, first decide whether the recovered unsaved
   `無題*` project may be discarded or must be saved elsewhere.
2. Only after that decision, start a clean untitled project.
3. Import only
   `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/derived_yymm4_import.csv`.
4. Record whether a mapping dialog appears; confirm 9 VoiceItems, 3
   `ゆっくり霊夢` plus 6 `ゆっくり魔理沙`, exact linked text/order,
   `csv_row_1` through `csv_row_9`, S1 through S3, and timing order.
5. Record the fifth check as the CSV responsibility boundary. ImageItem and
   independent TextItem absence is not a CSV failure; the diagnostic project
   must remain `not_authorized / not_attempted`.
6. Close the new observation project without saving. Do not render/export or
   create, patch, or save a diagnostic/production `.ymmp`.

On success, return a new `ymm4_gui_observation_receipt.v2`. Do not edit the
2026-07-10 receipt.
