# Episode 002 YMM4 Observation Readback Handoff

Date: 2026-07-09 JST
Branch: `codex/episode-002-ymm4-observation-readback-v1`
Artifact/package commit before this docs-only remote seal: `506ec9e`
Remote state before this docs-only remote seal: pushed, upstream parity `0 0`,
worktree clean.

## Scope

This handoff seals the Episode 002 YMM4 observation readback package:

`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/`

Primary review:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/observation_preview.html`

Machine readback:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/observation_readback.json`

Manual operator sheet:
`production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/manual_ymm4_observation_readback.md`

The package opens only the observation-readback lane. It does not render/export,
write a production `.ymmp`, replace real input, approve rights/public readiness,
approve final thumbnail, upload, fetch, scrape, or download external media.

## Observation State

YMM4 was detected locally:

`C:\Users\PLANNER007\Downloads\YukkuriMovieMaker_v4\YukkuriMovieMaker.exe`

The primary CSV import candidate exists:

`production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`

Actual GUI import observation was not attempted. The blocker is that this
worker has no safe manual/GUI visual readback channel for importing and
inspecting the YMM4 result. Therefore the package is an honest
operator-instruction hold, not an observation pass.

## Readback

- `status=blocked`
- `validation_status=passed`
- `observation_mode=operator_instruction_only`
- `actual_ymm4_import_attempted=false`
- `actual_ymm4_imported=false`
- `observed_at=not_observed_2026-07-09_JST`
- `cue_count_expected=9`
- `cue_count_observed=0`
- `scene_count_expected=3`
- `voice_item_observed=not_observed`
- `subtitle_item_observed=not_observed`
- `timing_order_observed=not_observed`
- `placeholder_boundary_observed=not_observed`
- `screenshot_or_visual_evidence_paths=[]`
- `rendered_video_created=false`
- `ymmp_file_created=false`
- `production_ymmp_written=false`
- `real_input_replaced=false`
- `rights_approved=false`
- `public_ready=false`
- `next_gate=manual_ymm4_import_observation_return`

## Restart

From another terminal:

```powershell
git fetch --prune origin
git switch codex/episode-002-ymm4-observation-readback-v1
git pull --ff-only origin codex/episode-002-ymm4-observation-readback-v1
git rev-list --left-right --count "HEAD...@{u}"
```

Expected parity after push: `0 0`.

Then read:

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`
4. `docs/project-context.md` top handoff entry
5. this file
6. `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/observation_readback.json`

Open the review surface:

```powershell
Invoke-Item -LiteralPath "C:\Users\PLANNER007\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\ymm4_observation_readback_pack\observation_preview.html"
```

## Regeneration

```powershell
uv run python -m src.cli.main build-ymm4-observation-readback-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_ymm4_observation_readback_pack_v1 --format json
```

## Validation

Passed:

```powershell
uv run pytest tests/test_ymm4_observation_readback_pack.py tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_real_input_replacement_readiness_pack.py -q
```

Result: 16 passed.

Also passed:

- generated `observation_readback.json` parses
- no external refs in the observation package
- no forbidden production/public/YMM4 true claims in the observation package
- no media/render/image/audio/video/`.ymmp` files were created in the package
- `git diff --check`

Full pytest was not run by repo policy and slice scope.

## Operator Action

The next valid action is manual observation:

1. Open YMM4.
2. Import
   `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/regenerated_draft_yymm4.csv`.
3. Inspect cue order, VoiceItem count/order, subtitle mapping, timing order,
   and placeholder boundary.
4. Return the five observations listed in
   `manual_ymm4_observation_readback.md`.

Do not render/export. Do not save or write a production `.ymmp`. Do not replace
real input. Do not approve rights/public/final thumbnail. Do not upload.

## Next Decision

After actual observation returns, choose one lane based on evidence:

- adapter correction if cue/VoiceItem/subtitle/timing deviates
- real input receipt if import behavior is acceptable and the next bottleneck is verified local material
- later render proof only after explicit render/export gate opens
