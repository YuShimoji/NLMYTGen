# Episode 002 Verified Real Input Prep Handoff

Date: 2026-07-09 JST
Branch: `codex/episode-002-verified-real-input-prep-v1`

## Scope

This handoff seals the Episode 002 verified local input replacement readiness
pack:

`production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/`

Primary review:
`production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/real_input_replacement_preview.html`

Operator contract:
`production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/real_input_replacement_contract.md`

Machine readback:
`production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/validation_readback.json`

Placeholder input folder note:
`production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/input_dropzone/README.md`

The package prepares the replacement gate only. It does not replace real input,
fetch sources, download media, launch YMM4, render video, create a `.ymmp`, or
approve rights/public readiness.

## Readback

- `status=passed`
- `episode_id=yukkuri_newsroom_content_spine_002`
- `package_type=real_input_replacement_readiness`
- `source_episode_pack_reference=production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack`
- `placeholder_state=sample_diagnostic_only_no_verified_local_input`
- `required_local_input_count=5`
- `candidate_input_count=0`
- `actual_real_input_replaced=false`
- `live_fetch_performed=false`
- `external_media_downloaded=false`
- `actual_ymm4_imported=false`
- `rendered_video_created=false`
- `ymmp_file_created=false`
- `rights_approved=false`
- `public_ready=false`
- `next_gate=provide_verified_local_source_and_transcript`

The five required inputs are:

1. source audio/video/document path
2. transcript path or transcript generation receipt
3. source provenance/rights note
4. file hash or stable identity
5. Episode 002 cue-map alignment

The HTML surface is Japanese-first and uses a pipeline runway plus
matrix/status tables. It is intentionally not a primary card-grid dashboard.

## Restart

From another terminal:

```powershell
git fetch --prune origin
git switch codex/episode-002-verified-real-input-prep-v1
git pull --ff-only origin codex/episode-002-verified-real-input-prep-v1
git rev-list --left-right --count "HEAD...@{u}"
```

Expected parity after push: `0 0`.

Then read:

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`
4. `docs/project-context.md` top handoff entry
5. this file
6. `production_pilots/yukkuri_newsroom_content_spine_002/real_input_replacement_readiness_pack/validation_readback.json`

Open the review surface:

```powershell
Invoke-Item -LiteralPath "C:\Users\PLANNER007\NLMYTGen\production_pilots\yukkuri_newsroom_content_spine_002\real_input_replacement_readiness_pack\real_input_replacement_preview.html"
```

## Regeneration

```powershell
uv run python -m src.cli.main build-real-input-replacement-readiness-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_verified_real_input_replacement_readiness_pack_v1 --format json
```

## Validation

Passed:

```powershell
uv run pytest tests/test_real_input_replacement_readiness_pack.py tests/test_ymm4_import_ready_pack.py tests/test_local_edit_slice_execution_pack.py tests/test_editing_operations_readiness_pack.py tests/test_output_template_readiness_pack.py tests/test_real_input_intake_readiness_pack.py -q
```

Result: 24 passed.

Also passed:

- generated `validation_readback.json` parses and reports `status=passed`
- no external refs in the new package
- no forbidden production/public/YMM4 true claims in the new package
- no media/render/image/audio/video/`.ymmp` files were created in the package

Full pytest was not run by repo policy and slice scope.

## Closed Boundaries

Do not continue from this handoff into:

- actual real input replacement
- actual YMM4 GUI import
- YMM4 render/export
- production `.ymmp` write
- rights/legal/public-ready acceptance
- final thumbnail approval
- YouTube upload/publication
- live fetch/scraping
- external media download
- OAuth/API/payment work
- ClipPipeGen edits
- destructive git
- full pytest loops without a broader executable reason

## Next Move

The next valid product move is to provide verified local source/transcript
material and build a validated local input receipt. The deferred A lane,
YMM4 observation readback, remains second_launch and should only run after an
explicit future gate.
