# コア本開発レーン Prompt パック（A〜E 並行運用）

> 目的: コア本開発レーンを主軸に、A〜E レーンの入力を受け入れゲートで裁き、PASS 入力のみ次期ドラフトへ反映する。
> 本書は「今すぐ投げられる短文 Prompt」を固定する運用正本。

---

## 1. 参照ファイル（ファイルN 固定）

- ファイル1: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)
- ファイル2: [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)
- ファイル3: [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)
- ファイル4: [../OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)
- ファイル5: [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md)
- ファイル6: [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md)
- ファイル7: [VISUAL-QUALITY-PACKETS.md](VISUAL-QUALITY-PACKETS.md)
- ファイル8: [CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md)（**コア T0〜T3 のタスク設計・並行の組み合わせ**）
- ファイル9: **本ファイル**（`CORE-LANE-PARALLEL-PROMPT-PACK.md`）— 運用原則・§3.0 早見・サイクル手順の正本
- **ファイル10**: [CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md) — **コピペ用 Prompt 全文ブロック・検収チェックリスト・返却テンプレ**の正本（依頼時はここを開いてフェンスごとにコピーする）

---

## 2. 運用原則（コア本開発）

1. 受け入れ判定は常にファイル2を正本にする。
2. 差し戻しは条件のみ返し、未承認の実装要求は受け取らない。
3. ファイル3は PASS 入力のみ反映する（NEEDS_FIX は反映禁止）。
4. FEATURE_REGISTRY 未承認の新規 ID は実装しない。必要時は提案行のみ起票する。
5. 実行 Prompt の前面タスクには `hold` / `quarantined` / `rejected` を出さない（候補棚に隔離）。

---

## 3. 即実行 Prompt（レーン別）

**コピペ用の全文**（フェンス単位でエージェントに渡すブロック）は **ファイル10** に集約した。本節の **Prompt-A〜E / Core-*** の引用は早見・索引として残すが、**二重メンテを避けるため追記・改稿はファイル10 を先に更新**し、必要なら本節の短文を追随する。

### 3.0 早見（コピー用・最短）

| やりたいこと | 貼り付け |
|--------------|----------|
| コア：プラン承認まで | 「**ファイル8**のフェーズ **T0** に従い、**ファイル3**をユーザー承認できる状態に整えてください。**ファイル2**で PASS とならない入力はドラフトに反映せず差し戻し条件のみ返してください。」 |
| コア：文書・サンプル先行 | 「**ファイル8**のフェーズ **T1** に従い進めてください。未承認 FEATURE 実装は禁止。」 |
| コア：スライス 1 本実装 | 「**ファイル8**のフェーズ **T2** に従い、**CORE-DEV-POST-APPROVAL-SLICES** §1 の承認済みスライスを **1 本だけ**実装し、フル pytest を緑にしてください。」 |
| コア：handoff 同期 | 「**ファイル8**のフェーズ **T3** に従い、`runtime-state.md` / `project-context.md` を更新してください。」 |
| 並行 A | 「**ファイル4**の**レーンA**を進めてください。」（下記 **Prompt-A** が詳細） |
| 並行 B | 「**ファイル5**の**レーンB**を進めてください。」（**Prompt-B**） |
| 並行 C | 「**ファイル6**の**レーンC**を進めてください。」（**Prompt-C**） |
| 並行 画質パケット | 「**ファイル7**の **A1〜A4 / B1〜B4** から 1 パケット選び実施してください。」（**Prompt-C-Visual-Quality**） |
| 並行 D | 「**ファイル4**の**レーンD**を進めてください。」（**Prompt-D**） |
| 並行 E | 「**ファイル4**の**レーンE**を進めてください。」（**Prompt-E**） |
| 並行 視覚最低限（本編1案件） | **ファイル10** の **Prompt-V** を丸ごとコピー |
| 並行 改行ギャップ計測 | **ファイル10** の **Prompt-R** を丸ごとコピー |

### Prompt-A（Phase 1 実行）

「ファイル4のレーンAを進めてください。完了条件はB-11形式で取込前/後と4区分を埋め、P01に接続判定を1行追記すること。コア提出時はファイル2の受け入れ条件に自己照合した結果を添えてください。」

### Prompt-B（GUI LLM 同期）

「ファイル5のレーンBを進めてください。B-2/B-3/B-4/B-5を実施し、どのGPT構成（1体/2体）を採用したか、repo正本との差分有無を報告してください。コア提出はファイル2のPrompt同期条件に合わせてください。」

### Prompt-C（視覚三スタイル準備）

