# H-02 Thumbnail Strategy Dry Proof

> Date: 2026-04-06
> Sample: `AI監視が追い詰める生身の労働`
> Scope: repo-local dry proof using Packaging brief, thumbnail strategy spec, and existing script/cue artifacts
> Result type: specificity / banned-pattern / rotation contract check, not final GUI rerun proof

## Inputs

- script: `samples/AI監視が追い詰める生身の労働.txt`
- packaging brief: `samples/packaging_brief_ai_monitoring.md`
- thumbnail strategy spec: `docs/THUMBNAIL_STRATEGY_SPEC.md`
- thumbnail prompt: `docs/S8-thumbnail-copy-prompt.md`
- cue memo reference: `samples/AI監視が追い詰める生身の労働_cue_memo_received.md`

## Goal

Verify that H-02 is specific enough to make C-08 prefer concrete evidence over
abstract hype, exclude banned copy patterns, and return a readable rotation
recommendation before running a strict GUI comparison.

## Sample Constraints Read From Brief

| Constraint | Value |
|---|---|
| thumbnail_promise | 監視の強度と企業の建前のギャップを、割合や金額を使って一目で掴ませる |
| preferred_specifics | `71.4%`, `19億ドル`, `気温+1度で9%増` |
| banned_copy_patterns | `衝撃の真実`, `知らないと損`, `ヤバすぎる`, `閲覧注意` |
| preferred copy families | `number_fact`, `case_hook`, `contrast_fact` |
| preferred rotation | `number_left_character_right`, `confused_vs_angry`, `dark_blue_red_alert`, `number_fact` |

## Dry Assessment

| Check | Result | Notes |
|---|---|---|
| specificity-first constraint is explicit | pass | prompt now requires at least 3 of 5 main copies to include a `preferred_specific` unless the model explains why not |
| strongest evidence is inspectable | pass | `copy_family`, `strongest_evidence`, and `Specificity Ledger` make the evidence basis readable without guessing |
| banned pattern rejection is inspectable | pass | prompt now requires at least one explicit rejected pattern with a reason |
| rotation recommendation is inspectable | pass | 4-axis rotation output remains required and aligned with H-02 spec |
| brief compliance is inspectable | pass | prompt now ends with `Brief Compliance Check` for promise / overclaim / specificity-first |
| sample-specific good directions are identifiable | pass | `71.4%`, `吸入器で違反判定`, `19億ドル`, `感謝ボタンは免罪符か` are all repo-supported candidates |

## Good Candidate Shapes For This Sample

| Candidate shape | Why it fits |
|---|---|
| `71.4%が監視` | strongest specificity anchor; pays off early in body |
| `吸入器で違反判定` | strong human-scale hook; supports opening promise directly |
| `19億ドルの裏で何が起きた?` | money contrast is concrete and supports PR gap framing |
| `感謝ボタンは免罪符か` | contrast copy that stays inside the script's PR-vs-reality frame |

## Rejected / Weak Directions

| Candidate shape | Why it should be rejected or downgraded |
|---|---|
| `ヤバすぎる監視社会` | abstract hype with no strongest evidence visible |
| `知らないと損する労働の闇` | banned pattern + weak body payoff |
| `社会の闇が深すぎる` | no specificity, no promise anchor, no reusable rotation signal |

## Residual Risk

- `19億ドル` is strong but lands later than `71.4%` and the inhaler anecdote, so a money-first thumbnail can still outrun the opening if used carelessly.
- `9%増` is useful body evidence but may be secondary to `71.4%` on a first-pass thumbnail unless the copy explicitly frames road risk.
- This is still a dry proof. A same-sample GUI rerun is needed to show that actual thumbnail output moves away from abstract hype in practice.

## Minimal Operator Check

When running one strict GUI rerun for C-08, check only this:

- among the 5 main copy candidates, do at least 3 explicitly use one of `71.4%`, `19億ドル`, `9%増`, or the inhaler case, while avoiding banned patterns?

If yes, H-02 can be treated as workflow-proven enough to keep using.

## Assessment

| Item | Result |
|---|---|
| useful enough to keep using | yes |
| strongest improvement | H-02 now makes specificity usage and banned-pattern rejection inspectable instead of implicit |
| residual risk | no same-sample GUI rerun record yet |
| next improvement inside repo | use the same one-line operator check during the next C-08 rerun and then move to H-03 only if a new bottleneck remains |
