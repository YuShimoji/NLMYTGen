# BN-R0: Baseball Foundation Rebaseline

This report records the Baseball sidequest foundation state before BN-05 manual
preview work or any new feature implementation. It is an inventory, review
route, and reporting-format baseline. It does not promote the branch to
`master`, does not change the mainline `runtime-state.md` next action, and does
not claim production, render, rights, publishing, or creative acceptance.

## Single Review Procedure

1. From the repository root, run `start .\index.md`. That root page is the
   single Markdown entry; if a browser docs tree is needed, use the MkDocs
   command block already printed there and open the same report from the
   Overview nav.
2. Open this report:
   `docs/baseball/FOUNDATION_REBASELINE_2026-06-15.md`.
3. Check the navigation screenshot:
   `samples/_probe/baseball/foundation_rebaseline_2026-06-15/baseball_foundation_rebaseline_docs_view.png`.
4. Check the current Baseball manifests and readbacks:
   `samples/_probe/baseball/static/baseball_pitch_event_p05_manifest.json`,
   `samples/_probe/baseball/static/baseball_pitch_event_p05_readback.json`,
   `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_manifest.json`,
   `samples/_probe/baseball/animation/baseball_pitch_event_p05_animation_readback.json`,
   `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_manifest.json`,
   and
   `samples/_probe/baseball/placement/baseball_pitch_event_p05_placement_proof_readback.json`.
   The gap report is the "Remaining Uncertainty" section in this file.
5. Check the consumed BN-05 manual preview evidence in
   `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png`,
   `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_review.json`,
   and the "Manual Visual Proof Captured" section of
   `docs/PROGRESS_SCREENSHOT_INDEX.md`.

## Inventory

