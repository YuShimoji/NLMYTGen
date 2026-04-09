# CLAUDE.md（Claude Code 用入口）

**運用ルールの正本:** [`docs/REPO_LOCAL_RULES.md`](../docs/REPO_LOCAL_RULES.md)（Hard Rules・Read Order・Checklist・Hooks 説明）

本ファイルはツールが慣例で読む **短い入口** に留める。境界・再アンカリングの正本は [`AGENTS.md`](../AGENTS.md)。

最低限ここだけでも:

- この repo 以外は読まない・書かない。
- 詳細は **`docs/REPO_LOCAL_RULES.md`** → **`AGENTS.md`** → **`docs/ai/*.md`**。
- 機械ガード: **`.claude/hooks/guardrails.py`**
