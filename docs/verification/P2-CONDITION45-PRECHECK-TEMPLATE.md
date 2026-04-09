# P2 条件4/5 先行入力テンプレ（YMM4 未確認時）

目的: `YMM4見え方` 実測前に、S6 §2 の条件4/5を先に埋めて `OPEN` のまま前進する。

参照:

- [S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md) §2
- [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) §2.3

---

## 1. 条件4（PoC 合格条件の機械判定可能）ログ

### 1.1 実行コマンド（どちらか 1 本以上）

```powershell
uv run python -m src.cli.main apply-production samples/production.ymmp samples/p2_overlay_se_ir.json --palette samples/palette.ymmp --csv samples/reflow.csv --dry-run
```

```powershell
uv run python -m src.cli.main measure-timeline-routes samples/production.ymmp --expect --profile production_ai_monitoring_lane
```

### 1.2 記録欄

- 実行日時:
- 実行コマンド:
- exit code:
- 判定:
  - PASS（機械判定ログとして使用可）
  - FAIL（failure class を記録し、OPEN 継続）
- ログ保存先（verification ファイル or コマンド出力抜粋リンク）:
- failure class（あれば）:

実績（2026-04-09）:

- 実行日時: 2026-04-09
- 実行コマンド: `uv run python -m src.cli.main measure-timeline-routes samples/production.ymmp --expect samples/timeline_route_contract.json --profile production_ai_monitoring_lane`
- exit code: `0`
- 判定: PASS（機械判定ログとして使用可）
- ログ保存先（verification ファイル or コマンド出力抜粋リンク）: 本ファイル `P2-CONDITION45-PRECHECK-TEMPLATE.md`（条件4ログ実績）
- failure class（あれば）: なし

実績（2026-04-10）:

- 実行日時: 2026-04-10
- 実行コマンド: `uv run python -m src.cli.main measure-timeline-routes samples/production.ymmp --expect samples/timeline_route_contract.json --profile production_ai_monitoring_lane`
- exit code: `0`
- 判定: PASS（機械判定ログとして使用可）
- ログ保存先（verification ファイル or コマンド出力抜粋リンク）: 本ファイル `P2-CONDITION45-PRECHECK-TEMPLATE.md`（条件4ログ実績）
- failure class（あれば）: なし

---

## 2. 条件5（既存運用接続点）記録

### 2.1 接続点（1 行）

- 接続点: `CSV -> YMM4 -> apply-production` のうち、今回の投入位置を 1 行で記入
- 接続点: CSV 生成後の `production.ymmp` に `apply-production` を適用し、YMM4 で見え方確認へ接続

記入例:

- 接続点: CSV 生成後の `production.ymmp` に `apply-production` を適用し、YMM4 見え方確認へ接続

### 2.2 根拠リンク

- [OPERATOR_WORKFLOW.md](../OPERATOR_WORKFLOW.md)
- [S6-background-animation-next-step-plan-prep.md](../S6-background-animation-next-step-plan-prep.md)

---

## 3. P2/S6 行への反映（暫定2行）

以下 2 行を [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) の P2/S6 行へ反映する。

```text
- YMM4見え方: NG - 未実施（環境制約: 端末でYMM4リソース非共有）
- S6§2(5条件): 充足 - 条件4/5の根拠は `P2-CONDITION45-PRECHECK-TEMPLATE.md`、OPEN理由はYMM4実測待ちのみ
```

備考:

- 条件4/5をこのファイルで満たした状態を正本化し、`P2-READY-INPUT-TEMPLATE.md` §6 と同じ判定根拠を使う。

---

## 4. 次アクション

- YMM4 可能端末で実測後、1 行目を `OK|NG` 実測値へ更新
- `OK + 5条件充足` のときのみ READY 判定

