# Runtime State — NLMYTGen

Project-State-ID: episode-002-milestone-integrated-default-branch-v1
State-Revision: 2026-07-13.1
Updated: 2026-07-13 JST
Product-State: episode-002-milestone-integrated-on-default-branch
Product-Gate: verified-external-editorial-input-selection
Recommended-Next: select-or-provide-verified-editorial-source
External-State: public-repo-default-branch

## Current Slice

- **Approved integration complete**: user-approved Option A was executed as one
  normal fast-forward of `master`. The integrated history contains the fixed
  subject `d8e959c54b8c8f28c31cc2b586bbdd8c79f69f97`, its direct audit child
  `a8b81e43616281691b73520a045dfa6ff44d2054`, and one integration-seal commit.
- **Provenance retained**: the subject, audit, and integration branches remain
  available without rewrite or deletion. The final integration commit is
  resolved from Git refs and the AGENT_REPORT rather than self-embedded here.
- **Bounded metadata rebind complete**: only the pilot's state-dependent source
  manifest, input-validation readback, and internal-review manifest were
  rebound to this runtime state. The rebind is deterministic and does not read
  or regenerate local media or YMM4 projects.
- **Evidence identity preserved**: canonical script text/JSON, claim semantics,
  canonical and derived CSV, source observation receipts, render/project/media
  identities, and immutable pre-integration audit artifacts did not change.
- **Integration checks pass**: the accepted focused milestone suite plus the
  metadata-rebind test, project-state sync, JSON/privacy/path/binary checks,
  canonical/media identity checks, merge-tree, and Git diff checks passed.

## Product Position

- The validated Episode 002 local-evidence workflow is now reachable from the
  repository default branch. `README_INTERNAL_REVIEW.md` and
  `render_receipt.json` remain the internal milestone review/receipt authority.
- `public-repo-default-branch` describes repository placement only. It does not
  mean that any video, editorial source, creative result, rights decision, or
  production output is public or approved.
- Human visual/editorial acceptance, the YMM4 profile/environment version gap,
  cross-machine local `.ymmp` portability, external editorial input, production,
  rights, upload, and publication remain separate gates.

## Exact Next Action

Select or provide one verified external editorial source with explicit source
and provenance/rights context, stable identity, and cue alignment. Keep the
intake internal and non-public; do not infer editorial adoption, creative
acceptance, rights approval, production readiness, or publication approval.

## Evidence and Access

- Integration evidence:
  `docs/verification/EPISODE_002_DEFAULT_BRANCH_INTEGRATION_2026-07-12.md`
- Machine integration receipt:
  `docs/verification/episode_002_default_branch_integration_receipt.json`
- Immutable pre-integration audit:
  `docs/verification/EPISODE_002_MILESTONE_INTEGRATION_AUDIT_2026-07-12.md`
- Milestone review surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/README_INTERNAL_REVIEW.md`

## Integration Boundaries

- No force/non-fast-forward push, merge commit, rebase, squash, cherry-pick, PR,
  branch deletion, YMM4, Computer Use, media regeneration, dependency install,
  publication, upload, or rights action belongs to this completed slice.
- Historical absolute paths, stale secondary docs, human review, and YMM4/local
  project portability remain the five accepted nonblocking debt areas.
- Full-suite drift remains outside this focused integration gate.

## Maintenance Note

Keep this capsule within 160 lines. History remains in `docs/project-context.md`
and Git; the dated integration receipt is the durable transition evidence.
