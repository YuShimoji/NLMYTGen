# AGENTS.md — NLMYTGen 入口ファイル
# このファイルは repo の運用入口であり、状態スナップショットの複製ではない。
# Claude Code / Web版Claude がこの repo で作業を開始するとき、最初にここを読む。

---

## このプロジェクトについて
- **プロジェクト名:** NLMYTGen
- **プロジェクト root:** このファイルがある repo のルート
- **種別:** CLI を中核とするパイプライン（CLI artifact mode 適用）。デスクトップ GUI（Electron、`gui/`・`start-gui.bat`）は CLI の操作面。成果物の正本は CSV 等の artifact
- **最終成果物到達経路:** NLM transcript → YMM4 CSV → 動画1本完成
- **Artifact Surface:** CSV ファイル → YMM4 読込 → レンダリング結果

---

## Read order の関係（正本）

- **通常再開（default）**: 毎回の読了対象は最小にする。`AGENTS.md` の境界、`docs/REPO_LOCAL_RULES.md` の Hard Rules / Block-Start Checklist、`docs/runtime-state.md` の `next_action` を確認し、そこから必要な正本だけを追加で読む。
- **フル再アンカリング（例外）**: 新規セッションで境界が不明、ルール変更直後、正本間 drift 検出、user が REANCHOR / REFRESH / AUDIT を明示、または `runtime-state.md` だけでは作業接続できない場合に限る。下記「フル再アンカリング手順」を使う。
- **正本 docs の扱い**: `docs/ai/*.md` / `docs/INVARIANTS.md` / `docs/USER_REQUEST_LEDGER.md` / `docs/OPERATOR_WORKFLOW.md` / `docs/INTERACTION_NOTES.md` は削除禁止の canonical source だが、通常再開時に全文読了する義務はない。変更対象・判断対象に応じて該当節だけ参照する。
- **`.claude/CLAUDE.md`** は Claude Code 等が読む **入口ポインタ**。日々の Hard Rules の正本は **`docs/REPO_LOCAL_RULES.md`**、非交渉境界は `docs/INVARIANTS.md`。

---

## 通常再開手順（default）

この repo 以外のファイルは読まない。通常は以下で止め、必要になった正本だけ追加で読む。

```
1. AGENTS.md → repo 境界・削除禁止・現在の入口責務を確認
2. docs/REPO_LOCAL_RULES.md → Hard Rules / Block-Start Checklist / Ask Hygiene を確認
3. docs/runtime-state.md → `slice` / `next_action` / `last_change_relation` / `last_verification` を確認
4. 必要時のみ:
   - 迷ったら docs/NAV.md
   - handoff や決定履歴が必要なら docs/project-context.md の HANDOFF SNAPSHOT / 該当 DECISION LOG だけ
   - status / backlog 判断なら docs/FEATURE_REGISTRY.md の該当 ID だけ
   - ルール・境界・対話失敗を扱うなら docs/ai/*.md / INVARIANTS / USER_REQUEST_LEDGER / OPERATOR_WORKFLOW / INTERACTION_NOTES の該当節だけ
5. 全景確認を出力:
   📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]
   🏷️ 案件モード: CLI artifact
```

---

## フル再アンカリング手順（例外）
通常再開で接続できない場合だけ使う。

```
1. このファイル（AGENTS.md）を読む → プロジェクト概要・境界ルール
2. docs/REPO_LOCAL_RULES.md を読む → repo-local の運用ルール（Hard Rules・再開読了予算・Checklist）の正本
3. docs/ai/CORE_RULESET.md → docs/ai/DECISION_GATES.md → docs/ai/STATUS_AND_HANDOFF.md → docs/ai/WORKFLOWS_AND_PHASES.md を読む → canonical rules
4. docs/INVARIANTS.md → docs/USER_REQUEST_LEDGER.md → docs/OPERATOR_WORKFLOW.md → docs/INTERACTION_NOTES.md を読む → durable context / pain / ask hygiene
5. docs/runtime-state.md → docs/project-context.md の HANDOFF SNAPSHOT / 必要な DECISION LOG → docs/FEATURE_REGISTRY.md の該当 ID → docs/AUTOMATION_BOUNDARY.md の該当節を読む → 現在地・handoff・backlog・境界（`project-context.md` は長大で、全文読了ではなく該当節を読む）
   - （任意）ドキュメント地図: `docs/NAV.md` — 正本への短い導線。迷子対策であり、全ファイル読了義務ではない。
6. 必要な時だけ CLAUDE.md / docs/ARCHITECTURE.md / docs/PIPELINE_SPEC.md / docs/WORKFLOW.md / ADR を読む
7. 全景確認を出力:
   📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]
   🏷️ 案件モード: CLI artifact
```

