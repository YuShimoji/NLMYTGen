# Project Context

## Overview

NLMYTGen v2: NotebookLM transcript to YMM4 CSV pipeline.
NLMandSlideVideoGenerator の設計ドリフトを断ち切った再建プロジェクト。

## Current State (2026-03-27)

- Phase 0~3 完了 (基盤文書 + 実装骨格 + CLI拡張 + ラベルなし入力対応)
- **全工程 E2E 達成:** NLM transcript → CSV → YMM4 台本読込 → タイムライン配置
- 19 commits, 15 tests all passing, mock ゼロ
- 外部依存ゼロ (Python stdlib のみ)
- CLI: build-csv / validate / inspect / generate-map の4コマンド
- オプション: --unlabeled, --speaker-map, --speaker-map-file, --dry-run, --stats, --merge-consecutive
- CSV出力: UTF-8 BOM付き (utf-8-sig)。YMM4 互換確認済み
- WORKFLOW.md: NLM → CSV → YMM4 → 動画 の全工程手順書
- 全 blocker 解消。次スライス未定

## What Exists

- 3 data contracts: RawTranscript, StructuredScript, YMM4CsvOutput
- 3 pipeline modules: normalize, assemble_csv, validate_handoff
- CLI (build-csv / validate / inspect) via `python -m src.cli.main`
- 基盤文書: README, PROJECT_CHARTER, ARCHITECTURE, PIPELINE_SPEC, 3 ADR, MIGRATION_LEDGER

## What Does NOT Exist Yet

- LLM 構造化補助 (Gemini 等) — 評価中 (IP-01)
- 画像取得 / サムネイル生成
- Web UI / API
- YouTube 連携
- ~~複数ファイルの一括処理~~ → IP-04 で実装済み

## Key Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-24 | YMM4 CSV は 2列 (speaker, text) | YMM4 台本読込の実フォーマット。画像/アニメ列は初期スコープ外 |
| 2026-03-24 | Phase 1 は LLM 依存ゼロ | 純粋な機械的変換。LLM は将来のオプション拡張 |
| 2026-03-24 | async 不使用 | ファイル I/O に不要。旧 PJ の過剰 async を踏襲しない |
| 2026-03-24 | 全 dataclass は frozen=True | 旧 PJ で mutable state がバグ源だった |
| 2026-03-26 | validate_handoff から speaker_map 依存を除去 | assembly 後の値側チェックはロジック誤り。CLI で pre-assembly チェックに変更 |
| 2026-03-26 | 話者プレフィックス除去を動的化 | 任意の話者名に対応。静的パターン + 動的チェックの2段階 |
| 2026-03-26 | --speaker-map-file で JSON/key=value ファイル対応 | 毎回のコマンドライン指定の手間を削減 |
| 2026-03-26 | --merge-consecutive で連続発話マージ | NotebookLM の同一話者分割出力への対応 |
| 2026-03-27 | 実 NotebookLM transcript はラベルなし形式と判明 | サンプルは "Speaker: text" だが実際は生テキスト行。パーサー拡張が必要 |
| 2026-03-27 | merge_consecutive の区切り文字なし結合を修正 | 句読点なしの行末に「。」を自動補完 |
| 2026-03-27 | --unlabeled フラグで行交互割当方式を採用 | 実 NLM transcript がラベルなし形式。短行(≤3文字)は前行結合で音声認識分断を緩和 |
| 2026-03-27 | CSV 出力を UTF-8 BOM 付き (utf-8-sig) に変更 | YMM4 が BOM なし UTF-8 を Shift-JIS と誤認する問題への対応 |
| 2026-03-27 | 台本読込メニューは「ツール → 台本読み込み」 | 「ファイル → プロジェクトを開く」ではない。WORKFLOW.md に明記 |
| 2026-03-29 | Gemini API 技術調査完了。SDK統合済み(google-genai)だがSDK依存が重い。urllib直叩きなら外部依存ゼロ維持可能 | 旧SDK非推奨化済み。モデル廃止サイクルが速い(数ヶ月)。Flash-Lite $0.003/件 |
| 2026-03-29 | IP-01 採否はgold set (正解ラベル)完成後に数値判定 | 行交互の精度が未測定のままLLM導入に進まない。Go/No-Go基準を先に定義 |
| 2026-03-29 | ルールベース改善はカスケード問題で限界あり | 文分断検出が1箇所のずれを全行に波及させる。行単位の独立判定が必要 |

## IDEA POOL

| ID | Idea | Status | Note |
|----|------|--------|------|
| IP-01 | LLM 構造化補助 (Gemini) | **no-go** | パターン正答率92.3%で行交互は高精度。LLM費用対効果が低い。代わりにロール推定機能を追加 |
| IP-02 | YMM4 テンプレート連携 | hold | スコープ拡大時 |
| IP-03 | YMM4 プラグイン開発 | hold | スコープ拡大時 |
| IP-04 | 複数ファイル一括処理 | **done** | build-csv で複数入力をサポート。エラーハンドリング・サマリー表示付き |
| IP-05 | 実 NotebookLM transcript E2E | **done** | --unlabeled で 143行→136 utterances→CSV 生成成功 |
| IP-06 | YMM4 実読込確認 | **done** | YMM4 通常版で台本読込 → タイムライン配置確認。Lite版は起動不具合あり |
| IP-07 | ラベルなし入力対応 (行交互割当) | **done** | --unlabeled フラグで実装。短行結合あり |
