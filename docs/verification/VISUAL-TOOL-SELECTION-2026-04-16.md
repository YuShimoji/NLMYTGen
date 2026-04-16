# 視覚効果ツール選定 slice — 進捗証跡

**開始日**: 2026-04-16
**ステータス**: Step 1-2 完了 / Step 3 以降は user actor で YMM4 GUI 作業待ち
**正本**: [VISUAL_EFFECT_SELECTION_GUIDE.md](../VISUAL_EFFECT_SELECTION_GUIDE.md) / [VISUAL_TOOL_DECISION.md](../VISUAL_TOOL_DECISION.md) / [MATERIAL_SOURCING_RULES.md](../MATERIAL_SOURCING_RULES.md)
**plan 外部**: `C:/Users/PLANNER007/.claude/plans/splendid-popping-horizon.md`

---

## 1. 背景

`runtime-state.md` の優先表で「視覚効果ツール選定」は **hold (user 判断待ち)** 状態が続いていた。完了の目安が立たないため主軸昇格できず、サムネ 0 件・茶番劇アニメ 0 件・図解アニメ 0 件の未自動化状態が継続。

2026-04-16 ユーザー要望で本 slice に着手。assistant 側で判断材料 (4 類 × 3 ルート比較・エフェクト 111 種用途別再編・テンプレバンドル 5 種案) を整備し、user 側でツール決定・素材ルール・YMM4 テンプレ作成を進める構造とした。

---

## 2. 完了したこと (assistant actor)

### 2.1 新規 docs 3 件

| ファイル | 内容 |
|---------|------|
| [VISUAL_EFFECT_SELECTION_GUIDE.md](../VISUAL_EFFECT_SELECTION_GUIDE.md) | 視覚効果 4 類 × 3 ルート比較・YMM4 エフェクト 111 種の用途別再編・テンプレバンドル 5 種案・ハンズオン 5 ステップ (読み物の正本) |
| [VISUAL_TOOL_DECISION.md](../VISUAL_TOOL_DECISION.md) | Step 1 用 7 問記入テンプレ → **2026-04-16 user 記入完了** |
| [MATERIAL_SOURCING_RULES.md](../MATERIAL_SOURCING_RULES.md) | Step 2 用素材調達ルール記入テンプレ → **2026-04-16 user 記入完了** |

### 2.2 既存 docs 更新

- [NAV.md](../NAV.md): 正本マップに 3 件の索引を追加
- [USER_REQUEST_LEDGER.md](../USER_REQUEST_LEDGER.md): Backlog Delta に slice 起点・Canva 除外方針を追記
- [WORKFLOW.md](../WORKFLOW.md) §S-8: サムネ作成手順から Canva を除去
- [THUMBNAIL_ONE_SHEET_WORKFLOW.md](../THUMBNAIL_ONE_SHEET_WORKFLOW.md): Canva を除去し YMM4 完結 + 将来自動化前提を明記

### 2.3 回帰確認

- `uv run pytest --tb=no` → **329 passed / 21 skipped** (regression なし)
- `src/` 変更なし

---

## 3. ユーザー決定内容 (user actor)

### 3.1 ツール決定 ([VISUAL_TOOL_DECISION.md](../VISUAL_TOOL_DECISION.md))

| Q | 決定 | 備考 |
|---|------|------|
| Q1 茶番劇 | **B**: 外部素材 + ゆっくり頭 | いらすとや / AI 生成 (白背景) + TachieItem 重畳 |
| Q2 情報列挙 | **A**: YMM4 テキスト+図形 | 補助は AI 生成 (白背景) |
| Q3 地図・関係図 | **B**: Figma / Inkscape + AI 生成 | **Canva は使わない** |
| Q4 ムード | **A**: YMM4 内エフェクト | Pixabay/Pexels + AI 生成素材 |
| Q5 サムネイル | **A**: YMM4 内 (1 フレーム書き出し) | 将来 NLMYTGen 側で素材置き換え自動化を別途実装予定。**Canva 除外** |
| Q6 コミュプラグイン | **Yes** (自PC完結) | Wave / Tiling / VignetteBlur / Bloom 等使用可 |
| Q7 素材サイト | **いらすとや + Pixabay + Pexels + AI 生成 (白背景)** | イメージイラスト範囲内で運用 |

### 3.2 素材調達ルール ([MATERIAL_SOURCING_RULES.md](../MATERIAL_SOURCING_RULES.md))

| 項目 | 決定 |
|------|------|
| 保存場所 | A: `samples/Mat/` 続投 (全案件共通) |
| 立ち絵命名 | `{speaker}_{emotion}.png` |
| 背景命名 | `bg_{scene_type}_{variant}.png` |
| オーバーレイ命名 | `ov_{type}_{variant}.png` |
| SE 命名 | `se_{action}.wav` |
| ライセンス | A: 素材同階層に `LICENSE.csv` |
| 差し替え方針 | 既定フロー (palette 更新 → extract-template → validate-ir) |

---

## 4. 3 つの重要方針 (今回固定)

