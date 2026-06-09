# Pre-Execution Dry-Run Flow Design - 2026-06-10

This is a docs-only design slice for
`pre_execution_dry_run_flow_design_001`.

It does not implement real `codex exec`, add `subprocess.run`, pipe stdin,
create a runtime worker loop, send external notifications, create `.agent`
runtime artifacts, or modify Python code/tests.

The purpose is to define the next safe common-foundation step after the parked
preflight / operator-surface state: a pre-execution dry-run flow that lets a
human inspect the intended runner inputs, command shape, preflight result,
operator card, and next decision before any real runner implementation exists.

## Purpose

The flow should answer one human question before any real runner exists:

> If this work were later allowed to run, what exactly would be attempted, what
> would be inspected first, why would it be allowed or blocked, and what must a
> human decide next?

The dry-run flow is therefore a review flow, not an execution flow. It should
make the future attempt legible without turning a preflight result into
permission to execute.

## Current Parked State

The current common foundation is parked after human review of the standalone
preflight preview card.

Current sealed layers:

| Layer | Current status | Boundary |
| --- | --- | --- |
| Fake runner scaffold | Exists as a synthetic test/helper path. | Not a real `codex exec` route. |
| Single fake execution flow | Exists as a test/helper-only composition. | Not exposed through normal CLI/runtime behavior. |
| Operator Review Surface | Exists as read-only Markdown cards. | Review surface, not execution authority. |
| Disabled real-runner preflight | Exists and returns structured allow/block data. | Preflight itself starts no runner. |
| Raw preflight preview card | Exists for human-readable raw preflight output. | A readable preview, not permission. |

Sealed safety fields remain:

- `codex_execution_started=false`
- `real_subprocess_started=false`
- real `codex exec` is unimplemented
- real subprocess runner is unimplemented
- stdin prompt piping is unimplemented
- runtime worker loop is unimplemented
- external notification service is unimplemented
- `.agent/reports`, `.agent/logs`, and `.agent/needs_human.json` runtime
  artifact creation is not opened by this design

## Human-Visible Dry-Run Flow

The future dry-run flow should be linear and stop after the human-readable
preview.

1. Select a worker and prompt source.
2. Build a would-be execution plan without starting anything.
3. Show the selected prompt, schema, report path, working directory, timeout,
   notification policy, and planned command argv.
4. Run `build_execution_preflight` against that plan and the current repo
   status.
5. Render the raw preflight preview card from the preflight result.
6. Ask the human for the next decision.
7. Stop.

The flow must not call a runner after step 6. It must not create a report,
notify stub, runtime log, or needs-human file. It may print the preview to the
terminal or another explicitly read-only surface. If a future slice wants a
saved example, it should use a docs fixture or verification document, not
`.agent/reports` runtime output.

## Inputs Shown To The Human

Before any execution can be considered, the human should see these fields in
plain language:

| Input | Human sees | Why it matters |
| --- | --- | --- |
| Worker | `advance`, `audit`, `fix`, or `summarize` | Shows which fixed prompt family is being selected. |
| Prompt source | Repo-local prompt path, expected digest/size metadata if available | Confirms what would be sent to stdin later without exposing private content unnecessarily. |
| Schema path | `.agent/schemas/worker_report.schema.json` | Confirms the output contract the worker would be held to. |
| Planned report path | `.agent/reports/{timestamp}-{worker}.report.json` | Shows where a future real run would be required to write one report. |
| Command shape | Shell-free argv preview | Lets the human check that no shell string, pipe, or broad command is hidden. |
| Working directory | Repo root | Confirms the command would run in the intended checkout. |
| Timeout | Positive bounded integer | Confirms the future run cannot be unbounded. |
| Repo state summary | branch, upstream parity, staged/tracked dirty state, untracked allowlist result | Shows whether attribution and artifact hygiene are safe. |
| Authority summary | execution flag, explicit human authority, notification policy | Separates eligibility from permission. |
| Runtime artifact policy | report/log/needs-human containment | Confirms the future run would not write elsewhere. |

Missing, ambiguous, repo-external, traversal, or credential-like inputs stop the
flow before any approval discussion.

## Command Shape Preview

The preview should show an argv shape, not a shell command string.

Proposed future argv display:

