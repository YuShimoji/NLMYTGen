# G-26 Motion Recipe Pipeline Slice 3 End-to-End Proof — 2026-04-30

## 結論

[MOTION_PRODUCTION_PIPELINE.md](../MOTION_PRODUCTION_PIPELINE.md) の 5-phase pipeline を、自然言語シーン記述から YMM4 review artifact 生成まで end-to-end で 1 周回し、機械検証 pass を確認した。同時に **「novel goal_id = preset 拡張必須」** という現行アーキテクチャ制約を発見し、S-5 prompt と PIPELINE doc に明文化した。

## 入力 (自然言語シーン)

| Scene | 自然言語 |
|-------|---------|
| A | ふと何かに気づいて、軽く目を見開いてからゆっくり頷く |
| B | 落ち込んで体を傾けたまま、ぼんやり画面がぼやける |

## Phase A: S-5 motion brief prompt 判定 (LLM 推論をトレース)

### Scene A → `realization_nod`

S-5 prompt の 7-step 判定フロー:

1. **emotion**: `agreement` (頷きが終端、最も支配的。途中の thinking は短いので副次)
2. **既存ラベル fit**: `nod_clear` に近いが「気づき」の zoom-in 先行がない → 既存 fit せず
3. **novel goal_id 命名**: `<emotion>_<descriptor>` ルールから `realization_nod`
4. **intensity**: `medium` (見開きは軽く、頷きはゆっくり)
5. **duration_frames**: agreement medium 既定 48f → realization では zoom phase + nod phase が必要 → 90f に拡張
6. **reset_policy**: `returns_to_neutral` (頷き終わりに 0° 復帰)
7. **forbidden_patterns**: `wrong motion` (順序逆転) / `too subtle` (zoom が見えない)

### Scene B → `sad_tilt_blur`

1. **emotion**: `sadness`
2. **既存ラベル fit**: `sad_droop` は Y droop 主軸、本シーンは持続的傾き + 視覚 blur で異なる
3. **novel goal_id**: `sad_tilt_blur`
4. **intensity**: `medium` (sustained quality)
5. **duration_frames**: sadness medium 120f (sustained に合致)
6. **reset_policy**: `hold` (傾きと blur が clip 終端まで残る、neutral に戻らない)
7. **forbidden_patterns**: `wrong motion` / `too busy` (blur が強すぎ) / `looks like nod` (Rotation 一過性に見える)

## Phase A.5: preset 拡張 (architecture 制約への対応)

CLI は `DEFAULT_RECIPE_PRESETS` に登録された goal_id しか受け付けない。S-5 が出力した novel goal_id 用に [`src/pipeline/motion_recipe.py`](../../src/pipeline/motion_recipe.py) に 2 entry を追加:

```python
"realization_nod": {
    "motion_goal": "Realization beat: brief zoom-in spike followed by a slow nod.",
    "emotion": "agreement",
    "intensity": "medium",
    "duration_frames": 90,
    "reset_policy": "returns_to_neutral",
    "forbidden_patterns": ["wrong motion", "too subtle"],
    "rotation_values": [0.0, 0.0, -10.0, 0.0],     # 4 keyframes: 前半 0, 後半に nod
    "zoom_delta_values": [0.0, 4.2, 0.0, 0.0],     # 第 2 keyframe で +4.2 (108 相当の zoom spike)
    "effect_names": ["CenterPointEffect"],
    "effect_candidates": ["CenterPointEffect", "ZoomEffect", "RepeatMoveEffect"],
},
"sad_tilt_blur": {
    "motion_goal": "Sustained sad tilt with screen blur for despondent stillness.",
    "emotion": "sadness",
    "intensity": "medium",
    "duration_frames": 120,
    "reset_policy": "hold",
    "forbidden_patterns": ["wrong motion", "too busy", "looks like nod"],
    "rotation_values": [0.0, -12.0, -12.0],
    "effect_names": ["CenterPointEffect", "GaussianBlurEffect"],
    "effect_candidates": ["CenterPointEffect", "GaussianBlurEffect", "OpacityEffect"],
},
```

数値の根拠:

- `realization_nod` Rotation `[0, 0, -10, 0]`: AnimationType `直線移動` + 4 keyframes 等間隔で 30/30/30 frame に分割 → 0-30f 静止、30-60f で 0→-10° に nod 開始、60-90f で 0° に戻る
- `realization_nod` Zoom delta `[0, 4.2, 0, 0]`: base 103.8 + delta 4.2 = 108.0 (zoom 4% spike)。第 1 keyframe peak で「気づき」を表現
- `sad_tilt_blur` Rotation `[0, -12, -12]`: 3 keyframes、0→-12° で傾き、-12 のまま hold (3 つ目が同値で sustain)
- `sad_tilt_blur` `GaussianBlurEffect`: motion_library から Blur=5 (defocus 値) が引かれる

