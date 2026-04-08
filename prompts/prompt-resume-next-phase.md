# Claude Code Resume Prompt — Next Phase Direction

この prompt は再開のための補助です。状態の正本は常に repo 内 docs です。
`AGENTS.md` の read order に従い、必要ならこの prompt より docs を優先してください。

## 最初にやること

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`（正本。`.claude/CLAUDE.md` は入口ポインタ）
3. `docs/ai/*.md`
4. `docs/INVARIANTS.md` / `docs/USER_REQUEST_LEDGER.md` / `docs/OPERATOR_WORKFLOW.md` / `docs/INTERACTION_NOTES.md`
5. `docs/runtime-state.md` / `docs/project-context.md` / `docs/FEATURE_REGISTRY.md` / `docs/AUTOMATION_BOUNDARY.md`
6. 必要に応じて `CLAUDE.md` / `docs/ARCHITECTURE.md` / `docs/PIPELINE_SPEC.md` / `docs/WORKFLOW.md`

最初に以下の形式で全景確認を出してください。

`📍 NLMYTGen / 🧩 [現在のスライス] / 🔲 [次のアクション]`
`🏷️ 案件モード: CLI artifact`

## この prompt の役割

- 次フェーズの方向を整理する補助
- 実装前に bottleneck / actor / value path を確認する補助
- handoff や chat summary が古い場合、repo docs に戻るための補助

## 進め方

1. repo docs を読んだうえで、現在地と bottleneck を短く要約する
2. `runtime-state` と `project-context` の handoff が最新 docs と矛盾していないか確認する
3. `FEATURE_REGISTRY` の status を厳密に守り、`approved` 以外は勝手に実装しない
4. 次候補を出すなら `Advance / Audit / Excise / Unlock` の lane と actor/owner を明示する
5. 推奨案を出すなら、workflow pain・value path・境界適合の3点を必ず書く

## 強い制約

- `NotebookLM is upstream`
- Python は品質の本体を生成しない
- Path A only (`NotebookLM -> NLMYTGen -> YMM4`)
- 画像生成・.ymmp 生成・演出指定・直接動画生成はやらない
- 他プロジェクトを参照しない
- prompt に書いてある古い next step を docs より優先しない

## 期待する出力形式

1. 全景確認
2. 現在地の要約
3. bottleneck と設計判断ポイント
4. 選択肢 3〜5 個
5. 推奨案 1 つ
6. 最小次アクション 1〜3 個
7. 更新すべき docs / ファイル一覧
