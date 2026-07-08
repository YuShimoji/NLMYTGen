# Episode 002 YMM4 Import-Ready Remote Handoff - 2026-07-08 JST

This is the cross-terminal restart card for the Episode 002 YMM4 import-ready edit package lane.

## Repo State To Resume

- Repository: `YuShimoji/NLMYTGen`
- Branch: `codex/episode-002-ymm4-import-ready-edit-package-v1`
- Artifact completion commit before this docs-only handoff note: `a39ce95 feat: add episode 002 ymm4 import ready pack`
- Upstream after push: `origin/codex/episode-002-ymm4-import-ready-edit-package-v1`
- Expected clean/parity check after push: `git status --short --branch` clean, `git rev-list --left-right --count "HEAD...@{u}"` -> `0 0`

## Fast Restart Commands

```powershell
cd "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen"
git fetch --prune origin
git switch codex/episode-002-ymm4-import-ready-edit-package-v1
git pull --ff-only origin codex/episode-002-ymm4-import-ready-edit-package-v1
git rev-list --left-right --count "HEAD...@{u}"
```

Expected final parity output is `0 0`.

## Read First

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`
4. This file
5. `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/validation_readback.json`
6. `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/edit_slice_to_ymm4_cue_map.json`
7. `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/manual_ymm4_import_observation_sheet.md`

## Primary Artifact

- Human review: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/ymm4_import_ready_preview.html`
- Manual observation sheet: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/manual_ymm4_import_observation_sheet.md`
- Machine readback: `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/validation_readback.json`
- Local open command:

```powershell
Invoke-Item -LiteralPath "C:\Users\thank\Storage\Media Contents Projects\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\ymm4_import_ready_pack\ymm4_import_ready_preview.html"
```

## What Was Built

The package converts `local_edit_slice_execution_pack` into YMM4-facing import/observation concepts while keeping actual import/render closed.

Generated package path:

`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/`

Required package files present:

- `ymm4_import_ready_manifest.json`
- `edit_slice_to_ymm4_cue_map.json`
- `manual_ymm4_import_observation_sheet.md`
- `ymm4_import_ready_preview.html`
- `validation_readback.json`
- `gate_readback.json`
- `source_artifact_index.json`
- `ymmp_adapter_plan.json`
- `README_YMM4_IMPORT_READY.md`
- `limitations.md`

## Key Readback Values

- `status`: `passed`
- `artifact_id`: `nlm-e002-ymm4-import-ready-edit-package-v1-001`
- `queue_count`: `7`
- `scene_count`: `3`
- `cue_count`: `9`
- `observation_check_count`: `5`
- `ymm4_import_state`: `ready_for_manual_import_observation`
- `actual_ymm4_imported`: `false`
- `rendered_video_created`: `false`
- `real_input_replaced`: `false`
- `rights_approved`: `false`
- `public_ready`: `false`
- `gates_closed`: `true`
- `ymmp_file_created`: `false`
- `external_dependency_status`: `none_found`
- `forbidden_true_claims_absent`: `true`
- `temporary_copy_absent`: `true`
- `full_pytest_run`: `false`

## Cue Map

- 9 cue rows are derived from `voice_subtitle_operation_map.json`.
- Each cue records provisional timing, voice/subtitle action, visual action, citation/thumbnail placeholder action, expected YMM4 layer/track, required asset state, import risk, and manual observation question.
- Expected YMM4 lane language stays descriptive: `VoiceItem/subtitle import lane plus ImageItem/TextItem placeholder scene lanes`.
- Timing is approximate and comes from provisional scene duration splits, not actual YMM4 timing.

## Manual Observation Sheet

The sheet gives exactly 5 checks for a future explicit YMM4 observation gate:

- cue order and timing sequence;
- VoiceItem/subtitle readability;
- visual/overlay placeholder interpretability;
- placeholder versus real/final asset boundary;
- specific blocker before render.

## Validation Already Run

```powershell
python -m src.cli.main build-ymm4-import-ready-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id nlm-e002-ymm4-import-ready-edit-package-v1-001 --format json
uv run pytest tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q
git diff --check
git diff --cached --check
```

Results:

- CLI build readback: `passed`
- Targeted pytest: `20 passed`
- Generated JSON parse check: passed
- Diff whitespace checks: passed
- Static scan for external refs / forbidden production-public-YMM4 true claims: no hits
- Generated files are JSON/HTML/MD only; no `.ymmp`, media, render, image, audio, or video file was created

## Files Changed By Artifact Commit

- Added `src/pipeline/ymm4_import_ready_pack.py`
- Updated `src/cli/main.py` with `build-ymm4-import-ready-pack`
- Added `tests/test_ymm4_import_ready_pack.py`
- Added `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/`

## Do Not Resume Without A New Explicit Gate

- Actual YMM4 GUI import.
- YMM4 render/export.
- Production `.ymmp` write.
- Real input replacement execution.
- Rights/legal/public-ready acceptance.
- Final thumbnail approval.
- YouTube upload or publication.
- Live fetch/scraping or external media download.
- OAuth/API keys/payment work.
- ClipPipeGen edits.
- Destructive git or pushed-history rewrite.
- Full pytest loops unless a future code change requires them.

## Next Good Entrances

| Entrance | Reduces | Enables |
|---|---|---|
| Future explicit YMM4 import observation using the manual sheet | Unknown actual VoiceItem/subtitle timing and readability | Fill observation evidence without render/public claims |
| Verified real local source/transcript replacement gate | Placeholder content and citation wording uncertainty | Replace diagnostic text before a higher-fidelity YMM4 observation |
| Citation/thumbnail approval packet | Public-rights and final creative uncertainty | Later human approval without claiming production readiness |

## Regeneration Command

```powershell
python -m src.cli.main build-ymm4-import-ready-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id nlm-e002-ymm4-import-ready-edit-package-v1-001
```

Use targeted tests after regenerating:

```powershell
uv run pytest tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q
```
