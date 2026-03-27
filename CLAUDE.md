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

直近の状態 (2026-03-27):
  - Phase 0 (基盤文書) + Phase 1 (実装骨格) + Phase 2 (CLI拡張・品質改善) 完了
  - 15 tests, 0 failed (pytest), mock ゼロ
  - 外部依存ゼロ (Python stdlib のみ)
  - CLI: build-csv / validate / inspect (--speaker-map, --speaker-map-file, --dry-run, --stats, --merge-consecutive)
  - **実データ発見:** 実 NotebookLM transcript はスピーカーラベルなしの生テキスト形式。パーサー拡張（ラベルなし入力対応）が E2E の前提
  - merge_consecutive 区切り文字なし結合バグ修正済み
  - 次のアクション: ラベルなし入力対応 → 実データ E2E → YMM4 実読込確認
