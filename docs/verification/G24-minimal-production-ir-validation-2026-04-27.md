# G-24 Minimal Production IR Validation — alias-enabled registry (2026-04-27)

## Purpose

Create the minimum production-oriented skit_group IR input because no repo-local real production IR currently targets the canonical skit_group layer.

This pass does not search more repo-local IRs, author new YMM4 motions, edit the registry, change CLI/API contracts, or generate a confirmation `.ymmp`.

## Inputs

- Corpus: `samples/canonical.ymmp`
- IR: `samples/g24_skit_group_minimal_production_ir.json`
- Registry: `samples/registry_template/skit_group_registry.template.json`

The IR is a minimal production-intake sample for a delivery-person skit_group actor. It targets `motion_target: layer:9` and intentionally covers:

- exact v1 intents
- registered production-like aliases
- one unresolved `panic_shake` case

## Command

```bash
python3 -m json.tool samples/g24_skit_group_minimal_production_ir.json >/tmp/g24_min_ir.json.check

python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/g24_skit_group_minimal_production_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

## Result

- Anchor group: `haitatsuin_delivery_v1`
- Anchor remark: `haitatsuin_delivery_main`
- Anchor layer: `9`
- Summary: `exact=3 / fallback=2 / manual_note=1`
- Verdict: **PASS as minimum production-input sample; one intentional unresolved label remains classified**

| utt | requested intent | resolution | template / note | classification |
| --- | --- | --- | --- | --- |
| 1 | `enter_from_left` | `exact` | `delivery_enter_from_left_v1` | covered by v1 |
| 3 | `surprise_jump` | `fallback` | `delivery_surprise_oneshot_v1` | safe alias |
| 4 | `panic_shake` | `manual_note` | intent not registered | keep unresolved; manual/new-template candidate |
| 5 | `deny_shake` | `fallback` | `delivery_deny_oneshot_v1` | safe alias |
| 6 | `nod` | `exact` | `delivery_nod_v1` | covered by v1 |
| 7 | `exit_left` | `exact` | `delivery_exit_left_v1` | covered by v1 |

## Unresolved Classification

`panic_shake` is not mapped to an existing template in this pass.

- **Current handling**: `manual_note`
- **New-template candidate**: yes, only if real production repeatedly needs a stronger panic reaction
- **IR wording avoidance**: acceptable when production can express the beat with `surprise_jump`, `deny_shake`, or narration instead
- **Registry action**: none; do not alias `panic_shake` to `deny_oneshot` or `surprise_oneshot` without user acceptance

## Next Use

Use `samples/g24_skit_group_minimal_production_ir.json` as the smallest valid input shape for future real production skit_group IRs:

- set skit_group actor motions on utterances
- include `motion_target: layer:9`
- pair with `samples/canonical.ymmp` for preflight
- report `exact / fallback / manual_note` before any new motion authoring
