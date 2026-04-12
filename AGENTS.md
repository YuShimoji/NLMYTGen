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

- **フル再アンカリング**（新規セッション・境界の再確認）: 下記「再アンカリング手順」のステップ 1〜5 が正。ステップ 2 の `docs/REPO_LOCAL_RULES.md` とステップ 6 のルート `CLAUDE.md` は別物（後者は方針・技術スタック・成功定義。日々の Hard Rules の正本は **`docs/REPO_LOCAL_RULES.md`**、非交渉境界は `docs/INVARIANTS.md`）。**`.claude/CLAUDE.md`** は Claude Code 等が読む **入口ポインタ**（毎回参照してよいが、中身の正本ではない）。
- **`docs/REPO_LOCAL_RULES.md` の Read Order リスト**: 上記ステップ 1（本ファイル）および 2〜5 と同じファイル列。ルート `CLAUDE.md` はリストに含めないが、方針確認のためステップ 6 相当として読む。
- **`docs/ai/WORKFLOWS_AND_PHASES.md` の「Recommended read order」**: 同一チェーンの **サブセット**。`docs/ai/CORE_RULESET.md` から入るのは **resume / continue / refresh** 向け。境界・repo-local 運用が必要なときは本ファイルと `docs/REPO_LOCAL_RULES.md` に戻ること。

---

## 再アンカリング手順（この repo で作業を開始・再開するとき）
以下の順で読むこと。この repo 以外のファイルは読まない。

```
1. このファイル（AGENTS.md）を読む → プロジェクト概要・境界ルール
2. docs/REPO_LOCAL_RULES.md を読む → repo-local の運用ルール（Hard Rules・Read Order・Checklist）の正本
3. docs/ai/CORE_RULESET.md → docs/ai/DECISION_GATES.md → docs/ai/STATUS_AND_HANDOFF.md → docs/ai/WORKFLOWS_AND_PHASES.md を読む → canonical rules
4. docs/INVARIANTS.md → docs/USER_REQUEST_LEDGER.md → docs/OPERATOR_WORKFLOW.md → docs/INTERACTION_NOTES.md を読む → durable context / pain / ask hygiene
5. docs/runtime-state.md → docs/project-context.md → docs/FEATURE_REGISTRY.md → docs/AUTOMATION_BOUNDARY.md を読む → 現在地・handoff・backlog・境界（`project-context.md` は長大で、IDE の Markdown プレビューが空白になることがある。**航海日誌を読むときはエディタのソース表示・生 MD で開く**）
   - （任意）ドキュメント地図: `docs/NAV.md` — 正本への短い導線。上記ステップの省略にはしない。
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
  resume/handoff の canonical source であり、「補助 docs」として省略しない。

---

## ファイルの責務分担

| ファイル | 責務 | 更新タイミング |
|---------|------|--------------|
| AGENTS.md | 入口。概要・境界・再アンカリング手順 | PJ 構成変更時のみ |
| docs/REPO_LOCAL_RULES.md | repo-local 運用ルール（Hard Rules・Read Order・Checklist）の **正本** | ルール変更時のみ |
| .claude/CLAUDE.md | Claude Code 等の **入口ポインタ**（正本は `docs/REPO_LOCAL_RULES.md`） | 正本パス変更時のみ |
| docs/ai/*.md | vendor-neutral の AI 運用ルール | ルール変更時のみ |
| docs/INVARIANTS.md | 非交渉条件・責務境界・禁止ショートカット | 条件が明示されたブロックで即時 |
| docs/USER_REQUEST_LEDGER.md | 継続要求・未反映是正・backlog delta | 要求や是正が増えたブロックで即時 |
| docs/OPERATOR_WORKFLOW.md | 実ワークフロー・痛点・品質目標 | pain / workflow proof が分かったブロックで即時 |
| docs/INTERACTION_NOTES.md | 報告形式・質問 hygiene・嫌われる形式 | 対話上の学習があったブロックで即時 |
| docs/runtime-state.md | 現在位置。カウンター・状態値・active_artifact | 毎ブロック終端 |
| docs/NAV.md | ドキュメント地図。再開 3 枚・正本索引への導線・テンプレと状態の区別 | 索引や迷子対策を増やしたとき |
| docs/verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md | 立ち絵 複数体×顔差し替えの準備パック（FEATURE G-19/G-20 proposed・別スレッド用 Prompt） | 体+顔スライスを起票したとき |
| docs/project-context.md | 航海日誌。DECISION LOG・IDEA POOL・HANDOFF SNAPSHOT | セッション終端・HANDOFF 時 |
| CLAUDE.md (ルート) | プロジェクト方針・技術スタック・成功定義・同ファイル内「絶対的な制約」。日々の運用 Hard Rules の正本は `docs/REPO_LOCAL_RULES.md`、非交渉境界の正本は `docs/INVARIANTS.md` | 方針変更時のみ（運用ルール・不変条件は各正本側） |

---

## 現在の状況（概要のみ。詳細は docs/ を参照）
- 成功定義 3/3 達成（2026-03-29）。コアパイプライン完成
- 機能追加は docs/FEATURE_REGISTRY.md で管理。登録→承認→実装の順
- 自動化の境界は docs/AUTOMATION_BOUNDARY.md で定義
- ブラウザ向け Web UI / API / YouTube 連携はまだ優先しない（デスクトップ GUI は別）
- 次 frontier は docs/runtime-state.md の **`next_action`** と **「次以降の推奨プラン」**、および docs/project-context.md の `HANDOFF SNAPSHOT` を正本とする
