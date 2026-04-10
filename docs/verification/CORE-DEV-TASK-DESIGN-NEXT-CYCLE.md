# コア本開発 — 今後タスク設計（次サイクル正本）

**役割**: コア本開発レーンを主軸にした「次に何をするか」を固定する。並行レーン A〜E は **価値が出るときだけ** 同時進行させる。  
**Prompt の正本索引**: [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（ファイル番号とコピー用一文）。  
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

> 全文・分割版は [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md) §3（**Prompt-Core-T0〜T3** 等）。複合・別セッションは同 **§3.1**。

| ID | 貼り付け一文 |
|----|----------------|
| **Core-T0** | 「**ファイル8**のフェーズ **T0** に従い、**ファイル3**をユーザー承認できる状態に整えてください。**ファイル2**で PASS とならないオペレータ入力はドラフトに反映せず、差し戻し条件だけ返してください。」 |
| **Core-T1** | 「**ファイル8**のフェーズ **T1** に従い、verification・サンプル・runbook 中心で進めてください。未承認 FEATURE の実装は禁止。**ファイル2**に照らし不足があればファイル3へは書かないでください。」 |
| **Core-T2** | 「**ファイル8**のフェーズ **T2** に従い、**CORE-DEV-POST-APPROVAL-SLICES** §1 の **承認済みスライスを 1 本だけ**実装し、`NLMYTGEN_PYTEST_FULL=1 uv run pytest` を緑にしてください。」 |
| **Core-T3** | 「**ファイル8**のフェーズ **T3** に従い、`runtime-state.md` と `project-context.md` の HANDOFF を更新し、次セッションの `next_action` を一文で残してください。」 |
| **Core-Full** | 「**ファイル8**→**ファイル1**→**ファイル2**→**ファイル3**の順で読み、**ファイル9**（本パック）の **Prompt-Core** 全文どおりにコア本開発レーンを進めてください。」 |

※ **ファイル9** = [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（パック自体をファイル9として参照する運用。§1 一覧参照）。

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

---

## 6. 次サイクルでコアが最初に読む順序（短縮）

1. [runtime-state.md](../runtime-state.md)（現在位置・`next_action`）  
2. **本ファイル** §2（今どの T か）  
3. [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md)  
4. [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（投げる Prompt を選ぶ）

---

## 7. 今後タスク設計（コア本開発レーン・T1 完了後）

> **前提**: T1（`T1-P2-DOCSAMPLE` / `T1-RUNBOOK-GUI`）は完了済み。`runtime-state.md` の `next_action` は **T2** を指す想定で記載する。

### 7.1 直近タスク（フェーズ T2）

| 順 | やること | 正本・参照 |
|----|----------|------------|
| 1 | [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 を開き、**コード変更を伴う**承認済みスライスを **ちょうど 1 本**選ぶ | §2 チェックリスト、[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) |
| 2 | **該当スライスが無い**（文書のみ・準備メタのみの行だけ等）場合は、ユーザーと合意の上で (a) `proposed`→承認→§1 へ新規行を起票してから T2 に入る、(b) T2 をスキップして T3 のみ実施、(c) 次 **T0**（ファイル3 の改訂・再承認）へ進む、のいずれかを選び、`runtime-state.md` の `next_action` を更新する | [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) §3 テンプレ |
| 3 | 選定したスライスを **縦 1 本**で実装し、`NLMYTGEN_PYTEST_FULL=1 uv run pytest` を緑にする | [P2A-phase2-motion-segmentation-branch-review.md](P2A-phase2-motion-segmentation-branch-review.md)（一括禁止の精神） |
| 4 | §1 表の PR/コミット欄を更新し、必要なら T3（handoff）へ進む | [runtime-state.md](../runtime-state.md)、[project-context.md](../project-context.md) |

**コア本幹用コピー Prompt（最短）**: [ファイル9](CORE-LANE-PARALLEL-PROMPT-PACK.md) §3.0「コア：スライス 1 本実装」＝ **Prompt-Core-T2**。

### 7.2 その後のタスク（ループ）

| フェーズ | 目的 | 典型的な出口 |
|----------|------|----------------|
| **T2**（繰り返し可） | §1 の残るコードスライスを 1 本ずつ潰す | スライスが尽きる、または次方針のため T0 へ |
| **T3** | `runtime-state` / `project-context` / 最終検証日付の同期 | 次 `next_action` が一文で分かる |
| **T0** | ファイル3（ドラフト）の再承認・差し替え | §6 承認記録、§1 への新スライス起票 |
| **T1** | 文書・サンプル・runbook 先行 | フル pytest 緑、FEATURE 新規行なしを維持 |

推奨ループ: **T2（×N）→ T3 →（必要なら）T0 → T1 → …** 。並行レーンは §3 のまま。

### 7.3 並行開発が効くときの「役割分担」

コア本開発（**ファイル8** の T2/T3/T0）とオペレータ作業を **別セッション（別エージェント）**に分けると、コンテキストが混線しにくい。

| コア側（主） | 並行側（従・別 Prompt） | 合流点 |
|--------------|-------------------------|--------|
| **ファイル8** フェーズ **T2** | **ファイル4** **レーンA**（P0 実測） | **ファイル2** で PASS のみ採用（ドラフトへは PASS のみ） |
| **ファイル8** フェーズ **T3** | **ファイル4** **レーンA** または **レーンB**（同期が急ぎのとき） | HANDOFF に「並行で受領した PASS 要約」を 1 行足してよい |
| **ファイル8** フェーズ **T1** | **ファイル6** **レーンC** ＋ **ファイル7**（画質パケット 1 つ） | ファイル3 §5 ルールどおり PASS のみ反映検討 |
| プロンプト直後の drift 疑い | **ファイル5** **レーンB** | ファイル2 の「プロンプト同期」行 |

**すぐ貼る並行 Prompt 一覧**は [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md) §3.0 および **§3.1（複合・セッション分割）**。

### 7.4 オーケストレーション用（コアを主に明示する一文）

複数レーンを**同一セッション**で扱う場合の型（長くなりがちなので、原則は §7.3 の**分割推奨**）:

「**コア本開発レーン**として **ファイル8** のフェーズ **（T0|T1|T2|T3 のいずれか）** に従ってください。並行で価値がある場合のみ、追加指示として **ファイル4 のレーンA**（または **ファイル5 のレーンB** / **ファイル6 のレーンC** / **ファイル7 の A1〜B4 の1パケット**）の成果を受け取り、**ファイル2** で PASS/NEEDS_FIX を判定してください。未承認 FEATURE の実装は禁止。」

---

## 8. 変更履歴

- 2026-04-10: §7 追加。T1 完了後のコア本幹タスク・並行分担・オーケストレーション一文を正本化。
- 2026-04-10: 初版。コア T0〜T3 と並行レーンの組み合わせ、コピー Prompt 早見を正本化。
