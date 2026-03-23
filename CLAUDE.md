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
