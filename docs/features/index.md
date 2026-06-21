# Common Foundation Feature Index

This index groups the common foundation feature surfaces that are otherwise
spread across docs and verification artifacts.

| Feature / topic | Status | Health | Source of truth | Next action |
| --- | --- | --- | --- | --- |
| Hold-state audit | Recorded | Watch | `docs/verification/COMMON-FOUNDATION-HOLD-STATE-AUDIT-2026-06-15.md` | Keep as historical evidence; use dashboard JSON for current cockpit state. |
| Operator surface readback | Corrected | Good | `docs/verification/COMMON-FOUNDATION-OPERATOR-SURFACE-READBACK-CORRECTION-2026-06-15.md` | Preserve fake/evaluation-only vs real-runner wording in future report surfaces. |
| Docs operator alignment | Aligned | Good | `docs/verification/COMMON-FOUNDATION-DOCS-OPERATOR-SURFACE-ALIGNMENT-2026-06-15.md` | Keep `AGENT_OPERATOR_SURFACE.md` and `AGENT_ORCHESTRATION.md` linked from the cockpit. |
| Wiki/dashboard bootstrap | Access and IA polished | Good | `docs/dashboard/project-status.json` | Use `scripts/operator/open_dashboard.ps1` or `docs/dashboard/README.md` for open-only freeform review. |

The live registry for status, progress, active artifacts, and next actions is
`docs/dashboard/project-status.json`.
