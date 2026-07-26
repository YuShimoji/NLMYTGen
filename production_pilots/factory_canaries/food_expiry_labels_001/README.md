# Food Expiry Labels Factory Canary

`賞味期限と消費期限の違い`をFactory Contract v2.1の
`package_prepared` lifecycleで検証する第4 internal canary。

- 4 cues / 1 scene / れいむ4
- official Japanese public-institution sources 2
- source-backed raster assets 2
- cue-media mappings 4/4
- source project / generated project / MP4 / render receiptなし
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
