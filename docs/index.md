# NLMYTGen Docs Entry

This page is the lightweight entry point for the current docs review surface.
For normal restarts, keep using `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, and
`docs/runtime-state.md` first. This index only helps a human inspect the common
foundation cockpit/dashboard slice without hunting through folders.

## Common Foundation Cockpit

- [Cockpit dashboard](dashboard/index.html)
- [Project status JSON](dashboard/project-status.json)
- [Dashboard screenshot evidence](review/common-foundation-dashboard-2026-06-17.png)
- [PowerShell dashboard launcher](../scripts/operator/open_dashboard.ps1)
- [Bash dashboard launcher](../scripts/operator/open_dashboard.sh)
- [Operation Cockpit report template](_templates/operation-cockpit-report.md)

One-touch local access:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1
```

## Common Foundation Topic Docs

- [Agent orchestration](AGENT_ORCHESTRATION.md)
- [Agent operator surface](AGENT_OPERATOR_SURFACE.md)
- [Feature index](features/index.md)
- [Workflow index](workflows/index.md)
- [Decision index](decisions/index.md)

## Verification Evidence

Historical verification artifacts are linked for evidence. They are not the
current dashboard state by themselves.

- [Common Foundation hold-state audit](verification/COMMON-FOUNDATION-HOLD-STATE-AUDIT-2026-06-15.md)
- [Operator surface readback correction](verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md)
- [Docs operator surface alignment](verification/COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15.md)
- [Status input audit design](verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md)
- [Live repo status JSON producer design](verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md)

## Boundaries

This dashboard slice is docs/review/access only. Real runner remains No: no
real `codex exec`, no subprocess runner, no stdin piping, no runtime loop, no
external notification, and no `.agent/reports`, `.agent/logs`, or
`.agent/needs_human.json` runtime artifact creation is authorized by this page.
