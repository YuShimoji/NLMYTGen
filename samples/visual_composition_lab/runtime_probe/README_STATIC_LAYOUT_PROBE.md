# Generic static-layout YMM4 probe

このpackageは、リンク字幕のsafe areaを主対象に、静止ImageItem 1件と短い独立TextItem 1件を同じYMM4 projectで後から目視確認するためのH0準備物です。現時点で確認済みなのはproject構造、決定的生成、source不変、safe-mode、countだけであり、YMM4上の見え方やC3 capabilityは未確認です。

## Current result

H1 user operationは完了し、exact same-machine compositeの3項目はすべてpassとして
sanitized intake済みです。このprobeを再実行しません。現在の人間向け結果は
[`README_STATIC_LAYOUT_PROBE_RESULT.md`](README_STATIC_LAYOUT_PROBE_RESULT.md)、機械正本は
`runtime_observation_receipt.json`と`runtime_observation_readback.json`です。H0 contractと
materialization readbackの`unverified_H1`表記は実行前構造証拠の履歴であり、current resultを
上書きしません。

## 構成

- 1920x1080の下部をリンク字幕reserveにする。
- 上部左の非重複zoneに、repo内生成の抽象RGB PNGを参照するImageItemを1件置く。
- 上部右の非重複zoneに `PROBE LABEL` のTextItemを1件置く。
- carrierのVoiceItemとリンク字幕設定はsemantic-preserving copyとし、carrier sourceは変更しない。
- ShapeItem、callout、外部asset、fade、transition、motion、非defaultのopacity/zoom/rotation、renderは対象外。

YMM4 serializerでopenableなitemに必要な `Opacity=100`、`Zoom=100`、`Rotation=0`、`FadeIn=0`、`FadeOut=0` は静的default fieldとして保持します。これらをcapabilityとして行使・観測したとは扱いません。

## H0再生成とsafe確認

```powershell
uv run python -m src.pipeline.generic_static_layout_probe materialize
powershell -NoProfile -ExecutionPolicy Bypass -File .\samples\visual_composition_lab\runtime_probe\operator_batch\run_generic_static_layout_probe.ps1 -PreflightOnly
```

`materialize` はtracked neutral sampleをread-onlyで解析し、既存Image/Tachieを引き継がず、VoiceItemと対応Character設定だけを保持します。出力projectとPNGは `local_outputs/` 配下でignoreされます。

## H1 user operation（completed history; do not repeat）

以下は完了済みoperationの履歴です。新しい条件変更がない限り再実行しません。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\samples\visual_composition_lab\runtime_probe\operator_batch\run_generic_static_layout_probe.ps1
```

1. 上のbatch commandを実行する。
2. 開いたprojectで字幕、Image、Textの3点を確認し、renderもproject saveもせずYMM4を閉じる。
3. terminalへ戻り、3回答を入力してcollectionを完了する。

screen captureは不要です。結果はignored `local_outputs/operator_result.json` に保存され、tracked matrixは自動更新されません。

## Recovery

既存のlocal evidenceは削除・上書きしません。再実行前に、PowerShellで次のように個別targetをtimestamp archiveへ移動してください。`archive` 自身は移動対象に含めません。

```powershell
$probe = Resolve-Path .\samples\visual_composition_lab\runtime_probe
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$archive = Join-Path $probe "local_outputs\archive\$stamp"
New-Item -ItemType Directory -Force -Path $archive | Out-Null
@(
  'local_outputs\generic_static_layout_probe.local.ymmp',
  'local_outputs\operator_result.json',
  'local_outputs\operator_batch.local.json',
  'local_outputs\operator_observations.local.json',
  'local_outputs\assets\generic_probe_image.png'
) | ForEach-Object {
  $source = Join-Path $probe $_
  if (Test-Path -LiteralPath $source) { Move-Item -LiteralPath $source -Destination $archive }
}
```

実観測で残るdebtは、字幕readability/non-overlap、Image crop/anchor、Text wrap/anchor、cross-machine portability、second-topic C5です。
