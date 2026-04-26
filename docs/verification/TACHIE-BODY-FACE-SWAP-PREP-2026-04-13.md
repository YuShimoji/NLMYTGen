# 立ち絵 — 複数体素材 × ゆっくり顔差し替え（履歴・調査パック）

**ステータス**: **G-19 done / G-20 approved**（2026-04-13〜15 で実装・承認が進行）。台帳は [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) を参照。  
**目的**: G-19 / G-20 当時の調査・実装境界を残す。現行 G-24 `delivery_nod_v1` の入口ではなく、通常再開では読まない。

---

## 混同注意（2026-04-15 追記）

本書は **2 つの異なる機能**が混在している。読む際に区別すること。

| 節 | 対応 FEATURE | 方式 | 適用対象 |
|----|-------------|------|---------|
| §3.1 G-19 用 `face_map` 束ね | **G-19 `done`** | **ゆっくり系 TachieItem 内部**の body パーツを束ねる（body_variant） | ゆっくり魔理沙・霊夢等、ゆっくり系素材の体を入れ替える |
| §3 ymmp 幾何調査 | **G-20 `approved`** | 既存 GroupItem の X/Y/Zoom 操作 + 反転 | ゆっくり系でも外部素材+頭でも共通 |
| **§3.2 体テンプレ構想** | **G-21 `hold`**（旧案。現行主軸ではない） | **外部人物素材 ImageItem + ゆっくり頭 TachieItem の重畳** | **配達員・消防員等の外部素材にゆっくり頭を重ねる茶番劇運用** |

**典型的な混乱**: 「複数体素材 × ゆっくり顔」という表現は G-19 と G-21 の両方に当てはまるが、**技術実装は別物**。G-19 はゆっくり立ち絵の内部パーツ差し替え、G-21 はタイムラインでの複数アイテム重畳。

---

## 1. ユーザー要求 → 作業への対応表

| 要求 | 第一の置き場 | 機械化する場合の候補 |
|------|----------------|----------------------|
| 複数体にゆっくり顔を載せる | YMM4 テンプレ + **face_map**（パーツパス） | **G-19**: 体バリアントごとの map 束ね、IR からの選択 |
| 反転・平行移動で崩れない | テンプレ既定 or ymmp の幾何プロパティ調査 | **G-20**: IR + `validate-ir` + patch（**ymmp キー調査が先**） |
| より複雑な動き | 既存 **G-17**（`motion_map` / `tachie_motion_effects_map` / timeline profile） | まず G-17 範囲で足りるか検証。足りなければ **別途 `proposed` 起票** |

## 2. パス移植性（共有可能な `face_map` 束へ）

フェーズ B および G-19 束ね案では、**`D:\...` 等のローカル絶対パスに依存した ymmp / `face_map` は共有・CI・別マシンでは再現できない**ため、リポ内の相対パスへ正規化するか、素材をリポ同階層にコピーしたうえで YMM4 から保存し直し、束ね JSON も同じ根から参照するまで持ち込まない。

---

## 3. ymmp 幾何調査（G-20 の履歴メモ）

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

この構想は G-21 として `hold` 済み。現行の茶番劇演者主軸は G-24 `skit_group` template-first であり、本節から新規実装へ戻らない。

---

## 4. 台帳との対応

| ID | 内容 |
|----|------|
| **G-19** | 複数体素材に対応した **face_map（束ね）＋ IR からの体バリアント選択**（語彙 / CLI / `validate-ir` 拡張を含みうる） |
| **G-20** | 顔・体の **幾何（反転・平行移動・相対オフセット）** を IR から決定的に patch（§3 調査完了後にスコープ確定） |

**承認なしでよいこと**: §3 の調査メモ追記、サンプル ymmp の readback、ドキュメントのみの整理。  
**承認が必要なこと**: `src/` の新規挙動・IR 語彙の追加・`validate-ir` 契約変更。

---

## 5. 変更履歴

- 2026-04-13: 初版。G-19/G-20 の準備・調査パックとして作成。
- 2026-04-13: §2.1（フェーズ A〜C 記入）、§3 要旨・§3.1（face_map 束ねパス案）・§3.2（承認サマリ）を追加。[TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md) へ幾何 readback を分離。
- 2026-04-12: §2.1 フェーズ **B** 行を更新（`haitatsuin_2026-04-12.ymmp` のパス寄せ、`extract-template` / `--labeled` 結果パス、幾何メモ §6 へのリンク）。§B 先頭チェックに Remark 前提の注記。
- 2026-04-13: `haitatsuin` 進行可否プラン反映 — 幾何メモ冒頭に **二次 readback** 行。§2.1 フェーズ B に `--labeled` CLI 再実行ログ。§2.2 **パス移植性**（絶対パス禁止の一文方針）。
