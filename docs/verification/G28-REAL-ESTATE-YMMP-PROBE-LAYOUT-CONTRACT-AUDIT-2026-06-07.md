# G-28 Real Estate YMM4 Probe Layout Contract Audit - 2026-06-07

This audit records the layout contract status of the polished
`real_estate_information_gap` YMM4 diagnostic probe.

The original audit pass was docs-only. A later bounded implementation slice in
this same file records the diagnostic builder/readback contract update. Neither
slice approves production status, rights status, slot-fill, render output, or
creative acceptance.

## Scope

| Field | Value |
| --- | --- |
| probe | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp` |
| readback | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json` |
| builder inspected read-only | `scripts/build_g28_real_estate_ymmp_probe.js` |
| human re-review decision | `accept_as_diagnostic_gui_probe_with_layout_contract_followup` |
| readback classification | `pass_probe_polished` |
| diagnostic_only | `true` |
| production_candidate | `false` |

## Readback Baseline

- frame: `1920x1080 / 16:9`
- caption reserve: `x=0 y=810 w=1920 h=216`, clear
- focal chain: `元付情報 -> ポータル掲載 -> 借主判断`
- callout count: 3
- host role: `non_focal_lower_corner_decoration_emotional_anchor`
- external image count: 0
- external URL count: 0
- source footage count: 0
- audio / TTS count: 0 / 0
- token-like pattern count: 0

## Rectangle Text Centering Formula

Current formula, extracted from the builder:

```text
estimated_text_width = round(sum(char_width_em) * font_size)
estimated_text_height = font_size
target_center = center(polished_rect_for(target_item)) + visual_offset_px
screen_top_left.x = target_center.x - estimated_text_width / 2
screen_top_left.y = target_center.y - estimated_text_height / 2
ymm4_top_left.x = screen_top_left.x - frame_width / 2
ymm4_top_left.y = screen_top_left.y - frame_height / 2
```

Character width approximation:

- Japanese full-width ranges count as `1.0em`.
- Other characters count as `0.55em`.
- Height is approximated as `font_size`.

The formula is usable as a diagnostic contract, but the baseline / optical
centering adjustment is not derived from font metrics. It is carried by manual
vertical offsets:

- title text: `x=0, y=-2`
- focal node labels: `x=0, y=-4`
- callout labels: `x=0, y=-3`

Current measured label-center error versus the containing box center:

| Label | Text | Error |
| --- | --- | --- |
| `G28_LDC_Title_Text` | `情報非対称の流れ` | `dx=0, dy=-2` versus source title rect |
| `G28_LDC_Node_Left_Label` | `元付情報` | `dx=0, dy=-4` |
| `G28_LDC_Node_Center_Label` | `ポータル掲載` | `dx=0, dy=-4` |
| `G28_LDC_Node_Right_Label` | `借主判断` | `dx=0, dy=-4` |
| `G28_LDC_CalloutSlot_1_Label` | `情報遅延` | `dx=0, dy=-3` |
| `G28_LDC_CalloutSlot_2_Label` | `掲載粒度の欠落` | `dx=0, dy=-3` |
| `G28_LDC_CalloutSlot_3_Label` | `仲介インセンティブ` | `dx=0, dy=-3` |

Audit judgement:

- The arithmetic placement rule is explicit enough to describe.
- The optical centering values are manual offsets, not a font-derived formula.
- Reuse should require an offset registry plus tolerance readback before this is
  treated as a generic layout system.

## Connector Positioning Formula

Current polished connector rectangles:

| Connector | Rect | Relationship |
| --- | --- | --- |
| `G28_LDC_Connector_Left` | `x=490 y=394 w=70 h=12` | left node right edge `490` to focal core left edge `560` |
| `G28_LDC_Connector_Right` | `x=1360 y=394 w=70 h=12` | focal core right edge `1360` to right node left edge `1430` |

Current formula that explains the result:

```text
left.start_x = left_node.x + left_node.width
left.end_x = focal_core.x
right.start_x = focal_core.x + focal_core.width
right.end_x = right_node.x
connector.width = end_x - start_x
connector.thickness = 12
connector.y = side_node.center_y - connector.thickness / 2
```

Measured readback:

- left start gap to left node: `0px`
- left end gap to focal core: `0px`
- right start gap to focal core: `0px`
- right end gap to right node: `0px`
- connector center-y error versus side nodes: `0px`
- left/right connector width symmetry: exact (`70px` / `70px`)

Audit judgement:

- The current values can be explained as edge-to-edge connector bars.
- The builder currently stores them as polished rectangle overrides, not as a
  computed relationship over node rectangles.
- Reuse should convert this into a derived formula or add readback checks that
  prove the hard-coded values still satisfy the relationship.

## Callout Slot Layout Rule

Current polished callout slots:

| Slot | Rect | Text | Text width / slot width |
| --- | --- | --- | --- |
| `G28_LDC_CalloutSlot_1` | `x=375 y=642 w=330 h=90` | `情報遅延` | `0.364` |
| `G28_LDC_CalloutSlot_2` | `x=795 y=642 w=330 h=90` | `掲載粒度の欠落` | `0.636` |
| `G28_LDC_CalloutSlot_3` | `x=1215 y=642 w=330 h=90` | `仲介インセンティブ` | `0.818` |

