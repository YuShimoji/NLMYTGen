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

## Clarified Diagnostic Semantics

This variant explains a game-mechanics cause-and-effect structure, not the
atmosphere of a game screen. The focal chain should be read as:

```text
player input / state -> collision or rule check -> resulting feedback
```

The current diagnostic JSON/readback still uses `内部ルール` as the middle focal
label. That readback remains valid, but the revise target clarifies what the
label must mean: the middle node is the judgement step where the game resolves
whether the player's action or state becomes a valid event. For first review,
read that node as `判定 / 当たり判定`.

| Chain step | Clarified meaning | Preferred first-review wording |
| --- | --- | --- |
| player input / state | player action, timing, or current state entering the rules | `入力操作` |
| collision or rule check | internal judgement that resolves hit / miss / valid / invalid / state transition | `判定 / 当たり判定` |
| resulting feedback | visible result after the judgement resolves | `画面上の結果` |

`判定 / 当たり判定` is not an additional fourth node. It is the concrete first
example that sharpens the existing `内部ルール / 判定` middle node. A later
diagnostic JSON/report revision may rename or emphasize the middle label, but
this semantics clarification does not require a generator change or new variant.

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

Callout density remains bounded at 2-3. For a medium-caption shot, the safest
first-review read is:

- required: `判定 / 当たり判定`
- optional supporting: one or both of `操作感`, `リスクとリターン`

If all three are visible, the two supporting callouts should read as downstream
consequences, not parallel proof cards. Avoid indexed whiteboard layout, dense
tables, long bullets, and source-note style labels.

## Host And Caption Rules

- Hosts remain lower-corner non-focal decoration / emotional anchor.
- Hosts must not become proof, evidence, or the first reading target.
- Medium caption density is acceptable.
- If three callout slots are visible, in-frame text must stay short.
- Caption reserve remains protected; do not add lower text or source notes.

## Next Revision Boundary

The current clarification is sufficient as a diagnostic semantics correction.
No generator change, new variant generation, `.ymmp`, render, production
promotion, or YMM4 probe is needed in this slice.

If a later explicit diagnostic-artifact revision is opened, the minimum useful
change would be to update the game-mechanics artifact's semantic label/readback
wording so the focal chain reads as `入力操作` -> `判定 / 当たり判定` -> `画面上の結果`
or an equivalent short middle-node label. That later change should preserve:

- 3-node focal chain
- 2-3 callouts
- bottom caption reserve
- non-focal host role
- `dense_table=false`
- `indexed_whiteboard=false`
- no external image, URL, gameplay capture, or raw reference handling

## Safe Next Action

The next safe action is to use this note as the clarified revision input for a
narrow diagnostic JSON/report label pass, only if explicitly requested, or for a
later scoped carrier review. Semantics-note clarification alone is enough to
close the current revise-clarification slice.

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
