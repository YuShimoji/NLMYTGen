# G-26 Visual Acceptance Handoff

> **対象**: `build-motion-recipes` で生成済の 16 recipe を YMM4 で目視確認し、各 recipe を 9 区分で分類する作業手順。
>
> **位置づけ**: [MOTION_PRODUCTION_PIPELINE.md § 5 Phase E](../MOTION_PRODUCTION_PIPELINE.md) の実走 handoff。本書 1 件で acceptance を完遂できるよう独立して書く。
>
> **資料**: [`_tmp/g26/acceptance_pack/INDEX.md`](../../_tmp/g26/acceptance_pack/INDEX.md) に 16 recipe + 3 sheet + 3 promotion log のリンク集。

---

## 0. 前提

- `build-motion-recipes` が出力した 3 つの review `.ymmp` は **machine 検証 pass 済**（canvas / openability / asset path 健全）
- 残るのは「演出として読めるか」の **目視確認のみ**
- 機械では判定できない (`pass` / `wrong motion` / `body-face drift` / `too subtle` / `too strong` ...)
- 16 recipe あるため一度に全部見る必要はない。brief 単位 (12 + 2 + 2) で分けて取り組んで OK

---

## 1. YMM4 で開くファイル (絶対パス)

| # | brief | 開くパス | recipe 数 |
|--:|-------|---------|---------:|
| 1 | v1 | `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\_tmp\g26\recipe_pipeline\g26_motion_recipe_review_v1.ymmp` | 12 |
| 2 | slice3_proof | `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\_tmp\g26\recipe_pipeline\g26_motion_recipe_review_slice3_proof.ymmp` | 2 |
| 3 | slice4_proof | `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\_tmp\g26\recipe_pipeline\g26_motion_recipe_review_slice4_proof.ymmp` | 2 |

3 ファイルを順に開いていく。各ファイルの timeline 上に recipe が一定間隔で配置されている。

---

## 2. 各 recipe の確認手順 (1 件あたり 1〜2 分)

各 review `.ymmp` を YMM4 で開いた後:

1. **対応 sheet を別画面で開く** ([INDEX.md](../../_tmp/g26/acceptance_pack/INDEX.md) の "sheet" 列)
2. timeline の **frame 列**に sheet 上の frame 値を入力 (例: 420 → `Ctrl+G` などで frame jump、もしくはタイムスケール上で該当 frame まで scroll)
3. 該当 frame から **再生** (Space などで再生)
4. recipe の Length 分の動きを観察
5. sheet の `what to look for` 列を見て、期待動作と一致するか判定
6. 9 区分のいずれかを sheet の `class` 列に記入
7. 違和感があれば `note` 列に短くコメント (例: 「nod は OK だが zoom が遅すぎる」)

---

## 3. 9 区分の判定基準

| class | 判定基準 | 次手 |
|-------|---------|------|
| `pass` | 演出意図通りに動いて、シーンに使える品質 | library promotion 候補 |
| `wrong motion` | 意図と違う動き (例: 頷きを期待したが横揺れだった) | brief 見直し → Phase A 戻り |
| `body-face drift` | Rotation 系で **顔と体の anchor がずれる**。首だけ動くべきが身体ごと回る、など | CenterPointEffect の anchor 設定確認 |
| `too subtle` | 動きが弱すぎて気づかない | intensity 上げる (`light` → `medium` / `strong`)、振幅 / Rotation 角度を増やす |
| `too strong` | 動きが過剰でうるさい / 不自然 | intensity 下げる、振幅 / 角度を減らす |
| `screen spacing` | 画面位置 (X / Y baseline) がおかしい | seed / template-source 不一致疑い |
| `asset path` | 素材ファイル参照が切れていて表示されない | Phase D 出力やり直し |
| `openability` | YMM4 で開けない、エラーが出る | 通常は発生しない想定 (machine 検証 pass 済) |
| `community plugin missing` | community プラグインが無くてエフェクトが効かない | 動きの失敗ではない。プラグイン入れて再確認は別タイミング |

---

## 4. 報告形式 (どちらでも OK)

### 形式 A: チャットで列挙 (お手軽)

```
v1:
- frame 0 nod_clear: pass
- frame 140 nod_subtle: too subtle
- frame 280 nod_double: pass
- frame 420 jump_small: pass
- frame 560 jump_high: pass
- frame 700 jump_emphasis: pass
- frame 840 panic_crash: community plugin missing
- frame 980 shocked_jump: pass
- frame 1120 surprised_chromatic: too strong (zoom が大きすぎる)
- frame 1260 anger_outburst: pass
- frame 1400 shobon_droop: pass
- frame 1540 lean_curious: pass

slice3_proof:
- frame 0 realization_nod: pass
- frame 180 sad_tilt_blur: too subtle (blur が弱い)

slice4_proof:
- frame 0 excited_double_jump: pass
- frame 180 thinking_circle_pause: looks like nod (細かく揺れて見える)
```

### 形式 B: sheet を埋めて貼る

[`visual_acceptance_sheet.md`](../../_tmp/g26/acceptance_pack/visual_acceptance_sheet.md) / [`visual_acceptance_sheet_slice3_proof.md`](../../_tmp/g26/acceptance_pack/visual_acceptance_sheet_slice3_proof.md) / [`visual_acceptance_sheet_slice4_proof.md`](../../_tmp/g26/acceptance_pack/visual_acceptance_sheet_slice4_proof.md) の `class` 列を埋めて、編集後ファイルをチャットで貼る。

形式 A のほうが簡単。コメントが多い場合や複数項目の note を残したい場合は形式 B。

---

## 5. 特に注目してほしい点

