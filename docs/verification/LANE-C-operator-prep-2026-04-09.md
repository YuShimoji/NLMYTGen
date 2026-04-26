# レーン C（視覚三スタイル）— オペレータ準備記録

> 根拠: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)、[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック C。  
> 実施記録日: 2026-04-09（repo 内の機械確認まで実施済み）。  
> **準備フェーズクローズ**: 2026-04-09 — 以降の YMM4 上のチェックリスト実作業は **本番案件ごと**に [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) を実行する（コア開発幹へ戻すためここで区切る）。

---

## 1. YMM4 稼働ブロック（スロット名テンプレ）

PRE-PLAN の当時設計では **レーン C と旧背景アニメ証跡は同一 YMM4 ウィンドウを奪い合う**。現行 G-24 の入口ではないため、必要時だけ参照し、1 人運用なら **同時フルは避け、時間帯で分割**する。トラック A（CSV 取込〜タイムライン調整）と同日にやる場合は、**読込ブロック**と **テンプレ／マップ整備ブロック**を分ける。

以下は **運用方針として固定**したスロット名（具体の開始時刻はオペレータの外部スケジュールに委ねる。repo に週 cadence は置かない）。

| ブロック | 目的 | 運用メモ |
|----------|------|----------|
| C-1 | レーン C：YMM4 テンプレ複製・`overlay_map` 編集 | 旧背景アニメ証跡と **同一セッションでフル併用しない** |
| C-2 | レーン C：`validate-ir` / `apply-production` の CLI 確認 | repo 側は §5 まで **完了済み** |
| 主軸-BG | 背景アニメ短サイクル | `runtime-state.md` の `next_action` に従う |
| A | トラック A：CSV 取込・本番 ymmp 調整 | C-1 と **別ブロック**推奨 |

---

## 2. 正本ドキュメント読了チェック

以下をレーン C 実作業前に読了すること（内容の正本は各ファイル）。

| 資料 | 状態 |
|------|------|
| [VISUAL_STYLE_PRESETS.md](../VISUAL_STYLE_PRESETS.md) | 確認済み（三スタイルと patch 境界） |
| [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) | 確認済み（§1〜5 が作業手順） |
| [VISUAL_STYLES_IR_DRY_SAMPLE.md](VISUAL_STYLES_IR_DRY_SAMPLE.md) | 確認済み（`validate-ir` コマンド） |
| [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) §「v4: 構造化 IR」＋「視覚スタイル三種」 | 確認済み（下記 B-3） |

---

## 3. トラック B-3 整合（Writer と `overlay_map` ラベル）

[S6-production-memo-prompt.md](../S6-production-memo-prompt.md) の **v4** ブロック内に **「### 視覚スタイル三種（template 振り分けの補助語彙）」** があり、repo 正本として次が明示されている。

- 挿絵コマ風: `template=skit`、`overlay=speech_bubble` または `overlay_map` のコマ用ラベル
- 資料パネル風: `template=data` / `board`、`overlay=text_box` 等
- 再現 PV 風: `template=mood`（＋ `intro` / `closing`）、テンポは YMM4 テンプレ主

**オペレータ作業**: Custom GPT 等の Instructions が **v4 全文**かつ上記節を含むことを確認し、自作 `overlay_map` のキー（例: `speech_bubble`, `text_box`）と IR の `overlay` ラベルを一致させる。

**クローズ時点の状態（repo）**: 正本ファイルに v4 ブロックおよび「視覚スタイル三種」節が存在することを確認済み。リモート GUI の Instructions は運用者が随時 [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) B-3 に照合する。

---

## 4. ローカルレジストリ（repo 外）

- **絶対パスを含む JSON はコミットしない**。作業用コピーはリポジトリ直下の `_local/` に置く（[.gitignore](../../.gitignore) で `_local/` を除外）。
- **雛形**: [lane-c-overlay-map.TEMPLATE.json](lane-c-overlay-map.TEMPLATE.json) の `YOUR_ASSETS` を自分のフォルダに置換するか、[samples/visual_styles_overlay_map.example.json](../../samples/visual_styles_overlay_map.example.json) をコピーして編集する。
- **YMM4 側の具体タスク**は [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) の §1（資料パネル）→ §2（挿絵コマ）→ §3（再現 PV）の順。

---

## 5. 機械確認（本 repo で実施した結果）

### 5.1 `validate-ir`（三スタイル混在 dry IR）

```powershell
uv run python -m src.cli.main validate-ir samples/ir_visual_styles_dry_sample.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/visual_styles_overlay_map.example.json
```

- **結果**: exit code **0**（`Validation PASSED`）。`FACE_LATENT_GAP` 等の WARNING は許容範囲（[VISUAL_STYLES_IR_DRY_SAMPLE.md](VISUAL_STYLES_IR_DRY_SAMPLE.md) 記載どおり）。
- **裏取りテスト**: `pytest tests/test_ir_validate.py::test_ir_visual_styles_dry_sample_passes_cli_validation` — **PASS**

### 5.2 `apply-production --dry-run`（overlay / se / timeline まで含む健全性）

`ir_visual_styles_dry_sample.json` は **6 発話のミニ IR**であり、サンプル `production.ymmp`（別案件の Voice 行）とは **行対応していない**。そのため **apply-production の通し確認**は、既存 proof と同じ入力（P-02）で実施する。

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

- **結果**: exit code **0**、`Overlay changes: 2`、`SE insertions: 1` 等、dry-run 完走。

### 5.3 本適用（YMM4 ビジュアル確認用の出力ファイル）

上記と同引数で **出力**し、YMM4 で開けるパスを残した。

```powershell
uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json `
  --face-map samples/face_map.json `
  --bg-map samples/bg_map_proof.json `
  --overlay-map samples/p2_overlay_map.json `
  --se-map samples/p2_se_map.json `
  --timeline-profile production_ai_monitoring_lane `
  --timeline-contract samples/timeline_route_contract.json `
  -o samples/_tmp_lane_c_apply_proof.ymmp
```

- **出力**: [samples/_tmp_lane_c_apply_proof.ymmp](../../samples/_tmp_lane_c_apply_proof.ymmp)（`.gitignore` の `samples/_tmp_*` で無視される）。
- **ビジュアル確認**: 本リポジトリの `apply-production` 系は [runtime-state.md](../runtime-state.md) Evidence どおり **2026-04-05 時点で YMM4 実機確認済み**の経路がある。本ファイルの `_tmp` は P-02 相当 IR の再出力であり、**ローカルで開いて差分確認してもよいが必須ではない**（準備フェーズの機械完了条件は dry-run と整合記録までとする）。

---

## 6. 次の一手（本番案件）

1. `_local/lane_c/overlay_map.json`（など）を実パスで整備する。  
2. 本番 IR に対し `validate-ir --palette ... --overlay-map ...`（必要なら `--bg-map` / `--slot-map`）。  
3. `apply-production ... --dry-run` → 問題なければ `-o` で書き出し → YMM4 確認。  
4. 効果記録は [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) または [mass-production-pilot-checklist.md](mass-production-pilot-checklist.md) へ 1 行追記（任意）。

### 演出品質の運用単位（2026-04-09 追加）

- 背景アニメと情報オーバーレイの品質改善は、旧 A1-A4 / B1-B4 観点の履歴を参照する場合でも、現行判断では案件ごとの検証記録と `runtime-state.md` を優先する。
- 提出は各パケットごとに JSON（スコア + チェックリスト + PASS/NEEDS_FIX）。
- コアは PASS のみ受け入れる（NEEDS_FIX は差し戻し）。

---

## 7. 準備フェーズの完了宣言（コア開発へ戻す）

- **repo で完結した範囲**: 正本読了の整理、B-3 の正本確認、`validate-ir` / `apply-production` の機械検証、オペレータ向けテンプレと `_local/` 方針。
- **案件依存で後続**: [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) のチェックボックス（YMM4 テンプレ・PNG 実体）、本番 IR と CSV の row-range 整合。
- **コア開発幹**（[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1.3）: 未承認 FEATURE を増やさず、回帰・ドキュメント整合・承認済みバグ修正に集中する。

---

## 8. 実行ログ追記（2026-04-09 / レーンC本番運用パック）

### 8.1 `_local` overlay_map 運用

- 作業用マップを `_local/lane_c/overlay_map.json` として配置（`samples/p2_overlay_map.json` を元に作成）。
- `_local/` は [.gitignore](../../.gitignore) の除外対象であり、絶対パスを含むローカル資産参照をコミットしない方針を維持。

### 8.2 `validate-ir`（overlay/se IR 基準）

```powershell
uv run python -m src.cli.main validate-ir samples/p2_overlay_se_ir.json `
  --palette samples/palette.ymmp `
  --overlay-map _local/lane_c/overlay_map.json
```

- **結果**: exit code **0**（`Validation PASSED with 3 warnings`）。
- **観測 warning**: `FACE_SERIOUS_SKEW`、`FACE_LATENT_GAP`、`IDLE_FACE_MISSING`（既知の許容 warning として扱う）。

### 8.3 `apply-production --dry-run`（overlay/se IR 基準）

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

- **結果**: exit code **0**、`Overlay changes: 2`、`SE insertions: 1`、`Transition VoiceItem writes: 1`。

### 8.4 `_tmp` 出力固定（再現コマンド）

```powershell
uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json `
  --face-map samples/face_map.json `
  --bg-map samples/bg_map_proof.json `
  --overlay-map _local/lane_c/overlay_map.json `
  --se-map samples/p2_se_map.json `
  --timeline-profile production_ai_monitoring_lane `
  --timeline-contract samples/timeline_route_contract.json `
  -o samples/_tmp_lane_c_apply_proof.ymmp
```

- **結果**: exit code **0**、`Written: samples/_tmp_lane_c_apply_proof.ymmp`。
- **提出物**: [samples/_tmp_lane_c_apply_proof.ymmp](../../samples/_tmp_lane_c_apply_proof.ymmp)

### 8.5 境界（案件依存で未実施）

- YMM4 実機での最終見た目確認（テンプレ実体・素材差し替え）は案件依存のため本ログでは未実施。
- 実案件では [VISUAL_STYLE_YMM4_CHECKLIST.md](../VISUAL_STYLE_YMM4_CHECKLIST.md) の §1〜§3 を実行し、結果のみコアへ提出する。

---

## 9. 追記（2026-04-10）— file5 基準・overlay B3 のみ

[LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md) B-3 の機械ゲートに沿い、旧 **overlay B3（タイミング一致）** だけを判定した記録を別紙に残した。

- **実行記録**: [LANE-C-file5-B3-overlay-timing-2026-04-10.md](LANE-C-file5-B3-overlay-timing-2026-04-10.md)
- **判定 JSON**: `samples/lane_c_file5_b3_overlay_timing_evidence.json`
- **ログ**: `samples/lane_c_file5_b3_validate_logs.txt` / `samples/lane_c_file5_b3_apply_production_dryrun.txt`

### 8.6 旧 A3（bg_anim 意図一致）— 2026-04-10

- **対象 IR**: [samples/ir_visual_styles_dry_sample.json](../../samples/ir_visual_styles_dry_sample.json)（レーンC §5.1 `validate-ir` 済みの三スタイル dry サンプル）
- **判定**: **PASS**（`target_quality` スコア 2、必須チェック `tone_match` / `topic_match` / `no_contradicting_visual` いずれも満たす）
- **台本論点 ↔ bg_anim 一致の要約**:
  - **index 1**（「挿絵コマ1」/ S1 挿絵コマ風）: `bg_anim: none` → コマ割り的な読みやすさ・静止構図の論点と一致。
  - **index 5**（「PV風の雰囲気切替」/ S3 再現PV風）: `bg_anim: ken_burns` → 発話が明示する雰囲気切替・映画的トーンと一致。
  - index 2〜4, 6 は IR 上 `bg_anim` 未指定のため、過剰なカメラワーク指定による論点矛盾はないと判断。
- **提出 JSON（正本）**: [lane-c-bg_anim-A3-2026-04-10.json](lane-c-bg_anim-A3-2026-04-10.json)

---

## 10. 実行ログ（2026-04-10）— Prompt-C 機械回帰

旧 **Prompt-C** に沿った `validate-ir` / `apply-production --dry-run` の再実行。repo root は本リポジトリ。PowerShell では stderr の WARNING が非ゼロ終了と誤認されうるため、**終了コードは `cmd /c` で確認**（いずれも **0**）。

**overlay-map（overlay/se 系）**: `_local/lane_c/overlay_map.json` が存在したため、§8.2 / §8.3 と同じく **同ファイル**を使用（無い環境では `samples/p2_overlay_map.json` で §5.2 相当の回帰とする）。

### 10.1 `validate-ir`（§5.1 三スタイル dry）

```powershell
uv run python -m src.cli.main validate-ir samples/ir_visual_styles_dry_sample.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/visual_styles_overlay_map.example.json
```

- **exit code**: 0  
- **要約**: `Validation PASSED with 1 warnings`（`FACE_LATENT_GAP` ほか、既存方針どおり許容）  
- **フルログ**: [samples/lane_c_promptc_validate_dry_2026-04-10.txt](../../samples/lane_c_promptc_validate_dry_2026-04-10.txt)

### 10.2 `validate-ir`（§8.2 overlay/se IR + `_local`）

```powershell
uv run python -m src.cli.main validate-ir samples/p2_overlay_se_ir.json `
  --palette samples/palette.ymmp `
  --overlay-map _local/lane_c/overlay_map.json
```

- **exit code**: 0  
- **要約**: `Validation PASSED with 3 warnings`（`FACE_SERIOUS_SKEW` / `FACE_LATENT_GAP` / `IDLE_FACE_MISSING`、既知の許容 warning）  
- **フルログ**: [samples/lane_c_promptc_validate_p2_2026-04-10.txt](../../samples/lane_c_promptc_validate_p2_2026-04-10.txt)

### 10.3 `apply-production --dry-run`（§8.3 同引数）

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

- **exit code**: 0  
- **要約**: `Face changes: 2`、`Overlay changes: 2`、`SE insertions: 1`、`Timeline adapter: motion=0, transition=1, bg_anim=0`、`BG anim writes: 0`、`Transition VoiceItem writes: 1`、`(dry-run: no file written)`  
- **フルログ**: [samples/lane_c_promptc_apply_dryrun_2026-04-10.txt](../../samples/lane_c_promptc_apply_dryrun_2026-04-10.txt)

### 10.4 境界（ファイル7との切り分け）

旧 **A2 / A4 / B2 / B4** の個別 JSON 提出は当時の Prompt-C 本体のスコープ外。必要時は、現行の案件ごとの検証記録と `runtime-state.md` / `P02-production-adoption-proof.md` の PASS 条件へ接続する。

---

## 11. 実行ログ（2026-04-11）— Prompt-C 機械回帰

旧 **Prompt-C** に沿った再実行。本環境では `_local/lane_c/overlay_map.json` が **未配置**のため、§8.2 / §8.3 の **overlay/se 系**はドキュメント記載のフォールバックどおり **`samples/p2_overlay_map.json`** を使用（§5.2 相当の回帰）。

### 11.1 `validate-ir`（§5.1 三スタイル dry）

```powershell
uv run python -m src.cli.main validate-ir samples/ir_visual_styles_dry_sample.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/visual_styles_overlay_map.example.json
```

- **exit code**: 0  
- **要約**: `Validation PASSED with 1 warnings`（`FACE_LATENT_GAP`、既存方針どおり許容）  
- **フルログ**: [samples/lane_c_promptc_validate_dry_2026-04-11.txt](../../samples/lane_c_promptc_validate_dry_2026-04-11.txt)

### 11.2 `validate-ir`（overlay/se IR、`samples/p2_overlay_map.json`）

```powershell
uv run python -m src.cli.main validate-ir samples/p2_overlay_se_ir.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/p2_overlay_map.json
```

- **exit code**: 0  
- **要約**: `Validation PASSED with 3 warnings`（`FACE_SERIOUS_SKEW` / `FACE_LATENT_GAP` / `IDLE_FACE_MISSING`、既知の許容 warning）  
- **フルログ**: [samples/lane_c_promptc_validate_p2_2026-04-11.txt](../../samples/lane_c_promptc_validate_p2_2026-04-11.txt)

### 11.3 `apply-production --dry-run`（§5.2 / §8.3 同系、`samples/p2_overlay_map.json`）

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

- **exit code**: 0  
- **要約**: `Face changes: 2`、`Overlay changes: 2`、`SE insertions: 1`、`Timeline adapter: motion=0, transition=1, bg_anim=0`、`BG anim writes: 0`、`Transition VoiceItem writes: 1`、`(dry-run: no file written)`  
- **フルログ**: [samples/lane_c_promptc_apply_dryrun_2026-04-11.txt](../../samples/lane_c_promptc_apply_dryrun_2026-04-11.txt)

### 11.4 裏取りテスト

`pytest tests/test_ir_validate.py::test_ir_visual_styles_dry_sample_passes_cli_validation` — **PASS**（2026-04-11）