```text
argv:
- codex
- exec
- -
- --output-schema
- .agent/schemas/worker_report.schema.json
- -o
- .agent/reports/{timestamp}-{worker}.report.json
stdin_source:
- .agent/prompt_catalog/{worker}.md
```

The preview must say:

- this command is not executed by the dry-run flow
- stdin is not piped in this design slice
- `subprocess.run` is not added by this design slice
- a future runner implementation must keep command construction argv-based and
  shell-free

If the command is represented only as a string such as
`"codex exec ..."` in a future implementation preview, that should block the
real runner path until it is normalized to argv.

## Use Of `build_execution_preflight`

The dry-run flow uses `build_execution_preflight` as the policy checkpoint for
the would-be plan.

The future dry-run should pass or derive:

- requested flow mode: `pre_execution_dry_run`
- intended runner mode: `real_runner` or another explicit mode being previewed
- selected worker
- prompt path
- schema path
- planned report path
- working directory
- timeout
- repo status
- execution authority summary
- notification policy summary

The returned preflight result must preserve:

- `codex_execution_started=false`
- `real_subprocess_started=false`
- `allowed`
- `safe_to_start_real_runner`
- human-readable `reasons`
- `inspected_paths`
- `authority_summary`
- planned `report_path`

The dry-run flow is allowed to render the result. It is not allowed to consume
an allowed result by starting a runner.

## Preflight Result Shown To The Human

The human should see the preflight result as an explanation, not as a raw dump.

Minimum display:

| Result field | Human-readable label |
| --- | --- |
| `allowed` | Preflight passed for this preview / preflight blocked this preview |
| `safe_to_start_real_runner` | Real-runner eligibility signal, not execution permission |
| `reasons` | Why the plan passed or blocked |
| `inspected_paths` | Files and paths checked before any run |
| `authority_summary` | Whether execution and notification authority are explicit |
| `report_path` | Where the future report would be required to appear |
| `codex_execution_started` | Must be false |
| `real_subprocess_started` | Must be false |

For `safe_to_start_real_runner=true`, the card must still say:

> This means the plan is eligible for a separately authorized real-runner step.
> It does not start execution and does not grant permission by itself.

For `safe_to_start_real_runner=false`, the card should name the blocking
reason in language a human can act on, such as dirty tracked tree, missing
explicit authority, unsafe report path, ambiguous prompt source, missing
timeout, or notification ambiguity.

## Operator Card Usage

The raw preflight preview card is the human-facing surface for the dry-run
flow. It should sit before any runner result card.

The card should show:

- what would be attempted
- selected worker
- prompt source
- schema path
- planned report path
- exact argv shape
- preflight pass/block state
- `safe_to_start_real_runner` with an explicit "not permission" label
- reasons
- inspected paths
- authority summary
- execution boundary
- human next action

It should not show:

- "runner started"
- "report written"
- "gate evaluated report"
- "notify stub written"
- "external notification sent"

Those belong only to a post-run flow result. A pre-execution dry-run has no
worker report and no gate result from a real run.

## Files The Human Inspects

The dry-run card should give exact repo-local files to inspect:

- `AGENTS.md`
- `docs/REPO_LOCAL_RULES.md`
- `docs/runtime-state.md`
- `docs/AGENT_ORCHESTRATION.md`
- `docs/AGENT_OPERATOR_SURFACE.md`
- `.agent/state.json`
- `.agent/repo_adapter.json`
- `.agent/prompt_catalog/{worker}.md`
- `.agent/schemas/worker_report.schema.json`
- the planned report path string under `.agent/reports/`

The planned report path is inspected as a path, not opened as an existing file.
The dry-run flow should not create it.

## What Counts As Approval

The human can approve the dry-run review surface in these narrow ways:

- The selected worker and prompt source are understandable.
- The schema and report path are correct for a future report.
- The argv preview is the expected command shape.
- The preflight reasons are understandable.
- The operator card gives enough information to choose a next action.
- A later implementation slice may build the preview-only dry-run flow.

This approval can authorize a future preview implementation slice. It does not
authorize real execution.

## What Does Not Count As Approval

The following do not count as permission to run a real worker:

