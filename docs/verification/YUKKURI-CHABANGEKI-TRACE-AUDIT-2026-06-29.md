# Yukkuri Chabangeki Trace Audit (2026-06-29)

This memo preserves the repo evidence for the user question:

> このプロジェクトに、「ゆっくり茶番劇風」のアニメーション自動生成に関する作業の痕跡は残っていますか？

## Live Checkout

- Repo: `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen`
- Branch before this docs handoff: `codex/baseball-bn08-script-beat-linkage`
- Upstream: `origin/codex/baseball-bn08-script-beat-linkage`
- Pre-handoff HEAD: `4abb199 test: validate baseball BN-08 script beat linkage`
- Sync checks before this memo:
  - `git fetch --prune origin`
  - `git pull --ff-only origin codex/baseball-bn08-script-beat-linkage`
  - `git rev-list --left-right --count "HEAD...@{u}"` => `0 0`
  - `git status --short --branch` => clean tracked tree

## Answer

Yes. The exact phrase `ゆっくり茶番劇風` is not the main durable key, but the work remains under related names:

- `ゆっくり茶番劇`
- `茶番劇風`
- `background skit`
- `skit_group`
- `pilot_yukkuri_theater_v1`

The trace is not just a stray note. It includes design docs, implementation, tests, sample IR / `.ymmp` artifacts, validation reports, and ignored local episode-run residue.

## Main Evidence

- `docs/C07-visual-pattern-operator-intent.md`
  - Records the original variant pattern: external person artwork such as delivery staff / firefighters / idols with a yukkuri head overlaid, treated as one consistent character.
  - It explicitly separates this from normal yukkuri speaker tachie work.
- `docs/SKIT_GROUP_TEMPLATE_SPEC.md`
  - Current main specification for background chabangeki / `skit_group`.
  - Defines background chabangeki as an independent visual side story, not a line-by-line reaction track to narrator dialogue.
  - Establishes the current route: repo-tracked YMM4 `GroupItem` template source + registry resolution + patch-time placement.
  - Fixes a hard boundary: `TachieItem` is reserved for yukkuri narrator standing pictures; external chabangeki actors use `ImageItem` children under `GroupItem`.
- `docs/AUTOMATION_BOUNDARY.md`
  - Defines what NLMYTGen does and does not automate.
  - Allows CSV / IR / registry / manifest generation and limited post-import `.ymmp` patching.
  - Rejects `.ymmp` zero-generation, YMM4 script-import replacement, audio generation, automatic asset acquisition, and universal YMM4 GUI control.
- `docs/verification/CHABANGEKI-E2E-PROOF-2026-04-13.md`
  - Records a chabangeki-style E2E proof using existing face / idle_face / slot / motion fields.
  - It proves the pipeline can control expression, placement, and movement in a chabangeki-like way, but does not claim production-quality automation.
- `docs/PILOT_YUKKURI_THEATER_SCENE_BIBLE.md`
  - Keeps `pilot_yukkuri_theater_v1` background chabangeki as an IR-before-YMM4 scene-bible contract.
  - Separates transport/readback proof from creative / production acceptance.
- `docs/BACKGROUND_SKIT_BLUEPRINT_TIMETABLE_WORKFLOW.md`
  - Defines the stricter blueprint / timetable workflow before background chabangeki can move into IR and YMM4 timing.
- `docs/verification/REAL-ESTATE-DX-BACKGROUND-SKIT-BLUEPRINT-2026-05-06.md`
  - Records the Real Estate DX background skit blueprint and validation state.
  - Keeps older `real_estate_dx_skit_group_patched.ymmp` as transport/readback proof only, not creative acceptance.

## Implementation Evidence

- `src/pipeline/skit_group_placement.py`
  - Implements `apply_skit_group_placement`.
  - Extracts YMM4 `GroupItem` templates from a template source and inserts resolved `skit_group` clips into the timeline.
  - Rejects `TachieItem` inside `skit_group` templates.
