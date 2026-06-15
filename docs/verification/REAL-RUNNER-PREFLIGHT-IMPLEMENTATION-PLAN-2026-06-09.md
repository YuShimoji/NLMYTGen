# Real Runner Preflight Implementation Plan - 2026-06-09

This is a docs-only planning slice for a future disabled-by-default real runner
preflight. It accepts
`docs/verification/REAL-RUNNER-BOUNDARY-DESIGN-2026-06-09.md` as the current
boundary design and narrows the next implementation surface before any real
execution work is considered.

This plan does not implement real `codex exec`, does not add
`subprocess.run`, does not pipe prompt content to stdin, does not create a
runtime worker loop, does not add external notification, and does not create
runtime artifacts under `.agent/reports/` or `.agent/logs/`.

## Scope

The future preflight is a fail-closed decision step that runs before any real
runner starts. Its job is to inspect authority, paths, repo state, command
shape, prompt source, schema/report destinations, timeout, environment, and
notification policy, then return a structured result that can be shown to an
operator.

| Item | In scope for this plan | Still out of scope |
| --- | --- | --- |
| Execution mode | Define how dry-run, fake runner, and future real runner are distinguished. | Starting real `codex exec`. |
| Safety checks | Define the checks the future preflight must perform. | Implementing Python code or tests in this slice. |
| Operator review | Define result fields that can be rendered or summarized by the operator card. | Treating the operator card as execution authority. |
| Runtime artifacts | Define containment and overwrite refusals for future reports/logs. | Creating report/log/needs-human runtime output now. |
| Notification | Keep local notify stub and external notification boundaries explicit. | Adding an external notification service. |

The default state remains disabled. A future real runner can only be considered
when both of these are true:

- a disabled-by-default execution flag is explicitly enabled for that run
- human authority explicitly says that one bounded real execution may start

## Inputs The Future Preflight Must Inspect

The future preflight should receive or derive a complete execution plan before
returning `allowed=true`. Missing values fail closed.

| Input | Required check | Blocking concern |
| --- | --- | --- |
| Requested mode | Must be one of the known modes: dry-run preview, fake runner helper/test flow, or future real runner. | Ambiguous automation requests can accidentally imply real execution. |
| Worker | Must be one of the configured worker names such as `advance`, `audit`, `fix`, or `summarize`. | Unknown worker can select an unintended prompt or report path. |
| Prompt source | Must be explicit, repo-local, traversal-safe, and unambiguous. | Stdin must not be assembled from unclear or private sources. |
| Schema path | Must point to the repo-local worker report schema. | Missing or unsafe schema prevents reliable gate validation. |
| Report path | Must be under `.agent/reports/`, traversal-safe, non-existing, and repo-local. | Unsafe write paths or overwrites can destroy evidence. |
| Log path | If present, must be under `.agent/logs/` and traversal-safe. | Logs must not escape runtime artifact containment. |
| Working directory / repo root | Must resolve to the current repo root. | Repo-external cwd can read or write the wrong project. |
| Timeout | Must be a positive bounded integer. | Unbounded execution and missing timeout are not acceptable for a first real runner. |
| Execution authority flag | Real execution requires both enabled policy and explicit human authority for the run. | Default-disabled policy must remain fail-closed. |
| Dirty tracked tree | Must be clean before future real execution. | Existing modifications make attribution and rollback unclear. |
| Staged files | Must be absent before future real execution. | Staged changes can be accidentally carried into later commits. |
| Untracked files policy | Unknown untracked files must block unless explicitly allowlisted by policy. | Runtime residue and unrelated files can be mistaken for runner output. |
| Environment / credential policy | Environment use must be reviewed, and credential-like values must not be injected by the runner. | Secrets can leak into prompts, logs, reports, or subprocess environment. |
| Notification policy | Must state local stub only, or a separately authorized external path. | Notification must not become implicit execution or publication authority. |

## Required Refusal Cases

