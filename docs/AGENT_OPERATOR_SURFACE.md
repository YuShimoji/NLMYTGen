# Agent Operator Surface

This page defines the smallest human-readable review surface for the current
common foundation fake / single-fake flow. It is a review card, not an execution
entry point.

The card exists so an operator can answer these questions without reading test
output or Python implementation:

- what was attempted
- which worker and scenario were used
- whether this is a deterministic example or a real result card
- whether preflight passed
- whether the local simulation runner started
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

To render a real card, pass an existing repo-local orchestration flow JSON:

```powershell
uv run python scripts/agent_operator_surface.py path\to\flow-result.json
```

The script only reads a JSON file inside this repo and prints Markdown. It does
not run Codex, does not run the local simulation runner, does not create a
subprocess, does not pipe stdin, does not start a worker loop, and does not send
external notifications.

## Example Card

```markdown
# NLMYTGen Operator Review Card

## Summary
- Card mode: example
- Plain-language result: Audit worker reached a human-review stop.
- Human action required: yes
- Decision to make: Inspect the listed artifacts, then choose whether to run summarize, request a fix, or stop.
- This is a deterministic sample card; it did not run or verify any worker artifacts.

## Status
- Flow status: completed
- Preflight check: passed
- Local simulation runner started: yes
- Gate result: needs human review
- Human action required: yes

## What happened
- Attempted work: Review an existing local simulation result
- Worker / scenario: Audit worker / Needs human review
- Prompt: .agent/prompt_catalog/audit.md
- Schema: .agent/schemas/worker_report.schema.json
- Planned report: .agent/reports/example-audit.report.json
- Runner report written: yes
- Runner exit: 0
- Runner timed out: no
- Runner error kind: none

## Human decision needed
- Human action required: yes. Decide whether to continue with the suggested next worker, send the result back for a fix, or keep the run stopped for more human input.
- Decision to make: Inspect the listed artifacts, then choose whether to run summarize, request a fix, or stop.
- Report note: Review the example report shape and decide whether the next real worker result should be summarized, fixed, or held for more human input.
- Gate reasons:
- status:needs_human
- Preflight reasons:
- none

## Files to inspect
- Note: Example paths only; this example command does not check whether these files exist.
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
- Local notify stub: only written after gate_result.needs_human=true

## Next safe actions
- Open the report and needs-human stub paths listed above.
- Answer the human question or choose the next worker after inspecting the gate reasons.
- Treat this as a local review stop, not a production or release approval.

## Raw identifiers
- mode: single_fake_execution_flow_for_test
- worker: audit
- scenario: needs_human
- preflight_allowed: yes
- runner_started: yes
- gate_decision: needs_human
- report_path: .agent/reports/example-audit.report.json
```

## Boundary

The operator card is deliberately downstream of existing outputs. It can make a
flow understandable, but it is not authority to continue through a gate.

- `needs_human=true` remains a local review stop.
- `codex_execution_started=false` and `real_subprocess_started=false` remain the
  expected state for the fake and single-fake flow.
- Real runner boundary design is still a separate future slice.
- External notification remains unimplemented; the local notify stub is the only
  visible notification artifact.
