# skit_01_delivery_dispute v2 proof (2026-04-20)

**今回の生成物（正本）**: 茶番用の再生成 YMMP は **`_tmp/skit_01_v2.ymmp`**（`apply-production` の `-o` 指定）。`skit_02.ymmp` という固定ファイルは置いていない; 同内容を `_tmp/skit_02.ymmp` として出すなら `-o` だけ差し替え。

**位置づけ**: one-shot を**軸別**（驚き=縦 / 否定=横 / 登場=横+着地）に再定義し、GroupItem `Remark` に `motion:…` を焼き込み。誤配茶番の **登場 → 行動 → 反応 → 退場**が追いやすいことを狙う。

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
- Layer 9 GroupItem: **8 segment**。各 segment の **Remark** に `motion:<label> utt:<index>`（パン区間は `utt:?` のことがある）

### motion 対応表（`_tmp/skit_01_v2.ymmp` Layer 9 GroupItem）

| Frame range | Remark | motion | 意図 |
|---|---|---|---|
| F=0–200 (L=201) | `motion:enter_from_left utt:1` | enter_from_left | 登場（横接近→着地） |
| F=201–475 | `motion:nod utt:2` | nod | 行動（会釈相当・RepeatMove） |
| F=476–573 | `motion:surprise_oneshot utt:3` | surprise_oneshot | 驚き（**Y 軸のみ**の one-shot） |
| F=574–1201 | `motion:none utt:?` | none | 台詞のみ・カメラ pan |
| F=1202–1346 | `motion:deny_oneshot utt:8` | deny_oneshot | 否定（**X 軸のみ**の one-shot） |
| F=1347–1490 | `motion:none utt:?` | none | pan |
| F=1491–1666 | `motion:exit_left utt:10` | exit_left | 退場 |
| F=1667–1987 | `motion:none utt:?` | none | pan 残響 |

inspect 実測（差分の大きい one-shot のみ）:

| seg | F | L | X / Y（要点） | VideoEffects |
|---|---|---|---|---|
| 0 | 0 | 201 | X 多段、Y は **最後だけ** -73 付近へ沈む | `[]` |
| 2 | 476 | 98 | **Y のみ** 7 キーで大きく上下、Rotation 0 固定 | `[]` |
| 4 | 1202 | 145 | **X のみ** ±220 級で往復、Y は一定 | `[]` |

**なぜ deny / surprise を見分けやすいか**

- ライブラリで **surprise は Y のみ・deny は X のみ**に分離したため、合成で斜めに見えにくい。
- 各 segment に **Remark** が入るため、タイムライン上でラベルと見た目を突き合わせできる。

- one-shot segment (0/2/4) の VideoEffects=[] → base prop 焼き込みで純粋 one-shot
- pan segment (1/3/5/7) は v6 clip/remap で元軌跡を保持、境界連続
- 既存 library エントリ (nod / exit_left) も同時併用可能

## UX 判定 (user)

YMM4 で `_tmp/skit_01_v2.ymmp` を開き、タイムライン再生で次を確認:

1. scene 1: 配達員が左外から入り、軽い行き過ぎ後に着地する（登場として読める）
2. scene 2: 誤配に気づく台詞と同時に、**縦方向だけ**大きく跳ねる（斜め漂いではない）
3. scene 3: 「今はダメです!」で **左右方向だけ**大きく往復する（驚きの縦ジャンプと軸が違う）
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
