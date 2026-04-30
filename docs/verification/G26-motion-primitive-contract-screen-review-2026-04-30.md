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
