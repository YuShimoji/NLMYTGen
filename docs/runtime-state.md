# Runtime State — NLMYTGen

# BLOCK SUMMARY のたびに更新する。

# compact 後の再アンカリングではこのファイルを読む。

## 現在位置

### Session Handoff (2026-04-23)

- **G-25 YMM4 property-based variation probe (2026-04-29 / openability fixed 2026-04-30)**: Implemented `probe-ymmp-variations` as an isolated successor-lane probe for manual YMM4 acting clips. It reads non-variation `Remark` clips from Group/Image/Text/Shape items, reports patchable `X/Y/Zoom/Rotation`, observed flip routes, and `VideoEffects` stack fingerprints, and emits conservative variation candidates. With `-o`, review output now requires a YMM4-saved full project canvas when the probe source is a template/stub; pass `--review-seed` so source templates stay extraction-only and the output preserves YMM4 timeline/root metadata. Review clips use `variation:<source_remark>:<variant_id>` remarks; the probe does not connect to G-24 production placement automatically, does not zero-generate `.ymmp`, and does not synthesize images/effect types. Current proof: `samples/templates/skit_group/delivery_v1_templates.ymmp` + `samples/canonical.ymmp` review seed -> `_tmp/variation/delivery_v1_representative_review.ymmp` (17 representative candidates / 67 item insertions).
- **G-25 creative acceptance result (2026-04-30)**: User confirmed the regenerated review opens in YMM4, but the generated animation variants are not usable. `nudge / scale / rotate / effect_reuse` are property variations, not meaningful motion variations; manual combinations of nod / exit / hop / tilt produce drift such as wrong tilt direction, exiting while tilted, and hopping while tilted. G-25 remains done only as a route/openability/property probe and must not feed production placement. Successor is G-26 motion primitive grammar / compatibility probe. Proof note: `docs/verification/G25-animation-variation-acceptance-2026-04-30.md`.
- **Contaminated-patch boundary unblocking (2026-04-29)**: Reframed B-10/C-02/C-04/C-05/D-01/E-02/F-03 so old rejected/hold entries block unsafe methods, not the production goals. New terms are fixed in `FEATURE_REGISTRY.md`: `method-rejected` (old method rejected), `goal-allowed` (same goal may proceed through approved boundaries), and `successor-lane` (a safer successor artifact/route). Practical effect: old `--emit-meta`, Python image generation, `.ymmp` zero-generation, YMM4 GUI万能制御, and Python YMM4 preview remain blocked; diagnostic JSON / IR / manifest / packaging brief, G-24 template-source placement, H-02 thumbnail `thumb.*` slot patch, and future H-01/H-02-based metadata drafts are not blocked by the old pollution cleanup.
- **External visual-return analysis consistency audit (2026-04-29)**: Checked the pasted "Visual Return Contract" analysis against the current repo. Its core diagnosis is useful — human visual work must return as machine-readable assets — but its `delivery_nod_v1` premise is stale: G-24 v1 is 5/5 in the repo-tracked template source, analyzed placement and GUI connection exist, and the open G-24 item is compact-review creative acceptance. Added [VISUAL-RETURN-ANALYSIS-CONSISTENCY-2026-04-29.md](verification/VISUAL-RETURN-ANALYSIS-CONSISTENCY-2026-04-29.md). Effective response: do not open a broad new `visual_return_manifest` now; close the concrete thumbnail real-template proof and G-24 compact review first, using existing registry/readback/session-manifest paths as the return contract.
- **Follow-up worklog verification / B-17 measured reflow test hardening (2026-04-28)**: Verified the second pasted analysis against the repo. `impl_file_count` drift was real (`src/**/*.py = 35`), while `test_file_count` remained 31. Added direct tests for `reflow_subtitles_measured()` covering short passthrough, measured-width wrapping, and punctuation/single-character-line safety, plus a CLI WPF-backend smoke test using a fake helper executable. `build-csv --format json` now includes `measure_exe` in `overflow_params` when WPF measurement is used. This does not close YMM4 visual paired evidence; it closes the local code-path verification gap.
- **Worklog consistency audit / stale boundary correction (2026-04-28)**: Audited the pasted work logs against the current worktree. The earlier risks around large unstaged changes and stale test counters are now resolved: the branch is clean, recent work is split into commits, and collected tests are `31 files / 419 tests`. Found and corrected one remaining blind spot in this file: the older "Python text-only / `.ymmp` operation prohibited" section and 2026-04-06 workflow coverage table conflicted with the current allowed `patch-ymmp` boundary. Updated the wording to distinguish prohibited zero-from-scratch `.ymmp` / YMM4 production emulation from allowed limited post-import `.ymmp` patching.
- **Thumbnail real-template acceptance readback (2026-04-28)**: Implemented the missing machine readback step for the thumbnail real-template lane. `patch-thumbnail-template` now verifies patched in-memory values and, when `-o/--output` is used, reloads the written `.ymmp` and returns `file_readback` checks for text, image path, color, and X/Y/Zoom/Rotation values. `_tmp/thumbnail/patch_smoke.json` was prepared with a Windows-readable sample image path, but `_tmp/thumbnail/real_template.ymmp` is not present in this workspace yet, so real YMM4 visual acceptance remains pending.
- **Thumbnail template slot audit / limited patch v1 (2026-04-28)**: Corrected the prior thumbnail drift from docs-only planning to working `.ymmp` slot tooling. Added `audit-thumbnail-template` and `patch-thumbnail-template` with implementation in `src/pipeline/thumbnail_template.py`. Contract: humans duplicate/rough-place a YMM4 thumbnail template and mark existing items with `Remark=thumb.text.<id>` or `Remark=thumb.image.<id>`; the CLI can then audit patchable fields and patch text, ImageItem `FilePath`, existing color route, and X/Y/Zoom/Rotation first values into a copied `.ymmp`. Repo scan still found no real thumbnail `.ymmp` template, so real YMM4 visual acceptance remains open; `samples/canonical.ymmp` correctly fails audit with `THUMB_TEMPLATE_NO_SLOTS`.
- **B-17 measured-width subtitle reflow (2026-04-28)**: Addressed the remaining YMM4/display-width gap by adding an opt-in measured reflow path for `build-csv`. New CLI options: `--wrap-px`, `--wrap-safety`, `--measure-backend eaw|wpf`, `--font-family`, `--font-size`, `--letter-spacing`, and `--measure-exe`. `src/pipeline/text_measure.py` keeps the legacy East Asian Width model as fallback and adds a WPF-backed measurer; `tools/MeasureTextWpf` contains the Windows helper source. The GUI CSV tab now exposes Wrap Width / Measure Backend / font fields, and stats reports measured wrap params. This shifts B-17 from pure character-count approximation toward YMM4 display-condition-based wrapping while still requiring YMM4-side auto-wrap to be OFF or wide enough to avoid double wrapping.
- **Non-thumbnail workflow ambiguity cleanup (2026-04-28)**: Implemented the requested docs-only cleanup for non-thumbnail workflow boundaries. `S6-production-memo-prompt.md` now treats C-07 v4 as main-video Production IR only and keeps thumbnail copy/design in the S-8/H-02 lane. `VISUAL_STYLE_PRESETS.md` and `VISUAL_EFFECT_SELECTION_GUIDE.md` now reflect current G-15〜G-18 / G-24 adapter capabilities instead of older "not written" language. `WORKFLOW.md`, `OPERATOR_WORKFLOW.md`, `INVARIANTS.md`, `AUTOMATION_BOUNDARY.md`, and `GUI_MINIMUM_PATH.md` now distinguish Writer IR capability, adapter write capability, GUI-exposed inputs, and YMM4 creative acceptance. No GUI implementation was added; overlay/se/motion map UI remains a future GUI-completion task if production requires it.
- **Production session manifest / handoff sheet v1 (2026-04-28)**: Implemented `build-session-manifest` as the CLI artifact that bundles S-3 CSV, B-18 diagnostics, S-6 IR validation/apply results, YMM4 manual acceptance placeholders, and sibling `thumbnail_design` records into one JSON/Markdown handoff. The implementation lives in `src/pipeline/session_manifest.py`; `thumbnail_design` is recorded only and is not passed to `validate-ir` / `apply-production`. v1 deliberately does not add GUI buttons, YMM4 thumbnail `.ymmp` generation, YMM4 operation, or image generation.
- **B-17 YMM4 subtitle font source auto inference (2026-04-28)**: Extended subtitle reflow compensation so the CSV generation step now explicitly asks for either a manual `Subtitle Font Scale (%)` or a `YMM4 Subtitle Font Source` `.ymmp`. `build-csv` accepts `--subtitle-font-source-ymmp PATH` and infers `subtitle_font_scale` from YMM4 subtitle `FontSize` using `FontSize=45` as the default 100% baseline; `--subtitle-base-font-size N` can change that baseline. Multiple font-size candidates use the maximum value as a safety-side wrap width correction. This still is not pixel/layout calibration, but it closes the missing workflow step where font-size spec had to be considered before generating wrapped subtitles.
- **Thumbnail generation boundary clarification (2026-04-28)**: User asked whether prior thumbnail-generation specs were vague/nonexistent around AI generation timing and separation from script/Production IR. Clarified that existing H-01/H-02/H-05/one-sheet specs covered promise, copy strategy, visual direction, manual scoring, and YMM4 manual production, but did not clearly define the artifact boundary. Updated `THUMBNAIL_STRATEGY_SPEC.md`, `THUMBNAIL_ONE_SHEET_WORKFLOW.md`, `S8-thumbnail-copy-prompt.md`, and the 2026-04-28 thumbnail/workflow audits: `thumbnail_design` is a sibling artifact under H-01, may be generated in the same AI session as script refinement and Production IR, but must not be embedded in the script body or Production IR and must not be passed to `apply-production`. YMM4 thumbnail `.ymmp` generation/slot patch remains a future template-audit lane.
- **B-17 subtitle font scale reflow compensation (2026-04-28)**: Implemented lightweight font-scale compensation for subtitle wrapping. `build-csv` now accepts `--subtitle-font-scale PERCENT`, keeps `100` as the legacy behavior, and uses `effective_chars_per_line = floor(chars_per_line * 100 / PERCENT)` for `reflow_subtitles_v2`, `split_long_utterances`, and overflow stats. The GUI CSV tab now exposes `Subtitle Font Scale (%)`, and JSON stats reports `chars_per_line` / `subtitle_font_scale` / `effective_chars_per_line`. This is a simple scale correction to reduce YMM4 font-enlargement one-character pushout, not YMM4 pixel measurement or template-specific calibration.
- **User workflow rewiring audit (2026-04-28)**: User asked assistant to own workflow optimization because the GUI is usable but the total production path remains long, and recent YMM4 timeline acting work mixed production, development, and research concerns. Added [USER-WORKFLOW-REWIRING-AUDIT-2026-04-28.md](verification/USER-WORKFLOW-REWIRING-AUDIT-2026-04-28.md). Current reading: keep G-24 production acceptance as the main lane, treat B-17/YMM4 width as maintenance paired-evidence work, keep thumbnail design as a sibling `thumbnail_design` lane under H-01/H-02, and separate YMM4 timeline "acting creation" into production placement / template authoring / adapter hardening / route research. Recommended next development candidate is a production session manifest / handoff sheet before adding more effects.
- **Thumbnail variation / IR planning audit (2026-04-28)**: User clarified the basic line: humans duplicate a YMM4 thumbnail template and replace text / standing pictures / background, but the project still needs a plan for per-video variation, fine placement/color adjustments, and whether thumbnail design should be requested alongside script/production IR. Added [THUMBNAIL-VARIATION-AND-IR-PLAN-2026-04-28.md](verification/THUMBNAIL-VARIATION-AND-IR-PLAN-2026-04-28.md) and linked it from the capability audit. Decision: keep thumbnail design as a sibling `thumbnail_design` companion JSON under H-01/H-02, not as fields inside Production IR Micro entries. Safe development path is YMM4 thumbnail template slot contract -> read-only audit -> limited text/color/geometry patch -> image slot replacement -> variation history warnings. Current blocker is absence of a repo-tracked thumbnail `.ymmp` template with `thumb.*` slot Remarks.
- **B-17 one-character subtitle tail analysis (2026-04-28)**: User reported frequent one-character subtitle wraps and asked for ownership. Added [B17-one-character-tail-analysis-2026-04-28.md](verification/B17-one-character-tail-analysis-2026-04-28.md). Root cause is not “B-17 absent” but missing accompaniment around it: GUI defaults had drifted to `Chars/Line=20` while CLI/docs standard is display width `40`; YMM4 actual subtitle width is still uncalibrated against `display_width`; and `--stats` does not separately surface one-character tail risk. Local measurement on `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv` found 0 explicit one-character CSV lines, but at assumed actual cap 40 there are 10 one-character-tail risks and at cap 38 there are 35. Fixed GUI/default docs to standard `2 / 40` and tightened the regression test so a full-width single-character line is not accepted by display-width math alone.
- **G-24 user workflow optimization / GUI connection (2026-04-28)**: Took ownership of the current user-workflow bottleneck around skit_group placement. G-24 analyzed placement itself was already implemented; the remaining workflow gap was that production operators still had to drop to CLI to pass `--skit-group-registry`, `--skit-group-template-source`, `--skit-group-only`, and strict intent validation. The Electron production tab now exposes Skit Group Registry / Template Source selectors, strict skit_group intent validation, and a skit_group-only mode that intentionally omits CSV(row-range) because it uses aligned IR anchors. `apply-production` now accepts optional `--strict-skit-group-intents` and enforces it even in skit_group-only mode. Docs now split skit_group work into production / development / research lanes and keep YMM4 composition acceptance separate from machine readback.
- **Thumbnail generation capability audit (2026-04-28)**: User asked assistant to take ownership of the thumbnail-generation area and first investigate current capability. Added [THUMBNAIL-GENERATION-CAPABILITY-AUDIT-2026-04-28.md](verification/THUMBNAIL-GENERATION-CAPABILITY-AUDIT-2026-04-28.md). Current repo capability is judgment support / workflow / manual score aggregation only: H-01 brief template, C-08/H-02 copy strategy, H-03/H-04 diagnostics, H-05 `score-thumbnail-s8`, and YMM4 one-sheet workflow. There is no repo-tracked thumbnail `.ymmp` template/source/slot registry, no image generation/composition, no image analysis, and no GUI H-05 button. All 15 `samples/*thumb*.png` files checked share the same SHA256, so they are continuity anchors rather than a diverse production corpus. A safe next development lane is thumbnail template slot audit/registry for YMM4 template replacement, not Python image generation.
- **G-24 template-analyzed placement planner implementation (2026-04-28)**: Implemented analyzed skit_group placement in `src/pipeline/skit_group_placement.py`. The placement path now derives a canonical rest pose from template-source GroupItem transform medians, shifts each cloned GroupItem `X` / `Y` / `Zoom` value list from template-local baseline to that rest pose, preserves relative motion deltas / child ImageItem offsets / timing, and fails fast with `SKIT_TEMPLATE_ANALYSIS_INSUFFICIENT` when numeric transform facts are missing. Follow-up correction after visual feedback: ImageItem `FilePath` now writes YMM4-readable Windows paths instead of WSL `/mnt/c/...`, and `--skit-group-compact-review` generates a non-scattered visual review artifact. Regenerated `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` and added `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp`; both read back as 9 GroupItems / 10 ImageItems / 0 missing assets / 0 POSIX asset paths. Compact review frames are 0 / 240 / 480 / 720 / 960 for the five cues.
- **remote sync / local readiness check (2026-04-28)**: Fetched `origin`, created local tracking branch `codex/g24-nod-sync-adoption` from `origin/codex/g24-nod-sync-adoption`, and kept the next frontier on G-24 template-analyzed placement. Local validation initially exposed a WSL/Windows-path-sensitive assertion in `tests/test_skit_group_placement.py`; the test now uses the same repo asset resolver as `skit_group_placement.py` instead of raw `Path(FilePath).exists()`. This is a test portability fix only and does not change production placement behavior.
- **G-24 skit_group placement automation direction correction (2026-04-27/28)**: Re-centered G-24 on `.ymmp` write capability instead of operator hand placement. Added `src/pipeline/skit_group_placement.py`, `patch-ymmp/apply-production --skit-group-template-source`, `validate-ir --strict-skit-group-intents`, repo-tracked template source `samples/templates/skit_group/delivery_v1_templates.ymmp`, and fixture `samples/_probe/g24/skit_group_placement_base.ymmp`. After the user saved `samples/nod.ymmp` with a nod-only animation and `Remark=nod`, the repo-tracked source now contains all five v1 templates including normalized `delivery_nod_v1`; future missing templates must still fail fast with `SKIT_TEMPLATE_SOURCE_MISSING`. The previous real-estate packet is retained as history only; operator hand placement is not production automation.
- **G-24 real estate DX YMM4 production packet (2026-04-27)**: Added [G24-real-estate-dx-ymm4-production-packet-2026-04-27.md](verification/G24-real-estate-dx-ymm4-production-packet-2026-04-27.md) to turn the validated CSV / skit_group IR into an operator-ready S-4 / S-6 packet. The packet fixes the open target as a copied production YMM4 template project, the source CSV as `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv`, and the skit_group cue table as IR indexes 1 / 15 / 35 / 39 / 104 / 143. It keeps `panic_shake` as `manual_note`, treats the 18 CSV overflow candidates as B-17 residue only if visible in YMM4, and does not add new CLI, motion authoring, registry alias, or `.ymmp` generation.
- **G-24 real estate DX skit_group IR validation (2026-04-27)**: Accepted the corrected NotebookLM-derived real estate DX script as the case input, saved `samples/不動産DX_魔法の鍵とキュレーション.txt`, built `samples/不動産DX_魔法の鍵とキュレーション_ymm4.csv` (352 rows), and generated `samples/不動産DX_魔法の鍵とキュレーション_skit_group_ir.json`. `audit-skit-group` against `samples/canonical.ymmp` returned `exact=3 / fallback=2 / manual_note=1`; `panic_shake` is the only manual_note. Added [G24-real-estate-dx-skit-group-ir-validation-2026-04-27.md](verification/G24-real-estate-dx-skit-group-ir-validation-2026-04-27.md). Also recorded that NotebookLM text is low-trust and must pass B-18/C-09/manual QC before CSV/IR.
- **G-24 production IR generation flow sync (2026-04-27)**: Reflected the passed minimal production IR shape into `docs/S6-production-memo-prompt.md`, `docs/PRODUCTION_IR_SPEC.md`, `docs/SKIT_GROUP_TEMPLATE_SPEC.md`, and `docs/WORKFLOW.md`. Real skit_group actor utterances must include `motion_target: "layer:9"` and use exact v1 intents or registered alias intents; `panic_shake` remains the manual/unresolved candidate. Re-ran `audit-skit-group` on `samples/g24_skit_group_minimal_production_ir.json`: `exact=3 / fallback=2 / manual_note=1`. Added [G24-production-ir-generation-flow-sync-2026-04-27.md](verification/G24-production-ir-generation-flow-sync-2026-04-27.md). No additional repo IR exploration or motion authoring.
- **G-24 minimal production IR validation (2026-04-27)**: Added `samples/g24_skit_group_minimal_production_ir.json` as the minimum production-oriented skit_group IR input because repo-local production-ish IRs do not target the canonical skit_group layer. Validated it with `audit-skit-group samples/canonical.ymmp ... --skit-group-registry samples/registry_template/skit_group_registry.template.json --format text`: `exact=3 / fallback=2 / manual_note=1`. `surprise_jump` and `deny_shake` resolve via registry fallbacks; `panic_shake` remains `manual_note` / new-template candidate / IR wording avoidance option. Added [G24-minimal-production-ir-validation-2026-04-27.md](verification/G24-minimal-production-ir-validation-2026-04-27.md). No further repo IR broad search is needed.
- **G-24 real production candidate scan (2026-04-27)**: Searched repo-local IR candidates for alias-enabled `audit-skit-group` validation. Only probe IRs contain skit_group layer-9 targets; production-ish root samples audited against `samples/canonical.ymmp` all returned `exact=0 / fallback=0 / manual_note=0` because they contain no skit_group-targeted entries. Added [G24-real-production-candidate-scan-2026-04-27.md](verification/G24-real-production-candidate-scan-2026-04-27.md). This led to the minimum production IR input sample above; no new YMM4 motion authoring or registry mapping was opened.
- **G-24 alias registration PASS (2026-04-27)**: Registered safe production-like label fallbacks in `samples/registry_template/skit_group_registry.template.json`: `surprise_jump -> delivery_surprise_oneshot_v1` and `deny_shake -> delivery_deny_oneshot_v1`. `panic_shake` remains `manual_note` / new-template candidate. Validation after aliasing: IR A `exact=3 / fallback=0 / manual_note=1`; IR B `exact=1 / fallback=2 / manual_note=1`; focused tests `tests/test_capability_atlas.py tests/test_skit_group_audit.py` PASS. Added [G24-alias-registration-2026-04-27.md](verification/G24-alias-registration-2026-04-27.md). Next frontier is real production IR/corpus validation, not another planning-only report.
- **G-24 production-like gap classification PASS (2026-04-27)**: Ran `audit-skit-group` on `samples/canonical.ymmp` with `samples/_probe/b2/haitatsuin_ir_oneshot_block2.json` and `samples/_probe/b2/haitatsuin_ir_10utt_v3_motions.json`. Results: IR A `exact=3 / fallback=0 / manual_note=1`; IR B `exact=1 / fallback=0 / manual_note=3`. Covered intents: `enter_from_left`, `surprise_oneshot`, `deny_oneshot`, `nod`. Alias candidates: `surprise_jump -> surprise_oneshot`, `deny_shake -> deny_oneshot`. New-template/manual candidate: `panic_shake`. Added [G24-production-like-gap-classification-2026-04-27.md](verification/G24-production-like-gap-classification-2026-04-27.md). No registry, `src/`, template, or `.ymmp` changes were made for this classification pass.
- **G-24 repo-probe production-use validation PASS (2026-04-27)**: Ran `audit-skit-group` on `samples/canonical.ymmp` + `samples/_probe/skit_01/skit_01_ir.json` with `samples/registry_template/skit_group_registry.template.json`. Result: `exact=5 / fallback=0 / manual_note=0`; all 5 v1 intents resolve to `delivery_*_v1` templates. Added [G24-production-use-validation-report-2026-04-27.md](verification/G24-production-use-validation-report-2026-04-27.md). No confirmation `.ymmp` was generated, and `samples/haitatsuin_2026-04-12_g24_proof.ymmp` remains compact template/sample proof rather than validation input. Next frontier is applying the same validation shape to a real production IR / compatible production corpus.
- **G-24 v1 planned set completion sync (2026-04-27)**: User completed the remaining 2 samples (`delivery_deny_oneshot_v1` / `delivery_exit_left_v1`) and asked assistant to confirm and move forward. Repo inspection of `samples/haitatsuin_2026-04-12_g24_proof.ymmp` found plain body/face `ImageItem` children, Layer 9 `GroupItem` snippets with matching Remarks, and `TachieItem` count 0. `deny_oneshot` is represented as a short X-axis one-shot sway; `exit_left` uses OUT `InOutMoveEffect` leftward. `skit_group.intent.deny_oneshot` and `skit_group.intent.exit_left` are promoted to `direct_proven`, completing the v1 planned set. The proof `.ymmp` is now a compact template/sample proof rather than the earlier voice-anchored adoption corpus, so the next frontier is **production-use validation** with `samples/canonical.ymmp` + real/probe IR, not more motion authoring.
- **G-24 roadmap loop-stop correction (2026-04-27)**: User flagged that the current source of truth could imply endless “make another plausible motion” work and did not clearly answer what happens after a motion is authored. Canonical docs now state that planned author/export stops after `deny_oneshot` -> `exit_left`; after `exit_left`, the next move is production-use validation, where real IR resolves to exact / fallback / manual note and the result is judged by whether it reduces S-6（背景・演出設定）selection work. New skit motions are only re-opened when a concrete production gap appears.
- **G-24 role clarification (2026-04-27)**: User clarified the intended flow: user authors a small reusable motion set, then assistant uses those templates plus registry/know-how to generate or organize production-like samples, and user reviews the output. This is not a workflow where user manually creates every sample/template.
- **G-24 `delivery_nod_v1` PASS sync (2026-04-27)**: User reported that `delivery_nod_v1` was created, saved as a YMM4 native GroupItem template, and given the same Remark. User acceptance also confirmed body + face move together, the nod is visible but not scene-dominating, and no `TachieItem` is included. This closes the `nod` cautious gate and promotes `skit_group.intent.nod` to `direct_proven`; the next frontier was `deny_oneshot` followed by `exit_left`, later superseded by the v1 planned set completion sync above.
- **strong doc-excision follow-up (2026-04-27)**: A second deletion pass removed stale roadmap authority from the top of `docs/project-context.md` and deleted the old "copy into another thread" prompt block from `docs/verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md`. `CLAUDE.md` now aligns GUI/YMM4 with CLI artifact mode, and `AGENTS.md` now states that `runtime-state.md` `next_action` is the current frontier source while `project-context.md` is a targeted log. No production artifact, FEATURE status, or G-24 `next_action` changed.
- **next roadmap branch prep (2026-04-27)**: After the legacy-document cleanup and template-formalism correction, the next roadmap was fixed as a gate-shaped G-24 sequence: close `delivery_nod_v1` author/export first, promote `nod` only after user-owned PASS, then widen to `deny_oneshot -> exit_left`. `docs/project-context.md` recorded the formal-plan entry branches (未報告 / PASS / FAIL / 新規制作案件), and `docs/verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md` §2.3.1 mirrored the same pre-plan decision point. This state was superseded first by the `delivery_nod_v1` PASS sync, then by the v1 planned set completion sync above.
- **strong legacy-plan deletion (2026-04-27)**: Old core-dev, lane prompt, parallel prompt-hub, and visual-quality packet files were deleted instead of bannered. Current state must be recovered from `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then from `P02` / `PRE-PLAN` only when the current G-24 gate needs detail.
- **documentation pollution excision (2026-04-27)**: Resume-prompt authority was removed; `verification/` is now evidence storage rather than a current-canonical table; `USER_REQUEST_LEDGER.md` keeps only active durable requirements; date-fixed rule headings and old background-animation/S6 front-facing language were demoted. Current restart remains `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file.
- **restart read budget correction (2026-04-27)**: Normal restart no longer means reading every protected/canonical doc. The default path is `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> this file, then targeted sections only (`project-context` HANDOFF / DECISION LOG, FEATURE ID, invariant, ledger, workflow, interaction failure class, or AI gate as needed). Full re-anchoring is an exception for boundary uncertainty, drift, explicit REANCHOR / REFRESH / AUDIT, or failure to connect work from this file.
- **G-24 `delivery_nod_v1` implementation pass (2026-04-27)**: Assistant implemented the non-user-owned part of the plan by re-running readiness checks. At that historical point, `audit-skit-group` on both `samples/canonical.ymmp` and `samples/haitatsuin_2026-04-12_g24_proof.ymmp` stayed `exact=5 / fallback=0 / manual_note=0`. `apply-production --dry-run` on the proof corpus returned `success=true`, `motion_changes=8`, and `group_motion_changes=0` when run with `--tachie-motion-map samples/tachie_motion_map_library.json`. A dry-run without that motion map fails with `MOTION_UNKNOWN_LABEL`, so the motion map is part of the required readiness command. This was readiness-only before the later user-owned PASS sync; the current worktree proof `.ymmp` is now a compact template/sample proof.
- **template formalism correction (2026-04-27)**: Short return formats and prompt/checklist templates must not outrank task connectivity. For manual/shared actions, docs must first state the open target, created/modified artifact, source object, actor, owner artifact, acceptance meaning, and replan condition. `PASS` / `FAIL` / `OK` / `NG` is only the final result label, not a substitute for the operation.
- **roadmap pre-plan prep after legacy cleanup (2026-04-27)**: Updated the pre-plan intake docs away from the older background-animation/S6 axis and into the G-24 gate-shaped sequence. This was later advanced by the `delivery_nod_v1` PASS sync and then by the v1 planned set completion sync; the current anchor is production-use validation.
- **docs cleanup / interaction failure framing correction (2026-04-26)**: Obsolete prompts, archived packets, and superseded roadmap/setup docs were deleted; `docs/INTERACTION_NOTES.md` now uses structural failure classes (`REASK_DEBT`, `BROAD_STOP`, `OPTION_COLLAPSE`, `MANUAL_PROOF_TRANSFER`, `VALUE_PATH_DRIFT`, `STATUS_DRIFT`, `DOMAIN_PACKET_COLLAPSE`). The durable rule is that interaction notes must prevent project-stalling inefficiency rather than record personal reactions. Synced `docs/ai/CORE_RULESET.md` role wording and `docs/USER_REQUEST_LEDGER.md`.
- **nod cautious gate readiness + packet sync (2026-04-23 snapshot; superseded)**: Assistant reran `audit-skit-group` on `samples/canonical.ymmp` and `samples/haitatsuin_2026-04-12_g24_proof.ymmp`, confirmed that `delivery_nod_v1` stayed `exact`, and rechecked `apply-production --dry-run` with `success=true` / `group_motion_changes=0`. At that snapshot, the repo tracked only the canonical anchor plus the two starter copies (`delivery_enter_from_left_v1`, `delivery_surprise_oneshot_v1`) and did not yet track a discrete `delivery_nod_v1` source. This historical user-owned export step was superseded by the v1 completion sync and the 5/5 repo-tracked template source; do not use this entry as current `next_action`.
- **starter batch export sync（2026-04-21）**: G-24 の初回 authoring 範囲は `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` の 2 件に固定していた。`samples/canonical.ymmp` には frame 0 の canonical anchor `haitatsuin_delivery_main` に加え、frame 306 `delivery_enter_from_left_v1` と frame 658 `delivery_surprise_oneshot_v1` の GroupItem copy が追加済みで、各 group は Layer 9 / `GroupRange=2` / 隣接 Layer 10-11 の `ImageItem` ペアを維持する。加えて user report では、この 2 件を **名前そのまま・GroupItem template・ImageItem 2 点込み**で standalone native template library へ登録済み。assistant 側は registry / preflight / P02 / handoff をこの starter export 状態に同期済み。当時 `delivery_deny_oneshot_v1` / `delivery_exit_left_v1` / `delivery_nod_v1` は canonical corpus で exact を維持する catalog entry だったが、現在は v1 completion sync により全 5 件 `direct_proven`。
- **cautious gate all-pass (2026-04-21)**: The export order remains **manual acceptance -> 1 production adoption proof -> export**, and the starter batch still counts as PASS across all three steps. `audit-skit-group` stayed at `exact=5 / fallback=0 / manual_note=0`, and `apply-production --dry-run` stayed at `success=true` / `group_motion_changes=0`. Machine-readable `warnings[]` still shows only `bg label 'studio_blue' not found in bg_map`; CLI output also replays the known `FACE_PROMPT_PALETTE_EXTRA` / `FACE_LATENT_GAP` / `IDLE_FACE_MISSING` baseline warnings. These warnings remain non-fatal and do not change the starter-batch PASS state.
- **manual acceptance PASS（2026-04-21 user report）**: `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` の見え方確認は完了。`enter_from_left` は同テンプレ内に紛れていた退場設定を YMM4 上でカット済みで、repo-local inspection でも `InOutMoveFromOutsideFrameEffect` は `IsOutEffect=False`。2 件とも loop / body-face drift なし。
- **同期確認**: `git log -1 --oneline` が最新。**motion 軸別 one-shot + motion_target Remark** の実装コミットは **`396ea4b`**。続けて **引き継ぎ本文（本節）と `.gitignore`** を入れたコミットがその直後。**本ブロック完了後**は `git push origin master` でリモートと揃えること。
- **検証用 ymmp（再生成・`_tmp/` は gitignore）**: `skit` 系・B2 one-shot proof は verification 短文に記載のパスに合わせて再生成すること（具体パスは [B2-oneshot-library-v3-2026-04-19.md](verification/B2-oneshot-library-v3-2026-04-19.md)、[skit_01_delivery_dispute_v1_2026-04-19.md](verification/skit_01_delivery_dispute_v1_2026-04-19.md)）。
- **workflow breakage（2026-04-20 正本、2026-04-27 表現是正）**: `_tmp/skit_ManualSample_01.ymmp` / `_tmp/skit_01_v2.ymmp` はローカルに存在する場合があるが、gitignored / untracked の一時物であり active gate や比較基準にしない。`_tmp/skit_01_v2_verify.ymmp` も現作業ツリーでは存在を前提にしない。**新しい ManualSample 作成依頼は禁止**。比較・切り分けは [skit_01-workflow-breakage-audit-2026-04-20.md](verification/skit_01-workflow-breakage-audit-2026-04-20.md) + `python3 samples/_probe/skit_01/audit_skit_01_proof.py` で repo 内 tracked docs / sample / registry を優先する。
- **canonical anchor（2026-04-20 採用）**: `samples/canonical.ymmp` を haitatsuin canonical skit_group の official artifact として扱う。`haitatsuin_delivery_main` / Layer 9 / ImageItem-only / 左向き基準姿勢。正本 [G24-canonical-anchor-adoption-2026-04-20.md](verification/G24-canonical-anchor-adoption-2026-04-20.md)。
- **再開時**: segment / Group 確認は `inspect_v5_group_segments.py` 系。茶番 E2E 経路は既存 IR + `apply-production`（IR 例: `samples/_probe/skit_01/skit_01_ir.json`）。
- **既知メモ**: pan のみ区間で Remark が `motion:none utt:?` になりうる。camera pan の X と縦 one-shot が重なると画面上は斜めに見える可能性。`nod` は RepeatMove、`nod_oneshot` は未実装。
- **YMM 効果サンプル（共有参照）**: `samples/_probe/b2/effect_full_samples.json` をリポジトリに同梱する（作業環境の突き合わせ用）。motion プリセットの正本は引き続き `tachie_motion_map_library.json` / `EffectsSamples_*.ymmp` / [MOTION_PRESET_LIBRARY_SPEC.md](MOTION_PRESET_LIBRARY_SPEC.md)。

ドキュメント地図（任意）: [NAV.md](NAV.md) / Electron 最小経路・検証ラダー: [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md)（2026-04-14: balance-lines GUI 露出・ウィザード範囲明記）

- project: NLMYTGen
- git: **既定の開発ブランチは `master`**（2026-04-09: PR [#1](https://github.com/YuShimoji/NLMYTGen/pull/1) で `feat/phase2-motion-segmentation` をマージ済み。新規作業は `master` からブランチを切る）
- lane: **コア開発幹**（回帰・ドキュメント整合・承認済みバグ修正）。**主軸は本開発** — エージェント作業は未承認 FEATURE を増やさず上記に集中。オペレータ並行: Phase 1 Block-A (通過済、メンテ層の継続観測) / 主軸 (演出配置自動化の実戦投入) は runbook どおり。**レーン A（Phase 1）の repo 準備はオペレータ側でクローズ**（[OPERATOR_LANE_A_ENV.md](verification/OPERATOR_LANE_A_ENV.md)、[LANE_A_PREP_CHECKLIST.md](verification/LANE_A_PREP_CHECKLIST.md)）。**レーン D（H-01 brief）オペレータ完了・当面クローズ**（[H01-lane-d-prep-2026-04-09.md](verification/H01-lane-d-prep-2026-04-09.md) §6、2026-04-09）
- slice: **Thumbnail template slot patch v1 has saved-file readback; real thumbnail template acceptance is now the open thumbnail lane**. `audit-thumbnail-template` / `patch-thumbnail-template` can operate on copied YMM4 thumbnail templates with `thumb.text.*` / `thumb.image.*` Remark slots and `patch-thumbnail-template -o` now reports `file_readback`. `build-session-manifest` remains available for production handoff. G-24 compact-review acceptance remains open but is no longer the only immediate lane.
- next_action: **Primary — G-26 preflight / 仮contract検証**. Do not keep expanding G-25 `nudge / scale / rotate` candidates. Start from read-only route evidence, not implementation: confirm the paths for the four manual `.ymmp` motions (`うなずき` / `退場` / `小ジャンプ` / `傾き`), extract at least 2 and ideally 4 examples of `X` / `Y` / `Rotation` / `Zoom` / `IsFlipped` / `VideoEffects` / `Values`, then decide whether the grammar should be single-axis variant composition, motion primitives, or a hybrid of core primitive + modifier. `primitive_id`, `motion_role`, `start_pose`, `end_pose`, `dominant_channels`, `reset_policy`, `direction_semantics`, and compatibility/forbidden-after rules are initial candidates only and are finalized after route readback. Output should be a JSON compatibility report and small checklist before any new review `.ymmp`. Do not touch `LayerSettings` / `ymmp_openability.py`, do not generate `.ymmp` from Python, and do not connect G-25/G-26 to G-24 production placement. **Secondary lanes**: real thumbnail template slot patch remains available when operator time allows; G-24 production placement remains separate and must not consume G-25 variants.
  - **assistant (A)**: Keep Writer IR strict: skit_group actor utterances require `motion_target: "layer:9"` and registry v1/alias intents only; `panic_shake` is not normal Part 2 JSON vocabulary.
  - **assistant (B)**: Use `samples/templates/skit_group/delivery_v1_templates.ymmp` as the repo-tracked template source and analysis input. It now contains all five v1 templates; any future missing template must remain a fail-fast diagnostic, not a silent fallback.
  - **assistant (C)**: Treat `samples/_probe/g24/real_estate_dx_skit_group_compact_review.ymmp` as the current visual acceptance artifact. Treat `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` as the production-timing artifact. Do not ask the user to manually correct spacing in YMM4 unless readback shows a missing source fact.
  - **assistant (D)**: Run placement for IR indexes 1 / 15 / 35 / 39 / 143; keep index 104 out unless a new registered template exists.
  - **shared (E)**: Treat preflight/audit as diagnostics only. The acceptance signal is GroupItem insertion readback in the patched `.ymmp`.
  - **assistant (F)**: Treat "Visual Return Contract" as a useful cross-route abstraction, not the immediate implementation target. For now, record accepted visual work through existing route artifacts: skit_group registry/template source/readback, thumbnail `thumb.*` template readback, and `build-session-manifest` acceptance slots.
- parallel_replan_2026_04: **視覚最低限 + 改行／YMM4 ギャップ**の到達定義・チェックリスト・計測テンプレは [VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md)。`next_action` の主軸とは別軸の **並列オプション**。オペレータ時間の並列で、同文書の **トラック A（演出 IR 実戦 = 主軸の実務サブセット）** / **トラック B（改行ギャップ記録 = メンテ層 B-17 観測）** を配分する。汎用 Prompt ハブは削除済みなので、依頼時は作業対象・作成物・owner・acceptance を先に書き、必要な詳細手順だけを参照する。
- recommended_frontier_order: **G-24 茶番劇 Group template-first 運用** → 演出配置自動化の実戦投入 (P02) → 台本品質の継続観測 (メンテ) → 補助経路 (G-22 / PNG overlay) の必要最小限運用
  - **再開ショートカット（推奨対応）**: G-20 スライス1-2 完了（group_target バリデーション + `mode: relative`）は前提として維持。ただし主軸は `group_motion` の拡張ではなく、**canonical skit_group template → 派生 template 群 → production での template 解決**。
  - **G-24 の出口**: planned author/export は `deny_oneshot` → `exit_left` で止める。以後は実制作 IR に対して exact / fallback / manual note が S-6（背景・演出設定）の選択負荷を減らすかを見る。新しい小演出は production gap が出た時だけ再起票する。
  - **役割分担**: user は少数の reusable YMM4 native GroupItem template を作る。assistant はその組み合わせ・registry・fallback note で production-like sample / 解決結果を作り、user は確認に集中する。
  - **並列の読み**: 上記フロンティア順と別に、[VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md](verification/VISUAL-MINIMUM-AND-REFLOW-PLAN-2026-04.md) の **トラック A**（最小視覚 = 主軸の実務サブセット）と **トラック B**（B-17 済み L2 と YMM4 実表示のギャップ計測 = メンテ層観測）を **同時期に進めてよい**。先にオペレータ時間を取る軸は案件による（ユーザー合意で `next_action` 本文は変えず、配分のみ記録してよい）。
- 再現ルール: 異種サンプル 1 本で打ち切り済み。以後は新しい failure が出たときだけ追加検証
- operator/agent ガード: [REPO_LOCAL_RULES.md](REPO_LOCAL_RULES.md)（正本）+ `.claude/hooks/guardrails.py` で repo 外逸脱 / broad question 停止 / repeated visual proof を常設抑止（`.claude/CLAUDE.md` は入口ポインタ）
- 案件モード: CLI artifact

## 優先順位 (正本)

目的: 実制作の手間を減らすこと。未承認のコード機能は増やさない ([FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) 準拠)。順序を変える場合はユーザー合意で `next_action` と本節を更新する。

**判断基準**: 主軸は以下 4 条件をすべて満たす — ① 制作物の質に直接効く / ② 現在 bottleneck が顕在化 / ③ 着手しないと制作 workflow が詰まる / ④ 明確な完了の目安がある。据え置きは状態別に `hold` (再開条件あり) / `quarantined` (汚染バッチ由来) / `rejected` (廃止) に分ける。


| 層 | 内容 | 担い手 | 完了の目安 |
| --- | --- | --- | --- |
| **主軸 (唯一)** | **G-24 茶番劇 Group template-first 運用**: 配達員などの外部素材演者を `speaker_tachie` から分離し、**repo-tracked YMM4 template source → registry 解決 → analyzed placement plan → GUI/patch-ymmp による GroupItem 自動配置**に寄せる。正本 [SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) / [PRODUCTION_IR_CAPABILITY_MATRIX.md](PRODUCTION_IR_CAPABILITY_MATRIX.md) | user (少数の YMM4 template 作成 / acceptance) + assistant (registry / 仕様 / template-source 同期 / analyzer / placement planner / `.ymmp` placement 実装 / GUI 接続) | v1 planned set 5 件は `direct_proven`、repo-tracked source も 5/5 同梱済み。analyzed write/readback と GUI 接続は通った。次は compact review `.ymmp` の YMM4 visual acceptance |
| **メンテ (並行低負荷)** | ① **台本品質の継続観測 (B-18)** — Block-A 通過済、新台本は [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) に 1 行追記のみ。詳細手順 [B18](prompts/B18-script-diagnostics-observation-prompt.md)。② **Packaging brief / one-sheet (H-01/H-02)** — 新しい packaging brief が必要な案件でのみ起動。[PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md)、[THUMBNAIL_ONE_SHEET_WORKFLOW.md](THUMBNAIL_ONE_SHEET_WORKFLOW.md)、詳細手順 [H01](prompts/H01-packaging-brief-prompt.md) / [H02](prompts/H02-thumbnail-one-sheet-prompt.md)。③ **字幕 B-17 残差観測** — drift が見えた時だけ起動。詳細手順 [B17](prompts/B17-reflow-residue-observation-prompt.md) | オペレータ (GUI) / 別セッション assistant | 既定順は **B-18 → H-01/H-02 on demand → B-17 on drift**。verification 更新のみで回す |
| **hold (補助経路)** | **G-22 dual-rendering / PNG overlay**。背景キャラや一枚絵補助では有効だが、茶番劇演者の主軸ではない。必要時のみ使用 | user + assistant | skit_group template だけでは吸収できない案件で補助利用したとき |
| **hold (条件待ち)** | E-01 (YouTube 投稿自動化) / E-02 (旧 standalone YouTube メタデータ) — 自動投稿や本線注入は制作パイプと混ぜない。H-01/H-02 を入力にした metadata draft は successor-lane として再起票可 | — | integration point が明示されるまで |
| **汚染バッチ gate** | F-01 / F-02 は `quarantined`、D-02 は C-07 v3 吸収済み `hold`。いずれも個別再審査なしに backlog 化しない | — | 再審査・spec 化まで触らない |
| **rejected** | B-10 (旧 `--emit-meta`、撤去済) — method-rejected。承認済み artifact 生成まで塞がない | — | 要望再浮上時は新 ID / successor-lane で再起票 |


**触らない原則**: spec/proof の採掘を増やさない。done 件数を進捗指標にしない。face を broad visual retry loop に戻さない。リモートは `origin/master` を正本とし、追加スライスは master からブランチを切る ([P2A-phase2-motion-segmentation-branch-review.md](verification/P2A-phase2-motion-segmentation-branch-review.md) は歴史的判断として参照)。

## 主成果物

- active_artifact: NLM transcript → YMM4 CSV → ゆっくり解説動画制作ワークフロー
- artifact_surface: CLI → CSV → YMM4 台本読込 → 演出設定 → レンダリング → サムネイル → 投稿
- last_change_relation: **2026-04-30** G-25 creative acceptance closed negative; G-26 proposed. The review opens, but property variations are not usable animation. Recorded failure classes and shifted the next slice from static property deltas to motion primitive grammar / compatibility.

## カウンター

- blocks_since_user_visible_change: 0
- blocks_since_manual_evidence: 0
- blocks_since_visual_audit: 0

## 量的指標

- test_file_count: 32
- test_count: 430
- mock_file_count: 0
- impl_file_count: 36
- mock_impl_ratio: 0.00
- open_todo_count: 0

## 最終検証

- last_verification: **2026-04-30 G-25 acceptance follow-up**. User-side YMM4 openability confirmed. Creative animation acceptance failed: generated property variants are not usable as motion variations. Added `docs/verification/G25-animation-variation-acceptance-2026-04-30.md` and proposed G-26. No code path changed in this follow-up block.

## Evidence（CLI artifact mode）

- evidence_status: Production E2E 実証済み (2026-04-05)。palette.ymmp → extract-template --labeled → face_map.json (11表情) → Part 1+2IR_row_range.json (28 utt, row-range) → production.ymmp (60 VI) → production_patched.ymmp (face 133 changes) → YMM4 visual proof OK。全編にわたって表情切替を確認。**茶番劇 E2E (2026-04-13)**: face 138 + idle_face 16 + slot 10 + motion 6 を IR → apply-production → YMM4 で実証。正本 [CHABANGEKI-E2E-PROOF-2026-04-13.md](verification/CHABANGEKI-E2E-PROOF-2026-04-13.md)
- last_e2e_data: AI監視(60 VoiceItem) の production.ymmp + chabangeki_e2e_ir.json (28 utt, row-range + idle_face + slot + motion) + face_map + slot_map_e2e + tachie_motion_map_e2e
- external_tool_verification: YMM4 visual proof OK (2026-04-13)。Phase 1 (face + idle_face) および Phase 2 (+ slot + motion) ともに PASS。実運用フィードバック: 表情はテンプレ指定のほうが実用的、speaker マッピングの左右逆転が発生
- final_artifact_reached: Yes (CSV → YMM4 台本読込 → IR → patch-ymmp → 表情差し替え済み ymmp)
- blocking_dependency: なし。face は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE`_* / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class か、最終 creative judgement NG のときだけ再オープン

