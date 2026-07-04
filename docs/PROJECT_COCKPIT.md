# Project Cockpit

This is a navigation cockpit only. It does not replace `AGENTS.md`,
`docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, `docs/INVARIANTS.md`, or
the feature/spec owner docs.

## Current Checkpoint

| lane | state | primary artifact | gate |
|---|---|---|---|
| T+0 content spine package | generated | `production_pilots/yukkuri_newsroom_content_spine_001/` | local/offline review only |
| T+0 IR/CSV bridge | generated | `production_pilots/yukkuri_newsroom_content_spine_001/ir_bridge/` | draft Writer IR / cue packet / CSV only |
| T+1 transcript substitution readiness | active/generated | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/` | real transcript provenance, rights, timing, and human review still required |
| T+2 dashboard ingest | advisory | not built here | future dashboard state intake |
| T+3 YMM4 import preview pack | advisory | not built here | future YMM4 import/readback, no GUI/render in this slice |

## True Gates

- Real or NotebookLM transcript provenance and rights review.
- Human source/claim review before public use.
- YMM4 CSV import and VoiceItem timing readback.
- `validate-ir` / `apply-production` inputs and maps when a production route is
  actually approved.

## Non-Gates In This Slice

- No live RSS fetch, scraping, media download, OAuth, paid API, or YouTube action.
- No YMM4 GUI launch, render, production `.ymmp`, or public-ready acceptance.
- No Baseball hash residue repair unless it blocks narrow validation.

## Latest Regeneration

Use this command from the repo root:

```bash
python -m src.cli.main build-transcript-substitution --package production_pilots/yukkuri_newsroom_content_spine_001
```

If a real transcript is available, place it under the generated
`real_input/` drop-zone or pass `--transcript path/to/transcript.txt`.
