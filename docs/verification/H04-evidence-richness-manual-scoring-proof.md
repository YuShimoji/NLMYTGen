# H-04 Evidence Richness Manual Scoring Proof

> Purpose: verify that H-04 warnings can be converted into concrete repair actions
> Status: proof packet
> Updated: 2026-04-06

---

## Goal

H-04 is only useful if it produces repairable guidance rather than a vague score.

This packet checks one real topic and confirms:

1. category scoring is understandable
2. warnings are actionable
3. the result helps packaging and script revision without replacing human judgement

---

## Suggested Sample

Use the existing repo-local sample set:

- script: `samples/AI監視が追い詰める生身の労働.txt`
- packaging brief: `samples/packaging_brief_ai_monitoring.md`
- optional cue memo: `samples/AI監視が追い詰める生身の労働_cue_memo_received.md`

This sample is useful because:

- it already has a packaging brief
- it already depends on concrete numbers and named mechanisms
- it is likely to reveal weakness in `anecdote`, `freshness`, or `promise_payoff`

---

## Scoring Sheet

Score each category from 0 to 3 using `docs/EVIDENCE_RICHNESS_SCORE_SPEC.md`.

| Category | Score (0-3) | Notes |
|---|---|---|
| `number` |  |  |
| `named_entity` |  |  |
| `anecdote` |  |  |
| `case` |  |  |
| `study` |  |  |
| `freshness` |  |  |
| `promise_payoff` |  |  |

Then list:

- warnings
- best supports
- missing or weak evidence
- recommended repairs

---

## Pass Conditions

H-04 manual proof is considered successful if all of the following are true:

1. the scorer can assign all 7 category scores without inventing new axes
2. at least one warning maps to a clear script repair
3. at least one warning maps to a packaging adjustment
4. the result explains *why* a promise feels weak, not just that it feels weak

---

## Repair Mapping Guide

Use this mapping when translating warnings into actions.

| Warning | Typical repair |
|---|---|
| `EVIDENCE_REQUIRED_MISSING` | add the missing support to body or weaken packaging promise |
| `EVIDENCE_REQUIRED_WEAK` | surface the evidence earlier or more concretely |
| `EVIDENCE_NO_NUMBER` | add a specific number or remove specificity-heavy thumbnail copy |
| `EVIDENCE_NO_ANECDOTE` | add one human-scale episode or witness scene |
| `EVIDENCE_NO_CASE` | add one concrete incident, company, or historical case |
| `EVIDENCE_NO_STUDY` | add report or research framing |
| `EVIDENCE_FRESHNESS_UNCLEAR` | add date or current trigger |
| `EVIDENCE_PROMISE_GAP` | reduce packaging claim or strengthen opening/body payoff |
| `EVIDENCE_ABSTRACT_DRIFT` | replace abstract explanation with concrete anchors |

---

## Output Template

```md
# Evidence Richness Proof

- total_score:
- band:

## Category Scores
- number:
- named_entity:
- anecdote:
- case:
- study:
- freshness:
- promise_payoff:

## Warnings
- ...

## Best Supports
- ...

## Missing Or Weak Evidence
- ...

## Recommended Repairs
- script:
- packaging:
```

---

## Sample Dry Expectation

Expected tendency for the AI monitoring sample:

- `number`: medium to high
- `named_entity`: medium
- `anecdote`: weak
- `case`: medium
- `study`: medium
- `freshness`: weak to medium
- `promise_payoff`: medium

Likely repairs:

- add one worker-scale anecdote
- make the "why now" anchor more explicit
- surface the strongest number earlier in the opening
