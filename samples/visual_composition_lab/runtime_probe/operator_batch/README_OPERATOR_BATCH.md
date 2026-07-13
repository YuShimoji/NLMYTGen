# Generic static-layout Operator Batch

このbatchは日本語firstのH1目視確認入口です。通常modeだけがprepared `.ymmp` を1回開きます。自動click、key injection、save、close、screen capture、renderは行いません。

## Safe modes

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\samples\visual_composition_lab\runtime_probe\operator_batch\run_generic_static_layout_probe.ps1 -PreflightOnly
powershell -NoProfile -ExecutionPolicy Bypass -File .\samples\visual_composition_lab\runtime_probe\operator_batch\run_generic_static_layout_probe.ps1 -CollectOnly
```

両方ともYMM4 executableの解決より前に分岐し、launch countは0です。`-CollectOnly` はtracked synthetic fixtureでcollector transportだけを検証し、実観測resultやcapability evidenceにはしません。

## Normal mode

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\samples\visual_composition_lab\runtime_probe\operator_batch\run_generic_static_layout_probe.ps1
```

YMM4が自動検出できない場合だけ `-Ymm4Exe <absolute-path>` を付けます。manual actionはcommand実行、3点確認してsave/renderせずclose、terminalで3回答、の3件です。既存local state/resultがある場合は停止するため、README_STATIC_LAYOUT_PROBE.mdのarchive手順で保存してから再実行してください。
