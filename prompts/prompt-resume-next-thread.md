# Claude Code Resume Prompt — Corrective Advance

この prompt は再開補助です。状態の正本は repo 内 docs であり、prompt の本文はそれを上書きしません。

## 最初に必ず読む順序

1. `AGENTS.md`
2. `.claude/CLAUDE.md`
3. `docs/ai/*.md`
4. `docs/INVARIANTS.md` / `docs/USER_REQUEST_LEDGER.md` / `docs/OPERATOR_WORKFLOW.md` / `docs/INTERACTION_NOTES.md`
5. `docs/runtime-state.md` / `docs/project-context.md` / `docs/FEATURE_REGISTRY.md` / `docs/AUTOMATION_BOUNDARY.md`
6. 必要に応じて `CLAUDE.md` / `docs/WORKFLOW.md` / `docs/ARCHITECTURE.md` / `docs/PIPELINE_SPEC.md`

最初に以下の形式で全景確認を出してください。

`📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]`
`🏷️ 案件モード: CLI artifact`

## 絶対に外さないこと

- この repo 以外の docs / memory / files を読まない
- Python の責務はテキスト変換のみ
- `FEATURE_REGISTRY` の status を厳密に守る
- `quarantined` / `hold` / `rejected` を通常の next step として扱わない
- prompt に古い backlog 状態が残っていても docs を優先する

## あなたにやってほしいこと

1. `runtime-state` / `project-context` / `FEATURE_REGISTRY` を照合し、現在地を短く要約する
2. handoff に抜けがないか、canonical docs に未反映の新事実がないか確認する
3. 次候補を出すなら、workflow pain / value path / actor / owner / status を明示する
4. 実装条件が満たされていないなら、勝手に実装せず `Authority Return Items` として返す

## 期待する出力形式

1. 全景確認
2. 現在地の要約
3. bottleneck と trust assessment
4. 実際に進められる候補 3 件以内
5. 推奨案 1 件
6. その場で進めてよい最小作業
7. 必要なら更新するファイル一覧
