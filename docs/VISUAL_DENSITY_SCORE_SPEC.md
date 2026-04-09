# VISUAL_DENSITY_SCORE_SPEC -- Visual density score v0.1

> Feature: H-03
> Status: spec v0.1
> Created: 2026-04-06
> Depends on: H-01 Packaging Orchestrator brief, C-07 cue memo or section plan
> Depended by: packaging review packet, future timeline diagnostics, future metadata consumer

## 1. Purpose

Visual density score is a production-side diagnostic that checks whether a video
has enough visual variation and information-bearing moments to support its
promise without collapsing into flat screens or repetitive layouts.

It is meant to answer two questions:

1. does the section plan create enough visual turnover to keep the topic legible?
2. if the video feels visually weak, what kind of visual density is missing?

This is not an automatic judgement of beauty. It is a stagnation-risk and
payoff-risk diagnostic.

## 2. Non-goals

This spec does not do the following:

- replace human judgement about what looks good in YMM4
- auto-generate backgrounds, animations, or thumbnails
- score final rendered quality from pixels
- force every video to have the same pace or maximal busyness

H-03 is a warning system, not an art director.

## 3. Inputs

Minimum inputs:

- Packaging Orchestrator brief (`H-01`)
- C-07 cue memo, section memo, or equivalent scene plan

Recommended inputs:

- main script
- IR section outline
- bg_map / template usage notes
- future ymmp readback metrics when available

## 4. Core Categories

H-03 starts with six density categories plus one payoff score.


| Category                | Meaning                                                                                    | Typical evidence                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| `scene_variety`         | sections are visually distinct                                                             | interior / warehouse / road / PR UI / future city                         |
| `information_embedding` | numbers, UI, charts, labels, and data moments are explicitly visualized                    | percentage card, timer UI, graph, law text, clause panel                  |
| `symbolic_asset`        | memorable objects or motifs exist                                                          | inhaler, scanner, countdown, thank-you button, drone                      |
| `tempo_shift`           | visual pacing changes across sections                                                      | tense cold open, dense UI section, slower reflective close                |
| `pattern_balance`       | human scene / UI scene / abstract explanation / contrast scene are not overly concentrated | anecdote block, data block, PR block, future thought block                |
| `stagnation_risk`       | repeated same-background risk is low                                                       | section-level turnover, multiple cue types, no single block visually flat |
| `promise_visual_payoff` | title / thumbnail promise has visible on-screen payoff                                     | `71.4%`, `19億ドル`, `タイム・オフ・タスク` become visual moments                      |


## 5. Scoring Model

Each category uses a 0-3 ordinal score.


| Score | Meaning                           |
| ----- | --------------------------------- |
| `0`   | absent                            |
| `1`   | weak or incidental                |
| `2`   | clearly present                   |
| `3`   | strong and intentionally surfaced |


Total score is the weighted sum below, normalized to 100.


| Category                | Weight |
| ----------------------- | ------ |
| `scene_variety`         | 15     |
| `information_embedding` | 15     |
| `symbolic_asset`        | 10     |
| `tempo_shift`           | 10     |
| `pattern_balance`       | 15     |
| `stagnation_risk`       | 15     |
| `promise_visual_payoff` | 20     |


Interpretation bands:


| Band     | Meaning                                                                |
| -------- | ---------------------------------------------------------------------- |
| `80-100` | strong visual support for current promise                              |
| `60-79`  | acceptable, but some sections may flatten                              |
| `40-59`  | noticeable visual stagnation risk                                      |
| `0-39`   | high risk that the video will feel flat or disconnected from packaging |


## 6. Category Heuristics

### 6.1 `scene_variety`

High score when:

- consecutive sections shift location, visual logic, or frame type
- section identities are visually memorable after reading the cue memo

### 6.2 `information_embedding`

High score when:

- key numbers and named systems are turned into visible assets, not just narration
- data moments appear in multiple sections, not only once

### 6.3 `symbolic_asset`

High score when:

- the viewer could remember one or more objects that stand for the theme
- those objects recur with purpose instead of random decoration

### 6.4 `tempo_shift`

High score when:

- visual pacing changes with the argument
- the plan avoids one constant explanatory speed from start to finish

### 6.5 `pattern_balance`

High score when:

- anecdote, UI/data, contrast, and abstract reflection each get an appropriate role
- one mode does not swallow the whole video

### 6.6 `stagnation_risk`

High score when:

- section notes imply regular visual turnover
- repeated backgrounds or cue types are either limited or justified

### 6.7 `promise_visual_payoff`

High score when:

- the strongest thumbnail/title promise becomes a visible on-screen event
- the viewer does not have to infer key packaging evidence from narration alone

## 7. Warning Classes

H-03 should emit explicit warnings instead of only a total score.


| Warning                         | Trigger                                                                  |
| ------------------------------- | ------------------------------------------------------------------------ |
| `VISUAL_SINGLE_BACKGROUND_RISK` | one section appears likely to sit on one background too long             |
| `VISUAL_DATA_PROMISE_UNPAID`    | packaging relies on data, but cue memo does not clearly visualize it     |
| `VISUAL_SYMBOL_MISSING`         | no memorable symbolic object or motif anchors the topic                  |
| `VISUAL_PATTERN_REPEAT`         | the same frame logic dominates too many sections                         |
| `VISUAL_TEMPO_FLAT`             | all sections appear to use similar explanatory pacing                    |
| `VISUAL_CONTRAST_MISSING`       | a PR-vs-reality or before-vs-after topic lacks clear visual contrast     |
| `VISUAL_ENDING_TOO_ABSTRACT`    | ending reflection lacks enough concrete carry-over from earlier sections |


## 8. Output Contract

H-03 should be renderable as either JSON or Markdown.

Recommended JSON shape:

```json
{
  "score_version": "0.1",
  "video_id": "amazon_ai_monitoring",
  "total_score": 74,
  "band": "acceptable",
  "category_scores": {
    "scene_variety": 3,
    "information_embedding": 2,
    "symbolic_asset": 3,
    "tempo_shift": 2,
    "pattern_balance": 2,
    "stagnation_risk": 2,
    "promise_visual_payoff": 2
  },
  "warnings": [
    "VISUAL_DATA_PROMISE_UNPAID",
    "VISUAL_PATTERN_REPEAT"
  ],
  "best_supports": [
    "inhaler incident",
    "scanner / timer UI",
    "thank-you button versus legal text"
  ],
  "stagnation_points": [
    "PR section can become UI-heavy and noisy",
    "ending can become too abstract if earlier motifs do not return"
  ],
  "recommended_repairs": [
    "visualize 71.4% and Time Off Task as distinct on-screen beats",
    "compress PR section into three contrast frames",
    "reuse one earlier motif in the ending"
  ]
}
```

## 9. Relationship to H-01 / H-02 / H-04

H-03 should consume H-01 directly.

Use these fields first:

- `thumbnail_promise`
- `required_evidence`
- `thumbnail_controls`
- `must_payoff_by_section`
- `consumer_hints.for_h03`

H-02 is upstream packaging shape.

- H-02 says what the thumbnail is promising
- H-03 checks whether the section plan creates enough visual payoff for that promise

H-04 is sibling evidence diagnosis.

- H-04 checks whether the body has enough factual support
- H-03 checks whether that support is likely to become visible on screen

## 10. Acceptance for H-03 "Defined"

H-03 can be treated as defined enough to implement or proof once the following are true:

1. score categories are fixed
2. warning classes are fixed
3. H-01 dependency is explicit
4. one real sample can be scored manually using cue memo plus brief
5. result can produce a visual repair suggestion, not just a total score

