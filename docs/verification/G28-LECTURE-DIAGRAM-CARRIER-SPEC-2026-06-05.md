# G-28 Lecture Diagram Carrier Concrete Spec — 2026-06-05

G-28 `Reference-Driven Generic Screen Carrier` のうち、Lecture Diagram
Carrier を最初に concrete spec / diagnostic skeleton へ進める。

この文書は production carrier approval、creative final acceptance、render、
実素材 slot-fill の完了報告ではない。Agent は diagnostic skeleton generation、
SCS mapping、readback artifact 生成までは進められる。人間側に残るのは
creative final acceptance、production carrier 昇格、実素材登録、最終 YMM4
配置判断である。

## Boundary

- diagnostic skeleton generation: Agent-owned
- SCS mapping / readback checklist: Agent-owned
- HTML visualization / JSON readback: Agent-owned
- creative final acceptance: human-owned
- production render: not run
- production slot-fill: not run
- reference image copying / transformation / path or URL recording: forbidden
- G-27 diagnostic carrier promotion: forbidden
- RSS / OPML / Inoreader / NotebookLM source-pack work: out of scope

`.ymmp` は今回生成しない。理由は implementation impossibility ではなく、現行
G-28 v0.1 が YMM4 `.ymmp` zero-generation を非目的としており、まずは
JSON / HTML / readback artifact で frame contract と SCS compliance を固定する
変更境界だからである。

## Frame Contract

- frame: 1920 x 1080 / 16:9
- outer safe margin: 5%
- title area: x=96, y=54, w=1728, h=96
- main canvas: x=96, y=150, w=1728, h=660
- caption / thesis reserve: x=0, y=810, w=1920, h=216
- bottom outer safe: y=1026-1080
- main carrier items must not overlap caption / thesis reserve

## Title Area

Purpose: short chapter / section label only.

- item group: `G28_LDC_TitleBand`
- visible text slot: `G28_LDC_Title_Text`
- text budget: one short title, no paragraph explanation
- patch rule: title text may be replaced later if it stays within text budget
- forbidden: source notes, long claims, reference image names, URLs

## Focal Area

Purpose: central mechanism / evidence focus. The first diagnostic skeleton uses
`center-focal` rather than a dense fact table.

- item group: `G28_LDC_FocalGroup`
- focal anchor: `G28_LDC_Focal_Core`
- focal label: `G28_LDC_Focal_Label`
- internal nodes: `G28_LDC_Node_Left`, `G28_LDC_Node_Right`
- connectors: `G28_LDC_Connector_Left`, `G28_LDC_Connector_Right`
- rule: the whole focal group is one semantic focal anchor, even if it uses
  multiple ShapeItem primitives
- forbidden: 4+ nodes, dense table, equal-weight cards

## Caption Reserve

Purpose: protect YMM4 subtitle / thesis band from collision.

- reserve id: `G28_LDC_CaptionReserve`
- y range: 810-1026
- patch forbidden: true
- production carrier condition: all main items and callouts stay above y=810
- readback condition: `caption_reserve_clear=true`

## Host Role

Purpose: lower-corner emotional anchor only.

- items: `G28_LDC_Host_Left`, `G28_LDC_Host_Right`
- SCS role: `decoration`
- semantic role: optional host placeholder
- placement: lower left/right, above caption reserve
- forbidden: host overlaps focal area, host becomes first reading target, host
  blocks captions

## Callout Rule

Purpose: hold 2-3 optional explanation points after a theme-specific slot-fill
slice exists.

- items: `G28_LDC_CalloutSlot_1` to `G28_LDC_CalloutSlot_3`
- count rule: 2-3 active callout slots only
- diagnostic state: slots are empty shapes, not text-filled claims
- slot-fill rule: later text fill must keep in-frame labels and chars within SCS
  budget, or split the shot
- forbidden: bullet list, table rows, source body text

## Layer Order

1. `G28_LDC_BG_Stage`: low-salience dark stage
2. `G28_LDC_TitleBand_BG`: title band boundary
3. `G28_LDC_Title_Text`: short title
4. `G28_LDC_Focal_Core`: central focal panel
5. `G28_LDC_Focal_Label`: focal label
6. `G28_LDC_Node_Left` / `G28_LDC_Node_Right`: internal diagram nodes
7. `G28_LDC_Connector_Left` / `G28_LDC_Connector_Right`: connectors
8. `G28_LDC_CalloutSlot_1` to `G28_LDC_CalloutSlot_3`: empty callout slots
9. `G28_LDC_Host_Left` / `G28_LDC_Host_Right`: non-focal host placeholders

