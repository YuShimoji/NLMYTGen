# NLMYTGen

NotebookLM transcript to YMM4 CSV pipeline.

## Rules

- Path A only. No alternate pipelines.
- NotebookLM is mandatory upstream context. Do not bypass it.
- Internal LLM is not the primary script author. LLM is for structuring/normalization/validation only.
- Do not introduce direct Python/Voicevox/MoviePy video generation.
- Keep one main entrypoint (`src/cli/main.py`).
- Prefer ADR update before architectural expansion.
- Ask before adding major scope.
- Respond in Japanese.
- No emoji.
- Tests are few and contract-focused. Do not inflate test count.
- No abstract classes, provider patterns, plugin architectures, or fallback chains unless explicitly decided via ADR.

## Key Paths

- Source: `src/`
- Tests: `tests/`
- Docs: `docs/`
- Samples: `samples/`
- CLI entry: `src/cli/main.py`

## Architecture

- Input: NotebookLM transcript (.txt or .csv)
- Internal: StructuredScript (frozen dataclass)
- Output: YMM4 CSV (2-column, no header, UTF-8)
- No external dependencies beyond Python stdlib.

## Project Status

直近の状態 (2026-03-28):
  - Phase 0~4 完了 (基盤文書 + 実装骨格 + CLI拡張 + ラベルなし入力対応 + 品質改善・一括処理)
  - 15 tests, 0 failed (pytest), mock ゼロ
  - 外部依存ゼロ (Python stdlib のみ)
  - CLI: build-csv / validate / inspect / generate-map (--unlabeled, --speaker-map, --speaker-map-file, --dry-run, --stats, --merge-consecutive)
  - **全工程 E2E 達成:** NLM transcript → --unlabeled → CSV (BOM付き) → YMM4 台本読込 → タイムライン配置
  - **品質改善:** 句読点終端の相槌を独立発話として保持 (136→142 utterances)
  - **一括処理 (IP-04):** build-csv で複数入力ファイルをサポート
  - WORKFLOW.md: NLM → CSV → YMM4 → 動画 の全工程手順書
