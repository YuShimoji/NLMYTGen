# G-26 Motion Primitive Contract / Screen Review — 2026-04-30

## 結論

別レーン報告の G-26 方向性は妥当。G-25 の失敗原因は `.ymmp` openability ではなく、`nudge / scale / rotate / effect_reuse` が motion primitive の意味単位になっていなかったこと。

本ブロックでは、推奨対応を待機せず適用し、Phase 3 仮 contract draft と YMM4 画面確認用 compact review artifact を作成した。

## 適用した判断

- `dominant_channels` は `X / Y / Z / Rotation / Zoom` に加えて `VFX:<EffectType>` を許可する。
- Rotation 系 primitive は `anchor_dependency` を一級フィールドとして持つ。
- `compatible_after` / `forbidden_after` は未観測のため `unknown` のままにする。
- `tilt` / compound motion は、単独または成功重畳 `.ymmp` が登録されるまで contract に含めない。
- G-26 artifact は G-24 production placement に接続しない。

## Draft contracts

Local draft artifacts:

- `_tmp/g26/draft_contracts/index.json`
- `_tmp/g26/draft_contracts/nod.json`
- `_tmp/g26/draft_contracts/exit_left.json`
- `_tmp/g26/draft_contracts/surprise_oneshot.json`

Contract summary:

| primitive | dominant_channels | reset_policy | anchor_dependency |
|---|---|---|---|
| `nod` | `Rotation` | `returns_to_neutral` | required `CenterPointEffect` on `GroupItem`, `Vertical=Bottom`, `Horizontal=Custom`, `X≈524.57`, `Y≈136.85` |
| `exit_left` | `VFX:InOutMoveEffect` | `terminal` | present but requirement unproven; VFX dependency is required |
| `surprise_oneshot` | `Y` | `returns_to_neutral` | not observed |

## Screen review artifact

Generated with the existing `patch-ymmp --skit-group-only --skit-group-compact-review` path, using a YMM4-saved full project canvas as seed. This is not Python preview, not image generation, and not `.ymmp` zero-generation.

Command:

```powershell
uv run python -m src.cli.main patch-ymmp samples/_probe/g24/real_estate_dx_csv_import_base.ymmp _tmp/g26/screen_review/motion_primitive_review_ir.json --skit-group-registry samples/registry_template/skit_group_registry.template.json --skit-group-template-source samples/templates/skit_group/delivery_v1_templates.ymmp --skit-group-only --skit-group-compact-review --skit-group-review-spacing 240 -o _tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp
```

Output:

- `_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp`
- `_tmp/g26/screen_review/readback.json`

Machine readback:

| frame | remark | length | dominant evidence |
|---:|---|---:|---|
| 0 | `skit_group:delivery_nod_v1 utt:1` | 41 | Rotation `[0.0, -6.2, 0.0]`, `CenterPointEffect` |
| 240 | `skit_group:delivery_surprise_oneshot_v1 utt:2` | 174 | normalized Y `[462.5, 412.5, 462.5, 462.5]` |
| 480 | `skit_group:delivery_exit_left_v1 utt:3` | 41 | `CenterPointEffect` + `InOutMoveEffect` |

Openability/readback:

- `canvas=true`
- `Timelines[].LayerSettings.Items` shape OK
- total items: 361
- inserted GroupItems: 3
- POSIX asset paths: 0
- blank asset paths: 0

## 妥当性評価

R1/R3/R4 の実施内容は repo 状態と整合する。`00b2676` は存在し、branch は `origin/codex/g24-nod-sync-adoption` より ahead 1。`_tmp/g26/route_readback/RECONCILE.md` と route readback JSON も実在する。

ただし、別レーン報告時点では Phase 3 contract draft と画面確認用 artifact は未生成だった。本ブロックでその未完了分を埋めた。

未解決として残すもの:

- `tilt` 単独 primitive の観測
- 2 motion 連続適用例による compatibility evidence
- G-26 と G-24 production placement の接続可否判断

`samples/real_estate_dx_csv_import_base.ymmp` の root 重複は破棄済み。screen review seed は既存の `samples/_probe/g24/real_estate_dx_csv_import_base.ymmp` を使用する。`docs/verification/VISUAL-RETURN-ANALYSIS-CONSISTENCY-2026-04-29.md` は本コミットでトラック化。

## Evidence Gate Follow-up

2026-04-30 の次ブロックで、本計画の assistant-owned 部分を再検証した。

Machine gate:

- source: `_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp`
- machine status: `machine_pass`
- JSON parse: `_tmp/g26/draft_contracts/*.json` and `_tmp/g26/screen_review/readback.json` pass
- openability: pass (`Timelines[].LayerSettings.Items`, 1 timeline, 361 items)
- inserted GroupItems: 3
- inserted frames: 0 / 240 / 480
- POSIX asset paths: 0
- blank asset paths: 0
- follow-up readback: `_tmp/g26/screen_review/evidence_gate_machine_readback.json`

Primitive machine readback:

