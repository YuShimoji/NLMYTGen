# Runtime State — NLMYTGen

Project-State-ID: episode-002-verified-local-evidence-internal-render-validated-v1
State-Revision: 2026-07-12.2
Updated: 2026-07-12 JST
Product-State: episode-002-verified-local-evidence-internal-render-validated
Product-Gate: milestone-integration-audit
Recommended-Next: audit-feature-branch-integration-after-render-milestone
External-State: public-repo-feature-branch

## Current Slice

- **Internal render validated**: the ignored local YMM4 project parses as the
  expected 3563-frame, 1920x1080/60 fps structure with 9 VoiceItems,
  3 ImageItems, 3 independent TextItems, and canonical speaker counts 3/6.
- **Original MP4 validated without mutation**: ISO-BMFF structure, `ffprobe`
  streams, reported duration/frame count, and full video+audio decode pass.
  The original remains ignored and hash-bound by `render_receipt.json`.
- **Review proxy available**: an ignored 1280x720/60 fps H.264/AAC proxy was
  derived from the original for internal review and independently full-decoded.
- **Operator result preserved**: the collected success result remains byte-for-byte
  unchanged. Collector hardening now uses explicit UTF-8 result files,
  collect-only recovery, and a dedicated error for a YMM4 project JSON saved
  under an `.mp4` name.
- **Tracked review package is primary**: render validation, receipt,
  source-to-output traceability, correction report, five-question review sheet,
  and limitations are the current review authority. Earlier static project
  artifacts are explicitly pre-operator contract snapshots.

## Product Position

- This is an internal, non-final, non-production recap pilot based only on
  tracked project evidence. A valid render does not grant editorial, rights,
  creative, public, or production approval.
- The operator observed YMM4 `4.54.0.1`; the tracked character profile records
  `4.53.0.9`. No mapping error was reported, but the version difference remains
  a documented portability debt.
- The operator described the output setting as `MPEG`; that is an observation,
  not a codec assertion. Machine evidence identifies H.264 video and AAC audio.
- No Computer Use, Worker-launched YMM4, rerender, original overwrite,
  production `.ymmp`, external fetch, upload, publication, merge, or rebase was
  performed in this slice.

## Exact Next Action

Audit this feature branch as an integration milestone: review the bounded diff,
tracked evidence privacy, review-package authority, and target-branch risk.
Return an integration recommendation only; do not merge or rebase automatically.

## Evidence and Access

- Primary review surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/verified_local_evidence_input_pilot/README_INTERNAL_REVIEW.md`
- Render machine validation:
  `verified_local_evidence_input_pilot/render_validation_readback.json`
- Hash-bound receipt and traceability:
  `verified_local_evidence_input_pilot/render_receipt.json` and
  `verified_local_evidence_input_pilot/source_to_output_traceability.json`
- Operator review questions:
  `verified_local_evidence_input_pilot/operator_review_sheet.md`
- Local original, proxy, project, and operator result remain ignored beneath
  `verified_local_evidence_input_pilot/local_outputs/`.

## Product Boundaries

- Machine-valid media is not human visual/editorial acceptance.
- The proxy is a review convenience, not the production master.
- External editorial input, real-media replacement, creative polish,
  rights/legal approval, final-thumbnail approval, production carrier approval,
  upload/publication, and default-branch integration remain separate decisions.
- Full-suite Integrity work remains outside this focused milestone.

## Maintenance Note

Replace this file as the current capsule. Keep history in
`docs/project-context.md` and Git. Keep this file within 160 lines and run the
explicit state-sync checker after any shared-field change.
