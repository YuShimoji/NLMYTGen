# G-27 Layout Instruction Compliance Proof

Artifact: `samples/_probe/g24/layout_instruction_proof.ymmp`

Diagnostic-only layout proof. Not a scene composition, not a render, not creative acceptance.

## Instruction Compliance Rollup

- `canvas_16_9_1920_1080`: `pass`
- `title_band_top`: `pass`
- `title_slot_width_for_18_chars`: `pass`
- `title_text_within_band`: `pass`
- `grid_2x2_cells`: `pass`
- `grid_boundary_visible`: `pass`
- `char_a_bust_left_bottom`: `pass`
- `char_b_bust_right_bottom`: `pass`
- `bust_up_no_intrusion_into_caption_safe`: `pass`
- `caption_safe_area_empty_of_major_items`: `pass`
- `region_labels_present`: `pass`
- `caption_indicator_present`: `pass`
- `shape_size_mode_widthheight`: `pass`
- `color_format_aarrggbb`: `pass`

## Title Slot

- center: cx=0, cy=-443
- band size: 1728x86
- font size: 64
- current text: "レイアウト指示遵守の検証" (12 chars)
- max chars assumption: 18
- slot width required for 18 chars: 1152px

## Grid 2x2 Slots

| id | row | col | cx | cy | width | height | fill |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LIP_GridCell_0_0` | 0 | 0 | -436 | -304 | 856 | 192 | `#FFE7ECF1` |
| `LIP_GridCell_0_1` | 0 | 1 | 436 | -304 | 856 | 192 | `#FFCFD8E0` |
| `LIP_GridCell_1_0` | 1 | 0 | -436 | -96 | 856 | 192 | `#FFCFD8E0` |
| `LIP_GridCell_1_1` | 1 | 1 | 436 | -96 | 856 | 192 | `#FFE7ECF1` |

## Character Placeholder Slots

### Character A (left)

- cx (center): -700
- head: cx=-700, cy=70, w=140, h=160
- shoulders: cx=-700, cy=210, w=280, h=100

### Character B (right)

- cx (center): 700
- head: cx=700, cy=70, w=140, h=160
- shoulders: cx=700, cy=210, w=280, h=100

## Caption Safe Area

- cy range: 324..540
- height: 216px (20% of 1080)
- indicator present: true

## Region Labels

- `LIP_Label_Title`: "[title band]" at cx=-800, cy=-480
- `LIP_Label_Grid`: "[grid 2x2]" at cx=-800, cy=-400
- `LIP_Label_CharA`: "[character A bust]" at cx=-800, cy=-20
- `LIP_Label_CharB`: "[character B bust]" at cx=800, cy=-20
- `LIP_Label_Caption`: "[caption safe area / empty]" at cx=0, cy=310

## Violations

- (none)

## YMM4 Preview Gate

Primary surface: open `samples/_probe/g24/layout_instruction_proof.ymmp` in YMM4 and check the frame-0 preview.

- Pass signal: title band is near the top and not clipped, the 2x2 grid has four visible cells, both bust placeholders sit left/right above the caption safe area, and the bottom caption area remains visually empty.
- Fix signal: any obvious TextItem anchor drift, clipped title, collapsed grid cell, character overlap into the caption area, or major object inside the caption safe area.
- Return payload: one preview screenshot plus a short PASS/FIX note. If FIX, name the failing region: title, grid, character A/B, caption safe area, or labels.
- Boundary: this is still a layout-instruction proof only; it is not render proof, scene composition acceptance, or production readiness.

## Status

- readback status: `passed`
- item count: 17 (Shape=11, Text=6)
- carrier modified in place: `false`