### 優先度 高: body-face drift と too subtle

これら 2 つはコード / brief / preset の **修正起点**になりやすい:

- **body-face drift**: Rotation 系 recipe (nod / lean_curious / sad_tilt_blur / realization_nod / surprised_chromatic / thinking_circle_pause) で、CenterPointEffect の anchor (Vertical=Bottom, X≈525, Y≈137) がずれている疑い。発生したら anchor 値の再確認が必要
- **too subtle**: 値の問題。intensity scaling formula ([MOTION_RECIPE_LOOP_TIMING § 4](../MOTION_RECIPE_LOOP_TIMING.md)) で 1.5〜2 倍に上げて再 build

### 優先度 中: thinking_circle_pause の "looks like nod"

`thinking_circle_pause` は forbidden_patterns に `looks like nod` が入っている。Rotation hold 形 (0→-5→-5→-5→0) が単純な対称揺れに見えてしまう場合は failure。傾けて保持しているように見えるなら pass。

### 優先度 中: surprised_chromatic の color split

`surprised_chromatic` は `ChromaticAberrationEffect` を使う初の recipe。色収差がちゃんと出ているか、Zoom 110% spike と同期しているかを観察。

### 優先度 低: panic_crash の community plugin

`panic_crash` は `CameraShakeEffect` (community plugin) を含む。プラグイン未導入の環境では `community plugin missing` で OK。**動きの失敗ではない**ので深追いせず、別タイミングでプラグイン入れて再確認すれば良い。

---

## 6. assistant 側 promotion フロー (ユーザー報告受領後の作業)

ユーザー分類報告を受けたら、assistant が以下を実行 (1 commit にまとめる想定):

1. **promotion_log.json 3 件を埋める**
   - `_tmp/g26/acceptance_pack/promotion_log{,_slice3_proof,_slice4_proof}.template.json` の `entries[]` 各行に visual_class / visual_note / promote_to / promotion_reason を入力
   - `template.json` → 受領済確定版にリネーム保存

2. **`pass` recipe について library 反映**
   - `samples/tachie_motion_map_library.json` の `motions` dict に新 entry 追加
     - effect chain は preset 経路なら `DEFAULT_RECIPE_PRESETS` の値、brief-only なら brief の `effect_names` から構築
     - parameters は readback の route_values を `build_library_v2.py` 形式に変換
   - `docs/MOTION_PRESET_LIBRARY_SPEC.md § 3` のラベル表に新ラベル行を append (emotion カテゴリ別)
   - `docs/FEATURE_REGISTRY.md` G-26 行に「**Phase E promotion (2026-05-01)**: N recipe accepted, library 更新」を追記

3. **`too subtle` / `too strong` recipe について再 build**
   - intensity scaling formula で値調整
     - too subtle: amplitude 1.5x, Period 0.8x
     - too strong: amplitude 0.6x, Period 1.2x
   - preset 経路は `motion_recipe.py` の `DEFAULT_RECIPE_PRESETS` を編集、brief-only は brief を編集
   - 同 brief で `build-motion-recipes` 再実行 → 修正版 review .ymmp を出力
   - 修正版用の sheet と promotion_log を新規作成 (再 acceptance 用)

4. **`wrong motion` / `body-face drift` recipe について Phase A 戻り**
   - S-5 brief 見直し: scene_input の解釈が違っていないか、emotion / intensity 設定が適切か再判定
   - body-face drift は CenterPointEffect anchor 値の再観測 (Vertical=Bottom, X / Y 値の再測定)

5. **`community plugin missing` は記録のみ**
   - 動きの失敗ではないので library 反映なし、再 build なし
   - プラグイン環境整備は別タスクとして runtime-state に記録

6. **runtime-state.md 更新**
   - `next_action` を「acceptance 待ち」から次手に更新 (例: pass 件数によっては「Slice 5 候補へ」)
   - `last_change_relation` / `last_verification` を Phase E 結果で更新

7. **verification doc 作成**
   - `docs/verification/G26-phase-e-promotion-result-2026-05-01.md` に集計記録
     - 16 recipe 中: pass N / fail M (内訳) / community-pending K
     - library に追加された emotion ラベル一覧
     - 再 build / brief 見直し対象の goal_id 一覧
     - 次手 (Slice 5 候補 / Phase E 完了 / etc.)

8. **1 commit + push**
   - 修正済 promotion log 3 件 + library 更新 + spec 表 + registry + verification doc を 1 commit に
   - commit message に accepted / failed の件数集計を含める

---

## 7. 参考リンク

- [INDEX.md](../../_tmp/g26/acceptance_pack/INDEX.md) — 16 recipe 全件 + sheet / log / inventory のリンク集
- [MOTION_PRODUCTION_PIPELINE.md § 5](../MOTION_PRODUCTION_PIPELINE.md) — Phase E 正本
- [MOTION_RECIPE_LOOP_TIMING.md § 4](../MOTION_RECIPE_LOOP_TIMING.md) — intensity scaling formula
- [MOTION_PRESET_LIBRARY_SPEC.md § 3](../MOTION_PRESET_LIBRARY_SPEC.md) — emotion ラベル表 (promotion 先)
- [G26-visual-acceptance-pack-2026-04-30.md](G26-visual-acceptance-pack-2026-04-30.md) — v1 用 acceptance pack の説明 (parallel lane 作成)
- 16 recipe の brief 出典:
  - `samples/recipe_briefs/g26_motion_recipe_brief.v1.json` (12)
  - `samples/recipe_briefs/g26_motion_recipe_brief.slice3_proof.json` (2)
  - `samples/recipe_briefs/g26_motion_recipe_brief.slice4_proof.json` (2)