---

## 境界ルール（厳守）

### 他プロジェクトへの逸脱禁止
- **この repo 以外のプロジェクトのファイルを読み書きしない。**
- HoloSync / NLMandSlideVideoGenerator / NarrativeGen / VastCore 等のファイル・memory・docs を参照しない。
- 「NLMYTGen 用の memory がない」場合は**スキップする。他 PJ の memory を代用しない。**
- AskUserQuestion の選択肢に「別プロジェクトへ移動」を含めない。
- 別 repo への移動はユーザーが明示的に指示した場合のみ。

### AskUserQuestion の範囲制限
- 選択肢はこの repo 内の Advance / Audit / Excise / Unlock に限定すること。
- 他 repo のタスクを候補に混ぜない。
- 「別セッションで別 PJ」の提案はこの repo の判断としては出さない。

### 運用ファイルの削除禁止
- AGENTS.md / docs/REPO_LOCAL_RULES.md / .claude/CLAUDE.md / docs/runtime-state.md / docs/project-context.md は
  「重複」として削除しない。それぞれ異なる責務を持つ入口・正本ファイルである（`.claude/CLAUDE.md` はポインタ、運用本文の正本は `docs/REPO_LOCAL_RULES.md`）。
- docs/ai/*.md と docs/INVARIANTS.md / docs/USER_REQUEST_LEDGER.md / docs/OPERATOR_WORKFLOW.md / docs/INTERACTION_NOTES.md も
  resume/handoff の canonical source であり、「補助 docs」として削除しない。ただし通常再開で全文読了しない。判断対象に応じて該当節を参照する。

---

## ファイルの責務分担

| ファイル | 責務 | 更新タイミング |
|---------|------|--------------|
| AGENTS.md | 入口。概要・境界・通常再開 / フル再アンカリング手順 | PJ 構成変更時のみ |
| docs/REPO_LOCAL_RULES.md | repo-local 運用ルール（Hard Rules・再開読了予算・Checklist）の **正本** | ルール変更時のみ |
| .claude/CLAUDE.md | Claude Code 等の **入口ポインタ**（正本は `docs/REPO_LOCAL_RULES.md`） | 正本パス変更時のみ |
| docs/ai/*.md | vendor-neutral の AI 運用ルール | ルール変更時のみ |
| docs/INVARIANTS.md | 非交渉条件・責務境界・禁止ショートカット | 条件が明示されたブロックで即時 |
| docs/USER_REQUEST_LEDGER.md | 継続要求・未反映是正・backlog delta | 要求や是正が増えたブロックで即時 |
| docs/OPERATOR_WORKFLOW.md | 実ワークフロー・痛点・品質目標 | pain / workflow proof が分かったブロックで即時 |
| docs/INTERACTION_NOTES.md | interaction failure・質問 hygiene・手動確認 conventions | 対話上の構造的 failure mode が分かったブロックで即時 |
| docs/runtime-state.md | 現在位置。カウンター・状態値・active_artifact | 毎ブロック終端 |
| docs/NAV.md | ドキュメント地図。再開 3 枚・正本索引への導線・テンプレと状態の区別 | 索引や迷子対策を増やしたとき |
| docs/verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md | 立ち絵 複数体×顔差し替えの履歴・調査パック（G-19 done / G-20 approved）。現行 G-24 判断の入口ではない | 体+顔スライスを再確認するとき |
| docs/project-context.md | 航海日誌。DECISION LOG・IDEA POOL・HANDOFF SNAPSHOT | セッション終端・HANDOFF 時 |
| CLAUDE.md (ルート) | プロジェクト方針・技術スタック・成功定義・同ファイル内「絶対的な制約」。日々の運用 Hard Rules の正本は `docs/REPO_LOCAL_RULES.md`、非交渉境界の正本は `docs/INVARIANTS.md` | 方針変更時のみ（運用ルール・不変条件は各正本側） |

---

## 現在の状況（概要のみ。詳細は docs/ を参照）
- 成功定義 3/3 達成（2026-03-29）。コアパイプライン完成
- 機能追加は docs/FEATURE_REGISTRY.md で管理。登録→承認→実装の順
- 自動化の境界は docs/AUTOMATION_BOUNDARY.md で定義
- ブラウザ向け Web UI / API / YouTube 連携はまだ優先しない（デスクトップ GUI は別）
- 次 frontier は docs/runtime-state.md の **`next_action`** を正本とする。docs/project-context.md は航海日誌であり、必要時に `HANDOFF SNAPSHOT` / 該当 DECISION LOG だけ参照する
