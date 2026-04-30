# Visual Return Analysis Consistency Audit — 2026-04-29

## Purpose

User provided an external analysis claiming that NLMYTGen is stuck because human visual work in YMM4 does not return to AI-readable assets. This audit checks that claim against the current repo state and converts the useful part into a bounded plan.

## Verdict

- The core diagnosis is useful: visual work must come back as machine-readable assets, not only as a human impression.
- Several concrete premises in the analysis are stale. `delivery_nod_v1` is no longer the open frontier; it was accepted, promoted to `direct_proven`, and the repo-tracked source now contains all five v1 templates.
- G-24 is no longer only a preflight/audit lane. It has template-source resolution, analyzed placement, `.ymmp` write/readback, GUI exposure, and compact-review artifact generation.
- The remaining problem is narrower: creative acceptance and reuse records are still route-specific. G-24 has a strong return path; thumbnail/template, diagram, mood/background, and overlay-style work do not yet share one generic visual return contract.

## Current Facts

| Area | Current repo state | Meaning |
| --- | --- | --- |
| G-24 skit_group | `samples/templates/skit_group/delivery_v1_templates.ymmp` contains the v1 planned set 5/5; `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` and `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp` exist | Human template authoring is already captured as repo-tracked template source and reusable registry/placement input |
| G-24 acceptance | Machine readback passed for inserted GroupItems / assets / path form; compact review still needs YMM4 creative acceptance | Mechanical return is closed; visual judgement remains intentionally human |
| Thumbnail | `audit-thumbnail-template` / `patch-thumbnail-template` exist and saved-file readback is implemented; `_tmp/thumbnail/real_template.ymmp` is missing in this workspace | Return path exists in code, but real template proof is not closed |
| Session manifest | `build-session-manifest` bundles CSV / diagnostics / IR / apply result / patched `.ymmp` / manual acceptance placeholders | Production handoff exists, but it is not a generic visual memory layer |
| B-17 | Measured/font-scale paths exist; paired YMM4 evidence is drift-triggered only | Not a current visual-return blocker |

## Consistency With Previous Plan

The previous plan said:

1. Primary: close the real thumbnail template proof.
2. Secondary: take G-24 compact-review creative acceptance.
3. Maintenance: B-18 / H-01-H-02 / B-17 drift-only.

This remains correct. The external analysis does not justify replacing the current `next_action` with a broad new `visual_return_manifest` implementation. It does justify tightening the reporting rule: every human visual acceptance must name the owner artifact, the machine-readable return artifact, and the next reuse point.

## Useful Translation of "Visual Return Contract"

Do not start by adding a broad new feature. Use existing route-specific contracts first:

| Route | Return artifact now | Reuse point | Missing only if repeated pain appears |
| --- | --- | --- | --- |
| `skit_group` | template source `.ymmp`, registry, analyzed placement readback, compact-review acceptance note | `apply-production --skit-group-template-source` / GUI production tab | Generic cross-route visual return JSON |
| thumbnail | copied `.ymmp` with `thumb.*` Remarks, patch JSON, `file_readback`, YMM4 acceptance note | `patch-thumbnail-template` and `thumbnail_design` companion artifact | Real template proof and optional history/rotation warning |
| overlay / diagram / mood | map JSON / image path / cue or diagram packet | `overlay_map`, `bg_map`, cue/diagram packet | Asset affordance metadata only after concrete reuse cases |

## Effective Response

1. Keep `next_action` concrete: prepare one real thumbnail template copy, audit it, patch it, and capture `file_readback`.
2. Keep G-24 acceptance concrete: view the compact-review `.ymmp`; if NG, return to analyzer/placement normalization rather than asking for hand placement.
3. Use `build-session-manifest` as the current production-level return sheet instead of inventing a second broad handoff file immediately.
4. When a visual result is accepted, record:
   - source artifact path
   - returned machine-readable artifact path
   - route (`skit_group`, `thumbnail`, `overlay`, `diagram`, `mood_bg`)
   - status (`PASS`, `NEEDS_REPLAN`, `FAIL`)
   - failure tags or reuse note
5. Consider a dedicated `visual_return_manifest` only after at least two routes need the same repeated fields and existing route-specific artifacts become awkward.

## What Not To Do

- Do not reopen `delivery_nod_v1`; it is historical and superseded.
- Do not add new skit motions merely to prove progress.
- Do not make Python generate images, compose thumbnails, or emulate YMM4.
- Do not treat visual proof as a repeated mechanical gate. Use readback for mechanical checks and YMM4 only for creative acceptance.
- Do not turn "Visual Return Contract" into a new planning-only layer before the real thumbnail proof and G-24 compact review are closed.

## Immediate Plan

1. Close thumbnail real-template proof.
2. Close or record G-24 compact-review creative acceptance.
3. Use `build-session-manifest` for the next production pass.
4. If accepted visual decisions start repeating across routes, then split a thin, route-agnostic visual return contract into `FEATURE_REGISTRY` as an approved subtask before code changes.
