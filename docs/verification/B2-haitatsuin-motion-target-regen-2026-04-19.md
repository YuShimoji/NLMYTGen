# B-2 haitatsuin motion_target v3 ymmp 再生成 proof (2026-04-19)

**位置づけ**: G-24 茶番劇 Group template-first 運用の user 視覚確認 (a) を unblock するための再生成。runtime-state `next_action` assistant 先行 (B) の実行記録。

**ステータス**: **PASS** (Face changes 50 / VideoEffects writes motion 6 / fatal 0)。

## run_id

`b2_haitatsuin_motion_regen_2026-04-19`

## 目的

v3 IR (`motion_target: "layer:10"` 付き 4 件) を haitatsuin 本体に適用して、user が YMM4 で Layer 10 の配達員 ImageItem の VideoEffects を視覚確認できる ymmp を生成する。これは [motion-target-implementation-context.md §8](motion-target-implementation-context.md) の user 先行 #1 を解消する下準備。

## 入力アーティファクト

| 種別 | パス |
|------|-----|
| production ymmp | `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` |
| IR (10 utt, motion_target x 4) | `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` |
| face_map (character-scoped, 10 表情) | `samples/face_map_bundles/haitatsuin.json` |
| bg_map | `samples/_probe/b2/palette_extract/bg_map.json` |
| tachie_motion_map | `samples/tachie_motion_map_library.json` (G-23 23 label) |

## 実行コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/b2_haitatsuin_motion_applied_v2.ymmp
```

## 結果

| 指標 | 値 |
|------|-----|
| exit code | **0** (成功) |
| fatal_warning | **0** |
| Face changes | **50** |
| Slot changes | 0 |
| Timeline adapter | motion=6, transition=10, bg_anim=0 |
| Transition VoiceItem writes | 10 |
| **VideoEffects writes (motion)** | **6** (motion_target: layer:10 x 4 entries が 6 segment に分割) |
| GroupItem geometry writes | 0 |
| 出力 ymmp サイズ | 42.66 MB (`_tmp/b2_haitatsuin_motion_applied_v2.ymmp`) |

## motion_target 対応表

v3 IR の motion_target 付き utterance と Layer 10 への VideoEffects 適用:

| IR index | speaker | face | motion | motion_target | 意図 |
|----------|---------|------|--------|---------------|------|
| 1 | 霊夢 | thinking | nod | layer:10 | 配達員がうなずく |
| 3 | 魔理沙 | surprised | surprise_jump | layer:10 | 配達員がジャンプ |
| 5 | 霊夢 | serious | panic_shake | layer:10 | 配達員が震える |
| 8 | 魔理沙 | sad | deny_shake | layer:10 | 配達員が首振り |

残 6 件 (index 2/4/6/7/9/10) は motion: "none" で配達員静止。

## 非 fatal warning (4 件、全て B-2 v2 proof と同一クラス)

1. `FACE_PROMPT_PALETTE_EXTRA: palette label 'neutral' is not listed in prompt contract` — palette に neutral あり。今回 IR では未使用
2. `FACE_LATENT_GAP: character '魔理沙' is missing prompt labels: surprised` — 将来 face_map 拡張で解消
3. `IDLE_FACE_MISSING: idle_face is not specified in any utterance` — 最小 IR では未指定
4. `bg label 'studio_blue' not found in bg_map` — IR default_bg に対応する bg_map エントリ不在。今回 bg 変更は対象外

ERROR はゼロ。

## 次 user action (視覚確認 (a))

1. YMM4 を起動して `_tmp/b2_haitatsuin_motion_applied_v2.ymmp` を開く
2. タイムラインで **Layer 10 の ImageItem** (配達員の絵) を探す。6 segment に分割されているはず
3. 各 segment をクリックして右ペインの「ビデオエフェクト」欄を確認:
   - index 1 (nod) / index 3 (surprise_jump) / index 5 (panic_shake) / index 8 (deny_shake)
4. プレビュー再生で **配達員の絵だけが動き**、霊夢・魔理沙の立ち絵 (Layer 4/3) は静止していることを確認

### 判定

- OK: VideoEffects が意図どおり配達員のみに効く → 視覚確認 (a) PASS、次は canonical skit_group template 作成 (user 先行 C)
- NG (配達員が動かない / 立ち絵が動く) → [motion-target-implementation-context.md](motion-target-implementation-context.md) §6 検証に基づき再調査

## 関連

- [motion-target-implementation-context.md](motion-target-implementation-context.md) — motion_target 実装の全コンテキスト
- [SKIT_GROUP_TEMPLATE_SPEC.md](../SKIT_GROUP_TEMPLATE_SPEC.md) — G-24 主軸仕様
- [B2-haitatsuin-dryrun-proof-2026-04-17.md](B2-haitatsuin-dryrun-proof-2026-04-17.md) — dry-run 先行 proof (face_map 10 表情拡張版)
- [P02-production-adoption-proof.md](P02-production-adoption-proof.md) — adoption 証跡台帳

根拠: runtime-state next_action assistant 先行 (B) + [B2-haitatsuin-dryrun-proof-2026-04-17.md](B2-haitatsuin-dryrun-proof-2026-04-17.md) dry-run PASS
