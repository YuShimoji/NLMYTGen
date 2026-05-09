# REPO_LOCAL_RULES.md — repo-local operating rules

NLMYTGen の通常再開で読む短い front-door。ここには毎回効く行動ルールだけを置く。事故履歴、報告テンプレート、個別 lane の手順、status snapshot は置かない。

詳細の置き場:

- 非交渉の product boundary: `docs/INVARIANTS.md`
- 現在位置 / next action: `docs/runtime-state.md`
- 対話・報告 failure class: `docs/INTERACTION_NOTES.md`
- workflow pain / operator 手順: `docs/OPERATOR_WORKFLOW.md`
- 決定履歴 / handoff history: `docs/project-context.md`
- 迷子時の索引: `docs/NAV.md`

## Restart Read Budget

通常再開で読むのは次の 3 点まで。

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`

追加で読むのは、今の作業を進める根拠が不足している場合だけ。読む範囲は該当節・該当 ID・該当 artifact に限定し、全文読了を progress にしない。

## Core Rules

- Repo-local authority comes first. Global Codex files and prompt helpers are fallback only.
- `AGENTS.md` is an entry pointer. Do not add procedures, status, roadmaps, report formats, option menus, or history there.
- Stay inside this repo unless the user explicitly names a cross-project scope. If cross-project scope is explicit, touch only that scope.
- Do not ask broad questions when repo evidence can decide the next move. If a question is necessary, ask only the decision that changes the bottleneck.
- Prefer assistant-owned mechanical closure: dry-run, readback, gap report, drift check, docs sync, or focused tests before asking for manual proof.
- Do not request repeated YMM4 visual proof. Use it for first E2E, changed review surfaces, or final creative judgement.
- Keep task-specific scars out of this file. Put lane-specific constraints in the relevant spec, registry, handoff artifact, or `runtime-state`.

## Git And Tests

- Git follow-through is assistant-owned by default. After a validated slice, run non-destructive `git add` / `git commit` / `git push` without asking again.
- Stop before destructive operations, pushed-history rewrites, ambiguous large deletions, cross-repo publication, or explicit user prohibition.
- For `src/`, `gui/`, or CLI contract changes, run the narrow relevant test first; use `uv run pytest` as the normal repo-level Python check.
- Use `NLMYTGEN_PYTEST_FULL=1 uv run pytest` only when subprocess/integration coverage is relevant.
- Do not run pytest for docs-only or runtime-state-only edits unless the docs changed an executable contract.
- Playwright and commit-history analysis are optional diagnostics, not default gates.

## Reporting Rule

Reports should make the work usable without forcing the user to open files. State what changed, why it matters, what remains uncertain, and what the next concrete move is.

Do not emit fixed closeout labels such as `summary`, `evidence`, `risk`, `next owner`, `assistant status`, or `assistant next` unless the user asks for that structure. Those concepts are internal checks, not output fields.

If user action is required, include the executable details in normal language: exact path or artifact, required versus optional inputs, success signal, what to return on failure, and what the assistant will verify after receiving it. Do not replace those details with a docs link.

When listing residual work or options, give each item enough context to choose: purpose, effect, prerequisite, current state, and next move. Avoid `P0/P1`, path lists, or test names as the explanation.

## Ask Hygiene

- Ask only high-level decisions with real tradeoffs.
- Offer 2-4 options only when they solve different bottlenecks.
- Do not include unrelated repos, memories, or tools as options unless the user made that scope explicit.
- When corrected, verify the claim against repo evidence, then proceed with the smallest safe fix in the same block.

## Hooks

Machine-checkable violations belong in `.claude/hooks/guardrails.py`, not as more prose in this file. Keep this file short enough to read and apply every restart.
