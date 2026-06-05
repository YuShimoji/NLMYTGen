# G-28 Game Mechanics Human Review Packet - 2026-06-05

This packet lets a human judge the existing G-28 Lecture Diagram diagnostic
artifact for one game-mechanics shot. It is not a new theme variant, carrier
skeleton, generator, YMM4 project, render, production timing pass, source intake,
or creative final acceptance artifact.

## Review Target

| Field | Value |
| --- | --- |
| shot | Game mechanics explanation: hit detection, control feel, and risk/reward. |
| selected carrier | Lecture Diagram Carrier. |
| backup carrier | Source-Footage Carrier, future-only. Use only if a later production slice says real gameplay footage itself must be inspected as evidence. |
| decision source | `docs/verification/G28-SHOT-CARRIER-SELECTION-GAME-MECHANICS-2026-06-05.md` |
| diagnostic precedent | `samples/_probe/g28/lecture_diagram_carrier_game_mechanics_explanation.*` |
| readback state | Passed; `diagnostic_only=true`, `production_candidate=false`, no `.ymmp`, no render, no external image or URL. |

## What To Judge

| Review question | Accept signal | Revise signal |
| --- | --- | --- |
| Does the diagram communicate input operation -> internal rule / judgement -> on-screen result? | The viewer can explain the three-step relationship without needing footage. | The node chain feels too abstract, too generic, or unclear about which part is player input, rule judgement, or visible result. |
| Are the callouts for control feel, judgement / hit detection, and risk/reward useful? | The callouts add meaning without becoming a list or table. | A callout is missing, duplicated, too vague, or too detailed for a medium-caption shot. |
| Does the host stay non-focal? | Hosts read as lower-corner emotional anchors only. | A host competes with the diagram, reads as proof, or distracts from the input/rule/result chain. |
| Is caption reserve protected? | Bottom caption area remains visually safe and the diagram can coexist with medium caption density. | The focal group, callouts, or hosts look likely to collide with subtitles or compete with spoken explanation. |
| Is the information density controlled? | The screen avoids gameplay screenshot overload, indexed whiteboard feel, and host-as-proof. | The screen needs fewer labels, fewer callouts, a split shot, or a different carrier. |

## Human Response Format

Return one of these decisions. Add only the notes needed to make the next move
unambiguous.

```text
decision: accept / revise / reject
carrier: Lecture Diagram Carrier / Source-Footage Carrier / other
diagram chain note:
callout note:
host note:
caption / density note:
next requested action:
```

Use `accept` when the existing Lecture Diagram grammar is good enough for a
scoped follow-up review. Use `revise` when the carrier is right but semantics,
labels, callouts, host balance, or density need adjustment. Use `reject` when the
shot should not use this diagnostic Lecture Diagram precedent.

## Common Revise Patterns

| Pattern | What to return | Safe next action |
| --- | --- | --- |
| Node names are too abstract | Name which node is unclear and what concrete role it should express. | Revise diagram semantics only; do not generate a new theme variant by default. |
| Callouts are too many / too few | Name which callout to keep, cut, merge, or add conceptually. | Update review notes or a future semantics plan; do not slot-fill production text here. |
| Source-Footage is needed | State that the gameplay screen itself must be inspected as evidence. | Open a separate Source-Footage design-only checklist slice; do not intake footage here. |
| Caption and information density may collide | State whether the issue is bottom reserve, label count, callout density, or shot length. | Split the shot or reduce in-frame labels in a later design pass. |
| Host reads as proof | Say whether to hide, shrink, mute, or move host emphasis. | Keep host as non-focal decoration; do not turn host into evidence. |

## Hard Boundary

- This packet is not creative final acceptance.
- This packet is not G-28 production completion.
- Do not generate `.ymmp`.
- Do not render.
- Do not run production timing.
- Do not ask for gameplay footage, screenshots, image paths, URLs, or raw
  references.
- Do not create a Source-Footage Carrier generator.
- Do not create a new carrier skeleton.
- Do not add a new theme variant by default.
- Do not modify existing JSON, HTML, readback JSON, generated reports, or
  generators.
- Do not revive G-27 as an active blocker.
- Do not route back into RSS / OPML / Inoreader / NotebookLM work.

## Next Safe Action

| Human decision | Next safe action | Still not allowed |
| --- | --- | --- |
| accept | Consider a scoped YMM4-saved carrier review for this Lecture Diagram grammar. | Creative final acceptance, render, production timing, or source footage intake. |
| revise | Convert the human notes into diagram semantics changes or a narrow review plan. | New variant generation unless explicitly requested, production slot-fill, `.ymmp`. |
| reject: Source-Footage needed | Open a separate Source-Footage design-only checklist for frame, HUD protection, marker, and caption reserve. | Footage import, screenshot intake, image path/URL/raw reference commit. |
| reject: different carrier needed | Re-run the shot through the carrier selection worksheet with the revised shot purpose. | Treating this diagnostic artifact as failed production work. |
