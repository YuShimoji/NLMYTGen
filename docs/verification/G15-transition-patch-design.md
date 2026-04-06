# G-15 `transition` patch（実装正本）

> ステータス: **done**（[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md)）。2026-04 承認スコープどおり実装済み。

## スコープ（承認どおり）

- IR の `transition` は **`none`** と **`fade`** のみ `patch_ymmp` が反映。
- **`fade`** は **`VoiceItem` の `VoiceFadeIn` / `VoiceFadeOut` / `JimakuFadeIn` / `JimakuFadeOut`** のみ（**立ち絵 `TachieItem` の Fade は含めない**）。
- 仕様 §3.9 にある **`slide_left` / `wipe` / `cut` 等**は **`validate-ir` で `TRANSITION_UNKNOWN_LABEL`（ERROR）**。
- フェード秒数は **`ymmp_patch` の定数**（`G15_*_SEC`）。将来 **registry で拡張**可能。

## 発話アンカー

- **index モード**: 発話 `index` に対応する **1 個の VoiceItem**。
- **row-range モード**: `row_start`〜`row_end` の **VoiceItem 列**に対し、**先頭に fade-in、末尾に fade-out**（中間は 0）。

## 正本コード

- [`src/pipeline/ymmp_patch.py`](../../src/pipeline/ymmp_patch.py): `_apply_transition_voice_items`、`TRANSITION_ALLOWED`
- [`src/pipeline/ir_validate.py`](../../src/pipeline/ir_validate.py): `TRANSITION_UNKNOWN_LABEL`
- [`tests/test_ymmp_transition_patch.py`](../../tests/test_ymmp_transition_patch.py)

## 関連

- [G12-timeline-route-measurement.md](G12-timeline-route-measurement.md)
- [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)
