# G-26 Motion Recipe Pipeline Slice 4 — Brief-supplied Recipe Architecture

## 結論

Slice 3 で発見した **「novel goal_id を提案するには motion_recipe.py のコード変更が必要」** という制約 (Phase A.5 preset 拡張) を解消した。`_resolve_brief_recipes` を拡張し、`DEFAULT_RECIPE_PRESETS` 未登録の goal_id でも brief entry が必須キー + route + effect を含めば end-to-end で build 可能になった。

これにより S-5 motion brief prompt が出力する novel goal entry は、エンジニアが motion_recipe.py を編集することなく直接 CLI で消費できる。Phase A.5 は「再利用見込みの goal を library promotion 時に preset 化する」という選択工程に格下げ、必須工程ではなくなった。

## 変更内容

### `src/pipeline/motion_recipe.py`

`_resolve_brief_recipes` の preset lookup 後の分岐を拡張:

```python
preset = DEFAULT_RECIPE_PRESETS.get(goal_id)
if preset is None:
    # Novel goal_id: brief entry must self-define all required fields
    if not isinstance(raw_recipe, dict):
        raise ValueError(f"MOTION_RECIPE_UNKNOWN_GOAL: {goal_id}")
    recipe = {"goal_id": goal_id, **overrides}
else:
    recipe = {"goal_id": goal_id, **copy.deepcopy(preset), **overrides}
required_keys = (
    "motion_goal", "emotion", "intensity",
    "duration_frames", "reset_policy", "forbidden_patterns",
)
if preset is None:
    required_keys = required_keys + ("effect_candidates",)
for required_key in required_keys:
    if required_key not in recipe:
        raise ValueError(f"MOTION_RECIPE_FIELD_REQUIRED: {goal_id}.{required_key}")
```

設計判断:

- 文字列 entry (`goal_id` のみ) は依然 preset 必須 (string では route 値を持てないため)。dict entry のみ novel 受け入れ
- novel goal は `effect_candidates` を必須化 (空だと `_build_recipe_items` が `MOTION_RECIPE_EFFECT_SHORTLIST_EMPTY` で raise するため、上流で明確化)
- preset がある場合の動作は不変 (既存 brief は影響を受けない)

### `tests/test_motion_recipe.py`

2 件追加:

1. `test_brief_supplied_recipe_without_preset` — novel goal_id を brief 完全定義で build。route 値が期待通り反映されることを assert
2. `test_brief_unknown_goal_without_required_fields_raises` — 必須キー欠でも明確に `MOTION_RECIPE_FIELD_REQUIRED` を raise する

合計 5 tests passing。既存 3 件に regression なし。

## End-to-End 実証 (slice4_proof brief)

### Brief

`samples/recipe_briefs/g26_motion_recipe_brief.slice4_proof.json` に 2 novel goal を完全定義:

| goal_id | emotion | intensity | duration | route 構成 | preset 拡張 |
|---------|---------|-----------|---------:|-----------|:----------:|
| `excited_double_jump` | happiness | strong | 90f | `y_delta_values: [0, -45, 5, -35, 0]` (2-bounce with mid-rest) | **無し** |
| `thinking_circle_pause` | thinking | light | 80f | `rotation_values: [0, -5, -5, -5, 0]` + `zoom_delta_values: [0, 1.5, 1.5, 1.5, 0]` | **無し** |

`motion_recipe.py` を一切編集していない。両 goal ともコード上には存在しない。

### コマンド

```powershell
uv run python -m src.cli.main build-motion-recipes \
  --brief samples/recipe_briefs/g26_motion_recipe_brief.slice4_proof.json \
  --out-ymmp _tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice4_proof.ymmp \
  --out-readback _tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice4_proof_readback.json \
  --out-manifest _tmp/g26/recipe_pipeline/g26_motion_recipe_review_slice4_proof_manifest.md \
  --corpus-ymmp "" \
  --format json
```

### Machine readback

| frame | length | recipe | Rotation | Y (resolved) | Zoom (resolved) | effects |
|------:|------:|--------|---------|-------------|-----------------|---------|
| 0 | 90 | `excited_double_jump` | static (0) | [462.5, **417.5**, **467.5**, **427.5**, 462.5] | static (103.8) | CenterPointEffect |
| 180 | 80 | `thinking_circle_pause` | [0, **-5**, **-5**, **-5**, 0] | static (462.5) | [103.8, **105.3**, **105.3**, **105.3**, 103.8] | CenterPointEffect |

- canvas: True (`is_ymmp_project_canvas` pass)
- recipe_count: 2
- POSIX asset paths: 0
- blank asset paths: 0
- success: True
- warnings: なし

Y delta が base 462.5 に正しく加算されている (excited_double_jump)。Rotation hold + Zoom hold の同時適用 (thinking_circle_pause) も期待通り。

## アーキテクチャ上の意味

### 解消した制約

| 項目 | Slice 3 まで | Slice 4 以降 |
|------|------------|--------------|
| novel goal_id の試作 | `DEFAULT_RECIPE_PRESETS` に preset 追加が必要 (コード変更 + commit) | brief 内完全定義で OK (data-only) |
| 試作サイクル | brief 編集 + code 編集 + test 実行 + 2 commit | brief 編集のみ + 1 commit |
| S-5 prompt と CLI の接続 | preset 拡張ブロック生成が必要 | brief entry 1 つで完結 |
| library promotion (Phase E) | コード経由 (preset 化) が前提 | 選択工程 (再利用見込みの goal のみ preset 化) |

### Phase 構造の変化

```
旧:  A → A.5 (preset 拡張、必須) → B+C+D → E
新:  A → B+C+D → E (→ promotion: preset 化は選択)
```

### S-5 prompt の出力形式変更

novel goal の場合の出力は brief entry 1 つ (route + effect 含む)。preset 拡張ブロックの並列出力は廃止。

### `MOTION_PRODUCTION_PIPELINE.md` の Phase A 節を「経路 1 / 経路 2」二段構造で書き換え

経路 1 = brief 内完全定義 (推奨、必須コード変更なし)
経路 2 = preset 化 (再利用見込みの goal のみ、library promotion 工程で実施)

## 残作業 (Phase E)

### Visual acceptance 待ちの review .ymmp (現在の累積)

| brief | recipes | machine status | visual status |
|-------|--------:|----------------|---------------|
| `g26_motion_recipe_brief.v1.json` (12 preset) | 12 | pass | not recorded |
| `g26_motion_recipe_brief.slice3_proof.json` (2 preset) | 2 | pass | not recorded |
| `g26_motion_recipe_brief.slice4_proof.json` (0 preset、brief 完全定義) | 2 | pass | not recorded |

合計 16 recipe が visual acceptance pending。8 区分のいずれかでユーザーが分類することで Phase E が動き出す。

### Library promotion 候補

経路 1 で acceptance pass した novel goal のうち、複数案件で再利用見込みのもの (例: `excited_double_jump` が happiness 系の標準として定着しそう、など) を `DEFAULT_RECIPE_PRESETS` に preset 化する。これは visual acceptance 後の判断。

## Slice 4 が証明したこと

1. brief-supplied recipe アーキテクチャが end-to-end で動作する (canvas pass / route 値正確 / asset paths 健全)
2. 既存 v1 brief / Slice 3 brief は regression なし (5 tests passing、preset 経路は不変)
3. novel goal_id 試作のフリクションが「コード変更 + commit」から「brief 編集のみ」に縮小
4. S-5 prompt と CLI の接続切れ (Slice 3 で発見した制約) が構造的に解消
5. Phase E が「acceptance → 必要なら preset 化」のシンプルなループに整理された
