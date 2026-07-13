# Runtime State — NLMYTGen

Project-State-ID: new-banknote-yymm4-import-observed-visual-decision-ready-v1
State-Revision: 2026-07-14.1
Updated: 2026-07-14 JST
Product-State: new-banknote-yymm4-import-observed-visual-direction-review-ready
Product-Gate: human-visual-direction-selection
Recommended-Next: select-new-banknote-visual-direction
External-State: public-repo-feature-branch

## Current Slice

- **Manual import structurally observed**: the ignored operator result reports
  success with zero failed checks and an operator-confirmed absence of
  mapping/error/update/character mismatch. Independent headless parsing of the
  immutable local project verifies 9 VoiceItems, Reimu 3 / Marisa 6, exact
  character/text order, missing 0, duplicate 0, and no unexpected item.
- **Actual timing captured**: the imported project is 60 fps, 4415 frames, and
  73.583333 seconds. Per-cue frame/length evidence is tracked as informational
  timing and does not become a fixed production timing contract.
- **Local evidence remains local**: project SHA-256 is
  beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54;
  operator-result SHA-256 is
  e4ecb1bf5e4b5780990a00094804dd871d66068a917000015f9fecfd83e8ddfa.
  The project, result, batch state, embedded path, and executable path remain
  ignored and byte-preserved. Tracked receipts use repo-relative identities.
- **Approved identity unchanged**: all six approved script/CSV/traceability
  hashes remain frozen. The contract is 9 cues, scenes 2/4/3, canonical and
  YMM4 speakers 3/6, and zero unsupported spoken claims.
- **Visual decision packet ready**: exactly three routes are available. Route A
  Security Inspection Lab is RECOMMENDED; Route B Everyday Verification and
  Route C Design Evolution remain compact alternatives. Recommended does not
  mean selected, approved, implemented, or rights-cleared.
- **Route A scene spine complete**: all nine cues map once into S1 question and
  overview, S2 four-technique inspection, and S3 identification plus the final
  透かす / 触る / 傾ける / ルーペで見る sequence. Every cue retains claim/source
  anchors, actual VoiceItem timing, factual limits, placeholder, future rights
  decision, and expected YMM4 item family.
- **Review surface bounded**: the self-contained HTML board uses system fonts,
  CSS geometry, repo-relative links, and no external assets, scripts, URLs, or
  private paths. The review sheet asks only four human questions.

## Product Position

- The verified NotebookLM-to-script-to-CSV chain has now reached one real,
  structurally successful YMM4 import without speaker repair or content drift.
- H0 creates evidence and a human decision surface only. It is not production
  value, a selected visual route, a YMM4 visual project, a render, or creative
  acceptance.
- Route A has the strongest explanatory fit and lowest asset/rights burden
  because it uses original abstract diagrams for the four source-backed checks.

## Exact Next Action

Review
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/visual_scene_decision/visual_direction_board.html`
and return A, B, or C. Also answer whether the S1/S2/S3 flow fits, whether any
diagram could mislead viewers, and whether the motion proposal is restrained.
A cue ID or scene ID may be supplied instead of a route when revision is needed.

## Evidence and Access

- Import review:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_YMM4_IMPORT_OBSERVATION.md`
- Sanitized receipt/readback:
  `yymm4_import_observation_receipt.json` and
  `yymm4_import_observation_readback.json` beside that README.
- Visual review:
  `visual_scene_decision/README_VISUAL_SCENE_DECISION.md`,
  `visual_direction_board.html`, and `visual_review_sheet.md`.
- Machine plans:
  three-route options, recommended direction, script beat IR, scene layout,
  motion beats, asset/rights matrix, and the not-authorized YMM4 contract live
  in `visual_scene_decision/`.

## Active Boundaries

- No YMM4 launch, Computer Use, screenshot, image generation, external fetch,
  asset download, visual project, render, media, production, rights approval,
  publication, upload, or master integration occurred in this slice.
- All proposed banknote visuals are original abstract schematic geometry. They
  must not reproduce recognizable portraits, serials, seals, full-note layouts,
  real security textures, or repeatable exact placement/detail.
- Audio rhythm, pronunciation, subtitle readability, and visual effectiveness
  remain human judgments. Structural import success does not imply them.

## Retained Review Debt

| Debt | Impact | Owner | Revisit trigger |
| --- | --- | --- | --- |
| Human audio/rhythm/terminology review | Blocks editorial acceptance beyond structural import proof | human editorial reviewer | after route selection or before diagnostic-project acceptance |
| Human visual-direction choice | Blocks any selected-route implementation | human visual reviewer | current A/B/C review |
| S04/S05 provenance precision | Leaves historical binary/source identity incomplete without weakening adopted claim support | source provenance reviewer | stable S04 identity or exact S05 original becomes available |
| Cross-machine local `.ymmp` portability | Prevents treating the ignored imported project as a portable production base | YMM4 integration owner | before moving a selected-route diagnostic project to another machine |

## Maintenance Note

Keep this capsule within 160 lines. Durable evidence belongs in the tracked
receipts, plans, tests, and Git history; local project/result data stays ignored.