## Phase B+C+D: build-motion-recipes 実行

### Brief

`samples/recipe_briefs/g26_motion_recipe_brief.slice3_proof.json` を新規作成。`recipes` 配列に 2 entry。

### コマンド

```powershell
uv run python -m src.cli.main build-motion-recipes \
  --brief samples/recipe_briefs/g26_motion_recipe_brief.slice3_proof.json \
  --out-ymmp _tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof.ymmp \
  --out-readback _tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof_readback.json \
  --out-manifest _tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof_manifest.md \
  --corpus-ymmp "" \
  --format json
```

### 出力

```
_tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof.ymmp
_tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof_readback.json
_tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof_manifest.md
```

## Machine readback

| frame | length | recipe | Rotation | Zoom | effects |
|------:|------:|--------|---------|------|---------|
| 0 | 90 | `realization_nod` | [0, 0, -10, 0] | [103.8, 108.0, 103.8, 103.8] | `CenterPointEffect` |
| 180 | 120 | `sad_tilt_blur` | [0, -12, -12] | [103.8] | `CenterPointEffect` + `GaussianBlurEffect` |

- canvas: `True` (`is_ymmp_project_canvas` pass)
- `Timelines[].LayerSettings.Items` shape OK
- total items: 6 (2 GroupItem L9 + 4 ImageItem L10/L11)
- recipe GroupItems: 2
- POSIX asset paths: 0
- blank asset paths: 0
- warnings: (なし)
- success: True

## 既存 tests に regression なし

```
$ uv run pytest tests/test_motion_recipe.py -q
... [100%]
3 passed
```

`DEFAULT_RECIPE_ORDER` を変更していないため、v1 brief は依然 12 recipe を出力する。`DEFAULT_RECIPE_PRESETS` の追加は append-only。

## アーキテクチャ findings

### 制約: novel goal_id = preset 拡張必須

S-5 prompt は LLM に novel goal_id を生成する自由度を与えていたが、`build-motion-recipes` の `_resolve_brief_recipes()` は `DEFAULT_RECIPE_PRESETS` lookup が必須で、未登録 goal_id は `MOTION_RECIPE_UNKNOWN_GOAL` で reject される。

これは pipeline の運用設計と CLI 実装の食い違いだったため、本 slice で:

1. S-5 prompt に「novel goal_id を提案する場合は preset 拡張ブロックも出力する」段を追加
2. PIPELINE doc に **Phase A.5** として preset 拡張手順を明記
3. Slice 4 候補として「`_resolve_brief_recipes` を拡張して brief 内完全定義を許可」を記録

### library promotion の経路

Phase E (visual acceptance) で pass した recipe は:

- `MOTION_PRESET_LIBRARY_SPEC § 3` のラベル表に append
- `tachie_motion_map_library.json` に corresponding effect chain を追加
- `FEATURE_REGISTRY.md` G-26 の contract status 更新

`realization_nod` / `sad_tilt_blur` は visual acceptance 待ちのため `proposed` 状態。

## 残作業 (Phase E pending)

- YMM4 で `_tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice3_proof.ymmp` を開く
- Frame 0 の `realization_nod`: zoom spike → nod の順序が読めるか、duration 90f が長すぎないか
- Frame 180 の `sad_tilt_blur`: 12° tilt + blur が「しょんぼり静止」として読めるか、blur が強すぎないか
- 8 区分のいずれかで分類報告

`pass` 判定なら Phase E (library promotion) へ。`adjust` 系なら preset 値を変えて再ビルド。`reject` なら brief を見直す。

## Slice 3 が証明したこと

1. 自然言語シーン → S-5 prompt 判定 → brief entry → preset 拡張 → CLI build → YMM4 review artifact の 5-phase pipeline が **end-to-end で動作する**
2. 既存 v1 brief への regression なし (3 tests pass)
3. Anti-Shortcut Rules を破らない: catalog inspection (effect_names は effect_catalog 内のもののみ) / brief 経由 / preset 拡張は documented value-based / 「感覚」ではなく LOOP_TIMING reference に依拠
4. 現行アーキテクチャの制約（novel goal_id = code 変更）を doc に明文化、Slice 4 で refactor 候補として記録
