# 三スタイル混在 IR — validate-ir dry サンプル

> Date: 2026-04-06  
> 関連: [VISUAL_STYLE_PRESETS.md](../VISUAL_STYLE_PRESETS.md)

## 目的

挿絵コマ風（`skit`）・資料パネル風（`data`/`board`）・再現PV方針（`mood`/`closing`）の `template` を同一 IR に混在させ、`validate-ir` が **ERROR なし**で通ることを repo 内で固定する。

## ファイル

- IR: [samples/ir_visual_styles_dry_sample.json](../../samples/ir_visual_styles_dry_sample.json)
- overlay 契約例: [samples/visual_styles_overlay_map.example.json](../../samples/visual_styles_overlay_map.example.json)（パスは環境に合わせて書き換える）

## コマンド

```bash
uv run python -m src.cli.main validate-ir samples/ir_visual_styles_dry_sample.json \
  --palette samples/palette.ymmp \
  --overlay-map samples/visual_styles_overlay_map.example.json
```

期待: exit code 0。`FACE_LATENT_GAP` 等の WARNING は palette と話者名の組み合わせにより出る場合あり。

## テスト

`tests/test_ir_validate.py` の `test_ir_visual_styles_dry_sample_passes_cli_validation` が上記と同等の CLI を実行する。
