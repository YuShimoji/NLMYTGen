# G-27 Layout Instruction Compliance Proof

Artifact: `samples/_probe/g24/layout_instruction_proof.ymmp`

Diagnostic-only layout proof. Not a scene composition, not a render, not creative acceptance.

## Instruction Compliance Rollup

- `canvas_16_9_1920_1080`: `pass`
- `title_band_top`: `pass`
- `title_slot_width_for_18_chars`: `pass`
- `title_text_within_band`: `pass`
- `title_grid_gap_visible`: `pass`
- `grid_2x2_cells`: `pass`
- `grid_boundary_visible`: `pass`
- `char_a_bust_left_bottom`: `pass`
- `char_b_bust_right_bottom`: `pass`
- `bust_up_no_intrusion_into_caption_safe`: `pass`
- `caption_safe_area_empty_of_major_items`: `pass`
- `region_labels_present`: `pass`
- `region_labels_clear_major_items`: `pass`
- `caption_indicator_present`: `pass`
- `shape_size_mode_widthheight`: `pass`
- `color_format_aarrggbb`: `pass`

## Title Slot

- center: cx=0, cy=-443
- band size: 1728x86
- font size: 60
- title text center y: -451 (offset -8px from band center)
- current text: "レイアウト指示遵守の検証" (12 chars)
- max chars assumption: 18
- slot width required for 18 chars: 1080px
- title-grid gap: 40px (min 32px)

## Grid 2x2 Slots

| id | row | col | cx | cy | width | height | fill |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LIP_GridCell_0_0` | 0 | 0 | -436 | -274 | 856 | 172 | `#FFE7ECF1` |
| `LIP_GridCell_0_1` | 0 | 1 | 436 | -274 | 856 | 172 | `#FFCFD8E0` |
| `LIP_GridCell_1_0` | 1 | 0 | -436 | -86 | 856 | 172 | `#FFCFD8E0` |
| `LIP_GridCell_1_1` | 1 | 1 | 436 | -86 | 856 | 172 | `#FFE7ECF1` |

## Character Placeholder Slots

### Character A (left)

- cx (center): -700
- head: cx=-700, cy=95, w=140, h=160
- shoulders: cx=-700, cy=245, w=280, h=100

### Character B (right)

- cx (center): 700
- head: cx=700, cy=95, w=140, h=160
- shoulders: cx=700, cy=245, w=280, h=100

## Caption Safe Area

- cy range: 324..540
- height: 216px (20% of 1080)
- indicator present: true

## Region Labels

- `LIP_Label_Title`: "[title band]" at cx=-785.5, cy=-511
- `LIP_Label_Grid`: "[grid 2x2]" at cx=-795.5, cy=-379
- `LIP_Label_CharA`: "[character A bust]" at cx=-861, cy=25
- `LIP_Label_CharB`: "[character B bust]" at cx=861, cy=25
- `LIP_Label_Caption`: "[caption safe area / empty]" at cx=-16.5, cy=307

## Violations

- (none)

## Status

- readback status: `passed`
- item count: 17 (Shape=11, Text=6)
- carrier modified in place: `false`
