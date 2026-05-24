# Real Estate DX Visual Proxy v2 Probe

Probe: `samples/_probe/g24/real_estate_dx_visual_proxy_v2_probe.ymmp`
Source compact review: `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json`

This is a bounded G-27 visual proxy probe. It improves marker-level rectangles into ShapeItem/TextItem primitive compositions for the same 7 ready candidates. It is not a render, not creative acceptance, and not production readiness.

## Rollup

- Readback status: `passed`
- Inserted items: `86` (ShapeItem=`52`, TextItem=`34`)
- Color-like scan failures: `0`
- Carrier modified in place: `false`

## Pass / Fix / Defer Table

| candidate | classification | visual intent | basis |
| --- | --- | --- | --- |
| `RE-02-beginning` | `pass` | public search UI vs broker/private database contrast | Public/private contrast is readable through two labeled panels and a restricted-access badge. |
| `RE-02-development` | `pass` | broker DB panel, public portal card, and property-card flow | Information volume and extraction are represented by many private cards flowing into a small public portal. |
| `RE-06-beginning` | `pass` | property card overload cluster | Too many property choices are represented by crowded cards plus an overload warning badge. |
| `RE-06-development` | `pass` | selected property sheet with drawback marker | A selected sheet, checklist, and drawback badge turn noisy cards into a readable curation proxy. |
| `RE-06-turn` | `pass` | property document editorial comparison | Two document panels and a recommendation ribbon make the proxy feel document-backed rather than a generic strategy diagram. |
| `RE-07D-beginning` | `pass` | AI panel plus matched property card | An abstract AI panel, confidence bars, and matched property card are visible without real product branding. |
| `RE-07D-development` | `pass` | AI-adjacent risk marker and warning state proxy | Boundary, inheritance, and neighborhood risks are separated into visible warning markers around a property context card. |

## Candidate Counts

| candidate | ShapeItems | TextItems | source lines |
| --- | ---: | ---: | --- |
| `RE-02-beginning` | 8 | 5 | 13-24 |
| `RE-02-development` | 10 | 4 | 13-24 |
| `RE-06-beginning` | 8 | 5 | 61-82 |
| `RE-06-development` | 7 | 4 | 61-82 |
| `RE-06-turn` | 7 | 5 | 61-82 |
| `RE-07D-beginning` | 6 | 5 | 130-143 |
| `RE-07D-development` | 6 | 6 | 130-143 |

## Boundaries

- Technical openability: the prior minimal probe opened in YMM4; this v2 readback keeps project-canvas structure and ShapeItem/TextItem-only output.
- Visual semantic adequacy: improved to a proxy-readback target with panels, cards, badges, arrows, checklists, and warning markers, but still needs GUI visual judgment.
- Production readiness: not ready. No render, production timing, creative acceptance, external assets, TTS, URL fetch, or publishing.
- Remaining distance to minimal render: one GUI readback of this v2 probe must confirm the compositions are legible enough before any later minimal render probe can be considered.
- `RE-02-turn` remains blocked outside this output; `RE-07D-turn` remains deferred outside this output.
