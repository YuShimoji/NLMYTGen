# G-24 Alias Registration — production-like IR hardening (2026-04-27)

## Purpose

Move the previous production-like gap classification out of the planning loop by registering safe label aliases in the skit_group registry.

This pass does not create new YMM4 motion templates, generate `.ymmp` samples, or map `panic_shake`.

## Changes

- `surprise_jump` now falls back to `delivery_surprise_oneshot_v1`.
- `deny_shake` now falls back to `delivery_deny_oneshot_v1`.
- `panic_shake` remains `manual_note` because it reads stronger than the current v1 denial / surprise templates.

## Validation

```bash
python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/b2/haitatsuin_ir_oneshot_block2.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

Result: `exact=3 / fallback=0 / manual_note=1`.

```bash
python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

Result: `exact=1 / fallback=2 / manual_note=1`.

```bash
uv run pytest tests/test_capability_atlas.py tests/test_skit_group_audit.py -q -s
```

Result: PASS.

## Next Frontier

Use a selected real production IR/corpus for the same `exact / fallback / manual_note` report.

Do not ask for additional YMM4 motion authoring unless the real production report leaves a concrete unresolved gap after aliases.