| Area | Current evidence | State | Still unverified |
| --- | --- | --- | --- |
| Branch / commit / upstream parity | Initial BN-R0 check on `codex/baseball-bn02-visual-data`, upstream `origin/codex/baseball-bn02-visual-data`, pre-edit HEAD `d7421e5 docs: refine baseball supervisor review prompt`, `HEAD...@{u}=0 0`, clean worktree. | Ready for docs-only rebaseline work on the Baseball branch. | Final BN-R0 commit and push are reported in the completion chat, because this file is part of that commit. |
| BaseballInfoGraphics | `BaseballInfoGraphics/README.md`, `Baseball Infographic.html`, `data.js`, `variants/detailed.jsx`, components, ambient SVG and `LICENSE.csv`. | C detailed design source exists with deterministic query controls and `window.BASEBALL_VISUAL_DATA` override. | It is still a browser design source, not a YMM4 proof or production renderer. |
| `lanes/sports_news` | schemas, sample episode/visual data, screen plan, card templates, BN-03/BN-04/BN-05 handoffs, placement proof builder. | Sports-news Baseball artifact bundle exists and is sample-data based. | Real source replacement, rights gate, news ingestion, RSS, NotebookLM, and publishing are not started here. |
| Docs / index / MkDocs view | Root `index.md`, `docs/index.md`, `docs/PROJECT_OVERVIEW.md`, `docs/PROGRESS_SCREENSHOT_INDEX.md`, `mkdocs.yml`, and this report. | Rebaseline is reachable from the root index and MkDocs Overview nav. | The generated MkDocs staging folder is ignored and must be regenerated locally before browser review. |
| Screenshots / samples / probe artifacts | Static PNG, five animation frames, placement proof `.ymmp`, BN-R0 docs-view screenshot, and BN-05 YMM4 preview screenshot path under `samples/_probe/baseball/`. | Evidence remains lane-local and marked as review/navigation/gate-only proof, not production proof. | BN-04 motion-design acceptance is still separate. |
| YMM4 placement proof | `baseball_pitch_event_p05_placement_proof.ymmp`, proof manifest, proof readback, proof handoff, BN-05 preview screenshot, and review JSON. | Mechanical transport/readback proof passed and the manual YMM4 preview gate is accepted as `accepted_gate_only`. | There is still no render proof, production proof, creative final acceptance, publish readiness, or real episode suitability. |
| BN-06 pipeline contract | `docs/baseball/BASEBALL_PIPELINE_CONTRACT.md` and `samples/_probe/baseball/pipeline/`. | Contract chain is defined for sample-only BaseballDataCapsule, ScriptBeatIR, VisualScenePlan, YMM4Adapter, and ReviewGate ownership. | It does not implement adapter generation, rendering, source replacement, clip export, TTS, thumbnail work, publishing, or creative acceptance. |
| BN-07 Data Capsule fixture | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05.json`, schema, readback, and fixture manifest. | P05 sample facts, pitch deltas, highlight candidates, and stable data refs are validated for ScriptBeatIR and VisualScenePlan consumers. | It does not perform script generation, visual redesign, motion transport, render, production, source replacement, or publishing. |
| Render manifest / readback / gap report | Static manifest/readback and animation manifest/readback exist; placement proof manifest/readback exist. This file records the rebaseline gap report. | Manifest/readback chain is enough to audit current sample artifacts. | No separate production gap report exists because no production or real-source gate has been opened. |
| Branch-local cleanup / docs routing | `git log origin/master..HEAD` shows Baseball commits plus docs routing/cleanup commits, including `25b74f8 docs: prune legacy claude entrypoints`. | Cleanup and docs routing are branch-local sidequest state. | Whether those cleanup/routing changes should move to `master` is an explicit human integration decision, not part of BN-R0. |

## Current Baseball Artifact Chain

| Slice | Path / command surface | Current state | Boundary that still matters |
| --- | --- | --- | --- |
| BN-02 visual data | `src/pipeline/baseball_visual_data.py`, `lanes/sports_news/schemas/baseball_visual_data.schema.json`, `lanes/sports_news/examples/baseball_pitch_event_visual_data_sample.json` | Implemented sample-to-visual-data contract. | Sample-only facts; no real source/provenance replacement. |
| BN-03 static export | `gui/capture_baseball_infographic_static.js`, `samples/_probe/baseball/static/baseball_pitch_event_p05.png` | 1280x720 static PNG, manifest, and readback passed. | Not YMM4 proof, not animation export, not creative acceptance. |
| BN-04 frame sequence | `gui/capture_baseball_infographic_frames.js`, `samples/_probe/baseball/animation/frames/baseball_pitch_event_p05/` | Five 1280x720 frames, manifest, and readback passed; unique visual states are two hashes. | Not codec clip export, not YMM4 placement, not publish gate. |
| BN-05 placement contract/proof | `lanes/sports_news/scripts/build_baseball_yymm4_placement_proof.js`, `samples/_probe/baseball/placement/` | Contract and minimal YMM4 transport proof passed mechanical readback; manual preview screenshot and freeform review are recorded as gate-only acceptance. | Future visual/layout redesign is separate from BN-05 gate closure. |
| BN-06 pipeline contract | `docs/baseball/BASEBALL_PIPELINE_CONTRACT.md`, `samples/_probe/baseball/pipeline/baseball_pipeline_contract_manifest.json` | Defines layer ownership and sample P05 handoff data from fact capsule to script beats, visual scene plan, adapter boundary, and review gate. | Contract-only; not a render proof, not production readiness, not creative final acceptance, and not a publish gate. |
| BN-07 Data Capsule fixture | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05_fixture_manifest.json` | Validates stable `fact_` refs, pitch sequence consistency, P04 to P05 delta, highlight candidates, synthetic provenance, and downstream reference resolution. | Data fixture only; not ScriptBeatIR generation, visual design V2, YMM4 motion transport, render proof, production readiness, or publish readiness. |

## Verification Commands And BN-R0 Start Results

These commands were run before writing BN-R0 files:

