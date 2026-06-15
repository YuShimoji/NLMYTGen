# Real Runner Boundary Design — 2026-06-09

This is a docs-only design slice for `real_runner_boundary_design_001`.
It does not implement real `codex exec`, `subprocess.run`, stdin piping,
a runtime worker loop, or an external notification service.

The purpose is to define the boundary that must exist before any real runner
implementation is considered.

## Current Sealed State

The common foundation has three sealed layers:

| Layer | Current status | Boundary that remains closed |
| --- | --- | --- |
| Fake runner scaffold | Implemented and committed as a tests-only scaffold. Synthetic reports are written to the planned report path and valid reports go through `agent_gate.evaluate_report`. | Not a real `codex exec` route. |
| Single fake execution flow | Implemented as a test/helper-only composition of execution plan, explicit repo-status preflight, fake runner, gate, and notify stub. It is not exposed through the default CLI/runtime path. | No `--single-fake-flow` runtime flag. |
| Operator Review Surface MVP | Implemented by `scripts/agent_operator_surface.py` and documented in `docs/AGENT_OPERATOR_SURFACE.md`. It renders existing repo-local flow JSON into a Markdown card. | Read-only review surface, not execution authority. |

The sealed safety fields remain:

- `codex_execution_started=false`
- `real_subprocess_started=false`
- real `codex exec` is unimplemented
- real subprocess runner is unimplemented
- stdin prompt piping is unimplemented
- runtime worker loop is unimplemented
- external notification service is unimplemented

## Real Runner Design Goal

A future real runner may be considered only if it keeps the existing sequence:

1. Build an execution plan.
2. Run explicit preflight.
3. If and only if human authority and preflight allow it, start one bounded real
   command.
4. Persist one report JSON under `.agent/reports/`.
5. Validate the report with `agent_gate`.
6. Invoke local notify stub, or future authorized notification, only after
   `gate_result.needs_human=true`.
7. Render an operator card so a human can read what happened and decide the next
   action.

The real runner should permit only a narrow, auditable execution path. It should
stop before unclear authority, unclear command construction, unsafe paths,
ambiguous prompt source, missing report output, failed schema validation,
unbounded runtime, or unclear notification behavior.

Before execution, the operator must be able to review:

- selected worker
- prompt source
- schema path
- report path
- exact command argv
- working directory
- timeout
- expected artifact paths
- whether real execution has explicit human authority
- what will happen after gate pass or gate needs-human

## Explicit Non-Goals For This Slice

This slice does not:

- implement real `codex exec`
- add `subprocess.run`
- pass prompt content to stdin
- create a runtime worker loop
- implement cancellation code
- implement external notification
- generate `.agent/reports/` runtime reports
- generate `.agent/logs/` runtime logs
- change `.agent/state.json`
- change Python implementation files
- change tests
- touch G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM,
  `.ymmp`, render, production, rights, or publishing automation

## Authority / Opt-In Policy

Real execution must require explicit human authority in addition to a passing
preflight. The default remains fail-closed and no real execution.

| Mode | Purpose | Execution authority |
| --- | --- | --- |
| Dry-run | Preview command shape, paths, and preflight reasons. | Always allowed when read-only. |
| Fake runner | Exercise gate/report/notify behavior with synthetic output. | Test/helper-only; not real execution. |
| Real runner | Run a bounded `codex exec` command and capture report output. | Requires separate human opt-in and a passing preflight. |

Unclear authority is a stop condition. A request to "continue automation" is not
enough if it does not explicitly authorize real execution and the exact boundary
for that execution.

## Subprocess Boundary

If a future implementation allows real execution, command construction should be
argv-based and shell-free by default.

Proposed future command shape:

- executable: `codex`
- argv head: `codex`, `exec`, `-`
- schema argument: `--output-schema`, `.agent/schemas/worker_report.schema.json`
- report argument: `-o`, `.agent/reports/{timestamp}-{worker}.report.json`
- prompt input: stdin from an explicit repo-local prompt source

Subprocess rules:

- shell expansion is disabled by default
- no command string concatenation for execution
- working directory is the repo root
- executable and argv are logged in the report or runner result
- environment is inherited only after an explicit allow/deny review
- credentials, API keys, service tokens, and token-like private values are not
  read from repo files or injected into the environment by the runner
- stdout and stderr are captured to bounded strings or bounded local log paths
- exit code `0` does not bypass report/schema/gate checks
- nonzero exit, missing report, invalid report, timeout, and cancellation all
  fail closed

## Stdin / Prompt Passing Boundary

Stdin must have an explicit source. The runner must distinguish:

- prompt file: repo-local path under `.agent/prompt_catalog/`
- prompt text: explicit human-provided text, only if a future slice allows it
- generated prompt: derived prompt content, only if a future slice defines its
  provenance and logging boundary

Prompt passing rules:

- prompt source is shown before execution
- prompt path is repo-local and traversal-safe
- prompt content size has a bounded limit
- logs should record prompt source and prompt digest/metadata, not necessarily
  full prompt body