| frame | primitive | status | machine evidence |
|---:|---|---|---|
| 0 | `nod` | machine pass | Rotation `[0.0, -6.2, 0.0]`, `CenterPointEffect` |
| 240 | `surprise_oneshot` | machine pass | Y `[462.5, 412.5, 462.5, 462.5]`, no `VideoEffects` |
| 480 | `exit_left` | machine pass | `CenterPointEffect` + `InOutMoveEffect` |

Visual acceptance:

- status: `not_recorded`
- reason: this block can verify `.ymmp` structure and readback, but cannot truthfully judge YMM4 screen appearance without operator visual confirmation.
- classification is not treated as FAIL; it remains a pending creative/visual acceptance item.

Tilt / compatibility source scan:

- scanned repo-local `.ymmp` files: 53
- matching tilt / chain remarks: 0
- scan output: `_tmp/g26/screen_review/tilt_chain_source_scan.json`
- result: `tilt` remains out-of-contract; `compatible_after` / `forbidden_after` remain `unknown`

Do not infer compatibility pairs from the existing three single primitive samples. For contract promotion, the next valid evidence is YMM4 visual acceptance of a concrete review clip or a YMM4-authored source clip with fixed Remarks:

- `delivery_tilt_left_v1`
- `delivery_tilt_right_v1`
- `chain_nod_exit_left_v1`
- `chain_tilt_left_exit_left_v1`
- `chain_tilt_left_surprise_oneshot_v1`

This gate must not be read as "assistant cannot propose or create new goal-motion samples." It only blocks contract promotion without visual evidence. Purpose-driven review labs are valid assistant work when they start from an existing YMM4-saved canvas and existing GroupItem/ImageItem template source, then patch transform values for a named acting goal.

## Purpose-driven recipe lab correction

The previous compact screen artifact was structurally correct but too weak as a sample: it mainly placed the already-known primitives and did not actively explore "うなずき" / "ジャンプ" / combination goals. This was a process failure caused by over-reading the tilt/chain evidence gate as a creation ban.

New local review artifact:

- `_tmp/g26/recipe_lab/g26_goal_motion_recipe_lab.ymmp`
- `_tmp/g26/recipe_lab/recipe_lab_readback.json`
- `_tmp/g26/recipe_lab/README.md`

Readback:

- seed: `samples/canonical.ymmp`
- template source: `samples/templates/skit_group/delivery_v1_templates.ymmp`
- openability: pass
- inserted recipe GroupItems: 12
- inserted ImageItems: 24
- POSIX asset paths: 0
- blank asset paths: 0

Recipes:

| frame | recipe | goal | route |
|---:|---|---|---|
| 0 | `nod_subtle` | light agreement / backchannel | Rotation `[0, -4, 0]` |
| 180 | `nod_clear` | readable nod / confirmation | Rotation `[0, -10, 0]` |
| 360 | `nod_double` | stronger double nod | Rotation `[0, -7, 0, -5, 0]` |
| 540 | `jump_small` | light surprise / pop emphasis | Y `[462.5, 427.5, 462.5]` |
| 720 | `jump_high` | strong surprise / discovery | Y `[462.5, 372.5, 462.5]` |
| 900 | `jump_emphasis` | jump with landing dip | Y `[462.5, 392.5, 462.5, 472.5, 462.5]` |
| 1080 | `tilt_left_hold` | doubt / thinking candidate | Rotation `[0, -10, -10, 0]` |
| 1260 | `tilt_right_hold` | counterpart-facing reaction candidate | Rotation `[0, 10, 10, 0]` |
| 1440 | `chain_nod_to_jump_01_nod` | nod before jump | Rotation `[0, -8, 0]` |
| 1488 | `chain_nod_to_jump_02_jump` | jump after nod | Y `[462.5, 392.5, 462.5]` |
| 1800 | `chain_jump_to_exit_01_jump` | jump before exit | Y `[462.5, 392.5, 462.5]` |
| 1860 | `chain_jump_to_exit_02_exit` | exit after jump | `CenterPointEffect` + `InOutMoveEffect` |

Acceptance handling:

- PASS on a standalone recipe can promote it to a candidate primitive draft.
- PASS on a chain can become compatibility evidence.
- FAIL must record a failure class (`wrong motion`, `body-face drift`, `screen spacing`, `too subtle`, `too strong`, `openability`, `asset path`) rather than forcing `compatible_after` / `forbidden_after`.
- Until visual acceptance is recorded, `FEATURE_REGISTRY` status remains `proposed` and no G-24 production placement connection is made.

## Follow-up: reusable recipe pipeline

The one-off recipe lab has been superseded by a reusable CLI artifact route:

```powershell
uv run python -m src.cli.main build-motion-recipes --format json
```

This route keeps the same safety boundary but makes the creative process repeatable:

1. read a goal brief,
2. inspect effect catalog / concrete effect samples / motion library,
3. build proposed recipes,
4. write a YMM4-openable review `.ymmp`,
5. emit machine readback and a review manifest.

Current proof is tracked separately in [G26-motion-recipe-pipeline-2026-04-30.md](G26-motion-recipe-pipeline-2026-04-30.md).
