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

---

## 2. 運用原則（コア本開発）

1. 受け入れ判定は常にファイル2を正本にする。
2. 差し戻しは条件のみ返し、未承認の実装要求は受け取らない。
3. ファイル3は PASS 入力のみ反映する（NEEDS_FIX は反映禁止）。
4. FEATURE_REGISTRY 未承認の新規 ID は実装しない。必要時は提案行のみ起票する。
5. 実行 Prompt の前面タスクには `hold` / `quarantined` / `rejected` を出さない（候補棚に隔離）。

---

## 3. 即実行 Prompt（レーン別）

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

### Prompt-Core（本開発幹）

「ファイル1→2→3の順でコア本開発レーンを進めてください。A〜E入力を受け入れ判定し、PASSのみ次期ドラフトへ反映、差し戻しは条件のみ返却してください。未承認FEATUREは増やさず、回帰・文書整合・承認済み修正に限定してください。」

---

## 4. 1サイクルの進め方

1. コアが Prompt-Core で提出待ち状態を宣言する。
2. A/B/C を先行実行し、D/E は案件状況で追随する。
3. コアはファイル2で PASS / NEEDS_FIX を判定する。
4. PASS 入力のみファイル3へ反映し、承認依頼を作成する。
5. ユーザー承認後に [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) へ移す。

---

## 5. 境界ガード（違反防止）

- P2/S6 は条件未充足なら OPEN 維持。コードスライス起票を禁止する。
- F-01/F-02 は quarantined を維持し、再審査ゲートなしで復活させない。
- 「新規機能先行」ではなく「受け入れ条件を満たした入力のみ採用」を厳守する。
- NotebookLM API（A-03, hold）などの保留項目は、日次/週次 Prompt の主タスクに含めない。

---

## 6. 変更履歴

- 2026-04-09: 初版（コア本開発レーン中心の Prompt パックを正本化）。
