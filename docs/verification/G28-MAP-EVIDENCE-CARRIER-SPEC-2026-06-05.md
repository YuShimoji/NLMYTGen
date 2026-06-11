# G-28 Map / Evidence Carrier Concrete Spec — 2026-06-05

G-28 `Reference-Driven Generic Screen Carrier` の別 archetype として、
Map / Evidence Carrier を diagnostic skeleton / readback artifact まで進める。

Lecture Diagram Carrier は mechanism explanation を中心にする。一方で
Map / Evidence Carrier は、地図・統計・産業立地・企業分布・人口・市場・
地域差・出典付き論証を、飾りではなく論証装置として扱う画面契約である。

この文書は production carrier approval、creative final acceptance、render、
実素材 slot-fill の完了報告ではない。

## Boundary

- diagnostic skeleton generation: Agent-owned
- frame contract / item group / readback checklist: Agent-owned
- HTML visualization / JSON readback: Agent-owned
- creative final acceptance: human-owned
- production render: not run
- production slot-fill: not run
- real map / satellite image use: forbidden
- image binary / image path / image URL / raw reference recording: forbidden
- source footage / gameplay screenshot intake: forbidden
- G-27 diagnostic carrier promotion: forbidden
- RSS / OPML / Inoreader / NotebookLM source-pack work: out of scope

`.ymmp` は今回生成しない。まず JSON / HTML / readback artifact で、地理・
統計・出典付き論証を支える carrier archetype としての frame contract を固定する。

## Later Diagnostic Carrier Slice

The 2026-06-05 slice intentionally stopped at JSON / HTML / readback
artifacts. A later speed-first G-28 slice on 2026-06-11 created a separate
diagnostic-only YMM4 carrier candidate at
`samples/_probe/g28/map_evidence_carrier_ymmp_diagnostic_probe.ymmp`, with
readback and report siblings. That later slice does not change this original
skeleton boundary and does not approve production, render, rights, source
intake, or creative final acceptance.

## Output Artifacts

- generator: `node scripts\build_g28_map_evidence_carrier_skeleton.js --write`
- output JSON: `samples/_probe/g28/map_evidence_carrier_skeleton.json`
- output readback: `samples/_probe/g28/map_evidence_carrier_skeleton_readback.json`
- output HTML: `samples/_probe/g28/map_evidence_carrier_skeleton.html`
- output report: `samples/_probe/g28/map_evidence_carrier_skeleton_report.md`
- artifact id: `g28_map_evidence_carrier_skeleton_v1`
- archetype: `Map / Evidence Carrier`
- diagnostic state: `diagnostic_only=true`, `production_candidate=false`

## Frame Contract

- frame: 1920 x 1080 / 16:9
- outer safe margin: 5%
- title band: x=96, y=54, w=1728, h=96
- main canvas: x=96, y=150, w=1728, h=660
- map / evidence focal area: x=240, y=180, w=1440, h=500
- caption reserve: x=0, y=810, w=1920, h=216
- main carrier items must not overlap caption reserve
- lower-corner hosts stay non-focal and above caption reserve

## SCS Mapping

- archetype: Map / Evidence Carrier
- composition type: `center-focal`
- no new SCS type is added
- rationale: a single map/evidence surface is the focal argument surface; label
  anchors, annotation slots, and source note support it without becoming
  equal-weight cards
- focal anchor: `G28_MEC_EvidenceSurface`
- supporting: `G28_MEC_AnnotationSlot_1` to `G28_MEC_AnnotationSlot_3`,
  `G28_MEC_SourceNote`
- connector: `G28_MEC_LabelAnchor_1`, `G28_MEC_LabelAnchor_2`,
  `G28_MEC_LeaderLine_1`
- decoration: low-salience stage and lower-corner host placeholders
- label: title text and short source note

Future G-28 archetypes may map to `mediator` or `chain` where that is already
allowed by SCS, but this diagnostic skeleton does not create a new composition
type.

## Item Groups

| Group | Role | Purpose |
|-------|------|---------|
| `G28_MEC_Stage` | decoration | dark low-salience stage and safe frame |
| `G28_MEC_TitleBand` | label | one-line map/evidence claim area |
| `G28_MEC_EvidenceSurface` | focal_anchor | abstract map/evidence surface, not an image asset |
| `G28_MEC_Annotations` | supporting / connector | 2-4 annotation slots plus label anchors |
| `G28_MEC_SourceNote` | supporting | short bounded source note area |
| `G28_MEC_Hosts` | decoration | lower-corner emotional anchors, not focal |

## Annotation Rule

- diagnostic slot count: 3
- allowed active slot count: 2-4
- diagnostic state: slots are empty shapes, not text-filled claims
- future slot-fill rule: fill only after text-budget validation
- forbidden: dense table, indexed whiteboard, source body text, long label stack

## Source Note Rule

The source note area exists to prove that provenance can be reserved without
turning the screen into a reference list.

- source note area exists: true
- text budget: short bounded note only
- diagnostic text: `出典確認済み`
- smallest visible text size: 32
- forbidden: long source body, many citations, external URL field, tiny footnote

## Readback Checklist

- `diagnostic_only=true`
- `production_candidate=false`
- frame is 1920 x 1080 / 16:9
- caption reserve is bottom 20%
- caption reserve is clear
- focal/evidence area is in main canvas
- annotation slot count is 2-4
- source note area exists
- source note text budget is bounded
- host role is non-focal
- `dense_table=false`
- `indexed_whiteboard=false`
- `tiny_text=false` or bounded
- `external_image_count=0`
- `external_url_count=0`
- `token_like_pattern_count=0`
- `image_path=false`
- `image_url=false`
- `raw_reference=false`

## Failure Modes

- `map_label_overload`: too many labels compete with the evidence surface
- `source_note_overload`: source note becomes a body-text reference list
- `indexed_whiteboard`: equal-weight numbered items replace visual argument
- `tiny_text`: evidence depends on text too small to read in video
- `subtitle_collision`: main content overlaps bottom caption reserve
- `decorative_map_without_argument`: map-looking surface carries no claim

## Acceptance State

The skeleton passes only when JSON, readback JSON, HTML visualization, and report
MD are generated, readback status is `passed`, external image / URL counts are
zero, caption reserve is clear, and the text budget is not dense.

Passing this spec does not complete G-28 production. It only establishes one
additional diagnostic archetype next to Lecture Diagram Carrier.
