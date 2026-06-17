# G-28 Reference Layout Prototype Pack - 2026-06-11

## Classification

`reference_layout_prototype_pack_created`

## Purpose

This packet switches the G-28 visual authoring route from direct
script-coordinate YMM4 `.ymmp` construction to HTML/SVG visual prototyping
before any YMM4 transfer.

The reason is the recorded blocker in
`G28-YMMP-CARRIER-GENERATION-METHOD-BLOCKER-2026-06-11.md`: the Map / Evidence
YMM4 probe passed structural readback but failed human visual review as a
practical screen. Readback pass is boundary / structure confirmation only, not
visual-quality assurance. The existing Map / Evidence `.ymmp`, builder,
readback, and report remain tracked as negative evidence / failed sample and
must not be regenerated or micro-tuned.

## Created Prototype Pack

| Prototype | HTML | Purpose |
| --- | --- | --- |
| `index` | `samples/_probe/g28/reference_layout_prototypes/index.html` | Review hub linking the original fixed-canvas prototypes, object catalog, and content-first additions. |
| `lecture_list` | `samples/_probe/g28/reference_layout_prototypes/lecture_list.html` | Dark explainer list with icon rhythm, numbers, short terms, dot leaders, host placeholder, and subtitle reserve. |
| `mechanism_diagram` | `samples/_probe/g28/reference_layout_prototypes/mechanism_diagram.html` | Two schematic panels with arrows, OK/NG comparison, and central explanation. |
| `map_evidence` | `samples/_probe/g28/reference_layout_prototypes/map_evidence.html` | Abstract map/evidence surface with labels, source note area, and bottom claim band. |
| `cluster_map` | `samples/_probe/g28/reference_layout_prototypes/cluster_map.html` | Abstract satellite/map-like surface with points, leader lines, and label clusters. |
| `evidence_table` | `samples/_probe/g28/reference_layout_prototypes/evidence_table.html` | Dark multi-column evidence table with readable density and lower short claim. |
| `conversation_board` | `samples/_probe/g28/reference_layout_prototypes/conversation_board.html` | Central board, left/right abstract host placeholders, subtitle reserve, and dialogue pacing space. |
| `source_footage_frame` | `samples/_probe/g28/reference_layout_prototypes/source_footage_frame.html` | Central footage placeholder with top title, lower telop, frame/safe area, and no actual footage. |
| `object_catalog` | `samples/_probe/g28/reference_layout_prototypes/object_catalog.html` | Visual object preset catalog for reusable slots, parameters, transfer cautions, and misuse risks. |
| `image_annotation_simple` | `samples/_probe/g28/reference_layout_prototypes/image_annotation_simple.html` | Large image placeholder with two or three annotation labels, arrows, highlight boxes, and subtitle reserve. |
| `screenshot_callout` | `samples/_probe/g28/reference_layout_prototypes/screenshot_callout.html` | UI / webpage screenshot placeholder with marker dots, callout boxes, source note, and subtitle reserve. |
| `two_image_compare` | `samples/_probe/g28/reference_layout_prototypes/two_image_compare.html` | Left / right or before / after placeholders with difference labels and one short bottom claim. |
| `article_quote_card` | `samples/_probe/g28/reference_layout_prototypes/article_quote_card.html` | Document / article placeholder with a short quote highlight, source note, and interpretation label. |
| `asset_plus_caption` | `samples/_probe/g28/reference_layout_prototypes/asset_plus_caption.html` | One dominant asset placeholder with a strong lower telop and optional side note. |
| `source_footage_annotated` | `samples/_probe/g28/reference_layout_prototypes/source_footage_annotated.html` | Footage placeholder with safe-area marks, arrows, labels, lower telop, and no actual footage. |

## Prototype Contract

- Fixed `1920x1080` / `16:9` canvas.
- Self-contained HTML/CSS/SVG only.
- No external links, external images, image paths, raw reference images,
  logos, third-party character reproduction, real map image, satellite image,
  source footage, audio, or TTS.
- Host figures are abstract placeholders only.
- Map/evidence surfaces are abstract geometry only.
- Subtitle reserve is visible in every prototype.
- Each prototype visibly marks grid, center, margins, and density intention.
- Each prototype includes an on-page note naming the abstracted grammar, what
  is intentionally not copied, and what should be reviewed before YMM4
  transfer.
