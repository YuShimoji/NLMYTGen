# Common Foundation Workflow Index

This index is for operator review workflows only. It does not authorize real
runner execution.

| Workflow | Agent-owned action | User-side action | Completion signal |
| --- | --- | --- | --- |
| Inspect cockpit | Generate/update dashboard, JSON, launchers, and validation ledger. | Open `docs/dashboard/index.html` through the launcher. | Human can see status, artifacts, stale docs, and next actions from one place. |
| Review operator surface | Keep fake/evaluation-only, dry-run preview, and future runner boundaries separated. | Read `docs/AGENT_OPERATOR_SURFACE.md` only when wording needs review. | Runtime-looking paths are not misread as hold-state output. |
| Audit orchestration docs | Keep `docs/AGENT_ORCHESTRATION.md` linked and classified. | Optional read for deeper implementation context. | Real runner remains explicitly closed until a separate authorized slice. |
| Continue common foundation | Use the dashboard status JSON as the active artifact. | Choose the next slice only when a decision is needed. | Next work can start without searching historical verification logs. |

Recommended one-touch access:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1
```
