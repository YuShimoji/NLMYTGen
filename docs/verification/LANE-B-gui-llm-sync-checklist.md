# レーン B — GUI LLM 正本同期チェックリスト

> **目的**: [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) トラック B（B-1〜B-5）を漏れなく実行し、Custom GPT / Claude Project / Gem の Instructions を repo 正本と一致させる。  
> **前提**: [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) のレーン B は **A レーンと独立**（台本 1 本の完了を待たない）。

---

## GPT（または Project / Gem）の分割方針

| 方針 | 内容 |
|------|------|
| **推奨（2 体）** | **体 1**: Phase 1 台本 refinement（C-09）のみ → 正本 [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md)。**体 2**: 演出 IR・素材メモ・サムネ素案（C-07 v4 中心）→ 正本 [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) の v4。runbook の A-2 / B-2 と B-3 が別 GPT でも矛盾しない。 |
| **1 体にまとめる場合** | Instructions を **C-07 v4（S6）** に寄せ、C-09 は **会話のたびに S1 のシステム節＋入力テンプレを先に貼る**など二段運用にする。トークンと取り違えリスクが上がるため非推奨。 |

---

## B-1. セットアップの全体像

- [ ] [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) を通読した（方式 A/B/C のどれを使うか決めた）
- [ ] 上表どおり **GPT 数（1 または 2）**を決めた
- [ ] 各ツールの「Instructions / Project instructions」編集画面を開ける

---

## B-2. S-1 台本 refinement（C-09）

**正本**: [S1-script-refinement-prompt.md](../S1-script-refinement-prompt.md)

- [ ] 「LLM への指示」相当がファイルと **一致**している
- [ ] 入力テンプレ（診断 JSON ＋ 元台本の渡し方）が **一致**している
- [ ] 任意参照の [PACKAGING_ORCHESTRATOR_SPEC.md](../PACKAGING_ORCHESTRATOR_SPEC.md)（H-01 があるときの整合）を運用するなら、S1 先頭の注記どおり扱う

**最小検証**: 診断 JSON ＋ 元台本を 1 ラウンド投入し、**修正済み台本全文のみ**など S1 の出力契約どおりか確認する。

---

## B-3. S-6 演出 IR（C-07 v4 / G-05）

**正本**: [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) の見出し **「### v4 プロンプト本体」**直下のコードフェンス **内の全文**（先頭は `あなたはゆっくり解説動画の演出 IR`、末尾は Part 4 制約まで）。

- [ ] 演出用 GPT の Instructions を **上記フェンス内だけ**で **丸ごと置換**した（v3 断片の混在なし）
- [ ] フェンス内に **「視覚スタイル三種」**節が含まれることを目視確認した
- [ ] 語彙の背景理解用に [VISUAL_STYLE_PRESETS.md](../VISUAL_STYLE_PRESETS.md) を必要なら開いた

**最小検証**: 短い台本で 1 回生成し、repo root で `uv run python -m src.cli.main validate-ir …` / `apply-production … --dry-run`（手順は S6 の「### v4 使い方」および runbook）でエラーがないか確認する。

---

## B-4. H-01 Packaging brief（任意）

**正本**: [PACKAGING_ORCHESTRATOR_SPEC.md](../PACKAGING_ORCHESTRATOR_SPEC.md)

- [ ] 動画 1 本につき brief を 1 ファイルにする運用にした（空テンプレ: [samples/packaging_brief.template.md](../../samples/packaging_brief.template.md)）
- [ ] C-07 入力時は **brief を台本より先に**貼る（runbook B-4）
- [ ] **H-01 連携文の扱いを決めた**: [S6-production-memo-prompt.md](../S6-production-memo-prompt.md) の「### H-01 連携 (推奨)」は v4 フェンス**外**にある。Instructions に **その節を v4 本体の直前に連結して貼る**か、貼らずに **会話のたびに brief を台本より先に貼る**運用で代替する（いずれかでよい）

---

## B-5. サムネコピー（C-08）と v4 Part 4 の使い分け

**C-08 正本**: [S8-thumbnail-copy-prompt.md](../S8-thumbnail-copy-prompt.md)

| 状況 | 推奨 |
|------|------|
| **H-02 準拠**（Specificity Ledger / Brief Compliance 等）が必要 | 別ラウンドで S8 を適用するか、**サムネ専用 GPT**に S8 を載せる。workflow 観点は [H01-packaging-orchestrator-workflow-proof.md](H01-packaging-orchestrator-workflow-proof.md)。 |
| **早い素案のみ**でよい | C-07 v4 の **Part 4（サムネイルコピー）**だけで足りる場合あり。厳密な H-02 チェックは S8 側。 |

- [ ] 上記のどちらで回すか **今回の案件で決めた**
- [ ] S8 を使う場合、Instructions または会話先頭に S8 正本と一致させた

---

## よくあるずれ（再同期時に確認）

- [gui-llm-setup-guide.md](../gui-llm-setup-guide.md) の **レガシー v3 統合ブロック**だけを貼って C-07 を固定していないか → **C-07 の正本は常に S6 v4 プロンプト本体**。

---

## 完了の記録（任意）

同期日とツール名を [project-context.md](../project-context.md) の DECISION LOG に 1 行残す、または本ファイル末尾に日付と署名を追記してよい。
