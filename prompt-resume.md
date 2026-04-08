# Resume Prompt — NLMYTGen

この repo の再開では、**repo 内 docs を正本**として扱ってください。
`docs/ai/*.md` が存在するので、tool-specific helper docs より先に canonical rules として読みます。

## Read Order

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`（運用ルール正本。Claude Code が `.claude/CLAUDE.md` だけ読んだ場合はそこから辿る）
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
15. 必要に応じて `CLAUDE.md` / `docs/WORKFLOW.md` / `docs/ARCHITECTURE.md` / `docs/PIPELINE_SPEC.md`

## First Response Format

`📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]`
`🏷️ 案件モード: CLI artifact`

## Required Checks

- `runtime-state` と `project-context` の handoff を照合する
- `FEATURE_REGISTRY` の status を厳密に守る
- `quarantined` / `hold` / `rejected` を通常の next step として扱わない
- docs にある既知文脈を再質問しない
- prompt の本文より repo docs を優先する

## Expected Output

1. 全景確認
2. 現在地の要約
3. bottleneck と trust assessment
4. 実際に進められる候補 3 件以内
5. 推奨案 1 件
6. その場で進めてよい最小作業
7. 必要なら更新するファイル一覧