## FEATURE_REGISTRY 状態サマリ (2026-04-29 更新)

- done: 47件（台帳集計、G-25 追加）
- approved: 3件（H-01, G-20, **G-24**）— G-24 は茶番劇 Group template-first 運用の正本化、G-20 は geometry helper
- proposed: 1件（G-26 motion primitive grammar / compatibility probe）
- info: 2件（C-01, C-06）
- hold: 9件（A-03, D-02, E-01, E-02, **G-01, G-03, G-04, G-21, G-22**）
- quarantined: 2件（F-01, F-02）
- rejected: 7件（B-10, C-02, C-03, C-04, C-05, D-01, F-03）

## Python のスコープ制約（2026-03-30 確定、2026-04-28 境界補正）

Python の責務は CSV / IR / registry / 台本読込後 `.ymmp` patch の接着層に限定する。YMM4 が持つ制作機能を Python 側で再生成しない。

許容済み:

- CSV / 診断 JSON / manifest などの CLI artifact 生成
- H-01 packaging brief / H-02 `thumbnail_design` / 将来の YouTube metadata draft など、制作・投稿判断を支える機械可読 artifact 生成
- 台本読込後 `.ymmp` に対する限定 patch（face / bg / slot / overlay / se / motion / bg_anim / transition / skit_group / thumb.* など、capability matrix と feature registry で範囲が固定されたもの）
- repo-tracked YMM4 template source / registry / readback に基づく限定的な値差し替え

