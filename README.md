# NLMYTGen

NotebookLM の出力を YMM4 (ゆっくりMovieMaker4) 用 CSV に変換し、演出 IR (中間表現) で S-6 (背景・演出設定) の半自動化を目指すパイプライン。

**GUI**: リポジトリ直下の [`start-gui.bat`](start-gui.bat) は **Shift_JIS (CP932) で保存**すること（UTF-8 / UTF-8-BOM にすると cmd で壊れる場合があります）。先頭 `REM` に同趣旨の注意あり。

## 目的

1. NotebookLM で生成した Audio Overview のトランスクリプトを、YMM4 の台本読込フォーマットに変換する (CSV 変換 -- 実装済み)
2. 台本から演出 IR を定義し、LLM (Custom GPT) が構造化された演出指示を出力できるようにする (演出 IR -- 設計中)
3. 演出 IR + テンプレート定義で、S-6 の背景・立ち絵・素材配置を段階的に効率化する (テンプレート半自動化 -- 計画中)

音声・字幕投入は YMM4 台本読込が不動の主経路。Python の責務は「テキスト変換 + 演出 IR 定義」であり、台本の品質は NotebookLM が生成する。

## 非目的

以下はこのプロジェクトの現行実装には含まれない:

- Python / Voicevox / MoviePy による直接動画生成
- NotebookLM を迂回した LLM による主台本生成
- Web UI / API サーバー
- YouTube 連携 / アップロード自動化 (台帳上は hold)
- 自前の音声合成 / TTS
- サムネイル生成
- .ymmp のゼロからの生成 (音声ファイル参照を含むため外部生成不可能。台本読込後の限定的な後段適用は patch-ymmp で実施)
- 素材の自動取得・ダウンロード (素材選定・収集は人間の責務)
- 多バックエンド対応 / プラグイン機構

## パイプライン

```
NotebookLM          Python (this repo)         LLM (Custom GPT)        YMM4
───────────         ──────────────────         ────────────────        ────
ソース投入 →
Audio Overview →
テキスト化 →        入力ファイル受取 →
                    パース・正規化 →
                    構造化スクリプト →
                    話者マッピング →
                    CSV 生成 →                                         台本読込 →
                    バリデーション →                                    音声合成 →
                                                                       字幕配置 →
                    台本テキスト ───→ Writer IR 生成 ──→                       ↓
                                      (scene_preset +                  [ymmp]
                                       optional override)                ↓
                                                  ↓                      ↓
                    Template Registry ── 意味ラベル→リソース解決           ↓
                                                  ↓                      ↓
                    YMM4 Adapter (patch-ymmp) ── face/bg 差し替え ──→ [ymmp']
                                                                       ↓
                                                            ──→ S-6 演出微調整 →
                                                                       レンダリング
```

**Path A (実装済み):** CSV 変換 → YMM4 台本読込 → 音声 + 字幕
**Path B (三層責務):** 台本 → Writer IR (LLM) → Template Registry (解決) → YMM4 Adapter (patch-ymmp) → S-6 微調整

## 入力

NotebookLM 由来のテキストファイル。以下のフォーマットを受け付ける:

- **CSV** (.csv): 2列 (話者名, テキスト)。ヘッダー行は自動スキップ
- **テキスト** (.txt): 話者タグ付き対話 (`Speaker: text` 形式)
- **ラベルなしテキスト** (.txt + `--unlabeled`): 話者タグなしの生テキスト。行交互で 2 話者 (Speaker_A/Speaker_B) に自動割当
- BOM 付き UTF-8 も自動対応

## 出力

YMM4 台本読込用 CSV:
- 2列、ヘッダーなし、UTF-8、カンマ区切り
- 列1: YMM4 キャラクター名
- 列2: 発話テキスト

## 使い方

### H-01 Packaging Brief の空テンプレ（品質診断の前段）

```bash
# Markdown テンプレ（仕様 v0.1 §5 相当）をファイルへ
python -m src.cli.main emit-packaging-brief-template -o packaging_brief.md

# 最小 JSON 骨格（score-evidence 等でそのまま読める形）
python -m src.cli.main emit-packaging-brief-template --format json -o packaging_brief.json
```

### CLI 一覧（抜粋）

