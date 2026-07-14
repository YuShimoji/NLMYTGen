# Generic static-layout runtime observation result

> **BOUNDED RUNTIME OBSERVATION / SAME-MACHINE EXACT COMPOSITE / NOT PRODUCTION**

The exact neutral probe was opened by the human operator in YMM4 and all three bounded visual checks passed. Structural facts remain machine-verified; the visual answers are operator-observed evidence.

## Observed result

- Probe: `generic_static_image_text_subtitle_safe_area_v1`
- Collected: `2026-07-14T17:36:50.239082Z`
- Linked subtitle readability/non-overlap: `pass`
- Image visibility/crop/anchor: `pass`
- Text visibility/wrapping/anchor: `pass`
- Observation grade: `observed_by_operator`
- Structural grade: `verified`

## Exact bounded composite

- One unchanged VoiceItem with its linked subtitle settings.
- One static 640x360 opaque RGB ImageItem in the upper-left conservative zone.
- One short independent TextItem (`PROBE LABEL`) in the upper-right conservative zone.
- 1920x1080, 60 fps, 109-frame Voice span, disjoint bottom subtitle reserve.
- Same-machine exact project and asset only; zero motion, fade, effect, transition, non-default transform, save, screenshot evidence, or render.

## Identity and evidence boundary

- Ignored project: `samples/visual_composition_lab/runtime_probe/local_outputs/generic_static_layout_probe.local.ymmp` (`100d4ebcd31e1665db90cc688492efec211d899e579d013e751c9643cc98eebc`)
- Ignored asset: `samples/visual_composition_lab/runtime_probe/local_outputs/assets/generic_probe_image.png` (`ad1f93bf29d07372a955645326129127a96f989786db642969ef77aad84b00b9`)
- Ignored operator result SHA-256: `a881c5e6bfd8be167b32c8aa7b232d0c4ed31b494563e192091aba119419dd03`
- Local project, asset, batch state, observations, result, and archives remain ignored and untracked.
- No global capability row was regraded. The result is recorded only as `bounded_runtime_observed_pass` for this exact composite.

This does not establish arbitrary subtitle typography, longer text, alternate image dimensions or anchors, motion/effects, cross-machine portability, C4 render evidence, C5 reuse, Route A behavior, production readiness, rights clearance, or publication approval.

Machine-readable authority: `runtime_observation_receipt.json` and `runtime_observation_readback.json`.
