# Research Notes

| Date | Topic | Source | Observation | Design implication | Adopted | Reason |
|---|---|---|---|---|---|---|
| 2026-07-10 | re-kickstart command source | `README.md`, `pyproject.toml`, `gui/package.json`, `docs/runtime-state.md` | Repo has Python CLI, optional pytest dev dependency, Electron GUI scripts, and current Episode 002 review artifacts | Validation docs should use repo-local commands and avoid generic web-server assumptions | yes | It directly determines `docs/VALIDATION.md` |
| 2026-07-10 | current product boundary | `docs/runtime-state.md`, `production_pilots/.../validation_readback.json` | Current pack is review/import-ready only; actual YMM4 import, render, real-input replacement, rights, and public-ready gates are closed | Next BUILD candidates must preserve closed-gate language | yes | Prevents proof existence from becoming a production claim |

## Research rule

Research is valid only when it connects to one of:

- adopted design decision
- rejected design decision
- implementation diff
- next probe
- monetization or platform decision gate

A research table alone does not complete BUILD.
