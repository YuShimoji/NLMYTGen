# Real Estate DX Minimal Patched .ymmp Probe Readback

Probe: `samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp`
Source compact review: `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json`

This report proves the generated probe contains only the 7 compact review candidates. It is not a render and not creative acceptance.

## Rollup

- Status: `passed`
- Inserted ShapeItem count: `14`
- Inserted TextItem count: `7`
- Candidate ids found: `RE-02-beginning, RE-02-development, RE-06-beginning, RE-06-development, RE-06-turn, RE-07D-beginning, RE-07D-development`
- Layer values found: `7, 8, 9`
- Missing / malformed items: `0` / `0`
- Carrier modified in place: `false`
- Next slice can proceed to YMM4 GUI readback / preview: `true`

## Candidate Readback

| candidate | item types | layers | start frames | durations | status |
| --- | --- | --- | --- | --- | --- |
| `RE-02-beginning` | ShapeItem + TextItem | 7, 8, 9 | 0 | 360 | `ready_for_gui_readback` |
| `RE-02-development` | ShapeItem + TextItem | 7, 8, 9 | 390 | 360 | `ready_for_gui_readback` |
| `RE-06-beginning` | ShapeItem + TextItem | 7, 8, 9 | 780 | 360 | `ready_for_gui_readback` |
| `RE-06-development` | ShapeItem + TextItem | 7, 8, 9 | 1170 | 360 | `ready_for_gui_readback` |
| `RE-06-turn` | ShapeItem + TextItem | 7, 8, 9 | 1560 | 360 | `ready_for_gui_readback` |
| `RE-07D-beginning` | ShapeItem + TextItem | 7, 8, 9 | 1950 | 360 | `ready_for_gui_readback` |
| `RE-07D-development` | ShapeItem + TextItem | 7, 8, 9 | 2340 | 360 | `ready_for_gui_readback` |

## Missing Or Malformed

- none

## Boundary

- Real `.ymmp` probe generated, but no source `.ymmp` was modified in place.
- No render, no creative acceptance, no TTS, no URL fetch, no publishing, no sports_news, and no pipeline hardening.
- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.
