# 立ち絵 — 複数体素材 × ゆっくり顔差し替え（準備パック・別スレッド起動用）

**ステータス**: 準備完了（**実装は未着手**）。台帳は [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) の **G-19 / G-20（`proposed`）** を参照。  
**目的**: 複数の体素材にゆっくり顔を差し替え、必要なら反転・平行移動で視覚整合を取り、将来はより複雑な動きまで拡張する。

---

## 0. 読む順（このスレッドで最初に）

1. [AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md) — L2/L3。C-04/C-05 **rejected**（Python が YMM4 内配置を直接操作しない）を再確認する。  
2. [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) — `face` / `slot` / `motion` の既存契約。  
3. [G02b-ymmp-structure-analysis.md](G02b-ymmp-structure-analysis.md) — `TachieFaceParameter` パーツ差し替えの前提。  
4. 実装入口: [src/pipeline/ymmp_patch.py](../../src/pipeline/ymmp_patch.py)（`_apply_face_to_voice_item` / `_apply_slots` / motion 系）。

---

## 1. ユーザー要求 → 作業への対応表

| 要求 | 第一の置き場 | 機械化する場合の候補 |
|------|----------------|----------------------|
| 複数体にゆっくり顔を載せる | YMM4 テンプレ + **face_map**（パーツパス） | **G-19**: 体バリアントごとの map 束ね、IR からの選択 |
| 反転・平行移動で崩れない | テンプレ既定 or ymmp の幾何プロパティ調査 | **G-20**: IR + `validate-ir` + patch（**ymmp キー調査が先**） |
| より複雑な動き | 既存 **G-17**（`motion_map` / `tachie_motion_effects_map` / timeline profile） | まず G-17 範囲で足りるか検証。足りなければ **別途 `proposed` 起票** |

---

## 2. フェーズ別チェックリスト（別スレッドの進め方）

### A — スコープ固定（コードを触る前）

- [ ] 対象プラグイン（例: AnimationTachie）とキャラ（例: 霊夢・魔理沙）を 1 行で固定する。  
- [ ] 「自動化する／手動のまま」の境界を [AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md) に照らして書く。  
- [ ] 成果物の定義: 「N 種類の体で同じ IR から apply が通る」等、**検証可能な一文**。

### B — YMM4 資産（オペレータ主）

