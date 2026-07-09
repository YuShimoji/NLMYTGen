# UI Rubric

## Non-completion conditions

- UI improvement without screenshot evidence is incomplete.
- Text-density review without a visual artifact is incomplete.
- Card avoidance alone is not a valid UI goal.
- Aesthetic commentary without a next reversible UI action is incomplete.

## Evaluation axes

| Axis | Pass condition |
|---|---|
| Primary action | The first user action is visually obvious. |
| Information hierarchy | Primary, secondary, and reference information are separated. |
| Text density | Dense explanatory blocks do not dominate the first viewport. |
| Layout choice | Cards, tables, timelines, sidebars, previews, and canvases are chosen by task structure. |
| Preview | The user can see output or state, not only descriptions. |
| Japanese UX | Primary labels and CTAs are natural Japanese. |
| Mobile evidence | Mobile layout is checked with screenshot or viewport capture when the UI surface is changed. |

## Screenshot evidence format

| Date | Surface | Viewport | Path | Finding | Next action |
|---|---|---|---|---|---|
| 2026-07-10 | Episode 002 YMM4 import-ready Japanese review surface | desktop HTML preview | `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_ready_pack/ymm4_import_ready_preview.html` | Verified present by `validation_readback.json`; no new screenshot captured in this docs/validation slice | Capture a PNG only if the next BUILD changes or evaluates this review surface |
