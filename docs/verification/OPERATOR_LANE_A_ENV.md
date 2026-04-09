# レーン A 用 — このリポジトリの実行環境メモ

[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) のトラック A を **このマシン**で実行するときの固定値。runbook に別ユーザーの `cd` 例が出る場合は、**常に下記 root に読み替える**。

## リポジトリ root（PowerShell）

```powershell
Set-Location "C:\Users\PLANNER007\NLMYTGen"
```

## 検証済みコマンド（2026-04-09）

以下は `C:\Users\PLANNER007\NLMYTGen` で **exit 0** を確認済み。

- `uv run python -m src.cli.main diagnose-script "samples/AI監視が追い詰める生身の労働.txt" --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" --format json`
- `uv run python -m src.cli.main build-csv "samples/AI監視が追い詰める生身の労働.txt" -o "samples/AI監視が追い詰める生身の労働_B11_ymm4.csv" --speaker-map "スピーカー1=れいむ,スピーカー2=まりさ" --max-lines 2 --chars-per-line 40 --reflow-v2 --stats --format json`

## デフォルトの対象台本・Speaker Map（サンプル案件）

| 項目 | 値 |
|------|-----|
| 台本 | `samples/AI監視が追い詰める生身の労働.txt` |
| Speaker Map | `スピーカー1=れいむ,スピーカー2=まりさ` |
| 診断 JSON の控え（例） | `_tmp_script_diag.json`（P01 手順どおり） |
| refined 稿（例） | `refined.txt`（C-09 後） |

実案件に切り替えるときは上表を差し替え、YMM4 キャラ名と CSV の話者列が一致することを確認する（[WORKFLOW.md](../WORKFLOW.md) S-4）。

## 関連

- レーン A 準備チェックリスト全体: [LANE_A_PREP_CHECKLIST.md](LANE_A_PREP_CHECKLIST.md)
- B-11 実測記録（同一サンプル）: [B11-workflow-proof-ai-monitoring-labor.md](B11-workflow-proof-ai-monitoring-labor.md)