- [ ] 体バリエーションを N 種、テンプレに載せ、`extract-template --labeled` で **安定ラベル**が取れるか確認（現状サンプル ymmp は VoiceItem **Remark 未設定**のため `--labeled` 抽出は 0 件。Remark 付与後に再実行が必要。未ラベル版でのパターン数確認は [§2.1](#21-フェーズ-ac-記入メモ準備スレッド2026-04-13) 参照）。  
- [ ] 各体で顔パーツの位置ずれが許容内か（代表フレームで目視）。  
- [ ] 反転・微移動を **テンプレだけで足りる**か、**patch が必要**か方針決め。

### C — 既存機械への寄せ（G-19 の前段）

- [ ] 体ごとに `face_map` を分ける or ラベル名前空間（例: `reimu_bodyA_smile`）の案を書く。  
- [ ] 最小 IR で `validate-ir` → `apply-production --dry-run` が **ERROR なし**になる組み合わせを 1 本決める。

### D — 実装（G-19 / G-20 が **`approved` になってから**）

- [x] [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) を `approved` に更新してからコード変更。（2026-04-13: G-19 approved + 実装完了）
- [x] 縦スライス 1 本 = 1 承認（[CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) の精神）。
- [x] `NLMYTGEN_PYTEST_FULL=1 uv run pytest` 緑。（328 pass）
- [x] [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) を追随。
- **G-20 は未実施**（YMM4 GUI 確認待ち）。

### E — 検証

- [x] [G19-face-map-bundle-implementation.md](G19-face-map-bundle-implementation.md) に実装記録。  
- [ ] 変更した `face_map` / IR サンプルパスを明記。

### 2.1 フェーズ A〜C 記入メモ（準備スレッド・2026-04-13）

| フェーズ | 状態 | 内容 |
|---------|------|------|
| **A** | 記入済 | **対象（1 行）**: プラグインは **`YukkuriMovieMaker.Plugin.Tachie.AnimationTachie`**（サンプル ymmp および G02b と一致）。キャラ名はプロジェクトごとに異なるため、検証時は **1 キャラの `CharacterName` 表記を 1 行で固定**（例: サンプル上の「ゆっくり魔理沙」系）し、以降の `face_map` キーと一致させる。**境界（AUTOMATION_BOUNDARY）**: L2 は **IR・`face_map`・registry・CSV・validate** まで。体パーツの画像合成・レンダリングは行わない。L3 は YMM4 上の見た目最終調整。patch は **台本読込後 ymmp の限定後段**のみ。**検証可能な成功条件（承認後スライス用）**: 同一 Production IR に対し、**体バリアント（`body_id`）を切り替えたマップ束ね**で `validate-ir` が ERROR なし、`apply-production --dry-run` が失敗しない（実装は G-19 `approved` 後）。 |
| **B** | 部分実施（2026-04-12 サンプル） | **対象 ymmp**: [samples/characterAnimSample/haitatsuin_2026-04-12.ymmp](../../samples/characterAnimSample/haitatsuin_2026-04-12.ymmp)。**パス寄せ**: `D:\\MovieCreationWorkspace\\...` を廃止し、立ち絵パーツ参照を [samples/characterAnimSample/migrated_tachie/](../../samples/characterAnimSample/migrated_tachie/) 配下（ymmp からの **相対パス**）へ寄せた（再現手順: [samples/characterAnimSample/_migrate_moviecreation_paths.py](../../samples/characterAnimSample/_migrate_moviecreation_paths.py)）。元 D ドライブ素材はリポに無いため、各ファイルは `reimu_easy.png` の複製プレースホルダ。**`extract-template --labeled`**: 出力 [samples/characterAnimSample/extract_template_labeled/face_map.json](../../samples/characterAnimSample/extract_template_labeled/face_map.json) は **{}**（Remark 未設定のため 0 パターン）。**未ラベル `extract-template`（参考）**: [samples/characterAnimSample/face_map_extracted.json](../../samples/characterAnimSample/face_map_extracted.json)（= [extract_template_unlabeled/face_map.json](../../samples/characterAnimSample/extract_template_unlabeled/face_map.json) 相当）に **2 パターン**（魔理沙黄縁 / 霊夢赤縁）。幾何・Tier への反映: [TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md) §6。 |
| **C** | 記入済 | **体ごと分離 vs ラベル名前空間**: 下記 §3.1 の **ディレクトリ束ね**（推奨）と **単一 JSON 束ね**（代替）を比較。**最小 IR 1 本の置き場（案）**: 既存 e2e 系と並べるなら `samples/e2e_test/` 配下の IR + [samples/e2e_test/face_map.json](../../samples/e2e_test/face_map.json) を起点に、束ね先パスだけ差し替えたドラフトを想定（ファイル作成は任意）。 |

---

## 3. ymmp 幾何調査（G-20 の前提タスク・必須メモ）

**詳細 readback・G-20 Tier A/B スコープ**: 専用メモ [TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md)（本節の正本の一次記述）。

**要旨（§3 三問への短答）**

- **体の反転**: readback 上は **`TachieItem.IsInverted`**（`TachieFaceParameter` 内には反転キーなし）。発話ブロック側には **`VoiceItem.IsInverted`** も別立てで存在するため、**両者の同期が必要か**は GUI で 1 回確認。  
- **顔と体の同量移動**: **GroupItem 化**（運用）または **`TachieItem` と `VoiceItem` の X/Y に同一デルタ**（patch 設計）が候補。  
- **patch アンカー**: 表情パスは **`VoiceItem.TachieFaceParameter`**、待機は **`TachieFaceItem`**、レイアウト・反転は **`TachieItem`**（＋要件次第で **`VoiceItem`** 幾何）。既存 `slot` は **TachieItem** 系。

**YMM4 GUI または ymmp readback**で、少なくとも次をメモする（[YMM4-bg-animation-operator-research-2026-04.md](YMM4-bg-animation-operator-research-2026-04.md) と同型でよい）。

- 体の反転: 触るキーは `TachieItem` 側か `TachieFaceParameter` 側か。  
- 顔と体を同量だけ動かす: **グループ化**か **個別 X/Y の差分同期**か。  
- `VoiceItem` / `TachieFaceItem` / `TachieItem` のどれを patch のアンカーにするか。

調査の書き方の例: [YMM4-bg-animation-operator-research-2026-04.md](YMM4-bg-animation-operator-research-2026-04.md)。  
調査結果を **§3 末尾に追記**するか、リンク先の専用メモに書き、本ファイルからリンクする。

### 3.1 G-19 用 `face_map` 束ね（サンプルパス案）

FEATURE_REGISTRY（G-19）の「**複数 face_map ファイル＋CLI/registry**」と「**単一構造内の body_variant**」の二者に対応するパス案。

| 案 | パス案 | 長所 | 短所 |
|----|--------|------|------|
| **A: ディレクトリ + マニフェスト（推奨）** | 体ごと: `samples/face_map_bundles/<character_name>/<body_id>.json`（各ファイルは現行 [samples/face_map.json](../../samples/face_map.json) と同型: キャラ名トップ → 表情ラベル → パーツキー）。束ね索引: `samples/face_map_bundle_registry.example.json`（`character_name` / `default_body_id` / `bodies: { body_id: "相対パス" }`）。 | `validate-ir` や diff が **ファイル単位**でしやすい。オペレータが体単位で差し替え可能。 | CLI フラグ（例: `--face-map-bundle`）追加が必要（承認後）。 |
| **B: 単一 JSON** | `samples/face_map.multi_body.example.json` — トップを `{ "bodies": { "body_id": { "face_label": { "Eyebrow": ... } } } }` 等とする。 | 1 ファイルで完結。 | 巨大化しやすく、git diff が煩雑。`_resolve_face_parts` の階層変更が集中する。 |

**推奨コメント**: テンプレ `extract-template --labeled` との連携では、**体バリアントを別ファイルに分けた案 A** の方がラベル運用と整合しやすい。最終判断はフェーズ B のラベル安定確認後。

### 3.2 体テンプレ構想（2026-04-13 追記）

**運用イメージ**: 立ち絵素材自体は変更せず、タイムライン上でゆっくり頭（TachieItem）と別の体画像（ImageItem）を重ねて配置する。位置合わせは手動で 1 回行いテンプレとして保存。テンプレを蓄積し、台本→IR で「今回は配達員テンプレを使う」のように指定する。

**既存パターンとの類似**: `bg` + `bg_map`（ラベル → ファイルパス）や `overlay` + `overlay_map`（ラベル → ImageItem 挿入）と同型。体画像もタイムラインに挿入する ImageItem であり、レジストリ解決 + 座標付きで処理できる。

**必要な新規要素（将来 FEATURE）**:

| 要素 | 内容 | 既存で流用可能なもの |
|------|------|---|
| IR 語彙 | `body_template` のような carry-forward フィールド | `bg` / `overlay` と同型 |
| レジストリ | `body_map`（ラベル → ファイルパス + x/y/zoom） | `bg_map` / `overlay_map` の JSON 形式 |
| patch 拡張 | ImageItem 挿入 + 座標適用 | `overlay` の ImageItem 挿入ロジック + `slot` の座標適用ロジック |

**YMM4 側の運用**: グループ制御で頭と体をまとめて移動・拡大縮小する。詳細は [TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md) §7。

**FEATURE_REGISTRY への起票は別ブロック**。proposed として G-21 等で登録する際に、上記の設計をスコープ文に使う。

### 3.3 ユーザー承認依頼サマリ（3〜5 行）

1. **G-19 を `approved` にすると**: 複数体素材向けの **`face_map` 束ね**（上表のマニフェスト＋体別 JSON または単一 JSON 案）と、IR または CLI による **`body_id` 選択**を実装し、`validate-ir` / `apply-production` と矛盾しない縦スライスに着手できる。  
2. **G-20 を `approved` にすると**: 専用メモの Tier B に列挙した **ymmp キー**（例: `TachieItem` / 必要なら `VoiceItem` の **`IsInverted`**・**X/Y** 同期）を IR から決定的に patch する範囲に着手できる（**§3 未確認の GUI 確認を完了してから**契約文を確定すること）。  
3. **承認なしで継続可能**: 本パック・専用メモへの追記、readback、サンプルパス案のドラフト（本 §3.1）。**`src/` 変更・IR 語彙の本番追加は不可**。

---

## 4. 台帳との対応

| ID | 内容 |
|----|------|
| **G-19** | 複数体素材に対応した **face_map（束ね）＋ IR からの体バリアント選択**（語彙 / CLI / `validate-ir` 拡張を含みうる） |
| **G-20** | 顔・体の **幾何（反転・平行移動・相対オフセット）** を IR から決定的に patch（§3 調査完了後にスコープ確定） |

**承認なしでよいこと**: §3 の調査メモ追記、サンプル ymmp の readback、ドキュメントのみの整理。  
**承認が必要なこと**: `src/` の新規挙動・IR 語彙の追加・`validate-ir` 契約変更。

---

## 5. 別スレッド開始用 Prompt（全文コピペ）

以下を **そのまま** 新しいエージェントチャットに貼る。リポジトリは **NLMYTGen のみ**（他プロジェクト参照禁止）。

```
あなたは NLMYTGen リポジトリの作業エージェントです。

## ゴール
立ち絵について、(1) 複数の体素材にゆっくり顔パーツを差し替える、(2) 反転や平行移動で体と顔の視覚整合を取る、(3) 可能なら既存の motion 経路でより複雑な動きまで検討する。

## 正本（必ず読む）
- docs/verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md（本パック全文）
- docs/FEATURE_REGISTRY.md の G-19 / G-20（現状 proposed）
- docs/AUTOMATION_BOUNDARY.md
- docs/PRODUCTION_IR_CAPABILITY_MATRIX.md

## 制約
- FEATURE_REGISTRY に無い機能は実装しない。コードを変える場合は G-19 または G-20 が approved になってから。
- まずはフェーズ A〜C と本パック §3 の ymmp 幾何調査を優先。調査結果は TACHIE-BODY-FACE-SWAP-PREP の §3 に追記するか、docs/verification 配下に短い調査メモを新設し本パックからリンクする。
- Python で画像合成・レンダリングはしない（プロジェクト方針）。

## 最初の成果物
1. §3 調査メモ（触る ymmp キー案と、G-20 のスコープ案）
2. G-19 用の「face_map 束ね」案（サンプル JSON のパス案でよい）
3. ユーザー承認依頼用の 3〜5 行サマリ（何を approved にすれば実装に入れるか）

終了時は変更ファイルパスと、次スレッドへの一行 next_action を書く。
```

---

## 6. 変更履歴

- 2026-04-13: 初版。別スレッド起動用パック、FEATURE_REGISTRY G-19/G-20（proposed）と連携。
- 2026-04-13: §2.1（フェーズ A〜C 記入）、§3 要旨・§3.1（face_map 束ねパス案）・§3.2（承認サマリ）を追加。[TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md) へ幾何 readback を分離。
- 2026-04-12: §2.1 フェーズ **B** 行を更新（`haitatsuin_2026-04-12.ymmp` のパス寄せ、`extract-template` / `--labeled` 結果パス、幾何メモ §6 へのリンク）。§B 先頭チェックに Remark 前提の注記。
