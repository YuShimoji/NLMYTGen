# Common Foundation Dashboard Mainline Adoption - 2026-06-22

Artifact id: `common_foundation_dashboard_mainline_adoption_2026_06_22`

This record documents the master-native adoption of the common foundation
dashboard/access surface from the stale source branch
`origin/codex/common-foundation-hold-state-audit` at
`b2c2cb46cfd0790cb028d8dacb493ab34d751e2f`.

The source branch was used as a reference only. This slice did not merge the
branch and did not cherry-pick the whole branch. Existing master docs and
runner files were not overwritten.

## Adopted Artifacts

| Artifact | Path |
| --- | --- |
| dashboard | `docs/dashboard/index.html` |
| status registry | `docs/dashboard/project-status.json` |
| access guide | `docs/dashboard/README.md` |
| screenshot evidence | `docs/review/common-foundation-dashboard-2026-06-17.png` |
| report template | `docs/_templates/operation-cockpit-report.md` |
| PowerShell launcher | `scripts/operator/open_dashboard.ps1` |
| Bash launcher | `scripts/operator/open_dashboard.sh` |
| common foundation feature index | `docs/features/index.md` |
| common foundation workflow index | `docs/workflows/index.md` |
| common foundation decision index | `docs/decisions/index.md` |
| hold-state audit evidence | `docs/verification/COMMON-FOUNDATION-HOLD-STATE-AUDIT-2026-06-15.md` |
| operator readback correction evidence | `docs/verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md` |
| docs operator alignment evidence | `docs/verification/COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15.md` |

## Master-Native Adjustments

- `docs/dashboard/project-status.json` now identifies `branch=master` and
  `remote_branch=origin/master`.
- `docs/dashboard/project-status.json` records the source branch as reference
  metadata under `mainline_adoption`.
- `docs/dashboard/index.html` now describes the surface as a master-native
  dashboard adoption, not a source-branch-only dashboard surface.
- `docs/index.md` keeps its existing Markdown browser guide and adds a narrow
  Common Foundation Cockpit section instead of replacing the page.
- Screenshot evidence was refreshed from `http://127.0.0.1:8765/dashboard/index.html`
  using Chrome headless after the master adjustments.

## Validation

| Check | Result |
| --- | --- |
| master parity before adoption | `HEAD...origin/master = 0 0` |
| source branch commit | `b2c2cb46cfd0790cb028d8dacb493ab34d751e2f` |
| dashboard/status link check | `checked_links=37`, `broken_links=0` |
| `uv run python -m json.tool docs/dashboard/project-status.json` | pass |
| `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1 -PrintPath` | pass; resolved dashboard path |
| `bash scripts/operator/open_dashboard.sh --print-path` | not executable in this Windows environment; Bash file retained as cross-platform launcher |
| screenshot recapture | pass; PNG header valid |

## Boundaries

This slice is docs/review/access only. It does not start a real runner, does
not run `codex exec`, does not add a subprocess runner, does not pipe stdin,
does not create a runtime loop, does not send notifications, and does not write
`.agent/reports`, `.agent/logs`, or `.agent/needs_human.json`.

No G-28, G-27, Newsroom, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM,
`.ymmp`, render, rights, production, publishing, or media output work was
opened.

## Next Use

Open the dashboard from master with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1
```

Fallback:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/operator/open_dashboard.ps1 -PrintPath
```

User review remains open-only / freeform. Fixed labels are not required.
