# G-24 Production IR Generation Flow Sync (2026-04-27)

## Purpose

Reflect the passed minimal production IR shape into the real production IR generation flow.

This pass does not search more repo-local IRs, author new YMM4 motions, edit registry aliases, change CLI/API contracts, or generate a confirmation `.ymmp`.

## Flow Changes

- `docs/S6-production-memo-prompt.md` now instructs IR generators to emit `motion_target: "layer:9"` for skit_group actor utterances.
- `docs/S6-production-memo-prompt.md` limits skit_group actor `motion` to existing v1 intents or registered alias intents.
- `docs/PRODUCTION_IR_SPEC.md` records the G-24 production IR shape and points to `samples/g24_skit_group_minimal_production_ir.json`.
- `docs/SKIT_GROUP_TEMPLATE_SPEC.md` records the same generation rule and the fixed `audit-skit-group` command.
- `docs/WORKFLOW.md` adds the S-6 skit_group template preflight step.

## Allowed skit_group intents

Exact v1:

- `enter_from_left`
- `surprise_oneshot`
- `nod`
- `deny_oneshot`
- `exit_left`

Alias:

- `surprise_jump -> delivery_surprise_oneshot_v1`
- `deny_shake -> delivery_deny_oneshot_v1`

Manual/unresolved candidate:

- `panic_shake`

## Validation

```bash
python3 -m json.tool samples/g24_skit_group_minimal_production_ir.json >/tmp/g24_min_ir.json.check

python3 -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/g24_skit_group_minimal_production_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

Result: `exact=3 / fallback=2 / manual_note=1`.

## Next Use

For the next real production case:

1. Generate or edit the production IR so skit_group actor utterances include `motion_target: "layer:9"`.
2. Use only exact v1 intents or registered aliases unless deliberately surfacing an unresolved candidate.
3. Run `audit-skit-group` against `samples/canonical.ymmp`.
4. Classify only `manual_note` entries such as `panic_shake`; do not reopen motion authoring for exact/fallback entries.