### 4.1 Canva 除外 (当初からの方針、2026-04-16 明示)

視覚効果・サムネイル・作図の候補から Canva を除外。サードパーティ SaaS への依存を作らず、ローカル完結のパイプラインを維持するため。サムネは YMM4 内作成 + 将来 NLMYTGen 側で「素材置き換え自動化」機能を別途実装する前提。

**影響範囲**: `VISUAL_EFFECT_SELECTION_GUIDE.md` / `VISUAL_TOOL_DECISION.md` / `WORKFLOW.md` §S-8 / `THUMBNAIL_ONE_SHEET_WORKFLOW.md` から Canva 推奨記述を全て除去済み。

### 4.2 Dual-rendering 運用 (2026-04-16 追加・G-22 として起票)

同一演出を **2 経路で実現可能**にする方針。詳細は [G22-dual-rendering-tachie-and-png-2026-04-16.md](G22-dual-rendering-tachie-and-png-2026-04-16.md) 正本。

- **経路 A (立ち絵 TachieItem)**: 既存の `face` / `idle_face` / `slot` + `face_map`。主要キャラの本編・表情遷移あり・整合性と演出蓄積を優先
- **経路 B (書き出し PNG の overlay 挿入)**: YMM4 で立ち絵を 1 フレーム透明 PNG に書き出し → `overlay_map` に登録 → 既存 `overlay` フィールドで挿入。背景キャラ・ワンシーン登場・サムネ素材等・工数削減を優先

**実装**: 既存 G-13 (done) でそのまま動作するため、**コード変更なし**が第一候補。registry メタ拡張 (`source: "tachie_render"` 等) は承認後に別起票。

**承認判定**: 視覚効果 slice Step 5 proof 完了時に、(A)/(B) 併用の実績から G-22 proposed → approved / 当面不要判定を決定。

### 4.3 立ち絵セットアップは踏まない (2026-04-16 明示)

視覚効果 slice の Step 3 以降で「立ち絵自体を YMM4 上で設定 (キャラクター登録・AnimationTachie プラグイン設定) し、タイムラインに立ち絵を表示させる」という手順を踏まない。既存の `samples/Mat/新れいむ/` `samples/Mat/新まりさ/` 配下のパーツ・表情はテストに十分。既存 palette.ymmp / haitatsuin.ymmp / characterAnimSample 等を **そのまま使う**。

**影響**: テンプレバンドル 5 種は、既存立ち絵入り ymmp を開いた状態で GroupItem にエフェクト追加 → テンプレ保存の運用。ゼロからの立ち絵環境構築は対象外 (G-19/G-20/G-21 系の責務)。

---

## 5. 次のステップ (user actor)

### Step 3: YMM4 テンプレ初期セット 5 種作成

**作業チェックリスト正本**: [STEP3_YMM4_TEMPLATE_CHECKLIST.md](../STEP3_YMM4_TEMPLATE_CHECKLIST.md) — 5 種テンプレ各エフェクトの parameter 初期値の目安・チェックボックス付き作業手順・失敗パターン。

