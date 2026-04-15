# コア本幹 + 並行レーン — Prompt 集約・検収ハブ（2026-04）

**役割**: エージェント依頼用に **そのままコピペできる Prompt 全文**と、作業ブロック終了時の **検収チェックリスト**・**親チャット返却テンプレ**を **この 1 ファイル**に集約する。  
**運用の針**（`next_action`・優先表）は引き続き **[runtime-state.md](../runtime-state.md)** を正とする。

**並行の注意**: YMM4 を使う重い作業は **レーン C（視覚三スタイル）** と **主軸 (背景アニメ) / 視覚最低限（Prompt-V）** が資源を奪い合う。人が 1 人なら **同時刻フル稼働は避け、時間分割**する（[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1）。

---

## レーン数・このファイルの役割・どこに何を渡すか

### いくつのレーンか


| 区分                   | 数                   | 名前 / Prompt                                                                 | 正本手順                                                                                                                                       |
| -------------------- | ------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **コア本幹**             | **1 系統**（フェーズは 4+1） | **Prompt-Core-T0〜T3**、**Prompt-Core（フル）**                                   | [ファイル8](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md) §2。リポジトリ上の **コード・ドラフト・verification** を動かす。                                                     |
| **オペレータ並行（runbook）** | **5**               | **Prompt-A〜E**                                                              | [ファイル4](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) のレーン A〜E。台本〜YMM4、GUI LLM 同期、視覚準備、brief、サムネ。                                                  |
| **本ハブで足したサブトラック**    | **3**               | **Prompt-C-Visual-Quality**（ファイル7）、**Prompt-V**（視覚最低限）、**Prompt-R**（改行ギャップ） | ファイル7 / [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) / P01 メモ。C と **V は YMM4 を奪い合う**ので同時刻フルは避ける。 |


**数え方の目安**: runbook 上の「並行軸」は **A〜E の 5**。その外に **コア幹 1** と、上表の **サブ 3**（画質・V・R）がある。コア幹は「レーン A〜E と別枠」の **リポジトリ開発の唯一の幹**（[ファイル1](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) §1.3）。

### 「このファイル」で何を進める想定か

**このファイル自体はタスク進捗をホールドしない。** やることは次の **2 点だけ**を想定している。

1. **依頼**: §5 のフェンスをコピーしてエージェント（別チャット・別担当）へ渡す。
2. **締め**: §3 で検収し、§4 を親チャット等に貼る。

進捗の **正本**は従来どおり **[runtime-state.md](../runtime-state.md)**（針・`next_action`）、案件ごとの **[P01](P01-phase1-operator-e2e-proof.md)** / **B-11** / **[P02](P02-production-adoption-proof.md)** など各 verification。ハブは **コピペ倉庫＋検収ゲート**。

### どこに何を渡すか（成果物の行き先）


| 使う Prompt                   | 主に書く・残す場所（リポジトリ内）                                                                                                                          | コア幹（次の実装サイクル）へ渡すもの                                |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| **Core-T0**                 | [ファイル3](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) の整理、承認依頼用メモ                                                                            | ユーザー承認後の方針文だけ（NEEDS_FIX は渡さない）                    |
| **Core-T1**                 | verification / `samples/*.json` / runbook / GUI 文言                                                                                         | 差分パス一覧＋ファイル2で PASS と自己判定した要約                      |
| **Core-T2**                 | コード、`FEATURE_REGISTRY`、pytest は code 変更時のみ default suite 緑                                                                                  | PR またはコミット＋ POST-APPROVAL §2 チェック                 |
| **Core-T3**                 | [runtime-state.md](../runtime-state.md)、[project-context.md](../project-context.md)                                                        | 次セッション用の `next_action` 一文（親チャットにも §4 で貼る）         |
| **Core-Full**               | 上記の組み合わせ                                                                                                                                   | 各フェーズに応じた上表の集合                                    |
| **Prompt-A**                | [P01](P01-phase1-operator-e2e-proof.md) 表、B-11 系 proof                                                                                     | **ファイル2**で PASS なら、コアは **要約＋ログパス**のみ（未承認の実装依頼は不可） |
| **Prompt-B**                | [ファイル5](LANE-B-gui-llm-sync-checklist.md)、[gui-llm-setup-guide.md](../gui-llm-setup-guide.md) 等                                            | 同上                                                |
| **Prompt-C**                | [ファイル6](LANE-C-operator-prep-2026-04-09.md)、`validate-ir` / `apply-production` ログ                                                          | **機械確認結果**のみコアへ（YMM4 実作業の細部は案件側に閉じる）              |
| **Prompt-C-Visual-Quality** | [ファイル7](VISUAL-QUALITY-PACKETS.md) に沿った JSON / 証跡                                                                                          | PASS/NEEDS_FIX とパス。NEEDS_FIX はファイル3に **書かない**     |
| **Prompt-D**                | brief ファイル、`PACKAGING` 系                                                                                                                   | ファイル2 PASS 時の要約のみ                                 |
| **Prompt-E**                | S-8 証跡、[P03](P03-thumbnail-one-sheet-proof.md) 等 runbook 記載先                                                                               | 運用記録の要約のみ                                         |
| **Prompt-V**                | [P02](P02-production-adoption-proof.md) 1 行 or 案件 verification                                                                             | **コード差分はコア幹に持ち込まない**（ドキュメント・ログのみ）                 |
| **Prompt-R**                | [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) §4 の表、[P01](P01-phase1-operator-e2e-proof.md) メモ列任意 | ギャップ記録。B-xx 起案は **データ後・別承認**                      |


**コア幹が受け取る境界**: 常に **[ファイル2](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)** でゲートする。**PASS** のものだけが [ファイル3](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) や実装に入る。並行レーンからは **「実装して」ではなく証跡・要約・パス**を渡す想定。

---

## 1. ファイル番号早見（他ドキュメントとの共通言語）


| 番号         | パス                                                                                       |
| ---------- | ---------------------------------------------------------------------------------------- |
| ファイル1      | [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)   |
| ファイル2      | [CORE-DEV-OPERATOR-INPUT-CHECKLIST.md](CORE-DEV-OPERATOR-INPUT-CHECKLIST.md)             |
| ファイル3      | [CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md](CORE-DEV-NEXT-IMPLEMENTATION-PLAN-DRAFT.md) |
| ファイル4      | [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)                |
| ファイル5      | [LANE-B-gui-llm-sync-checklist.md](LANE-B-gui-llm-sync-checklist.md)                     |
| ファイル6      | [LANE-C-operator-prep-2026-04-09.md](LANE-C-operator-prep-2026-04-09.md)                 |
| ファイル7      | [VISUAL-QUALITY-PACKETS.md](VISUAL-QUALITY-PACKETS.md)                                   |
| ファイル8      | [CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md](CORE-DEV-TASK-DESIGN-NEXT-CYCLE.md)                 |
| ファイル9      | [CORE-LANE-PARALLEL-PROMPT-PACK.md](CORE-LANE-PARALLEL-PROMPT-PACK.md)（運用原則・早見表・サイクル手順）  |
| **ファイル10** | **本ファイル**（コピペ全文・検収・返却テンプレの正本）                                                            |


---

## 2. コア本幹 — 次にやること（順序固定）

詳細は **ファイル8** §2。ここでは順序のみ固定する。


| フェーズ   | 目的（要約）                                                                                                       |
| ------ | ------------------------------------------------------------------------------------------------------------ |
| **T0** | ファイル3をユーザー承認可能に整える。NEEDS_FIX はドラフトに書かない。                                                                     |
| **T1** | verification・サンプル JSON・runbook / GUI 文言優先。未承認 FEATURE の実装は禁止。                                                |
| **T2** | [CORE-DEV-POST-APPROVAL-SLICES.md](CORE-DEV-POST-APPROVAL-SLICES.md) §1 の **承認済みスライスを 1 本だけ**実装。pytest は `src/` または `tests/` を触った場合のみ default suite 緑（FULL は opt-in）。 |
| **T3** | `runtime-state.md` / `project-context.md` HANDOFF 更新、`next_action` を一文で残す。                                   |


**次サイクルでの縛り**

- [runtime-state.md](../runtime-state.md) の `next_action`（**Phase 1 Block-A 狭義**＝YMM4 S-4 読込まで）と矛盾させない。経路 A／C-09 任意の整理は [P0-BLOCK-A-AND-PATH-A.md](P0-BLOCK-A-AND-PATH-A.md)。オペレータの Phase 1 Block-A 運用はコア T フェーズと独立しうる。
- **T2**: §1 表に **未実装かつ承認済み**のスライスがあるときのみ実施する。現状で次スライスが無い場合は **起票・ユーザー承認待ち**、または **回帰・既存バグ修正のみ**（[FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) 未承認の新規実装はしない）。

---

## 3. 検収（このブロックをここで完結させる条件）

作業終了時に次を満たすこと（コア変更時は特に 3〜4）。

- **ファイル2**に照らし、コアへ取り込むオペレータ入力は **PASS のみ**（NEEDS_FIX はドラフト・実装に混ぜない）。
- **FEATURE_REGISTRY** に無い機能を **承認なしで実装していない**（要望は `proposed` 行の起票に留めた）。
- コアで `src/` または `tests/` を変更した → `uv run pytest` (default suite) が緑。integration 込みは `NLMYTGEN_PYTEST_FULL=1` の opt-in で、必須ゲートではない。ドキュメントのみの変更では pytest 不要。
- `runtime-state.md` の `**next_action` / `last_change_relation` / `parallel_replan_2026_04`** が、実施内容と矛盾しない（更新したなら日付・リンクが辻褄が合う）。
- 並行レーンのみ実施した → コア幹には **機械ログ・証跡パス・P01/P02 等の追記場所**を返し、未承認の「実装して」要求を混ぜない。

---

## 4. 検収用返却テンプレ（親チャット・レビューに貼る）

以下をコピーし、括弧を埋める。

```
## 検収返却（NLMYTGen）
- run_id / ブランチ: （例: `hub_accept_2026-04-11_a` / `master`）
- 実施した Prompt: （例: Core-T1 / Prompt-A / Prompt-V）
- 変更の要約: （1〜3 文）
- 触った主なパス: （例: `docs/verification/foo.md` のみ）
- ファイル2 自己判定: PASS / NEEDS_FIX（NEEDS_FIX なら条件のみ列挙）
- pytest: 未実施 / PASS (default) / PASS (FULL)
- runtime-state 更新: なし / あり（一言）
- 次アクション一文: （例: ユーザー承認後に T2 でスライス X を実装）
```

---

## 5. コピペ用 Prompt 全文（ブロックごとにコピー）

各フェンス内を **丸ごと** エージェントに渡す。リポジトリは **NLMYTGen のみ**（他プロジェクト参照禁止）。

### Prompt-Core-T0

```
**ファイル8** フェーズ **T0**。**ファイル3** をユーザー承認できる状態に整備し、**ファイル2** に照らして NEEDS_FIX のオペレータ入力はドラフトに書き込まないでください。承認後のスライス起票は **CORE-DEV-POST-APPROVAL-SLICES** に従ってください。
```

### Prompt-Core-T1

```
**ファイル8** フェーズ **T1**。**ファイル3** §2 の方針に沿い、verification・サンプル JSON・runbook/GUI 文言を優先してください。コード変更は承認済みスライスまたは明確なバグ修正に限定し、FEATURE_REGISTRY 未承認の実装は禁止。
```

### Prompt-Core-T2

```
**ファイル8** フェーズ **T2**。**CORE-DEV-POST-APPROVAL-SLICES** §1 から **1 スライスだけ**選び実装してください。pytest は `src/` または `tests/` を触った場合のみ `uv run pytest` (default suite) を走らせる。integration 込みの `NLMYTGEN_PYTEST_FULL=1` は opt-in で、必須ゲートではない。
```

### Prompt-Core-T3

```
**ファイル8** フェーズ **T3**。**runtime-state.md** の最終検証・**project-context.md** HANDOFF を更新し、次セッションの `next_action` を一文で残してください。
```

### Prompt-Core（本開発幹・フル）

```
**ファイル8**の §2（フェーズ T0〜T3）を把握したうえで、**ファイル1**→**ファイル2**→**ファイル3**の順でコア本開発レーンを進めてください。A〜E 入力は受け入れ判定し、PASS のみファイル3へ反映、差し戻しは条件のみ返却してください。未承認 FEATURE は増やさず、回帰・文書整合・承認済み修正に限定してください。並行が効くタイミングは **ファイル8** §3 に従ってください。
```

### Prompt-A（Phase 1 実行）

```
ファイル4のレーンAを進めてください。完了条件はB-11形式で取込前/後と4区分を埋め、P01に接続判定を1行追記すること。コア提出時はファイル2の受け入れ条件に自己照合した結果を添えてください。
```

### Prompt-B（GUI LLM 同期）

```
ファイル5のレーンBを進めてください。B-2/B-3/B-4/B-5を実施し、どのGPT構成（1体/2体）を採用したか、repo正本との差分有無を報告してください。コア提出はファイル2のPrompt同期条件に合わせてください。
```

### Prompt-C（視覚三スタイル準備）

```
ファイル6のレーンCを進めてください。_local運用方針を守り、validate-ir/apply-productionの機械確認結果を提出してください。YMM4実作業は案件単位で分離し、コアには機械確認ログのみ渡してください。
```

### Prompt-C-Visual-Quality（bg_anim / overlay）

```
ファイル7のA1〜A4/B1〜B4を使って、対象演出を1パケットずつ実施してください。スコア＋チェックリストをJSONで提出し、PASS/NEEDS_FIXを明示してください。
```

### Prompt-D（H-01 brief 運用）

```
ファイル4のレーンDを進めてください。動画1本につきbriefを1ファイル作成し、C-07入力より先に適用した記録を提出してください。提出時はファイル2の受け入れ観点で不足がないか確認してください。
```

### Prompt-E（サムネ S-8）

```
ファイル4のレーンEを進めてください。S-8の1枚を完了し、テンプレ複製・差し替え・書き出しの実施証跡を提出してください。コアには成果物の運用記録のみ渡し、未承認機能要求は含めないでください。
```

### Prompt-V（視覚最低限・本編1案件）

```
このリポジトリ（NLMYTGen）のみを対象とすること。FEATURE_REGISTRY に無い機能の実装・新規 CLI オプションの追加は禁止（必要なら proposed 起票のみ）。

docs/verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md の §3「トラック A — 視覚最低限チェックリスト」を、本編 1 案件で実施する。validate-ir → apply-production（--dry-run の後に本適用）→ YMM4 で背景レイヤに実体があることを目視確認する。

結果を docs/verification/P02-production-adoption-proof.md に 1 行、または案件専用の verification に run_id・IR パス・ymmp 識別子・PASS/FAIL で残す。コア本幹への持ち込みはドキュメント追記とログパスに限り、未承認のコード変更を混ぜない。
```

### Prompt-R（改行／YMM4 ギャップ計測）

```
このリポジトリ（NLMYTGen）のみ。未承認の B-xx 実装は禁止（データが溜まった後に起票）。

docs/verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md の §4 の表を 1 セッション分埋める。build-csv --stats の代表行と YMM4 取込後の実表示を対にする。

任意で docs/verification/P01-phase1-operator-e2e-proof.md 末尾表のメモ列に 1 行追記してよい（形式は VISUAL プラン §4.2）。
```

---

## 6. 早見（一文・詳細は上の全文へ）

レーン数と成果物の置き場は **冒頭「レーン数・このファイルの役割・どこに何を渡すか」** を参照。


| やりたいこと      | 貼り付け（短文）                                                                             |
| ----------- | ------------------------------------------------------------------------------------ |
| コア T0       | 「**ファイル8** の **T0**、**ファイル3** 整備、**ファイル2** 準拠。詳細は **ファイル10** の Prompt-Core-T0 をコピー。」 |
| コア T1       | 「**ファイル8** の **T1**。詳細は **ファイル10** の Prompt-Core-T1。」                                |
| コア T2       | 「**ファイル8** の **T2**、スライス 1 本。詳細は **ファイル10** の Prompt-Core-T2。」                       |
| コア T3       | 「**ファイル8** の **T3**。詳細は **ファイル10** の Prompt-Core-T3。」                                |
| コアフル        | 「**ファイル10** の Prompt-Core（フル）を実行。」                                                   |
| 並行 A〜E / 画質 | 「**ファイル9** §3.0 早見＋**ファイル10** の該当 Prompt 全文。」                                        |
| 視覚最低限       | 「**ファイル10** の Prompt-V を実行。」                                                         |
| 改行ギャップ      | 「**ファイル10** の Prompt-R を実行。」                                                         |


---

## 7. 委任 Prompt 正本索引（詳細版 2026-04-15 追加）

§5 の Prompt は **短縮版**。別セッション・Custom GPT・user GUI 作業へ独立して委任する場合は、以下の **詳細版正本ファイル**を使う。受入基準・P01/P03 追記形式・実装フラグ整合まで含めて揃えている。

| 委任 Prompt 正本 | 対応 §5 Prompt | 主な用途 | 成果物の行き先 |
|---|---|---|---|
| [H01-packaging-brief-prompt.md](../prompts/H01-packaging-brief-prompt.md) | Prompt-D（H-01 brief） | Custom GPT 固定で動画 1 本の brief 生成 | `samples/<video_id>_brief.md` または brief JSON |
| [H02-thumbnail-one-sheet-prompt.md](../prompts/H02-thumbnail-one-sheet-prompt.md) | Prompt-E（サムネ S-8） | 1 枚分 one-sheet 生成 + `score-thumbnail-s8` payload 出力 | [P03](P03-thumbnail-one-sheet-proof.md) |
| [B17-reflow-residue-observation-prompt.md](../prompts/B17-reflow-residue-observation-prompt.md) | Prompt-R（改行／YMM4 ギャップ） | `build-csv --reflow-v2` 後の残差 4 項目観測 | [P01](P01-phase1-operator-e2e-proof.md) メモ列 1 行 |
| [B18-script-diagnostics-observation-prompt.md](../prompts/B18-script-diagnostics-observation-prompt.md) | Prompt-A の機械診断部 | 新規台本の `diagnose-script` 機械観測（warning 件数・コード集計） | [P01](P01-phase1-operator-e2e-proof.md) メモ列 1 行 |

**使い分け**: §5 の短縮 Prompt はハブ内で完結する即渡しコピー用。上記詳細版は、別担当者に文脈を再説明せず委譲するとき・Custom GPT 固定で繰り返し使うとき・受入基準と P01 追記形式まで厳密に固定したいときに使う。

---

## 8. 変更履歴

- 2026-04-15: §7 委任 Prompt 正本索引（詳細版 4 件）を追加。`docs/prompts/` に正本を分離。
- 2026-04-11: レーン数・本ファイルの役割（進捗はホールドしない）・成果物の行き先表を追加。§6 から冒頭節へ誘導。
- 2026-04-11: 初版。コア本幹タスク設計に沿った検収・全文 Prompt の単一ハブとして新設（ファイル10）。

