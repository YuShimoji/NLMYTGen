# Common Foundation Docs Operator Surface Alignment

artifact_id: COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15
title: Common Foundation docs operator surface alignment
purpose: Align the operator-facing docs with the fake/evaluation-only,
readback-only, and no-real-runner boundary wording emitted by
scripts/agent_orchestrator.py after 1906d32.
repo_relative_path: docs/verification/COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15.md
open_command: code docs/verification/COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15.md
generated_from: static docs review, orchestrator boundary wording readback,
repo status checks, and scoped docs-only edits in the dedicated common
foundation audit worktree.
observed_branch: codex/common-foundation-hold-state-audit
observed_HEAD: 1906d32 before this docs alignment diff
relation_to_origin_master: origin/master is an ancestor of HEAD; before this
slice, origin/master..HEAD contained 1906d32 chore(common-foundation): clarify
fake runner operator surface and 0da5594 docs(common-foundation): add
hold-state audit.

## Files Inspected

- AGENTS.md
- docs/REPO_LOCAL_RULES.md
- docs/runtime-state.md
- docs/AGENT_OPERATOR_SURFACE.md
- docs/AGENT_ORCHESTRATION.md
- docs/verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md
- scripts/agent_orchestrator.py

## Files Changed

- docs/AGENT_OPERATOR_SURFACE.md
- docs/AGENT_ORCHESTRATION.md
- docs/verification/COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15.md

No AGENTS.md, scripts/agent_orchestrator.py, tests/test_agent_orchestration.py,
.agent runtime files, or original dirty checkout files were edited.

## Alignment Results

| Surface | Alignment result | Boundary now carried by docs |
| --- | --- | --- |
| docs/AGENT_OPERATOR_SURFACE.md | Example card and boundary text now label the flow as fake/evaluation-only helper output. | Not real Codex execution, not runner permission, not runtime worker operation, and not hold-state authorization to create `.agent` runtime artifacts. |
| docs/AGENT_ORCHESTRATION.md | Orchestrator, dry-run, report evaluation, future real-runner, fake helper, and runtime retention sections now use the same boundary vocabulary. | `--report` is evaluation-only; hold-state preview creates no runtime artifacts; any future real runner needs a separate authorized and audited slice. |
| Examples corrected | The static operator card no longer presents `.agent/reports/*.report.json`, `.agent/needs_human.json`, or `.agent/logs/notify_stub.log` as normal hold-state outputs. | They are runtime-looking local outputs, inspected only when produced by explicit fake/report evaluation, not by hold-state previews. |

## Boundary Summary

1. Fake/evaluation-only wording result: fake and single-fake examples are now
   explicitly named fake/evaluation-only helper surfaces.
2. Report path boundary: `.agent/reports/*.report.json` is described as a
   runtime-looking fake/evaluation-only output path or separately authorized
   real-runner artifact, not normal hold-state output.
3. needs_human boundary: `.agent/needs_human.json` is described as absent from
   hold-state previews and only relevant as a local review stop when created by
   explicit report evaluation.
4. notify_stub boundary: `notify_stub.log` is described as a local stub log,
   not external notification.
5. Eligibility wording boundary: `safe_to_start_real_runner` remains
   eligibility/readback only and not execution permission.
6. Status signal boundary: status object signals remain input evidence and do
   not grant runner permission.
7. Future runner boundary: docs now say any future real runner requires a
   separately authorized and audited slice covering subprocess launch, stdin
   handling, timeout, cancellation, report artifact containment, notification
   policy, gate authority, and operator card readback boundaries.
8. Real runner implementation remains No.

## Remaining Warnings

- The docs still include runtime-looking paths as examples because those paths
  are part of the existing fake/report helper vocabulary. They are now bounded
  in-place as fake/evaluation-only or future separately authorized outputs.
- docs/AGENT_ORCHESTRATION.md still contains a manual cleanup command for local
  runtime artifacts. It is now described as post fake/report evaluation cleanup,
  not a docs-only or hold-state slice step.
- Existing adapter/prohibition references to repo-specific domains remain in
  docs/AGENT_ORCHESTRATION.md as boundary text. This slice did not add or open
  any cross-lane work.

## Blockers

None found. No code change was required.

## Validation Commands

- `pwd`
- `git status --short --branch`
- `git status --porcelain=v1`
- `git branch --show-current`
- `git log -5 --oneline`
- `git fetch --prune origin`
- `git merge-base --is-ancestor origin/master HEAD`
- `git log --oneline origin/master..HEAD`
- `git diff --check`
- `.agent/reports`, `.agent/logs`, and `.agent/needs_human.json` checks
- `git diff -- AGENTS.md scripts/agent_orchestrator.py tests/test_agent_orchestration.py`
- `rg -n "fake/evaluation-only|evaluation-only|hold-state preview|not runner permission|not execution permission|runtime-looking|notify_stub.log|needs_human.json|separately authorized and audited" docs/AGENT_OPERATOR_SURFACE.md docs/AGENT_ORCHESTRATION.md`

## Validation Result

validation_result: pass before commit

- `git diff --check`: pass
- `git status --porcelain=v1`: only the two allowed docs modified and this
  active artifact untracked before staging
- AGENTS.md, scripts/agent_orchestrator.py, and tests/test_agent_orchestration.py:
  no diff
- `.agent/reports/`: `.gitkeep` only
- `.agent/logs/`: `.gitkeep` only
- `.agent/needs_human.json`: absent
- `.venv` and `.pytest_cache`: absent
- tests: not run; this is a docs-only slice and no safe docs lint/check was
  required by repo-local rules
- push: not performed

## Review Status

review_status: ready_for_supervising_ai_review_after_commit

## Next Action

next_action: Commit this docs-only alignment slice, then hold. If common
foundation resumes later, prefer a supervising review of the three verification
artifacts before opening any new implementation lane.
