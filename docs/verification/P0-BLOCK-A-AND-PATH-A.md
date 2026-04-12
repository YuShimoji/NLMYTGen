# P0 Block-A と経路 A — タスク再設計クローズ（2026-04-12）

本ファイルは、[P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) の **Block-A** と [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) の **経路 A / 経路 B** の関係を、**運用で迷わない一文**に固定する。途中まで残っていた「P0＝必ず診断→C-09→CSV」という読みを正す。

---

## 1. 違和感の原因（なぜ CSV 手前で止まりやすかったか）

- `docs/runtime-state.md` の優先表「P0」行が、歴史的に **B-18 → C-09 → build-csv** の並びで書かれており、**NotebookLM 準拠の台本**でも「まず台本改善（C-09）」が必須に見える。
- 一方、Block-A の狭義は最初から **YMM4 S-4 での CSV 読込エラーなし**までに限定されている（黒背景・実字幕一致は含めない）。
- 台本が **ほぼ NLM 出力のまま**なら、**台本内容の改善を見ること自体が P0 の目的ではない**。その状態で C-09 を挟むと、ゲートと作業内容がすれ違う。

---

## 2. 再設計の結論（正本）

| 概念 | 定義 |
|------|------|
| **Block-A（必須）** | [P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) §2 のとおり。対象 CSV は §1「本番で読む CSV」（既定: `samples/v14_t3_ymm4.csv`）。**読込エラーなし**まで。話者割当は YMM4 UI で可（[P01](P01-phase1-operator-e2e-proof.md) の `lane_a_phase1_2026-04-09_a` と同型）。 |
| **機械前置き（repo）** | 案件に応じて **経路 A** または **経路 B** の手前処理。いずれも最終的に `validate` / `build-csv` が **exit 0** で CSV が生成されること。 |
| **経路 A** | `validate` → `build-csv` → YMM4。**C-09 は必須ではない**（[P01 §経路 A のみ](P01-phase1-operator-e2e-proof.md)、[S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md) 冒頭）。`diagnose-script` は任意（参照用）。 |
| **経路 B** | B-18 →（C-09 constrained rewrite）→ `validate` / `build-csv`。P01 表の **v5〜v14 連鎖**は主に **字幕・overflow コーパス検証**の記録。**全案件の標準 P0 手順ではない**。 |
| **本編 P0 縦の run_id** | 機械＋舵取り記録: `p0_mainline_v14_steering_2026-04-11_a`。再設計・機械再確認の追記: `p0_block_a_task_redesign_2026-04-12_a`（[P01](P01-phase1-operator-e2e-proof.md) 表）。 |

**実務ルール**: NotebookLM に近い台本で「読みやすさ改善」をしない方針なら、**経路 A で機械前置きを完走**し、その CSV で **Block-A（S-4）** に進む。C-09 に時間を使う必要はない。

---

## 3. 既定ブロック（本編 v14 アンカー）のコマンド例

リポジトリ root。台本は `samples/v14_timing_label_split_refined.txt`、出力 CSV は `samples/v14_t3_ymm4.csv`（[P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) §1）。

**PowerShell**（`^` は不要）:

```powershell
uv run python -m src.cli.main diagnose-script "samples/v14_timing_label_split_refined.txt" `
  --speaker-map "ホストA=れいむ,ホストB=まりさ" --format json `
  | Set-Content -Encoding utf8 "samples/p0_steering_v14_diag.json"

uv run python -m src.cli.main validate "samples/v14_timing_label_split_refined.txt" `
  | Set-Content -Encoding utf8 "samples/p0_steering_v14_validate.txt"

uv run python -m src.cli.main build-csv "samples/v14_timing_label_split_refined.txt" `
  -o "samples/v14_t3_ymm4.csv" `
  --speaker-map "ホストA=れいむ,ホストB=まりさ" `
  --max-lines 2 --chars-per-line 40 --reflow-v2 --stats `
  2>&1 | Set-Content -Encoding utf8 "samples/p0_steering_v14_build.txt"
```

- **経路 A だけ**のときは、上記のうち **`validate` と `build-csv` が必須**。`diagnose-script` は省略可。
- `diagnose-script` を回す場合、`diagnostics` が空（warning 0 件）であることは v14 アンカーでは既知の合格ライン。

---

## 4. YMM4 S-4（オペレータ）— Block-A 完了の書き方

1. [WORKFLOW.md](../WORKFLOW.md) の S-4（台本読込）に従い、§1 の CSV を読み込む。
2. 読込ダイアログで話者を `れいむ` / `まりさ` に割り当て（テンプレに合わせて調整）。
3. **読込エラーが出ず**、台本タイムラインが生成できれば **Block-A 通過**。
4. [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) 表の行 **`p0_mainline_v14_steering_2026-04-11_a`** の「接続判定」を **`PASS（YMM4 S-4）`** に更新する（メモに ymmp 識別子・短い所見を足してよい）。

**別台本・別 CSV** で Block-A を取った場合は、[P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) §1 に従い **P01 表に別 run_id 行**を切るか、既存行の対象パスを一貫して更新する。

---

## 5. 参照（短い導線）

| 用途 | 正本 |
|------|------|
| Phase 1 手順の全体 | [P01-phase1-operator-e2e-proof.md](P01-phase1-operator-e2e-proof.md) |
| P0 縦・ブロック表 | [P0-VERTICAL-STEERING-2026-04-11.md](P0-VERTICAL-STEERING-2026-04-11.md) |
| C-09 を使わない条件 | [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md) 冒頭 |
| いまの針・次アクション | [runtime-state.md](../runtime-state.md) |

---

## 6. 機械再確認ログ（本リポ・2026-04-12）

- `samples/p0_steering_v14_2026-04-12_diag.json` — `diagnostics`: 空（warning 0 件）
- `samples/p0_steering_v14_2026-04-12_validate.txt` — `OK: 163 utterances parsed`
- `samples/p0_steering_v14_2026-04-12_build.txt` — `samples/v14_t3_ymm4.csv`（365 rows）、`[WARN]` 16 行（v14 既報の overflow 候補と一致）

YMM4 実機は本環境では実行しない。**Block-A の最終 PASS はオペレータが S-4 で記録**する。