## SCS Mapping

- archetype: Lecture Diagram Carrier
- default composition type: `center-focal`
- alternate composition types for later variants: `chain`, `split`, `reveal`
- focal_anchor: `G28_LDC_FocalGroup`
- supporting: three callout slots
- connector: left/right connector primitives inside focal group
- decoration: low-salience stage and lower-corner hosts
- label: title text and focal label
- reading order: title -> left node -> focal core -> right node -> callouts
- in-frame text budget: two active text items, 16 chars in the diagnostic skeleton

## YMM4 Item / Group Mapping

The diagnostic artifact is JSON/HTML, but names are chosen so a later YMM4
carrier or slot-fill adapter can reuse the same mapping.

| Group | Role | Patch allowed later | Patch forbidden later |
|-------|------|---------------------|-----------------------|
| `G28_LDC_Stage` | decoration | visibility for review guides | stage geometry, external image |
| `G28_LDC_TitleBand` | label | title text within budget | title area geometry |
| `G28_LDC_FocalGroup` | focal_anchor | visibility / theme label only | focal geometry, composition type |
| `G28_LDC_CalloutSlots` | supporting | callout text after validation | more than 3 callouts, table rows |
| `G28_LDC_Hosts` | decoration | visibility on/off | host as focal, caption overlap |

## Readback Checklist

- `diagnostic_only=true`
- `production_candidate=false`
- no image binary / image path / image URL / raw reference
- `ymmp_generation=not_generated_boundary`
- frame is 1920 x 1080 / 16:9
- title area is top short label area
- caption reserve is bottom 20%
- caption reserve has no overlapping main item
- focal group is inside main canvas
- host placeholders are above caption reserve
- active callout slot count is 2-3
- primitive item count is <= 14
- semantic group count remains bounded
- ShapeItem size mode is `WidthHeight`
- in-frame text budget passes
- no `indexed_whiteboard`

## Theme Variant v1: `real_estate_information_gap`

The first theme-specific diagnostic variant is generated from the same skeleton,
without changing the generic skeleton output path.

- generator: `node scripts\build_g28_lecture_diagram_carrier_skeleton.js --write --variant real_estate_information_gap`
- output JSON: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.json`
- output readback: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_readback.json`
- output HTML: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap.html`
- output report: `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_report.md`
- variant id: `g28_ldc_real_estate_information_gap`
- composition type: `center-focal`
- focal chain: `元付情報` -> `ポータル掲載` -> `借主判断`
- callout semantics: `情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`
- visible in-frame text budget: two text items / 15 chars
- slot-fill state: semantic labels only; callout slots are not text-filled claims
- host role: non-focal lower-corner decoration
- dense table: false
- indexed whiteboard: false
- external image count: 0
- external URL count: 0
- token-like pattern count: 0

This variant is still diagnostic-only. It does not approve a production carrier,
does not revive G-27, does not generate `.ymmp`, does not render, does not use
source footage, and does not create or record image paths or external URLs.

## Failure Modes

- `indexed_whiteboard`: equal-weight cards or bullet rows replace focal hierarchy
- `information_overload`: callouts exceed three slots or text becomes table-like
- `subtitle_collision`: any main item overlaps y=810-1026 caption reserve
- `host_as_focal`: lower-corner host becomes the main visual object
- `shape_size_mode_invalid`: ShapeItem does not use `WidthHeight`
- `text_budget_overrun`: title/callout fill exceeds SCS budget
- `source_over_decoration`: future source footage is decorated instead of being
  left as Source-Footage Carrier

## Acceptance Criteria

Diagnostic acceptance requires:

- generated JSON skeleton exists
- generated readback JSON reports `status=passed`
- generated HTML visualization exists and uses only inline shapes/text
- generated MD report exists
- no reference image, image path, URL, token-like text, raw OPML, or article body
  appears in the generated files
- no `.ymmp`, render, production timing, creative final acceptance, or G-27
  promotion is claimed

Production acceptance remains separate and requires a later scoped slice with
YMM4-saved carrier review and human creative judgement.
