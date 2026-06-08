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

## Reviewability Repair - 2026-06-08

Human review returned `decision: revise` while keeping Lecture Diagram Carrier
as the correct carrier. The issue was not carrier selection; the existing HTML
did not make the semantic labels visible enough for a human to judge the left
and right nodes or the callout slots.

The existing `game_mechanics_explanation` diagnostic artifact has now been
repaired in place rather than regenerated as a new variant. The HTML includes a
review-only overlay, and the readback/report include an inspector layer for the
same labels. Production visible text budget remains separate from review labels.

| Review surface | Human-visible labels now exposed | Boundary |
| --- | --- | --- |
| diagram chain | `入力操作`, `内部ルール`, `画面上の結果` | Review-only semantic labels; not production slot-fill. |
| callout slots | `操作感`, `判定 / 当たり判定`, `リスクとリターン` | Review-only callout meaning labels; not production copy approval. |
| readback inspector | `production_visible_text_items`, `review_visible_semantic_labels`, `review_label_layer_or_inspector_exists=true`, `semantic_labels_human_visible=true` | Diagnostic readback only. |

The repaired HTML remains visualization-only / review-only. It is not a render,
not production timing, not creative final acceptance, and not a Source-Footage
Carrier promotion.

## Reviewability Re-Repair - 2026-06-08

Human review then returned `decision: further revise`: the labels were visible,
but the HTML drew them as in-frame boxed overlays, making the left/right nodes,
callouts, and especially the center focal label look double-boxed. That problem
was review surface noise, not a carrier-selection failure.

The existing `game_mechanics_explanation` diagnostic artifact has now been
repaired in place again. The default 16:9 frame is clean: no review-only label
boxes are drawn over the diagram. Semantic labels remain human-visible in the
HTML review inspector below the frame and in readback fields.

| Review surface | Current behavior | Boundary |
| --- | --- | --- |
| 16:9 frame | Clean diagram frame; no in-frame review label overlay. | Diagnostic visualization only; not render output. |
| review inspector | Shows focal-chain and callout semantic labels in a table outside the frame. | Review-only labels; not production slot-fill. |
| readback inspector | Records `production_visible_text_items`, `review_visible_semantic_labels`, `review_label_layer_or_inspector_exists=true`, `semantic_labels_human_visible=true`, `production_text_budget_separate_from_review_labels=true`, `in_frame_review_overlay=false`, `review_overlay_default=false`, and `clean_frame_available=true`. | Diagnostic readback only. |

This re-repair does not create a new theme variant, carrier skeleton,
Source-Footage generator, `.ymmp`, render, production timing, or creative final
acceptance artifact.

## Review Surface Acceptance - 2026-06-08

Human review returned `decision: accept` for the repaired review surface while
keeping `carrier: Lecture Diagram Carrier`.

The accepted scope is review-surface usability only. The 16:9 frame no longer
has the double-box review overlay, and the clean frame is separated from the
Review Inspector. The frame alone does not show the left node, right node, or
callout meaning labels, but this is acceptable because the current design makes
semantic labels human-visible in the Review Inspector table.

| Review area | Accepted result | Still separate |
| --- | --- | --- |
| diagram chain | `入力操作 -> 内部ルール -> 画面上の結果` can be verified through the inspector table. | This is not production copy approval. |
| callouts | `操作感`, `判定 / 当たり判定`, and `リスクとリターン` are confirmable in the inspector without dirtying the frame. | The frame remains clean by default. |
| host | Hosts remain non-focal and do not become the main evidence. | Host visual acceptance for production is not claimed. |
| caption / density | Caption reserve is protected, and production-visible text is separated from review labels. | Production caption density remains a later slice. |

Accepted next action: record this as review surface accept. If needed, the next
safe work is only scoped condition planning for a YMM4-saved carrier review. Do
not proceed to Source-Footage, `.ymmp` generation, render, production timing, or
creative final acceptance from this acceptance record.

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
- Do not make further JSON, HTML, readback JSON, generated report, or generator
  changes unless the scope is another bounded diagnostic repair.
- Do not revive G-27 as an active blocker.
- Do not route back into RSS / OPML / Inoreader / NotebookLM work.

## Next Safe Action

| Human decision | Next safe action | Still not allowed |
| --- | --- | --- |
| accept | Consider a scoped YMM4-saved carrier review for this Lecture Diagram grammar. | Creative final acceptance, render, production timing, or source footage intake. |
| revise | Convert the human notes into diagram semantics changes or a narrow review plan. | New variant generation unless explicitly requested, production slot-fill, `.ymmp`. |
| reject: Source-Footage needed | Open a separate Source-Footage design-only checklist for frame, HUD protection, marker, and caption reserve. | Footage import, screenshot intake, image path/URL/raw reference commit. |
| reject: different carrier needed | Re-run the shot through the carrier selection worksheet with the revised shot purpose. | Treating this diagnostic artifact as failed production work. |
