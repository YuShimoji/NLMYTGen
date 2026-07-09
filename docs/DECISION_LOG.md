# Decision Log

## 2026-07-10: Integrate re-kickstart Project Capsule without overwriting repo authority

Decision:

- Add the kit Project Capsule docs that do not collide with existing NLMYTGen
  authorities.
- Do not overwrite root `AGENTS.md`; it is already the repo-local entry pointer.
- Do not overwrite `docs/runtime-state.md`; it is the current-state authority
  and collides with the kit's `docs/RUNTIME_STATE.md` on Windows.

Reason:

- NLMYTGen already has a mature restart chain:
  `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`.
- The kit docs are useful as compact BUILD/evidence surfaces, but the generic
  runtime and AGENTS templates would be lower-authority duplicates here.

Rejected alternatives:

- Replace `AGENTS.md` with the generic kit file.
- Rename the existing runtime state document only to satisfy template casing.
- Treat docs creation as the whole BUILD deliverable without material evidence.

Evidence:

- `docs/VALIDATION.md` now contains repo-real commands.
- `artifacts/review/rekickstart_2026-07-10_validation_log.txt` records passing
  `compileall`, targeted pytest, and `git diff --check`.

Reversal condition:

- If a future repo-local instruction explicitly makes the kit capsule the
  primary authority, update `AGENTS.md` and `docs/NAV.md` deliberately in a
  separate docs-authority slice.
