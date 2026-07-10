# Historical Common Foundation Workflow Index

This index is for operator review workflows only. It does not authorize real
runner execution.

| Workflow | Agent-owned action | User-side action | Completion signal |
| --- | --- | --- | --- |
| Inspect historical cockpit | Preserve the dated dashboard, JSON, launchers, access guide, screenshot, and validation ledger as evidence. | Open `docs/dashboard/index.html` only when the 2026-06-22 common-foundation design needs review. | The snapshot is understood without being mistaken for current state. |
| Review operator surface | Keep fake/evaluation-only, dry-run preview, and future runner boundaries separated. | Read `docs/AGENT_OPERATOR_SURFACE.md` only when wording needs review. | Runtime-looking paths are not misread as hold-state output. |
| Audit orchestration docs | Keep `docs/AGENT_ORCHESTRATION.md` linked and classified. | Optional read for deeper implementation context. | Real runner remains explicitly closed until a separate authorized slice. |
| Continue common foundation snapshot review | Treat the dashboard JSON as dated evidence only. | Use Project Cockpit for the current route. | Old common-foundation wording is not mistaken for live product state. |

Recommended one-touch access:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1
```

Fallback access:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1 -PrintPath
```
