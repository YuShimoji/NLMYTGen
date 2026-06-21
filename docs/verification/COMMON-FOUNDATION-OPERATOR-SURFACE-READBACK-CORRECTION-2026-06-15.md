# Common Foundation Operator Surface Readback Correction

artifact_id: COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15
title: Common Foundation operator surface readback correction
purpose: Confirm and correct operator-facing wording so fake helpers, report
evaluation, dry-run previews, runtime-looking paths, and eligibility signals are
not read as real runner permission.
repo_relative_path: docs/verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md
open_command: code docs/verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md
generated_from: static repo review, targeted grep readback, targeted
agent_orchestrator tests, and local git status checks in the dedicated
common-foundation audit worktree.
observed_branch: codex/common-foundation-hold-state-audit
observed_HEAD: 0da5594 before this correction commit; this artifact documents
the pending correction diff on top of that commit.
relation_to_origin_master: origin/master is an ancestor of HEAD; before this
slice, origin/master..HEAD contained only 0da5594 docs(common-foundation): add
hold-state audit.

## Files Inspected

- AGENTS.md
- docs/REPO_LOCAL_RULES.md
- docs/runtime-state.md
- docs/verification/COMMON-FOUNDATION-HOLD-STATE-AUDIT-2026-06-15.md
- docs/verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md
- docs/verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md
- docs/AGENT_OPERATOR_SURFACE.md
- docs/AGENT_ORCHESTRATION.md
- scripts/agent_orchestrator.py
- tests/test_agent_orchestration.py

## Files Changed

- scripts/agent_orchestrator.py
- tests/test_agent_orchestration.py
- docs/verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md

No original checkout files were edited. No AGENTS.md, repo-local rule, or
runtime-state files were changed.

## Readback Results

| Surface | Correction / observed boundary | Current status |
| --- | --- | --- |
| Fake runner wording | Synthetic report summaries now say `fake/evaluation-only runner ... synthetic report`, and fake helper results expose `operator_boundary.operator_label=fake/evaluation-only helper`. | Corrected in script and tests. |
| `--report` evaluation path | `run()` now attaches `report_evaluation_boundary` that says report mode is evaluation-only, not real Codex execution, not runner permission, not a runtime worker loop, and not an external notification path. | Corrected in script and tests. |
| `.agent/reports` readback | Pre-execution dry-run card now says `.agent/reports/*.report.json` is a runtime-looking output and only a planned path for that preview. | Corrected in preview rendering and tests. |
| `.agent/needs_human.json` boundary | Pre-execution dry-run card now says the file is not created or authorized by the preview. Report mode may still call the local notify stub only after an existing report gates as needs_human. | Corrected for preview/report readback; existing notify behavior unchanged. |
| `notify_stub.log` boundary | Pre-execution dry-run card now says no `notify_stub.log` is created and no external notification is sent. Report boundary says it is not an external notification path. | Corrected in preview/report readback and tests. |
| Status signal vs execution permission | Existing preflight card wording already says `safe_to_start_real_runner` is eligibility only, not execution permission. This slice keeps that boundary visible and adds broader operator boundary metadata. | No blocker found. |
| `safe_to_start_real_runner` eligibility wording | Existing tests already cover readable card output such as `Real-runner start eligibility: ... (not execution permission)` and dry-run preview output. | No blocker found. |

## Remaining Warnings

- docs/AGENT_OPERATOR_SURFACE.md and docs/AGENT_ORCHESTRATION.md still contain
  examples that mention `.agent/reports/...`, `.agent/needs_human.json`, and
  `.agent/logs/notify_stub.log`. They are mostly bounded as local/stub behavior,
  but they can still be visually misread as runtime authorization when skimmed.
- Existing test-only fake helper behavior can write configured repo-local
  synthetic outputs when explicitly invoked by tests. This is now labeled as
  fake/evaluation-only and not runner permission, but the helper itself remains
  present for test coverage.
- No real runner implementation was added. No subprocess runner, stdin piping,
  runtime loop, external notification service, or production candidate path was
  added.

## Validation Commands

- `git status --short --branch`
- `git merge-base --is-ancestor origin/master HEAD`
- `git log --oneline origin/master..HEAD`
- `rg -n "operator_boundary|pre-execution dry-run preview|fake/evaluation-only|report_evaluation_boundary|No Codex execution|--report evaluation" scripts/agent_orchestrator.py tests/test_agent_orchestration.py`
- `rg -n "safe_to_start_real_runner|execution permission|eligible|status signal|needs_human|notify_stub|fake runner|fake/evaluation|report evaluation|pre-execution" scripts/agent_orchestrator.py docs/AGENT_OPERATOR_SURFACE.md docs/AGENT_ORCHESTRATION.md tests/test_agent_orchestration.py`
- `$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest tests/test_agent_orchestration.py -k "fake_runner_pass_report_flows_through_gate_without_notify or single_fake_execution_flow_pass_builds_plan_preflights_runs_gate_without_notify or orchestrator_report_mode_labels_evaluation_only_boundary or pre_execution_dry_run_preview_renders_plan_preflight_card_without_artifacts or orchestrator_without_dry_run_or_report_still_cannot_execute_codex" -p no:cacheprovider`

## Validation Result

Targeted pytest result: 5 passed, 99 deselected.

Post-artifact static validation result: pass.

- `git diff --check`: pass
- `git status --porcelain=v1`: exactly the two implementation files modified
  and this artifact untracked before staging
- `.agent/reports/`: `.gitkeep` only
- `.agent/logs/`: `.gitkeep` only
- `.agent/needs_human.json`: absent
- `.venv` and `.pytest_cache`: absent after validation cleanup
- AGENTS.md, docs/REPO_LOCAL_RULES.md, and docs/runtime-state.md: no diff
- push: not performed

## Review Status

review_status: ready_for_supervising_ai_review_after_commit

The implementation corrects operator-surface wording and machine-readable
boundary metadata without granting runner permission. The real runner remains
No.

## Next Action

next_action: Run final static validation, commit this correction slice, then
hold. If a follow-up slice is approved, the most useful next slice is a
docs-only alignment of docs/AGENT_OPERATOR_SURFACE.md and
docs/AGENT_ORCHESTRATION.md so their examples carry the same readback boundary
language now present in the orchestrator output.
