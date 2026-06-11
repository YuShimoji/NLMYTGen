# G-28 Game Mechanics YMM4 Batch Visual Review Packet - 2026-06-11

This packet replaces the previous two-point visual recheck for the G-28
`game_mechanics_explanation` YMM4 diagnostic carrier. The right focal label and
lower callout labels remain known review points, but they are no longer the
only points to inspect. The next human review should look at the whole YMM4
preview surface in one batch and return one decision.

## Review Scope

| Field | Value |
| --- | --- |
| target carrier | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp` |
| carrier kind | `lecture_diagram_carrier` |
| variant | `game_mechanics_explanation` |
| diagnostic only | `true` |
| production candidate | `false` |
| external image / URL / source footage / audio / TTS counts | all zero in readback |
| render / production / rights / creative final acceptance | not included |
| new variant | no |
| redesign in this slice | no |

This is a review protocol for an existing diagnostic carrier. It does not ask
for a YMM4 carrier fix, builder change, regeneration, render, production
approval, rights change, or creative final acceptance.

## Current Known State

`27b4736 fix: align G-28 game mechanics YMM4 labels` is accepted as a one-pass
targeted layout fix for the existing YMM4 diagnostic carrier:

- Right focal label `画面上の結果`: font size 38, inherited rightward nudge
  removed, same text and node geometry preserved.
- Lower callout labels `操作感`, `判定 / 当たり判定`, and `リスクとリターン`: common
  centered callout rule at font size 28.
- Readback classification:
  `pass_game_mechanics_ymmp_label_layout_fixed`.
- Readback flags: `one_pass_targeted_fix=true` and
  `no_further_micro_tuning_recommended=true`.
- Readback fit checks passed for the right focal label, lower callout
  centering, and label overflow.

These fixed labels are now part of the batch review checklist. They should not
drive a new single-label tuning loop by themselves.

## Batch Visual Review Checklist

| Review row | What to check | Accept condition | Revise trigger | Default severity |
| --- | --- | --- | --- | --- |
| overall composition | The full 16:9 preview as one screen, including focal chain, callouts, hosts, and caption reserve. | The screen reads as one coherent diagnostic diagram without requiring item-by-item explanation. | The screen feels fragmented, unbalanced, or too confusing to review as a carrier. | must-fix |
| focal chain meaning | `入力操作 -> 内部ルール / 判定 -> 画面上の結果` reads in that order. | A reviewer can identify cause / rule / result in a single pass. | The order, arrows, or visual grouping make the chain ambiguous. | must-fix |
| central focal priority | `内部ルール / 判定` acts as the visual anchor. | The center node carries the main concept without overpowering every other element. | Left or right nodes, callouts, or hosts steal the main focal role. | must-fix |
| right focal label fit | `画面上の結果` fits inside the right focal node. | The label has visible breathing room and no clipped or cramped appearance. | It still looks squeezed, clipped, or off-center enough to interrupt review. | must-fix |
| lower callout label centering | `操作感`, `判定 / 当たり判定`, and `リスクとリターン` sit centered within their callout boxes. | The labels look intentionally centered as a set, not individually hand-placed. | Any lower callout reads visibly left/right-shifted enough to pull attention. | must-fix |
| callout meaning and count | The three callouts support the game-mechanics explanation without becoming a dense table. | Count is three, meanings are distinct, and each supports the focal chain. | Callouts feel redundant, too many, too sparse, or unrelated to the chain. | must-fix |
| label readability | All visible labels can be read at preview scale. | Text is legible without zooming and remains diagnostic copy, not production final copy. | Any key label cannot be read at normal preview size. | must-fix |
| spacing / margins | Internal margins around labels, nodes, callouts, and main canvas edges. | Spacing feels deliberate and no main element crowds another. | Overlap, near-touching, or edge pressure makes the screen hard to inspect. | must-fix |
| visual density | The screen stays diagram-like, not table-like or annotation-heavy. | Viewers can understand the structure before reading every label. | The preview becomes visually noisy or overloaded. | must-fix |
| host non-focal role | Lower-corner hosts stay decorative / emotional anchor only. | Hosts do not compete with the focal chain or imply production character approval. | Hosts become a primary focal object or distract from the diagram. | nice-to-have |
| bottom caption reserve | Bottom caption safe area remains visually clear. | The reserve area is not occupied by diagnostic diagram elements. | Any visible element intrudes into the caption area. | must-fix |
| eye flow | The viewer's gaze moves title -> focal chain -> callouts without backtracking confusion. | Eye flow supports one quick review pass. | The viewer has to hunt for the next meaningful element. | nice-to-have |
| generic carrier transferability | The screen still proves a reusable Lecture Diagram carrier, not a one-off game graphic. | The structure could plausibly transfer to another explanation topic. | The layout depends on game-specific hacks that would not generalize. | nice-to-have |
| YMM4 item / layer maintainability | Timeline/item structure looks understandable in YMM4. | A human can identify title, focal nodes, labels, callouts, hosts, and reserve without searching. | Timeline/layer organization blocks basic review or future maintenance. | nice-to-have |
| diagnostic usefulness | The carrier helps decide whether this archetype is useful for game-mechanics explanations. | The preview answers the diagnostic question even if not production-ready. | The screen is too unclear to evaluate the carrier's value. | must-fix |

## Human Return Format

Use this exact format:

```text
decision: accept / accept_with_caveats / revise_once / layout_system_debt / redesign_required

