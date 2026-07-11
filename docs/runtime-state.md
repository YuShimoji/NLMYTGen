# Runtime State — NLMYTGen

Project-State-ID: episode-002-verified-local-evidence-operator-batch-ready-v1
State-Revision: 2026-07-12.1
Updated: 2026-07-12 JST
Product-State: episode-002-verified-local-evidence-render-operator-batch-ready
Product-Gate: manual-yymm4-render-batch
Recommended-Next: run-one-yymm4-operator-batch
External-State: public-repo-feature-branch

## Current Slice

- **Verified local evidence bundle ready**: the Episode 002 CSV-gate receipt,
  diagnostic manifest/readback/GUI receipt, runtime capsule, and explicit
  character profile are hash-bound in
  `verified_local_evidence_input_pilot/source_bundle_manifest.json`.
- **Nine supported cues ready**: every Japanese cue has a machine-checked
  claim-ledger entry and authorized JSON pointer. Scene allocation is S1=2,
  S2=2, S3=5; canonical speakers remain `れいむ` 3 / `まりさ` 6.
- **Strict CSV derivation ready**: `canonical_yymm4.csv` and
  `derived_yymm4_import.csv` are headerless two-column, nine-row files with
  identical text/order. Only the speaker column is projected through the
  explicit profile to `ゆっくり霊夢` 3 / `ゆっくり魔理沙` 6.
- **Headless project path ready**: the generator requires a clean operator
  import base matching the new derived CSV, preserves all nine VoiceItem
  objects, and adds one ImageItem plus one independent TextItem for each of
  S1/S2/S3. Labels contain `INTERNAL REVIEW`, `NOT FINAL`, and
  `LOCAL EVIDENCE PILOT`.
- **Historical base classified**: the observed diagnostic import base remains
  structurally valid but contains the old dry-run VoiceItems, so it is not
  rewritten or reused for the new script.
- **One-shot operator gate ready**: the tracked PowerShell batch has five
  manual actions, three-or-fewer return items, explicit stop/prohibited
  conditions, and a passing `-PreflightOnly` path that does not launch YMM4 or
  create local outputs.

## Product Position

- The source is real tracked project evidence, but this is an internal recap
  pilot rather than external editorial input or real-media replacement.
- The existing `4.53.0.9` profile remains environment-specific. Runtime
  preflight may report a different installed version; the operator must stop
  on a mapping dialog, character mismatch, update requirement, or parse error.
- The static project readback proves the generator contract, not an actual
  YMM4-opened project. Actual project and MP4 evidence will be local and
  ignored until the manual batch collector runs.
- No Computer Use, Worker-launched YMM4, render/export, production `.ymmp`,
  external asset fetch, rights/public approval, upload, publication, or
  default-branch integration is part of this achieved state.

## Exact Next Action

From the operator-batch directory, after saving or closing any unrelated YMM4
work, run:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\run_yymm4_operator_batch.ps1`

The user remains the sole GUI operator. Import the instructed derived CSV,
stop on any listed mismatch/error, render once to the exact local target, close
safely, and let the script collect `operator_result.json`.

## Evidence and Access

- Primary operator surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/operator_batch/README_OPERATOR_BATCH.md`
- Source/claim/script/CSV validation:
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/input_validation_readback.json`
- Static project contract:
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/static_project_readback.json`
- Local ignored project target:
  `verified_local_evidence_input_pilot/local_outputs/episode_002_verified_local_evidence_internal_review.local.ymmp`
- Local ignored render target:
  `verified_local_evidence_input_pilot/local_outputs/episode_002_verified_local_evidence_internal_review.mp4`

## Product Boundaries

- Operator-batch-ready does not mean YMM4 import, project reopen, render, or
  MP4 validation has occurred.
- The generated project and render remain internal/non-final and do not become
  production assets through successful collection.
- External editorial source adoption, real-media replacement, creative polish,
  rights/legal approval, final-thumbnail approval, upload/publication,
  default-branch integration, and full-suite Integrity work remain separate.

## Maintenance Note

Replace this file as the current capsule. Keep history in
`docs/project-context.md` and Git. Keep this file within 160 lines and run the
explicit state-sync checker after any shared-field change.
