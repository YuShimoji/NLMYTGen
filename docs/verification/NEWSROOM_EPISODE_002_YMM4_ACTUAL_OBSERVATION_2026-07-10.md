# Episode 002 YMM4 actual observation — 2026-07-10

## Result

- Overall: `partial` / `pass_with_warnings`
- Observation mode: `actual_ymm4_gui_observation`
- Next gate: `adapter_correction_after_observation`
- Supervisor boundary base: accepted correction commit `c0d098f`
- Current implementation branch: `codex/episode-002-ymm4-five-point-observation-v1`

The tracked nine-row diagnostic CSV was imported in YMM4. It produced nine
ordered VoiceItems and matching linked subtitle text after manual character
mapping. The application was closed without saving the project.

## Current-machine inputs

- Repository: `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen`
- YMM4: `D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`
- YMM4 file version: `4.53.0.9`
- CSV: `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`
- CSV SHA-256: `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`
- Receipt: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_receipt_2026-07-10.json`

Paths under the old `C:\Users\PLANNER007` environment remain only in dated
historical handoffs. They are not the current launch or repository paths.

## Five observations

| Check | Result | Evidence |
| --- | --- | --- |
| Cue order | OK | Nine rows remained `csv_row_1` through `csv_row_9`; cue-map crosswalk gives S1 -> S2 -> S3. |
| VoiceItems | OK | Exactly nine items appeared: three Reimu items on layer 0 and six Marisa items on layer 1; no missing, duplicate, or reordered cue was seen. |
| Speaker / linked subtitle text | OK with manual correction | All text matched. `れいむ` mapped to `ゆっくり霊夢`; `まりさ` initially defaulted to `ゆっくり霊夢` and was corrected to `ゆっくり魔理沙` before apply. |
| Timing order | OK with variance | Order remained intact. YMM4 recalculated provisional four-second blocks to 2790 frames / 46.50 seconds at 60 fps. Sampled items: row 1 = frame 0, length 273; row 2 = frame 273, length 293; row 9 = frame 2317, length 473. |
| Placeholder boundary | NG / adapter gap | CSV import created VoiceItem/subtitle lanes only. Expected ImageItem/TextItem placeholder scene lanes were absent. Diagnostic text remained visibly dry-run and did not claim final/public readiness. |

No persisted screenshot was created. The evidence is the direct GUI observation,
the tracked receipt, and the regenerated readback. Unobserved per-item frame
values were not inferred.

## Safety boundary

- Update prompt was cancelled; YMM4 was not upgraded.
- Cached unsaved project state was discarded with the user's explicit approval.
- No project `.ymmp` was saved or written.
- No render or export occurred.
- No real input was substituted.
- No rights, public-ready, or final-thumbnail approval was made.
- No upload, live fetch, or external-media download occurred.

## Regeneration and validation

```powershell
$env:NLMYTGEN_YMM4_EXE = 'D:\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe'
uv run python -m src.cli.main build-ymm4-observation-readback-pack `
  --package production_pilots/yukkuri_newsroom_content_spine_002 `
  --observation-receipt production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_receipt_2026-07-10.json `
  --artifact-id episode_002_ymm4_observation_readback_pack_v1 `
  --format json

uv run pytest tests/test_ymm4_observation_readback_pack.py `
  tests/test_ymm4_import_ready_pack.py `
  tests/test_local_edit_slice_execution_pack.py `
  tests/test_real_input_replacement_readiness_pack.py -q
```

Observed result: generator `validation_status=passed`; focused regression
`24 passed`.

## Residual work

| Purpose | Effect | Requirements | State | Owner | Next move |
| --- | --- | --- | --- | --- | --- |
| Bind source speaker aliases automatically | Remove manual mapping and the incorrect Marisa default | Evidence-backed alias/character policy; preserve existing speaker text | open / recommended | adapter implementation lane | Map `れいむ` to `ゆっくり霊夢` and `まりさ` to `ゆっくり魔理沙`, then repeat bounded import |
| Generate expected placeholder scene lanes | Make the cue-map ImageItem/TextItem contract visible in YMM4 | Diagnostic-only placeholder data; no production asset or rights claim | open / required | adapter implementation lane | Add the missing lanes without render/export, then repeat the same five checks |
| Replace diagnostic input | Move from sample fixture to verified real material | Verified source/transcript, provenance/rights note, stable identity, cue alignment | blocked by missing inputs | real-input intake owner | Supply and validate the required receipt; do not infer readiness from this observation |
