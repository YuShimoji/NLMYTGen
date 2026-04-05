# Hooks

この directory には、Claude 側の明確な逸脱を機械的に止める hook を置く。

## Current Guardrails
- repo 外 project / memory / docs 参照の reject
- broad question による停止の reject
- repeated visual proof 要求の reject

## Scope
Hook は「悪い挙動を通さない」ための最低限の装置。
低価値な作業選択そのものまでは完全には防げないため、`../CLAUDE.md` の
block-start checklist とセットで運用する。
