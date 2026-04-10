# T1-P2-DOCSAMPLE — P2 段階投入の機械検証パック（正本）

**スライス**: [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 の **T1-P2-DOCSAMPLE**。  
**目的**: P2 向けに `overlay` / `se` / `bg_anim` / `transition` が **validate-ir** と **apply-production --dry-run** で機械的に通る経路を、**1 本の手順書**に固定する。YMM4 実機は本書のスコープ外（オペレータ案件）。  
**能力対照**: [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md)（語彙と patch 範囲の正本）。  
**FEATURE**: 本スライスは **ドキュメントと既存サンプルのみ**。台帳に新規 FEATURE 行は置かない。

---

## 1. 前提

- リポジトリルートで実行する（`uv` が利用可能であること）。
- Windows PowerShell では **WARNING が stderr に出る**と終了コードの見え方が紛らわしい。確実に確認する場合は次のいずれかを推奨する。
  - `cmd /c "uv run python -m src.cli.main ... 2>&1"` のあと `%ERRORLEVEL%` が `0` であること
  - または PowerShell で `$LASTEXITCODE -eq 0` を確認する

---

## 2. 参照サンプル（repo 固定）

| 役割 | パス |
|------|------|
| P2 最小 IR（overlay + se + macro bg） | [samples/p2_overlay_se_ir.json](../../samples/p2_overlay_se_ir.json) |
| overlay 台帳 | [samples/p2_overlay_map.json](../../samples/p2_overlay_map.json) |
| SE 台帳 | [samples/p2_se_map.json](../../samples/p2_se_map.json) |
| 本番系 ymmp（AI 監視レーン想定） | [samples/production.ymmp](../../samples/production.ymmp) |
| palette / face | [samples/palette.ymmp](../../samples/palette.ymmp)、[samples/face_map.json](../../samples/face_map.json) |
| macro bg | [samples/bg_map_proof.json](../../samples/bg_map_proof.json) |
| タイムライン契約・プロファイル | [samples/timeline_route_contract.json](../../samples/timeline_route_contract.json)、プロファイル名 `production_ai_monitoring_lane` |
| P2 小規模 bg_anim IR | [samples/p2_bg_anim_small_scope.ir.json](../../samples/p2_bg_anim_small_scope.ir.json) |
| 上記用 ymmp / マップ | [samples/test_verify_4_bg_p2_small.ymmp](../../samples/test_verify_4_bg_p2_small.ymmp)、[samples/bg_map_p2_small_scope.json](../../samples/bg_map_p2_small_scope.json)、[samples/transition_map_p2_small_scope.json](../../samples/transition_map_p2_small_scope.json)、[samples/bg_anim_map_p2_small_scope.json](../../samples/bg_anim_map_p2_small_scope.json) |

### 2.1 サンプル JSON の正本優先順（T1 運用固定）

1. 本書 §2 のパスを **T1 の機械検証サンプル正本**とする。  
2. IR 語彙・patch 可能範囲の解釈が必要なときは、必ず [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) を先に参照する。  
3. 追加のローカル検証 JSON（`_local` など）は補助証跡として扱い、T1 の正本参照を上書きしない。

### 2.2 runbook / GUI 導線（T1-RUNBOOK-GUI との対称参照）

- オペレータ向けの実行順・責務分担は [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) のトラック A/B/C を正本にする。  
- GUI 側の C-09 導線・「台本診断 JSON」用語は [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) を正本にする。  
- runbook / GUI の用語一致と導線検証は [T1-RUNBOOK-GUI-terminology-alignment-proof.md](T1-RUNBOOK-GUI-terminology-alignment-proof.md) を参照する。  
- 本書は **P2 機械検証コマンドと期待ログ**のみを扱い、YMM4 実機見え方の判定は [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) を正本として扱う。

---

## 3. トラック A — overlay / se（`production.ymmp` ベース）

### 3.1 `validate-ir`

```powershell
uv run python -m src.cli.main validate-ir samples/p2_overlay_se_ir.json `
  --palette samples/palette.ymmp `
  --overlay-map samples/p2_overlay_map.json `
  --se-map samples/p2_se_map.json
```

**期待（exit code 0）**

- 標準出力に `Validation PASSED` を含む（警告は **許容**: `FACE_SERIOUS_SKEW`、`FACE_LATENT_GAP`、`IDLE_FACE_MISSING` 等。レーン C / チェックリスト正本と同様）。
- `Overlay Distribution` に `speech_bubble` と `arrow_red` が現れる。
- `SE Distribution` に `click` が現れる。

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

**期待（exit code 0）**

- `Face changes:` / `Overlay changes:` / `SE insertions:` が **いずれも 1 以上**（本サンプルでは `Face changes: 2`、`Overlay changes: 2`、`SE insertions: 1`）。
- `Timeline adapter: motion=0, transition=1, bg_anim=0`（本 ymmp・IR の組合せにおける機械集計）。
- `Transition VoiceItem writes: 1`
- `BG anim writes: 0`（本 IR は `bg_anim` 未指定のためキーフレーム系の bg_anim 書き込みは発生しない）。
- 末尾に `(dry-run: no file written)`。

### 3.3 `measure-timeline-routes`（G-12 契約）

```powershell
uv run python -m src.cli.main measure-timeline-routes samples/production.ymmp `
  --expect samples/timeline_route_contract.json `
  --profile production_ai_monitoring_lane
```

**期待（exit code 0）**

- `--- Contract Check ---` 節が出力され、契約不一致で **非ゼロ終了にならない**。

---

## 4. トラック B — 小規模 `bg_anim`（`test_verify_4_bg_p2_small.ymmp`）

`bg_anim` / `transition` の **G-14 キーフレーム系**とタイムラインアダプタ集計を、小さな IR で機械確認する。

```powershell
uv run python -m src.cli.main apply-production samples/test_verify_4_bg_p2_small.ymmp samples/p2_bg_anim_small_scope.ir.json `
  --bg-map samples/bg_map_p2_small_scope.json `
  --transition-map samples/transition_map_p2_small_scope.json `
  --bg-anim-map samples/bg_anim_map_p2_small_scope.json `
  --dry-run
```

**期待（exit code 0）**

- `BG anim writes:` が **1 以上**（本サンプルでは `3`）。
- `Transition VoiceItem writes:` が **1 以上**（本サンプルでは `4`）。
- `Timeline adapter: motion=0, transition=4, bg_anim=3` のように **adapter 行が出力される**。
- stderr に `Warning: no --palette or --face-map specified` が出る場合があるが、**本トラックは face 非対象の dry-run 確認として許容**（exit code は 0 を維持する）。

---

## 5. 能力マトリクスとの対応（要約）

| IR で触れるフィールド | マトリクス上の patch / validate | 本書での確認箇所 |
|----------------------|-----------------------------------|------------------|
| `overlay` | patch 可 / validate 可 | トラック A 3.1〜3.2 |
| `se` | 条件付き patch / validate 可 | トラック A 3.1〜3.2 |
| `transition`（fade） | patch 可 | トラック A 3.2、トラック B |
| `bg_anim`（キーフレーム等） | patch 可（経路は G-12 契約と整合） | トラック B |

---

## 6. 変更履歴

- 2026-04-10: T1-P2-DOCSAMPLE 用に初版。既存 `samples/p2_*` と LANE-C / LANE-B 実行記録を **単一路線**に集約。
