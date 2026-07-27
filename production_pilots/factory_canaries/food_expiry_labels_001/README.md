# Food Expiry Labels Factory Canary

`賞味期限と消費期限の違い`をFactory Contract v2.1の
`package_prepared`から`rendered`まで検証する第4 internal canary。

- 4 cues / 1 scene / れいむ4
- official Japanese public-institution sources 2
- source-backed raster assets 2
- cue-media mappings 4/4
- exact source project / generated project / MP4 / technical render receiptあり
- human acceptance / rights / production / publication / upload / releaseなし

`source_cache/`、`source_extracts/`、`local_media/`はignored local evidence。
tracked packageはprivate rasterが無い状態でもcontract validityを保ち、
availabilityだけを`receipt_only_no_live_file`へ下げる。

通常検証:

```powershell
uv run python -m src.cli.main validate-factory-package `
  --package production_pilots/factory_canaries/food_expiry_labels_001/factory_package_v2_1.json `
  --require-lifecycle package_prepared --check-live --format json
```

pre-render stage plan:

```powershell
uv run python -m src.cli.main build-episode-video `
  --factory-package production_pilots/factory_canaries/food_expiry_labels_001/factory_package_v2_1.json `
  --dry-run
```

このdry-runはcompleted video dry-runではない。source-project generation前に
成功停止し、YMM4、Electron、render driver、ffmpeg、playbackを起動しない。

source-project promotion後の正本:

- predecessor: `factory_package_v2_1.json` (`package_prepared`、immutable)
- successor: `factory_package_v2_1_source_project_ready.json`
- structural readback: `source_project_readback.json`
- promotion receipt: `source_project_promotion_receipt.json`
- local project:
  `local_outputs/food_expiry_labels_source.local.ymmp` (ignored)

同じauthorityとcontent identityで`advance-factory-package --execute`を再実行した
場合はvalidation-only `verified_noop`となる。

rendered lifecycleの正本:

- predecessor: `factory_package_v2_1_source_project_ready.json` (immutable)
- successor: `factory_package_v2_1_rendered.json`
- technical readback: `render_readback.json`
- one-shot promotion receipt: `render_promotion_receipt.json`
- resume no-op observation: `render_resume_observation.json`
- final local run:
  `auto_video_runs/food_expiry_labels_internal_review_v4/` (ignored)
- final MP4 SHA:
  `95558db7488a882b4d22a9ea68f302bcc81e23800dfed9687274fe8944d3daec`

queue-v3はliveで4件`verified_noop`、tracked-onlyで4件
`recorded_complete_no_live_file`となる。private artifactの不在は再render理由に
ならない。human decisionとrights/production/public authorityは別gateである。

full-episode review bundle v1の`background_visual_system`には、2026-07-28の
human full-episode reviewによるactive design quarantineがある。exact identity、
拒否signature、scope boundaryは
`design_direction_quarantines/NLMYTGEN-FEL-FULL-DQ-ALL-TEXT-RAPID-SWITCH-20260728-01.json`
を正本とし、release / supersession evidenceなしに通常候補へ戻さない。