overall:
-

must_fix:
-

nice_to_have:
-

do_not_fix_now:
-

notes:
-
```

## Severity Rules

- Only `must_fix` items can drive the next revision.
- `nice_to_have` items are recorded but not fixed immediately.
- `do_not_fix_now` items are explicitly parked.
- If `revise_once` is selected, all `must_fix` items must be handled in one
  consolidated fix.
- After one consolidated fix, do not continue same-screen pixel tuning.
- If issues remain after one consolidated fix, classify them as
  `layout_system_debt` or `redesign_required`.

## Decision Guidance

| Decision | Meaning |
| --- | --- |
| `accept` | Good enough as a diagnostic review surface; no immediate fix. |
| `accept_with_caveats` | Usable with noted caveats; no immediate fix. |
| `revise_once` | One consolidated fix is justified for listed `must_fix` items. |
| `layout_system_debt` | Layout rules are weak; do not keep tuning this screen. |
| `redesign_required` | Current carrier structure is not reviewable as a diagnostic surface. |

## Human Hands-on Steps

1. Open
   `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation_ymmp_diagnostic_probe.ymmp`
   in YMM4.
2. Look at the whole preview, not only the two labels fixed in `27b4736`.
3. Optionally save a preview screenshot under
   `samples/_probe/g28/game_mechanics_batch_review_preview_2026-06-11.png`.
4. Optionally save a timeline screenshot under
   `samples/_probe/g28/game_mechanics_batch_review_timeline_2026-06-11.png`.
5. Return the human review format above.

The optional screenshots are human-supplied review evidence. This packet does
not generate or commit them.

## Boundaries

Do not:

- modify `.ymmp`
- modify the builder
- regenerate artifacts
- create a new variant
- render
- mark the carrier as a production candidate
- change rights status
- claim creative final acceptance
- process Newsroom
- touch common foundation
- reopen real-estate work
- revive G-27
- touch GUI
- touch ClipPipeGen
- touch RSS / OPML / Inoreader / NotebookLM
- touch `.claude/worktrees/`
- touch `samples/2026-05-16.ymmp`
- run or enable a real runner / `codex exec`

## Next Safe Entry

The next safe action is human YMM4 batch visual review using the return format
above. If the decision is `revise_once`, do exactly one consolidated fix for
the listed `must_fix` items. If the decision is `accept`,
`accept_with_caveats`, `layout_system_debt`, or `redesign_required`, do not
start pixel tuning from this packet.
