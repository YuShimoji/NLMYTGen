# レーン C（§3 再現PV風）準備実行記録

> 指示系統: `File5` レーンC次区切り（§3 再現PV風）  
> 根拠: [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) §3、[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック C。  
> 実施日: 2026-04-09

---

## Run

- run_id: `lane_c_s3_2026-04-09_a`
- 対象: §3 再現PV風（`mood` + YMM4 ネイティブ）
- 判定: `partial`（repo 内の測定・検証は完了、YMM4 実機でのテンプレ最終固定は未完）

---

## 1. §3 前提の境界確認

- `mood` / `transition` / `motion` / `bg_anim` は語彙として IR に載るが、最終的な見た目品質は YMM4 テンプレ側の責務が大きい。  
  参照: [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)
- 再現PV風の「早いカット感・エフェクト」は、§3 の方針どおり YMM4 アイテムテンプレに寄せる。
- `measure-timeline-routes` と契約 JSON で、経路の実在可否を先に固定する方針を採用。

---

## 2. タイムライン経路測定（1サイクル）

実行コマンド:

```powershell
uv run python -m src.cli.main measure-timeline-routes "samples/test_verify_4_bg.ymmp" `
  --expect "samples/timeline_route_contract.json" `
  --profile motion_bg_anim_effects
```

観測結果:

- exit code: **0**
- 主要 route:
  - `motion`: `TachieItem.VideoEffects`
  - `bg_anim`: `ImageItem.X/Y/Zoom`, `ImageItem.VideoEffects`
  - `transition`: `VoiceItem.*Fade*`, `TachieItem.Fade*`, `ImageItem.Fade*`
- warning 切り分け:
  - 既知: `TIMELINE_ROUTE_OPTIONAL_MISS`（`template` optional route の未観測）
  - 新規: なし

補足: optional miss は契約上の警告であり、required route は満たしているため本サイクルでは許容。

---

## 3. dry-run 検証

### 3.1 `validate-ir`

```powershell
uv run python -m src.cli.main validate-ir samples/ir_visual_styles_dry_sample.json `
  --palette samples/palette.ymmp `
  --overlay-map _local/lane_c/overlay_map.json
```

- 結果: exit code **0**（`Validation PASSED with 1 warnings`）
- 既知 warning: `FACE_LATENT_GAP`
- 新規 warning: なし

### 3.2 `apply-production --dry-run`

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

- 結果: exit code **0**
- 観測:
  - `Overlay changes: 2`
  - `SE insertions: 1`
  - `Timeline adapter: motion=0, transition=1, bg_anim=0`
- 既知 warning: `FACE_SERIOUS_SKEW`, `IDLE_FACE_MISSING`
- 新規 warning: なし

---

## 4. §3 チェック進捗

| §3 チェック項目 | 状態 | メモ |
|-----------------|------|------|
| 早いカット感・エフェクトを YMM4 テンプレへバンドル | 未完（実機作業） | repo では方針確認まで |
| `mood`/`transition`/`motion`/`bg_anim` の自動化境界を理解して運用 | 完了 | 境界を本記録に固定 |
| `measure-timeline-routes` で契約整合確認 | 完了 | 1サイクル実行済み |
| SE 必要時の参照系（G-18）を確認 | 完了 | `apply-production --dry-run` 経路で再確認 |

---

## 5. 未完と次アクション

1. YMM4 実機で再現PVテンプレ（`mood` 系）を最終固定し、テンプレ名を local note に反映。  
2. 実案件 ymmp でも `measure-timeline-routes --expect ...` を1回実行し、案件固有差分を観測。  
3. §3 完了ラン（`prep-pass`）を追記してクローズする。

---

## 6. 関連ログ

- レーン C 集約: [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md)
- §2 前run: [LANE-C-s2-skit-completion-2026-04-09.md](LANE-C-s2-skit-completion-2026-04-09.md)
- G-12 正本: [G12-timeline-route-measurement.md](G12-timeline-route-measurement.md)
