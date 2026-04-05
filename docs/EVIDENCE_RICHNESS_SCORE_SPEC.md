# EVIDENCE_RICHNESS_SCORE_SPEC -- Evidence richness score v0.1

> Feature: H-04
> Status: spec v0.1
> Created: 2026-04-06
> Depends on: H-01 Packaging Orchestrator brief, NotebookLM script/source set
> Depended by: packaging review packet, future metadata consumer, future script diagnostics

## 1. Purpose

Evidence richness score is a packaging-side diagnostic that checks whether the
video's core promise is supported by enough concrete material in the script and
source set.

It is meant to answer two questions:

1. does the body contain enough concrete support to pay off the title and thumbnail promise?
2. if it feels weak, what kind of evidence is missing?

This is not a generic quality score. It is a promise-support score with
evidence category diagnostics.

## 2. Non-goals

This spec does not do the following:

- replace human judgement about whether a story is interesting
- verify factual truth on its own
- optimize for score-maxing as a standalone goal
- decide the final title or thumbnail by itself

H-04 is a gate and diagnostic, not a creative decider.

## 3. Inputs

Minimum inputs:

- Packaging Orchestrator brief (`H-01`)
- main script or NotebookLM-derived source script

Recommended inputs:

- source links or source set summary
- C-07 cue memo
- section outline or IR summary when available

## 4. Core Categories

H-04 starts with six category scores plus one payoff score.

| Category | Meaning | Typical evidence |
|---|---|---|
| `number` | hard quantity anchors exist | percentages, counts, money, year span, rankings |
| `named_entity` | concrete actors/institutions are named | company, person, product, law, program, organization |
| `anecdote` | there is at least one memorable story/episode | worker story, scene description, witness account |
| `case` | there is at least one concrete example or incident | company case, court case, product case, country case |
| `study` | academic or expert knowledge appears | paper, report, survey, academic framing |
| `freshness` | recency or current relevance is surfaced | recent date, latest development, update timing |
| `promise_payoff` | the strongest packaging promise is actually supported | title/thumbnail promise is paid off in opening/body |

## 5. Scoring Model

Each category uses a 0-3 ordinal score.

| Score | Meaning |
|---|---|
| `0` | absent |
| `1` | weak or incidental |
| `2` | clearly present |
| `3` | strong and well-surfaced |

Total score is the weighted sum below, normalized to 100.

| Category | Weight |
|---|---|
| `number` | 15 |
| `named_entity` | 10 |
| `anecdote` | 15 |
| `case` | 15 |
| `study` | 15 |
| `freshness` | 10 |
| `promise_payoff` | 20 |

Interpretation bands:

| Band | Meaning |
|---|---|
| `80-100` | strong support for current packaging promise |
| `60-79` | acceptable but with clear strengthening opportunities |
| `40-59` | weak support; packaging likely outruns body |
| `0-39` | high drift risk between packaging and script |

## 6. Category Heuristics

### 6.1 `number`

High score when:

- numbers are specific and relevant to the claim
- at least one number appears in opening or early body
- the number supports the title or thumbnail promise directly

### 6.2 `named_entity`

High score when:

- important actors are named explicitly
- the named entity is part of what makes the claim concrete

### 6.3 `anecdote`

High score when:

- the viewer can remember one person, story, or scene after watching
- a human-scale incident is narrated, not merely referenced

### 6.4 `case`

High score when:

- one or more concrete incidents are described with sufficient detail
- the case could be reused in title, subcopy, or body callback

### 6.5 `study`

High score when:

- the script includes expert framing, report findings, or research results
- the study materially changes how the viewer interprets the topic

### 6.6 `freshness`

High score when:

- recency is explicit and relevant
- the script explains why the topic matters now

### 6.7 `promise_payoff`

High score when:

- the strongest title/thumbnail promise is supported in opening and body
- `required_evidence` from H-01 is mostly `confirmed`
- packaging does not overclaim beyond what the script can pay

## 7. Warning Classes

H-04 should emit explicit warnings instead of only a total score.

| Warning | Trigger |
|---|---|
| `EVIDENCE_REQUIRED_MISSING` | an H-01 `required_evidence` item is still `missing` |
| `EVIDENCE_REQUIRED_WEAK` | an H-01 `required_evidence` item is only `weak` |
| `EVIDENCE_NO_NUMBER` | `number <= 0` while packaging relies on specificity |
| `EVIDENCE_NO_ANECDOTE` | `anecdote == 0` on a human-impact topic |
| `EVIDENCE_NO_CASE` | `case == 0` on an explanatory or controversial topic |
| `EVIDENCE_NO_STUDY` | `study == 0` when the script claims analytical seriousness |
| `EVIDENCE_FRESHNESS_UNCLEAR` | topic implies current relevance but no time anchor appears |
| `EVIDENCE_PROMISE_GAP` | `promise_payoff <= 1` |
| `EVIDENCE_ABSTRACT_DRIFT` | total is inflated by general explanation while concrete anchors remain weak |

## 8. Output Contract

H-04 should be renderable as either JSON or Markdown.

Recommended JSON shape:

```json
{
  "score_version": "0.1",
  "video_id": "amazon_ai_monitoring",
  "total_score": 72,
  "band": "acceptable",
  "category_scores": {
    "number": 3,
    "named_entity": 2,
    "anecdote": 1,
    "case": 2,
    "study": 2,
    "freshness": 1,
    "promise_payoff": 2
  },
  "warnings": [
    "EVIDENCE_REQUIRED_WEAK",
    "EVIDENCE_NO_ANECDOTE"
  ],
  "missing_or_weak_evidence": [
    "human-scale anecdote is still weak",
    "freshness anchor is not explicit"
  ],
  "best_supports": [
    "71.4%",
    "19 billion dollars",
    "Time Off Task"
  ],
  "recommended_repairs": [
    "add one concrete worker episode",
    "surface a time anchor in the opening",
    "connect the strongest number to the opening promise more directly"
  ]
}
```

## 9. Relationship to H-01 and H-02

H-04 should consume H-01 directly.

Use these fields first:

- `title_promise`
- `thumbnail_promise`
- `required_evidence`
- `missing_or_weak_evidence`
- `forbidden_overclaim`
- `consumer_hints.for_h04`

H-02 is a sibling, not a replacement.

- H-02 improves click packaging shape
- H-04 checks whether the underlying script can pay that shape back

## 10. Acceptance for H-04 "Defined"

H-04 can be treated as defined enough to implement or proof once the following are true:

1. score categories are fixed
2. warning classes are fixed
3. H-01 dependency is explicit
4. one real script can be scored manually using this spec
5. result can produce a repair suggestion, not just a number
