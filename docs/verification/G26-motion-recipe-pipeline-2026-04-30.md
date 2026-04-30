# G-26 Motion Recipe Pipeline v1 — 2026-04-30

## 結論

G-26 の制作手順を、単発の `.ymmp` 手作業ではなく **演出意図 → effect候補 → recipe案 → YMM4 review → readback → 採用/棄却** の CLI artifact pipeline として固定した。

新 CLI:

```powershell
uv run python -m src.cli.main build-motion-recipes --format json
```

既定出力:

- `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp`
- `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_readback.json`
- `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1_manifest.md`

## 入力 contract

- brief: `samples/recipe_briefs/g26_motion_recipe_brief.v1.json`
- seed: `samples/canonical.ymmp`
- template source: `samples/templates/skit_group/delivery_v1_templates.ymmp`
- effect catalog: `samples/effect_catalog.json`
- concrete effect samples: `samples/_probe/b2/effect_full_samples.json`
- motion library: `samples/tachie_motion_map_library.json`
- optional corpus: `_tmp/g26/composition/演出_palette_v2.ymmp`

The optional corpus is read as a candidate source only. It does not become accepted evidence by existing.

## 生成ルール

- `.ymmp` zero-generation はしない。既存 YMM4-saved canvas を seed とし、既存 GroupItem/ImageItem template をコピーして編集する。
- 各 sample は `recipe:<goal_id>` Remark を持つ。
- 各 recipe は `proposed` として出力し、YMM4 visual acceptance なしに `accepted_candidate` へ昇格しない。
- chain / compatibility は、YMM4 上で読めたものだけ `compatibility_evidence` に昇格できる。
- Python preview/rendering、画像生成、未知 effect type 合成、G-24 production placement 接続はしない。

## 初期 recipe set

| recipe | intent | primary route |
|---|---|---|
| `nod_clear` | 読みやすい頷き | Rotation |
| `nod_subtle` | 軽い相槌 | Rotation |
| `nod_double` | 強めの二度頷き | Rotation |
| `jump_small` | 軽い驚き | Y |
| `jump_high` | 強い驚き | Y |
| `jump_emphasis` | 着地沈み込みつきジャンプ | Y |
| `panic_crash` | パニック衝撃 | `CrashEffect` + `CameraShakeEffect` |
| `shocked_jump` | effect driven jump | `JumpEffect` |
| `surprised_chromatic` | 色ずれ強調 | Rotation + Zoom + `ChromaticAberrationEffect` |
| `anger_outburst` | 怒りの震え | `RepeatRotateEffect` |
| `shobon_droop` | しょんぼり下がり | Rotation + Y |
| `lean_curious` | 疑問・考え込み | Rotation |

## Machine readback

Current v1 run:

- openability: pass
- recipe GroupItems: 12
- ImageItems: 24
- POSIX asset paths: 0
- blank asset paths: 0
- warning: `CameraShakeEffect` is a community plugin effect and must be visually checked in YMM4.

Validation command:

```powershell
uv run pytest tests/test_motion_recipe.py -q
```

Result:

- `3 passed`

## Acceptance boundary

This pipeline creates review candidates only. It improves the creative exploration loop, but does not approve production use by itself.

YMM4 visual classification must use:

- `pass`
- `wrong motion`
- `body-face drift`
- `too subtle`
- `too strong`
- `screen spacing`
- `asset path`
- `openability`