```bash
# CSV 生成
python -m src.cli.main build-csv input.txt -o output.csv --speaker-map Host1=れいむ,Host2=まりさ

# 話者マッピングファイルを使用 (JSON or key=value テキスト)
python -m src.cli.main build-csv input.txt --speaker-map-file speakers.json

# プレビュー (CSV を書かずに結果を確認)
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ --dry-run

# 統計表示付き
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ --stats

# 入力検証
python -m src.cli.main validate input.txt

# 入力の詳細分析 + マッピングプレビュー
python -m src.cli.main inspect input.txt --speaker-map Host1=れいむ,Host2=まりさ

# 話者マッピングテンプレートを自動生成
python -m src.cli.main generate-map input.txt > speakers.txt
# speakers.txt を編集して --speaker-map-file で使用

# B-15 Phase 1: 外部 LLM / Automation に渡す cue packet を生成
python -m src.cli.main build-cue-packet input.txt -o cue_packet.md

# JSON packet として出力
python -m src.cli.main build-cue-packet input.txt --format json -o cue_packet.json

# packet markdown/json と workflow proof 雛形をまとめて出力
python -m src.cli.main build-cue-packet input.txt --bundle-dir samples

# B-16: 外部 LLM / Automation に渡す diagram brief packet を生成
python -m src.cli.main build-diagram-packet input.txt -o diagram_packet.md

# diagram packet markdown/json と workflow proof 雛形をまとめて出力
python -m src.cli.main build-diagram-packet input.txt --bundle-dir samples

# 同一話者の連続発話を結合
python -m src.cli.main build-csv input.txt --merge-consecutive --speaker-map Host1=れいむ

# 表示幅ベースで字幕はみ出しを抑える
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ,Host2=まりさ --max-lines 2 --chars-per-line 40 --stats

# 2行字幕向けに自然な改行を入れつつ、長い一文は節単位で積極的に分ける
python -m src.cli.main build-csv input.txt --speaker-map Host1=れいむ,Host2=まりさ --max-lines 2 --chars-per-line 40 --balance-lines --stats

# ラベルなし NLM transcript (話者タグなしの生テキスト)
python -m src.cli.main build-csv transcript.txt --unlabeled --speaker-map Speaker_A=れいむ,Speaker_B=まりさ

# ラベルなし + 連続結合 + 統計
python -m src.cli.main build-csv transcript.txt --unlabeled --merge-consecutive --speaker-map Speaker_A=れいむ,Speaker_B=まりさ --stats

# 複数ファイル一括処理 (各ファイルに {stem}_ymm4.csv を生成)
python -m src.cli.main build-csv file1.txt file2.txt file3.txt --speaker-map Host1=れいむ,Host2=まりさ
```

## 開発環境とテスト

`pytest` は `requirements-dev.txt` に固定してある。仮想環境を用意してインストールすれば `python -m pytest` でテストを実行できる。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest
```

`uv` を使う場合は `uv venv .venv && uv pip install -r requirements-dev.txt` と `uv run pytest` でも同じ結果になる（WSL の標準 Python には ensurepip が入っていないため、この方法の方が早い）。

この repo では `.venv` が Windows 形式 (`Scripts/`) の場合がある。WSL から確認する場合は、Linux 側の別名 venv を切るのが安全。

```bash
~/.local/bin/uv venv .venv-linux
~/.local/bin/uv pip install -r requirements-dev.txt --python .venv-linux
TMPDIR=/tmp TMP=/tmp TEMP=/tmp .venv-linux/bin/python -m pytest
```

WSL で実行する場合は `TMPDIR=/tmp TMP=/tmp TEMP=/tmp` を設定してから `pytest` を実行すると一時ファイルのパスずれを避けられる。

## LLM の役割

このプロジェクトで LLM を使う場合、責務は以下に限定する:

- transcript / notes の構造化
- セグメント化
- タイトル・見出し・要約の補助
- CSV 向けフィールド整形

LLM は NotebookLM の代替としての主台本生成には使わない。
LLM の主要な新しい役割は、台本から演出 IR (構造化 JSON) を生成すること (G-05 v4 プロンプト)。IR は意味ラベルのみを含み、座標・ファイルパスはテンプレート定義側で解決する。
Phase 1 では `build-cue-packet` により、外部 LLM / Automation に渡す text-only cue packet を生成する。
現在の cue contract は、section ごとに `主背景 1 つ + 補助素材 1 つ` を基本とし、音の cue は optional 扱いに寄せている。
図作成 bottleneck 向けには `build-diagram-packet` により、図版そのものではなく「図作成前の text-only brief」を生成できる。
