# Operation Cockpit Report Template

Use this template when a common foundation slice needs an Operation Cockpit
v1.10+ completion report. Keep identity and access separate for every
reviewable artifact. Use ASCII_SAFE meters only.

Routing Header:

```text
[ROUTE: NLMYTGen | AGENT->SUPERVISOR | <slice-id> | <turn> | target:<thread> | artifact:<repo-relative-artifact> | reply:<thread> | confidence:<high/medium/low>]
```

Meter rule:

- Source of truth is `done`, `total`, `unknown`, and `missing`.
- For `total <= 12`, use exact meters such as `[#####-] 5/6`.
- For `total > 12`, use a scaled 10-slot meter such as `[########--] 14/18`.
- For effort weights, use W1-W5 meters such as `W3 [###--]`.
- Do not use Unicode block, shaded, emoji, full-width, or box-drawing meters.

## Current State

- outcome:
- active artifact:
- health:
- routing_confidence:
- next owner:
- estimate_next_agent_run:
- estimate_user_work:
- Handoff Gate:

## Completion Matrix

| Gate group | Done | Total | Unknown | Meter | Missing |
| --- | ---: | ---: | ---: | --- | --- |
| Slice Acceptance |  |  |  | `[-----] 0/5` |  |
| Artifact Readiness |  |  |  | `[-----] 0/5` |  |
| Report Hygiene |  |  |  | `[----------] 0/13` |  |

## Work Performed vs Expected

| Expected | Actual | Assessment | Next correction |
| --- | --- | --- | --- |
|  |  |  |  |

## Changed Files

| File | Change | Reason |
| --- | --- | --- |
|  |  |  |

Use `none` when no files changed.

## Artifacts / Review Access

| Artifact ID | Identity | Access | Readiness | User action |
| --- | --- | --- | --- | --- |
| dashboard | `docs/dashboard/index.html` | `scripts/operator/open_dashboard.ps1` |  |  |
| status-json | `docs/dashboard/project-status.json` | linked from dashboard |  |  |
| screenshot | `docs/review/common-foundation-dashboard-2026-06-17.png` | linked from dashboard/docs index if present |  |  |
| report-template | `docs/_templates/operation-cockpit-report.md` | repo-relative reference |  |  |

## Review Card / Review Debt

- status: none / required / debt
- target:
- look_for:
- input_mode: freeform
- completion_signal:
- fixed_phrase_required: no

## Freeform Review Intake Result

- status: none / consumed
- target:
- intent:
- constraints:
- confidence:
- user_rewrite_required: no

## Command / Action Ledger

Use one of these action types: `EXECUTED_BY_AGENT`, `AGENT_TO_RUN`,
`USER_OPEN_ONLY`, `USER_REVIEW_FREEFORM`, `REFERENCE_ONLY`, or `DO_NOT_RUN`.

| Type | Owner | Purpose | Target or command | Result | User action |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## User-Side Work

- status: none / required / open-only
- type: none / USER_OPEN_ONLY / USER_REVIEW_FREEFORM
- estimate:
- action:
- completion_signal:
- fixed_phrase_required: no

## Agent-Side Work

- status:
- estimate:
- autonomy_scope:

| Next action | Bottleneck reduced | What becomes possible |
| --- | --- | --- |
|  |  |  |

## Goal Stack

- Immediate:
- Short-term:
- Mid-term:
- Long-term:

## Turn Calendar

| Turn | Owner | Weight | Estimate | Goal | Deliverable | Gate | Status | Branch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T+0 | Agent | W2 `[##---]` | ~5-10 min | verify state | clean verified state | 5/5 |  |  |
| T+1 | Agent | W3 `[###--]` | ~10-20 min | scoped implementation | updated artifacts | 6/7 |  |  |
| T+2 | Agent | W2 `[##---]` | ~5-10 min | validate and commit | local commit if changed | 5/5 |  |  |
| T+3 | Agent | W2 `[##---]` | ~5-10 min | push and readback | remote parity 0 0 | 4/4 |  |  |
| T+4 | Supervisor | W2 `[##---]` | ~5-10 min | review cockpit | next direction | 0/5 | future | none |

## Visual Summary

Derived from Completion Matrix:

- slice_acceptance:
- artifact_readiness:
- report_hygiene:

## Decision Packet

- status: none / required
- options:
- recommended default:
- reason for default:
- rejected alternatives:
- remaining decision point:
- work that can continue without the decision:
- response_mode: freeform

## Metric Change Note

- status: none / changed
- changed:
- reason:
- comparability:

## Continuation State / Handoff Gate

- handoff_gate:
- next actions:
- remaining uncertainty:
- true blockers:
- Handoff Gate satisfied:
