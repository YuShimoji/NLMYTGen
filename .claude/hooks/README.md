# Hooks

この directory には、Claude 側の明確な逸脱を機械的に止める hook を置く。

## Current Guardrails
- 明示 cross-project scope なしの repo 外 project / memory / docs 参照を、assistant output 上で reject
- broad question による停止の reject
- repeated visual proof 要求の reject

## Scope
Hook は「悪い挙動を通さない」ための最低限の装置で、入口ファイルの代替ではない。
ユーザーが cross-project 作業を明示した場合、repo 外参照はその明示範囲内で扱う。
低価値な作業選択そのものまでは完全には防げないため、[../../docs/REPO_LOCAL_RULES.md](../../docs/REPO_LOCAL_RULES.md) の
block-start checklist とセットで運用する（`../CLAUDE.md` は入口ポインタ）。
