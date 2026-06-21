# Common Foundation Dashboard Freshness Audit v1 - 2026-06-22

Artifact id: `common_foundation_dashboard_freshness_audit_v1_2026_06_22`

This audit classifies how `docs/dashboard/project-status.json` and
`docs/dashboard/index.html` should stay useful after the master adoption commit
`f19b6ae docs: adopt common foundation dashboard on master`.

This is not a runner implementation and not a generator implementation. It
does not start `codex exec`, add a subprocess runner, pipe stdin, create a
runtime loop, send external notifications, or write `.agent/reports`,
`.agent/logs`, or `.agent/needs_human.json`.

## Current State Verified

| Check | Result |
| --- | --- |
| working path | `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage` |
| branch | `master` |
| HEAD | `f19b6ae docs: adopt common foundation dashboard on master` |
| `HEAD...origin/master` | `0 0` |
| dashboard | `docs/dashboard/index.html` exists |
| status JSON | `docs/dashboard/project-status.json` parses |
| access guide | `docs/dashboard/README.md` exists |
| screenshot evidence | `docs/review/common-foundation-dashboard-2026-06-17.png` exists |
| launcher | `scripts/operator/open_dashboard.ps1 -PrintPath` resolves the dashboard |

## Freshness Classes

| Class | Fields / artifacts | Owner | Update trigger | Notes |
| --- | --- | --- | --- | --- |
| Generated repo facts | `generated_at`, `branch`, `remote_branch`, current HEAD, upstream parity, worktree dirty/staged state, required artifact existence, link check result, screenshot file size/hash | future minimal status producer | every dashboard refresh or pre-commit dashboard audit | Must be observed, fail-closed input only. It cannot grant runner permission. |
| Derived display values | Completion Matrix meters, artifact readiness counts, link/readiness summaries, screenshot currency | future minimal status producer or scoped dashboard update script | when generated repo facts or artifact set changes | Values should be derived from machine-readable counts, not hand-edited meters. |
| Manual editorial status | `entries[].status`, `entries[].health`, `entries[].progress_pct`, `entries[].next_action`, `review_card`, `freeform_review_intake`, `metric_change_note`, `docs_review` classifications | common-foundation reviewer / slice owner | after human review, accepted docs change, or explicit status decision | Do not auto-infer human judgement from clean Git or passing links. |
| Historical evidence | 2026-06-15 verification docs, adoption source branch metadata, prior screenshot artifact id, previous update rows | owning verification doc | only when adding a new evidence artifact or correcting a factual error | Historical artifacts should remain evidence, not live state. |
| Static access shell | `docs/dashboard/README.md`, `scripts/operator/open_dashboard.ps1`, `scripts/operator/open_dashboard.sh` | dashboard/access slice | only when dashboard path or supported access method changes | Launcher may resolve active checkout paths dynamically, but does not update dashboard state. |
| Static dashboard layout | HTML structure, CSS, first-screen layout, section names | dashboard UI/docs slice | only when review feedback asks for layout/readability change | Do not re-style in freshness-only work. |

## Static Snapshots Today

These fields are currently snapshots, not live telemetry:

- `generated_at`
- `head_before_bootstrap`
- `turn_calendar`
- `review_evidence[].validation`
- `launcher_validation`
- `entries[].last_touched`
- `entries[].progress_pct`
- `artifact_coverage`
- `docs_review`
- `agent_side_next_actions`
- `handoff_gate`
- `mainline_adoption`

They are acceptable as the adoption readback, but they become stale if treated
as current repo state after a later common-foundation slice.

## Regenerate From Repo Docs

A future minimal producer should be allowed to regenerate only bounded
observed/readback fields:

- current branch, HEAD short/long SHA, upstream name, and `HEAD...origin/master`
  count;
- tracked/staged/unstaged dirty state;
- required dashboard artifact existence;
- dashboard link check counts and missing links;
- JSON parse status for `docs/dashboard/project-status.json`;
- launcher `-PrintPath` result;
- screenshot existence, byte size, and PNG signature;
- source verification docs referenced by `artifact_coverage`;
- observed timestamp and command provenance.

