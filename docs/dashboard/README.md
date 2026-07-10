# Historical Common Foundation Dashboard Access

This dashboard is a 2026-06-22 common-foundation adoption snapshot. It is not
the current project registry. Read `docs/PROJECT_COCKPIT.md` for the current
GitHub-facing state and `docs/runtime-state.md` for the internal current
capsule.

Use the launcher from the checkout root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1
```

If the browser does not open, print the resolved file path and open it directly:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1 -PrintPath
```

The primary review surface is `docs/dashboard/index.html`. The dashboard links
`docs/dashboard/project-status.json`,
`docs/review/common-foundation-dashboard-2026-06-17.png`, and
`docs/_templates/operation-cockpit-report.md`.

User-side work is `USER_OPEN_ONLY` or `USER_REVIEW_FREEFORM`. No Git command,
test run, runner start, publish action, or production-lane operation is required
from the user to review this cockpit.

This access guide is repo-relative by design. Full local paths can be printed by
the launcher for the active checkout, but they are not canonical project state.
