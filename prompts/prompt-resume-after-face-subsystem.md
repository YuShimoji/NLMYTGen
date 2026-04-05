# Claude Code Resume Prompt — Post-Face Frontier

この prompt は再開補助です。状態の正本は repo 内 docs です。  
必ず `AGENTS.md` の read order に従い、この prompt より canonical docs を優先してください。

## 最初に必ず読む順序

1. `AGENTS.md`
2. `.claude/CLAUDE.md`
3. `docs/ai/CORE_RULESET.md`
4. `docs/ai/DECISION_GATES.md`
5. `docs/ai/STATUS_AND_HANDOFF.md`
6. `docs/ai/WORKFLOWS_AND_PHASES.md`
7. `docs/INVARIANTS.md`
8. `docs/USER_REQUEST_LEDGER.md`
9. `docs/OPERATOR_WORKFLOW.md`
10. `docs/INTERACTION_NOTES.md`
11. `docs/runtime-state.md`
12. `docs/project-context.md`
13. `docs/FEATURE_REGISTRY.md`
14. `docs/AUTOMATION_BOUNDARY.md`
15. 必要な時だけ `CLAUDE.md` / `docs/WORKFLOW.md` / `docs/PRODUCTION_IR_SPEC.md` / 関連 spec

最初に以下の形式で全景確認を出してください。

`📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]`  
`🏷️ 案件モード: CLI artifact`

## 現在の前提

- face 関連は独立サブクエストとして整理済み
- face は「未整理な改善ループ」ではなく、failure class で再オープンする completed subsystem として扱う
- `validate-ir` / `apply-production` は face の mechanical failure を class 付きで検出し、fatal 時は書き出し前に停止する
- repeated visual proof は禁止
- broad question (`判断をお願いします`, `何が足りないか教えてください`) で止まらない
- 今回の主 frontier は face ではなく H-01 Packaging Orchestrator brief

## face を再オープンしてよい条件

以下のいずれかが出た時だけ、face を独立 failure として扱ってよいです。

- `FACE_UNKNOWN_LABEL`
- `PROMPT_FACE_DRIFT`
- `FACE_ACTIVE_GAP`
- `ROW_RANGE_MISSING`
- `ROW_RANGE_INVALID`
- `ROW_RANGE_OVERLAP`
- row-range annotate の unmatched / uncovered
- `FACE_MAP_MISS`
- `IDLE_FACE_MAP_MISS`
- `VOICE_NO_TACHIE_FACE`
- 最終制作物で「現行 label inventory 自体が足りない」と人間が creative judgement した場合

上記以外では、face を主 frontier に戻さないでください。

## あなたにやってほしいこと

1. repo docs を読み、現在地を短く要約する
2. face サブクエストが本当に main frontier から切り離されているか確認する
3. H-01 Packaging Orchestrator brief の value path / actor / owner / integration point を整理する
4. 進めるなら H-01 を中心に実装または仕様固定を進める
5. docs と実装に差分が出たら同じ block で同期する

## 絶対に外さないこと

- repo 外の file / docs / memory を読まない
- `FEATURE_REGISTRY` の status を厳密に守る
- `approved` でない機能を勝手に実装しない
- `quarantined` / `hold` / `rejected` を通常の next step に混ぜない
- face を broad な manual retry loop として再開しない
- mechanical failure を visual proof に押し戻さない

## 期待する出力形式

1. 全景確認
2. 現在地の要約
3. bottleneck と trust assessment
4. face を再度触らない理由、または failure class による再オープン理由
5. 今回進める frontier の value path
6. その場で進めてよい最小作業
7. 更新する docs / files
