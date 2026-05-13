# Real Estate DX Primitive Visibility Calibration Probe

Probe: `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp`

This is not a video scene. It is a bounded drawing-semantics calibration probe for YMM4 ShapeItem/TextItem visibility, geometry, and authoring-surface hygiene.

## 1. What exactly is being calibrated?

- ShapeItem position, WidthHeight geometry, non-zero StrokeThickness visibility, opacity, color contrast, TextItem containment, connector visibility, and short YMM4 authoring labels.

## 2. Which assumptions from the failed micro scene are being tested?

- YMM4 ShapeItem rectangles need WidthHeight plus non-zero StrokeThickness to become material panels.
- X/Y coordinates are expected to behave as center-origin placement in the 1920x1080 preview canvas.
- Panel-contained TextItems should be legible when positioned inside a large panel, not as independent floating labels.
- A single light-stage tonal system should keep panel, text, markers, and connector readable without black/white background toggles.
- Human-readable short Remarks should keep the YMM4 authoring surface manageable while detailed provenance stays in readback/report.

## 3. Does the probe intentionally test coordinate / anchor behavior?

- Yes. `Center Marker` is placed at `(0, 0)`, `TL Marker` at the expected top-left corner of the 920x560 panel, and `BR Marker` at the expected bottom-right corner. If these markers do not align with panel geometry in YMM4, the X/Y anchor assumption is wrong or incomplete.

## 4. Does the probe intentionally test panel-contained text?

- Yes. `Panel Title`, `Panel Body`, and marker labels are positioned inside `Main Panel`; readback records expected panel relationships and rough text bounds.

## 5. Does the probe intentionally test high-contrast visibility?

- Yes. It uses one light-stage tonal system, a dark blue central panel, white panel text, high-contrast markers, and an amber connector. Primary opacity is 100%.

## 6. Does the probe keep provenance out of YMM4 item names / Remarks?

- Yes. YMM4 Remarks are short display names only. Detailed provenance is kept in the readback JSON and this report.

## Rollup

- Readback status: `passed`
- Items: `11` (ShapeItem=`6`, TextItem=`5`)
- Tonal system: `light-stage`
- Item name length failures: `0`
- Remark length failures: `0`
- Suspicious default item count: `0`
- Carrier modified in place: `false`

## Item Table

| item | type | layer | x/y | geometry | opacity | color | intended panel relation | suspicious defaults |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `BG` | `ShapeItem` | `5` | `0, 0` | `1920x1080, stroke=1080` | `100` | `#FFF4F7FB` | none | none |
| `Main Panel` | `ShapeItem` | `8` | `0, 0` | `920x560, stroke=560` | `100` | `#FF155EA8` | inside Main Panel; center=true | none |
| `Panel Title` | `TextItem` | `9` | `0, -145` | `font=68` | `100` | `#FFFFFFFF` | inside Main Panel; center=true | none |
| `Panel Body` | `TextItem` | `9` | `0, -60` | `font=38` | `100` | `#FFFFFFFF` | inside Main Panel; center=true | none |
| `Center Marker` | `ShapeItem` | `10` | `0, 0` | `56x56, stroke=56` | `100` | `#FFFF3B30` | inside Main Panel; center=true | none |
| `Center Label` | `TextItem` | `11` | `0, 74` | `font=34` | `100` | `#FFFFFFFF` | inside Main Panel; center=true | none |
| `TL Marker` | `ShapeItem` | `10` | `-460, -280` | `56x56, stroke=56` | `100` | `#FF16A34A` | inside Main Panel; center=true | none |
| `TL Label` | `TextItem` | `11` | `-350, -246` | `font=32` | `100` | `#FFFFFFFF` | inside Main Panel; center=true | none |
| `BR Marker` | `ShapeItem` | `10` | `460, 280` | `56x56, stroke=56` | `100` | `#FFFF9500` | inside Main Panel; center=true | none |
| `BR Label` | `TextItem` | `11` | `345, 246` | `font=32` | `100` | `#FFFFFFFF` | inside Main Panel; center=true | none |
| `Connector` | `ShapeItem` | `10` | `245, 140` | `420x42, stroke=42` | `100` | `#FFFFD43B` | inside Main Panel; center=true | none |

## 7. What should the user inspect in YMM4?

- Open the probe and check whether the light-stage background, large blue panel, panel title/body, three anchor markers, and connector are visible without toggling backgrounds.
- Confirm whether title/body text visually belongs to the panel rather than floating independently.
- Confirm whether `Center Marker`, `TL Marker`, and `BR Marker` align with the intended panel center/corners.
- Confirm whether timeline item labels are manageable: `BG`, `Main Panel`, `Panel Title`, `Panel Body`, `Center Marker`, `TL Marker`, `BR Marker`, `Connector`.

## 8. What screenshot angles or selected item properties should the user return?

- Preview screenshot of the full calibration frame.
- Screenshot of one selected panel item property, preferably `Main Panel`, including X/Y, opacity, Width/Height, StrokeThickness, and color.
- Screenshot of one selected text item property, preferably `Panel Title`, including X/Y, font size, opacity, and color.
- If a marker is off, include a screenshot with the relevant marker selected so coordinate/anchor behavior can be inferred.

## Completion Position

- Calibration probe is ready for user-side GUI inspection only.
- Existing micro scene work is not advanced in this slice.
- Minimal render smoke remains blocked until this calibration passes in YMM4 GUI review.
