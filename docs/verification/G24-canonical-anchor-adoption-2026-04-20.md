# G-24 canonical anchor adoption (2026-04-20)

## Why this exists

`samples/canonical.ymmp` was added after the earlier workflow-breakage audit. That changes the G-24 state in one specific way:

- the repo now has a **canonical skit_group anchor artifact**
- it also has **project-resident starter copies** inside that canonical corpus
- but it still does **not** have a full standalone native template library asset set for every exact catalog intent

This packet records that narrower upgrade so we do not over-promote the state to full G-24 completion.

2026-04-21 sync:

- starter 2 intents (`enter_from_left` / `surprise_oneshot`) now also have standalone native template export per user report
- this upgrades the first starter batch, but still does **not** imply that every exact catalog intent is exported

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
- Layer 9 `GroupItem` at frame `306` with `Remark = delivery_enter_from_left_v1`
- Layer 9 `GroupItem` at frame `658` with `Remark = delivery_surprise_oneshot_v1`
- all 3 groups keep `GroupRange = 2` with adjacent Layer 10/11 `ImageItem` pairs

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
- starter copies for `enter_from_left` and `surprise_oneshot` are now **repo-resident inside `samples/canonical.ymmp`**
- starter exports for `enter_from_left` and `surprise_oneshot` are now **synced as standalone native templates**
- registry intents can be classified as exact against the canonical corpus
- `audit-skit-group` is no longer blocked by `SKIT_CANONICAL_GROUP_MISSING` when run on the canonical corpus

## What is still not established

- a standalone **native template library asset set** for the remaining exact catalog intents
- full template-first completion as an asset set beyond the starter 2 intents
- fallback/manual_note proof against derived template gaps in a production-like corpus

That is why Capability Atlas now promotes `skit_group.canonical_anchor` plus starter exports `skit_group.intent.enter_from_left` / `skit_group.intent.surprise_oneshot` to `direct_proven`, while the remaining `skit_group.intent.*` stays `template_catalog_only`.

## skit_01 positioning after adoption

The repo now has two different proof roles:

- old source/proof corpus (`samples/characterAnimSample/haitatsuin_2026-04-12.ymmp` + `_tmp/skit_01_v2_verify.ymmp`)
  - mechanical motion proof
  - old corpus still reproduces `SKIT_CANONICAL_GROUP_MISSING`
- `samples/canonical.ymmp`
  - canonical anchor proof
  - exact template classification proof

Do not collapse these into one statement like "skit_01 is fully complete".

## Starter batch authored-copy sync (2026-04-21)

The first user-owned starter batch is now present in `samples/canonical.ymmp` as:

- `enter_from_left`
- `surprise_oneshot`

The remaining exact intents (`nod`, `deny_oneshot`, `exit_left`) stay in the registry catalog and remain mechanically classifiable on the canonical corpus, but they are **not** counted as exported starter native assets.

2026-04-21 export sync changes Capability Atlas only partially:

- `skit_group.intent.enter_from_left` -> `direct_proven`
- `skit_group.intent.surprise_oneshot` -> `direct_proven`
- `skit_group.intent.deny_oneshot` / `exit_left` / `nod` -> `template_catalog_only`

## Next frontier

The next frontier is no longer ManualSample recreation or starter export.
It is:

1. keep the starter 2 intents synchronized as exported assets
2. expand the same cautious gate to `nod`
3. then to `deny_oneshot`
4. then to `exit_left`