```powershell
git fetch --all --prune
git checkout codex/baseball-bn02-visual-data
git pull --ff-only origin codex/baseball-bn02-visual-data
git status --short --branch
git status --porcelain=v1
git rev-list --left-right --count "HEAD...@{u}"
git log -8 --oneline
git diff --check
```

Observed result: the branch was already up to date, porcelain output was empty,
upstream parity was `0 0`, latest pre-edit commit was `d7421e5`, and
`git diff --check` passed.

BN-R0 verification after this file is added should run:

```powershell
python tools\generate-doc-nav.py --format mkdocs --prepare-docs-dir .mkdocs-docs --write mkdocs.yml --force
python -m mkdocs build
git diff --check
git status --short --branch
git status --porcelain=v1
git rev-list --left-right --count "HEAD...@{u}"
```

## Baseball Codex Completion Report Shape

Use this shape for Baseball sidequest completion reports after BN-R0. Fill each
section with concrete facts; do not leave a heading with only a thin placeholder
line.

1. Summary
2. Branch / Commit / Push state
3. Changed files
4. Single review procedure
5. Screenshots
6. Artifacts / readbacks / gap report
7. Verification results
8. What did not change
9. Remaining uncertainty
10. Human decision required
11. 監修役AIに渡すPrompt（Baseball sidequest報告レビュー用。実装指示ではありません）
12. 次Codex用Prompt（Baseball sidequest実装再開用） only when a future implementation prompt is actually needed

The supervisor prompt label above is for report review only. It is not an
implementation restart prompt. The reusable supervisor prompt owner remains
`docs/BASEBALL_SUPERVISOR_REVIEW_PROMPT.md`.

## Remaining Uncertainty

| Uncertainty | Why it matters | Where to resolve it | Next enabled move |
| --- | --- | --- | --- |
| BN-05 manual YMM4 preview is accepted gate-only | Screenshot and freeform review close crop/readability/layer-overlap uncertainty for this QA gate only. | `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_screenshot.png` and `samples/_probe/baseball/placement/baseball_pitch_event_p05_yymm4_preview_review.json`. | Treat future visual/layout redesign as a separate later decision. |
| BN-06 adapter behavior is only contracted | The layer boundary now says what the adapter may consume and emit, but no generated `.ymmp` readback is added by BN-06. | `docs/baseball/BASEBALL_PIPELINE_CONTRACT.md` and `samples/_probe/baseball/pipeline/`. | Choose a separate follow-up for adapter readback design or motion export proof. |
| BN-07 fixture does not author the script | The Data Capsule now protects factual refs, but narrative emphasis remains a consumer decision. | `samples/_probe/baseball/pipeline/baseball_data_capsule_p05_readback.json`. | Open BN-08 as ScriptBeatIR linkage against validated refs. |
| BN-04 frames have not been accepted as motion design | Frame hashes prove deterministic capture, but not whether the pitch update communicates enough value. | `samples/_probe/baseball/animation/frames/baseball_pitch_event_p05/`. | Decide whether clip export is worth building. |
| Real source/provenance replacement is unopened | Current sample facts are intentionally fake/sample data. | `lanes/sports_news/schemas/` and future source/right manifests. | Plan real episode ingest only after sample route review is accepted. |
| Branch-local docs cleanup is not mainline policy | This branch contains docs routing and cleanup changes not automatically present on `origin/master`. | `docs/BRANCH_THREAD_SUPERVISION.md` and `git diff --name-status origin/master...HEAD`. | Make a separate human integration decision, or keep the changes sidequest-local. |

## What BN-R0 Does Not Change

BN-R0 did not implement BN-05 placement tuning, clip export, BN-06, BN-07,
RSS, NotebookLM, source collection, publishing, YouTube upload, or G-27 work,
and did not merge, cherry-pick, or push anything to `master`. BN-06 later adds
only the sample pipeline contract and does not change those production,
publishing, source, or mainline boundaries. BN-07 later strengthens only the
sample Data Capsule fixture and stable data refs.
