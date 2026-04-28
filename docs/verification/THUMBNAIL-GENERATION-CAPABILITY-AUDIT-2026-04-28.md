# Thumbnail Generation Capability Audit — 2026-04-28

目的: サムネイル生成周りについて、現時点で repo が実際に持っている機能、未実装領域、未完成の理由を棚卸しする。

## 結論

- 現在できることは **サムネイル生成そのものではなく、サムネ制作の判断支援・手順化・手動採点の機械記録**。
- 実サムネは **YMM4 のテンプレートを人間が複製し、文字・立ち絵・背景を差し替えて静止画書き出し**する運用。
- 2026-04-28 までの仕様は、コピー戦略 / one-sheet / score に分かれており、**AI 生成時に台本手直し・本編 Production IR・サムネ設計をどう分離するか**は明示が薄かった。
- 現行整理では、サムネ設計は台本本文でも本編 Production IR でもなく、H-01 から分岐する sibling artifact `thumbnail_design` として扱う。同じ AI 生成タイミングで出してよいが、保存・適用先は分ける。
- Python / repo 側の自動画像生成・画像合成は明示的に禁止 / rejected。
- repo にはサムネ PNG サンプルはあるが、確認した 15 件はすべて同一 SHA256 で、制作パターンの多様性や自動生成能力の証跡ではない。
- サムネ用の実 `.ymmp` テンプレート / template source は repo に存在しない。2026-04-28 追補で、既存 template copy に `thumb.text.*` / `thumb.image.*` Remark がある場合の read-only 監査と限定 patch CLI は追加済み。

## 現時点で可能なこと

### H-01 Packaging Brief

- `emit-packaging-brief-template` で Packaging Brief の Markdown / JSON テンプレートを出力できる。
- GUI の品質診断タブから H-01 テンプレ保存ができる。
- brief は title / thumbnail / script の promise、required evidence、forbidden overclaim、thumbnail controls を中央管理する。
- ただし H-01 の機械化範囲はテンプレ生成と GUI 保存まで。`build-csv` / `apply-production` への自動注入やスコア結果のクローズドループ反映は未承認。

### C-08 / H-02 Thumbnail Strategy

- `docs/S8-thumbnail-copy-prompt.md` と `docs/THUMBNAIL_STRATEGY_SPEC.md` により、サムネコピー案を specificity-first で生成する運用がある。
- 出力できる想定は main copy 5 案、sub copy 3 案、表情提案、背景方向性、rotation recommendation、Specificity Ledger、Brief Compliance Check。
- H-02 は done だが、これは **コピー戦略 / visual direction の仕様準拠 proof** であり、画像生成ではない。
- 2026-04-28 整理で、H-02 出力は `thumbnail_design` / one-sheet として台本本文・Production IR から分離することを明示した。

### H-03 / H-04 Quality Diagnostics

- `score-visual-density` は H-01 brief と手動カテゴリスコアから、動画内でサムネ / タイトル promise が視覚的に回収されるかを診断する。
- `score-evidence` は H-01 brief と手動カテゴリスコアから、title / thumbnail promise の本文根拠の強さを診断する。
- どちらも GUI 品質診断タブから実行可能。
- 画像解析や最終デザイン判断は行わない。

### H-05 / Lane E Probe

- `score-thumbnail-s8` は `single_claim` / `specificity` / `title_alignment` / `mobile_readability` の手動採点 `0..3` を集約する。
- `total_score >= 80` かつ warning なしで pass、そうでなければ needs_fix / high_risk。
- GUI ボタンはなく CLI のみ。
- 画像生成・画像解析・OCR・スマホ縮小シミュレーションはしない。

### YMM4 One-Sheet Workflow

- `docs/THUMBNAIL_ONE_SHEET_WORKFLOW.md` が、テンプレ複製 → 文字 / 立ち絵 / 背景差し替え → PNG 書き出し → 品質チェック、という手順を固定している。
- `docs/verification/P03-thumbnail-one-sheet-proof.md` に run_id 単位の運用記録がある。
- 実ファイル生成主体と最終採否は user / YMM4。

### Thumbnail Template Slot CLI（2026-04-28 追補）