- Content-first additions use explicit CSS variables for background, panel,
  text, muted text, accent, warning, grid, and subtitle reserve surfaces.
- The object catalog is a visual authoring catalog only; it is not an
  implementation schema or YMM4 transfer plan.

## Human Review Result - Chat-first Intake

| Field | Result |
| --- | --- |
| review classification | `accept_with_caveats_for_chat_first_review_protocol` |
| route judgement | HTML/SVG visual authoring first is useful after the YMM4 coordinate-generation method blocker. |
| review-method change | Future visual artifact reports need a chat-readable digest; a file path alone is not enough. |
| rich-review timing | Detailed visual review can be deferred until multiple artifacts accumulate, then reviewed by tag / issue family. |
| protocol owner | `docs/verification/G28-CHAT-FIRST-VISUAL-REVIEW-PROTOCOL-2026-06-11.md` |

The pack remains useful as a visual grammar reference, but the review process
should not require the human to open every HTML file before forming a light
decision. Future G-28 visual reports must summarize what is visible, what the
artifact is testing, what is already satisfied, what is weak, and exactly when
opening HTML / YMM4 / screenshot evidence becomes necessary.

### `mechanism_diagram` Caveat

`mechanism_diagram` is recorded as `causal_diagram_grammar_debt`.

The screen is reviewable as a prototype, but it is not a YMM4 transfer
candidate without later revision or explicit accepted caveat. The arrows and
boxes are not yet semantically coupled enough: the diagram structure implies
"important elements first, abstract statement last," while the middle of the
screen lacks enough concrete causal payload to make the relationship visible.

Do not fix this immediately in this slice. Treat it as a must-fix blocker only
if `mechanism_diagram` is selected for YMM4 transfer planning.

## Required Chat-first Digest For Future G-28 Visual Reports

Every future G-28 visual artifact report must include:

- artifact id
- visible summary
- primary focus
- layout grammar
- object slots
- fulfilled specs
- known weak points
- open-file trigger
- accumulated review tags
- next decision options

Review levels are:

| Level | Meaning |
| --- | --- |
| Level 1 | Chat-first digest for light decisions without opening files. |
| Level 2 | Optional visual check in browser, YMM4, or screenshot when spatial judgement is needed. |
| Level 3 | Accumulated rich review after multiple artifacts are available. |

Use accumulated tags such as `layout_system_debt`,
`causal_diagram_grammar_debt`, `density_debt`, `content_slot_gap`,
`subtitle_reserve_risk`, and `transfer_candidate` to group later rich review.

## Human Review Viewpoints

| Prototype | Look For |
| --- | --- |
| `lecture_list` | Whether the icon/list/dot-leader rhythm reads quickly without overcrowding the frame or stealing subtitle reserve. |
| `mechanism_diagram` | Whether OK/NG comparison, arrows, and central explanation create one clear mechanism reading path. |
| `map_evidence` | Whether the abstract evidence surface feels map/evidence-like without needing a real map image. |
| `cluster_map` | Whether points, leaders, and label clusters are readable without label collision or false real-location implication. |
| `evidence_table` | Whether the table is dense enough to feel evidence-rich while remaining legible as a screen. |
| `conversation_board` | Whether the central board stays dominant and abstract hosts remain pacing anchors, not character approvals. |
| `source_footage_frame` | Whether the frame, title, telop, and safe area read as a footage-carrier grammar without actual footage. |
| `object_catalog` | Whether the object presets are understandable as reusable visual slots with cautions and misuse risks. |
| `image_annotation_simple` | Whether a dominant image placeholder can carry two or three annotations without becoming a static mock. |
| `screenshot_callout` | Whether marker dots, callout boxes, and source note create a usable screenshot annotation grammar without a real capture. |
| `two_image_compare` | Whether two placeholders can be compared at matched scale with a short bottom claim. |
| `article_quote_card` | Whether quote, source note, and interpretation label work without copying source text. |
| `asset_plus_caption` | Whether one dominant asset plus lower telop gives a practical YouTube-simple layout. |
| `source_footage_annotated` | Whether footage-safe areas and annotation labels are readable without actual source footage. |

## Review Decision Conditions