禁止:

- 画像生成・画像合成（PIL/Pillow 含む）
- `.ymmp` のゼロからの生成、YMM4 台本読込の代替、YMM4 GUI 操作
- YMM4 native template 資産の Python 生成、YMM4 出力の模倣・Python preview
- 動画レンダリング・音声合成

## 外部メディア取得の方針（2026-03-30）

- 取得機能（acquisition）と受け取り機能（receiving）は分離する
- 最終的に自動化したい（ユーザー指示）
- A-04（RSS）は再審査済みで done。旧 D-02（背景動画取得 / 素材 API）は汚染バッチ gate 下にあり、現在の D-02 は C-07 v3 吸収済み hold として扱う

## Authority Return Items

- G-02 done。IR 語彙定義 v1.0
- G-02b done。ymmp 構造解析完了。bg+face 差し替えが最小実用単位
- G-05 done。v4 proof 完了。Custom GPT が 28 utterances / 5 sections の IR を正常出力
- G-06 done。patch-ymmp 変換器 + extract-template 実装済み。実機検証 OK
- G-07 done。idle_face (待機中表情) TachieFaceItem 挿入。carry-forward + character-scoped 対応
- G-11 done。`slot` contract を `validate-ir` / `apply-production` / `patch-ymmp` に統合し、TachieItem X/Y/Zoom の deterministic patch と `off` hide を CLI/readback まで閉じた
- G-12 completed。`measure-timeline-routes` CLI で ymmp から `VideoEffects` / `Transition` / template candidate route を readback でき、`--expect` / `--profile` で route contract miss と profile mismatch を検出できるようにした
- G-12 contract fixed。`docs/verification/G12-timeline-route-measurement.md` と `samples/timeline_route_contract.json` により、repo-local corpus では `motion=TachieItem.VideoEffects`、`bg_anim=ImageItem.X/Y/Zoom`、effect-bearing bg=`ImageItem.VideoEffects`、fade-family `transition`=`VoiceItem.VoiceFadeIn/Out` / `VoiceItem.JimakuFadeIn/Out` / `TachieItem.FadeIn/Out` まで mechanical に確定した
- G-12 corpus audit。repo-local `.ymmp` 16 本を測定し、fade-family `transition` route は production/probe sample で観測、`template` route は 0 件であることを確認。未確定は non-fade / template-backed transition family のみ
- G-13 done。`overlay` は `--overlay-map` から deterministic な `ImageItem` 挿入まで閉じ、`OVERLAY_UNKNOWN_LABEL` / `OVERLAY_MAP_MISS` / `OVERLAY_NO_TIMING_ANCHOR` / `OVERLAY_SPEC_INVALID` を mechanical failure として扱える
- G-13 done。`se` は `--se-map` で label と timing anchor を解決し、G-18 で `AudioItem` 挿入まで実装。機械的失敗は `SE_UNKNOWN_LABEL` / `SE_MAP_MISS` / `SE_NO_TIMING_ANCHOR` / `SE_SPEC_INVALID`
- G-18 done。`_apply_se_items` が既存 `AudioItem` テンプレまたは最小骨格で SE を挿入。`PatchResult.se_plans` は挿入件数
- G-14 done。`samples/timeline_route_contract.json` の `production_ai_monitoring_lane` で [samples/production.ymmp](samples/production.ymmp) の motion/transition を contract pass。bg_anim は本 ymmp に ImageItem 無しのため required 外
- G-23 done。`motion` preset library は `speaker_tachie` 専用として固定。茶番劇演者の主経路には使わない
- G-24 approved。茶番劇演者の主経路を **GroupItem template-first** に切り替え、canonical template → 小演出量産 → production で template 解決 + fallback + manual note を正本化
- timeline packet: G-11 slot patch hardening 完了 → G-12 timeline route measurement packet 完了 → G-13 overlay / se insertion packet 完了。timeline 編集は broad retry loop に戻さず、packet ごとに failure class / readback / boundary を定義して扱う
- H-01 dry proof 済み。`docs/verification/H01-packaging-orchestrator-ai-monitoring-dry-proof.md` により、brief が title / thumbnail / script の共有契約として機能することを repo-local artifact ベースで確認した。strict な before/after GUI rerun proof はまだ残る
- H-02 done (2026-04-06)。dry proof + strict GUI rerun proof pass。4/5案が preferred_specifics を使用、banned pattern なし、Specificity Ledger・Brief Compliance Check 出力確認済み。コピー品質の実用改善は別課題
- H-03 done。`score-visual-density` CLI + GUI 品質診断。dry proof は `docs/verification/H03-visual-density-ai-monitoring-proof.md`
- H-04 done。`score-evidence` CLI + GUI 品質診断。manual proof は `docs/verification/H04-evidence-richness-ai-monitoring-proof.md`
- B-18 done。`diagnose-script` + `docs/SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md`。dry proof `docs/verification/B18-script-diagnostics-ai-monitoring-sample.md`
- C-09 done。`docs/S1-script-refinement-prompt.md` + gui-llm-setup-guide 導線
- H-02 closed。packaging: H-02/H-03/H-04 は実装済み。H-01 は approved（schema + dry proof、運用で brief 固定）。timeline は新 sample または known failure class が出たときだけ再オープンする
- G-01/G-03: hold (タイムライン操作 API 非公開)
- G-05 v4 prompt doc が canonical。remote Custom GPT Instructions 側の drift は `PROMPT_FACE_DRIFT` / `FACE_PROMPT_PALETTE`_* で検出する
- D-02: hold (C-07 v3 に吸収完了)
- E-01 / 旧 E-02 standalone: hold 継続。metadata draft は successor-lane として別起票可
- F-01/F-02: quarantined 継続

