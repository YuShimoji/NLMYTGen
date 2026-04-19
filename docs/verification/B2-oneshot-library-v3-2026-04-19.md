# B-2 motion library v3: one-shot 3 sample proof (2026-04-19)

**位置づけ**: ループ系 motion を主役から外し、intentional skit に使える one-shot sample を 3 本導入。`base_prop_oneshot` schema で GroupItem segment の base X/Y/Zoom に anchor + delta を焼き込み、VideoEffects=[] として書き出す。

## 導入 3 label

| label | 用途 | delta_keyframes |
|---|---|---|
| `enter_from_left` | 登場 (左から) | X=[-800, 0] AT=直線移動 |
| `deny_oneshot` | 否定 (左右に 3 往復して戻る) | X=[0, -25, 25, -15, 15, 0] AT=直線移動 |
| `surprise_oneshot` | 驚き (Y 跳ね + Zoom ふくらみ) | Y=[0, -50, -25, -55, 0], Zoom=[0, 8, 4, 8, 0] AT=直線移動 |

いずれも `{"schema": "base_prop_oneshot", "delta_keyframes": {...}}` 形式で library に追記。

## 実装

- [src/cli/main.py](../../src/cli/main.py) `_load_tachie_motion_effects_map`: base_prop_oneshot dict entry を受理
- [src/pipeline/ymmp_patch.py](../../src/pipeline/ymmp_patch.py) `_motion_oneshot_base_deltas` + `_apply_oneshot_deltas_to_segment` 新設。`_apply_motion_to_layer_items` の GroupItem 分割時、v6 clip/remap 直後に anchor = clipped first-value を取り、`new Values = [anchor + d for d in delta]` を segment base prop に OVERRIDE
- `_motion_effects_for_label`: base_prop_oneshot entry は VideoEffects=[] を返す

方針: 感情表現・行動 segment 中は camera pan を一拍停めて motion を clean に見せる (intentional trade-off)。

## proof

入力 IR: [samples/_probe/b2/haitatsuin_ir_oneshot_block2.json](../../samples/_probe/b2/haitatsuin_ir_oneshot_block2.json) — v3 IR の index 1/3/8 を `enter_from_left` / `surprise_oneshot` / `deny_oneshot` に差替。

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/b2/haitatsuin_ir_oneshot_block2.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/b2_haitatsuin_oneshot_block2.ymmp
```

技術 PASS (inspect 実測):

| seg | motion | base prop 変換 | VideoEffects |
|---|---|---|---|
| [0] F=0 L=201 | enter_from_left | X=[-392, 408] (anchor 408 + delta) | `[]` |
| [2] F=476 L=98 | surprise_oneshot | Y=[-57, -107, -82, -112, -57] + Zoom=[103.8, 111.8, 107.8, 111.8, 103.8] | `[]` |
| [6] F=1202 L=145 | deny_oneshot | X=[-160.4, -185.4, -135.4, -175.4, -145.4, -160.4] (anchor -160.4 中心の shake) | `[]` |

v6 clip/remap は他 segment (index 2/4/5/7/9/10 などの pan-only) で引き続き機能し、元軌跡該当区間を保持。

pytest: 既存 32 件 PASS。

## UX 判定

user が YMM4 で `_tmp/b2_haitatsuin_oneshot_block2.ymmp` を開き、
- index 1 で配達員が左から登場する one-shot
- index 3 で Y 方向の 1 jump + Zoom ふくらみ
- index 8 で左右 3 往復の首振りが 1 回きりで終わる (ループしない)

を確認。OK なら library v3 導入成立、skit_01 に進める。

根拠: user 指示 2026-04-19「docs を書くより動く sample を 1 本増やす / loop 系 motion を主役にしない / 1 sample = 1 本の完結した one-shot」