The producer should output a JSON object to stdout first. Writing back to
`docs/dashboard/project-status.json` should be a separate explicit mode and
should preserve manual editorial fields unless an input patch explicitly
changes them.

## Manual Editorial Fields

The following fields require human/slice-owner judgement and should not be
auto-updated by a repo-status producer:

- `entries[].status`, `entries[].health`, and `entries[].progress_pct`;
- `entries[].next_action`;
- `review_card`;
- `freeform_review_intake`;
- `metric_change_note`;
- `docs_review[].classification`;
- `handoff_gate.status`;
- dashboard visible wording that interprets review posture.

Clean Git state can support these decisions, but it cannot make them.

## Authoritative Links / Artifacts

| Purpose | Authoritative path |
| --- | --- |
| primary review surface | `docs/dashboard/index.html` |
| machine-readable dashboard registry | `docs/dashboard/project-status.json` |
| open instructions | `docs/dashboard/README.md` |
| PowerShell launcher | `scripts/operator/open_dashboard.ps1` |
| Bash launcher | `scripts/operator/open_dashboard.sh` |
| screenshot evidence | `docs/review/common-foundation-dashboard-2026-06-17.png` |
| mainline adoption proof | `docs/verification/COMMON-FOUNDATION-DASHBOARD-MAINLINE-ADOPTION-2026-06-22.md` |
| status input design | `docs/verification/COMMON-FOUNDATION-STATUS-INPUT-AUDIT-DESIGN-2026-06-15.md` |

`docs/runtime-state.md` remains the restart authority. The dashboard is a
review/access surface, not a replacement for the restart read order.

## Stale Detection Gates

Treat the dashboard as stale when any of these are true:

1. `project-status.json.branch` does not match the live branch.
2. `project-status.json.remote_branch` does not match the live upstream.
3. `HEAD...origin/master` is not `0 0` when the dashboard claims remote parity.
4. The live HEAD is newer than the status registry's recorded adoption/update
   context and a common-foundation dashboard-affecting file changed.
5. A linked artifact in `docs/dashboard/index.html`, `docs/index.md`,
   `docs/features/index.md`, `docs/workflows/index.md`, or
   `docs/decisions/index.md` is missing.
6. `docs/dashboard/project-status.json` fails to parse.
7. `scripts/operator/open_dashboard.ps1 -PrintPath` does not resolve
   `docs/dashboard/index.html`.
8. The screenshot path is missing, zero bytes, or lacks a PNG signature.
9. Manual editorial fields claim readiness or next action that contradicts
   `docs/runtime-state.md`.
10. Any `.agent` runtime artifact, `.codex` local state, `.claude/worktrees`,
    `_tmp`, `_local`, `.ymmp`, render/media output, credentials, or external
    fetch artifact appears in the staged dashboard slice.

## Future Minimal Status Producer Recommendation

Recommended, but only as a separate slice.

The minimal producer should be an observer/serializer with these boundaries:

- default mode writes JSON to stdout only;
- optional write-back mode may update generated repo facts and derived counts
  in `docs/dashboard/project-status.json`;
- it must not write `.agent/reports`, `.agent/logs`, or
  `.agent/needs_human.json`;
- it must not start `codex exec`, call a runner, pipe stdin, create a loop, or
  send notifications;
- it must fail closed on dirty/staged state, missing links, JSON parse errors,
  unknown untracked residue, or unexpected runtime artifacts;
- it must not edit manual editorial status without an explicit input patch.

The first producer slice should prove stdout-only behavior before any
write-back mode is considered.

## Explicitly Out Of Scope

- dashboard visual redesign or decoration;
- broad HTML generator;
- real runner or worker implementation;
- `codex exec`, subprocess runner, stdin piping, runtime loop, notifications;
- `.agent` runtime artifact creation;
- G-27, G-28, Newsroom, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM;
- `.ymmp`, render, rights, production, publishing, or media output.

## Next Use

Use this audit before any future dashboard refresh. If the next slice only
changes common-foundation docs, refresh or verify the generated repo facts and
link checks. If the next slice needs automation, create a separate
stdout-only minimal status producer slice first.
