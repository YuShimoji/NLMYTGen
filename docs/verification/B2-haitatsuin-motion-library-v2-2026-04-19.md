# B-2 haitatsuin library v2 ymmp 再生成 proof (2026-04-19)

**位置づけ**: `tachie_motion_map_library.json` を v1 (flat only) → v2 (flat + animation params) に改訂し、motion_target 経路で ImageItem/GroupItem に**可視的な動き**が出ることを検証。

**ステータス**: **技術 PASS / UX 未達** (機械的書き込みは成功したが、Layer 10 body only の制約により演者全体の所作 proof には至らず。user 視覚確認結果: 「前のファイルの値を少し弱くしただけに見える」「body だけが動いて顔は乗ったまま」)。

## run_id

`b2_haitatsuin_motion_regen_v3_2026-04-19`

## 背景 (v1 の限界)

v1 library はパラメータ値が空 (flat param のみ、animation param 未設定)。TachieItem にはデフォルトキーフレームが効くが、**ImageItem/GroupItem への motion_target 直書き時は YMM4 のデフォルト補完が効かず振幅ゼロ相当**。user が v1 で再生成した ymmp を YMM4 で開いて視覚確認した結果「体のみ伸び縮みしているだけ」「左右移動はそのまま」「殆ど制御できていない」と報告。原因は:
- `RandomZoomEffect` (panic_shake) の Zoom: 0.0 が唯一値を持っていた → 「伸び縮み」
- Move 系は全て `Values: [{Value: 100}]` のような EffectsSamples デフォルト値に解決されず空に近い → 「制御されていない」

## v2 の設計方針

- flat + animation param 両方を library に埋める
- EffectsSamples の実サンプル値を基準に、各 motion の感情表現に応じて控えめな実用値へ調整
- 適用対象を TachieItem / ImageItem / GroupItem 横断に拡張 (speaker_tachie 専用制限を解除)
- panic_shake から RandomZoomEffect を除去

## v2 の主要 motion パラメータ

| motion | Effects | 主要パラメータ |
|---|---|---|
| `nod` | RepeatMove | Y: 15px, Span: 0.4s, Sine InOut Centering |
| `surprise_jump` | Jump + RandomRotate | JumpHeight: 50px, Period: 0.4s, Interval: 0.8s / Rotate Z: 10°, Span: 0.2s |
| `panic_shake` | RandomMove + RandomRotate (Zoom 除去) | Move X: 8px / Y: 6px, Span: 0.05s / Rotate Z: 4°, Span: 0.05s |
| `deny_shake` | RepeatMove | X: 25px, Span: 0.5s, Sine InOut Centering |
| `happy_sway` | RepeatMove + RepeatRotate | X: 12px / Z: 5°, Span: 1.5s |
| `happy_bounce` | Jump (控えめ) | JumpHeight: 25px, Period: 0.5s, Interval: 0.3s |
| `angry_shake` | RandomMove + RandomRotate | Move X:15 / Y:10, Span: 0.08s / Rotate Z: 8°, Span: 0.08s |
| `thinking_zoom` | ZoomEffect (脈動) | Zoom: 100→108→100, Span: 1.5s (user 確認要) |
| `sad_droop` | Opacity + RepeatMove | Opacity: 85%, Move Y: 8px, Span: 2.0s (戻る動作、user 確認要) |
| `focus_zoom` | ZoomEffect (前進) | Zoom: 100→115→115, Span: 2.0s (user 確認要) |

flashback / defocus / entrance_* / exit_* / tsukkomi は既存 full parameter を維持。

## 入力アーティファクト

| 種別 | パス |
|------|-----|
| production ymmp | `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` |
| IR (v3, motion_target x 4) | `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` |
| face_map | `samples/face_map_bundles/haitatsuin.json` |
| bg_map | `samples/_probe/b2/palette_extract/bg_map.json` |
| **tachie_motion_map (v2)** | `samples/tachie_motion_map_library.json` (102KB、v2.0.0) |
| v1 バックアップ | `samples/_probe/b2/tachie_motion_map_library_v1_backup.json` |
| 生成スクリプト | `samples/_probe/b2/build_library_v2.py` |

## 実行コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/b2_haitatsuin_motion_applied_v3.ymmp
```

## 結果

| 指標 | 値 |
|------|-----|
| exit code | **0** |
| fatal_warning | **0** |
| Face changes | **50** |
| Timeline adapter | motion=6, transition=10, bg_anim=0 |
| **VideoEffects writes (motion)** | **6** (motion_target 4 entries が 6 segment に分割) |
| 出力 ymmp | `_tmp/b2_haitatsuin_motion_applied_v3.ymmp` (42.66 MB、gitignore) |

## motion_target 対応表

| IR index | speaker | motion | motion_target | 期待される見え方 (v2) |
|----------|---------|--------|---------------|--------|
| 1 | 霊夢 | nod | layer:10 | 配達員が上下 15px の往復でうなずく (0.4s 周期) |
| 3 | 魔理沙 | surprise_jump | layer:10 | 配達員が 50px 跳ね上がり、同時に 10° 小回転 |
| 5 | 霊夢 | panic_shake | layer:10 | 配達員が 8x6px の小刻みランダム移動 + 4° 回転震え (0.05s 周期)。**伸び縮みは除去** |
| 8 | 魔理沙 | deny_shake | layer:10 | 配達員が左右 25px の水平首振り (0.5s 周期) |

残 6 件 (index 2/4/6/7/9/10) は motion: "none" で配達員静止。

## 次 user action

1. YMM4 で `_tmp/b2_haitatsuin_motion_applied_v3.ymmp` を開く
2. Layer 10 配達員 ImageItem の 6 segment の動きを視覚確認
3. v1 のときと比べて実用レベルの感情表現になっているか判定

### 判定の観点

- **nod (index 1)**: 縦方向の控えめな往復うなずきが出ているか
- **surprise_jump (index 3)**: 明確な跳ね上がり + 小回転が出ているか
- **panic_shake (index 5)**: 小刻みな全方向震えが出ているか。**伸び縮みが消えているか**
- **deny_shake (index 8)**: 水平首振りが出ているか

## UX 未達の原因と次ブロックの対処

**根本制約**: `motion_target: "layer:10"` は body ImageItem (Layer 10) のみを動かし、顔 ImageItem (Layer 11) は対象外。library v2 のパラメータをいくら調整しても「演者全体の所作」にはならない。

**次ブロックでの対処**: `motion_target` を複数 layer 配列に拡張 (`["layer:10","layer:11"]`) し、body + 顔を同期して動かす短期検証ブリッジを追加する。詳細: [B2-haitatsuin-motion-layer-array-2026-04-19.md](B2-haitatsuin-motion-layer-array-2026-04-19.md) (次ブロック生成予定)

## 関連

- [MOTION_PRESET_LIBRARY_SPEC.md](../MOTION_PRESET_LIBRARY_SPEC.md) — library 仕様 (Phase 2 更新済)
- [SKIT_GROUP_TEMPLATE_SPEC.md](../SKIT_GROUP_TEMPLATE_SPEC.md) §7 G-23 — 適用対象の再定義
- [B2-haitatsuin-motion-target-regen-2026-04-19.md](B2-haitatsuin-motion-target-regen-2026-04-19.md) — v1 (空パラメータ) での先行 proof
- [INVARIANTS.md](../INVARIANTS.md) Responsibility Boundaries — library 適用対象の汎用化

根拠: user 指示 2026-04-19「要素は全て揃っているはず。一つ一つ丁寧に設定してください」+ EffectsSamples_2026-04-15.ymmp 実サンプル値