- private data, credentials, API keys, service tokens, or token-like private
  values must not be mixed into stdin
- stdin piping failure must fail closed before or during command execution

## Timeout / Cancellation Boundary

A future real runner must define hard timeout behavior before implementation.

Required behavior:

- timeout is a positive integer from the execution policy
- default remains bounded and conservative
- timeout produces a reportable runner state
- timeout result has `needs_human=true` or an equivalent fail-closed gate result
- cancellation produces a reportable runner state
- cleanup behavior is documented before real implementation
- orphan process risk remains a future implementation concern until process-tree
  cleanup is proven on the target OS

The first real runner implementation should support one worker, one command, one
report, and no loop semantics.

## Report Path Containment

Report and log paths must stay inside the repo-local runtime artifact roots:

- reports under `.agent/reports/`
- logs under `.agent/logs/`
- needs-human local state at `.agent/needs_human.json`

The runner must refuse:

- absolute report paths outside the repo
- `..` traversal
- path separators that escape `.agent/reports/`
- arbitrary write paths
- existing report overwrite unless a future explicit overwrite policy exists
- production output paths such as `samples/production*`, `release/`, `dist/`,
  `publish/`, or `published/`

## Gate / Notify Sequence

The gate sequence remains the authority chain:

1. Runner produces output.
2. Runner writes or confirms report JSON.
3. Report JSON is schema-validated.
4. `scripts/agent_gate.py` evaluates policy.
5. Gate returns pass or needs-human.
6. Local notify stub is called only if `gate_result.needs_human=true`.
7. Future external notification is still a separate authorization slice.

Default notification behavior:

- pass does not notify
- needs-human writes only local stub artifacts unless external notification is
  separately authorized
- invalid JSON, missing report, nonzero exit, timeout, cancellation, and blocked
  policy all fail closed
- notification never substitutes for the operator review card

## Operator Review Surface Integration

Any future real runner result must be renderable by
`scripts/agent_operator_surface.py` or by a future adapter with the same
human-readable contract.

The card must show:

- attempted command or execution plan
- worker and scenario/mode
- prompt source
- report path
- preflight result
- runner start and exit state
- gate result
- human action requirement
- files to inspect
- safety boundary
- next safe action

The operator card is not execution authority. It is a review surface after an
existing result, or a preview surface if a future dry-run adapter renders
pre-execution data.

## Runtime Artifact Hygiene

Runtime artifacts remain local unless a future slice explicitly promotes a
fixture or docs example.

- `.agent/reports/.gitkeep` remains the tracked report placeholder.
- `.agent/logs/.gitkeep` remains the tracked log placeholder.
- `.agent/reports/*.report.json` remains local runtime output.
- `.agent/logs/notify_stub.log` remains local runtime output.
- `.agent/needs_human.json` remains local runtime state.
- No production artifacts belong under `.agent/`.
- No `.ymmp`, render, rights, publishing, or release artifact should be created
  by common foundation runner paths.

Cleanup expectations:

- generated reports and logs are removable local runtime residue
- cleanup must not delete tracked `.gitkeep` files
- cleanup must not reach outside `.agent/reports/`, `.agent/logs/`, and the
  configured local needs-human file

## Minimum Future Implementation Checklist

Before any implementation slice, require tests or equivalent proof for:

- default policy refuses real execution
- explicit opt-in is required
- dirty tracked tree stops execution
- staged files stop execution
- unknown untracked files stop execution unless explicitly allowlisted
- prompt path containment
- schema path containment
- report path containment
- repo-external path refusal
- traversal refusal
- existing report overwrite refusal
- command argv construction without shell expansion
- stdout/stderr capture shape
- exit code handling
- missing report fail-closed behavior
- invalid JSON fail-closed behavior
- timeout fail-closed behavior
- cancellation fail-closed behavior, if cancellation is implemented
- no external notification by default
- notify stub only after `gate_result.needs_human=true`
- pass result does not notify by default
- operator card renders real-runner result shape

External notification tests are out of scope unless a separate slice authorizes
external notification design and implementation.

## Stop Conditions

Stop before implementation or execution when any of these appear:

- dirty tracked tree
- staged files that are not part of the authorized slice
- missing or ambiguous human authority for real execution
- ambiguous command shape
- shell-dependent command construction
- repo-external report path
- path traversal in prompt, schema, report, log, or needs-human path
- credentials, API keys, service tokens, or token-like private values in prompt,
  stdin, environment, logs, report, or docs
- unclear notification boundary
- request to mix this work with G-28, Newsroom, G-27, ClipPipeGen, RSS, OPML,
  Inoreader, NotebookLM, `.ymmp`, render, rights, production, publishing, or
  release automation
- request to treat the operator card as execution approval
- request to add external notification without separate authorization

## Recommended Next Move

The next safe move is not implementation. Review this design for missing
boundary cases. If accepted, the following slice can be a narrow implementation
plan for a disabled-by-default real runner preflight, still without starting
`codex exec`.
