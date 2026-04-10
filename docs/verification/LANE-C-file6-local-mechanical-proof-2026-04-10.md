# LANE-C File6 Prompt-C 機械確認提出（_local 運用） — 2026-04-10

> 指示: 「ファイル6のレーンCを進めてください。_local運用方針を守り、validate-ir/apply-productionの機械確認結果を提出してください。YMM4実作業は案件単位で分離し、コアには機械確認ログのみ渡してください。」
>  
> 境界根拠: [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md) §4 / §7 / §10

---

## 1. _local 運用確認

- 使用 overlay map: `_local/lane_c/overlay_map.json`
- `_local/` は `.gitignore` 除外対象であり、案件固有パスをコア正本に混在させない。
- 初回実行で `OVERLAY_UNKNOWN_LABEL: arrow_red` を検知し、**案件ローカル定義のみ**を補完して再実行。
  - 追記キー: `overlays.arrow_red`
  - コア側コード・契約ファイル（`docs/` / `src/` / `samples` 正本）は変更なし。

---

## 2. validate-ir（機械確認）

実行コマンド:

```powershell
uv run python -m src.cli.main validate-ir samples/p2_overlay_se_ir.json `
  --palette samples/palette.ymmp `
  --overlay-map _local/lane_c/overlay_map.json
```

- exit code: **0**
- 判定: `Validation PASSED with 3 warnings`
- 主な出力:
  - `Overlay Distribution`: `arrow_red=1`, `speech_bubble=1`
  - warning: `FACE_SERIOUS_SKEW`, `FACE_LATENT_GAP`, `IDLE_FACE_MISSING`（既知許容）
- ログ: `samples/lane_c_file6_validate_p2_2026-04-10.txt`

---

## 3. apply-production --dry-run（機械確認）

実行コマンド:

```powershell
uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json `
  --face-map samples/face_map.json `
  --bg-map samples/bg_map_proof.json `
  --overlay-map _local/lane_c/overlay_map.json `
  --se-map samples/p2_se_map.json `
  --timeline-profile production_ai_monitoring_lane `
  --timeline-contract samples/timeline_route_contract.json `
  --dry-run
```

- exit code: **0**
- 主な集計:
  - `Face changes: 2`
  - `Overlay changes: 2`
  - `SE insertions: 1`
  - `Timeline adapter: motion=0, transition=1, bg_anim=0`
  - `BG anim writes: 0`
  - `Transition VoiceItem writes: 1`
- ログ: `samples/lane_c_file6_apply_dryrun_2026-04-10.txt`

---

## 4. YMM4 実作業の分離（コア渡し境界）

- 本提出は **CLI 機械確認ログのみ**をコアへ渡す。
- YMM4 上の見た目確認・素材差し替え・テンプレ実体調整は、案件単位で [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) を使って別運用する。
- したがって、コア側には案件固有アセットパスや目視結果を混在させない。