- `audit-thumbnail-template` は YMM4 `.ymmp` 内の `thumb.text.*` / `thumb.image.*` Remark slot を列挙し、Text / FilePath / Color / X/Y/Zoom/Rotation が patchable かを返す。
- `patch-thumbnail-template` は patch JSON から既存 slot の text、ImageItem `FilePath`、既存 Color route、X/Y/Zoom/Rotation 先頭値だけを更新し、別 `.ymmp` に書き出せる。
- 実サムネ template `.ymmp` はまだ repo に無いため、現時点の proof は unit/CLI fixture に留まる。YMM4 上の visual acceptance と PNG 書き出しは未完了。

## 確認したローカル証跡

- `uv run python -m src.cli.main emit-packaging-brief-template --format json` は JSON テンプレートを出力できた。
- `score-thumbnail-s8` は手動スコア all `2` で `total_score=67` / `needs_fix`、all `3` で `total_score=100` / `pass` を返した。
- `samples/*thumb*.png` 15 件はすべて `1920x1080` RGBA PNG。
- 15 件の SHA256 はすべて `bef38190d45d368a66bb5015e1ed057a9bff219335b05b8fc6a9485fcf96ebb4` で同一。
- `*thumb*.ymmp` / `*thumbnail*.ymmp` / `*サムネ*.ymmp` は見つからなかった。

## できない / 未実装

- Python によるサムネイル画像生成。
- Python による画像合成 / レイアウト描画 / PIL 等でのサムネ作成。
- 実サムネ YMM4 テンプレートに対する文字 / 画像スロット差し替え実証。
- サムネ用 template source の repo 管理。
- 画像からの自動採点、OCR、可読性解析、CTR 最適化。
- GUI からの H-05 実行。
- サムネ制作物の多様な実例コーパス。

## 未完成になっている事情

1. **境界条件が強い**: `README.md` / `AUTOMATION_BOUNDARY.md` / `INVARIANTS.md` / `FEATURE_REGISTRY.md` で、Python 画像生成・合成は非目的 / rejected とされている。
2. **成果物 owner が人間 / YMM4**: サムネイル最終判断は creative judgement であり、スコア CLI は代替しない。
3. **これまでの主投資が別軸**: CSV 変換、台本品質、YMM4 Adapter、face/bg/slot/overlay/se/skit_group など、本編制作の重い S-3〜S-6 に開発が集中していた。
4. **H 系は補助機能として閉じた**: H-01〜H-05 は packaging / scoring / prompt / one-sheet までで、「生成」には踏み込まないよう意図的に止められている。
5. **テンプレ資産が repo にない**: 将来想定の「素材置き換え自動化」には、YMM4 側のサムネテンプレート、差し替え対象の命名規約、text/image slot registry が必要だが、まだ存在しない。
6. **P03 の pass は品質完成ではない**: 多くの run は接続維持や記録継続を示すもので、実サムネ品質の改善 proof ではない。

## 次に開くなら安全な開発面

破壊的変更や依存追加なしで進めるなら、画像生成ではなく **YMM4 テンプレート差し替え自動化の前段**が最短。

詳細な変奏軸・IR 接続・スライス案は [THUMBNAIL-VARIATION-AND-IR-PLAN-2026-04-28.md](THUMBNAIL-VARIATION-AND-IR-PLAN-2026-04-28.md) を参照。

1. user が YMM4 で作ったサムネ `.ymmp` テンプレート copy を repo-local sample として受け取る。
2. `thumb.text.*` / `thumb.image.*` Remark を付け、`audit-thumbnail-template` で TextItem / ImageItem / Remark / Layer / FilePath の存在を確認する。
3. `patch-thumbnail-template` で文字列・素材パス・X/Y/Zoom の限定 patch を 1 件通し、YMM4 で開けるか確認する。
4. 実 template の readback 結果に合わせて TextItem color route / ShapeItem / panel を拡張する。
5. H-05 の GUI ボタン化は有用だが、現台帳では「CLI のみ」と明記されているため、実装前に FEATURE_REGISTRY のスコープ更新が必要。

この方向なら「画像を生成する」のではなく、「YMM4 テンプレート内の既存スロットを安全に差し替える」ため、現行境界と比較的整合しやすい。
