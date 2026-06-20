# Common Foundation Decision Index

This index records the current decision posture for the cockpit/bootstrap
layer. Historical details remain in the linked verification artifacts.

| Decision | Current posture | Why it matters | Next movement |
| --- | --- | --- | --- |
| Real runner | No | The foundation still separates preview/readback from execution authority. | Only reopen through a separately authorized runner-consumption design. |
| Active artifact | `docs/dashboard/project-status.json` | Status is now inspectable without reading several verification logs. | Keep this JSON current when common foundation docs move. |
| Primary review surface | `docs/dashboard/index.html` | Human review has a cockpit-first screen with links and next actions. | Use launcher or `docs/dashboard/README.md` for open-only freeform review. |
| Historical verification logs | Evidence only | The three 2026-06-15 logs prove the branch state but are not a live ledger. | Link from dashboard; do not rewrite as polished Wiki pages. |
| Stale / unclear docs | Visible in dashboard | Over-guarded or historical wording can cause operator friction. | Improve narrow docs wording only when the dashboard identifies the bottleneck. |