## 実制作ワークフロー自動化カバレッジ (2026-04-06 棚卸し)

FEATURE_REGISTRY 上 done 42 件だが、実際の動画制作ワークフロー全体に対するカバレッジは限定的。
ユーザーフィードバックに基づき、各工程の自動化状態と実際の重さを正確に記録する。

### 工程別カバレッジ


| #   | 工程                  | 担当                   | 自動化状態      | 実際の重さ   | 備考                                                                                       |
| --- | ------------------- | -------------------- | ---------- | ------- | ---------------------------------------------------------------------------------------- |
| 1   | 台本作成                | NotebookLM           | 外部ツール (手動) | **重い**  | NLM出力はそのまま使えない。下記「台本品質問題」参照                                                              |
| 2   | 台本→CSV変換            | build-csv CLI        | **自動**     | 軽い      | B-01〜B-17 で字幕分割品質も改善済み                                                                   |
| 3   | CSV→YMM4読込          | YMM4 台本読込            | 手動操作 (1回)  | 軽い      | C-01 (info) として記録済み                                                                      |
| 4   | 演出IR生成              | Custom GPT (C-07)    | 半手動 (コピペ)  | 中       | GPTへの入力と出力の受け渡しが手動                                                                       |
| 5   | IR→ymmp適用 | apply-production CLI / GUI 演出適用タブ | **一部自動** | 軽〜中 | face/bg/slot/overlay/se/motion/bg_anim/transition/skit_group は capability matrix 範囲で限定 patch 可能。GUI 露出は face/bg/skit_group 中心で、overlay/se/motion map 類は未露出 |
| 6   | **YMM4上の演出配置** | YMM4 + template-first tooling | **一部自動 / acceptance は手動** | **重い** | G-24 skit_group は repo-tracked template source → registry → analyzed placement → `.ymmp` readback まで到達。最終 composition / 間隔 / テンポは YMM4 creative acceptance として残る |
| 7   | **視覚効果・サムネ制作** | YMM4 / 人間 + 限定 patch 補助 | **補助あり / 生成なし** | **重い** | サムネは `thumbnail_design` sibling artifact + `thumb.*` template slot patch が最小入口。画像生成・PNG 書き出し・完成判断は自動化しない。実サムネ template proof は未完了 |
| 8   | レンダリング              | YMM4                 | 手動トリガー     | 軽い      | C-06 (info) として記録済み                                                                      |
| 9   | YouTube投稿           | YouTube Studio       | 手動         | 中       | E-01 と旧 E-02 standalone は hold。H-01/H-02/H-04 由来 metadata draft は successor-lane として別起票可 |


