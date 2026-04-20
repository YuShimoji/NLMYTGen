# G-24 canonical anchor adoption (2026-04-20)

## Why this exists

`samples/canonical.ymmp` was added after the earlier workflow-breakage audit. That changes the G-24 state in one specific way:

- the repo now has a **canonical skit_group anchor artifact**
- but it still does **not** have a repo-resident derived native template asset set

This packet records that narrower upgrade so we do not over-promote the state to full G-24 completion.

## Canonical artifact facts

Trusted canonical artifact:

- ymmp: `samples/canonical.ymmp`
- canonical remark: `haitatsuin_delivery_main`
- anchor layer: `9`
- composition: `ImageItem` children only (body + face)
- base pose: left-facing

Repo-local inspection confirms the following item shape:

- Layer 10 `ImageItem`
- Layer 11 `ImageItem`
- Layer 9 `GroupItem` with `Remark = haitatsuin_delivery_main`

## Audit result

Command:

```bash
python -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/_probe/skit_01/skit_01_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format json
```

Result summary:

- `status=ok`
- `group_key=haitatsuin_delivery_v1`
- `anchor_remark=haitatsuin_delivery_main`
- `anchor_layer=9`
- `summary: exact=5 / fallback=0 / manual_note=0`

Resolved intents:

- `enter_from_left` -> exact
- `nod` -> exact
- `surprise_oneshot` -> exact
- `deny_oneshot` -> exact
- `exit_left` -> exact

## What is established now

- canonical anchor existence is now **repo-resident and mechanically provable**
- registry intents can be classified as exact against the canonical corpus
- `audit-skit-group` is no longer blocked by `SKIT_CANONICAL_GROUP_MISSING` when run on the canonical corpus

## What is still not established

- repo-resident **derived native template assets**
- full template-first completion as an asset set
- fallback/manual_note proof against derived template gaps in a production-like corpus

That is why Capability Atlas promotes only `skit_group.canonical_anchor` to `direct_proven`, while `skit_group.intent.*` remains `template_catalog_only`.

## skit_01 positioning after adoption

The repo now has two different proof roles:

- old source/proof corpus (`samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` + `_tmp/skit_01_v2_verify.ymmp`)
  - mechanical motion proof
  - old corpus still reproduces `SKIT_CANONICAL_GROUP_MISSING`
- `samples/canonical.ymmp`
  - canonical anchor proof
  - exact template classification proof

Do not collapse these into one statement like "skit_01 is fully complete".

## Next frontier

The next user-owned frontier is not ManualSample recreation.
It is:

1. save 1-2 derived native templates from `samples/canonical.ymmp`
2. sync registry entries to those assets
3. accumulate exact / fallback / manual_note proof one step at a time
