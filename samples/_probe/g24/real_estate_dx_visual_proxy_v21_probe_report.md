# Real Estate DX Visual Proxy v2.1 Probe

Probe: `samples/_probe/g24/real_estate_dx_visual_proxy_v21_probe.ymmp`
Source compact review: `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json`

This is a bounded G-27 visual proxy v2.1 probe. It reduces indexed whiteboard / sticky-note feel by using one focal panel per candidate, stronger hierarchy, and distinct layout grammar for RE-02 / RE-06 / RE-07D. It is not a render, not creative acceptance, and not production readiness.

## Rollup

- Readback status: `passed`
- Inserted items: `96` (ShapeItem=`65`, TextItem=`31`)
- Color-like scan failures: `0`
- Carrier modified in place: `false`

## Pass / Fix / Defer Table

| candidate | classification | visual intent | basis |
| --- | --- | --- | --- |
| `RE-02-beginning` | `pass` | search/database contrast with one central access split | The frame is dominated by a single access-split composition: public portal on the left, private database depth on the right, and a locked threshold between them. |
| `RE-02-development` | `pass` | database-to-public extraction pipeline | The frame uses a left-to-right pipeline: large private database stack, narrow extraction funnel, and a small public portal output. |
| `RE-06-beginning` | `pass` | property comparison board with overload pressure | A single comparison board owns the frame while excess candidate cards crowd its edges, so it reads as property comparison rather than sticky notes. |
| `RE-06-development` | `pass` | selected property with rejected cards and drawback callout | The layout has one selected property sheet in focus, rejected cards pushed aside, and a large drawback callout attached to the selected sheet. |
| `RE-06-turn` | `pass` | document-backed recommendation decision | A document comparison table leads into one green recommendation decision, making the scene feel like a recommendation derived from evidence. |
| `RE-07D-beginning` | `pass` | AI recommendation system focused on one matched card | The AI panel is a dark system block with scan bars pointing to one highlighted property card, reducing whiteboard feel and avoiding product branding. |
| `RE-07D-development` | `pass` | AI recommendation interrupted by risk warning zones | Risk zones are layered over the recommendation as warning bands, so it reads as AI/risk tension rather than a list of notes. |

## Candidate Counts

| candidate | ShapeItems | TextItems | source lines |
| --- | ---: | ---: | --- |
| `RE-02-beginning` | 12 | 4 | 13-24 |
| `RE-02-development` | 10 | 4 | 13-24 |
| `RE-06-beginning` | 10 | 4 | 61-82 |
| `RE-06-development` | 8 | 5 | 61-82 |
| `RE-06-turn` | 9 | 4 | 61-82 |
| `RE-07D-beginning` | 9 | 4 | 130-143 |
| `RE-07D-development` | 7 | 6 | 130-143 |

## Boundaries

- Technical openability: the prior minimal probe and v2 opened in YMM4; this v2.1 readback keeps project-canvas structure and ShapeItem/TextItem-only output.
- Visual semantic adequacy: locally improved from indexed whiteboard toward focal scene proxies with split-screen, pipeline, comparison board, document decision, AI match, and warning-zone grammar. GUI visual judgment is still required.
- Production readiness: not ready. No render, production timing, creative acceptance, external assets, TTS, URL fetch, or publishing.
- Remaining distance to minimal render: if this v2.1 GUI readback passes as meaningful video proxy, the next slice may be minimal render smoke; otherwise keep local fixes in v2.1.
- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.