### 台本品質問題 (工程1の詳細)

NotebookLM で生成した台本には以下の構造的弱点があり、動画用に大きな手動調整が必要。資料を持っているのが NotebookLM である以上、これは前段ボトルネックとして扱い、CSV / IR 生成前に B-18 / C-09 / manual QC を挟む:

- **NLM臭**: NotebookLM特有の会話構造・語彙・展開パターンが残り、ゆっくり解説として不自然
- **誤字・誤変換**: 指示を理解しないまま出力し、固有名詞・専門語・日常語を壊すことがある
- **話者混同**: 聞き手 (れいむ) と解説 (まりさ) のセリフ担当が混同することがある
- **様式不適合**: ゆっくり解説の様式 (ボケツッコミ、視聴者への問いかけ、テンポ等) への最適化が必要
- **YT視聴者向け調整**: YouTube視聴者の離脱を防ぐ構成・フック・情報密度の調整が必要
- **演出IRとの連鎖**: 台本品質が低いと、C-07 で生成する演出IRの質も下がる。台本の構造が曖昧だと、演出指示も曖昧になる

### 演出配置の未自動化問題 (工程6の詳細)

現状の patch-ymmp / apply-production でできること:

- face (表情) の差し替え: 133 changes 実証済み
- bg (背景) のセクション切替: 2ラベルで実証済み
- slot (キャラ位置): X/Y/Zoom の deterministic patch
- overlay: deterministic な ImageItem 挿入
- se (SFX): fully implemented through `AudioItem` writes (G-18 done). Readback proof lives in `samples/AudioItem.ymmp` and `docs/verification/G13-overlay-se-insertion-packet.md`.
- motion / bg_anim / fade-family transition: capability matrix 範囲で write route 固定済み
- skit_group: template source / registry 解決 / analyzed placement / readback まで実装済み。creative acceptance は別

