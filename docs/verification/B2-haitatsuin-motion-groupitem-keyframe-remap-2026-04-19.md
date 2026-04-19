# B-2 haitatsuin GroupItem 分割時 keyframe clip/remap proof (2026-04-19)

**位置づけ**: v5 で発覚した main bug「GroupItem 分割時の既存 animated 属性 deep copy」を解消する正本 proof。v5 までは `copy.deepcopy(target)` が元 Values を丸ごと全 segment に複製しており、各 segment で元アニメが segment_length に圧縮再生されていた。

## run_id

`b2_haitatsuin_motion_groupitem_keyframe_remap_2026-04-19`

---

## 前回 (v5) までの main bug

元 Layer 9 GroupItem:
- `Frame=0, Length=1988`
- `X: Values=[408.0, -250.0, 178.0], Span=0.0, AnimationType="直線移動"`

v5 生成後の 8 分割 segment 全てに、同じ `X: Values=[408.0, -250.0, 178.0]` が deep copy されていた (例: Frame=0 Length=201 の segment で、元 1988f かけて 408→-250→178 と動くアニメが 201f に圧縮再生される)。結果として body + 顔が各発話 timing ごとに大きく動き回る破綻挙動となる。

**根拠**: [samples/_probe/b2/inspect_v5_group_segments.py](../../samples/_probe/b2/inspect_v5_group_segments.py) 実行結果

---

## 修正方針 (採用案): keyframe clip + 境界補間 remap

案 W' (2-point linear remap) は中間 keyframe を跨ぐ segment で形状損失するため棄却。採用案:

1. 元 animated 属性 Values を時刻付き keyframe 列 `[(t_i, v_i)]` として扱う (等間隔配置: `t_i = i * original_length / (n-1)`)
2. 各 segment の元 timeline 上範囲 `[seg_start, seg_end]` に対して:
   - 範囲内の元 keyframe はそのまま保持
   - `seg_start` / `seg_end` が keyframe と一致しない場合、AnimationType の補間則で境界値を計算・挿入
   - 時刻を segment ローカルに再正規化
3. `AnimationType="なし"` または 1 点のみ: deep copy のまま (非アニメ)
4. `AnimationType="直線移動"`: 最小サポート
5. その他 (加速減速・Bezier 等): warning 出力 + deep copy fallback

根拠: user 指示 2026-04-19「2-point linear remap の限界を正面から認めて修正」+ inspect 実測「Values 3 点以上では単一直線 1 本ではない」

---

## 実装

| 種別 | パス | 変更 |
|---|---|---|
| 実装 | [src/pipeline/ymmp_patch.py](../../src/pipeline/ymmp_patch.py) | `_clip_animated_to_segment(prop, seg_start_local, seg_length, original_length, ...)` 新設。`_apply_motion_to_layer_items` の GroupItem 分割 deep copy 直後に `X/Y/Zoom/Rotation/Opacity` へ適用 |
| test | [tests/test_ymmp_motion_patch.py](../../tests/test_ymmp_motion_patch.py) | `test_clip_animated_to_segment_no_straddle`, `test_clip_animated_to_segment_straddle`, `test_clip_animated_to_segment_fixed_regression` の 3 件追加 |

### テスト類型

1. **no-straddle**: 元 `Values=[100,200] AT=直線移動` original=100f → seg `[0,50]`=`[100,150]`, seg `[50,100]`=`[150,200]`
2. **straddle**: 元 `Values=[100,200,300] AT=直線移動` original=100f (中間 keyframe t=50f 値 200) → seg `[0,80]`=`[100,200,260]` (中間 keyframe 保持 + 右境界補間), seg `[80,100]`=`[260,300]`
3. **fixed regression**: 元 `Values=[150] AT=なし` → 全 seg `[150]` deep copy

---

