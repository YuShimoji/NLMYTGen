# B-2 haitatsuin motion_target 配列対応 ymmp 再生成 proof (2026-04-19)

**位置づけ**: `motion_target` の複数 layer 配列対応 (`["layer:10","layer:11"]`) を使って、body (Layer 10) と 顔 (Layer 11) を同期させた短期検証。canonical template (B 本筋) 完成までのブリッジ。library v2 proof の「body-only 制約で UX 未達」を解消するのが目的。

## run_id

`b2_haitatsuin_motion_layer_array_2026-04-19`

---

## 技術 PASS (機械的書き込み成功の確認)

| 指標 | 値 |
|------|-----|
| exit code | **0** |
| fatal_warning | **0** |
| Face changes | **50** |
| Timeline adapter | motion=10, transition=10, bg_anim=0 |
| **VideoEffects writes (motion)** | **10** (Layer 10 body x 6 segments + Layer 11 顔 x 4 segments = 10) |
| 出力 ymmp | `_tmp/b2_haitatsuin_motion_applied_v4.ymmp` (~42.6 MB、gitignore) |

v3 proof (body only, motion_target `"layer:10"`) の writes: 6 → v4 (配列): 10 (+4) に増加。増分 4 がそのまま Layer 11 顔への書き込み。

## 技術 PASS と UX PASS の分離

- 上記指標は「apply-production が library v2 の VideoEffects を両レイヤーに機械的に書き込めた」ことを示すのみ
- **user が YMM4 で視覚確認して「演者全体の所作に見える」と判定するまで UX PASS とは呼ばない**
- v2 proof で「技術 PASS を UX PASS と混同」した反省の反映

---

## motion_target 配列対応表

v3 IR の motion_target 付き utterance (4 件) を `"layer:10"` → `["layer:10","layer:11"]` に上書き:

| IR index | speaker | motion | motion_target (v4) | 期待 UX |
|----------|---------|--------|--------------------|--------|
| 1 | 霊夢 | nod | `["layer:10","layer:11"]` | 配達員 body + 顔 が同期してうなずく |
| 3 | 魔理沙 | surprise_jump | `["layer:10","layer:11"]` | 配達員 body + 顔 が同期して跳ねる |
| 5 | 霊夢 | panic_shake | `["layer:10","layer:11"]` | 配達員 body + 顔 が同期して震える |
| 8 | 魔理沙 | deny_shake | `["layer:10","layer:11"]` | 配達員 body + 顔 が同期して首振り |

残 6 件 (index 2/4/6/7/9/10) は `motion: "none"` で配達員静止。

---

## 入力アーティファクト

| 種別 | パス |
|------|-----|
| production ymmp | `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` |
| IR (v3, motion_target array 化済) | `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` |
| face_map (10 表情) | `samples/face_map_bundles/haitatsuin.json` |
| bg_map | `samples/_probe/b2/palette_extract/bg_map.json` |
| tachie_motion_map (v2.0.0) | `samples/tachie_motion_map_library.json` |

## 実行コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/b2_haitatsuin_motion_applied_v4.ymmp
```

## 非 fatal warning (4 件、B-2 v2 と同一クラス)

1. `FACE_PROMPT_PALETTE_EXTRA: palette label 'neutral' is not listed in prompt contract`
2. `FACE_LATENT_GAP: character '魔理沙' is missing prompt labels: surprised`
3. `IDLE_FACE_MISSING: idle_face is not specified in any utterance`
4. `bg label 'studio_blue' not found in bg_map`

---

## user 視覚確認手順 (UX PASS 判定)

1. YMM4 で `_tmp/b2_haitatsuin_motion_applied_v4.ymmp` を開く
2. タイムラインで **Layer 10** (配達員 body) と **Layer 11** (配達員 顔) を両方確認。どちらも同じ位置・同じ発話区間で 4 segment に分割されているはず
3. 各 segment のビデオエフェクト欄で library v2 のパラメータ付き motion が書き込まれていることを確認
4. プレビュー再生で **配達員の body と 顔が同期して動く**ことを確認:
   - index 1 (nod): body + 顔が一緒にうなずく
   - index 3 (surprise_jump): body + 顔が一緒に跳ねる
   - index 5 (panic_shake): body + 顔が一緒に震える
   - index 8 (deny_shake): body + 顔が一緒に首を振る
5. 解説役の立ち絵 (Layer 4 霊夢 / Layer 3 魔理沙 の TachieItem) は静止していることを確認

### UX PASS 判定

| 判定 | 次アクション |
|---|---|
| **OK** (body+顔同期が取れ、v2 の貧弱な印象から改善) | canonical template (B 本筋) に進む。または振幅調整を user 判断 |
| **部分 OK** (同期はしているが振幅・周期が合わない) | library v2 のパラメータを調整 (具体的に弱い/強い motion を指摘) |
| **NG** (顔が body と同期しない / 顔が消える / 立ち絵が動く) | 原因切り分け (layer 分割タイミング / Z-index / Layer 11 ImageItem の segment 生成) |

---

## 関連

- [B2-haitatsuin-motion-library-v2-2026-04-19.md](B2-haitatsuin-motion-library-v2-2026-04-19.md) — library v2 での先行 proof (body only 制約により UX 未達)
- [B2-haitatsuin-motion-target-regen-2026-04-19.md](B2-haitatsuin-motion-target-regen-2026-04-19.md) — v1 library での先行 proof
- [motion-target-implementation-context.md](motion-target-implementation-context.md) §5 — 受理値仕様 (配列対応追記済)
- [SKIT_GROUP_TEMPLATE_SPEC.md](../SKIT_GROUP_TEMPLATE_SPEC.md) — canonical template 主経路 (本 proof が解消する短期制約の本筋)

根拠: user 指示 2026-04-19「Layer 10 body only が根本制約」+ 外部分析 #1 + INVARIANTS §skit_group の主経路は canonical template (本 proof はブリッジ)
