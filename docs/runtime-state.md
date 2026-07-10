# Runtime State — NLMYTGen

Project-State-ID: supervisor-only-control-boundary-restored-v1
State-Revision: 2026-07-10.4
Updated: 2026-07-10 JST
Product-State: episode-002-ymm4-observation-ready
Product-Gate: five-point-ymm4-import-observation
Recommended-Next: verify-ymm4-five-observations
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
- **Product scope**: no Episode 002 artifact, import candidate, adapter contract,
  real-input receipt, default-branch integration, or publication setting was
  changed in this correction.
- **Cross-device resume**: after the normal three-document read budget, use the
  top `現在の別端末再開ハンドオフ` section in `docs/project-context.md`. It names
  the tracked branch, clean/parity check, current product facts, and exact
  return path without recreating a repository-side session prompt.

## Product Position

- The Episode 002 operator package, Japanese preview, five-point observation
  sheet, machine readback, and nine-cue import CSV candidate are present.
- Package generation and focused product validation are proven. The latest
  product regression covered 16 tests for observation readback, import
  readiness, local edit execution, and real-input readiness.
- Actual YMM4 import has not happened. Cue count, VoiceItem creation, subtitle
  creation, timing order, and placeholder boundaries remain unobserved.
- No verified Episode 002 source/transcript bundle has been supplied, so sample
  input has not been replaced by real material.
- A 2026-07-10 full-suite audit reported 22 known failures and tracked-fixture
  side effects. Those writes were restored; full-suite repair remains a
  separate Integrity / Triage task and is not the product gate.

## Current Decision Menu

| Entry | Resolves | What becomes possible |
| --- | --- | --- |
| **Verify — recommended** | Five YMM4 observations are still unknown | Decide from evidence whether the import adapter needs a correction |
| **Advance** | There is no verified real source/transcript | Validate a supplied receipt and replace the diagnostic sample input |
| **Integrate** | Feature-branch work is not yet reconciled with the default branch | Audit the branch/default diff and choose the safe integration path |

Explore is review debt, not the next product entry. Use a product Direction
Check only when a future visible layout, language, color/type, content, or
animation decision would otherwise be expensive to reverse. Excise is not a
current entry. Default-branch integration and optional GitHub Pages publication
are separate decisions; this public repository already exposes tracked Markdown.

## Human or External Decision Points

- **YMM4 verification**: a human operator imports the tracked CSV and returns
  the five bounded observations. The assistant can then read back and repair
  only evidence-backed adapter defects.
- **Real-input route**: a verified source/transcript, provenance/rights note,
  stable identity, and cue alignment are required before real replacement.
- **Integration**: inspect the then-current feature/default diff before merging;
  do not infer approval for default-branch mutation from this state record.

## Product Boundaries

- Do not claim actual import, render/export, production `.ymmp`, real-input
  replacement, rights approval, final thumbnail approval, upload, or public
  readiness without corresponding evidence.
- Do not turn compact state, task routing, or product review guidance back into
  a repository-side session prompt or response gate.

## Maintenance Note

Replace this file as a compact current capsule; put durable decisions and old
handoffs in `docs/project-context.md`, dated verification artifacts, and Git
history. When these shared fields change, update `docs/PROJECT_COCKPIT.md` in
the same commit and invoke the checker explicitly if validation is needed.