The future preflight must return `allowed=false` and
`safe_to_start_real_runner=false` for these cases:

- no explicit real-execution authority
- real execution requested while the disabled-by-default execution flag is not
  enabled
- dirty tracked tree
- staged files
- unknown untracked files unless allowlisted by policy
- repo-external prompt, schema, report, log, or needs-human path
- `..` path traversal
- absolute unsafe path
- existing report overwrite
- shell-dependent command shape
- command represented only as a shell string
- missing timeout or non-positive timeout
- invalid worker
- missing schema
- prompt source ambiguity
- credential-like strings in prompt, environment, config, report path, log path,
  or future runner metadata
- notification ambiguity
- request to mix this common-foundation work with G-28, Newsroom, G-27,
  ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, `.ymmp`, render, rights,
  production, publishing, or release automation

Credential detection cannot prove that no secret exists, but it should block on
obvious token-like strings and should avoid logging full prompt/environment
content when metadata or digests are enough.

## Required Allow Cases

The future preflight should allow only narrow non-execution flows by default,
and real execution only after explicit opt-in.

| Case | Allowed result | Reason |
| --- | --- | --- |
| Dry-run preflight preview | `allowed=true`, `safe_to_start_real_runner=false` | The operator can inspect command shape, paths, and refusal/allow reasons without starting a runner. |
| Fake runner test/helper flow | `allowed=true`, `safe_to_start_real_runner=false` | The existing fake path remains synthetic and must keep `codex_execution_started=false` and `real_subprocess_started=false`. |
| Future real runner with disabled flag explicitly enabled and human authority explicit | `allowed=true`, `safe_to_start_real_runner=true` | This is the only condition that can pass control to a separate real runner step. |
| Repo-local prompt/schema/report paths | Eligible for allow after all other checks pass. | Path containment is necessary but not sufficient for real execution. |

An allowed preflight result does not itself execute anything. It only states
whether a separate runner step may start.

## Proposed Preflight Result Shape

The future implementation should return a plain structured object that can be
serialized to JSON and rendered by an operator card.

```json
{
  "allowed": false,
  "mode": "real_runner",
  "worker": "audit",
  "reasons": [
    "execution_policy.codex_exec_enabled=false",
    "missing_explicit_human_authority"
  ],
  "safe_to_start_real_runner": false,
  "codex_execution_started": false,
  "real_subprocess_started": false,
  "report_path": ".agent/reports/20260609-audit.report.json",
  "inspected_paths": [
    ".agent/prompt_catalog/audit.md",
    ".agent/schemas/worker_report.schema.json",
    ".agent/reports/20260609-audit.report.json"
  ],
  "authority_summary": {
    "execution_policy_enabled": false,
    "human_real_execution_authority": false,
    "notification_policy": "local_stub_only"
  }
}
```

Required field meanings:

- `allowed`: whether this mode/path/policy combination passes preflight
- `mode`: requested mode after normalization
- `worker`: selected worker after validation
- `reasons`: human-readable allow or block reasons
- `safe_to_start_real_runner`: true only for a future authorized real runner
- `codex_execution_started`: always false inside preflight
- `real_subprocess_started`: always false inside preflight
- `report_path`: planned repo-relative report path, if applicable
- `inspected_paths`: repo-relative paths reviewed by preflight
- `authority_summary`: compact record of execution and notification authority

The preflight result should avoid full secret-bearing values. If later fields
are added for environment or prompt metadata, they should prefer labels,
booleans, digests, sizes, and policy names over raw content.

## Operator Card Mapping

The preflight result must be renderable or summarizable by the existing
operator-card contract in `docs/AGENT_OPERATOR_SURFACE.md`.