**前提**: 既存の立ち絵入り ymmp を 1 本ベースにする。候補: `samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` (復旧 B で立ち絵パス書き換え済み。ただし YMM4 側キャラクター登録の修正が未完な場合あり → [HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 2026-04-17 追記参照)。テンプレ作成は **別名で複製した作業用 ymmp** で行うのが安全。

**作業内容**:

| テンプレ名 | ベース | 追加エフェクト | 用途 |
|-----------|--------|---------------|------|
| `skit_reaction_jump` | 既存立ち絵 GroupItem | JumpEffect + RandomRotateEffect | 茶番劇の驚き |
| `board_list_entry` | テキスト/図形 | InOutGetUpEffect + GradientEffect | 黒板リスト項目 |
| `map_pan_zoom` | ImageItem (背景) | CameraPositionEffect (キーフレーム) | 地図パン |
| `mood_sepia_blur` | ImageItem (背景) | SepiaEffect + GaussianBlurEffect | 雰囲気回想 |
| `intro_punch` | タイトル構成 | InOutCrashEffect + ZoomEffect | 冒頭アタック |

**GUI 手順**:

1. YMM4 で既存 ymmp を別名複製して開く
2. タイムラインの対象アイテム (GroupItem / TachieItem / ImageItem) を選択
3. 右ペインの **映像効果** から対応エフェクトを追加
4. パラメータを調整
5. 対象アイテム右クリック → **テンプレートとして保存** (上記の名前で)
6. 5 種分繰り返す
7. `ItemSettings.json` の `Templates` 配列に 5 件追加されたことを確認

### Step 3 補助: 立ち絵レンダリング PNG 書き出し (G-22 運用準備・任意)

経路 B (書き出し PNG の overlay 挿入) を使う場合の準備。**Step 3 のテンプレ作成と並行してよい**。

**作業パイプライン正本**: [STEP3_TACHIE_RENDERING_PIPELINE.md](../STEP3_TACHIE_RENDERING_PIPELINE.md) — 透明背景 PNG 書き出し・overlay_map 登録・検証までのチェックボックス付き手順・失敗パターン。

概略:

1. Step 3 と同じ作業用 ymmp を YMM4 で開く
2. 対象 VoiceItem を選択し、`TachieFaceParameter` で表情プリセットを選択 (GUI)
3. タイムライン上の背景レイヤーを一時ミュート
4. 動画出力 → **範囲 1 フレーム・透明 PNG** で書き出し
5. 出力 PNG を `samples/Mat/{speaker}_{emotion}.png` に配置 ([MATERIAL_SOURCING_RULES.md](../MATERIAL_SOURCING_RULES.md) §2-c-i の命名規約)
6. 主要表情ぶん (例: reimu_anger / reimu_easy / reimu_shocked 等) を繰り返す

詳細: [G22-dual-rendering-tachie-and-png-2026-04-16.md §3](G22-dual-rendering-tachie-and-png-2026-04-16.md)

### Step 4: registry 登録 (Step 3 と並行可)

- `bg_map.json` / `overlay_map.json` (`samples/registry_template/` から複製) にラベル登録
- **Step 3 補助で書き出した PNG も `overlay_map.json` に登録** (例: `"reimu_anger_rendered": "./samples/Mat/reimu_anger.png"`)
- `scene_presets` は G-21 承認後に assistant が雛形作成予定

### Step 5: 1 本の実案件で proof

1. `build-csv` で CSV 生成
2. Custom GPT で演出 IR 生成 (新テンプレ名を指定)
3. `validate-ir` と `apply-production --dry-run` で ERROR 0
4. YMM4 で開き、視覚効果が意図どおり出ているか目視
5. OK なら [P02-production-adoption-proof.md](P02-production-adoption-proof.md) に 1 行追記
6. [runtime-state.md](../runtime-state.md) の優先表で「視覚効果ツール選定」を hold → **done** に昇格

---

## 6. 現在の止まり位置

assistant 側の immediate 成果 (判断材料・記入テンプレ・Canva 除外・立ち絵 non-setup 方針) は出揃った。**Step 3 の YMM4 GUI 作業は user actor の責務**で、ここで本 slice は **user 作業待ちで保留**。

assistant 側で追加可能な下ごしらえ (G-21 承認後の `scene_presets.template.json` 雛形等) は、Step 5 proof 完了で G-21 昇格判定が出た後に着手する。

---

## 7. 関連ファイル

- plan (外部): `C:/Users/PLANNER007/.claude/plans/splendid-popping-horizon.md` / `C:/Users/thank/.claude/plans/fluffy-greeting-panda.md` (本セッション)
- docs: [VISUAL_EFFECT_SELECTION_GUIDE.md](../VISUAL_EFFECT_SELECTION_GUIDE.md) / [VISUAL_TOOL_DECISION.md](../VISUAL_TOOL_DECISION.md) / [MATERIAL_SOURCING_RULES.md](../MATERIAL_SOURCING_RULES.md)
- **Step 3 補助 docs (2026-04-17 新設)**: [STEP3_YMM4_TEMPLATE_CHECKLIST.md](../STEP3_YMM4_TEMPLATE_CHECKLIST.md) / [STEP3_TACHIE_RENDERING_PIPELINE.md](../STEP3_TACHIE_RENDERING_PIPELINE.md)
- registry 雛形: [samples/registry_template/](../../samples/registry_template/)
- エフェクトカタログ: [samples/effect_catalog.json](../../samples/effect_catalog.json) / [samples/EFFECT_CATALOG_USAGE.md](../../samples/EFFECT_CATALOG_USAGE.md)
- 既存立ち絵: `samples/Mat/新れいむ/` / `samples/Mat/新まりさ/`
- 既存 ymmp (テンプレベース候補): [samples/characterAnimSample/haitatsuin_2026-04-12.ymmp](../../samples/characterAnimSample/haitatsuin_2026-04-12.ymmp)

---

## 8. 変更履歴

- 2026-04-16: 初版。Step 1-2 完了時点の進捗を記録。Step 3-5 は user actor 作業待ち
- 2026-04-16: Dual-rendering 運用を §4.2 に追加し G-22 起票。Step 3 補助 (立ち絵レンダリング PNG 書き出し) と Step 4 の PNG 登録指示を追加
- 2026-04-17: Step 3 / Step 3 補助のチェックリスト正本として [STEP3_YMM4_TEMPLATE_CHECKLIST.md](../STEP3_YMM4_TEMPLATE_CHECKLIST.md) / [STEP3_TACHIE_RENDERING_PIPELINE.md](../STEP3_TACHIE_RENDERING_PIPELINE.md) を新設・リンク。[MATERIAL_SOURCING_RULES.md](../MATERIAL_SOURCING_RULES.md) §2-c-i に立ち絵レンダリング PNG の命名規約を追記。user の B-2 haitatsuin 視覚確認 NG 所見を [HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md](HAITATSUIN-TACHIE-PATH-RECOVERY-2026-04-16.md) 末尾に追記 (原因は YMM4 キャラクター登録側の migrated_tachie 参照)
