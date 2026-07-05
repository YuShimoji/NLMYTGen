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
| T+4 YMM4 import preview pack | generated | `production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/` | local/offline import handoff preview; no YMM4 GUI/import/render/public acceptance |
| T+5 thumbnail visual proof pack | generated | `production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/` | static abstract proof; no external media/final image/public-ready claim |
| T+6 episode factory template registry | generated | `production_pilots/yukkuri_newsroom_content_spine_001/episode_factory_template_registry/` | reusable local/offline templates and seed sample only |
| T+7 factory seed instantiation dry-run | generated | `production_pilots/yukkuri_newsroom_content_spine_001/factory_seed_dry_run_002/` | second episode seed initialized from registry; synthetic dry-run only |
| T+8 real transcript rerun | advisory | `transcript_substitution_readiness/real_input/` or `--transcript` | requires verified local transcript input |
| T+9 actual YMM4 import review | advisory | not built here | future VoiceItem/timing readback; no render claim |
| T+10 production micro proof / deeper GUI adapter | advisory | not built here | future surface only if it reduces review friction |

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
python -m src.cli.main instantiate-episode-factory-seed --registry production_pilots/yukkuri_newsroom_content_spine_001/episode_factory_template_registry
```

The current factory seed dry-run package is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/factory_seed_dry_run_002/
```

The primary machine readback file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/factory_seed_dry_run_002/seed_instantiation_manifest.json
```

The primary human review file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/factory_seed_dry_run_002/review_checklist.md
```

Episode factory template registry can still be regenerated with:

```bash
python -m src.cli.main build-episode-factory-template-registry --package production_pilots/yukkuri_newsroom_content_spine_001
```

Thumbnail visual proof pack can still be regenerated with:

```bash
python -m src.cli.main build-thumbnail-visual-proof-pack --package production_pilots/yukkuri_newsroom_content_spine_001
```

The current thumbnail visual proof package is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/
```

The primary machine readback file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/thumbnail_proof_manifest.json
```

The primary human review files are:

```text
production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/thumbnail_proof_panel.html
production_pilots/yukkuri_newsroom_content_spine_001/thumbnail_visual_proof_pack/thumbnail_layout_proof.svg
```

YMM4 import preview pack can still be regenerated with:

```bash
python -m src.cli.main build-yymm4-import-preview-pack --package production_pilots/yukkuri_newsroom_content_spine_001
```

The current YMM4 import preview package is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/
```

The primary machine readback file is:

```text
production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/import_readiness_summary.json
```

The primary human review files are:

```text
production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/import_preview_panel.md
production_pilots/yukkuri_newsroom_content_spine_001/ymm4_import_preview_pack/import_preview_panel.html
```

GUI dashboard panel can still be regenerated with:

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
