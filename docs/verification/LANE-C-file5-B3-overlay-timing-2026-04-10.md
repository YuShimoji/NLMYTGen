# レーン C / overlay B3（タイミング一致）— file5 基準 実施記録

**実施日**: 2026-04-10  
**スコープ**: [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) の **B-3**（`validate-ir` / `apply-production --dry-run`）に相当する機械検証 **のみ**に加え、旧 **overlay B3**（発話論点と表示タイミングの同期）の **判定 JSON** を提出。B-1 / B-2 / B-4 / B-5 および bg_anim A 系は未実施。

---

## 1. 対象入力（確定）

| 役割 | パス |
|------|------|
| 発話単位 overlay 割当の根拠 IR | `samples/ir_visual_styles_dry_sample.json` |
| その overlay マップ | `samples/visual_styles_overlay_map.example.json` |
| apply-production 通し確認用 IR | `samples/p2_overlay_se_ir.json` |
| overlay/se マップ | `samples/p2_overlay_map.json` |
| パレット | `samples/palette.ymmp` |
| 本番相当 ymmp | `samples/production.ymmp` |

---

## 2. 実行コマンドと exit code

### 2.1 validate-ir（三スタイル混在 IR）

```powershell
uv run python -m src.cli.main validate-ir samples/ir_visual_styles_dry_sample.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/visual_styles_overlay_map.example.json
```

- **exit code**: `0`（`Validation PASSED with 1 warnings`）

### 2.2 validate-ir（overlay + SE IR）

```powershell
uv run python -m src.cli.main validate-ir samples/p2_overlay_se_ir.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/p2_overlay_map.json
```

- **exit code**: `0`（`Validation PASSED with 3 warnings`）

### 2.3 apply-production --dry-run

```powershell
uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json `
  --face-map samples/face_map.json `
  --bg-map samples/bg_map_proof.json `
  --overlay-map samples/p2_overlay_map.json `
  --se-map samples/p2_se_map.json `
  --timeline-profile production_ai_monitoring_lane `
  --timeline-contract samples/timeline_route_contract.json `
  --dry-run
```

- **exit code**: `0`
- **観測**: `Overlay changes: 2`（`speech_bubble` / `arrow_red` が同一発話の行レンジに対応）

---

## 3. 発話同期（B3）の根拠要約

1. **`ir_visual_styles_dry_sample.json`**: `speech_bubble` は index 1 の台詞「挿絵コマ1」、`text_box` は index 3 の「データ説明」（S2 資料パネル節）に付与。index 2 では overlay なし → IR 仕様上、表示は発話 index に紐づき、次行への持ち越しなし。
2. **`p2_overlay_se_ir.json`**: 単一発話 `index: 1` に `row_start` / `row_end` が `1` で揃い、`overlay` は `speech_bubble` と `arrow_red`。`apply-production --dry-run` で overlay 変更が 2 件計上され、パイプラインが当該発話行にオーバーレイを束ねることを確認。

**境界**: YMM4 タイムライン上のフレーム単位の見た目は案件依存のため、本記録は [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md) §8.5 と同様、**IR + CLI 機械証跡まで**とする。

---

## 4. 提出物（証跡）

| 種別 | パス |
|------|------|
| B3 判定 JSON（PASS） | [samples/lane_c_file5_b3_overlay_timing_evidence.json](../../samples/lane_c_file5_b3_overlay_timing_evidence.json) |
| validate-ir ログ要約 | [samples/lane_c_file5_b3_validate_logs.txt](../../samples/lane_c_file5_b3_validate_logs.txt) |
| apply-production dry-run ログ | [samples/lane_c_file5_b3_apply_production_dryrun.txt](../../samples/lane_c_file5_b3_apply_production_dryrun.txt) |

**判定**: `result: pass`（`scores.target_quality` / `timing_fit` 等および B3 必須チェック 3 項すべて満足 — 詳細は上記 JSON）。

---

## 5. 参照

- file5 正本: [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) §B-3  
- B3 定義: 旧 overlay B3（発話論点と表示タイミングの同期）
- コマンド雛形: [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md) §5 / §8