| Preflight field | Operator card use |
| --- | --- |
| `allowed` | Shows whether preflight passed or blocked. |
| `mode` / `worker` | Shows what was attempted. |
| `reasons` | Shows the human-readable block or allow explanation. |
| `safe_to_start_real_runner` | Distinguishes dry-run/fake allow from real-runner start permission. |
| `codex_execution_started` / `real_subprocess_started` | Preserves the safety boundary before execution. |
| `report_path` / `inspected_paths` | Gives the operator exact repo-local files to inspect. |
| `authority_summary` | Shows whether execution and notification authority were explicit. |

Blocked preflight should show a concise reason that an operator can act on, such
as `dirty_tracked_tree`, `missing_explicit_human_authority`, or
`repo_external_report_path`.

Allowed preflight must still say that no execution has started and that a
separate runner step is required before any real command can run.

## Future Implementation Plan

The implementation should be split so each step can be reviewed without
starting real execution.

1. Define a small preflight input/result type near the existing orchestrator
   code, without changing the default CLI into a real runner.
2. Normalize requested mode, worker, prompt path, schema path, report path, cwd,
   timeout, execution authority, repo status, environment policy, and
   notification policy.
3. Add fail-closed path containment helpers or reuse existing policy helpers
   where they already exist.
4. Add repo-state checks for tracked dirty files, staged files, and untracked
   files according to the configured policy.
5. Add credential-like string screening for planned prompt/environment/config
   surfaces without logging raw secrets.
6. Return the proposed result shape and make dry-run preview able to display it.
7. Only after the preflight is reviewed and tested, consider a separate real
   runner slice that consumes an already allowed preflight result.

This plan intentionally does not decide the final Python function names or file
edits. Those belong to the implementation slice and should be chosen in sympathy
with the existing `scripts/agent_orchestrator.py` structure at that time.

## Future Test Plan

When implementation is authorized, add narrow tests before any real subprocess
path is enabled.

| Test case | Expected result |
| --- | --- |
| Clean tree dry-run preview | Allows preview, keeps `safe_to_start_real_runner=false`. |
| Dirty tracked tree | Blocks real runner. |
| Staged file | Blocks real runner. |
| Unknown untracked file | Blocks unless allowlisted by policy. |
| Report path traversal | Blocks. |
| Repo-external prompt/schema/report/log path | Blocks. |
| Missing real-execution authority | Blocks. |
| Disabled execution flag | Blocks real runner even if the command shape is otherwise valid. |
| Shell command string or shell-dependent command shape | Blocks. |
| Missing timeout | Blocks. |
| Invalid worker | Blocks. |
| Missing schema | Blocks. |
| Prompt source ambiguity | Blocks. |
| Credential-like string | Blocks or escalates to human review before execution. |
| Notification ambiguity | Blocks. |
| Fake runner helper flow | Allows synthetic helper/test flow without real execution. |
| Authorized future real runner | Allows only when disabled-by-default flag is enabled, human authority is explicit, tree/path checks pass, and timeout is bounded. |

The tests should assert that preflight itself leaves
`codex_execution_started=false` and `real_subprocess_started=false`.

## Stop Conditions

Stop before or during the implementation slice if any of these appear:

- any need to edit scripts or tests during this planning slice
- unclear existing policy that cannot be resolved from repo docs
- runtime artifact creation under `.agent/reports/`, `.agent/logs/`, or
  `.agent/needs_human.json`
- pressure to start a subprocess
- pressure to pipe prompt content to stdin
- pressure to add external notification
- request to mix another repo or lane into this common-foundation path
- request to treat dry-run, fake runner, or operator-card review as production,
  release, rights, publishing, or real-execution approval

If one of these stop conditions appears in a future implementation slice, record
the block as a policy/design gap before changing implementation files.

## Current Slice Closure

This planning slice should end with only docs updates:

- this plan document
- a minimal `docs/runtime-state.md` note
- a minimal `docs/project-context.md` decision entry

No implementation file, test file, source file, GUI file, sample, `.ymmp`,
runtime report, runtime log, Newsroom path, or ClipPipeGen path should be
changed for this slice.