- `src/pipeline/skit_group_audit.py`
  - Loads and audits `skit_group` registry resolution.
- `src/pipeline/background_skit_blueprint.py`
  - Validates background skit blueprint / timetable readiness.
- `src/pipeline/ymmp_patch.py` and `src/cli/main.py`
  - Wire `--skit-group-registry`, `--skit-group-template-source`, `--skit-group-only`, and compact-review placement into `patch-ymmp` / `apply-production`.
- `.claude/hooks/guardrails.py` and `tests/test_guardrails.py`
  - Guard against role drift, including treating background skit as narrator line reactions, overclaiming creative acceptance, and underclaiming the adapter role.

## Sample / Artifact Evidence

Tracked examples:

- `samples/chabangeki_e2e_ir.json`
- `samples/chabangeki_e2e_patched.ymmp`
- `samples/chabangeki_e2e_patched_v2.ymmp`
- `samples/g24_skit_group_minimal_production_ir.json`
- `samples/registry_template/skit_group_registry.template.json`
- `samples/templates/skit_group/delivery_v1_templates.ymmp`
- `samples/_probe/skit_01/skit_01_ir.json`
- `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp`
- `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp`
- `samples/_probe/g24/real_estate_dx_background_skit_blueprint.json`
- `samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json`

Ignored local residue observed by filename/state scan:

- `_tmp/episode_runs/pilot_yukkuri_theater_v1/`
- `_tmp/skit_01_v1.ymmp`
- `_tmp/skit_01_v2.ymmp`
- `_tmp/skit_ManualSample_01.ymmp`
- `_tmp/baseball_branch_export2/` and `_tmp/baseball_branch_export3/` copies containing the same tracked-context surfaces

Ignored residue is useful as same-machine evidence but is not repo-truth. A restart from another terminal should trust the tracked docs and samples first.

## Current Interpretation

The repo contains real work toward chabangeki-style automation, but the accepted boundary is narrower than "fully automatic animation generation":

- Proven / retained:
  - yukkuri dialogue and expression-control E2E proof
  - `skit_group` registry / template-source resolution
  - YMM4 `GroupItem` placement from repo-tracked template source
  - compact review and readback surfaces
  - blueprint validation for background skit planning
- Not proven / intentionally out of scope:
  - automatic new character art generation
  - automatic asset download / acquisition
  - `.ymmp` generation from zero as a replacement for YMM4 script import
  - creative acceptance or production acceptance of old chabangeki carriers
  - universal YMM4 GUI control

## Residual Work

- Purpose: decide whether to revive this lane or just keep it as historical / reference context.
  Effect: revival would move from evidence review into a scoped feature slice; historical retention requires no implementation.
  Requirement: user must explicitly pick this as an active lane because current checkout work is on `codex/baseball-bn08-script-beat-linkage`.
  State: evidence is present and indexed here; no code changes were made by this audit.
  Owner: user for lane selection, assistant for follow-up audit or implementation once selected.
  Next move: if revived, start from `docs/SKIT_GROUP_TEMPLATE_SPEC.md`, `docs/PILOT_YUKKURI_THEATER_SCENE_BIBLE.md`, and this memo, then decide whether the target is a blueprint-only report, a compact-review `.ymmp`, or a production-timing path.

- Purpose: avoid overclaiming the old artifacts.
  Effect: keeps transport/readback proof separate from creative / production acceptance.
  Requirement: any next report must preserve the `diagnostic / transport proof only` boundary unless fresh human YMM4 review accepts a specific artifact.
  State: older Real Estate DX and pilot artifacts remain blocked from creative acceptance.
  Owner: assistant for wording and validation boundaries; user for creative review.
  Next move: do not promote `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` or ignored `_tmp` episode artifacts without a new acceptance signal.

## Restart Note

For another terminal, read in this order:

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`
4. This memo, only if the task is about yukkuri chabangeki / background skit / `skit_group`
