# G-28 Chat-first Visual Review Protocol - 2026-06-11

## Classification

`g28_chat_first_visual_review_protocol`

## Purpose

This protocol records the human review result for the G-28 reference layout
prototype pack and changes future G-28 visual review reporting from
file-open-first to chat-first / accumulated review.

The HTML/SVG visual-prototype-first route remains useful after the direct
coordinate-generated YMM4 method blocker, but a visual artifact is not
reviewable enough if the chat report only points to a file path. Future G-28
visual artifact reports must carry a compact digest that lets the reviewer make
a light decision in chat before deciding whether to open HTML, YMM4, or
screenshot evidence.

## Human Review Intake

| Field | Result |
| --- | --- |
| reviewed pack | `samples/_probe/g28/reference_layout_prototypes/index.html` |
| reviewed screens | `lecture_list`, `mechanism_diagram`, `map_evidence`, `cluster_map`, `evidence_table`, `conversation_board`, `source_footage_frame` |
| route judgement | HTML/SVG visual authoring first is a useful direction |
| review-method concern | Opening the HTML pack every time is too inefficient for repeated reviews |
| protocol change | Require a chat-readable digest for each future visual artifact report |
| rich-review mode | Defer detailed visual review until multiple artifacts accumulate, then review by tag / issue family |
| immediate implementation work | none |

The current prototype pack is usable as a reference surface, but not every
screen is transfer-ready. In particular, `mechanism_diagram` carries causal
diagram grammar debt and must not become a YMM4 transfer candidate without a
later revision or explicit accepted caveat.

The later revise-once expansion adds `object_catalog` and six content-first
simple layouts. Those additions follow the same digest contract and are
recorded in
`G28-LAYOUT-PRESET-OBJECT-CATALOG-2026-06-11.md`.

## Mechanism Diagram Note

| Field | Value |
| --- | --- |
| issue type | `causal_diagram_grammar_debt` |
| affected artifact | `mechanism_diagram` |
| current status | reviewable prototype, not transfer-ready |
| transfer gate | must-fix before YMM4 transfer planning |
| immediate fix in this slice | no |

The issue is not that the abstract structure is invalid. The problem is that
the arrows and boxes are not semantically coupled enough as a causal diagram.
The screen says, in effect, "important elements first, abstract statement last,"
but the middle of the diagram does not yet show enough concrete causal payload
to make the relation visible. A later revision should make the link between
inputs, mechanism, and outcome visible through meaningful box contents and
arrow relationships before any YMM4 transfer.

## Chat-first Digest Contract

Every future G-28 visual artifact report must include a digest before asking
the human to open a file.

| Digest field | Required content |
| --- | --- |
| artifact id | Stable artifact name, variant, and path. |
| visible summary | What a reviewer would see at a glance without opening the file. |
| primary focus | The main decision the artifact is meant to support. |
| layout grammar | The screen pattern being tested, such as list rhythm, mechanism diagram, map/evidence, table, conversation board, or footage frame. |
| object slots | Major visual objects / slots and their intended roles. |
| fulfilled specs | The constraints that are already satisfied. |
| known weak points | Caveats, debts, or suspected failure modes. |
| open-file trigger | The exact condition that makes HTML, YMM4, or screenshot inspection necessary. |
| accumulated review tags | Tags that should be carried into later cross-artifact review. |
| next decision options | The bounded decisions available next. |

File paths remain evidence, not the whole review surface. A report that only
links an HTML file, `.ymmp`, screenshot, or generated artifact is incomplete for
G-28 visual review.

## Review Levels

| Level | Name | Use when | Output |
| --- | --- | --- | --- |
| 1 | Chat-first digest | The artifact can be judged lightly from a faithful digest. | A chat decision, caveats, and tags. |
| 2 | Optional visual check | Spatial judgement, transfer readiness, or digest sufficiency is uncertain. | Browser / YMM4 / screenshot notes plus a decision. |
| 3 | Accumulated rich review | Several artifacts share repeated visual issues. | Cross-artifact review grouped by tags and issue families. |

Level 2 does not need to happen on every artifact. Level 3 should be opened
after enough artifacts accumulate to make cross-screen patterns visible.

## Accumulated Review Tags

Tags are routing aids for later rich review. They are not production approval
states and do not by themselves authorize a fix.

| Tag | Use for |
| --- | --- |
| `layout_system_debt` | Centering, spacing, split layout, or generalizability problems shared across screens. |
| `causal_diagram_grammar_debt` | Diagrams where arrows, boxes, and causal payload are not semantically coupled. |
| `density_debt` | Screens that are too sparse or too dense to judge quickly. |
| `content_slot_gap` | Screen grammar is plausible, but concrete slot contents are missing or too generic. |
| `subtitle_reserve_risk` | Bottom caption reserve or safe area is visually ambiguous. |
| `transfer_candidate` | Artifact appears suitable for a later bounded YMM4 transfer plan. |

Later rich review should group issues by tag, not only by individual artifact.
This keeps repeated review from turning into a file-by-file manual inspection
loop.

## Open-file Triggers

Opening HTML, YMM4, or screenshot evidence is required when:

- a report proposes YMM4 transfer or production-adjacent work
- the digest says `chat_digest_sufficient=no`
- a `must_fix` item depends on spatial judgement
- the reviewer needs to verify a tag such as `subtitle_reserve_risk`
- the artifact is a candidate for `transfer_candidate`
- the human explicitly asks for visual inspection

Opening a file is optional when:

- the digest is enough to decide `accept_with_caveats`, `hold`, or `revise_once`
- the artifact is only being logged as negative evidence
- the next action is accumulated review rather than immediate revision

## Human Return Format

```text
decision: accept / accept_with_caveats / revise_once / reject / redesign_required

overall:
-

chat_digest_sufficient:
- yes / no

prototype_notes:
- lecture_list:
- mechanism_diagram:
- map_evidence:
- cluster_map:
- evidence_table:
- conversation_board:
- source_footage_frame:
- object_catalog:
- image_annotation_simple:
- screenshot_callout:
- two_image_compare:
- article_quote_card:
- asset_plus_caption:
- source_footage_annotated:

must_fix:
-

nice_to_have:
-

do_not_fix_now:
-

accumulated_review_tags:
-

next_requested_action:
-
```

## Boundary Confirmation

This protocol is docs-only. It does not modify HTML prototypes, create or
modify any YMM4 `.ymmp`, create a YMM4 builder, regenerate generated YMM4
artifacts, modify existing game-mechanics or map-evidence carriers, render,
mark a production candidate, approve rights, claim creative final acceptance,
process Newsroom, touch common foundation, reopen G-27, touch ClipPipeGen, RSS
/ OPML / Inoreader / NotebookLM, run a real runner / `codex exec`, import
external images, or introduce raw reference material.
