# Hooks

この directory には、Claude 側の明確な逸脱を機械的に止める hook を置く。

## Current Guardrails
- 明示 cross-project scope なしの repo 外 project / memory / docs 参照を、assistant output 上で reject
- broad question による停止の reject
- repeated visual proof 要求の reject
- `.md` / README / manifest を user-owned 手順本文の代替にする handoff laundering の reject

## Scope
Hook は「悪い挙動を通さない」ための最低限の装置で、入口ファイルの代替ではない。
ユーザーが cross-project 作業を明示した場合、repo 外参照はその明示範囲内で扱う。
低価値な作業選択そのものまでは完全には防げないため、[../../AGENTS.md](../../AGENTS.md) と
[../../docs/REPO_LOCAL_RULES.md](../../docs/REPO_LOCAL_RULES.md) の core rules とセットで運用する。
