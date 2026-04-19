# skit_01_delivery_dispute v2 proof (2026-04-20)

**位置づけ**: library v3 one-shot を UX 再設計したうえで、`skit_01` を「誤配トラブル」の短い茶番として再構成。**登場 → 行動 → 反応 → 退場**の 4 ビートが連続して読めることを確認する。

## storyboard (3 scene)

| scene | utter | 内容 | 使用 motion |
|---|---|---|---|
| 1: 登場 | 1 | 配達員が勢いよく滑り込んで登場 | `enter_from_left` (base_prop one-shot) |
| 1: 行動 | 2 | 受け取り拒否を受けて応対する | `nod` (短尺、主役化しない) |
| 2: 反応 | 3 | 誤配に気づき強く驚く | `surprise_oneshot` (base_prop one-shot) |
| 2: 進行 | 4-7 | 行き先確認と立て直し会話 | `none` |
| 3: 否定 | 8 | 「その向きはダメ」を強く否定 | `deny_oneshot` (base_prop one-shot) |
| 3: 収束 | 9 | 配達員がやり直しを宣言 | `none` |
| 4: 退場 | 10 | 左へ退場して場面を閉じる | `exit_left` (InOutMove OUT) |

## 入力 / 実行

```bash
uv run python -m src.cli.main apply-production \
  samples/characterAnimSample/haitatsuin_2026-04-12.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --face-map samples/face_map_bundles/haitatsuin.json \
  --bg-map samples/_probe/b2/palette_extract/bg_map.json \
  --tachie-motion-map samples/tachie_motion_map_library.json \
  -o _tmp/skit_01_v2.ymmp
```

## 技術 PASS

- exit 0 / fatal_warning 0 / Face changes 50 / VideoEffects writes (motion) 10
- Layer 9 GroupItem: **8 segment に分割**。各 segment に意図どおりの motion / base prop を焼き込み

inspect 実測:

| seg | F | L | X Values | Y Values | VideoEffects | 役割 |
|---|---|---|---|---|---|---|
| 0 | 0 | 201 | [-572.0, -12.0, 318.0, 432.0, 408.0] | [13.0, -21.0, -49.0, -69.0, -57.0] | `[]` | **enter_from_left** (滑り込み + 着地) |
| 1 | 201 | 275 | [274.9, 92.9] (pan 継続) | [-57.0] | `[RepeatMoveEffect]` | **nod** (既存 library) |
| 2 | 476 | 98 | [92.9, 28.0] (pan 継続) | [-57.0, -39.0, -161.0, -111.0, -83.0, -57.0] | `[]` | **surprise_oneshot** (のけぞり + 跳ね) |
| 3 | 574 | 628 | [28.0, -250.0, -160.4] (pan、straddle 中間 keyframe 保持) | [-57.0] | `[]` | none (pan) |
| 4 | 1202 | 145 | [-160.4, -280.4, -50.4, -256.4, -72.4, -204.4, -160.4] | [-57.0, -47.0, -49.0, -51.0, -53.0, -55.0, -57.0] | `[]` | **deny_oneshot** (強い首振り否定) |
| 5 | 1347 | 144 | [-98.0, -36.0] | [-57.0] | `[]` | none (pan) |
| 6 | 1491 | 176 | [-36.0, 39.8] + VideoEffects | [-57.0] | `[InOutMoveFromOutsideImageEffect]` | **exit_left** |
| 7 | 1667 | 321 | [39.8, 178.0] | [-57.0] | `[]` | none (pan 残響) |

- one-shot segment (0/2/4) の VideoEffects=[] → base prop 焼き込みで純粋 one-shot
- pan segment (1/3/5/7) は v6 clip/remap で元軌跡を保持、境界連続
- 既存 library エントリ (nod / exit_left) も同時併用可能

## UX 判定 (user)

YMM4 で `_tmp/skit_01_v2.ymmp` を開き、タイムライン再生で次を確認:

1. scene 1: 配達員が左外から入り、軽い行き過ぎ後に着地する（登場として読める）
2. scene 2: 誤配に気づく台詞と同時に、のけぞり→跳ね戻りが走る（反応として読める）
3. scene 3: 「今はダメです!」で左右首振りの否定が明確に出る（平行移動だけに見えない）
4. scene 4: 退場台詞で左へ抜け、場面が閉じる

各 one-shot motion がループせずに 1 発で終わることを確認する。OK なら skit_01 成立。

## 関連

- [B2-oneshot-library-v3-2026-04-19.md](B2-oneshot-library-v3-2026-04-19.md) — library v3 の 3 one-shot proof
- [B2-haitatsuin-motion-groupitem-keyframe-remap-2026-04-19.md](B2-haitatsuin-motion-groupitem-keyframe-remap-2026-04-19.md) — v6 clip/remap (pan segment の基盤)

## 残課題 (skit_02 以降)

- 既存 `nod` が RepeatMoveEffect 依存 (ループ) → `nod_oneshot` を base_prop_oneshot schema で追加する
- `look_aside` / `puzzled_oneshot` / `point_at` / `approach` / `back_off` / `turn_around` 等、感情表現 + 軽アクション系の残り sample
- 複数キャラ同時登場 (霊夢・魔理沙の同期モーション)

根拠: user 指示 2026-04-19「一本の意図ある茶番劇を実際に作る / 動くものを先に」
