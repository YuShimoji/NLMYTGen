# G-24 Real Estate DX YMM4 Production Packet (2026-04-27)

> Historical note: this packet is retained as a handoff record, not as the current frontier. The project direction has moved back to `.ymmp` write capability: `exact` / `fallback` skit_group cues must be placed by `patch-ymmp --skit-group-template-source`, and operator hand placement is not considered production automation.

## Purpose

Turn the validated real estate DX CSV / skit_group IR artifacts into an operator-ready S-4 / S-6 packet for YMM4 production.

This packet does not add a new CLI, author new motions, alias `panic_shake`, change registry semantics, or generate a confirmation `.ymmp`.

## Inputs

- Corrected script: `samples/不動産DX_魔法の鍵とキュレーション.txt`
- YMM4 CSV: `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`
- Skit group IR: `samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json`
- Audit corpus: `samples/canonical.ymmp`
- Skit group registry: `samples/registry_template/skit_group_registry.template.json`

## YMM4 S-4 Import

- **Open target**: a copied production YMM4 template project, not `samples/haitatsuin_2026-04-12_g24_proof.ymmp`.
- **Source artifact**: `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`.
- **Operation**: YMM4 `ツール → 台本読み込み`で CSV を読み込み、話者 `れいむ` / `まりさ` を確認してタイムラインへ追加する。
- **Acceptance meaning**: YMM4 voice items and subtitles are created from the 352-row CSV without remapping the speakers.
- **B-17 residue**: 18 rows were overflow candidates during CSV build. Treat them as normal YMM4 residual observation only if they visibly overflow in the actual project.

## S-6 Skit Group Cues

All skit_group actor cues target `motion_target: "layer:9"`.

| IR index | beat | motion | resolution | production handling |
| --- | --- | --- | --- | --- |
| 1 | magic key / secret library opener | `enter_from_left` | exact | Apply/use `delivery_enter_from_left_v1` |
| 15 | REINS as private VIP club | `nod` | exact | Apply/use `delivery_nod_v1` |
| 35 | hidden “darkness” reveal | `surprise_jump` | fallback | Use `delivery_surprise_oneshot_v1` |
| 39 | dual agency / conflict of interest | `deny_shake` | fallback | Use `delivery_deny_oneshot_v1` |
| 104 | SNS gray zone warning | `panic_shake` | manual_note | Do not alias now; choose manual note, wording avoidance, or future new template after review |
| 143 | gatekeeper exits, curator remains | `exit_left` | exact | Apply/use `delivery_exit_left_v1` |

## Decision Rules

- `exact` and `fallback` are production-use candidates.
- `panic_shake` remains intentionally unresolved; do not map it to `deny_oneshot` without user acceptance.
- Do not request a new YMM4 native template unless this or later production work repeatedly needs a stronger panic/shaking acting beat.
- If S-4/S-6 reveals a concrete gap, classify it as `fallback`, `manual_note`, `new_template_candidate`, `B-17 residue`, or `repo bug` before adding new motion work.

## Verification

Run before using this packet as the current production input:

```bash
uv run python -m json.tool samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json

uv run python -m src.cli.main audit-skit-group \
  samples/canonical.ymmp \
  samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json \
  --skit-group-registry samples/registry_template/skit_group_registry.template.json \
  --format text
```

Expected audit summary: `exact=3 / fallback=2 / manual_note=1`.