現状の patch-ymmp / apply-production でできないこと (= 手動または template authoring に残る部分):

- **素材の調達と準備**: 背景画像、図解素材、茶番劇用のキャラポーズ等の入手・加工
- **新規テンプレ authoring**: YMM4 native template と素材登録は人間が作る
- **最終レイアウト判断**: 画面上の間隔・テンポ・見栄えは creative acceptance
- **GUI 未露出 map 類**: overlay / se / motion / bg_anim / timeline-profile は production で必要化したら GUI 補完スライス
- **未登録の茶番劇 intent**: production gap が出た時だけ新テンプレとして起票
- **図解アニメーション**: 情報伝達のための図解・チャート等の動的表示

### 視覚効果の未実現 (工程7の詳細)

- サムネイルを 1枚も完成させていない
- 茶番劇風アニメーション: ゼロ (方向性のみ記録済み: feedback_nlmytgen_visual_direction)
- 図解アニメーション: ゼロ
- 現状は画像表示のみ
- H-02 の C-08 prompt は仕様準拠だがコピー品質が不足 (抽象煽りは抑えたが視聴者の感情フックが弱い)

### ギャップの構造

done 42 件の大半は「テキスト変換パイプライン」と「spec/proof整備」に集中している。
実際の動画制作で最も時間がかかる工程 (演出配置・視覚効果・台本品質) は未自動化または部分的。
packaging spec (H-01〜H-04) は判断支援フレームワークとして整備済みだが、
その出力を実際の制作物に変換する工程が手動のまま。

