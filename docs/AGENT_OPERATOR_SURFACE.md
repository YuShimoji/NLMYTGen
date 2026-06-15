# Agent Operator Surface

This page defines the smallest human-readable review surface for the current
common foundation fake/evaluation-only helper flow and standalone preflight
preview. It is a review card, not an execution entry point.

The card exists so an operator can answer these questions without reading test
output or Python implementation:

- what was attempted
- which worker and scenario were used
- whether this is a deterministic example or a real result card
- whether preflight passed
- whether the fake/evaluation-only helper was invoked
- what the gate decided
- whether human action is required
- what decision the human should make
- which files should be inspected
- what is explicitly outside the run
- what the next safe action is

## How to use it

Open this document for the static example, or print the deterministic example:

```powershell
uv run python scripts/agent_operator_surface.py --example
```

To render a card from an existing repo-local orchestration flow JSON:

```powershell
uv run python scripts/agent_operator_surface.py path\to\flow-result.json
```

To render a deterministic raw preflight preview card:

```powershell
uv run python scripts/agent_operator_surface.py --preflight-example
```

To print the current pre-execution dry-run preview, use the orchestrator. This
builds the plan, runs preflight in preview mode, embeds the raw preflight card,
and stops:

```powershell
uv run python scripts/agent_orchestrator.py --worker audit --pre-execution-dry-run --repo-status-clean
```

The script only reads a JSON file inside this repo and prints Markdown. It does
not run Codex, does not run the fake/evaluation-only helper, does not create a
subprocess, does not pipe stdin, does not start a worker loop, and does not send
external notifications.

The preflight preview adapter takes an already-created preflight result and
renders it as a read-only Markdown card. It shows the preflight status, mode,
worker, review-only allow decision, `safe_to_start_real_runner` as eligibility
only, reasons, inspected paths, authority summary, execution boundary, and
human next action. It does not wrap a raw preflight result into a runner flow,
does not validate a worker report, and does not authorize real execution by
itself.

The orchestrator's pre-execution dry-run preview reuses that same card inside a
larger Markdown review surface with selected worker, prompt source, schema path,
planned report path, working directory, timeout, argv preview, repo status
summary, authority summary, and an explicit stop boundary. In that outer
surface, the report path is labeled as planned only, the repo-status source is
labeled as operator-provided and not checked by the CLI, and the embedded card
is labeled as the raw preflight result. It still does not write runtime
artifacts or evaluate a worker report from a real run.

## Example Card

```markdown
# NLMYTGen Operator Review Card

## Summary
- Card mode: example
- Boundary label: fake/evaluation-only helper; not real Codex execution
- Plain-language result: Synthetic audit-helper output reached a human-review stop.
- Human action required: yes
- Decision to make: Inspect only if these paths came from an explicit fake/report evaluation result, then choose whether to summarize, request a fix, or stop.
- This is a deterministic sample card; it did not run Codex, grant runner permission, or authorize hold-state runtime artifacts.

## Status
- Flow status: completed
- Preflight check: passed
- Fake/evaluation-only helper invoked: yes
- Gate result: needs human review
- Human action required: yes

## What happened
- Attempted work: Review an existing fake/evaluation-only helper result
- Worker / scenario: Audit worker / Needs human review
- Prompt: .agent/prompt_catalog/audit.md
- Schema: .agent/schemas/worker_report.schema.json
- Planned report: .agent/reports/example-audit.report.json
- Report path boundary: runtime-looking fake/evaluation-only output path; not a normal authorized hold-state artifact
- Synthetic helper report written: yes, in this deterministic fake/evaluation-only example only
- Synthetic helper exit: 0
- Synthetic helper timed out: no
- Synthetic helper error kind: none

## Human decision needed
- Human action required: yes. Decide whether to continue with the suggested next worker, send the result back for a fix, or keep the evaluation stopped for more human input.
- Decision to make: Inspect only if these paths came from an explicit fake/report evaluation result, then choose whether to summarize, request a fix, or stop.
- Report note: Review the example report shape and decide whether a future separately authorized worker result should be summarized, fixed, or held for more human input.
- Gate reasons:
- status:needs_human
- Preflight reasons:
- none

## Files to inspect
- Note: Example paths only; this example command does not check whether these files exist or create them.
- Boundary: `.agent/reports/*.report.json`, `.agent/needs_human.json`, and `.agent/logs/notify_stub.log` are runtime-looking local outputs. They are not created or authorized by hold-state previews.
- .agent/prompt_catalog/audit.md
- .agent/schemas/worker_report.schema.json
- .agent/reports/example-audit.report.json
- .agent/needs_human.json
- .agent/logs/notify_stub.log

## Safety boundary
- Real Codex execution: not started
- Real subprocess runner: not started
- Codex stdin piping: not implemented
- Runtime worker loop: not implemented
- External notification service: not implemented
- Local notify stub: local stub log only; not external notification
- .agent/reports/*.report.json: runtime-looking fake/evaluation-only output path; not normal hold-state output
- .agent/needs_human.json: not created or authorized by hold-state previews
- .agent/logs/notify_stub.log: local stub log only after needs_human in fake/report evaluation

## Next safe actions
- If this came from an explicit fake/report evaluation result, inspect the report and local needs-human stub paths listed above.
- Answer the human question or choose the next worker after inspecting the gate reasons.
- Treat this as a local review stop, not a production or release approval.

## Raw identifiers
- mode: single_fake_execution_flow_for_test
- worker: audit
- scenario: needs_human
- preflight_allowed: yes
- fake_helper_invoked: yes
- gate_decision: needs_human
- report_path: .agent/reports/example-audit.report.json
- operator_boundary: fake/evaluation-only helper; not runner permission
```

## Boundary

The operator card is deliberately downstream of existing outputs. It can make a
flow or preflight preview understandable, but it is not authority to continue
through a gate or start a real runner.

- `needs_human=true` remains a local review stop, not permission to continue
  into real execution.
- `codex_execution_started=false` and `real_subprocess_started=false` remain the
  expected state for the fake and single-fake flow.
- Fake / single-fake flow examples are fake/evaluation-only helper surfaces.
  They are not real Codex execution, not runner permission, not runtime worker
  operation, and not hold-state authorization to create `.agent` runtime
  artifacts.
- A preflight preview with `safe_to_start_real_runner=true` is only a readable
  preview of a preflight result; real execution still belongs to a separate
  authorized runner slice.
- The pre-execution dry-run preview can show an allowed preview result, but it
  stops after stdout and does not consume that result by starting any runner.
- `--repo-status-clean` is an operator assertion after external checks, not a
  Git check performed by the preview CLI.
- Future live repo status JSON readback should follow
  `docs/verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md`.
  The audit-facing field mapping and status-input fail-closed contract should
  follow
  `docs/verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md`.
  The card should show branch, HEAD, upstream parity, tracked / staged /
  untracked state, allowlist match, runtime artifact state, needs-human
  presence, inspected paths, command provenance, timestamp, source provenance,
  adapter id, and confidence / trust boundary. Machine-collected status is
  still only input evidence; it is not execution permission.
- Any future real runner requires a separately authorized and audited slice
  covering subprocess launch, stdin handling, timeout, cancellation, report
  artifact containment, notification policy, gate authority, and operator card
  readback boundaries.
- External notification remains unimplemented; `notify_stub.log` is only a local
  stub log and must not be read as an external notification result.
