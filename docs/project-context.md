# Project Context

## Overview

NLMYTGen v2: NotebookLM transcript to YMM4 CSV pipeline.
NLMandSlideVideoGenerator の設計ドリフトを断ち切った再建プロジェクト。

## Current State (2026-03-24)

- Phase 0 (基盤文書) + Phase 1 (最小実装骨格) 完了
- 29 files, 2 commits, pushed to origin/master
- 15 tests all passing
- 外部依存ゼロ (Python stdlib のみ)
- CLI 動作確認済み: build-csv / validate

## What Exists

- 3 data contracts: RawTranscript, StructuredScript, YMM4CsvOutput
- 3 pipeline modules: normalize, assemble_csv, validate_handoff
- CLI (build-csv / validate) via `python -m src.cli.main`
- 基盤文書: README, PROJECT_CHARTER, ARCHITECTURE, PIPELINE_SPEC, 3 ADR, MIGRATION_LEDGER

## What Does NOT Exist Yet

- LLM 構造化補助 (Gemini 等)
- 画像取得 / サムネイル生成
- Web UI / API
- YouTube 連携
- 実際の NotebookLM transcript での E2E 検証

## Key Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-24 | YMM4 CSV は 2列 (speaker, text) | YMM4 台本読込の実フォーマット。画像/アニメ列は初期スコープ外 |
| 2026-03-24 | Phase 1 は LLM 依存ゼロ | 純粋な機械的変換。LLM は将来のオプション拡張 |
| 2026-03-24 | async 不使用 | ファイル I/O に不要。旧 PJ の過剰 async を踏襲しない |
| 2026-03-24 | 全 dataclass は frozen=True | 旧 PJ で mutable state がバグ源だった |
