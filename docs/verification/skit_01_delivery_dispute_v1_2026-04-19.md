# skit_01_delivery_dispute v1 proof (2026-04-19)

**位置づけ**: library v3 の one-shot sample と v6 clip/remap を組み合わせた、**最初の intentional skit**。登場 → 会釈 → 驚き → 否定 → 退場までを 1 本の完結した流れとして組み立て、YMM4 で実再生可能な形に焼く。

## storyboard (3 scene)

| scene | utter | 内容 | 使用 motion |
|---|---|---|---|
| 1: 導入 | 1 | 配達員が画面外から中央へ登場 | `enter_from_left` (library v3 one-shot) |
| 1: 導入 | 2 | 軽く会釈 | `nod` (既存 library v2, RepeatMove) |
| 2: 驚き | 3 | 話の展開に驚く | `surprise_oneshot` (library v3 one-shot) |
| 2: 間 | 4-7 | 沈黙 (camera pan 継続) | `none` |
| 3: 反発 | 8 | 否定 (左右 3 往復) | `deny_oneshot` (library v3 one-shot) |
| 3: 間 | 9 | 余韻 | `none` |
| 3: 退場 | 10 | 左へ退場 | `exit_left` (既存 library v2 InOutMove OUT) |

## 入力 / 実行

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/skit_01_v1.ymmp
```

## 技術 PASS

- exit 0 / fatal_warning 0 / Face changes 50 / VideoEffects writes (motion) 10
- Layer 9 GroupItem: **8 segment に分割**。各 segment に意図どおりの motion / base prop を焼き込み

inspect 実測:

| seg | F | L | X Values | Y Values | VideoEffects | 役割 |
|---|---|---|---|---|---|---|
| 0 | 0 | 201 | [-392.0, 408.0] | [-57.0] | `[]` | **enter_from_left** (anchor 408 + delta [-800, 0]) |
| 1 | 201 | 275 | [274.9, 92.9] (pan 継続) | [-57.0] | `[RepeatMoveEffect]` | **nod** (既存 library) |
| 2 | 476 | 98 | [92.9, 28.0] (pan 継続) | [-57.0, -107, -82, -112, -57] | `[]` | **surprise_oneshot** (Y jump + Zoom pop) |
| 3 | 574 | 628 | [28.0, -250.0, -160.4] (pan、straddle 中間 keyframe 保持) | [-57.0] | `[]` | none (pan) |
| 4 | 1202 | 145 | [-160.4, -185.4, -135.4, -175.4, -145.4, -160.4] | [-57.0] | `[]` | **deny_oneshot** (anchor -160.4 中心 shake) |
| 5 | 1347 | 144 | [-98.0, -36.0] | [-57.0] | `[]` | none (pan) |
| 6 | 1491 | 176 | [39.8] + VideoEffects | [-57.0] | `[InOutMoveFromOutsideImageEffect]` | **exit_left** |
| 7 | 1667 | 321 | [39.8, 178.0] | [-57.0] | `[]` | none (pan 残響) |

- one-shot segment (0/2/4) の VideoEffects=[] → base prop 焼き込みで純粋 one-shot
- pan segment (1/3/5/7) は v6 clip/remap で元軌跡を保持、境界連続
- 既存 library エントリ (nod / exit_left) も同時併用可能

## UX 判定 (user)

YMM4 で `_tmp/skit_01_v1.ymmp` を開き、タイムライン再生で次を確認:

1. scene 1: 配達員が左から滑り込んで中央に到着、会釈する
2. scene 2: utter 3 で 1 発ジャンプ (Y + Zoom pop) が走る、その後は camera pan のみ
3. scene 3: utter 8 で左右 3 往復 1 回きりの首振り、utter 10 で左へ退場

各 one-shot motion がループせずに 1 発で終わることを確認する。OK なら skit_01 成立。

## 関連

- [B2-oneshot-library-v3-2026-04-19.md](B2-oneshot-library-v3-2026-04-19.md) — library v3 の 3 one-shot proof
- [B2-haitatsuin-motion-groupitem-keyframe-remap-2026-04-19.md](B2-haitatsuin-motion-groupitem-keyframe-remap-2026-04-19.md) — v6 clip/remap (pan segment の基盤)

## 残課題 (skit_02 以降)

- 既存 `nod` が RepeatMoveEffect 依存 (ループ) → `nod_oneshot` を base_prop_oneshot schema で追加する
- `look_aside` / `puzzled_oneshot` / `point_at` / `approach` / `back_off` / `turn_around` 等、感情表現 + 軽アクション系の残り sample
- 複数キャラ同時登場 (霊夢・魔理沙の同期モーション)

根拠: user 指示 2026-04-19「一本の意図ある茶番劇を実際に作る / 動くものを先に」
