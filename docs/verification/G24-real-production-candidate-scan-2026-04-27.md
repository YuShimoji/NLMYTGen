# G-24 Real Production Candidate Scan — alias-enabled registry (2026-04-27)

## Purpose

Find a repo-local real production IR/corpus that can validate the alias-enabled G-24 skit_group registry, then report `exact / fallback / manual_note`.

This pass does not author new YMM4 motions, edit the registry, change CLI/API contracts, or generate a confirmation `.ymmp`.

## Validation Criterion

A useful G-24 production validation target must include at least one IR utterance with:

- a non-empty `motion`
- a `motion_target` that resolves to the canonical skit_group anchor layer
- a compatible corpus containing the canonical GroupItem anchor

Current compatible corpus for mechanical audit:

- `samples/canonical.ymmp`
- anchor group: `haitatsuin_delivery_v1`
- anchor remark: `haitatsuin_delivery_main`
- anchor layer: `9`

## Repo Scan Result

The repo-local JSON scan found only probe IRs with skit_group layer-9 targets:

| IR | classification | layer-9 skit_group targets |
| --- | --- | ---: |
| `samples/_probe/skit_01/skit_01_ir.json` | repo probe, already audited | 5 |
| `samples/_probe/b2/haitatsuin_ir_oneshot_block2.json` | production-like probe, already audited | 4 |
| `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json` | production-like probe, already audited | 4 |

No repo-local real production IR with skit_group `motion_target` entries was identified.

## Audit Commands

The following production-ish repo candidates were audited against `samples/canonical.ymmp` and the alias-enabled registry:

```bash
python3 -m src.cli.main audit-skit-group samples/canonical.ymmp <ir> \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

## Results

| IR | exact | fallback | manual_note | classification |
| --- | ---: | ---: | ---: | --- |
| `samples/Part 1+2IR.Json` | 0 | 0 | 0 | no skit_group-targeted entries |
| `samples/Part 1+2IR_idle.json` | 0 | 0 | 0 | no skit_group-targeted entries |
| `samples/Part 1+2IR_row_range.json` | 0 | 0 | 0 | no skit_group-targeted entries |
| `samples/global_crisis_ir.Json` | 0 | 0 | 0 | no skit_group-targeted entries |
| `samples/chabangeki_e2e_ir.json` | 0 | 0 | 0 | motion exists, but no skit_group `motion_target` |
| `samples/micro.json` | 0 | 0 | 0 | motion exists, but no skit_group `motion_target` |
| `samples/n3_multi_utterance_ir.json` | 0 | 0 | 0 | no skit_group-targeted entries |
| `samples/test_ir.json` | 0 | 0 | 0 | no skit_group-targeted entries |

These are mechanically successful audits, but they do not validate alias coverage because the audited IRs contain no utterance targeting the canonical skit_group layer.

## Conclusion

Repo-local real production candidate is insufficient for the requested next frontier.

The current alias-enabled registry state remains:

- `surprise_jump -> delivery_surprise_oneshot_v1`
- `deny_shake -> delivery_deny_oneshot_v1`
- `panic_shake` remains `manual_note` / new-template candidate

## Minimal Next Input

Provide or point to one real production IR/corpus pair that includes skit_group-targeted utterances, or provide a real production IR intended to be paired with `samples/canonical.ymmp` for preflight.
