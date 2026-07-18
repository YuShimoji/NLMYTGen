# Runtime State — NLMYTGen

Project-State-ID: new-banknote-successor-integration-audited-selective-ready-v1
State-Revision: 2026-07-19.2
Updated: 2026-07-19 JST
Product-State: new-banknote-successor-integration-audited-selective-ready
Product-Gate: new-banknote-successor-selective-integration
Recommended-Next: integrate-audited-new-banknote-successor-artifacts
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

## Current Slice

- **H0 remains accepted**: the primary branch keeps the explicit option A
  human receipt, all eight approved hashes, T00–T07 lineage, and the
  current-lineage YMM4 revalidation. The approved script, cue/order, scene
  2/4/3, Reimu/Marisa 3/6, 15 claims, 20 units, 21 edges, and both CSVs are
  unchanged.
- **Exact graph audited**: primary `5e50ff7`, candidate `833717f`, common
  baseline `b05eb386`, and origin/master `37a02fb` were verified after fetch.
  Divergence is 7 primary-only and 13 candidate-only commits. Both baselines
  remain unambiguous ancestors.
- **Coverage complete**: all 20 unique commits and all 84 side-path entries
  covering 77 union paths are classified; unclassified commits and paths are
  zero. Commit, path, authority, conflict, and integration-contract evidence
  is tracked under `docs/verification/`.
- **Approved identity resolved**: primary is 8/8 exact. Candidate is 7/8
  exact; only its metadata-linked `README_CANONICAL_SCRIPT_REVIEW.md` differs.
  That variant is excluded because the primary approved hash wins. Canonical
  script JSON/TXT, both CSVs, cue trace, and source manifest are cross-branch
  exact.
- **Authority is one-to-one**: primary T00–T07 is the current content surface;
  candidate D00–D10 becomes secondary editorial deep-audit evidence. Primary
  revalidation is current YMM4 structural authority; candidate tracked import
  observation is historical predecessor evidence over the same bytes and
  metrics.
- **Operator tooling resolved**: primary five-action approval/lineage-aware
  Operator Batch remains current. Candidate four-action batch and its add/add
  module/test conflict are excluded; its bounded supervisor review receipt may
  remain historical.
- **Visual proposal compatible but unselected**: candidate A/B/C maps the same
  nine cues and 2/4/3 scenes. Route A remains `recommended_not_selected`,
  human selection is required, implementation is unauthorized, and rights are
  unresolved proposal-only.
- **Normal merge rejected**: non-mutating merge-tree reports seven conflicts—
  five current-state documents and two Operator Batch code/test paths. The
  accepted recommendation is `selective_integration_ready`, using exact
  candidate paths rather than a merge or whole-commit cherry-pick.
- **Regeneration boundary explicit**: candidate editorial provenance README,
  content lock, and validation readback encode candidate-current and
  same-machine disposition and must be regenerated against primary authority.
  All compact state surfaces must also be regenerated after later integration.
- **Source branches preserved**: no merge, rebase, cherry-pick, visual choice,
  approved-content edit, YMM4 operation, render, media, publication, rights
  action, or master mutation occurred in this audit.

## Product Position

The project now has an evidence-backed selective integration contract rather
than an ambiguous branch merge. It identifies 27 candidate paths for
integration, two historical paths to retain, eight surfaces to regenerate,
and 14 candidate paths to exclude. This audit does not integrate them; it
makes the later successor construction bounded and reviewable.

## Exact Next Action

The next Worker owns `new-banknote-successor-selective-integration-v1`. Create
`codex/new-banknote-successor-selective-integration-v1` from exact primary
`5e50ff707806724e67a5e0cec215bdd3b604ce32`, materialize only the exact
candidate paths listed in the audit JSON from candidate `833717f`, keep all
primary approved/lineage/revalidation/Operator Batch bytes, rebind and
regenerate the three provenance authority surfaces, then regenerate one
current state and run the recorded targeted validation. Do not select A/B/C.

## Evidence and Access

- Primary audit surface:
  `docs/verification/NEW_BANKNOTE_SUCCESSOR_BRANCH_INTEGRATION_AUDIT.md`.
- Recommendation and exact later contract:
  `docs/verification/new_banknote_successor_integration_audit.json`.
- Exhaustive inventories:
  `new_banknote_successor_commit_inventory.json` and
  `new_banknote_successor_path_inventory.json`.
- One-to-one authority result:
  `new_banknote_successor_authority_conflict_matrix.json`.
- H0 authority remains the pilot's `README_CONTENT_LINEAGE.md` and
  `README_EXISTING_YMM4_EVIDENCE_REVALIDATION.md` packages.

## Active Boundaries

- No source branch is integrated; actual selective integration is H1.
- Pronunciation/rhythm/clipping, exact S04/S05 historical identity,
  token-level authorship, remote CI/branch policy, and human visual preference
  remain unknown or unresolved.
- H2 human A/B/C selection, diagnostic YMM4 work, render, production project,
  rights/legal/final-thumbnail approval, upload/publication, master
  integration, and full-suite Integrity work remain undone.

## Maintenance Note

Keep this capsule within 160 lines. Exact path lists and conflict mechanics
belong in the audit artifacts; resolve the audit commit from the current
branch tip after closeout.
