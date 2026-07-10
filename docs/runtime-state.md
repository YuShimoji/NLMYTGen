# Runtime State — NLMYTGen

Project-State-ID: workflow-velocity-and-current-state-v1
State-Revision: 2026-07-10.1
Updated: 2026-07-10 JST
Product-State: episode-002-ymm4-observation-ready
Product-Gate: five-point-ymm4-import-observation
Recommended-Next: verify-ymm4-five-observations
External-State: tracked-branch-mirror-pages-unpublished

## Current Slice

- **Development slice**: `workflow-velocity-and-current-state-v1` on
  `codex/workflow-velocity-and-current-state-v1`, based on `99477a0`.
- **State**: completed locally after remote refresh, development-environment
  repair, workflow redesign, focused validation, and current-state sync.
- **Why this slice exists**: the supervisor-AI to developer-AI loop had become
  slow because advisory quality rules behaved as hard stops, implementation
  prompts were split into small steps, current state was copied into several
  stale documents, and visual direction was reviewed after high-cost builds.
- **Primary result**: normal repo-local work now runs as one outcome-sized
  slice. Reversible implementation, related fixes, narrow validation, status
  sync, commit, and push remain assistant-owned. Only a real direction change
  or a high-impact boundary crosses a decision gate.
- **Tracked external-reading mirror**: `docs/PROJECT_COCKPIT.md`. It carries the
  same shared state fields and is linked from the repository README. After this
  branch is pushed, repository viewers can read it on GitHub if visibility
  permits; a stable Pages/Wiki URL is not yet configured.
- **Freshness check**: `uv run python scripts/check_project_state_sync.py`.

## Product Position

- **Episode 002 YMM4 observation readiness** is the latest completed product
  artifact. The operator package, Japanese preview, five-point observation
  sheet, machine readback, and nine-cue import CSV candidate are present.
- **What is proven**: package generation and validation. The latest focused
  regression passed 16 tests covering observation readback, import readiness,
  local edit execution, and real-input readiness; the workflow guard and state
  sync checks passed another 59 tests.
- **Full-suite debt**: a 2026-07-10 `uv run pytest` audit reported 22 failures
  and rewrote 39 tracked generated fixtures. Those writes were restored.
  Full-suite cleanup belongs to an explicit Integrity /
  Triage slice; it is not allowed to block the focused green product path.
- **What is not proven**: an actual YMM4 import has not been attempted in this
  slice; observed cue count remains zero. VoiceItem creation, subtitle creation,
  timing order, and placeholder boundaries therefore remain unobserved.
- **Real material**: no verified Episode 002 source/transcript bundle has been
  supplied, so real-input replacement has not happened.

## Assistant Can Continue Without Asking

- Repair code, docs, tests, and status mirrors that stay inside an approved
  slice and do not change a product or external contract.
- Batch related corrections and proportional validation instead of requesting
  one Prompt per mechanical step.
- For a new visible direction, prepare two or three low-cost alternatives and
  a recommendation before committing to a high-fidelity implementation.

## Human or External Decision Points

- **YMM4 verification**: a human operator may import the tracked CSV and return
  the five observations in
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_observation_readback_pack/manual_ymm4_observation_readback.md`.
- **Real-input route**: a verified local source/transcript bundle is required
  before real content can replace the sample diagnostic input.
- **Stable external status URL**: GitHub Pages or Wiki publication requires a
  repository-visibility and promotion-policy decision. No external publication
  is performed by this slice.

## Hard Gates

- Stop for destructive operations, dependency additions, DB/auth/API contract
  changes, external publication or rights/payment actions, conflicting product
  specifications, or a creative decision that changes the approved direction.
- Do not claim actual YMM4 import, render/export, production `.ymmp`, real-input
  replacement, rights approval, final thumbnail approval, upload, or public
  readiness without the corresponding evidence.
- Current non-goals are not hard gates. Work that remains inside the approved,
  reversible slice should continue to local verification and Git follow-through.

## Maintenance Contract

Replace this file as a compact current capsule; do not prepend handoff history.
Durable decisions and old handoffs belong in `docs/project-context.md`, dated
verification artifacts, and Git history. Keep this file at or below 160 lines,
update `docs/PROJECT_COCKPIT.md` in the same slice, and run the freshness check
before closeout.
