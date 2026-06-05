# G-28 Game Mechanics Diagram Semantics Note - 2026-06-05

This note records the human `revise` response for the existing G-28 game
mechanics Lecture Diagram diagnostic artifact. It is a semantics note only. It
does not create a new theme variant, carrier skeleton, generator, source-footage
route, YMM4 project, render, production timing pass, or creative final acceptance
claim.

## Human Decision

| Field | Value |
| --- | --- |
| decision | revise |
| carrier | Lecture Diagram Carrier |
| current diagnostic precedent | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` |
| selected shot focus | hit detection / judgement first; control feel and risk/reward as supporting context |
| Source-Footage state | future-only backup, not opened by this decision |

## Diagram Chain Semantics

The existing direction is correct:

```text
入力操作 -> 内部ルール / 判定 -> 画面上の結果
```

The weak point is that `内部ルール` is too abstract for the first human review.
Keep the three-node chain, but make the middle node selectable as one concrete
internal process example.

| Node | Current meaning | Revised semantic role | First-review label guidance |
| --- | --- | --- | --- |
| 1 | player input | player action that enters the system | `入力操作` |
| 2 | internal rule / judgement | concrete internal processing example | primary: `判定 / 当たり判定`; optional later examples: `無敵時間`, `硬直` |
| 3 | on-screen result | visible outcome after the internal process resolves | `画面上の結果` |

Do not make all three internal examples visible at once. The carrier should keep
one concrete internal processing example in focus, with the others reserved as
future semantic substitutions if a later shot needs them.

## Callout Priority

The current three callouts are directionally valid, but the first review should
not treat all three as equal-weight claims.

| Priority | Callout | Role in first review | Display guidance |
| --- | --- | --- | --- |
| primary | `判定 / 当たり判定` | main explanatory axis | Keep as the first callout or the semantic emphasis around the middle node. |
| supporting | `操作感` | feel/readability consequence | Keep available, but do not compete with hit-detection explanation. |
| supporting | `リスクとリターン` | gameplay consequence | Keep available, but treat as downstream implication rather than the main proof. |

If medium caption density makes three callouts feel crowded, prioritize the
primary hit-detection callout and reduce the two supporting callouts to short
labels, muted slots, or later-shot notes. Do not convert the callouts into a
dense list or table.

## Host And Caption Rules

- Hosts remain lower-corner non-focal decoration / emotional anchor.
- Hosts must not become proof, evidence, or the first reading target.
- Medium caption density is acceptable.
- If three callout slots are visible, in-frame text must stay short.
- Caption reserve remains protected; do not add lower text or source notes.

## Safe Next Action

The next safe action is to use this note as the revision input for a narrow
diagram semantics plan or a later scoped carrier review.

Still forbidden in this slice:

- No new theme variant generation.
- No Source-Footage Carrier work.
- No gameplay screenshot or source footage intake.
- No image path, URL, or raw reference recording.
- No `.ymmp` generation.
- No render, production timing, or creative final acceptance.
- No generated JSON / HTML / readback / report modification.
- No G-27 active blocker revival.
- No RSS / OPML / Inoreader / NotebookLM work.
