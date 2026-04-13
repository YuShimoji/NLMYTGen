# G-19: face_map bundle (multi-body) — 実装記録

**ステータス**: done (2026-04-13)
**コミット**: `0b71142` (実装本体), `4cc665c` (validate-ir), `e4b6d49` (GUI)
**テスト**: 328 pass (`NLMYTGEN_PYTEST_FULL=1 uv run pytest`)

---

## 概要

1 キャラ = 1 body の制約を緩和し、`body_id` による複数体素材切替を実装。

## 方式

**Option A: ディレクトリ + マニフェスト**

```
samples/face_map_bundle_registry.example.json   ← レジストリ
samples/face_map_bundles/default.json           ← 通常体
samples/face_map_bundles/haitatsuin.json        ← 配達員体
```

レジストリ構造:
```json
{
  "bodies": {
    "default": { "face_map": "face_map_bundles/default.json" },
    "haitatsuin": { "face_map": "face_map_bundles/haitatsuin.json" }
  },
  "characters": {
    "ゆっくり魔理沙黄縁": { "default_body": "default" }
  }
}
```

## 変更ファイル

| ファイル | 変更 |
|---------|------|
| `src/pipeline/ymmp_patch.py` | `_select_face_map_for_body` ヘルパー、carry-forward に `body_id`、`patch_ymmp` にバンドルパラメータ |
| `src/pipeline/ir_validate.py` | `known_body_ids` パラメータ、`BODY_ID_UNKNOWN` チェック |
| `src/cli/main.py` | `_load_face_map_bundle` ローダー、`--face-map-bundle` CLI フラグ (patch-ymmp / apply-production / validate-ir) |
| `gui/index.html` | 演出適用タブに「Face Map Bundle (G-19)」ファイル選択 |
| `gui/renderer.js` | filePaths / fileFilters / opts / settings に faceMapBundle 追加 |
| `gui/main.js` | apply-production / validate-ir IPC に `--face-map-bundle` 引数 |
| `docs/FEATURE_REGISTRY.md` | G-19: proposed → approved |
| `docs/PRODUCTION_IR_SPEC.md` | `body_id` (Micro) + `default_body_id` (SectionHeader) |
| `docs/PRODUCTION_IR_CAPABILITY_MATRIX.md` | `body_id` 行 |
| `tests/test_face_map_bundle.py` | 15 テスト |

## フォールバックチェーン

`_select_face_map_for_body`:
1. 明示 `body_id` → バンドル内の該当 face_map
2. character の `default_body` → バンドル内の該当 face_map
3. `"default"` キー → バンドル内の該当 face_map
4. すべて失敗 → flat face_map (後方互換)

## 後方互換

- `--face-map-bundle` 未指定時は従来と完全同一動作
- `--face-map` と `--face-map-bundle` は排他

## 制約 (V1)

- `body_id` はシーンレベル (全キャラ共通)。キャラ別は別スライス
- `--palette` 経路は single-body のまま (multi-body は手動で per-body face_map を用意)

## 次のステップ

- [ ] YMM4 で Remark 設定 → `extract-template --labeled` で安定ラベル確認 (オペレータ)
- [ ] 実案件で IR + bundle → `apply-production` → YMM4 目視 (オペレータ)
- [ ] G-20 (幾何) の YMM4 GUI 確認 → 別スライスで承認
