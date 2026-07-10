# Newsroom Handoff Supervision Gate - 2026-06-09

## Classification

- `supervision_gate / cross-repo-boundary-review`
- Final decision: `request_authority / no-op_wait`
- Purpose: Preserve the refreshed Newsroom handoff review in-project so another terminal can resume without relying on chat history.

## Sync State

NLMYTGen:

- Repo: `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen`
- Branch: `master`
- Pre-handoff sync base: `39dd9ad docs: seal single fake flow handoff`
- Upstream parity before docs-only handoff: `HEAD...@{u}=0 0`
- Tracked working tree before docs-only handoff: clean
- Known untracked residue left untouched:
  - `.claude/worktrees/`
  - `samples/2026-05-16.ymmp`

Newsroom, checked read-only:

- Repo: `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline`
- Branch/head supplied and verified: `main` / `1296b8e`
- Upstream parity: `HEAD...origin/main=0 0`
- Export: `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853`

## Docs Read

NLMYTGen authority:

- `AGENTS.md`
- `README.md`
- `docs/REPO_LOCAL_RULES.md`
- `docs/runtime-state.md`
- `docs/project-context.md`
- `docs/FEATURE_REGISTRY.md`
- `docs/INVARIANTS.md`
- `docs/USER_COPYPASTE_BLOCKS.md`

G-28 authority:

- `docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md`
- `docs/verification/G28-GAME-MECHANICS-YMM4-SAVED-CARRIER-REVIEW-CONDITIONS-2026-06-08.md`
- `docs/verification/G28-GAME-MECHANICS-DIAGRAM-SEMANTICS-NOTE-2026-06-05.md`
- `docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md`

Newsroom export files inspected read-only:

- `export_manifest.json`
- `script.csv`
- `script_ir.json`
- `visual_ir.json`
- `visual_plan.md`
- `source_list.md`
- `quote_manifest.yml`
- `asset_manifest.yml`
- `ymm4_notes.md`

## Readback

Newsroom export readback:

- `episode_id`: `episode_756343df9853`
- `story_id`: `story_20260603_503c39418f15862d`
- `script_id`: `script_d2a46430e084`
- `packet_id`: `packet_20260603_2de578dcd4b0`
- `warnings`: `[]`
- `deferred`: `[]`
- `source_list.md`: primary Microsoft Blog, critical NIST
- `ymm4_notes.md`: speaker `ナレーター`, no warnings, `human_required=0`

## Branch Decision

The Newsroom handoff is valid candidate downstream input, but it is not active NLMYTGen authority yet.

Current active NLMYTGen lane:

- G-28 `game_mechanics_explanation` diagnostic reviewability
- Later scoped YMM4-saved carrier review conditions
- Diagnostic-only boundary remains active:
  - `diagnostic_only=true`
  - `production_candidate=false`
  - no Source-Footage
  - no `.ymmp` generation
  - no render
  - no production timing
  - no creative final acceptance

Reason for `request_authority / no-op_wait`:

- The export exists and is readable, but no human has chosen copy-in versus read-only reference for NLMYTGen.
- No human has explicitly paused or superseded the current G-28 game_mechanics lane.
- Newsroom export inspect/readback is upstream candidate evidence, not NLMYTGen production proof.
- There is no concrete downstream failure requiring a targeted fix.

## Required Human Input

To start Newsroom downstream intake, the user must choose:

1. Whether NLMYTGen should copy selected Newsroom handoff data into tracked docs/artifacts, or only reference the Newsroom export by read-only absolute path.
2. Whether the current G-28 game_mechanics lane should be paused or superseded by Newsroom downstream intake.
3. The first authorized NLMYTGen output shape:
   - docs-only intake plan
   - manifest-to-adapter mapping
   - adapter implementation slice

Files and items to inspect when making that decision:

- Newsroom export folder:
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853`
- Key manifest:
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\export_manifest.json`
- Script handoff:
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\script.csv`
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\script_ir.json`
- Visual handoff:
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\visual_ir.json`
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\visual_plan.md`
- Source/rights review:
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\source_list.md`
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\quote_manifest.yml`
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\asset_manifest.yml`
- YMM4 notes:
  - `C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853\ymm4_notes.md`

Recommended human-side procedure:

1. Open `export_manifest.json` and confirm the episode/story/script/packet IDs match the intended episode.
2. Open `source_list.md`, `quote_manifest.yml`, and `asset_manifest.yml`; confirm the export contains no raw article body, private data, or copyright-unclear tracked material that NLMYTGen should copy.
3. Decide copy-in versus read-only path reference.
4. Decide whether G-28 game_mechanics remains active or is paused/superseded.
5. Provide one explicit next seed: docs-only intake plan, manifest mapping, or adapter implementation.

## Runtime Artifact Handling

- Newsroom runtime/export/proof files were inspected read-only.
- No Newsroom export file was copied into NLMYTGen.
- No runtime DB/export/proof/screenshot was staged.
- Existing NLMYTGen local residue stayed untouched:
  - `.claude/worktrees/`
  - `samples/2026-05-16.ymmp`

## Prohibited From This Gate

- Re-implementing Newsroom M7-D source-role backfill
- Auto-adopting seeds as approved stories
- Auto-adopting source candidates
- Broad crawling, social trend scraping, Inoreader OAuth, or NotebookLM API automation
- Tracking raw article body, private data, or copyright-unclear text
- Bringing YMM4 geometry, subtitle placement, overlay proof, full `.ymmp`, publishing, or render work into Newsroom or this handoff gate
- Adding NLMYTGen subprocess/path/pip/shared dependency on Newsroom
- Committing runtime DB/export/proof/screenshots
- Creating or expanding `AGENTS.md`

## Next Prompt

The original restart text was legacy `docs/USER_COPYPASTE_BLOCKS.md` SECTION 21.
It was removed from the active prompt file on 2026-07-10; recover it only with
`git show 99477a0:docs/USER_COPYPASTE_BLOCKS.md`. This historical gate still
records that the operator was to stop at `request_authority / no-op_wait` unless
the user supplied the copy/read-only decision and lane-supersession decision.
