# G-28 Layout Preset Object Catalog - 2026-06-11

## Classification

`g28_reference_layout_pack_revise_once_object_catalog`

## Purpose

This revise-once slice expands the G-28 reference layout prototype pack from a
screen-mock set into a small reusable layout / object / content-slot system.

The goal is not to make production HTML, YMM4 carriers, or final visual
acceptance. The goal is to make future G-28 reports easier to judge in chat:
which object slots exist, which simple content-first layouts can receive an
image / screenshot / footage placeholder, and what should trigger opening the
HTML pack for visual review.

## Added Review Surfaces

| Artifact | Path | Purpose |
| --- | --- | --- |
| `object_catalog` | `samples/_probe/g28/reference_layout_prototypes/object_catalog.html` | Visual preset catalog for reusable object slots, parameters, YMM4 cautions, and misuse risks. |
| `image_annotation_simple` | `samples/_probe/g28/reference_layout_prototypes/image_annotation_simple.html` | One dominant image placeholder with two or three annotation labels, arrows, highlight boxes, and caption reserve. |
| `screenshot_callout` | `samples/_probe/g28/reference_layout_prototypes/screenshot_callout.html` | UI / webpage screenshot placeholder with marker dots, callout boxes, source note, and caption reserve. |
| `two_image_compare` | `samples/_probe/g28/reference_layout_prototypes/two_image_compare.html` | Left / right or before / after image placeholders with difference labels and one short bottom claim. |
| `article_quote_card` | `samples/_probe/g28/reference_layout_prototypes/article_quote_card.html` | Document / article card placeholder with a short quote highlight, interpretation label, and bounded source note. |
| `asset_plus_caption` | `samples/_probe/g28/reference_layout_prototypes/asset_plus_caption.html` | YouTube-simple layout with one dominant asset placeholder, strong lower telop, optional side note, and caption reserve. |
| `source_footage_annotated` | `samples/_probe/g28/reference_layout_prototypes/source_footage_annotated.html` | Footage frame placeholder with safe-area marks, arrows / labels, lower telop, and caption reserve. |

`index.html` now links to `object_catalog.html` and the six content-first
prototype pages by local file navigation. `object_catalog.html` also links back
to the index and out to the six content-first layout pages.

## Object Preset Catalog

The catalog is a visual authoring catalog, not an implementation schema.

| Object preset | Role | YMM4 transfer caution | Misuse risk |
| --- | --- | --- | --- |
| `image_slot` | Abstract still / asset area. | Replace only after rights and source approval. | Fake real media. |
| `screenshot_slot` | UI or webpage capture frame. | Verify source rights and capture provenance first. | Implies a real capture when none exists. |
| `footage_slot` | Video frame region. | Prototype must not embed footage. | Source-footage claim without evidence. |
| `highlight_box` | Mark a content area. | Keep above the media layer and out of subtitles. | Covers key text. |
| `arrow` | Direct attention. | Avoid implying false causality. | Overclaims relation. |
| `leader_line` | Attach label to a point. | Preserve anchor target in transfer. | Label drift. |
| `label_chip` | Short tag. | Cap text length. | Becomes a paragraph. |
| `callout_box` | Explain a marked area. | Do not crowd caption reserve. | Turns into a mini slide deck. |
| `lower_third_telop` | Short narrated claim above subtitles. | Keep above subtitle reserve. | Subtitle collision. |
| `source_note` | Bounded provenance. | Never paste URLs, tokens, or raw private source strings. | Fake source authority. |
| `quote_card` | Short excerpt container. | Keep quote short and compliant. | Full article copy. |
| `comparison_panel` | Matched before / after pair. | Keep both sides at the same visual scale. | Unfair comparison. |
| `table_row` | Compact evidence row. | Avoid tiny text. | Unreadable density. |
| `host_placeholder` | Pacing / emotional anchor. | Do not treat as character approval. | Steals focus. |
| `caption_reserve` | Bottom subtitle band. | Never place content in it. | Caption collision. |

## Theme Tokens

The new pages define explicit CSS variables for:

- `background`
- `panel` / `panel2` or card surfaces
- `text`
- `muted`
- `accent`
- `warning`
- `grid`
- `subtitle`

This keeps the prototype review independent from browser light / dark mode
auto styling. The pages remain intentionally static and do not add a theme
switcher.

## Chat-first Review Digest

| Digest field | Value |
| --- | --- |
| artifact id | G-28 reference layout prototype pack revise_once / object preset catalog |
| visible summary | The pack now includes an object catalog and six content-first simple layouts for image, screenshot, comparison, quote, asset + caption, and annotated footage placeholders. |
| primary focus | Move G-28 from static mock review toward reusable edit presets and content slots without entering YMM4 transfer. |
| layout grammar | Content-first annotation, screenshot callout, two-image comparison, article quote card, asset plus caption, and source-footage annotation. |
| object slots | `image_slot`, `screenshot_slot`, `footage_slot`, `highlight_box`, `arrow`, `leader_line`, `label_chip`, `callout_box`, `lower_third_telop`, `source_note`, `quote_card`, `comparison_panel`, `table_row`, `host_placeholder`, `caption_reserve`. |
| fulfilled specs | Self-contained HTML/CSS/SVG, no external assets, no external URLs, fixed `1920x1080`, visible subtitle reserve, local navigation, no YMM4 transfer. |
| known weak points | The new content-first layouts are still schematic; `mechanism_diagram` remains `causal_diagram_grammar_debt` and outside this revision. |
| open-file trigger | Open `index.html` and `object_catalog.html` if the digest is enough to start visual review or if transfer-candidate tagging is being considered. |
| accumulated review tags | `content_slot_gap`, `transfer_candidate`, `density_debt`, `subtitle_reserve_risk`. |
| next decision options | Internal normalization may use `accept_with_caveats`, `revise_once`, `reject`, or `hold`; reviewer freeform text is valid and no fixed phrase is required. |

## Boundary Confirmation

This slice changes docs and static HTML only. It does not create or modify any
YMM4 `.ymmp`, create a YMM4 builder, modify the game-mechanics carrier, modify
the map-evidence carrier, regenerate generated YMM4 artifacts, render, mark a
production candidate, approve rights, claim creative final acceptance, process
Newsroom, touch common foundation, reopen G-27, touch ClipPipeGen, RSS / OPML /
Inoreader / NotebookLM, run a real runner / `codex exec`, import external
images, use raw reference material, or add real map / satellite / company /
character / footage assets.