## 実行コマンド

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/b2_haitatsuin_motion_applied_v6.ymmp
```

---

## 技術 PASS (機械的書き込み成功の確認)

| 指標 | 値 |
|------|-----|
| exit code | **0** |
| fatal_warning | **0** |
| Face changes | **50** |
| Timeline adapter | motion=10, transition=10, bg_anim=0 |
| VideoEffects writes (motion) | **10** |
| 出力 ymmp | `_tmp/b2_haitatsuin_motion_applied_v6.ymmp` (gitignore) |
| pytest (新規 3 件) | **PASS** |
| pytest (既存含む 32 件) | **PASS** |

### GroupItem segment の X Values 遷移 (v5 との決定的差)

元軌跡: `t=0 → 408`, `t=994 → -250` (中間 keyframe), `t=1988 → 178`。

v6 での 8 分割 segment:

| # | Frame | Length | X Values | straddle t=994 | 元軌跡該当区間保持 |
|---|---|---|---|---|---|
| 0 | 0 | 201 | `[408.0, 274.9]` | × | ✓ |
| 1 | 201 | 275 | `[274.9, 92.9]` | × | ✓ |
| 2 | 476 | 98 | `[92.9, 28.0]` | × | ✓ |
| 3 | 574 | 192 | `[28.0, -99.1]` | × | ✓ |
| 4 | 766 | 144 | `[-99.1, -194.4]` | × | ✓ |
| 5 | 910 | 292 | `[-194.4, -250.0, -160.4]` | **◯ (中間 keyframe 保持)** | ✓ |
| 6 | 1202 | 145 | `[-160.4, -98.0]` | × | ✓ |
| 7 | 1347 | 641 | `[-98.0, 178.0]` | × | ✓ |

### 境界連続性 (seg[i] 終値 == seg[i+1] 始値)

| 境界 | seg[i] 終値 | seg[i+1] 始値 | 一致 |
|---|---|---|---|
| [0]→[1] | 274.944 | 274.944 | ✓ |
| [1]→[2] | 92.901 | 92.901 | ✓ |
| [2]→[3] | 28.028 | 28.028 | ✓ |
| [3]→[4] | -99.070 | -99.070 | ✓ |
| [4]→[5] | -194.394 | -194.394 | ✓ |
| [5]→[6] | -160.439 | -160.439 | ✓ |
| [6]→[7] | -98.004 | -98.004 | ✓ |

**全 7 境界で浮動小数点一致**。v5 まで各 segment が独立して元アニメを頭から再生していた状態 (常に 408 から始まる) が解消。

**v5 との比較 (X Values)**:
- v5: 全 segment で `[408.0, -250.0, 178.0]` が deep copy されていた
- v6: 各 segment が元軌跡の該当区間のみ保持、境界値が連続

---

## 技術 PASS と UX PASS の分離

上記指標は「keyframe clip/remap が Values 遷移として正しく動作した」ことを示すのみ。
**user が YMM4 で視覚確認して「発話 timing 起因の破綻が消え、元の振り向きアニメ + motion effect が重畳される」と判定するまで UX PASS とは呼ばない**。

### user 視覚確認手順

1. YMM4 で `_tmp/b2_haitatsuin_motion_applied_v6.ymmp` を開く
2. タイムライン Layer 9 (GroupItem) が 8 segment に分割されていること
3. 各 segment の `X` を GUI で確認 — 隣接 segment 間で値が連続し、元の振り向き軌跡が保たれていること (各 segment で 408 から再始動せず、前 segment 末の位置から続く)
4. プレビュー再生で、元の左右振り向きの流れが維持されたうえで、motion 付き segment (nod / surprise_jump / panic_shake / deny_shake) で library v2 の motion effect が重畳されること
5. 平行移動が全 segment で繰り返し再生される v5 の破綻が解消していること

### UX PASS 判定

| 判定 | 次アクション |
|---|---|
| **OK** (元軌跡 + motion 重畳) | canonical template 主経路が user 実感として成立。次は本番運用 |
| **部分 OK** (軌跡は滑らかだが motion の振幅が弱い/強い) | library v2 のパラメータ調整 (別 ticket) |
| **NG** (依然として平行移動が繰り返される or 顔が追従しない) | 原因切り分け: GroupItem 配下の ImageItem 側に直接 animated 属性が書かれていないか / _clip_animated_to_segment の適用範囲漏れ |

---

## スコープ境界と別 ticket

| 対象 | 対象外 (別 ticket) |
|---|---|
| Layer 9 GroupItem の X/Y/Zoom/Rotation/Opacity 分割時 clip | TachieItem `Length=65098` (意図なしの仮置き、patch 対象外) |
| AnimationType="なし" / "直線移動" | 加速減速・Bezier 等 (warning + fallback で回避) |
| `_apply_motion_to_layer_items` の GroupItem/ImageItem 分割 | `_apply_motion_to_tachie_items` の TachieItem 分割 (今回範囲外) |

### 切り離し論点

- **RandomRotate の body/顔 独立発火**: library 側挙動。本 proof では未検証。v6 の visual 観察で前景化すれば別 ticket
- **array 対応コード** (`_parse_motion_target_layers`): 維持。装飾のみ演者 case で活きる
- **library RandomRotate→RepeatRotate 置換**: 別 ticket

---

## 関連

- [B2-haitatsuin-motion-groupitem-2026-04-19.md](B2-haitatsuin-motion-groupitem-2026-04-19.md) — v5 proof (本 proof の前提となる GroupItem 分割経路)
- [B2-haitatsuin-motion-library-v2-2026-04-19.md](B2-haitatsuin-motion-library-v2-2026-04-19.md) — library v2 proof (本 proof で library v2 のパラメータがそのまま効く)
- [SKIT_GROUP_TEMPLATE_SPEC.md](../SKIT_GROUP_TEMPLATE_SPEC.md) — canonical template 主経路

根拠: user 指示 2026-04-19「2-point linear remap は不十分、keyframe clip/remap に修正」+ inspect 実測 + INVARIANTS §skit_group canonical template 主経路