The labels below are internal normalization targets, not required user reply
phrases. Human review may be freeform; the agent should parse it into target,
intent, constraints, and confidence, then map it to the closest internal
decision only when useful.

### Accept

Use `accept` when the original prototypes and content-first additions are
usable as visual grammar references:

- The screen reads as an intentional 16:9 composition at first glance.
- The grammar is clear enough to plan a later YMM4 transfer.
- Subtitle reserve, margins, and center line remain understandable.
- No prototype appears to copy a reference image, logo, character, map,
  satellite surface, company material, or source footage.
- Any remaining issues are minor enough to record as caveats without another
  design pass.

### Accept With Caveats

Use `accept_with_caveats` when the pack is usable for YMM4 transfer planning,
but specific screens need caution notes that should be carried into transfer
planning rather than fixed immediately.

### Revise Once

Use `revise_once` when one consolidated HTML/SVG revision can solve listed
`must_fix` issues without changing the route or reopening direct `.ymmp`
coordinate generation.

Examples:

- A prototype is too sparse or too dense to judge.
- A label cluster or table row is hard to read.
- A subtitle reserve is visually unclear.
- A host placeholder becomes too focal.
- A note is too vague to support later transfer review.

### Reject / Redesign Required

Use `reject` or `redesign_required` when the pack does not provide useful
screen-level visual grammar or when the route itself should change.

Examples:

- A prototype still feels like direct coordinate construction rather than a
  composition-first visual prototype.
- A map/evidence screen implies a real map or copied geography.
- A source-footage frame implies actual footage or screenshot use.
- Multiple prototypes cannot be judged as 16:9 screens without a broader
  redesign.

## YMM4 Transfer Gate

YMM4 transfer may be considered only after:

- Human freeform review is confidently normalized to `accept` or
  `accept_with_caveats`, or a completed `revise_once` pass is accepted.
- The selected prototype(s) have a clear visual grammar, safe areas, text
  budgets, and non-copied abstract assets.
- The transfer is opened as a separate bounded slice that defines what YMM4
  items, names, and human-authored surfaces are allowed.
- The transfer plan preserves diagnostic-only boundaries until a later explicit
  production decision.

Do not proceed to YMM4 transfer when:

- The human decision is `reject` or `redesign_required`.
- Any `must_fix` item remains unresolved after a `revise_once` pass.
- `mechanism_diagram` is selected while its
  `causal_diagram_grammar_debt` remains unresolved or unaccepted as a caveat.
- The proposed transfer would regenerate the failed Map / Evidence `.ymmp`,
  modify the game-mechanics carrier, create a builder, or resume direct
  coordinate-generated `.ymmp` visual authoring.
- The prototype depends on raw reference images, external material, real map or
  satellite imagery, source footage, logos, third-party character reproduction,
  or company-specific assets.
- The next action would imply render, production candidate status, rights
  approval, creative final acceptance, Newsroom intake, common foundation work,
  G-27, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, or real runner work.

## Review Card / Freeform Review Intake

When this pack needs human review, place a Review Card next to the artifact
digest instead of requiring a fixed return template. Freeform review is valid
input. The agent may normalize it internally to `accept`,
`accept_with_caveats`, `revise_once`, `reject`, or `redesign_required`.

Review Card contents:

- target: the prototype pack, a named prototype, or a tag family
- what to look at: at most three concrete points
- freeform review allowed: yes
- examples: short natural-language comments that mention direction, concern,
  or constraint
- how the agent will interpret it: target / intent / constraints / confidence
- completion signal: the agent can proceed when confidence is medium or high

Example freeform replies:

- `object catalog は使えそう。source_note と footage_slot の誤用注意だけ強めて。`
- `mechanism_diagram は因果が弱いので transfer_candidate から外して。`
- `全体は hold。HTMLをさらに開くより次の artifact を増やして。`

## Boundary Confirmation

This packet creates docs and static HTML only. It does not create or modify any
YMM4 `.ymmp`, YMM4 builder, existing game-mechanics carrier, existing
map-evidence carrier, generated YMM4 artifact, render, production candidate,
rights state, creative final acceptance, Newsroom path, common foundation path,
G-27 path, ClipPipeGen path, RSS / OPML / Inoreader / NotebookLM path, real
runner, external image, raw reference, or source-footage intake.
