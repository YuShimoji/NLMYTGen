# B-2 haitatsuin GroupItem 単一 layer 指定 ymmp 再生成 proof (2026-04-19)

**位置づけ**: 実機観察で発見した「既存 Layer 9 GroupItem が body + 顔を包んでいる (canonical template 済)」事実を受け、`motion_target: "layer:9"` 指定で GroupItem 単位に motion を書き込む proof。array 対応 (v4) からの訂正。

## 前回までの認識誤り

v4 proof 時点で assistant は:
- 「canonical template は未完成、user が GroupItem 化する必要あり」と誤認
- Layer 9 の既存 GroupItem の存在を事実確認せず、array 対応 (`["layer:10","layer:11"]`) で対応しようとした
- user 指摘「GroupItem の値を調整するだけで同じように破綻なく動くことを確認済み」「グループ化されているようです」を **既に完成済みの canonical** として解釈できなかった

**訂正**: canonical template は `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` で**既に完成**していた (Layer 9 GroupItem が body + 顔 を包み、座標・倍率を相対配置済)。user 作業は不要だった。

**根拠**: `samples/_probe/b2/inspect_group_layer.py` の Layer 分布ダンプ結果

## run_id

`b2_haitatsuin_motion_groupitem_2026-04-19`

## 既存 Layer 9 GroupItem の事実

| 項目 | 値 |
|---|---|
| Layer | 9 |
| Frame / Length | 0 / 1988 (動画全長) |
| Remark | `""` (空) |
| X / Y / Zoom | 408.0 / -57.0 / 103.8% |
| 配下 | Layer 10 body ImageItem x2 + Layer 11 顔 ImageItem x2 (物理的に包含) |

user 確認済: GroupItem の X/Y/Zoom を動かせば body + 顔 が相対配置を保ったまま破綻なく同期する。

## 実行コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/b2_haitatsuin_motion_applied_v5.ymmp
```

v3 IR の motion_target を `["layer:10","layer:11"]` → `"layer:9"` に変更。コード側は既存の `_apply_motion_to_layer_items` が ImageItem と GroupItem 両方を対象とするため、追加実装なしで適用できた。

## 技術 PASS

| 指標 | 値 |
|------|-----|
| exit code | 0 |
| fatal_warning | 0 |
| Face changes | 50 |
| VideoEffects writes (motion) | 10 |

## GroupItem segment 分割 (v4 との決定的差)

Layer 9 GroupItem が utterance timing で **8 segment に正確に分割** された:

| # | Frame | Length | VideoEffects | 対応 utterance (motion) |
|---|---|---|---|---|
| 0 | 0 | 201 | RepeatMoveEffect | index 1 (nod) |
| 1 | 201 | 275 | (空) | index 2 (none) |
| 2 | 476 | 98 | JumpEffect + RandomRotate | index 3 (surprise_jump) |
| 3 | 574 | 192 | (空) | index 4 (none) |
| 4 | 766 | 144 | RandomMoveEffect + RandomRotate | index 5 (panic_shake) |
| 5 | 910 | 292 | (空) | index 6 (none) |
| 6 | 1202 | 145 | RepeatMoveEffect | index 8 (deny_shake) |
| 7 | 1347 | 641 | (空) | index 9,10 (none) |

Layer 10/11 の ImageItem には直接書き込みなし (GroupItem 配下で effect が継承される)。

**v4 からの改善**:
- v4 (array): Layer 10/11 の元 item 境界 (Frame 634/910) に複数 motion が後勝ち上書き → 非対称で構造的に同期しない
- v5 (GroupItem): 発話 timing で GroupItem 自体が分割され、各 motion segment が独立・1 対 1 対応。既存 item 境界とは無関係

## UX PASS 期待

- body + 顔 が GroupItem 配下として相対配置を保ったまま同期して動く (user 確認済の挙動)
- 発話タイミングで motion segment が切り替わる
- 既存の user 配置 (body/顔 の相対位置・倍率) は保たれる
- 既存の user モーション (別 layer にある振り向き等) は今回の patch とは独立 (motion_target=layer:9 は Layer 9 GroupItem のみに効く)

## user 視覚確認手順

1. YMM4 で `_tmp/b2_haitatsuin_motion_applied_v5.ymmp` を開く
2. タイムラインで **Layer 9 (GroupItem)** を確認。8 segment に分割されていること
3. 各 motion 付き segment のビデオエフェクト欄に library v2 のパラメータが入っていること
4. プレビュー再生で **body + 顔 が同じ motion で同期して動く**ことを確認
   - index 1 (nod): 上下 15px のうなずき
   - index 3 (surprise_jump): 跳ね上がり + 小回転
   - index 5 (panic_shake): 小刻みな震え
   - index 8 (deny_shake): 左右 25px の首振り

## 関連

- [B2-haitatsuin-motion-layer-array-2026-04-19.md](B2-haitatsuin-motion-layer-array-2026-04-19.md) — array 対応 proof (代替実現により本番経路ではなくなった。array 対応自体は装飾のみの演者等の case で活きる)
- [B2-haitatsuin-motion-library-v2-2026-04-19.md](B2-haitatsuin-motion-library-v2-2026-04-19.md) — library v2 proof (v5 で library v2 のパラメータがそのまま効く)
- [SKIT_GROUP_TEMPLATE_SPEC.md](../SKIT_GROUP_TEMPLATE_SPEC.md) — canonical template 主経路 (本 proof がその実現)

根拠: user 指摘「GroupItem は既に正しく設定されていて調整するだけで動く」+ inspect_group_layer.py 実機確認 + INVARIANTS §skit_group の主経路は canonical template
