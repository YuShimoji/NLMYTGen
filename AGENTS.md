# AGENTS.md — NLMYTGen entry pointer

This file is only a repo entry pointer. Do not grow it into an operations
manual, status snapshot, closeout template, roadmap, or handoff log.

## Read Order

1. `docs/REPO_LOCAL_RULES.md`
2. `docs/runtime-state.md`

Read additional docs only when the current task needs them. If you are unsure
where to look, use `docs/NAV.md`.

Shared development principles: `~/.claude/docs/ops/principles.md` (canonical copy: Recordinator `docs/PRINCIPLES.md`).
Write Tasks, progress, questions, proposals, and returns to the Recordinator Task (see "Task" in principles and `recordinator-forms`).
Project ID: p8130fd12f2.

## Authority

- User / developer instructions override this file.
- Repo-local docs override global Codex fallback rules and global prompt helpers.
- `docs/REPO_LOCAL_RULES.md` owns daily hard rules, restart budget, ask hygiene,
  closeout expectations, and git follow-through.
- `docs/runtime-state.md` owns the current slice and next action.
- `docs/INVARIANTS.md` owns non-negotiable product boundaries.

## Anti-Growth Rule

Do not add detailed procedures, work history, report formats, option menus,
feature status, or temporary plans to this file.

Put changes in the narrow owner instead:

- Rules / ask / closeout behavior: `docs/REPO_LOCAL_RULES.md` or
  `docs/INTERACTION_NOTES.md`
- Current state / next action: `docs/runtime-state.md`
- Decision log / handoff history: `docs/project-context.md`
- Document map: `docs/NAV.md`

Global files under `C:\Users\thank\.codex\` are fallback helpers, not NLMYTGen
authority.
