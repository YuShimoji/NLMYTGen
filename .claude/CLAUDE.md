# CLAUDE.md（Claude Code 用入口）

**運用ルールの正本:** [`docs/REPO_LOCAL_RULES.md`](../docs/REPO_LOCAL_RULES.md)（短い front-door。Core Rules / Reporting / Ask Hygiene / Hooks）

本ファイルはツールが慣例で読む **短い入口** に留める。`AGENTS.md` も入口ポインタであり、詳細手順・履歴・報告テンプレは置かない。

最低限ここだけでも:

- 通常はこの repo 以外は読まない・書かない。ユーザーが cross-project / 他 repo 作業を明示した場合は、その明示範囲だけ扱う。
- 通常再開は **`docs/REPO_LOCAL_RULES.md`** → **`docs/runtime-state.md`**。`AGENTS.md` は入口確認だけ、`docs/ai/*.md` は該当 gate が必要なときだけ追加参照。
- 略称は `ID（説明名）` 形式で書く。正本: `docs/ai/CORE_RULESET.md` §Terminology。グロサリー: `CLAUDE.md`（ルート）の「工程・レイヤー略語の読み方」表。
- 機械ガード: **`.claude/hooks/guardrails.py`**
