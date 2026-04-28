# GUI 操作ガイド（NLMYTGen Electron）

NLMYTGen GUI（`start-gui.bat` / `gui/`）で「何を用意すればよいか」「どこまでが自動で、どこからが YMM4 か」を一本にまとめる。**演出 IR の語彙・patch 契約の詳細は本書で複製しない**。[PRODUCTION_IR_SPEC.md](PRODUCTION_IR_SPEC.md)・[PIPELINE_SPEC.md](PIPELINE_SPEC.md)・[AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md)を正とする。

---

## 基本方針

- 制作は GUI のみ。CLI が要る状態は GUI 不足として台帳・実装で潰す（`docs/INVARIANTS.md`）。
- YMM4 は (1) テンプレ登録 (2) 全素材後の配置・書出 のみ。増分で繰り返し開かない。
- 品質ゲートは INVARIANTS のとおり（速度優先で柔軟）。

---

## この GUI が自動化するもの / しないもの

| する | しない |
|------|--------|
| 台本 → YMM4 用 CSV（`build-csv`） | 音声合成・レンダリング（YMM4 内蔵） |
| IR 検証・`apply-production` 経由の ymmp 部分更新 | .ymmp のゼロ生成・完全自動配置 |
| パッケット用テキスト出力・H-01 テンプレ保存・H-03/H-04 スコア集計 | サムネ画像生成、YouTube 投稿 |

詳細は [AUTOMATION_BOUNDARY.md](AUTOMATION_BOUNDARY.md)。

---

## 制作ウィザードの範囲

ウィザード 5 ステップは **S-3（CSV 変換）と S-6b（IR 適用）** に対応する。

| 工程 | ウィザードとの関係 |
|------|-------------------|
| S-4（台本読込）・S-5（読み上げ確認・字幕修正） | **YMM4 上で手動**。本 GUI の外。 |
| S-6c（手動微調整）以降の見た目微調整 | **YMM4 上で手動**。 |
| S-7（通し確認・レンダリング）・S-8（サムネイル制作）・S-9（YouTube投稿） | **本 GUI の範囲外**。 |

---

## 最低限必要なファイル

### CSV 変換タブ — S-3（CSV変換工程）

| 入力 | 必須 |
|------|------|
| 台本 `.txt` | はい |
| Speaker Map | 台本の話者名と YMM4 表示名を合わせるとき |
| Max lines / Chars per line | 2 行字幕にするとき。標準は `2` / `40` |
| YMM4 Subtitle Font Source | 字幕仕様の `.ymmp` があるとき。字幕 `FontSize` から倍率を自動推定 |
| Subtitle Font Scale (%) | `.ymmp` 未選択時の手動指定。標準は `100`、大きいほど早めに改行 |
| Wrap Width (px) / Measure Backend | YMM4 の折り返し幅を固定しているとき。WPF helper がある場合は実測幅で改行 |
| 自然改行（balance-lines） | 改行品質を使うとき（**Max lines 指定時のみ有効**） |
| Reflow v2 | v2 リフロー経路を使うとき（balance-lines と併用可） |

**話者統計・はみ出し候補**: Dry Run / Build CSV 後に結果パネル（F-04、`stats` JSON）。

**字幕改行の運用**: NLMYTGen 側で明示改行する場合は、YMM4 側の自動折り返しを OFF か十分広くする。両方を有効にすると二重折り返しでズレる。

### 演出適用タブ — S-6b（演出適用工程）

| ファイル | 必須 / 任意 | なぜ必要か |
|-----------|-------------|-----------|
| Production `.ymmp` | **必須** | 台本読込済みのベースプロジェクト。これに対して演出を適用する |
| IR JSON | **必須** | LLM が生成した演出指示。貼り付け→保存でも可 |
| Palette `.ymmp` | **IR に face が含まれるとき必須** | 表情ラベル（serious, smile 等）を YMM4 のパーツに変換するための辞書 |
| CSV（row-range 用） | **row-range を使うとき必須** | CSV 変換タブで生成した CSV。発話と IR の対応付けに使う |
| BG Map JSON | **IR に bg があるとき推奨** | 背景ラベル（studio_blue 等）を YMM4 の画像パスに変換する辞書 |
| Face Map Bundle JSON | **複数キャラ運用時のみ** | キャラクターごとに異なる表情辞書を束ねるファイル |
| Skit Group Registry JSON | **G-24 skit_group を使うとき必須** | 外部茶番劇演者の intent / fallback / template 名を解決する辞書 |
| Skit Group Template Source `.ymmp` | **G-24 skit_group を配置するとき必須** | YMM4 で作った GroupItem テンプレート集。template-analyzed placement の入力 |

**G-24 の標準手順**: `skit_group intent を registry に限定` を ON にして Validate IR → Dry Run → Apply Production。`skit_group 配置だけを適用` は face/bg 等を切り離す切り分け用で、ON のとき CSV(row-range) はコマンドへ渡さない。

**現 GUI の露出範囲**: 制作導線として画面に出しているのは production `.ymmp` / IR / palette / CSV / BG map / face map bundle / G-24 skit_group registry・template source。`slot_map` / `overlay_map` / `se_map` / `motion_map` / `tachie_motion_map` / `transition_map` / `bg_anim_map` / `group_motion_map` / `timeline_profile` は adapter 側の能力として存在するが、現 GUI の入力欄にはまだ出していない。これらが制作上必須になった場合は、CLI 運用を標準化せず GUI 補完課題として扱う。

### 品質診断タブ

| 内容 | 必須 |
|------|------|
| H-01 Packaging Brief + H-04 / H-03 手採点 | **任意**。パッケージ整合の記録用 |
| B-18（台本診断） | 任意 |
| H-05（サムネ採点） | 任意。[dev/CLI_REFERENCE.md](dev/CLI_REFERENCE.md) の `score-thumbnail-s8`。ウィザード非必須 |

---

## 変更レイヤー → 推奨検証

| レイヤー | 変更例 | 推奨検証 | YMM4 を開くか |
|----------|--------|----------|---------------|
| **L2（Python変換工程）** | CSV 変換・字幕リフロー | コード変更時のみユニットテスト | **開かない** |
| **L3（YMM4内部工程）** | patch-ymmp / timeline adapter | GUI の Dry Run | **契約変更時のみ** |
| **creative（創作判断）** | 表情の見え方・テンポ | 人判断 | 完成物を見るとき |

G-24 skit_group は L3 の機械配置と creative composition acceptance を分ける。`SKIT_TEMPLATE_SOURCE_MISSING` / `SKIT_TEMPLATE_ANALYSIS_INSUFFICIENT` は GUI 上の failure class として先に止め、YMM4 での手置き修正へ押し戻さない。

---

## 既知の落とし穴

- **balance-lines**: Max lines 指定と併用が必要。GUI では Max lines 未設定時はチェックを付けても送信しない（エラー回避）
- **Reflow v2 と balance-lines**: 両方オン + Max lines で意図通りの改行品質になる

---

## 関連リンク

- [dev/CLI_REFERENCE.md](dev/CLI_REFERENCE.md) — 開発用 CLI 索引
- [OPERATOR_WORKFLOW.md](OPERATOR_WORKFLOW.md) — 痛点・検証の境界
- [gui-llm-setup-guide.md](gui-llm-setup-guide.md) — Custom GPT 同期
- [NAV.md](NAV.md) — ドキュメント地図
- [WORKFLOW.md](WORKFLOW.md) — S-0〜S-9 全体
