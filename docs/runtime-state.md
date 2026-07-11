# Runtime State — NLMYTGen

Project-State-ID: episode-002-ymm4-diagnostic-placeholder-proof-observed-v1
State-Revision: 2026-07-11.2
Updated: 2026-07-11 JST
Product-State: episode-002-ymm4-diagnostic-placeholder-proof-observed
Product-Gate: supervisor-next-slice-decision
Recommended-Next: decide-real-input-or-integration
External-State: public-repo-feature-branch

## Current Slice

- **CSV gate passed**: the recovered unsaved project matched the authorized
  discard target. A clean YMM4 `4.53.0.9` import of the derived CSV opened no
  mapping dialog and produced nine ordered `VoiceItem`s with linked subtitles:
  `ゆっくり霊夢` 3 and `ゆっくり魔理沙` 6.
- **Observed timing recorded**: text and cue order remained intact. YMM4
  recalculated the timeline to 2790 frames / 46.50 seconds at 60 fps; exact
  duration variance is informational rather than a gate failure.
- **Separate diagnostic gate passed**: the generated diagnostic project was
  reopened in YMM4 without an unexpected dialog. It preserved the nine
  `VoiceItem`s and linked subtitles and exposed three `ImageItem`s, three
  independent `TextItem`s, and readable S1 / S2 / S3 non-final labels.
- **Portable evidence retained**: the local `.ymmp` files are ignored because
  YMM4 stores an absolute asset reference. The deterministic generator,
  placeholder PNG, manifest, machine readback, and GUI receipt are tracked.
- **Historical inputs preserved**: the canonical CSV remains at SHA-256
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`;
  the derived CSV remains at
  `5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC`;
  the 2026-07-10 historical receipt remains byte-identical at
  `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`.

## Product Position

- Automatic character binding is now observed for the explicit
  `ymm4_4_53_0_9_yukkuri_characters_ja_v1` profile. This is environment-specific
  evidence, not a universal YMM4 default claim.
- The CSV gate still owns only `VoiceItem` plus linked-subtitle import. The
  `ImageItem` and independent `TextItem` placeholders were proven through the
  separately authorized diagnostic-project route.
- The tracked proof pack records deterministic structure and hashes; its GUI
  receipt records the actual YMM4 reopen observation. A screenshot was not
  captured and was not a required gate.
- No render/export, production `.ymmp`, real-input replacement, rights/public
  approval, final-thumbnail approval, upload, publication, or default-branch
  integration occurred.

## Current Decision Menu

| Entry | Resolves | What becomes possible |
| --- | --- | --- |
| **Advance** | The proof still uses a diagnostic sample | After verified source/transcript, provenance and rights context, stable identity, and cue alignment are supplied, validate a real-input replacement |
| **Integrate** | The feature branch is not reconciled with the default branch | Audit the then-current feature/default diff and choose a safe integration path without implying production acceptance |

Neither route starts automatically. The next state change requires a supervisor
choice between real-input work and integration review.

## Human or External Decision Points

- **Real-input route**: verified source/transcript, provenance and rights note,
  stable identity, and cue alignment remain required before replacement.
- **Integration route**: remeasure the feature/default branch relationship and
  explicitly select the integration path; this slice did not merge or rebase.

## Product Boundaries

- Diagnostic placeholder proof is observed, but it is explicitly non-final and
  non-public. It does not authorize creative polish or production assets.
- Ignored local `.ymmp` files are same-machine evidence, not portable tracked
  deliverables. Reproduction must use the tracked generator and evidence pack.
- Do not infer render/export, production `.ymmp`, real input, rights/public/final
  thumbnail approval, upload, publication, or default-branch integration.
- Compact state files and task routing remain navigation surfaces, not a
  repository-side session prompt or Worker control plane.

## Maintenance Note

Replace this file as the current capsule. Keep historical decisions in
`docs/project-context.md`, dated verification artifacts, and Git history. Update
`docs/PROJECT_COCKPIT.md` with the same shared fields and run the explicit state
checker when those fields change.
