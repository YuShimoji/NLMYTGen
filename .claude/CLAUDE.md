# CLAUDE.md（Claude Code 用入口）

**運用ルールの正本:** [`docs/REPO_LOCAL_RULES.md`](../docs/REPO_LOCAL_RULES.md)（Hard Rules・再開読了予算・Checklist・Hooks 説明）

本ファイルはツールが慣例で読む **短い入口** に留める。境界・再アンカリングの正本は [`AGENTS.md`](../AGENTS.md)。

最低限ここだけでも:

- この repo 以外は読まない・書かない。
- 通常再開は **`docs/REPO_LOCAL_RULES.md`** → **`docs/runtime-state.md`**。`AGENTS.md` と `docs/ai/*.md` は境界・該当 gate が必要なときだけ追加参照。
- 略称は `ID（説明名）` 形式で書く。正本: `docs/ai/CORE_RULESET.md` §Terminology。グロサリー: `CLAUDE.md`（ルート）の「工程・レイヤー略語の読み方」表。
- 機械ガード: **`.claude/hooks/guardrails.py`**
