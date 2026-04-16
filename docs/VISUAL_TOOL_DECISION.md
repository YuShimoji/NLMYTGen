# 視覚効果ツール決定記録

> **読み物**: [VISUAL_EFFECT_SELECTION_GUIDE.md](VISUAL_EFFECT_SELECTION_GUIDE.md)(選択肢・推奨の正本)
> **姉妹**: [MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md)(素材調達ルール)
> **目的**: Step 1「ツール決定」の結果を 1 ファイルに固定する。判断の根拠と日付をここに残す。

## 記入方法

1. 推奨デフォルト(**太字**)をそのまま採用する場合も、明示的に記入する
2. 日付は `YYYY-MM-DD` で 1 行
3. 必要なら「備考」欄に判断理由(コスト・既存素材・学習コスト等)を書く

---

## 決定記録

**決定日**: `2026-04-16`

### Q1. 茶番劇アニメのルート

- [ ] A: YMM4 完結 (立ち絵+テキスト+フキダシ素材のみで組む)
- [✓] **B: 外部素材 + ゆっくり頭 (推奨)** — いらすとや人物等に TachieItem を重畳、G-21 方針と一致
- [ ] C: 完全外製 (AviUtl / AE で動画素材作成)

**決定**: B
**備考**: いらすとや / AI 生成 (白背景) で配達員・消防員等の人物素材を用意し、ゆっくり頭を重畳。G-21 方針と一致。

### Q2. 情報列挙 (黒板・カード) のルート

- [✓] **A: YMM4 テキスト+図形 (推奨)** — テンプレ化すれば 3 本目以降の摩擦小
- [ ] B: 外部エディタ (PowerPoint 等) → PNG 書出し → `overlay_map`
- [ ] C: 図解アニメ (AE)

**決定**: A
**備考**: YMM4 完結。補助素材が必要な場合は AI 生成 (白背景) で追加可能。

### Q3. 地図・関係図のルート

- [ ] A: YMM4 図形組み合わせ (手間大)
- [✓] **B: 外部エディタ (Figma / Inkscape 等) で作図 → PNG (推奨)** — 複雑な作図は YMM4 上では非効率
- [ ] C: 動画作図 (AE) ・GIS ツール

**決定**: B
**備考**: Figma / Inkscape 等のローカル/Web 作図ツール + AI 生成 (白背景) を活用。Canva は使わない。

### Q4. ムードのルート

- [✓] **A: YMM4 内エフェクト (推奨)** — Pixabay 等でDLした画像/動画に `effect_catalog` 適用
- [ ] B: Pixabay/Pexels 動画を YMM4 配置
- [ ] C: 自作撮影・生成 AI

**決定**: A
**備考**: Pixabay / Pexels の画像・動画 + AI 生成素材に YMM4 内エフェクトを適用。

### Q5. サムネイルのルート

- [✓] **A: YMM4 内 (1 フレーム書き出し)** — 本編と統一感。将来は NLMYTGen 側で素材置き換え自動化を実装予定
- [ ] B: Photoshop / GIMP
- [ ] C: AI 生成 (Midjourney / Gemini)
- ~~Canva~~ — 選択肢から除外（依存を作らない方針）

**決定**: A
**備考**: 当初からの方針。サムネは YMM4 内で作成し、将来的に NLMYTGen 側で「素材置き換え自動化」機能を別途実装する前提。Canva への依存は作らない。

### Q6. コミュニティプラグインを使うか

- [✓] Yes — 自 PC 完結案件のみ。Wave / Tiling / VignetteBlur / Bloom など使用可
- [ ] No — 配布・共有安全優先。本体 71 件のみ

**決定**: Yes
**備考**: 案件ごとに切り替えてもよい

### Q7. 素材サイト (複数選択可)

- [✓] いらすとや — 人物・職業・動作・感情・日常シーン (茶番劇 Q1=B の主素材)
- [✓] Pixabay — 風景・建物・自然 (ムード Q4=A の背景)
- [✓] Pexels — 同上 (動画素材豊富)
- [ ] 写真 AC — 日本風景・食品
- [ ] ICOOON MONO — シンプルアイコン
- [ ] 自作 — 撮影・スキャン
- [✓] その他: **AI 生成 (白背景書き出し)** — 茶番劇用立ち絵・小物・背景の補助。イメージイラストの範囲内で利用

**決定**: いらすとや + Pixabay + Pexels + AI 生成 (白背景)
**備考**: 差し当たりこの 3 サイト + AI 生成でカバー。AI 生成は白背景書き出しで立ち絵・小物・背景を補完。イメージイラストの範囲内で運用。

---

## 決定後のチェックリスト

決定が埋まったら、以下に進む:

- [ ] 本ファイルの「決定日」を記入
- [ ] [MATERIAL_SOURCING_RULES.md](MATERIAL_SOURCING_RULES.md) を記入 (Step 2)
- [ ] YMM4 テンプレ初期セット 5 種を作成 (Step 3)
- [ ] `bg_map.json` / `overlay_map.json` にラベル登録 (Step 4)
- [ ] 1 本の実案件で proof → [verification/P02-production-adoption-proof.md](verification/P02-production-adoption-proof.md) に追記 (Step 5)
- [ ] [runtime-state.md](runtime-state.md) の優先表で「視覚効果ツール選定」を hold → done に昇格

---

## 変更履歴

- 2026-04-16: 初版。ユーザー記入用テンプレ
