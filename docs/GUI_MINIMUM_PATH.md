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
| Max lines / Chars per line | 2 行字幕にするとき |
| 自然改行（balance-lines） | 改行品質を使うとき（**Max lines 指定時のみ有効**） |
| Reflow v2 | v2 リフロー経路を使うとき（balance-lines と併用可） |

**話者統計・はみ出し候補**: Dry Run / Build CSV 後に結果パネル（F-04、`stats` JSON）。

### 演出適用タブ — S-6b（演出適用工程）

| ファイル | 必須 / 任意 | なぜ必要か |
|-----------|-------------|-----------|
| Production `.ymmp` | **必須** | 台本読込済みのベースプロジェクト。これに対して演出を適用する |
| IR JSON | **必須** | LLM が生成した演出指示。貼り付け→保存でも可 |
| Palette `.ymmp` | **IR に face が含まれるとき必須** | 表情ラベル（serious, smile 等）を YMM4 のパーツに変換するための辞書 |
| CSV（row-range 用） | **row-range を使うとき必須** | CSV 変換タブで生成した CSV。発話と IR の対応付けに使う |
| BG Map JSON | **IR に bg があるとき推奨** | 背景ラベル（studio_blue 等）を YMM4 の画像パスに変換する辞書 |
| Face Map Bundle JSON | **複数キャラ運用時のみ** | キャラクターごとに異なる表情辞書を束ねるファイル |

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