Current rule that explains the three-slot row:

```text
slot_width = 330
slot_height = 90
slot_gap = 90
row_y = 642
slot_1.x = 375
slot_2.x = slot_1.x + slot_width + slot_gap
slot_3.x = slot_2.x + slot_width + slot_gap
label_center = slot_center + { x: 0, y: -3 }
```

The three-slot row works because:

- total row width is `1170px` (`330 * 3 + 90 * 2`)
- it stays inside the main canvas
- it leaves symmetric host-side gaps of about `59px`
- the row bottom is `732`, leaving `78px` above the caption reserve at `y=810`
- max text width ratio is `0.818`, below the proposed warning threshold

Two callouts would likely remain safe if centered in the same row. Four callouts
would require a new layout rule because keeping `330px` slots and `90px` gaps
would consume `1590px`, leaving little room for hosts and side breathing space.

## Manual Offset Registry

| Target | Current value | Reason | Tolerance proposal | Reuse risk |
| --- | --- | --- | --- | --- |
| title text | `{ x: 0, y: -2 }` | optical centering inside source title rect | abs offset <= `4px` | medium; source title rect is not the title-band background |
| focal node labels | `{ x: 0, y: -4 }` | YMM4 TextItem top-left optical correction | abs offset <= `6px` | medium; font/baseline specific |
| callout labels | `{ x: 0, y: -3 }` | optical centering inside compact callout boxes | abs offset <= `5px` | medium; text length and font specific |
| left connector | source rect changed from `500,395,90,10` to `490,394,70,12` | align exactly from left node edge to focal edge | endpoint gap <= `2px`, y error <= `2px` | medium until computed from node geometry |
| right connector | source rect changed from `1330,395,90,10` to `1360,394,70,12` | align exactly from focal edge to right node edge | endpoint gap <= `2px`, y error <= `2px` | medium until computed from node geometry |
| callout slots | source widths `300` became `330`, y moved from `650` to `642` | improve callout readability and spacing | max density <= `0.85`, caption gap >= `60px` | medium-high for 4 callouts |
| hosts | no polish override; source rects retained | lower-corner emotional anchors only | each host area <= `3%` frame, above caption, below focal | low for this probe, medium across themes |

## Tolerance Readback Proposal

These metrics should be added in a later implementation slice if the layout
system is reused. They are not added in this audit slice.

| Metric | Definition | Pass threshold proposal |
| --- | --- | --- |
| `text_center_error_px` | label center minus `(target box center + registered offset)` | <= `1px` implementation error; registered optical offset <= `6px` |
| `connector_alignment_error_px` | max endpoint gap and y-center error against adjacent node/focal edges | <= `2px` |
| `caption_reserve_overlap_px` | overlap of non-background visual items with caption reserve | `0px` |
| `callout_density` | max label width / slot width, plus label height / slot height | width <= `0.85`, height <= `0.45`; warning above `0.85` |
| `host_focality_risk` | decoration role, area ratio, vertical placement, absence of text/image evidence cues | low if each host <= `3%` frame, below focal, above caption, no text/image |

Current diagnostic estimate:

- `text_center_error_px`: implementation-consistent; optical offsets are manual
  `2-4px`
- `connector_alignment_error_px`: `0px`
- `caption_reserve_overlap_px`: `0px`
- `callout_density`: max width ratio `0.818`
- `host_focality_risk`: low

## Reuse Risk

Reusable parts:

- 1920x1080 frame contract
- bottom caption reserve boundary
- center-focal / three-node mechanism diagram pattern
- edge-to-edge connector relationship
- TextItem top-left conversion from screen coordinates to YMM4 coordinates
- bounded callout density concept

Probe-specific or weakly generalized parts:

- manual vertical text offsets
- hard-coded connector rectangle overrides
- hard-coded three-callout row positions
- host-side spacing that assumes exactly two lower-corner hosts
- no tolerance metrics in readback yet

Risk judgement:

- The polished probe is acceptable as a diagnostic GUI probe.
- It is not yet a reusable layout system contract.
- If reused across themes, longer labels or a different callout count can break
  the current hard-coded row and optical-centering assumptions.

## Next Decision

Original audit recommendation: `needs_layout_contract_implementation`.

Operationally, this should be handled as one bounded layout-system revision
before Review Console ingest. The next slice should not be another visual
polish pass. It should implement or sidecar-record:

- derived connector geometry from node/focal rectangles
- explicit text offset registry
- callout row formula for 2-3 callouts, with a documented fail-fast rule for 4
  callouts
- tolerance readback metrics listed above

Only after that contract exists should the project decide whether this probe is
ready for Review Console ingest. This recommendation does not approve production
rendering, production carrier approval, creative final acceptance, rights
automation, slot-fill, or external material intake.

## Implementation Result

Implementation revision: `g28_real_estate_information_gap_layout_contract_v1`.

Post-implementation classification:
`pass_layout_contract_implemented`.

Post-implementation next decision:
`ready_for_human_gui_recheck_before_review_console_ingest`.

