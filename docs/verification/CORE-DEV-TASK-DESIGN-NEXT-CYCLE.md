# コア本開発 — 今後タスク設計（次サイクル正本）

**役割**: コア本開発レーンを主軸にした「次に何をするか」を固定する。並行レーン A〜E は **価値が出るときだけ** 同時進行させる。  
**Prompt の正本索引**: [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（ファイル番号・早見・原則）。**全文コピペ・検収**は [CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)（ファイル10）。  
**ドラフト承認の正本**: [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)（§2〜§3 はユーザー承認までコードに反映しない）。  
**受け入れの正本**: [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)。

---

## 1. 前提（変えない）

- 未承認の FEATURE は [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) に `proposed` のみ起票し、**実装しない**。
- オペレータ入力は **PASS のみ** [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) に反映する。
- 実装は [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 の **承認済みスライス 1 本ずつ**。
- 検証の最低ライン: `NLMYTGEN_PYTEST_FULL=1 uv run pytest` が緑。

---

## 2. コア本開発フェーズ（順序固定・主軸）

| フェーズ | 目的 | 主な成果物 | 完了条件 |
|----------|------|------------|----------|
| **T0** | 次期方針の確定 | ファイル3（ドラフト）の承認、§1 表への「承認日・差し替え」記録 | ユーザーが §2〜§3 を承認または差し替え明示。NEEDS_FIX 入力はドラフトに書かない |
| **T1** | Gate B 寄りの **文書・サンプル先行** | verification 手順、IR/JSON サンプル、runbook/GUI 文言の明確化（[ファイル3](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) §2 整合） | コード変更が無いか、あっても既存承認スライス・バグ修正の範囲。フル pytest 緑 |
| **T2** | **承認済みスライス**の縦実装 | §1 に起票した 1 スライス = 1 PR/コミット単位の実装 | FEATURE_REGISTRY 遷移遵守、`POST-APPROVAL` チェックリスト完了 |
| **T3** | 同期・再アンカー | `runtime-state.md` / `project-context.md` HANDOFF / 最終検証日付 | 次サイクルの `next_action` が一文で分かる |

**推奨サイクル**: T0 →（並行でレーン A・C・7 が走りうる）→ T1 → T2（スライス数だけ繰り返し）→ T3 → 再度 T0。

---

## 3. 並行開発を「効果が出る」組み合わせ

| いつ | 並行レーン | 理由 |
|------|------------|------|
| T0 中 | 通常不要 | 方針未確定のまま入力を増やさない |
| T1 中 | **ファイル6 レーンC** + **ファイル7（A1〜B4）** | 演出パケットの PASS 証跡がファイル3 §5・ファイル2 へそのまま流せる |
| T1〜T2 | **ファイル4 レーンA（P0）** | 台本→CSV の実測がコアの Gate 判断と独立して価値を生む |
| プロンプト変更直後 | **ファイル5 レーンB** | IR/refinement の drift を止める |
| 案件単位 | **ファイル4 レーンD・E** | brief / サムネは本編と同じタイミングで効く |

---

## 4. コア用コピー Prompt（ファイル番号のみ指定）

> 詳細な前文は [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md) §3 を正とする。全文ブロックは **ファイル10**。

| ID | 貼り付け一文 |
|----|----------------|
| **Core-T0** | 「**ファイル8**のフェーズ **T0** に従い、**ファイル3**をユーザー承認できる状態に整えてください。**ファイル2**で PASS とならないオペレータ入力はドラフトに反映せず、差し戻し条件だけ返してください。」 |
| **Core-T1** | 「**ファイル8**のフェーズ **T1** に従い、verification・サンプル・runbook 中心で進めてください。未承認 FEATURE の実装は禁止。**ファイル2**に照らし不足があればファイル3へは書かないでください。」 |
| **Core-T2** | 「**ファイル8**のフェーズ **T2** に従い、**CORE-DEV-POST-APPROVAL-SLICES** §1 の **承認済みスライスを 1 本だけ**実装し、`NLMYTGEN_PYTEST_FULL=1 uv run pytest` を緑にしてください。」 |
| **Core-T3** | 「**ファイル8**のフェーズ **T3** に従い、`runtime-state.md` と `project-context.md` の HANDOFF を更新し、次セッションの `next_action` を一文で残してください。」 |
| **Core-Full** | 「**ファイル8**→**ファイル1**→**ファイル2**→**ファイル3**の順で読み、**ファイル10** の **Prompt-Core（フル）** を実行すること。**ファイル9** §2 の運用原則に従うこと。」 |

※ **ファイル9** = [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（運用原則・§3.0 早見・サイクル手順）。**ファイル10** = [CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)（**コピペ用の全文 Prompt フェンス・検収・返却テンプレ**の正本）。

§4 の表は **早見（一文）** 用である。**エージェントへ渡す全文**はファイル10からフェンスごとにコピーする。

---

## 5. オペレータ並行用コピー Prompt（早見）

| レーン | 貼り付け一文 |
|--------|----------------|
| **A** | 「**ファイル4**の**レーンA**を進めてください。」（詳細は同パック **Prompt-A**） |
| **B** | 「**ファイル5**の**レーンB**を進めてください。」（**Prompt-B**） |
| **C** | 「**ファイル6**の**レーンC**を進めてください。」（**Prompt-C**） |
| **C-画質** | 「**ファイル7**の **A1〜A4 / B1〜B4** の該当パケットを 1 つ選び実施してください。」（**Prompt-C-Visual-Quality**） |
| **D** | 「**ファイル4**の**レーンD**を進めてください。」（**Prompt-D**） |
| **E** | 「**ファイル4**の**レーンE**を進めてください。」（**Prompt-E**） |
| **V**（視覚最低限） | 「**ファイル10** の **Prompt-V** を丸ごとコピーして実行。」 |
| **R**（改行ギャップ） | 「**ファイル10** の **Prompt-R** を丸ごとコピーして実行。」 |

---

## 6. 次サイクルでコアが最初に読む順序（短縮）

1. [runtime-state.md](../runtime-state.md)（現在位置・`next_action`）  
2. **本ファイル** §2（今どの T か）  
3. [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)  
4. [CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md](CORE-PARALLEL-PROMPTS-AND-ACCEPTANCE-HUB-2026-04.md)（全文 Prompt・検収）→ 必要なら [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（原則・早見表）

---

## 7. 変更履歴

- 2026-04-12: オペレータ **P0 Block-A** と [P01](P01-phase1-operator-e2e-proof.md) **経路 A** の対応を [P0-BLOCK-A-AND-PATH-A.md](P0-BLOCK-A-AND-PATH-A.md) に正本化（`runtime-state.md` の P0 行と整合）。並行レーン表（§3）の趣旨は不変。
- 2026-04-11: **ファイル10**（コピペ全文・検収ハブ）を索引に追加。§4 Core-Full をファイル10準拠に更新。§6 の読み順にファイル10を挿入。
- 2026-04-10: 初版。コア T0〜T3 と並行レーンの組み合わせ、コピー Prompt 早見を正本化。
