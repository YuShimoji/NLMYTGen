# G-24 Production-Use Validation Report — repo probe (2026-04-27)

## Purpose

Validate the completed G-24 v1 skit_group template set in repo-local probe mode, without creating new YMM4 motions or generating a confirmation `.ymmp`.

## Inputs

- YMM4 corpus: `samples/canonical.ymmp`
- IR: `samples/_probe/skit_01/skit_01_ir.json`
- Registry: `samples/registry_template/skit_group_registry.template.json`

Do not use `samples/haitatsuin_2026-04-12_g24_proof.ymmp` as validation input in this pass. It is currently a compact template/sample proof and does not contain the canonical voice-anchored group anchor.

## Command

```bash
python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

## Result

- Anchor group: `haitatsuin_delivery_v1`
- Anchor remark: `haitatsuin_delivery_main`
- Anchor layer: `9`
- Summary: `exact=5 / fallback=0 / manual_note=0`
- Verdict: **PASS — repo-probe production-use validation is mechanically clean**

| utt | intent | resolution | template | user review point |
| --- | --- | --- | --- | --- |
| 1 | `enter_from_left` | `exact` | `delivery_enter_from_left_v1` | Landing position, overshoot, settle timing |
| 2 | `nod` | `exact` | `delivery_nod_v1` | Nod amplitude, does not dominate scene |
| 3 | `surprise_oneshot` | `exact` | `delivery_surprise_oneshot_v1` | Y-axis jump height, one-shot behavior |
| 8 | `deny_oneshot` | `exact` | `delivery_deny_oneshot_v1` | X-axis sway range, one-shot behavior |
| 10 | `exit_left` | `exact` | `delivery_exit_left_v1` | Exit direction, speed, scene closure timing |

## Next Frontier

- Move from repo-probe validation to the same validation shape on a real production IR / compatible production corpus.
- If real production returns `exact=5`, continue production-use hardening and user review.
- If `fallback` / `manual_note` / missing-template appears, classify the gap before authoring any new motion.
- No new YMM4 native template is requested from the user unless that concrete production gap requires it.
