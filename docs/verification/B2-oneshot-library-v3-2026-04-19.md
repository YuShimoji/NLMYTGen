# B-2 motion library v3: one-shot 3 sample proof (2026-04-19)

**位置づけ**: ループ系 motion を主役から外し、intentional skit に使える one-shot sample を 3 本導入。`base_prop_oneshot` schema で GroupItem segment の base X/Y/Zoom に anchor + delta を焼き込み、VideoEffects=[] として書き出す。

## 導入 3 label

| label | 用途 | delta_keyframes |
|---|---|---|
| `enter_from_left` | 登場 (横接近 + 最終フレームだけ着地) | X=[-1050, -520, -110, 26, 0], Y=[0, 0, 0, -16, 0]（移動中は縦ゼロ） |
| `deny_oneshot` | 否定 (左右のみ・大振幅) | X=[0, -220, 220, -185, 185, -125, 125, 0] のみ |
| `surprise_oneshot` | 驚き (縦のみ) | Y=[0, -28, -155, -185, -125, -55, 0] のみ |

いずれも `{"schema": "base_prop_oneshot", "delta_keyframes": {...}}` 形式で library に追記。

## 実装

- [src/cli/main.py](../../src/cli/main.py) `_load_tachie_motion_effects_map`: base_prop_oneshot dict entry を受理
- [src/pipeline/ymmp_patch.py](../../src/pipeline/ymmp_patch.py) `_motion_oneshot_base_deltas` + `_apply_oneshot_deltas_to_segment` 新設。`_apply_motion_to_layer_items` の GroupItem 分割時、v6 clip/remap 直後に anchor = clipped first-value を取り、`new Values = [anchor + d for d in delta]` を segment base prop に OVERRIDE
- 同上 `_apply_motion_to_layer_items`: 分割後の各 GroupItem に `Remark` を `motion:<label> utt:<index>` で付与（タイムライン上で segment と motion を対応づけ）
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

技術 PASS (inspect 実測、`_tmp/b2_haitatsuin_oneshot_block2.ymmp`):

| seg | Remark | motion | base prop（要点） | VideoEffects |
|---|---|---|---|---|
| [0] F=0 L=201 | `motion:enter_from_left utt:1` | enter_from_left | X 多段 + Y は最後だけ沈み、Zoom/Rotation なし | `[]` |
| [2] F=476 L=98 | `motion:surprise_oneshot utt:3` | surprise_oneshot | **Y だけ**が大きく変化（7 キー）、Rotation 固定 0 | `[]` |
| [6] F=1202 L=145 | `motion:deny_oneshot utt:8` | deny_oneshot | **X だけ**が ±220 級で往復、Y は一定 | `[]` |

**なぜ前より読み分けやすいか（設計）**

- `surprise_oneshot`: delta を **Y のみ**に限定し Zoom/Rotation を外した → 斜め・ふわふわの主因だった複合軸を排除。
- `deny_oneshot`: delta を **X のみ**に限定し振幅を上げた → pan 上でも「横方向のレール」として単独で目立つ。
- `enter_from_left`: 横接近は X のみ、縦は **着地 1 拍**だけ → 「流れてくる」と「止まる」の二段が分離。

v6 clip/remap は他 segment (pan-only) で引き続き機能し、元軌跡該当区間を保持。

pytest: 既存 32 件 PASS。

## UX 判定

user が YMM4 で `_tmp/b2_haitatsuin_oneshot_block2.ymmp` を開き、
- index 1: 横スライドのあと一拍だけ縦が沈み、**止まって着地**したように見える
- index 3: **縦だけ**大きく跳ねる（驚き）。斜め漂いに見えないこと
- index 8: **左右だけ**大きく往復し、否定として追える。驚き区間と**動きの軸**が違うこと

を確認。OK なら library v3 導入成立、skit_01 に進める。

根拠: user 指示 2026-04-19「docs を書くより動く sample を 1 本増やす / loop 系 motion を主役にしない / 1 sample = 1 本の完結した one-shot」
