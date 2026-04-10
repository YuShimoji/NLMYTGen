# A〜E 移譲後 — コア開発ドキュメント索引

オペレータが [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) の **A〜E** を担当し、リポジトリ側は **回帰・承認ゲート・PR** に集中するときの正本一覧。


| 順   | ドキュメント                                                                                   | 用途                                                      |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1   | [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)   | 並行レーン数・コア幹の原則                                           |
| 2   | [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)                   | レーンA〜Eとコア幹の即実行 Prompt 集                                 |
| 3   | [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)             | B-11 / P01 / プロンプト / P2・S6 の受け入れ・差し戻し                   |
| 4   | [P2-READY-INPUT-TEMPLATE.md](P2-READY-INPUT-TEMPLATE.md)                                 | 分岐Cの READY 入力フォーマット（YMM4 見え方 / S6 §2 5条件）               |
| 5   | [P2-CONDITION45-PRECHECK-TEMPLATE.md](P2-CONDITION45-PRECHECK-TEMPLATE.md)               | 分岐Cで条件4/5を先行入力するテンプレ（YMM4 未確認時の OPEN 継続運用）                |
| 6   | [CORE-DEV-LANE-PROMPT-QUICKREF.md](CORE-DEV-LANE-PROMPT-QUICKREF.md)                     | 「File N のレーンX」を即指示できるクイックプロンプト集                        |
| 7   | [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) | Gate 取り込み後の次期実装ドラフト（承認前。OPEN/READY 判定はチェックリスト正本）                |
| 8   | [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md)                     | 承認済みスライス表・実装チェックリスト（`master` 起点・フル回帰）                   |
| 9   | [CORE-DEV-MASTER-PR-RUNBOOK.md](CORE-DEV-MASTER-PR-RUNBOOK.md)                           | 大型統合 PR の手順（**PR #1 はマージ済み**。今後は `master` 起点のトピックブランチ用） |
| 10  | [CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md)                 | コア本開発 **T0〜T3** のタスク設計・並行レーンの相性（Prompt パック **ファイル8**）        |


関連: [B11-pre-plan-execution-pack-2026-04-07.md](B11-pre-plan-execution-pack-2026-04-07.md)、[runtime-state.md](../runtime-state.md)。

---

## 変更履歴

- 2026-04-10: `P2-CONDITION45-PRECHECK-TEMPLATE.md` と `CORE-DEV-LANE-PROMPT-QUICKREF.md` を追加し、File N 参照の導線を拡張。
- 2026-04-10: 分岐C向け `P2-READY-INPUT-TEMPLATE.md` を追加し、索引順を更新。
- 2026-04-10: `CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md`（ファイル8）を索引に追加。
- 2026-04-09: コア復帰プラン反映。P2/S6 判定の更新は [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md) を正本として追従。
- 2026-04-09: `CORE-LANE-PARALLEL-PROMPT-PACK.md` を索引に追加。
- 2026-04-09: 初版。