- `allowed=true`
- `safe_to_start_real_runner=true`
- a clean repo
- a readable operator card
- a human saying the preview "looks good"
- this design document
- a docs-only commit or pushed handoff

Real execution requires a separate later request that explicitly authorizes one
bounded real-runner implementation or run, with the command boundary and
artifact policy restated.

## Human Decisions

The dry-run flow should end with one of these decisions:

| Decision | Meaning | Next move |
| --- | --- | --- |
| Hold / no-op | Do not proceed. | Keep parked state. |
| Revise preview inputs | Worker, prompt, schema, report path, timeout, authority, or notification policy is unclear. | Adjust design or future dry-run preview before implementation. |
| Request design fix | The human-visible card is still confusing. | Update docs/design, not code execution. |
| Authorize preview-only implementation | Build a dry-run preview flow that prints the plan/preflight/card and stops. | Future code/test slice, still no real execution. |
| Request real-runner design review | Start a separate runner consumption design or implementation plan. | Separate docs/design slice. |
| Explicitly authorize one real runner slice | Only if a future prompt says so directly. | Separate implementation/run slice with preflight gate and stop conditions restated. |

The dry-run flow should not offer "run now" as a default next action.

## Stop Conditions

Stop before real execution if any of these appear:

- dirty tracked files
- staged files
- unknown untracked files outside the allowlist
- missing prompt path
- missing schema
- planned report path outside `.agent/reports/`
- path traversal
- existing report overwrite
- command preview is a shell string rather than argv
- missing or non-positive timeout
- prompt source ambiguity
- notification ambiguity
- credential-like value in planned prompt, config, environment, report path,
  log path, or metadata
- external notification requested without separate authorization
- request to treat `safe_to_start_real_runner=true` as execution permission
- request to mix this common-foundation path with G-28, Newsroom, G-27,
  ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights,
  production, publishing, or release automation

Each stop condition should produce a human-readable reason. The stop reason
should be something the human can correct or explicitly defer.

## Required Future Implementation Boundaries

If this design is accepted and a future implementation slice is opened, that
slice must keep these boundaries:

- preview-only implementation first
- no real `codex exec`
- no `subprocess.run`
- no stdin piping
- no runtime worker loop
- no external notification
- no `.agent/reports`, `.agent/logs`, or `.agent/needs_human.json` runtime
  artifact creation
- no writes outside the authorized docs/code/test scope for that future slice
- no G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM,
  `.ymmp`, render, rights, production, publishing, or release automation

A future preview implementation may add code and tests only if separately
authorized. It should still prove that no runner starts and no runtime artifacts
are created.

## Minimal Future Tests

If a future implementation slice is authorized, prioritize human comprehension
over broad internal test growth. Add only tests that protect the visible
contract.

Minimal tests:

- preview prints selected worker, prompt path, schema path, report path, cwd,
  timeout, and argv shape
- preview invokes preflight and renders the preflight result
- preview preserves `codex_execution_started=false`
- preview preserves `real_subprocess_started=false`
- preview does not create `.agent/reports`, `.agent/logs`, or
  `.agent/needs_human.json`
- preview labels `safe_to_start_real_runner=true` as eligibility, not
  permission
- dirty tracked tree or staged files appear as human-readable stop reasons
- repo-external or traversal report path appears as a human-readable stop reason
- notification ambiguity appears as a human-readable stop reason

Avoid adding broad test matrices unless a specific boundary is at risk.

## Non-Goals

This design does not:

- implement real runner behavior
- run Codex
- run a subprocess
- pipe stdin
- validate a real worker report
- write a report JSON
- write a notify stub
- write runtime logs
- create `.agent` runtime state
- approve release, publish, rights, production, render, or `.ymmp` work
- supersede G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, or
  NotebookLM boundaries

## Next Safe Slice After This Design

The next safe slice is human review of this design.

If accepted, the next implementation-oriented slice should be a narrow
`pre_execution_dry_run_flow_preview_implementation_001` that only prints the
planned inputs, command argv, preflight result, and operator card, then stops.
It must still avoid real execution, `subprocess.run`, stdin piping, runtime
worker loops, external notification, and runtime artifact creation.

If the human wants a different route, the alternative safe slice is a docs-only
runner consumption design that explains how an already-approved preflight would
be consumed later. That still should not implement or run the real runner.
