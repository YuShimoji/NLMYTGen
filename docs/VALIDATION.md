# Validation

Re-kickstart validation source for NLMYTGen. Commands are repo-local and were
filled from `README.md`, `pyproject.toml`, `gui/package.json`, and the current
Episode 002 runtime state on 2026-07-10 JST.

## Install

```powershell
uv sync --extra dev
```

- Date: 2026-07-10 JST
- Result: confirmed from `pyproject.toml` and `README.md`; not rerun this turn
  because the existing environment already executed the tests below.
- Output path or log summary: dev dependency source is `pyproject.toml`;
  README recommends `uv sync` + `uv run pytest`.

## Development server

```text
NOT_AVAILABLE_IN_THIS_REPO
```

- Date: 2026-07-10 JST
- Result: no browser dev server is configured; this repo has a Python CLI and
  an Electron desktop GUI.
- Output path or log summary: use Preview or Screenshot capture for GUI/review
  surfaces.

## Build

```powershell
uv run python -m compileall -q src tests
```

- Date: 2026-07-10 JST
- Result: passed.
- Output path or log summary:
  `artifacts/review/rekickstart_2026-07-10_validation_log.txt`
  (`compileall_exit: 0`).

## Test

```powershell
uv run pytest tests/test_ymm4_import_ready_pack.py -q
```

- Date: 2026-07-10 JST
- Result: passed, 4 tests.
- Output path or log summary:
  `artifacts/review/rekickstart_2026-07-10_validation_log.txt`
  (`pytest_exit: 0`).

## Lint

```text
NOT_AVAILABLE_IN_THIS_REPO
```

- Date: 2026-07-10 JST
- Result: no dedicated lint command or ruff/black/mypy configuration was found
  in `pyproject.toml` or GUI package scripts.
- Output path or log summary: use `git diff --check` as the whitespace gate;
  it passed in `artifacts/review/rekickstart_2026-07-10_validation_log.txt`.

## Preview

```powershell
Invoke-Item -LiteralPath "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\ymm4_import_ready_pack\ymm4_import_ready_preview.html"
```

- Date: 2026-07-10 JST
- Result: preview artifact verified present; not opened this turn.
- Output path or log summary:
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/validation_readback.json`
  reports `access_state=verified_present`.

## Screenshot capture

```powershell
Push-Location gui; npm run capture:pipeline-smoke-gui; Pop-Location
```

- Date: 2026-07-10 JST
- Result: command exists in `gui/package.json`; not run this turn.
- Output path or log summary: expected output is
  `samples/_probe/pipeline_smoke/pipeline_smoke_gui_screenshot.png` with a JSON
  readback when Electron dependencies are installed.

## Artifact generation

```powershell
uv run python -m src.cli.main build-ymm4-import-ready-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id nlm-e002-ymm4-import-ready-edit-package-v1-001
```

- Date: 2026-07-10 JST
- Result: existing generated pack is present and its validation readback passes;
  generation was not rerun this turn to avoid unnecessary artifact churn.
- Output path or log summary:
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/validation_readback.json`
  reports `status=passed`, `queue_count=7`, `scene_count=3`, `cue_count=9`,
  and all production/public/YMM4 gates closed.

## Validation rule

A validation entry is valid only when it includes:

- command
- date
- result
- output path or log summary

## Re-kickstart task

All placeholders from the project validation template have been replaced with
repo-real commands or explicit `NOT_AVAILABLE_IN_THIS_REPO` entries. This
document is not the material deliverable by itself; this turn also produced the
validation log above.
