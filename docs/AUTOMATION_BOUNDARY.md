# AUTOMATION BOUNDARY — 自動化の境界

NLMYTGen の自動化がどこで動作するかを明確にする。
「YMM4 の中で何をするか」と「YMM4 の外で何をするか」を混同しないためのドキュメント。

---

## 全体像

```
┌──────────────────────────────────────────────────────────────────┐
│                    動画制作ワークフロー                            │
│                                                                  │
│  [L1 入力取得]     [L2 変換]        [L3 YMM4内部]    [L4 配信]   │
│                                                                  │
│  NotebookLM   →  NLMYTGen CLI  →  YMM4           →  YouTube    │
│  RSS/ソース       Python           テンプレート       投稿API     │
│                   GUI (将来)        プロジェクト                   │
│                                     音声合成                      │
│                                     レンダリング                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## レイヤー定義

### L1: 入力取得（NLMYTGen の外）

NotebookLM やその他のソースから素材を取得する段階。

| 何をするか | 誰がやるか | 自動化の余地 |
|-----------|-----------|------------|
| NotebookLM にソース投入 | 人間（手動） | RSS 連携でソース収集を半自動化 |
| Audio Overview 生成 | NotebookLM | API 未公開のため手動 |
| 元台本テキスト取得 | 人間（コピペ） | API 公開時に自動化 |
| 音声書き起こし（fallback） | Whisper / Google Docs | CLI で自動化可能 |
| 背景動画・素材の取得 | 人間 or スクリプト | 素材サイト API で自動化可能 |

**NLMYTGen がやること:** 取得されたテキストファイルを受け取る。RSS フィードからのトピック候補取得 (A-04 `fetch-topics`) は実装済み。
**現状:** A-04 (RSS フィード連携) は done。D-02 (背景動画取得) は `quarantined` のまま、価値経路・権利・受け取り境界の個別再審査が済むまで通常候補として扱わない。

---

### L2: 変換（NLMYTGen の中 — Python）

テキストを YMM4 が読み込める形式に変換し、演出 IR を定義して S-6 を支援する段階。

| 何をするか | 誰がやるか | 現状 |
|-----------|-----------|------|
| テキスト → YMM4 CSV | NLMYTGen CLI | done (build-csv) |
| 話者マッピング | NLMYTGen CLI | done (--speaker-map) |
| 長文分割 | NLMYTGen CLI | done (--max-length, --display-width, --max-lines, --chars-per-line) |
| 入力検証 | NLMYTGen CLI | done (validate) |
| 演出 IR 語彙定義 | NLMYTGen docs | done (G-02, PRODUCTION_IR_SPEC.md v1.0) |
| IR 出力プロンプト | Custom GPT Instructions | done (G-05、proof 待ち) |
| YouTube メタデータ生成 | NLMYTGen CLI (将来) | hold。単体では value path が弱い |

**境界ルール:**
- Python は CSV / テキストメタデータ / 演出 IR 定義 (テキスト仕様) までが限界
- 演出 IR は意味ラベルのみ。ピクセル座標・ファイルパス・YMM4 固有形式は含まない
- **画像生成・画像合成・動画レンダリング・音声合成は Python ではやらない**
- 外部 TTS (Voicevox 等) は使用しない

**タイムライン演出の際限:** `motion` / `transition` / `bg_anim` など、IR 語彙としては定義されていても、Python アダプタがすべてを ymmp に自動反映しているわけではない。語彙・`validate-ir`・`patch_ymmp`・G-12 測定・YMM4 手動の対応関係は [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) を正本とする。

---

### L3: YMM4 内部（NLMYTGen の外）

YMM4 上での操作。音声合成・字幕配置・動画レンダリングはすべてここ。
動画制作工程の大部分を占める。各工程の詳細手順は WORKFLOW.md を参照。

| 何をするか | 誰がやるか | 省力化の方法 | WORKFLOW.md |
|-----------|-----------|------------|-------------|
| プロジェクトテンプレート構築 | 人間（初回のみ） | 一度作れば以降は複製して使う | S-0 |
| CSV 台本読込 | YMM4（手動操作） | -- | S-4 |
| 音声合成 | YMM4 内蔵 TTS | 台本読込時に自動実行 | S-4 |
| 字幕配置 | YMM4 | 台本読込で自動配置 | S-4 |
| 読み間違い修正 | 人間 | YMM4 辞書登録で定型化 | S-5a |
| 字幕はみ出し調整 | 人間 | テンプレートで初期設定を統一 | S-5b-c |
| 背景画像の配置・Animation | 人間 | -- | S-6a-b |
| 立ち絵の表情切り替え | 人間 | テンプレートで表情パターンを事前定義 | S-6c |
| BGM・SE 配置 | 人間 | テンプレートで基本 BGM を事前配置 | S-6d-e |
| 最終プレビュー確認 | 人間 | -- | S-7a |
| 動画レンダリング | YMM4 | YMM4 が実行 | S-7b-c |

**NLMYTGen がやること:** YMM4 が読み込めるファイル (CSV) を生成する。加えて、演出 IR (意味ラベルベースの構造化データ) を定義し、LLM (Custom GPT) が IR を出力するプロンプトを提供して S-6 を支援する。台本読込後の ymmp に対して、IR に基づく限定的な後段適用 (face/bg 差し替え) を行う (G-06 patch-ymmp)。次段では timeline edit packet として、slot の deterministic patch (G-11) までを assistant-owned mechanical scope に広げる。
**NLMYTGen がやらないこと:** .ymmp のゼロからの生成 (音声ファイル参照を含むため不可能)、素材の自動取得・ダウンロード、ピクセル座標の直接指定、YMM4 内部の万能制御。patch-ymmp は台本読込後の ymmp に対する限定変換器であり、ゼロからの生成とは区別する。

**省力化の原則:**
YMM4 のプロジェクトテンプレート（S-0 で構築）を毎回複製することで、キャラクター設定・字幕スタイル・立ち絵・BGM の初期設定を引き継ぐ。Python から YMM4 の GUI を操作する経路は存在しない。台本読込後の ymmp ファイルに対する後処理 (patch-ymmp) は、YMM4 内部の制御ではなく、出力ファイルの限定的な属性差し替えとして位置づける。

---

### L4: 出力・配信（NLMYTGen の外）

動画完成後の公開・配信。

| 何をするか | 誰がやるか | 自動化の余地 |
|-----------|-----------|------------|
| YouTube 投稿 | 人間（手動） | YouTube Data API v3 で自動化 |
| タイトル・説明・タグ設定 | 人間 | E-02 単体では手入力が残るため、E-01 か別 integration point とセットでのみ価値が出る |
| サムネイル制作 | 人間 | YMM4 テンプレートの文字・画像入れ替え。WORKFLOW.md S-8 |

---

## 絶対に越えない境界

| 禁止事項 | 理由 | 根拠 |
|---------|------|------|
| Python で画像を生成・合成する | 視覚的成果物の生成は Python の責務外 | ユーザー指示 (2026-03-30) |
| Python で動画をレンダリングする | YMM4 の責務 | ADR-0003 |
| Python で音声を合成する | YMM4 内蔵 TTS を使う | ADR-0003 |
| Voicevox / 外部 TTS を使う | 外部依存を増やさない | ユーザー指示 |
| Python で字幕を配置する | YMM4 の責務 | ADR-0003 |
| Python で .ymmp をゼロから生成する | 音声ファイル参照を含むため外部生成不可能 | ユーザー指示 (2026-03-30)。台本読込後の限定的な後段適用 (face/bg 差し替え、将来的には slot patch) は patch-ymmp 系で実施 |
| NotebookLM の代わりに LLM で台本を生成する | NotebookLM が upstream | ADR-0002 |
| ffmpeg で動画を合成する | YMM4 の責務 | ADR-0003 |

---

## 判断に迷ったとき

「この機能は Python でやるべきか、YMM4 でやるべきか？」の判断基準:

1. **それは「テキストファイルを生成する」作業か？** → Python (L2)
   - CSV、テキストメタデータ（タイトル・説明・タグ等）
2. **それは「画像・音声・映像を生成する」作業か？** → Python ではやらない
   - 画像合成、音声合成、字幕レンダリング、動画エンコード → YMM4 (L3) または外部ツール
3. **それは「YMM4 の設定を決める」作業か？** → YMM4 内部 (L3)
   - テンプレート設定、演出指定、素材配置はすべて YMM4 の責務
   - Python から .ymmp をゼロから生成する経路は存在しない。ただし台本読込後の ymmp に対する限定的な後段適用 (IR に基づく face/bg 差し替え、将来的には slot patch) は patch-ymmp 系で実施する
4. **それは「外部サービスと通信する」作業か？** → L1 or L4
   - 入力取得なら L1、配信なら L4

## 三層責務構造 (2026-04-02)

L1-L4 は「ワークフロー上の位置」を表す。三層責務は「設計上の責務分担」を表す。両者は直交する。

### 層の定義

| 層 | 名称 | 責務 | 正本 |
|----|------|------|------|
| 第1層 | Writer IR | LLM が台本から高水準の演出意味ラベル (scene_preset + optional override) を出力する | PRODUCTION_IR_SPEC.md セクション6 |
| 第2層 | Template Registry | 制作環境の再利用資産を辞書化する。YMM4 native template 名、face_map、bg_map、slot、se を束ねる | PRODUCTION_IR_SPEC.md セクション6.4。量産時の「創作パターン vs registry 自動化」の方針: [C07-visual-pattern-operator-intent.md](C07-visual-pattern-operator-intent.md)。試験手順: [verification/mass-production-pilot-checklist.md](verification/mass-production-pilot-checklist.md) |
| 第3層 | YMM4 Adapter | IR + Registry → ymmp の接着層。ネイティブで解決できるものはネイティブへ寄せ、届かない部分だけ後段補正 | PRODUCTION_IR_SPEC.md セクション6.3 |

### L1-L4 との対応

| ワークフロー層 | 三層責務との関係 |
|---------------|----------------|
| L1 入力取得 | 三者分担の対象外 |
| L2 変換 (Python) | Writer IR の定義・プロンプト管理。Adapter (patch-ymmp) の実装。Template Registry の JSON 管理 |
| L3 YMM4 内部 | Template Registry が参照する native template の実体。Adapter が出力した ymmp の消費先 |
| L4 配信 | 三者分担の対象外 |

### 設計原則

- YMM4 ネイティブに解決できるもの (エフェクト、アニメーション、場面バンドル) は native template に委ねる。Python で再発明しない
- Adapter (patch-ymmp) は face/bg/slot 等の JSON キー置換レベルの差し替えに集中する
- Writer IR は逐次属性の全列挙ではなく、scene_preset による高水準バンドル参照 + optional override を基本とする
- 「実測済み / 推測 / 未確認」の三分割は YMM4-AUTOMATION-RESEARCH.md セクション7 に記録する。未確認事項を確定事実として設計に組み込まない
- G-11 はこの safe zone に含めてよい。`slot` は registry 解決 + ymmp readback が成立すれば assistant-owned mechanical patch として扱う
- G-12 (`motion` / `transition` / `bg_anim`) は safe zone 外。native template 参照か VideoEffects / transition key 書き換えかを実測で確定するまでは manual / research 扱いに留める
- G-13 (`overlay` / `se`) も safe zone 外。timing anchor と挿入先キーの readback proof が得られるまで、設計と測定のみを先行し、最終 mix judgement は人間に残す

---

## backlog hygiene メモ

- `quarantined` 項目 (D-02, F-01, F-02) は boundary を越えていなくても、汚染バッチ由来なら通常候補として扱わない
- `hold` 項目は「やらない」ではなく「今は bottleneck を減らさない」状態
- helper prompt より `docs/ai/*.md` と project-local canonical docs を優先する
