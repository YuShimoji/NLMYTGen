# Runtime State — NLMYTGen

Project-State-ID: supervisor-only-control-boundary-restored-v1
State-Revision: 2026-07-10.5
Updated: 2026-07-10 JST
Product-State: episode-002-ymm4-observation-completed-with-adapter-gap
Product-Gate: evidence-backed-adapter-correction
Recommended-Next: correct-speaker-mapping-and-placeholder-lane-gap
External-State: public-repo-feature-branch

## Current Slice

- **Completed boundary correction**: repository-side Supervisor Prompt storage,
  generic Worker authority, response-quality lint, and the automatic state-sync
  Stop hook have been removed. A self-contained prompt supplied by the Web
  supervisor is the session execution authority.
- **Repository role**: this file and `docs/PROJECT_COCKPIT.md` persist compact
  project state for navigation. `docs/THREAD_REGISTRY.md` routes task history,
  and `docs/PROJECT_PIPELINE.mmd` maps the product path. None is a substitute
  prompt or a Worker control plane.
- **Explicit integrity tool**: `scripts/check_project_state_sync.py` remains an
  opt-in checker for the shared runtime/cockpit fields. It is not invoked by a
  Stop hook and has no retry/fail-open behavior.
- **Product scope**: the tracked nine-row diagnostic CSV was imported in YMM4
  `4.53.0.9`, observed, closed without saving, and persisted as an evidence
  receipt plus regenerated readback. No render/export, production `.ymmp`, real
  input, rights/public decision, default-branch integration, or upload changed.
- **Cross-device resume**: after the normal three-document read budget, use the
  top `現在の別端末再開ハンドオフ` section in `docs/project-context.md`. It names
  the tracked branch, clean/parity check, current product facts, and exact
  return path without recreating a repository-side session prompt.

## Product Position

- The Episode 002 nine-row CSV produced nine ordered VoiceItems. Row order
  remained `csv_row_1` through `csv_row_9`, corresponding to S1 -> S2 -> S3;
  no missing, duplicate, or reordered cue was observed.
- Linked subtitle text matched the speaker/cue after manual character mapping:
  `れいむ` -> `ゆっくり霊夢` and `まりさ` -> `ゆっくり魔理沙`. Automatic
  binding was not proven and the initial `まりさ` default was incorrect.
- Timing order remained intact, but YMM4 recalculated the provisional
  four-second blocks to 2790 frames / 46.50 seconds at 60 fps.
- The result is `partial`: VoiceItem/subtitle lanes appeared, but the expected
  ImageItem/TextItem placeholder scene lanes did not. Diagnostic text retained
  its dry-run boundary and did not claim final/public readiness.
- Receipt-driven regeneration and focused product validation are proven. The
  current regression covers 24 tests for observation readback, import
  readiness, local edit execution, and real-input readiness.
- No verified Episode 002 source/transcript bundle has been supplied, so sample
  input has not been replaced by real material.
- A 2026-07-10 full-suite audit reported 22 known failures and tracked-fixture
  side effects. Those writes were restored; full-suite repair remains a
  separate Integrity / Triage task and is not the product gate.

## Current Decision Menu

| Entry | Resolves | What becomes possible |
| --- | --- | --- |
| **Correct — recommended** | Speaker aliases require manual mapping and placeholder scene lanes are absent | Repair only the two evidence-backed adapter gaps, then repeat the bounded observation |
| **Advance** | There is no verified real source/transcript | Validate a supplied receipt and replace the diagnostic sample input |
| **Integrate** | Feature-branch work is not yet reconciled with the default branch | Audit the branch/default diff and choose the safe integration path |

Explore is review debt, not the next product entry. Use a product Direction
Check only when a future visible layout, language, color/type, content, or
animation decision would otherwise be expensive to reverse. Excise is not a
current entry. Default-branch integration and optional GitHub Pages publication
are separate decisions; this public repository already exposes tracked Markdown.

## Human or External Decision Points

- **Adapter correction**: use the recorded five-point observation to correct
  automatic speaker binding and ImageItem/TextItem placeholder-lane generation
  without widening into render, production `.ymmp`, or visual acceptance.
- **Real-input route**: a verified source/transcript, provenance/rights note,
  stable identity, and cue alignment are required before real replacement.
- **Integration**: inspect the then-current feature/default diff before merging;
  do not infer approval for default-branch mutation from this state record.

## Product Boundaries

- Actual import is proven only for this bounded diagnostic run. Do not claim
  render/export, production `.ymmp`, real-input replacement, rights approval,
  final thumbnail approval, upload, or public readiness without corresponding
  evidence.
- Do not turn compact state, task routing, or product review guidance back into
  a repository-side session prompt or response gate.

## Maintenance Note

Replace this file as a compact current capsule; put durable decisions and old
handoffs in `docs/project-context.md`, dated verification artifacts, and Git
history. When these shared fields change, update `docs/PROJECT_COCKPIT.md` in
the same commit and invoke the checker explicitly if validation is needed.