「ファイル6のレーンCを進めてください。_local運用方針を守り、validate-ir/apply-productionの機械確認結果を提出してください。YMM4実作業は案件単位で分離し、コアには機械確認ログのみ渡してください。」

### Prompt-C-Visual-Quality（bg_anim / overlay）

「ファイル7のA1〜A4/B1〜B4を使って、対象演出を1パケットずつ実施してください。スコア＋チェックリストをJSONで提出し、PASS/NEEDS_FIXを明示してください。」

### Prompt-D（H-01 brief 運用）

「ファイル4のレーンDを進めてください。動画1本につきbriefを1ファイル作成し、C-07入力より先に適用した記録を提出してください。提出時はファイル2の受け入れ観点で不足がないか確認してください。」

### Prompt-E（サムネ S-8）

「ファイル4のレーンEを進めてください。S-8の1枚を完了し、テンプレ複製・差し替え・書き出しの実施証跡を提出してください。コアには成果物の運用記録のみ渡し、未承認機能要求は含めないでください。」

### Prompt-Core（本開発幹・フル）

「**ファイル8**の §2（フェーズ T0〜T3）を把握したうえで、**ファイル1**→**ファイル2**→**ファイル3**の順でコア本開発レーンを進めてください。A〜E 入力は受け入れ判定し、PASS のみファイル3へ反映、差し戻しは条件のみ返却してください。未承認 FEATURE は増やさず、回帰・文書整合・承認済み修正に限定してください。並行が効くタイミングは **ファイル8** §3 に従ってください。」

### Prompt-Core-T0（プラン承認前・ドラフト整備）

「**ファイル8** フェーズ **T0**。**ファイル3** をユーザー承認可能な形に整備し、**ファイル2** に照らして NEEDS_FIX のオペレータ入力はドラフトに書き込まないでください。承認後のスライス起票は **CORE-DEV-POST-APPROVAL-SLICES** に従ってください。」

### Prompt-Core-T1（文書・サンプル先行）

「**ファイル8** フェーズ **T1**。**ファイル3** §2 の方針に沿い、verification・サンプル JSON・runbook/GUI 文言を優先してください。コード変更は承認済みスライスまたは明確なバグ修正に限定し、FEATURE_REGISTRY 未承認の実装は禁止。」

### Prompt-Core-T2（承認スライス 1 本実装）

「**ファイル8** フェーズ **T2**。**CORE-DEV-POST-APPROVAL-SLICES** §1 から **1 スライスだけ**選び実装し、`NLMYTGEN_PYTEST_FULL=1 uv run pytest` を緑にしてください。」

### Prompt-Core-T3（runtime / handoff）

「**ファイル8** フェーズ **T3**。**runtime-state.md** の最終検証・**project-context.md** HANDOFF を更新し、次セッションの `next_action` を一文で残してください。」

---

## 4. 1サイクルの進め方

1. コアは **ファイル8** §2 で現在のフェーズ（T0〜T3）を決め、**Prompt-Core-T0** から順に使うか、**Prompt-Core（フル）**でまとめて進める。
2. T0 完了後、並行は **ファイル8** §3 に従う（T1 ではレーン C + ファイル7 が相性良い）。
3. オペレータは **§3.0 早見**の「ファイル4のレーンA」形式でエージェントに投げる。
4. コアは **ファイル2** で PASS / NEEDS_FIX を判定する。
5. PASS 入力のみ **ファイル3** へ反映し、ユーザー承認依頼を出す。
6. 承認後 [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 にスライスを起票し **Prompt-Core-T2** で実装する。

---

## 5. 境界ガード（違反防止）

- P2/S6 は条件未充足なら OPEN 維持。コードスライス起票を禁止する。
- F-01/F-02 は quarantined を維持し、再審査ゲートなしで復活させない。
- 「新規機能先行」ではなく「受け入れ条件を満たした入力のみ採用」を厳守する。
- NotebookLM API（A-03, hold）などの保留項目は、**定期バッチ型 Prompt の主タスク**に含めない（日付・週 cadence で主副を切り替えない）。

---

## 6. 変更履歴

- 2026-04-11: **ファイル10**（コピペ全文・検収ハブ）を追加。§3 冒頭に集約方針、§3.0 に Prompt-V / Prompt-R 早見を追加。ファイル9の説明を「早見・原則」に限定。
- 2026-04-10: **ファイル8・ファイル9** を追加。§3.0 早見、Prompt-Core 分割（T0〜T3）、サイクル手順を **CORE-DEV-TASK-DESIGN-NEXT-CYCLE** と整合。
- 2026-04-09: 初版（コア本開発レーン中心の Prompt パックを正本化）。
