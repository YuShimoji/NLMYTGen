# Project Cockpit

This is a navigation cockpit only. It does not replace `AGENTS.md`,
`docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md`, `docs/INVARIANTS.md`, or
the feature/spec owner docs.

## Current Checkpoint

| lane | state | primary artifact | gate |
|---|---|---|---|
| T+0 content spine package | generated | `production_pilots/yukkuri_newsroom_content_spine_001/` | local/offline review only |
| T+0 IR/CSV bridge | generated | `production_pilots/yukkuri_newsroom_content_spine_001/ir_bridge/` | draft Writer IR / cue packet / CSV only |
| T+1 transcript substitution readiness | generated/sample-fixture | `production_pilots/yukkuri_newsroom_content_spine_001/transcript_substitution_readiness/` | real transcript provenance, rights, timing, and human review still required |
| T+2 dashboard readiness ingest | generated | `production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/` | read-only status ingest; no production/public acceptance |
| T+3 GUI dashboard panel | generated | `production_pilots/yukkuri_newsroom_content_spine_001/gui_dashboard_panel/` | static read-only panel; no YMM4 GUI/render/public acceptance |
| T+4 real transcript rerun | advisory | `transcript_substitution_readiness/real_input/` or `--transcript` | requires verified local transcript input |
| T+5 YMM4 import preview pack | advisory | not built here | future YMM4 import/readback, no GUI/render in this slice |
| T+6 thumbnail visual proof | advisory | not built here | future visual proof; no image generation/public-ready claim here |

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
python -m src.cli.main build-gui-dashboard-panel --package production_pilots/yukkuri_newsroom_content_spine_001
```

The current GUI/static panel file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/gui_dashboard_panel/dashboard_panel_preview.html
```

The current GUI adapter file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/gui_dashboard_panel/gui_dashboard_adapter.json
```

Dashboard readiness ingest can still be regenerated with:

```bash
python -m src.cli.main build-dashboard-readiness-ingest --package production_pilots/yukkuri_newsroom_content_spine_001
```

The current human review file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/dashboard_preview.md
```

The current machine readback file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/dashboard_readiness_ingest/readiness_summary.json
```

Transcript readiness can still be regenerated with:

```bash
python -m src.cli.main build-transcript-substitution --package production_pilots/yukkuri_newsroom_content_spine_001
```

If a real transcript is available, place it under the generated
`real_input/` drop-zone or pass `--transcript path/to/transcript.txt`.
