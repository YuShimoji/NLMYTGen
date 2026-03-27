# Project Context

## Overview

NLMYTGen v2: NotebookLM transcript to YMM4 CSV pipeline.
NLMandSlideVideoGenerator の設計ドリフトを断ち切った再建プロジェクト。

## Current State (2026-03-27)

- Phase 0~3 完了 (基盤文書 + 実装骨格 + CLI拡張 + ラベルなし入力対応)
- 15 tests all passing, mock ゼロ
- 外部依存ゼロ (Python stdlib のみ)
- CLI: build-csv / validate / inspect / generate-map の4コマンド
- オプション: --unlabeled, --speaker-map, --speaker-map-file, --dry-run, --stats, --merge-consecutive
- **実データ E2E (コード側) 達成:** 実 NLM transcript (143行) → 136 utterances → YMM4 CSV
- WORKFLOW.md 作成済み: NLM → CSV → YMM4 → 動画 の全工程手順書
- 残り: YMM4 での実読込確認 (手動ステップ)

## What Exists

- 3 data contracts: RawTranscript, StructuredScript, YMM4CsvOutput
- 3 pipeline modules: normalize, assemble_csv, validate_handoff
- CLI (build-csv / validate / inspect) via `python -m src.cli.main`
- 基盤文書: README, PROJECT_CHARTER, ARCHITECTURE, PIPELINE_SPEC, 3 ADR, MIGRATION_LEDGER

## What Does NOT Exist Yet

- LLM 構造化補助 (Gemini 等)
- 画像取得 / サムネイル生成
- Web UI / API
- YouTube 連携
- 複数ファイルの一括処理

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

## IDEA POOL

| ID | Idea | Status | Note |
|----|------|--------|------|
| IP-01 | LLM 構造化補助 (Gemini) | hold | 実データ E2E 完了後に再評価 |
| IP-02 | YMM4 テンプレート連携 | hold | スコープ拡大時 |
| IP-03 | YMM4 プラグイン開発 | hold | スコープ拡大時 |
| IP-04 | 複数ファイル一括処理 | hold | PIPELINE_SPEC でスコープ外として明記 |
| IP-05 | 実 NotebookLM transcript E2E | **done** | --unlabeled で 143行→136 utterances→CSV 生成成功 |
| IP-06 | YMM4 実読込確認 | **next** | CSV は生成済み。YMM4 での手動読込テスト待ち |
| IP-07 | ラベルなし入力対応 (行交互割当) | **done** | --unlabeled フラグで実装。短行結合あり |