Implemented in `scripts/build_g28_real_estate_ymmp_probe.js`:

- connector geometry is now derived from the left/focal/right rectangles
- the text offset registry is serialized into item/readback metadata
- the three-callout row is represented as a 2-3 callout contract with an
  explicit four-callout risk note
- readback now records layout contract metrics and tolerance pass/fail checks
- the report now includes layout contract revision and readback sections

Readback after `node scripts\build_g28_real_estate_ymmp_probe.js --write`:

- `diagnostic_only=true`
- `production_candidate=false`
- `layout_contract_metrics_present=true`
- `layout_contract_tolerances_pass=true`
- `text_center_error_px=0`
- `registered_optical_offset_max_px=4`
- `connector_alignment_error_px=0`
- `caption_reserve_overlap_px=0`
- `callout_density.max_width_ratio=0.818`
- `callout_density.max_height_ratio=0.333`
- `host_focality_risk=low`
- external image / URL / source footage / audio / TTS / token-like counts remain
  `0`

This closes the original `needs_layout_contract_implementation` recommendation
for the diagnostic probe only. It does not approve Review Console ingest by
itself; the next human-facing step is a YMM4 GUI recheck of the updated
diagnostic probe/readback pair.

## Right-Node Alignment Follow-up

The YMM4 GUI recheck after layout-contract implementation returned
`revise_probe_again_narrow_right_node_text_alignment`. All major diagnostic
checks passed, but the right-side node label `借主判断` still appeared optically
off-center to the human reviewer.

Follow-up implementation:

- revision: `g28_real_estate_information_gap_right_node_alignment_v1`
- classification: `pass_right_node_alignment_fixed`
- target: `G28_LDC_Node_Right_Label`
- previous registered offset: `{ x: 0, y: -4 }`
- applied registered offset: `{ x: 4, y: -4 }`
- formula change: none; the common TextItem top-left formula is unchanged
- scope: right-node label only

Metric caveat:

`text_center_error_px=0` measures placement against the registered offset and
estimated text box. It is not proof of rendered YMM4 glyph optical center.
Human GUI review remains the authority for whether this right-node visual fix is
sufficient before any Review Console ingest decision.

## Callout Label Alignment Follow-up

A later human GUI correction clarified that the actual remaining visual target
was not the right node label but the lower-right callout label
`仲介インセンティブ`.

Follow-up implementation:

- revision: `g28_real_estate_information_gap_callout_label_alignment_v1`
- classification: `pass_callout_label_alignment_fixed`
- target: `G28_LDC_CalloutSlot_3_Label`
- previous registered offset: `{ x: 0, y: -3 }`
- applied registered offset: `{ x: 4, y: -3 }`
- previous right-node fix: retained
- formula change: none; the common callout label placement formula is unchanged
- scope: lower-right callout label only

Metric caveat:

`text_center_error_px=0` measures placement against the registered offset and
estimated text box. It is not proof of rendered YMM4 glyph optical center.
Human GUI review remains the authority for whether this callout-label visual fix
is sufficient before any Review Console ingest decision.

## Human-Calibrated Callout Override And Layout System Debt

Human GUI recheck after `g28_real_estate_information_gap_callout_label_alignment_v1`
reported that the lower-right callout label `仲介インセンティブ` still read
left-shifted. The human-measured correct YMM4 TextItem X is `313.0`.

Follow-up implementation:

- revision: `g28_real_estate_information_gap_callout_label_human_calibration_v1`
- classification: `pass_callout_label_human_calibrated`
- target: `G28_LDC_CalloutSlot_3_Label`
- computed X before human calibration: `289`
- previous polished X: `289`
- human calibrated X: `313.0`
- calibration delta X: `24`
- formula change: none as a reusable success claim; the generated YMM4 TextItem
  X is overridden once with the human-calibrated value
- scope: lower-right callout label only

Debt interpretation:

- reason: the estimated text box plus registered offset can report centered
  placement while the rendered YMM4 glyph still appears left-shifted to a human
  reviewer
- metric/perception gap: `text_center_error_px` verifies registered placement,
  not rendered glyph optical center
- reuse risk: high; `x=313.0` must not be generalized to other labels, themes,
  fonts, or callout counts
- future fix direction: replace per-label overrides with a callout text layout
  model that accounts for YMM4 font rendering, target text width, and visual
  centering acceptance
- stop condition: if this still reads off in YMM4, stop individual offset
  tuning and redesign the callout text layout system

## Boundary

Original audit slice:

- No `.ymmp` regeneration.
- No builder or generator change.
- No readback JSON change.
- No probe report change.

Implementation slice:

- The same diagnostic builder was updated.
- The same diagnostic probe/readback/report paths were regenerated or checked.
- No new variant was created.

Both slices:

- No new variant generation.
- No render, MP4, production carrier approval, or creative final acceptance.
- No rights automation or `production_candidate=true`.
- No external image, URL, raw reference, source footage, audio, or TTS.
- No G-27 revival.
- No common foundation or Codex Worker Orchestration implementation.
- No ClipPipeGen access.
- No RSS / OPML / Inoreader / NotebookLM source-pack work.
