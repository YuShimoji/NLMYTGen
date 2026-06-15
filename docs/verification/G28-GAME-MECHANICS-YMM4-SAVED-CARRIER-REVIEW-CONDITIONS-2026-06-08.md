# G-28 Game Mechanics YMM4-Saved Carrier Review Conditions - 2026-06-08

This note defines the conditions for moving the accepted
`game_mechanics_explanation` diagnostic review surface into a scoped
YMM4-saved carrier review. It is a condition checklist only. It does not create
a YMM4 project, does not generate `.ymmp`, does not render, does not run
production timing, and does not claim creative final acceptance.

## Review Scope

| Field | Value |
| --- | --- |
| target shot | Game mechanics explanation. |
| selected carrier | Lecture Diagram Carrier. |
| diagnostic precedent | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` |
| accepted state | Review surface accepted after repair; not production approval. |
| accepted review surface | Clean 16:9 HTML frame plus lower Review Inspector separation. |
| current boundary | `diagnostic_only=true`, `production_candidate=false`. |
| future-only backup | Source-Footage Carrier, only if a separate later slice says real gameplay footage itself must be inspected. |

The accepted diagnostic surface establishes that a human can understand the
carrier semantics: `入力操作` -> `内部ルール` -> `画面上の結果`, with `操作感`,
`判定 / 当たり判定`, and `リスクとリターン` as review-visible callout meanings.
That acceptance does not approve a YMM4 carrier, a production layout, a render,
or final creative quality.

## Conditions Before YMM4-Saved Carrier Review

Move to a scoped YMM4-saved carrier review only when all required inputs below
are available. This slice does not produce those inputs.

| Condition | Required return | Why it matters |
| --- | --- | --- |
| Human explicitly selects YMM4-saved carrier review | A note that this review targets a YMM4-saved carrier for the game-mechanics Lecture Diagram Carrier. | Prevents treating HTML diagnostic acceptance as automatic YMM4 approval. |
| Carrier path is supplied | Repo-relative or user-supplied carrier path for the YMM4-saved project under review. | Gives the review a concrete artifact without generating a new `.ymmp` in this slice. |
| Preview screenshot is available | Preview screenshot or equivalent human-visible proof of the carrier frame. | Lets the reviewer judge the actual YMM4 visual surface rather than the HTML precedent. |
| Timeline screenshot is available | Timeline screenshot or equivalent proof of the relevant YMM4 section. | Confirms that the inspected surface is a saved carrier state, not a detached mock. |
| Item or layer confirmation is available | Item/layer names or screenshots sufficient to identify title, focal chain, callouts, hosts, and caption reserve. | Lets later readback or review notes connect human findings to stable carrier structure. |
| Bottom caption safe area can be checked | Human note or screenshot showing bottom caption reserve is clear. | Keeps subtitle/caption collision from being hidden until production timing. |

If any required input is missing, the safe next action is to request the missing
review evidence. Do not fill the gap by generating `.ymmp`, importing gameplay
footage, rendering, or promoting the HTML diagnostic artifact.

## What To Check In YMM4

| YMM4 review point | Accept signal | Revise signal |
| --- | --- | --- |
| Title readability | `操作と結果の関係` is readable without crowding the frame. | Title is too small, too low-contrast, clipped, or competes with the diagram. |
| Diagram chain | `入力操作` -> `内部ルール` -> `画面上の結果` remains visually understandable. | The left/right node roles or middle rule/judgement role become ambiguous. |
| Callout density | `操作感`, `判定 / 当たり判定`, and `リスクとリターン` are readable and not table-like. | Callouts are crowded, too tiny, too similar, or overpower the main chain. |
| Host role | Host stays non-focal and does not read as evidence or proof. | Host competes with the mechanism, blocks attention, or implies source authority. |
| Caption reserve | Bottom caption safe area remains clear. | Diagram, callouts, or hosts collide with the caption reserve. |
| Text separation | Production visible text and review labels remain distinguishable. | Review labels appear to have become production copy or slot-fill approval. |

The YMM4 review is allowed to produce a human `accept`, `revise`, or `reject`
decision for the saved carrier review surface. It still must not be interpreted
as production render approval, production timing approval, rights/public-use
approval, or creative final acceptance.

## Human Return Format

Return the smallest notes needed to make the next move unambiguous.

```text
decision: accept / revise / reject
carrier:
diagram chain note:
callout note:
host note:
caption / density note:
YMM4-specific issue:
next requested action:
```

Use `accept` only when the saved YMM4 carrier is good enough as a diagnostic
review surface. Use `revise` when the carrier concept is right but placement,
readability, density, caption reserve, host emphasis, or label separation needs
another bounded diagnostic pass. Use `reject` when the saved carrier should not
represent this game-mechanics Lecture Diagram review surface.

## Hard Boundaries

- Do not generate `.ymmp` in this condition-planning slice.
- Do not render.
- Do not run production timing.
- Do not claim creative final acceptance.
- Do not approve production carrier status.
- Do not create a Source-Footage Carrier generator.
- Do not intake source footage.
- Do not intake gameplay screenshots.
- Do not add image paths, URLs, or raw references.
- Do not modify existing JSON / HTML / readback / report / generator artifacts.
- Do not return to G-27 as an active blocker.
- Do not route back into RSS / OPML / Inoreader / NotebookLM work.

## Safe Next Move

| If the user wants to proceed | Ask for / inspect | Still out of scope |
| --- | --- | --- |
| YMM4-saved carrier review | Carrier path, preview screenshot, timeline screenshot, item/layer confirmation, caption safe-area evidence. | `.ymmp` generation, render, production timing, creative final acceptance. |
| More diagnostic planning | Clarify which YMM4 evidence fields are hard to provide and write a smaller review request. | Filling missing evidence with generated assets. |
| No YMM4 review yet | Keep the accepted HTML/readback precedent as the current diagnostic surface. | Treating accept as production completion. |