### YouTube投稿自動化の分離

E-01 と旧 E-02 standalone metadata template は動画制作ワークフローとは独立したタスクとして切り出す。
ただし、H-01/H-02/H-04 を入力にした YouTube metadata draft は、投稿自動化ではなく packaging artifact の successor-lane として再起票できる。制作パイプラインへ自動注入したり YouTube Studio 操作まで含める場合は、別 ID で integration point を明示する。

## 既知の問題

- 直前 handoff は 53f3718 時点の内容で止まっており、後続 commit `8a1c710` で追加された canonical docs とその未充足状態は含んでいなかった
- E-02 の旧 standalone metadata template は YouTube Studio への手入力をテキストファイル生成に置き換えるだけで弱い。ただし H-01/H-02/H-04 と接続する metadata draft は successor-lane として再起票可
- D-02 / F-01 / F-02 は前セッションの汚染バッチ由来で、個別精査前に normal backlog として扱えない。これは目的の禁止ではなく、再審査なしの通常復帰禁止
- A-04 は実装済み・再審査済みだが、runtime/context の一部に旧 `quarantined` 記述が残っていたため handoff trust を要再同期
- B-14 後の追加観測では、長すぎる行は大幅に減り、全字幕が 3 行以内に収まる水準まで改善した。残 pain は bulk overflow ではなく、境界ケースの改行品質に移っている
- B-11/B-12/B-13/B-14 により、辞書や timing ではなく字幕改行が支配的な pain だと確認。B-14 後は `ー`、カギ括弧、数値+記号などの individual judgement が主で、次は heuristic を積み増すより corpus-based な例収集へ寄せる方が自然
- 別機能の feasibility を棚卸しした結果、次の本命候補は S-6 LLM adapter。E-01/旧E-02 standalone は secondary、D-02/F-01/F-02 は引き続き汚染バッチ gate
- resume 用プロンプト正本は廃止済み。再開判断は `AGENTS.md` / `docs/REPO_LOCAL_RULES.md` / 本ファイルを起点に、必要な正本節だけを読む
- `group_motion` は `GROUP_MOTION_NO_GROUP_ITEM` / `GROUP_MOTION_TARGET_MISS` / `GROUP_MOTION_TARGET_AMBIGUOUS` を fatal 扱いに変更済み。運用側で `group_target` 命名規約（通常 `Remark`）のばらつきが残る場合は、次スライスで `validate-ir` lint を優先する。
- G-07 done。idle_face carry-forward により待機中表情を維持。TachieFaceItem 挿入で non-speaker キャラの表情を制御
- れいむの surprised が palette.ymmp に未定義でも、現在は `FACE_ACTIVE_GAP` / `FACE_LATENT_GAP` として事前に可視化される。これは data-side gap であり、face サブシステム自体の未完成を意味しない

