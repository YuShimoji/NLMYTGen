# NLMYTGen

NotebookLM の出力を YMM4 (ゆっくりMovieMaker4) 用 CSV に変換するパイプライン。

## 目的

NotebookLM で生成した Audio Overview のトランスクリプトを、YMM4 の台本読込フォーマットに変換する。
Python の責務は「構造化・整形・検証」であり、台本の品質は NotebookLM が生成する。

## 非目的

以下はこのプロジェクトのスコープ外:

- Python / Voicevox / MoviePy による直接動画生成
- NotebookLM を迂回した LLM による主台本生成
- Web UI / API サーバー
- YouTube 連携 / アップロード自動化
- 自前の音声合成 / TTS
- サムネイル生成
- 画像取得の本実装
- 多バックエンド対応 / プラグイン機構

## パイプライン (Path A only)

```
NotebookLM          Python (this repo)         YMM4
───────────         ──────────────────         ────
ソース投入 →
Audio Overview →
テキスト化 →        入力ファイル受取 →
                    パース・正規化 →
                    構造化スクリプト →
                    話者マッピング →
                    CSV 生成 →
                    バリデーション →           台本読込 →
                                               音声合成 →
                                               動画レンダリング
```

## 入力

NotebookLM 由来のテキストファイル。以下のフォーマットを受け付ける:

- **CSV** (.csv): 2列 (話者名, テキスト)
- **テキスト** (.txt): 話者タグ付き対話 (`Speaker: text` 形式)

## 出力

YMM4 台本読込用 CSV:
- 2列、ヘッダーなし、UTF-8、カンマ区切り
- 列1: YMM4 キャラクター名
- 列2: 発話テキスト

## 使い方

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
```

## LLM の役割

このプロジェクトで LLM を使う場合、責務は以下に限定する:

- transcript / notes の構造化
- セグメント化
- タイトル・見出し・要約の補助
- CSV 向けフィールド整形

LLM は NotebookLM の代替としての主台本生成には使わない。
