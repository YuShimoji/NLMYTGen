# AGENTS.md — NLMYTGen 入口ファイル
# このファイルは repo の運用入口であり、状態スナップショットの複製ではない。
# Claude Code / Web版Claude がこの repo で作業を開始するとき、最初にここを読む。

---

## このプロジェクトについて
- **プロジェクト名:** NLMYTGen
- **プロジェクト root:** このファイルがある repo のルート
- **種別:** CLI パイプライン（CLI artifact mode 適用）
- **最終成果物到達経路:** NLM transcript → YMM4 CSV → 動画1本完成
- **Artifact Surface:** CSV ファイル → YMM4 読込 → レンダリング結果

---

## 再アンカリング手順（この repo で作業を開始・再開するとき）
以下の順で読むこと。この repo 以外のファイルは読まない。

```
1. このファイル（AGENTS.md）を読む → プロジェクト概要・境界ルール
2. .claude/CLAUDE.md を読む → repo-local の運用ルール
3. docs/ai/CORE_RULESET.md → docs/ai/DECISION_GATES.md → docs/ai/STATUS_AND_HANDOFF.md → docs/ai/WORKFLOWS_AND_PHASES.md を読む → canonical rules
4. docs/INVARIANTS.md → docs/USER_REQUEST_LEDGER.md → docs/OPERATOR_WORKFLOW.md → docs/INTERACTION_NOTES.md を読む → durable context / pain / ask hygiene
5. docs/runtime-state.md → docs/project-context.md → docs/FEATURE_REGISTRY.md → docs/AUTOMATION_BOUNDARY.md を読む → 現在地・handoff・backlog・境界
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
- AGENTS.md / .claude/CLAUDE.md / docs/runtime-state.md / docs/project-context.md は
  「重複」として削除しない。それぞれ異なる責務を持つ入口ファイルである。
- docs/ai/*.md と docs/INVARIANTS.md / docs/USER_REQUEST_LEDGER.md / docs/OPERATOR_WORKFLOW.md / docs/INTERACTION_NOTES.md も
  resume/handoff の canonical source であり、「補助 docs」として省略しない。

---

## ファイルの責務分担

| ファイル | 責務 | 更新タイミング |
|---------|------|--------------|
| AGENTS.md | 入口。概要・境界・再アンカリング手順 | PJ 構成変更時のみ |
| .claude/CLAUDE.md | repo-local 運用ルール。global runbook への依存を減らす | ルール変更時のみ |
| docs/ai/*.md | vendor-neutral の AI 運用ルール | ルール変更時のみ |
| docs/INVARIANTS.md | 非交渉条件・責務境界・禁止ショートカット | 条件が明示されたブロックで即時 |
| docs/USER_REQUEST_LEDGER.md | 継続要求・未反映是正・backlog delta | 要求や是正が増えたブロックで即時 |
| docs/OPERATOR_WORKFLOW.md | 実ワークフロー・痛点・品質目標 | pain / workflow proof が分かったブロックで即時 |
| docs/INTERACTION_NOTES.md | 報告形式・質問 hygiene・嫌われる形式 | 対話上の学習があったブロックで即時 |
| docs/runtime-state.md | 現在位置。カウンター・状態値・active_artifact | 毎ブロック終端 |
| docs/project-context.md | 航海日誌。DECISION LOG・IDEA POOL・HANDOFF SNAPSHOT | セッション終端・HANDOFF 時 |
| CLAUDE.md (ルート) | プロジェクト方針・技術スタック・成功定義 | 方針変更時のみ |

---

## 現在の状況（概要のみ。詳細は docs/ を参照）
- 成功定義 3/3 達成（2026-03-29）。コアパイプライン完成
- 機能追加は docs/FEATURE_REGISTRY.md で管理。登録→承認→実装の順
- 自動化の境界は docs/AUTOMATION_BOUNDARY.md で定義
- Web UI / API / YouTube 連携はまだ優先しない
- 次 frontier は docs/runtime-state.md の `next_action` と docs/project-context.md の `HANDOFF SNAPSHOT` を正本とする