## 2026-04-05 Linebreak Note

- Structural major/minor reflow redesign landed in B-17 path.
- Sample proof target: `samples/AI監視が追い詰める生身の労働.txt`
- Verified result: catastrophic screen breaks such as `では / なく`, `）」 / という`, `） / 」`, and `19 / 億` were reduced; residual issues remain around some `XというY` and quoted explanatory phrases.
- Additional tuning now suppresses sparse first lines created by short comma-led intros when a better particle or later-phrase break is available.
- Close-bracket/content fallback and page-plan comparison are now enabled so quoted labels like `「配送サービスパートナー（DSP）」 / プログラム...` and `「サンクマイドライバー」という / プログラム...` no longer force the earlier worse splits.
- Emergency inner-break candidates inside long quoted labels are now available as a last resort, but residual 41-48 width lines still remain and likely need either YMM4-aware width calibration or a stronger policy on splitting long quoted labels.
- Single-hiragana tails after quoted terms are now handled separately, which improved cases like `「アルゴリズムによる最適化」 / と聞くと...` without reopening `」`-at-line-start regressions.
- Page carry-over scoring now differs from in-page line breaks: `close+tail` boundaries and overflow-relief plans can win when an extra page removes the screen break without reopening `」` line-head regressions.
- Additional exact page-count candidates are now compared with their own ideal page width, which fixed the residual `完璧に計算されたアルゴリズムが生身の / 人間という...` class by allowing one more page when the earlier exact plan still overflowed.
- Current sample residuals are down to 2 lines in `_tmp_structural_balance.csv`: `誰の汗とリスクを動力にして回り始めるのかを / 解剖していくということですね。` and `自発的にリスクを取らせる罠のようなものです。 / データによると、`.
