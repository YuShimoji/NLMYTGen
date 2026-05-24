# G-24 Production-Like Gap Classification — existing IR probes (2026-04-27)

## Purpose

Classify gaps that appear when existing production-like IR files are resolved against the completed G-24 v1 skit_group template set.

This pass is classification only. It does not create new motion templates, edit the registry, change CLI/API contracts, or generate a confirmation `.ymmp`.

## Inputs

- Canonical skit_group corpus: `samples/canonical.ymmp`
- Registry: `samples/registry_template/skit_group_registry.template.json`
- IR A: `samples/_probe/b2/haitatsuin_ir_oneshot_block2.json`
- IR B: `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json`

`samples/haitatsuin_2026-04-12_g24_proof.ymmp` remains compact template/sample proof and is not used as validation input.

## Commands

```bash
python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/b2/haitatsuin_ir_oneshot_block2.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text

python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

## Results

### IR A — `haitatsuin_ir_oneshot_block2.json`

Summary: `exact=3 / fallback=0 / manual_note=1`

| utt | intent | resolution | template / note | classification |
| --- | --- | --- | --- | --- |
| 1 | `enter_from_left` | `exact` | `delivery_enter_from_left_v1` | covered by v1 |
| 3 | `surprise_oneshot` | `exact` | `delivery_surprise_oneshot_v1` | covered by v1 |
| 5 | `panic_shake` | `manual_note` | intent not registered | new-template candidate, not an alias by default |
| 8 | `deny_oneshot` | `exact` | `delivery_deny_oneshot_v1` | covered by v1 |

### IR B — `haitatsuin_ir_10utt_v3_motions.json`

Summary: `exact=1 / fallback=0 / manual_note=3`

| utt | intent | resolution | template / note | classification |
| --- | --- | --- | --- | --- |
| 1 | `nod` | `exact` | `delivery_nod_v1` | covered by v1 |
| 3 | `surprise_jump` | `manual_note` | intent not registered | alias candidate for `surprise_oneshot` |
| 5 | `panic_shake` | `manual_note` | intent not registered | new-template candidate, not an alias by default |
| 8 | `deny_shake` | `manual_note` | intent not registered | alias candidate for `deny_oneshot` |

## Gap Classification

- **Alias candidates**: `surprise_jump -> surprise_oneshot`, `deny_shake -> deny_oneshot`.
- **New-template candidate**: `panic_shake`. It appears in both production-like IRs, but the current v1 set has no clear equivalent. Do not map it to `deny_oneshot` automatically without user acceptance, because panic reads as stronger / less controlled than a one-shot denial.
- **Already covered**: `enter_from_left`, `surprise_oneshot`, `deny_oneshot`, `nod`.

## User Review Points

- Confirm whether `surprise_jump` can be treated as the same production intent as `surprise_oneshot`.
- Confirm whether `deny_shake` can be treated as the same production intent as `deny_oneshot`.
- Decide later whether `panic_shake` is worth a new template, a fallback/manual note, or should be avoided in production IR wording.

## Next Frontier

- Next plan should choose between alias registration and real production IR selection.
- If alias registration is chosen, only alias labels should be added; no new motion/template authoring is required.
- If real production IR selection is chosen, use this report to interpret unresolved labels before requesting any new YMM4 work.
