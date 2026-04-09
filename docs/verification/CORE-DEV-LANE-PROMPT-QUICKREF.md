# 報告レーン本線 — 即実行プロンプト集（File N 参照）

目的: チャットで「ファイルNのレーンXを進めてください」と短く指示できるようにする。

---

## 1. File N 対応表


| File N | 参照先                                                                                      | 主用途                         |
| ------ | ---------------------------------------------------------------------------------------- | --------------------------- |
| File1  | [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)             | P2/S6 観測の正本、OPEN/READY 判定入力 |
| File2  | [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md)                                 | P2 入力 2 行フォーマット             |
| File3  | [P2-CONDITION45-PRECHECK-TEMPLATE.md](P2-CONDITION45-PRECHECK-TEMPLATE.md)               | 条件4/5を先行で埋めるテンプレ            |
| File4  | [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) | 判定条件と先行実行パケット               |
| File5  | [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)                | レーン A〜E 運用手順                |
| File6  | [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md)                     | READY 後の承認済みスライス運用          |


---

## 2. そのまま使える指示文

### 2.1 P2 条件4/5 先行

- 「**File3 のレーンP2先行を進めてください。条件4ログを1本取得し、条件5接続点を1行記入して、File1 に反映してください。**」

### 2.2 P2 暫定入力の更新

- 「**File2 のレーンP2入力を進めてください。環境制約前提の2行を作成し、File1 の P2/S6 行を更新してください。**」

### 2.3 レーンA（Phase1運用）

- 「**File5 のレーンAを進めてください。B-18→C-09→build-csv→YMM4読込まで実施し、必要なら P01 を追記してください。**」

### 2.4 レーンB（GUI LLM同期）

- 「**File5 のレーンBを進めてください。repo正本と Instructions の差分を確認し、同期結果を記録してください。**」

### 2.5 レーンC（視覚スタイル）

- 「**File5 のレーンCを進めてください。YMM4作業の準備チェックを1区切り進め、結果を verification に記録してください。**」

### 2.6 レーンD（H-01 brief）

- 「**File5 のレーンDを進めてください。動画1本分の brief を作成して上位制約として利用してください。**」

### 2.7 レーンE（S-8サムネ）

- 「**File5 のレーンEを進めてください。S-8 の 1 枚ワークフローを実施し、出力とメモを記録してください。**」

### 2.8 YMM4 実測後の再判定

- 「**File4 の再判定を進めてください。YMM4見え方の1行だけ File1 で更新し、READY/OPEN を判定してください。**」

### 2.9 READY 後の承認スライス移行

- 「**File6 の承認後スライスを進めてください。承認記録を反映し、master起点トピックブランチで実装準備を開始してください。**」

---

## 3. 運用ルール（短縮版）

- P2 は `OK + 5条件充足` になるまで OPEN 継続。
- YMM4 未確認でも、条件4/5と暫定2行は先行で埋める。
- READY 判定後も、承認まではコードスライス起票しない。

---

## 4. 変更履歴

- 2026-04-10: 初版。File N 参照でレーンA〜E/P2判定を即指示できるテンプレを追加。

