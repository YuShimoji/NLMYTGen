# G-24 capability atlas packet (2026-04-20)

## Why this packet exists

`ManualSample.ymmp` が欠落したままでも、operator が `IR -> registry -> ymmp` のどこで判断すべきかを repo 内だけで説明できる状態が必要になった。

今回の Capability Atlas は、次の混同を止めるための正本である。

- route が観測されたこと
- patch path が実装されていること
- template-first として completion したこと
- raw effect が repo に存在すること

これらは同義ではない。

## Evidence source

Atlas は次の repo-local artifact を根拠にする。

- `samples/effect_catalog.json`
- `samples/timeline_route_contract.json`
- `samples/tachie_motion_map_library.json`
- `samples/registry_template/skit_group_registry.template.json`
- `docs/PRODUCTION_IR_CAPABILITY_MATRIX.md`
- `docs/verification/G12-timeline-route-measurement.md`
- `docs/verification/skit_01-workflow-breakage-audit-2026-04-20.md`

機械台帳は `python scripts/build_capability_atlas.py` で `samples/_generated/capability_atlas.json` に再生成する。

## Classification examples

### `direct_proven`

- `speaker_tachie.motion`
  - route contract が `TachieItem.VideoEffects` を観測済み
  - motion library と adapter path が存在
- `overlay_se.overlay`
  - registry + timing anchor + patch path が正本化済み
- `transition.fade`
  - fade-family は G-12 / capability matrix で成立
- `skit_group.intent.enter_from_left`
- `skit_group.intent.surprise_oneshot`
  - manual acceptance + production adoption proof + standalone native template export が starter 2 件で同期済み

### `template_catalog_only`

- `skit_group.intent.deny_oneshot`
- `skit_group.intent.exit_left`
- `skit_group.intent.nod`

これらは registry と preflight で分類できるが、**standalone native template asset**の completion proof はまだ無い。

### `probe_only`

- raw effect atom (`effect_atom.*`)

`effect_catalog.json` は YMM4 effect の辞書として有用だが、IR の正規契約ではない。catalog に存在するだけでは production path に昇格しない。

### `unsupported`

- non-fade transition
- raw effect 名からの IR 直書き
- repo 根拠のない template route

## Why old `skit_01` still does not become a standalone-template proof by itself

old `skit_01` は mechanical motion proof としては有益だが、それ単体で G-24 completion を名乗れるわけではない。

理由:

- `audit-skit-group` は old corpus で `SKIT_CANONICAL_GROUP_MISSING` を返す
- 欠落した ManualSample を gate に戻さない
- surviving ymmp は motion-labeled artifact としては使えるが、canonical template asset の証跡にはならない
- starter 2 件の `direct_proven` は **canonical copy + proof corpus + standalone export sync** の 3 点セットで成立している

したがって Atlas でも remaining `skit_group` template intent は `template_catalog_only` に留める。

## Resulting operator rule

次回以降の operator 判断は、まず Atlas を見て support level を確認する。

- `direct_proven` -> 既存 adapter path で前進
- `template_catalog_only` -> registry / preflight / asset authoring の話として扱う
- `probe_only` -> material planning / registry design の材料として扱う
- `unsupported` -> route measurement か方針変更が先
