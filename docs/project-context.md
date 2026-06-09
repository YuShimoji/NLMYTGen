# Project Context — NLMYTGen

## PROJECT CONTEXT
- プロジェクト名: NLMYTGen
- 環境: Python / uv / CLI
- ブランチ戦略: master
- 現在地の正本: 通常再開では `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md` で止める。本ファイル冒頭は状態スナップショットではなく、航海日誌への短い入口。
- 現フェーズ: G-27 Real Estate DX の production carrier 待ちは active blocker から外し、case-specific evidence として保持する。次は `runtime-state.md` の通り、newsroom-produced bundle の downstream adapter intake、または G-28 Reference-Driven Generic Screen Carrier の Lecture Diagram diagnostic skeleton / theme variants / Map-Evidence diagnostic skeleton 済み状態からの refinement へ進む。
- 古い roadmap / prompt / verification packet は現行判断に使わない。必要な履歴は DECISION LOG と HANDOFF SNAPSHOT の該当行だけ読む。
- Python のスコープは「テキスト変換 + IR/registry + ymmp 限定後段適用」。動画レンダリング・画像生成・YMM4 GUI 操作は Python の責務ではない。

---

## ACTIVE ARTIFACT
- Active Artifact: NLM transcript → YMM4 CSV → Writer IR → Template Registry → YMM4 Adapter → 動画制作ワークフロー効率化
- Artifact Surface: CLI artifact → CSV / registry / patched ymmp → YMM4 読込・確認・レンダリング
- 現在のスライス: G-27 は diagnostic carrier / review console / SCS lessons を証跡として残し、active production carrier blocker としては閉じる。G-28 は proposed であり、受領済み参照画像から構図原理を抽出した `docs/verification/G28-REFERENCE-STYLE-BRIEF-2026-06-05.md`、Lecture Diagram の concrete spec / diagnostic skeleton / readback artifact、`real_estate_information_gap` と `game_mechanics_explanation` diagnostic variants、Map / Evidence の concrete spec / diagnostic skeleton / readback artifact を refinement の入口にする。
- 成功状態: G-27 の失敗と学びを捨てずに、production 昇格・slot-fill・render へ飛躍しないまま、参照画像の principle extraction を SCS mapping / generic carrier archetype / diagnostic skeleton / theme-specific diagnostic variant / Map-Evidence archetype / readback artifact / future YMM4 carrier review へ段階変換できる状態にすること。

---

## CURRENT LANE
- 主レーン: Explore / Audit（G-28 Reference-Driven Generic Screen Carrier）。現行の優先は [runtime-state.md](runtime-state.md) の `next_action`。
- 今このレーンを優先する理由: G-27 の carrier 待ちが不動産DX固有の production blocker として長期化したため、既存 evidence を参照資産に畳み、構図・密度・余白・色階層・視線誘導・UI感を汎用化する方が次の制作摩擦を減らせる。

---

## ROADMAP UPDATE (2026-04-27 post-cleanup prep)

This section narrows the next roadmap after the legacy-document cleanup. It does not approve new implementation scope. The gate-shaped author/export pass is now closed for the v1 planned set; the current value path is production-use validation with existing templates.

### 現行ロードマップの主軸

1. **G-24 `delivery_nod_v1` cautious gate を閉じる（完了）**
   - actor: user + assistant
   - owner artifact: YMM4 native template asset + `skit_group` registry / Capability Atlas state
   - bottleneck: `audit-skit-group` readiness と standalone native template export proof の分離
   - done condition: `delivery_nod_v1` が GroupItem + body/face の 2 `ImageItem` children + no `TachieItem` で export され、manual acceptance (`nod amplitude`, `does not dominate scene`) を PASS する
2. **`deny_oneshot -> exit_left` を同じ gate で処理する（完了）**
   - actor: shared
   - owner artifact: `skit_group.intent.*` の support level
   - bottleneck: starter 2 件の成功を remaining intent 群へ安全に横展開すること
   - done condition: `deny_oneshot` / `exit_left` が `direct_proven` after export proof になること
   - result: user completed both samples; repo inspection found ImageItem body/face + no `TachieItem`; both intents are now `direct_proven`
3. **P02 production adoption を template 解決の実戦運用へ寄せる（現行）**
   - actor: assistant + user
   - owner artifact: production adoption proof / template resolution notes
   - bottleneck: 小演出 authoring 自体を progress と誤認せず、作った template が実制作の選択負荷を減らすかへ接続すること
   - done condition: exact / fallback / manual note が、実制作の S-6（背景・演出設定）でどの手作業を減らすかまで記録される
   - loop stop: `exit_left` 後は追加 motion 作成へ進まず、実制作 IR の template 解決結果を見て production gap が出た時だけ新テンプレートを再起票する
   - role split: user は少数の reusable native template を作り、assistant は組み合わせ・registry・fallback note で production-like sample / 解決結果を作る。user は全サンプル作成ではなく確認に集中する
4. **メンテ層は on-demand に保つ**
   - actor: operator / assistant
   - owner artifact: B-18 台本診断、B-17 改行残差、H-01/H-02 packaging / thumbnail briefs
   - bottleneck: G-24 の主軸を、done 件数稼ぎや古い spec/proof 整備で薄めないこと
   - done condition: 新台本・新サムネ・drift 発生時だけ起動し、通常の次 frontier にはしない

### formal plan の分岐条件

- **通常**: 次プランは existing v1 template set を使った production-like sample / 解決結果作成から始める。assistant が exact / fallback / manual_note を整理し、user は YMM4 上で結果確認に集中する。
- **十分**: exact coverage が制作負荷を減らすなら production-use hardening を続ける。追加 motion authoring はしない。
- **不足**: `fallback` / `manual_note` / missing-template / body-face drift / `TachieItem` 混入 / repo bug を failure class として分け、追加テンプレート起票か修正かを選ぶ。FAIL を代替成功にしない。
- **新規制作案件が先に来た場合**: G-24 の主軸は維持し、メンテ層は B-18 → H-01/H-02 on demand → B-17 drift-only の順で必要分だけ起動する。

### プラン作成前に揃えるもの

- [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) は G-24 production-use validation を現行アンカーとして更新済み。
- `runtime-state.md` と `verification/P02-production-adoption-proof.md` は、v1 template completion と production-use validation を分離する現行参照先として更新済み。
- 削除済みレガシードキュメント名への repo-local 参照は `git grep` で残存なし。
- `formal plan の分岐条件` は本節に固定済み。次プランはこの分岐のどれに入ったかを冒頭で宣言してから書く。
- 次の formal plan は **production-like sample / 解決結果作成** から始める。追加 motion authoring は production gap が具体化した時だけ起票する。

### 今回やらないこと

- 新しい FEATURE を増やさない。
- `motion_target` / `group_motion` を `nod` の代替成功として扱わない。
- 背景アニメ/S6 の古い証跡を、現行判断に混ぜない。
- `audit-skit-group` の `exact` を standalone export proof と読み替えない。

## DECISION LOG

Latest supervision gate (2026-06-09): `newsroom_handoff_request_authority_no_op_wait`
records the refreshed cross-repo review of the supplied `newsroom-yt-pipeline`
handoff. The handoff is candidate downstream input, not active NLMYTGen
authority yet. NLMYTGen remains on the G-28 `game_mechanics_explanation`
diagnostic lane. This refresh did verify the Newsroom repo and export read-only:
`C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline` was on
`main` / `1296b8e` with `HEAD...origin/main=0 0`, and
`C:\Users\thank\Storage\Media Contents Projects\newsroom-yt-pipeline\data\exports\episode_756343df9853`
contained `export_manifest.json`, `script.csv`, `script_ir.json`,
`visual_ir.json`, `visual_plan.md`, `source_list.md`, `quote_manifest.yml`,
`asset_manifest.yml`, and `ymm4_notes.md`. The selected decision still remains
`request_authority / no-op_wait` because no human decision has authorized
copy-in versus read-only reference, no human decision has paused or superseded
the current G-28 game_mechanics lane, and the inspected Newsroom export is not
NLMYTGen production proof. Do not couple to Newsroom by subprocess/path/pip
dependency, copy runtime export files into tracked artifacts, start
implementation, Review Console changes, context visual plugin work, `.ymmp`
generation, render, production timing, rights approval, creative final
acceptance, G-27 revival, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM, common
foundation, or real `codex exec` work from this gate. If the user wants
Newsroom downstream intake, first collect explicit authority for copy-in versus
read-only reference and explicit authority to pause/supersede the current G-28
game_mechanics lane. Detailed gate evidence is in
`docs/verification/NEWSROOM-HANDOFF-SUPERVISION-GATE-2026-06-09.md`.
Reporting format scar: for ChatGPT handoff blocks, wrap the whole copy block in
one outer Markdown code fence, keep `BEGIN_COPY_BLOCK_FOR_CHATGPT` and
`END_COPY_BLOCK_FOR_CHATGPT` inside it, and do not use nested code fences in the
`next prompt` field.

Latest common foundation decision (2026-06-09): `single_fake_execution_flow_committed_audited`
records that `post_commit_audit_single_fake_execution_flow_001` passed for
`e509863 feat: update orchestration scaffold`, with the commit pushed to
`master` and upstream parity verified as `HEAD...@{u}=0 0`. This retires
stale staged-work prompts for the slice: `stage_single_fake_execution_flow_001`,
`single_fake_execution_flow_staged_diff_review_001`, and any fake runner
scaffold stage/commit prompt. The active common foundation state is committed
and audited: fake runner scaffold exists, the single fake execution flow helper
exists, the helper is test/helper-only, and normal CLI/runtime behavior does
not expose the fake flow. There is no `--single-fake-flow` flag. Valid fake
reports go through `agent_gate.evaluate_report`; the local notify stub is only
after `gate_result.needs_human=true`; pass writes no notify artifact; invalid
JSON, missing report, nonzero exit, and timeout fail closed. Real `codex exec`
remains disabled/unimplemented: `codex_execution_started=false`,
`real_subprocess_started=false`, no `subprocess.run`, no stdin piping, no
runtime worker loop, and no external notification service. The next common
foundation work is not immediate real execution. If explicitly authorized
later, use design-only `real_runner_boundary_design_001`, covering explicit
opt-in execution policy, subprocess boundary, stdin piping boundary,
timeout/cancellation, report path containment, gate authority, notify boundary,
runtime artifact hygiene, and no external notification without separate
authorization.

G-28 real-estate diagnostic review surface acceptance (2026-06-08):
Record `overall_decision=accept_as_diagnostic_review_surface_with_title_metric_caveat`
for the YMM4 diagnostic probe and stop the individual pixel-tuning loop for
this artifact. The accepted scope is diagnostic review surface use only:
openability, focal chain, connector treatment, X=313.0 lower-right callout
alignment, caption reserve, diagnostic host placeholders, and diagnostic
boundary pass, while title metric debt and layout-system debt remain. Do not
continue title-Y / callout / right-node micro-offset fixes; any future visual
centering problem should become a text/layout system redesign slice. This does
not approve Review Console implementation changes, production render,
production carrier approval, creative final acceptance, rights automation,
source footage, G-27 authority reuse, common foundation work, or ClipPipeGen
access.

G-28 real-estate evidence note (2026-06-08):
`pass_dom_evidence_needs_manual_screenshot` is recorded in
`docs/verification/G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-EVIDENCE-2026-06-07.md`
for the earlier `real_estate_information_gap` read-only Review Console panel.
Existing Electron DOM smoke confirmed `#g28-review-console-ingest`, artifact
inventory, diagnostic badges, readback summary, human GUI summary, caveats,
allowed diagnostic decisions, and absence of production approval labels. No
Review Console implementation files, generated probe artifacts, builders,
readback/report files, render, production approval, creative final acceptance,
rights automation, G-27 authority, ClipPipeGen, RSS / NotebookLM, or common
foundation work changed. A manual screenshot or separately authorized
G-28-specific capture slice remains optional if visual screenshot evidence is
still required.

Latest G-28 decision (2026-06-08): `remote_handoff_sealed_after_g28_game_mechanics_inspector_accept`
keeps the accepted `game_mechanics_explanation` inspector-first diagnostic
review surface context in-project for another terminal. The restart owner is
`AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md` plus
`docs/USER_COPYPASTE_BLOCKS.md` SECTION 20. The accepted contract remains
`review_surface=inspector_first`, `in_frame_review_overlay=false`,
`clean_frame_available=true`, `semantic_labels_human_visible=true`,
`diagnostic_only=true`, and `production_candidate=false`. This handoff does not
authorize Source-Footage, `.ymmp` generation, render, production timing,
creative final acceptance, G-27 revival, RSS / OPML / Inoreader / NotebookLM,
common foundation, ClipPipeGen, generated artifact rewrites, or generator
changes. The next safe input is human-supplied evidence for the already scoped
YMM4-saved carrier review conditions, or a decision to stay with the accepted
HTML/readback diagnostic precedent.

Latest G-28 decision (2026-06-08): `g28_game_mechanics_ymmp_saved_carrier_review_conditions`
adds the scoped condition checklist for moving the accepted
`game_mechanics_explanation` Lecture Diagram review surface toward a later
YMM4-saved carrier review. The required inputs are explicit human selection of
that review mode, a carrier path, preview screenshot, timeline screenshot,
item/layer confirmation, and bottom caption safe-area evidence. This is
conditions-only documentation: no `.ymmp` generation, render, production timing,
creative final acceptance, Source-Footage intake, gameplay screenshot intake,
image path/URL/raw reference intake, G-27 revival, RSS, NotebookLM, generated
artifact rewrite, or generator change is approved.

Latest G-28 decision (2026-06-08): `g28_game_mechanics_review_surface_accept`
records human `decision: accept` for the repaired `game_mechanics_explanation`
Lecture Diagram review surface. The accepted scope is reviewability only:
the clean 16:9 frame and lower Review Inspector are separated, the frame no
longer has double-box review overlays, semantic labels remain visible through
the inspector, host remains non-focal, and caption reserve / density are
acceptable for this diagnostic surface. This does not approve production:
`diagnostic_only=true`, `production_candidate=false`, no Source-Footage, no
`.ymmp` generation, no render, no production timing, and no creative final
acceptance. Next safe work, only if needed, is scoped condition planning for a
YMM4-saved carrier review.

Latest G-28 decision (2026-06-08): `g28_game_mechanics_review_surface_inspector_first`
is implemented for the existing `game_mechanics_explanation` Lecture Diagram
diagnostic artifact after human `decision: further revise`. The previous
review-only labels were visible but appeared as in-frame boxed overlays, making
the left/right nodes, callouts, and center focal look double-boxed. The artifact
is repaired in place: default HTML keeps the 16:9 frame clean, moves semantic
labels into the lower review inspector, and records
`in_frame_review_overlay=false`, `review_overlay_default=false`, and
`clean_frame_available=true` in readback. This remains diagnostic-only:
`production_candidate=false`, no new theme variant, no Source-Footage generator,
no `.ymmp`, no render, no production timing, and no creative final acceptance.

Latest common foundation decision (2026-06-08): `fake_runner_scaffold_committed`
adds a tests-only fake runner scaffold in `da254ff feat: add fake runner
scaffold`. The helper writes synthetic reports to `ExecutionPlan.report_path`,
keeps valid report authority in `agent_gate.evaluate_report`, invokes the local
notify stub only after `gate_result.needs_human=true`, and fails closed for
invalid JSON, missing report, nonzero exit, and timeout. This does not enable
real `codex exec`, stdin piping, subprocess runner behavior, runtime worker
loop, external notification service, ClipPipeGen support, publish/release,
rights automation, or `production_candidate` handling. It also does not resume
G-28 mainline work. The next common-foundation slice should keep the same
boundary unless real runner support is explicitly authorized.

Latest G-28 decision (2026-06-08): `remote_handoff_sealed_after_review_console_ingest`
keeps the latest context in-project for another terminal. The durable restart
packet is now `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`
plus `docs/USER_COPYPASTE_BLOCKS.md` SECTION 18. The next safe work is only
screenshot / Electron smoke evidence or human GUI confirmation of the read-only
G-28 Review Console panel; this does not reopen `.ymmp` generation, builders,
readback/report artifacts, production carrier approval, creative final
acceptance, render, rights/public-use automation, slot-fill, G-27 authority,
ClipPipeGen, RSS, NotebookLM, or common foundation work. Local residue remains
explicitly outside this handoff scope.

Latest G-28 decision (2026-06-08): `pass_review_console_ingest_implemented`
is recorded for the calibrated real-estate YMM4 diagnostic probe. The Review
Console now has a read-only G-28 panel that references the existing `.ymmp`,
readback JSON, report MD, human review record, and ingest plan in place, checks
repo-relative artifact existence, shows diagnostic boundary badges, summarizes
readback/human GUI results, exposes caveats for X=313, title readback debt, host
placeholders, and glyph optical-center limits, and limits visible decisions to
diagnostic review-surface outcomes. DOM smoke verifies the panel and the absence
of production approval labels. This does not change `.ymmp`, builder,
readback/report artifacts, render, production carrier approval, creative final
acceptance, rights/public-use automation, slot-fill, G-27 authority, common
foundation, ClipPipeGen, RSS, or NotebookLM work. Next safe action is screenshot
/ Electron smoke evidence or human GUI confirmation of the read-only panel.

Latest G-28 decision (2026-06-08): `G28-REAL-ESTATE-REVIEW-CONSOLE-INGEST-PLAN-2026-06-07`
is added as the docs-only plan for read-only Review Console ingest of the
accepted real-estate YMM4 diagnostic probe. The plan defines the input artifact
inventory, diagnostic status badges, readback summary, human GUI result summary,
title readback follow-up requirements, host placeholder boundary,
human-calibrated callout caveat, diagnostic-only decision schema, future GUI
implementation surfaces, error states, and next-slice acceptance criteria. It
does not implement GUI ingest, modify GUI files, regenerate `.ymmp`, change the
builder, rewrite readback/report artifacts, approve production, approve render,
approve rights/public use, slot-fill, revive G-27, access ClipPipeGen, restart
RSS / NotebookLM work, or implement common foundation / Codex Worker
Orchestration. Next safe action is an explicitly authorized read-only Review
Console ingest implementation slice based on this plan.

Latest G-28 decision (2026-06-08): `accept_for_review_console_ingest_candidate_with_layout_metric_caveat`
is recorded for the calibrated real-estate YMM4 diagnostic probe. Human GUI
recheck accepted the X=313.0 lower-right callout label `仲介インセンティブ`:
openability, focal-chain readability, connector treatment, caption reserve,
diagnostic boundary, and major side-effect checks pass. This authorizes only a
Review Console ingest candidate record / ingest plan. It does not authorize
actual Review Console ingest implementation, production render, production
carrier approval, creative final acceptance, rights automation, slot-fill,
external material intake, G-27 revival, ClipPipeGen, RSS / NotebookLM, or common
foundation / Codex Worker Orchestration work. Layout metric debt remains part of
the candidate: current readback does not directly measure YMM4 glyph optical
center, title y=`-474.5` is visually acceptable but should become a future title
anchor/text-center/safe-area readback check, host placeholders are
diagnostic-only and not production character/visual assets, and X=313 remains a
human-calibrated override rather than reusable formula proof.

Latest G-28 decision (2026-06-08): `g28_real_estate_information_gap_callout_label_human_calibration_v1`
is implemented after human GUI recheck found the lower-right callout label
`仲介インセンティブ` still visually left-shifted after the bounded alignment fix.
The previous computed/polished YMM4 TextItem X was `289`; the human-measured
correct X is `313.0`, so the builder now applies a one-time
`human_calibrated_x=313` and records `calibration_delta_x=24`. This decision
does not claim formula success. It records callout text layout system debt:
`text_center_error_px` remains registered-placement proof only, and a remaining
visual mismatch after this slice should move to callout text layout system
redesign rather than another individual pixel/offset adjustment. Readback passes
as `pass_callout_label_human_calibrated` while the boundary remains
`diagnostic_only=true` / `production_candidate=false`; Review Console ingest,
production render, production approval, creative final acceptance, rights
automation, slot-fill, external materials, G-27 revival, ClipPipeGen, RSS /
NotebookLM, and common foundation / Codex Worker Orchestration remain
unapproved.

Latest G-28 decision (2026-06-07): `g28_real_estate_information_gap_callout_label_alignment_v1`
is implemented after human GUI correction clarified that the actual remaining
visual target is the lower-right callout label `仲介インセンティブ`, not the
right node `借主判断`. Only `G28_LDC_CalloutSlot_3_Label` changed: its
registered optical offset moved from `{x:0,y:-3}` to `{x:4,y:-3}`. The previous
right-node fix is retained because no adverse side effect was reported. The
shared callout formula, node labels, connectors, hosts, caption reserve, variant
id, and diagnostic boundary are unchanged. Readback passes as
`pass_callout_label_alignment_fixed`. This decision also records the metrics
caveat that `text_center_error_px=0` checks registered placement, not rendered
YMM4 glyph optical center. Next safe move is human YMM4 GUI recheck of this
callout-label-only fix; Review Console ingest and all production/rights/render/
slot-fill work remain unapproved.

Latest G-28 decision (2026-06-07): `g28_real_estate_information_gap_right_node_alignment_v1`
is implemented for the existing real-estate YMM4 diagnostic probe after human
GUI recheck returned `revise_probe_again_narrow_right_node_text_alignment`.
Only `G28_LDC_Node_Right_Label` changed: its registered optical offset moved
from `{x:0,y:-4}` to `{x:4,y:-4}`. The shared text-centering formula,
connectors, callouts, hosts, caption reserve, variant id, and diagnostic
boundary are unchanged. Readback passes as `pass_right_node_alignment_fixed`.
This decision also records the metrics caveat that `text_center_error_px=0`
checks registered placement, not rendered YMM4 glyph optical center. Next safe
move is human YMM4 GUI recheck of this right-node-only fix; Review Console
ingest and all production/rights/render/slot-fill work remain unapproved.

Latest G-28 decision (2026-06-07): `g28_real_estate_information_gap_layout_contract_v1`
is implemented for the existing real-estate YMM4 diagnostic probe. The builder
now records derived connector geometry, manual text offset registry, a bounded
2-3 callout formula with four-callout risk, and tolerance readback. Verification
passed as `pass_probe_polished` with
`layout_contract_metrics_present=true` and
`layout_contract_tolerances_pass=true`. This remains diagnostic-only
(`production_candidate=false`); the next safe move is human YMM4 GUI recheck
before any Review Console ingest decision. No production render, production
approval, creative final acceptance, rights automation, slot-fill, external
image/URL/raw reference, source footage/audio/TTS, G-27 revival, ClipPipeGen,
RSS / NotebookLM, or common foundation / Codex Worker Orchestration work is
approved by this decision.

| 日付 | 決定事項 | 選択肢 | 決定理由 |
|------|----------|--------|----------|
| 2026-06-07 | **G-28 real-estate polished YMM4 diagnostic probe の layout contract audit は `needs_layout_contract_implementation` を推奨する。** | Review Console ingestへ即進む / さらに目分量polishを続ける / probe pathを延期する / layout contractを1回だけbounded revisionする | `docs/verification/G28-REAL-ESTATE-YMMP-PROBE-LAYOUT-CONTRACT-AUDIT-2026-06-07.md` により、現在probeは diagnostic GUI surface としては accept 済みだが、再利用可能なlayout systemとしては未実装部分が残ると判断した。TextItemはtop-left formulaで説明できるがmanual optical offsetに依存し、connectorはedge-to-edge barとして説明できるがhard-coded override、callout rowは3件専用で4件以上の破綻リスクがある。次は追加polishではなく、derived connector geometry、explicit offset registry、2-3 callout formula、tolerance readbackを入れる bounded layout-system revision が妥当。今回 `.ymmp`、builder/generator、readback/report、render、production approval、creative final acceptance、rights automation、source footage/audio/TTS、外部画像/URL/raw reference、G-27、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 real-estate polished YMM4 diagnostic probe の GUI re-review は `accept_as_diagnostic_gui_probe_with_layout_contract_followup` として受け、次工程を layout contract audit に限定する。** | production approvalへ進む / さらに目分量polishを続ける / Review Console ingestへ即進む / re-review結果を記録し layout contract audit へ進む | 人間reviewでは YMM4 openability、focal chain、caption reserve、callout readability、host role、実在サービス/物件感、diagnostic boundary は pass/clear。yellow connector treatment と rectangle text alignment は見た目として改善したが `pass_partial` であり、残課題は数pxの再polishではなく、text centering formula、connector positioning formula、callout slot rule、manual offset registry、tolerance readback を明示する layout contract 問題として扱う。今回 `.ymmp`、builder/generator、readback/report再生成、render、production carrier approval、creative final acceptance、rights automation、source footage/audio/TTS、外部画像/URL/raw reference、G-27、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 real-estate YMM4 diagnostic probe bounded polish revision は `pass_probe_polished` として通過した。** | `revise_probe` を未処理に残す / production promotion に進む / 新variantに逃がす / 同一diagnostic probeを最小更新する | Human GUI review の `revise_probe` に対して、`scripts/build_g28_real_estate_ymmp_probe.js` は yellow connector alignment、callout slot spacing、TextItem visual offset の bounded polish だけを行うようになった。`samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.{ymmp,readback.json,report.md}` を同一pathに再生成し、readback は `diagnostic_only=true` / `production_candidate=false` / 1920x1080 / bottom 20% caption reserve clear / focal chain 3 / callout count 3 / non-focal hosts / bounded text budget / external image・URL・source footage・audio・TTS・token-like counts 0 を満たす。今回も diagnostic polish only であり、production render、creative final acceptance、production carrier approval、rights automation、real material slot-fill、G-27復帰、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 real-estate YMM4 diagnostic probe の human GUI review は `revise_probe` として受け、次は bounded polish revision に限定する。** | production 承認へ進む / probe を完了扱いにする / 新variantへ逃がす / human review result を記録し、同一probeのpolish revisionへ限定する | ユーザー確認では YMM4 openability、focal chain、caption reserve、host role、実在サービス/物件感、diagnostic boundary は pass/clear だが、callout readability は `pass_partial`、alignment/polish は `partial` であり、黄色い線の処理・矩形内テキスト整列・微妙な視覚ズレが認知摩擦として残ったため。`docs/verification/G28-REAL-ESTATE-YMMP-PROBE-HUMAN-REVIEW-2026-06-07.md` に記録し、次の許可範囲は同じ `variant_id=g28_ldc_real_estate_information_gap` / diagnostic-only / production-candidate-false 境界を保つ polish revision のみ。production render、creative final acceptance、production carrier approval、rights automation、real material slot-fill、外部画像/URL/raw reference、G-27復帰、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 `real_estate_information_gap` accepted diagnostic variant を self-contained YMM4-compatible probe へ進める。** | plan のまま待つ / production carrier approval へ進む / new G-28 variant を作る / accepted済み variant から shapes/text only の `.ymmp` diagnostic probe を作る | `g28_lecture_diagram_carrier_real_estate_information_gap_v1` は human decision が `accept_as_diagnostic_direction`、readback が `passed` であり、直前 plan が YMM4-compatible probe を次 slice として許可しているため。今回の成果は `scripts/build_g28_real_estate_ymmp_probe.js` と `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.{ymmp,readback.json,report.md}` に限定し、classification `pass_ymmp_probe_created` まで確認する。これは diagnostic GUI review surface であり、production render、creative final acceptance、production carrier approval、rights automation、real material slot-fill、external image/URL/raw reference、G-27復帰、common foundation、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 `real_estate_information_gap` を最初の YMM4-compatible diagnostic probe 候補として計画する。** | すぐ `.ymmp` を作る / production carrier approvalへ進む / deferred carrierを先にprobe化する / accepted済み Lecture Diagram variant の probe plan だけ作る | `g28_lecture_diagram_carrier_real_estate_information_gap_v1` は `accept_as_diagnostic_direction` 済みで、readback も `diagnostic_only=true` / `production_candidate=false` / caption reserve clear / 3-node focal chain / 3 callouts を満たしているため、最初の YMM4-compatible probe 候補として最も摩擦が少ない。一方で今回の目的は plan 作成のみなので、`docs/verification/G28-REAL-ESTATE-YMM4-COMPATIBLE-PROBE-PLAN-2026-06-07.md` に item/group mapping、layer order、readback requirements、human GUI checklist、next slice options を固定し、`.ymmp`、render、production approval、creative final acceptance、rights automation、new variant、generator変更、G-27復帰、common foundation、ClipPipeGen、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 game-mechanics の `revise` は、まず diagnostic semantics clarification で閉じる。** | すぐ generator / JSON を変更する / 新variantを作る / YMM4 probeへ進む / 既存 semantics note で `判定 / 当たり判定` 中心の因果構造を明確化する | `g28_lecture_diagram_carrier_game_mechanics_explanation_v1` の人間decisionは `revise` だが、求められている修正は production 昇格ではなく「何を説明する carrier か」の明確化であるため。既存 3-node chain は維持し、`入力操作` -> `内部ルール / 判定` -> `画面上の結果` の middle node を first-review では `判定 / 当たり判定` として読む。`操作感` / `リスクとリターン` は補助 callout に留め、caption reserve、non-focal host、dense table回避、indexed whiteboard回避を維持する。今回 generator、new variant、JSON/readback/report rewrite、`.ymmp`、render、production carrier approval、creative final acceptance、G-27復帰、common foundation、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 diagnostic artifacts 6件の human decision を記録し、production には進めない。** | 全件accept扱いにする / reviseからgenerator変更へ進む / deferをproduction probe扱いにする / supplied human decisions だけを decision record に記録する | 人間decision が明示されたため、`docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` にそのまま記録する。generic Lecture Diagram skeleton と `real_estate_information_gap` は `accept_as_diagnostic_direction`、`game_mechanics_explanation` は `revise`、Map / Evidence・Source-Footage definition-only・Conversation / Buffer definition-only は `defer_to_ymmp_carrier_probe`。accept は diagnostic direction の承認のみであり、production carrier approval、creative final acceptance、`.ymmp`、render、G-27復帰、common foundation実装、RSS / NotebookLM には進まない。 |
| 2026-06-07 | **G-28 human decision record は、判断を捏造せず pending intake surface として作る。** | accept / revise / reject / defer をAgent判断で埋める / 新variantやgenerator変更へ進む / pending_human_decision の decision record を作る | 今回の prompt では人間側の accept / revise / reject / defer 判断がまだ明示されていないため。既存 diagnostic artifacts は readback-passed / diagnostic_only=true / production_candidate=false なので、次の成果物は `docs/verification/G28-DIAGNOSTIC-HUMAN-DECISION-RECORD-2026-06-07.md` に human input fields と allowed decisions を固定することに限定する。production carrier approval、creative final acceptance、`.ymmp`、render、G-27 revival、common foundation 実装、RSS / NotebookLM には進めない。 |
| 2026-06-07 | **G-28 は追加 variant 量産ではなく、既存 diagnostic artifact を人間が判定する review packet に進める。** | さらに Lecture Diagram variant を追加する / production carrier や `.ymmp` probe へ飛ぶ / common foundation 実装へ戻る / 汎用 diagnostic human review packet を作る | 現存する Lecture Diagram generic skeleton、`real_estate_information_gap`、`game_mechanics_explanation`、Map / Evidence skeleton は readback-passed diagnostic-only であり、次の摩擦は生成不足ではなく人間が `accept_as_diagnostic_direction` / `revise` / `reject` / `defer_to_ymmp_carrier_probe` を返す decision surface の不足にあるため。今回の artifact は `docs/verification/G28-DIAGNOSTIC-HUMAN-REVIEW-PACKET-2026-06-07.md` に限定し、新しい JSON/HTML/readback/generator、production carrier approval、creative final acceptance、`.ymmp`、render、G-27 revival、RSS / NotebookLM、Codex Worker Orchestration 実装には進めない。 |
| 2026-06-05 | **G-28 game-mechanics human review は `revise` として受け、Lecture Diagram Carrier の diagram semantics note に落とす。** | acceptとして次へ進む / Source-Footageへ切り替える / 新variantを生成する / 既存carrierのsemantics noteに限定する | ユーザーが「入力操作 -> 内部ルール / 判定 -> 画面上の結果」は正しいが、`内部ルール` が抽象的なので `判定 / 当たり判定`、`無敵時間`、`硬直` のような具体内部処理例を1つ選べる余地を残したい、と返したため。最初のreview主軸は `判定 / 当たり判定`、`操作感` と `リスクとリターン` は補助扱いにする。host は non-focal、medium caption 前提、画面内textは短く保つ。新variant、Source-Footage、`.ymmp`、render、production timing、creative final acceptance には進めない。 |
| 2026-06-05 | **G-28 game-mechanics review packet までの文脈を repo-local handoff として保持し、別端末再開用 prompt を更新する。** | チャット報告だけで止める / AGENTS.md に長文追記 / runtime-state・decision log・USER_COPYPASTE_BLOCKS に最小追記して push | ユーザーが「全コンテキストをプロジェクトに保持しつつ、ローカルをリモートに反映」「別端末からすぐ再開」を明示したため。最新の実体は `docs/verification/G28-GAME-MECHANICS-HUMAN-REVIEW-PACKET-2026-06-05.md` までで、G-28 は diagnostic-only、Source-Footage は future-only backup、次は human `accept` / `revise` / `reject` 記録または design-only checklist に限る。AGENTS.md と既存 generated artifact は触らず、`.ymmp`、render、production timing、creative final acceptance、G-27、RSS / NotebookLM へは進めない。 |
| 2026-06-05 | **G-28 toolbox を、次の1 shot の carrier selection worksheet に落とす。** | 実際の shot が来るまで待つ / 新しい skeleton や theme variant を増やす / 既存 generated artifact を変更する / 空テンプレートと判定規則だけを verification artifact にする | 次の制作時の摩擦は「Lecture / Map / Source-Footage / Conversation のどれを選ぶか」なので、現存 toolbox に基づき shot purpose、source material、visual evidence type、claim type、required viewer action、caption density を埋めれば carrier を選べる worksheet を作るのが最小で有効。Source-Footage と Conversation / Buffer は未着手のまま進む条件だけを明示し、source intake、image path/URL、`.ymmp`、render、production timing、creative final acceptance、G-27 復帰、RSS / NotebookLM には進めない。 |
| 2026-06-05 | **G-28 archetype 群は、追加サンプルではなく画面設計の道具箱として整理する。** | 新しい theme variant を増やす / 新しい carrier skeleton を増やす / 既存 artifact を変更する / 4 archetype の目的・適用範囲・readback 状態・production 前判断を1つの verification artifact にまとめる | G-28 の次の詰まりは標本数ではなく、次の shot でどの carrier を選ぶかの判断摩擦に移ったため。Lecture Diagram と Map / Evidence は readback-passed の diagnostic-only、Source-Footage と Conversation / Buffer は definition-only と明示し、source intake、image path、URL、`.ymmp`、render、production timing、creative final acceptance、G-27 復帰、RSS / NotebookLM には進まない境界を維持する。 |
| 2026-06-05 | **G-28 Map / Evidence Carrier 完了後の全コンテキストを repo-local handoff として保持し、`origin/master` に反映する。** | チャット報告だけで止める / AGENTS.md に長文追記 / runtime-state・decision log・USER_COPYPASTE_BLOCKS に最小追記して push | ユーザーが「上記までで全コンテキストをプロジェクトに反映してプッシュ」を明示したため。通常再開入口を肥大化させないため `AGENTS.md` は触らず、現在位置は `docs/runtime-state.md`、判断履歴は本 decision log、ChatGPT へ貼る最新再開 prompt は `docs/USER_COPYPASTE_BLOCKS.md` に分離する。Map / Evidence は diagnostic skeleton であり、production carrier approval、`.ymmp`、render、creative final acceptance、G-27 promotion、RSS / NotebookLM へは進めない。 |
| 2026-06-05 | **G-28 Map / Evidence Carrier は、Lecture Diagram Carrier の追加 theme variant ではなく、別 archetype の diagnostic skeleton として生成する。** | Lecture Diagram variant を量産する / 実地図や衛星画像を取り込む / 新しいSCS typeを増やす / 既存SCSの `center-focal` に写像した Map-Evidence skeletonを追加 | ユーザーが地図・統計・産業立地・企業分布・人口・市場・地域差・出典付き論証を「飾りではなく論証装置」として扱う carrier archetype を1つだけ作るよう指定したため。今回の skeleton は `G28_MEC_EvidenceSurface` を focal anchor、3つの annotation slot、bounded source note、non-focal hosts を持つが、real map / satellite image / image path / URL / raw reference / `.ymmp` / render / production timing / creative final acceptance / source footage / gameplay screenshot intake には進まない。SCS mapping は `center-focal` で、新しい composition type は増やさない。 |
| 2026-06-05 | **G-28 `game_mechanics_explanation` は、Source-Footage Carrier へ進まず、Lecture Diagram Carrier の2つ目の theme-specific diagnostic variant として生成する。** | 不動産variantだけで止める / gameplay screenshot や source footage を取り込む / Lecture Diagram上の `center-focal` diagnostic variantを追加 | ユーザーが G-28 generic capability の確認として、ゲームレビュー / ゲームメカニクス解説へ転用できるかを1variantだけ検証するよう指定したため。今回のvariantは `入力操作` -> `内部ルール` -> `画面上の結果` の focal-chain semantics と、`操作感` / `判定 / 当たり判定` / `リスクとリターン` の callout semantics を持つが、source footage carrier ではなく、画像・URL・raw reference・production render・creative final acceptance・`.ymmp` 生成には進まない。 |
| 2026-06-05 | **G-28 `real_estate_information_gap` variant 完了後の全コンテキストを repo-local handoff として保持し、`origin/master` に反映する。** | チャット報告だけで止める / AGENTS.md に長文追記 / `runtime-state.md` と decision log に最小追記して push | ユーザーが「全コンテキストをプロジェクトに保持しつつ、ローカルをリモートに反映」を明示したため。通常再開入口を肥大化させないため `AGENTS.md` は触らず、現在位置は `runtime-state.md`、判断履歴は本 decision log に限定して保存する。既知未追跡 `.claude/worktrees/` と `samples/2026-05-16.ymmp` は local residue のまま触らない。 |
| 2026-06-05 | **G-28 `real_estate_information_gap` は、G-27 復帰や production carrier 昇格ではなく、既存 Lecture Diagram skeleton の theme-specific diagnostic variant として生成する。** | 汎用 skeleton のまま停止 / G-27 carrier path へ戻る / `.ymmp` production carrier へ飛ぶ / `--variant real_estate_information_gap` で JSON/HTML/readback/MD を生成 | ユーザーが theme を `real_estate_information_gap`、readback variant id を `g28_ldc_real_estate_information_gap` に固定し、approved carrier 不在で止めないこと、production / render / creative acceptance / source footage / image path / URL / RSS / NotebookLM に進まないことを明示したため。variant は `center-focal` の Lecture Diagram 上で `元付情報` -> `ポータル掲載` -> `借主判断` の3ノード focal-chain semantics と、`情報遅延` / `掲載粒度の欠落` / `仲介インセンティブ` の3 callout semantics を持つが、slot-fill済み production text ではない。根拠: user prompt + G28 Lecture Diagram spec + generated readback `status=passed` |
| 2026-06-05 | **G-28 Lecture Diagram Carrier は、production approval 待ちで停止せず、Agent-owned diagnostic skeleton / readback artifact まで進める。** | 人間がcarrierを作るまで停止 / `.ymmp` zero-generationへ飛ぶ / JSON/HTML/readback skeletonで実体化 | ユーザーが Human Authority 化 / carrier 官僚制の再発防止を明示したため、creative final acceptance と diagnostic skeleton generation を分離する。現行 G-28 v0.1 は `.ymmp` zero-generation を非目的に置くので、このスライスでは `docs/verification/G28-LECTURE-DIAGRAM-CARRIER-SPEC-2026-06-05.md` と `samples/_probe/g28/lecture_diagram_carrier_skeleton_*` の machine-readable artifact で frame contract / layer order / caption reserve / focal area / host role / callout count を閉じる。根拠: user prompt + REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md + SCENE_COMPOSITION_SCHEMA.md |
| 2026-06-05 | **G-28 の初回参照画像入力を受領済みとして扱い、画像丸コピーではなく reference style brief へ抽出する。** | input-wait 継続 / 画像を素材化 / G-27 carrier 待ちへ戻す / G-28 style brief に抽出 | ユーザーが 7 枚の参照画像と extraction 方針を渡したため、G-28 の parked 状態を解除し、`docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md` と SCS に沿って per-image extraction、共通画面文法、generic carrier archetype、YMM4 item/group 構成案へ変換するのが最小前進。根拠: runtime-state 2026-06-05 handoff + docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md + SCENE_COMPOSITION_SCHEMA.md |
| 2026-06-04 | **G-28 を parked / input-wait として保持し、詳細 handoff と ChatGPT 貼付用 block を repo 内に保存する。** | runtime-state の短文だけに留める / AGENTS.md に長文手順を追加 / verification handoff + USER_COPYPASTE_BLOCKS に分離 | ユーザーは全コンテキストを project に保持したうえで remote 反映を求めている。一方で通常再開入口を重くすると drift するため、現状態は `runtime-state.md`、詳細な G-28 parking context は `docs/verification/G28-REFERENCE-INPUT-WAIT-HANDOFF-2026-06-04.md`、ユーザーが ChatGPT へ貼る reusable block は `docs/USER_COPYPASTE_BLOCKS.md` に分離する。 |
| 2026-06-04 | **G-27 を active production carrier blocker から外し、case-specific legacy / reference evidence として保持する。後継として G-28 Reference-Driven Generic Screen Carrier を proposed 登録する。** | G-27 carrier 待ちを継続 / diagnostic carrier を production 昇格 / G-27 を削除 / 汎用 screen carrier issue へ再生成 | G-27 の diagnostic carrier、review console、SCS lessons は有用だが、不動産DX固有の carrier 未受領を active next action として延命すると制作摩擦が増える。画像丸コピーではなく、参照画像から構図・密度・余白・色階層・視線誘導・UI感を抽出して SCS / YMM4 carrier handoff へ変換する汎用能力に再定義する方が、NLMYTGen の downstream adapter / YMM4 接着層の責務に合う。根拠: INVARIANTS §Responsibility Boundaries + FEATURE_REGISTRY G-27/G-28 + docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md |
| 2026-06-04 | **Codex 側の作業完了・停止・確認報告は、ChatGPT へ一発コピーできる単一コードブロックを最後に含める。** 正本の通常再開は引き続き `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md` で、詳細テンプレは `docs/USER_COPYPASTE_BLOCKS.md`、対話上の report contract は `docs/INTERACTION_NOTES.md` に置く。 | チャットだけで運用 / AGENTS.md に長いテンプレを追加 / interaction note + reusable copypaste block に分ける | ユーザーは Codex の報告を ChatGPT 側へ毎回貼り付けて監修するため、ドラッグ選択なしでコピーできる唯一の正本が必要。一方で `AGENTS.md` を運用マニュアル化すると再開入口が重くなるため、入口・現状態・対話契約・ユーザー用テンプレを分離する。 |
| 2026-06-03 | **ChatGPT / Codex 間で再利用する長文 Prompt / PowerShell / 停止文 / 報告文を、Agent再開マニュアルではなくユーザー用コピペ資産として保存する。** 正本は `docs/USER_COPYPASTE_BLOCKS.md`。通常再開で読む3点は増やさず、active next action や runtime-state の代替にも使わない。 | 次Agentへのキックスタートとして扱う / repoに残さない / ユーザー用保存版として残す | ユーザーの目的は次Agentへ作業を実行させることではなく、毎回長文を手で組み立てる摩擦を減らすことだったため。RSS / OPML / NotebookLM source-pack selection は NLMYTGen では旧水路であり、保存版内でも downstream adapter 境界と G-27 分離を保つ必要がある。 |
| 2026-06-03 | **RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection を NLMYTGen の active lane から外し、`newsroom-yt-pipeline` 側の上流編集責務として扱う。** NLMYTGen 側の既存 RSS 実装や過去証跡は削除せず、legacy / reference-only として残す。今後の NLMYTGen は newsroom-produced packet / transcript / ScriptIR / VisualIR / export bundle を受け取ってから、YMM4 CSV、YMM4 adapter、Review Console、proof ingest へ落とす。 | NLMYTGenでOPML復元とsource-pack選定を継続 / RSS実装を削除 / active laneからretireしてnewsroomへ寄せる | newsroom-yt-pipeline が source ingest、article ledger、story clustering、scoring、NotebookLM packet preparation、script workbench interfaces、visual planning interfaces、rights manifests を持つ上流編集repoであり、NLMYTGen の価値経路は downstream adapter と YMM4 production proof にあるため。根拠: INVARIANTS §Responsibility Boundaries + runtime-state 2026-06-03 handoff |
| 2026-06-01 | **G-27 `G27_PublicVsBrokerDB` carrier は production slot-fill へ進む前の境界物として必要。ただし user が明示すれば既存 diagnostic carrier を production carrier に昇格する選択肢もある。** デフォルトは人間が YMM4 で最小 stable carrier を作る。速度優先なら `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp` を昇格対象にできるが、runtime-state と readback/boundary 記録を更新してから進む。`samples/2026-05-16.ymmp` は item 3 件のみで不可。 | 新規最小 carrier / diagnostic carrier 明示昇格 / carrier なし diagnostic 継続 | YMM4 が制作基盤で Python/assistant は CSV/IR/registry/post-import `.ymmp` patch の接着層であるため、assistant が diagnostic raw geometry を黙って production layout にしてはいけない。carrier は美麗な完成画面ではなく、固定 `G27PBD_*` item 名、card 数、caption safe area、短 Remark、後段 patch で触らない geometry/color/font/layout を固定する台座であるため。 |
| 2026-05-27 | **A-04 RSS Reader Sync v1.1 は `master` / `origin/master` に fast-forward 統合済み**。統合範囲は `da30ff2..1599cf5` で、OPML source sync、fetch coverage、Inoreader read-only adapter、`rss-smoke` sanitized evidence、live-smoke runbook、RSS tests を含む。PR は個人開発のため省略し、merge 前後に RSS narrow tests `41 passed`、full `uv run pytest` `525 passed, 25 skipped`、CLI help smoke、`git diff --check` を確認した。 | PR 作成 / master へ fast-forward / RSS branch 継続 | branch diff が RSS docs/code/tests + `.gitignore` に閉じ、G-27 / Baseball / Thumbnail / GUI / unrelated path と raw OPML / token / private feed URL / article body / live smoke evidence の混入がなかったため。OPML は v1 source of truth、Inoreader は read-only adapter のままで、DB・OAuth refresh・既読同期・購読変更・background polling は実装しない。 |
| 2026-05-26 | **A-04 RSS lane は `codex/rss-reader-sync-clean` を remote handoff 正本にする**。OPML sync v1、fetch coverage、Inoreader read-only adapter、`rss-smoke` one-command sanitized evidence、live-smoke runbook までを `origin/codex/rss-reader-sync-clean` に push 済み。別端末では `docs/runtime-state.md` と `docs/verification/RSS-LIVE-SMOKE-RUNBOOK-2026-05-26.md` から再開する。 | clean RSS branch を正本化 / G-27 差分混在 branch を継続 / master 直作業 | 既存作業ツリーには G-27 差分が残っているため、RSS PR/再開経路を汚さないには `origin/master` ベースの clean branch が安全。RSSの残作業は実OPMLまたは一時 Inoreader token による live smoke だけで、raw OPML/token/private URL/full body は commit しない。 |
| 2026-05-25 | **A-04 RSS Reader Sync v1 は OPML export を先に共通正本化する**。`fetch-topics` は URL 直接指定を維持しつつ `--opml` で人間側RSSリーダーの購読一覧をそのままAI側取得対象へ使い、`list-feed-sources` でAIが見る一覧を確認できるようにする。Inoreader OAuth / API 直結は後続の read-only adapter 候補として文脈だけ保存し、このスライスでは認証・DB・既読同期を増やさない。 | Inoreader 直結から開始 / OPML 正本化から開始 / 既存URL指定のみ維持 | Inoreader はOAuth app・token保管・利用条件・rate limit を伴うため、先に依存追加なしで「人間一覧とAI取得一覧が一致する」土台を閉じる方が安全。A-04 はL1入力取得であり、NotebookLM代替や制作artifact生成へ広げないため |
| 2026-04-30 | **G-26 目的別演出制作を `build-motion-recipes` pipeline として実装**。brief `samples/recipe_briefs/g26_motion_recipe_brief.v1.json`、effect catalog / concrete samples / motion library / optional composition corpus を読み、`_tmp/g26/recipe_pipeline/g26_motion_recipe_review_v1.ymmp`、readback JSON、manifest MD を生成する。初期 recipe は `nod_*` / `jump_*` / `panic_crash` / `shocked_jump` / `surprised_chromatic` / `anger_outburst` / `shobon_droop` / `lean_curious` の 12 件。 | 都度手作業で試作 / 既存サンプル再配置だけ / intent-first recipe pipeline | ユーザーの負担は「毎回一から演出を作る」ことなので、IR 作業と同じく意図・候補・readback・採否を machine-readable artifact に固定する必要があるため。effect catalog を機械参照し、最終的な動きから逆算する経路を CLI に閉じる。 |
| 2026-04-30 | **G-26 evidence gate の過剰解釈を修正し、目的別 recipe lab を正当な assistant 作業として扱う**。`_tmp/g26/recipe_lab/g26_goal_motion_recipe_lab.ymmp` は既存 YMM4-saved canvas `samples/canonical.ymmp` と既存 template source `samples/templates/skit_group/delivery_v1_templates.ymmp` から作成した、うなずき・ジャンプ・傾き・chain の review artifact。readback は openability pass / recipe GroupItems 12 / ImageItems 24 / POSIX asset paths 0。 | operator-authored source 待ちだけにする / 既存 sample を再配置するだけ / assistant が目的別 review lab を作る | ユーザーの要求は「既存動作の散布」ではなく「うなずき」「ジャンプ」のような目標を設定して試作すること。`compatible_after` / `forbidden_after` の推測禁止は contract 昇格条件であり、既存 YMM4 source をコピーして transform 値を調整する review sample 作成を止める理由ではないため。 |
| 2026-04-30 | **G-26 Evidence Gate は machine pass / visual not recorded / tilt-chain source absent として扱う**。`_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp` は openability pass、inserted GroupItems 3、POSIX asset paths 0。repo-local `.ymmp` 53 本の scan では tilt / chain Remark が見つからないため、`tilt` は contract 外、`compatible_after` / `forbidden_after` は `unknown` 維持。 | 推測で compatibility を埋める / machine pass だけで production 接続 / visual・tilt・chain を別 gate に分離 | 画面表示の真偽は YMM4 visual confirmation なしに判定できず、chain source なしで相性を埋めると G-25 の accidental composition failure を再発させるため。assistant 側で閉じられる machine readback は閉じ、観測不能部分だけを正確に残す。 |
| 2026-04-30 | **G-26 Phase 3 仮 contract と screen review を強進行で作成**。`dominant_channels` は `VFX:<EffectType>` を含め、Rotation 系の `anchor_dependency` を一級フィールドにする。`_tmp/g26/draft_contracts/*.json` と `_tmp/g26/screen_review/g26_motion_primitive_compact_review.ymmp` を作成し、readback は openability pass / inserted GroupItems 3 / POSIX asset paths 0。 | 追加確認待ち / contract のみ / contract + screen review | ユーザー要望は別レーン報告の妥当性確認だけでなく、推奨対応の自動適用と「画面上でまともにサンプルが見えていない」問題の前進だったため。G-24 production へ接続せず、既存の YMM4-saved seed + skit_group compact review 経路で安全に画面確認 artifact を作るのが最短だった。 |
| 2026-04-30 | **G-25 の creative acceptance を negative として閉じ、G-26 motion primitive grammar / compatibility probe を起票**。G-25 review はYMM4で開けるが、`nudge / scale / rotate / effect_reuse` は動きのvariationとして使えない。 | G-25候補を調整して継続 / productionへ接続 / G-26へ切替 | ユーザー確認で、うなずき・退場・小ジャンプ・傾きの機械的な組み合わせが、反対方向の傾き、傾いたままの退場、傾いた小ジャンプなどの不自然な動きを生むことが分かったため。次は座標差分ではなく、motion primitive の開始姿勢・終了姿勢・方向意味・reset policy・相性を扱う。 |
| 2026-04-30 | **G-25 review `.ymmp` の openability 修復を C案ベースで実施**。`LayerSettings` は array ではなく `{ "Items": [...] }` object をYMM4期待形として扱い、`probe-ymmp-variations -o` は template/stub source を直接 review surface にせず、必要時に `--review-seed` で YMM4 保存済み full project canvas を使う。 | guard反転のみ / full seed化のみ / guard反転 + full seed化 | ユーザー環境のYMM4エラーは `YukkuriMovieMaker.Project.LayerSettings` object 要求を示しており、repo内 `.ymmp` も object 形が主流だったため。JSON可読性とYMM4実読込schemaを混同し、stubをopenable artifactへ昇格させたことが不安定化の本体だった。 |
| 2026-04-29 | **G-25 YMM4 property-based variation probe を実装し、手動演出からの保守的な派生生成を初回検証へ進める**。`probe-ymmp-variations` は `Remark` clip、`X/Y/Zoom/Rotation`、反転 route、`VideoEffects` fingerprint を JSON report にし、`-o` 指定時だけ compact review `.ymmp` を追加生成する。 | さらに計画保留 / G-24 に直結 / 独立 probe として実装 | ユーザーの痛点は「手動演出のタグ・座標・反転・拡縮から variation を自動生成できるかが未試行」だったため。G-24 production placement に混ぜず、`.ymmp` ゼロ生成や Python 画像生成にも戻らない、限定 readback / derivative review として最小検証する。 |
| 2026-04-29 | **汚染パッチ由来の rejected / hold を手段単位に再定義**。B-10 旧 `--emit-meta`、C-02/C-04/C-05 の Python 万能制御、D-01 の Python 画像生成、F-03 の YMM4 表示エミュレーションは `method-rejected`。一方、診断 JSON / IR / manifest / packaging brief、G-24 template source placement、H-02 thumbnail slot patch、H-01/H-02 由来の metadata draft は `goal-allowed` / `successor-lane` として扱う。 | 目的ごと拒否 / 手段単位で拒否 / 一括再有効化なし | 旧拒否理由が「動画品質を上げるためのメタデータ・演出制御・サムネ・YouTube metadata」まで萎縮させるリスクがあったため。禁止対象を危険な生成・エミュレーション手段に限定し、承認済み artifact 経路を邪魔しないため。 |
| 2026-04-27 | **ドキュメント汚染を根絶し、再開時の入口を最小正本へ戻す**。resume 用プロンプト導線を削除し、`verification/` は証跡置き場に降格、`USER_REQUEST_LEDGER.md` は現在有効な要求だけへ圧縮、固定日付風のルール見出しと旧背景アニメ/S6 再採用を廃止する。 | テンプレ維持 / 古い証跡を正本化 / 最小正本へ集約 | 再スタート時の読了過多と「正本っぽい古い文書」による判断汚染が、G-24 `delivery_nod_v1` の作業接続性を落としていたため。 |
| 2026-04-27 | **次期ロードマップは G-24 `delivery_nod_v1` gate-shaped sequence から始める**。formal plan は `delivery_nod_v1` 未報告 / PASS / FAIL / 新規制作案件のどれかを冒頭で宣言し、未報告なら hands-on acceptance、PASS なら `nod` 昇格 + `deny_oneshot`、FAIL なら failure class 分解から開始する。 | 背景アニメ/S6 に戻す / 新 FEATURE を増やす / G-24 gate 分岐で開始 | レガシードキュメント整理後の bottleneck は `audit-skit-group` readiness と user-owned export proof の分離であり、`exact` を export proof と読み替えると status drift が再発するため。根拠: `runtime-state.md` next_action + `verification/P02-production-adoption-proof.md` + `INTERACTION_NOTES.md` TEMPLATE_FORMALISM |
| 2026-04-23 | **Keep the G-24 `nod` cycle at readiness-PASS, but do not promote to `direct_proven` yet**. Assistant rechecked `delivery_nod_v1` on the canonical/proof corpora and confirmed proof-corpus `group_motion_changes=0`. Because the repo still does not track a discrete canonical-project `delivery_nod_v1` copy, Phase 1 is corrected to YMM4 author/export from `samples/haitatsuin_2026-04-12_g24_proof.ymmp` or an equivalent local project, starting from Layer 9 `GroupItem` Remark `haitatsuin_delivery_main`. `skit_group.intent.nod` stays `template_catalog_only` until manual acceptance plus standalone export are confirmed. | Promote now / assume a tracked copy exists / keep the gate but correct the packet | Readiness is already proven, but assuming a nonexistent tracked copy would corrupt handoff. This keeps assistant-owned facts and user-owned export clearly separated while preserving the cautious-gate order. |
| 2026-04-21 | **starter 2 件の standalone native template export を完了扱いにする**。user report により `delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` は名前そのままの GroupItem template として登録済みで、body/face の `ImageItem` 2 点も含めて保存された。これにより starter 2 件は canonical-project copy / production adoption proof / standalone export の 3 点セットを満たしたとみなす。 | export 保留 / starter 2 件だけ export / 5 件一括 export | cautious gate の目的は「急ぎすぎず proof 後に資産化すること」だった。必要最小限の 2 件だけを先に独立資産化したほうが、Atlas 昇格と次の拡張 frontier を明確に切り分けられるため |
| 2026-04-21 | **G-24 cautious gate の Phase 2 を PASS として閉じる**。`samples/haitatsuin_2026-04-12_g24_proof.ymmp` を canonical-anchor + voice-anchored production proof ymmp として採用し、`samples/_probe/skit_01/skit_01_ir.json` に対する `audit-skit-group` と `apply-production --dry-run` を通す。starter 2 件は `exact`、非 starter 3 件も `exact`、`group_motion_changes=0` を確認したため、template-first が production proof 上でも成立したとみなす。 | proof 追加保留 / Phase 2 PASS / すぐ Atlas 昇格 | cautious gate の目的は standalone export 前に content/workflow proof を 1 件閉じることだった。proof ymmp が用意できた以上、そこで止めず repo-local で成立条件を実測し、昇格条件と export 判断を分離したほうが次の判断が明確だから |
| 2026-04-21 | **starter 2 件の manual acceptance を PASS として閉じる**。`delivery_enter_from_left_v1` / `delivery_surprise_oneshot_v1` の loop・body-face drift は無く、`enter_from_left` に紛れていた退場設定は YMM4 上でカット済みとして扱う。以後の blocker は acceptance ではなく、canonical anchor を持つ voice-anchored production ymmp 不在に切り替える。 | acceptance 継続保留 / PASS 化 / すぐ export | visual acceptance の論点は user 確認で閉じたため。今後は同じ見え方確認を繰り返すより、Phase 2 proof を閉じるための ymmp 条件に集中したほうが bottleneck 直撃だから |
| 2026-04-21 | **G-24 の standalone export を「受入+P02 先行」へ固定**。順番は `manual acceptance` → `1 件の production adoption proof` → `standalone native template export`。proof の内容候補は `skit_01_delivery_dispute_v2` + `samples/_probe/skit_01/skit_01_ir.json` に固定するが、現状 repo には canonical anchor を持つ voice-anchored production ymmp が無いため、Phase 2 は未成立のまま保守的に据え置く。 | 受入後すぐ export / production proof を後回し / 受入+P02 先行 | starter 2 件は repo 内 copy として観測できるが、standalone export を急ぐと content proof と workflow proof が再び混線するため。old corpus の stale gate に戻らず、exact/fallback/manual_note を 1 件で閉じてから昇格させるため |
| 2026-04-21 | **G-24 の初回スターターバッチは 2 件の canonical-project copy として観測済み**。`samples/canonical.ymmp` には frame 306 `delivery_enter_from_left_v1` / frame 658 `delivery_surprise_oneshot_v1` が追加され、assistant は registry / preflight / P02 / handoff をこの project-resident copy に同期した。`delivery_deny_oneshot_v1` / `delivery_exit_left_v1` / `delivery_nod_v1` は registry catalog と canonical-corpus preflight exact を維持するが、starter 完了扱いには含めない。Capability Atlas は `template_catalog_only` を据え置く。 | 5 件一括 / 2 件スターター / canonical のみ | bottleneck は「2 件をまず作って repo 内で観測できる状態にすること」だった。現状の証跡は canonical project 内 copy までなので、過剰に standalone native template library 完了へ昇格させないため |
| 2026-04-20 | **G-24 の正規入口を CLI preflight `audit-skit-group` に固定**。`patch-ymmp` / `apply-production` でも `--skit-group-registry` 指定時は同じ canonical anchor / exact / fallback / manual_note 監査を先に通し、anchor 不在・曖昧・registry 不正なら fail-fast する。 | docs-only 運用継続 / 暫定 script のみ維持 / CLI preflight 化 | `skit_01` を motion proof と template-first proof の間で曖昧にしないため。repo 内 artifact だけで G-24 成立/不成立を assistant-owned に切れる入口が必要で、しかも patch/apply の前に同じ gate を通す必要があるため |
| 2026-04-20 | **ManualSample 非依存の Capability Atlas を operator 正本として追加**。`IR -> registry -> ymmp` の接合点で route を `direct_proven` / `template_catalog_only` / `probe_only` / `unsupported` に分類し、raw effect 名から IR を逆算しない原則を固定する。 | docs 横断のまま運用 / probe packet のみ増やす / Capability Atlas 追加 | ManualSample が無くても『何ができるか』『どこから先が補助か』を repo 内 artifact だけで判断できる必要があるため。G-24 主軸を崩さず、timeline/effect の整理を operator が即利用できる形にするため |
| 2026-04-20 | **`samples/canonical.ymmp` を official canonical anchor artifact として採用**。`haitatsuin_delivery_main` / Layer 9 / ImageItem-only / 左向き基準姿勢を canonical fact とし、`audit-skit-group` success を repo proof に昇格。ただし派生 native template asset 群は未成立のため、intent 側は `template_catalog_only` のまま据え置く。 | canonical を informal sample 扱い / canonical adoption packet 追加 | old corpus の `CANONICAL_GROUP_REMARK_MISSING` を解消しつつ、G-24 completion を過剰宣言しないため。canonical anchor proof と derived asset proof を分離して handoff できるようにするため |
| 2026-04-20 | **`skit_01` の ManualSample gate を workflow breakage として固定し、repo 内 artifact-only audit へ切り替える**。欠落した `_tmp/skit_ManualSample_01.ymmp` を user に再作成させない。正本 [skit_01-workflow-breakage-audit-2026-04-20.md](verification/skit_01-workflow-breakage-audit-2026-04-20.md) / `samples/_probe/skit_01/audit_skit_01_proof.py` | stale handoff を維持 / user に ManualSample 再作成依頼 / repo artifact-only audit | `runtime-state.md` が存在しない ManualSample を参照し、proof docs/prompt が `_tmp/skit_01_v2.ymmp` を指す一方で surviving artifact は `_tmp/skit_01_v2_verify.ymmp`。registry も CLI 未消費のため、現状は G-24 workflow proof ではなく mechanical motion proof と扱うのが正確だから |
| 2026-04-17 | **茶番劇演者の主経路を template-first に固定**。配達員等の外部素材演者は `speaker_tachie` の `motion` と混同せず、**GroupItem canonical template → 小演出テンプレ量産 → production で template 解決 + fallback + manual note** を正本化。[SKIT_GROUP_TEMPLATE_SPEC.md](SKIT_GROUP_TEMPLATE_SPEC.md) | `motion` 拡張を主軸 / body_map 旧案継続 / template-first | 既存コードの route contract は `TachieItem` / Layer 0 背景 / Group geometry に分かれており、茶番劇演者の量産には直結しない。production bottleneck は direct write 不足より template 資産不足にあるため |
| 2026-04-13 | **茶番劇 E2E 実演 Phase 1/2 PASS**: face 138 + idle_face 16 + slot 10 + motion 6 を IR→apply-production→YMM4 で実証。src/ 変更なし。正本 [CHABANGEKI-E2E-PROOF-2026-04-13.md](verification/CHABANGEKI-E2E-PROOF-2026-04-13.md) | 既存 done 機能のみ / 新規実装 | トラック A（演出 IR 実戦）のサブセットとして、追加コード変更なしで E2E パイプライン動作を実証 |
| 2026-04-13 | **表情指定: テンプレ（プリセット名）のほうが実用的**。パーツ個別指定（face_map の Eyebrow/Eye/Mouth パス）だと YMM4 上で「カスタム」表示になり、運用上不便。将来の face_map 構造見直しの根拠 | パーツ指定維持 / テンプレ指定移行 | オペレータフィードバック。E2E Phase 1/2 で発見 |
| 2026-04-13 | **体テンプレ構想**: 別体素材（配達員等）にゆっくり頭を重ね、テンプレ蓄積→IR で指定する将来像。グループ制御で移動・拡大縮小は破綻なし。左右反転は素材分割が必要。FEATURE 起票は別ブロック。正本 [TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-ymmp-geometry-2026-04-13.md) §7 / [TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md](verification/TACHIE-BODY-FACE-SWAP-PREP-2026-04-13.md) §3.2 | 体テンプレ / パーツ差替（G-19）/ 保留 | オペレータ調査で YMM4 のグループ制御仕様を確認。IR + レジストリで制御する設計は overlay/bg と同型で実現可能 |
| 2026-04-12 | **P0 Block-A タスク再設計クローズ**: [P0-BLOCK-A-AND-PATH-A.md](verification/P0-BLOCK-A-AND-PATH-A.md) を正本化。[runtime-state.md](runtime-state.md) の P0 優先行を「C-09 必須」と読めないよう修正。Block-A＝S-4 読込エラーのみ／NotebookLM 準拠稿は経路 A で可 | 表を据え置き / 正本化 | CSV 手前で台本改善を前提にするとオペレータがブロックするため。機械再スモーク `samples/p0_steering_v14_2026-04-12_*` |
| 2026-04-11 | **正本の表現是正**: 「運用で二系統ある」という断定を撤回。**案件ごと可変**・現状が原文寄りでも本番固定ではない旨を bottleneck #1 と [P01-phase1-operator-e2e-proof.md](verification/P01-phase1-operator-e2e-proof.md) に反映。C-09 は任意、v14 は repo 検証アンカーと明記（[P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md) 等） | 二系統を正本に残す / 撤回 | ユーザー指摘: 二系統はエンティティ調査ではなく文書整理枠であり、本番方針まで固定しないため |
| 2026-04-11 | **開発正本から壁時計 cadence を除外**: 「2 週間」「週 1 回」「60〜90 分の固定ブロック」等の運用を repo 正本に置かず、**工程到達**（S-4 等）とオペレータセッション単位で記述する。反映: [P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md)、[OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md)、[LANE-C-operator-prep-2026-04-09.md](verification/LANE-C-operator-prep-2026-04-09.md)、[PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md)、`runtime-state.md` の `next_action` | 週次を正本に残す / 到達のみ | 開発リズムをカレンダー週に束縛しないため |
| 2026-04-11 | **P0 縦優先の固定**: 本編主軸＝AI監視 v14（`samples/v14_t3_ymm4.csv`）。Amazon Panopticon の B-11 §2 は **横**（別オペレータセッション）。正本 [P0-VERTICAL-STEERING-2026-04-11.md](verification/P0-VERTICAL-STEERING-2026-04-11.md)。P01 行 `p0_mainline_v14_steering_2026-04-11_a`（機械再スモーク）。`runtime-state.md` の `next_action` を P0 先頭へ。旧 T1 DOCSAMPLE の `validate-ir` は当時 PASS 済みだが、現行判断には使わない。 | Amazon 縦を先に採る / 本編のみ固定 | 縦スライスが品質横展開に埋もれないよう、YMM4 到達工程を 1 本に束ねるため（週 cadence は正本に置かない） |
| 2026-04-11 | レーン B（ファイル5）再検証: [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md) §8 を追記。正本コミット `927588e`、`validate-ir` / `apply-production --dry-run` を再実行し PASS。B-1/B-4/B-5 は従来方針継続。Custom GPT Instructions 突合はオペレータ（repo 外） | 再検証スキップ / 証跡のみ更新 | Prompt-B・ファイル2「プロンプト同期」の参照コミットを現 HEAD に更新するため |
| 2026-04-11 | **T0 クローズ（履歴）**: 旧コア計画で **T1-P2-DOCSAMPLE** / **T1-RUNBOOK-GUI** を起票し、開発フェーズを **T1** へ移行した。2026-04-27 の整理で当該計画文書は削除済み。 | 承認前に T1 着手 / T0 で差し替え協議 | 当時のゲート履歴のみ残す。現行の再開判断は `runtime-state.md` と G-24 gate を優先するため |
| 2026-04-10 | レーン B（ファイル5）再検証: [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md) §7 を追記。正本コミット `fb0659a`、`validate-ir` / `apply-production --dry-run` を再実行し PASS。B-1/B-4/B-5 は 2026-04-09 方針継続。Custom GPT Instructions 突合はオペレータ（repo 外） | 再検証スキップ / 証跡のみ更新 | 当時のプロンプト同期記録要件を満たすため。現行判断には使わない |
| 2026-04-10 | コア本開発の **フェーズ T0〜T3** と並行レーンの相性を旧文書で一時整理した。2026-04-27 の整理で旧設計文書・旧 Prompt ハブは削除済み。 | タスク設計なしで Prompt のみ / 設計ドキュメントを分離 | 履歴のみ残す。現行の作業接続は `runtime-state.md` / `verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md` / `verification/P02-production-adoption-proof.md` を使うため |
| 2026-04-10 | 並行レーン証跡・H-05（`score-thumbnail-s8`）・旧視覚品質パケット文書を master に統合コミットし、当時は次期コア実装をプラン設計・起票から再開するゲートに固定した。 | 実装を続行 / プラン入口で一旦止める | 2026-04-27 の整理後は、旧プラン入口ではなく `runtime-state.md` の G-24 gate から再開するため |
| 2026-04-09 | レーンB実施計画（Custom GPT / 2体分離）を実行し、運用固定を記録: [LANE-B-execution-record-2026-04-09.md](verification/LANE-B-execution-record-2026-04-09.md)。B-4 は「brief を会話ごとに先貼り」。B-5 は後続整理で、H-02厳密時も素案時も S8 を別レーンに分離 | 方針未固定のまま運用 / 連携方式を固定 | Instructions 側のドリフトを避け、案件ごとに迷わず切替できる最小運用を先に確立するため |
| 2026-04-09 | レーン E（サムネ S-8）の **repo 準備サイクルを完了・運用クローズ** とする: [LANE-E-S8-prep-2026-04-09.md](verification/LANE-E-S8-prep-2026-04-09.md) 運用クローズ節、P03 `lane_e_prep_2026-04-09_a`。公開直前の実 1 枚は P3・runbook トラック E で並行。**本開発幹へ復帰**（`runtime-state.md`） | 準備を開発ブロックに残す / クローズしてコアへ | 正本・チェックリスト・既定案件入力は repo 固定済み。YMM4 実書き出しは公開タイミングのオペレーションのためコア開発をブロックしない |
| 2026-04-09 | レーン B（GUI LLM 正本同期）の **repo 側準備を完了** とする: [LANE-B-gui-llm-sync-checklist.md](verification/LANE-B-gui-llm-sync-checklist.md)、[samples/packaging_brief.template.md](../samples/packaging_brief.template.md)、[gui-llm-setup-guide.md](gui-llm-setup-guide.md) の v4 正本優先化、runbook B-1/B-4/B-5 の整合。以降の主作業は **本開発幹**（`runtime-state.md` のコア・P0・B-11 ゲート等）。Custom GPT 等への実貼り付けはオペレータがチェックリストで実施 | 文書のみ完了扱い / 貼り付け完了までブロック | 正本と手順は repo に固定済み。GUI 同期は人間作業のため開発レーンをブロックしない |
| 2026-04-08 | P2 次サイクルで map 警告解消（`bg_anim_map` + `transition_map`）後に `test_verify_4_bg.ymmp` へ 4 セクション拡張適用を実施。`BG anim writes: 7` を確認 | 警告放置で拡張 / 先に警告ゼロ化 / bg_anim いったん停止 | 原因切り分けを明確化したうえで拡張でき、短サイクルの再現性を高められるため |
| 2026-04-08 | B-11 を最小クローズ（半分確認時点）し、改行 Pass / 辞書 0 をもって Gate B（運用側移行）を仮確定。P2 背景アニメ小規模適用を先行 | Gate A 維持 / Gate B 仮確定 / B-11 完全完了待ち | ループ停止を避けて最短で演出実戦へ入るため。`test_verify_4_bg.ymmp` で route は profile contract pass、`p2_bg_anim_small_scope.ir.json` で `BG anim writes: 2` を確認 |
| 2026-04-08 | B-11 AI監視 proof の取込後記録を集約し、Gate A（改行系支配）を確定。`runtime-state.md` の `next_action` / P0 説明を Gate 根拠付きへ更新 | 保留継続 / Gate 判定を先に固定 | 次プランを感覚で動かさず、4 区分実測（辞書 0 / 手動改行 5 / 再分割 10 / タイミング 0）で優先順位を固定するため |
| 2026-04-08 | 次以降の推奨プランを `runtime-state.md` に正本化（P0 Phase1 本番 1 本・P1 H-01 運用・P2 演出実戦・P3 サムネ・Parking motion ブランチ）。GUI CSV 同梱診断 JSON を Phase 1 導線に明記 | 暗黙の優先 / 文書固定 | 実制作 bottleneck 軽減レーンを再アンカーし、未承認実装を増やさない |
| 2026-04-07 | G-18 SE `AudioItem` 挿入を実装（`samples/AudioItem.ymmp` readback、`_apply_se_items`、テンプレート deepcopy または最小骨格）。旧 SE unsupported failure class を廃止 | ゲート維持 / 実装 | サンプルと骨格で write route を確定し、G-13 の `se` を mechanical scope まで拡張 |
| 2026-04-06 | G-15〜G-17 を実装（Micro `bg` 発話スパン / `overlay` 配列 / `--timeline-profile` + motion・transition・bg_anim マップ）。G-18 は AudioItem ymmp サンプル入手まで保留（verification に明記） | 一括 / ゲート付き | P2C に沿い SE write は corpus 確定後。G-12 `timeline_route_contract.json` と契約検証を先に置く |
| 2026-04-06 | 視覚三スタイル（挿絵コマ / 再現PV / 資料パネル）を IR 既存語彙にマッピングし doc 正本化。延伸は G-15〜G-18 proposed | 一括実装 / 文書→テンプレ→Writer→台帳パケット | patch 制約（単一 overlay・セクション bg のみ・motion 未書込）を隠さず、`VISUAL_STYLE_PRESETS.md` と v4 プロンプトで Writer と運用を揃える |
| 2026-04-06 | G-15〜G-18 のゲートと feat/phase2-motion-segmentation の保留判断を一度文書化。現在の正本は FEATURE_REGISTRY と各 verification 証跡に統合済み | 未承認を approved に昇格 / 文書のみ | プランに沿いゲートを明文化。実装は承認後のみ |
| 2025 | CLI パイプラインとして構築 | CLI / Web UI / Electron | 最小構成で検証可能 |
| 2025 | IP-01 No-Go | Go / No-Go | 要件未充足 |
| 2025 | Web UI / API / YouTube 連携は後回し | 優先 / 後回し | ロバスト性検証が先 |
| 2026-03-29 | B-10 (--emit-meta) を未承認で混入 | — | 未承認。後に rejected → コード除去 |
| 2026-03-30 | FEATURE_REGISTRY + AUTOMATION_BOUNDARY で機能管理 | 台帳管理 / ad-hoc | 未承認機能混入の再発防止 |
| 2026-03-30 | 自動化レイヤーを L1〜L4+GUI の5層で定義 | 5層 / 3層 / フラット | YMM4内部/外部の境界を明確化 |
| 2026-03-30 | Python での生成・レンダリングを手段単位で禁止 | method-rejected / 全面禁止 / 部分許容 | .ymmp ゼロ生成・音声合成・画像生成・YMM4 表示エミュレーションは不可。この教訓は「目的の禁止」ではなく「危険な手段の禁止」として扱う。CSV / IR / registry / manifest / brief 生成と、台本読込後 `.ymmp` への限定 patch は許容する。rejected: B-10, C-02, C-03, C-04, C-05, D-01, F-03 |
| 2026-03-30 | 外部メディア取得は分離設計で OK | L1拡張許容 / L2専念 | 取得機能と受け取り機能を分離すれば NLMYTGen に含めてよい。最終的に自動化する方針 |
| 2026-03-30 | WORKFLOW.md を S-0〜S-9 の全工程に再設計 | 全面改訂 / 部分改訂 | 前作業者がrejectedで隔離しただけでYMM4側の代替ワークフローが欠落していた。S-5(演出)が5行だけだった。rejected工程の代替手段を全てWORKFLOW.mdに記載 |
| 2026-03-30 | E-02 を先に仕様定義する | E-02 / A-04 / F-01 / 全件hold | ユーザーが選択。L2変換レイヤーで Python スコープ内に収まる唯一の候補 |
| 2026-03-30 | E-02 は単体では価値が薄い | 着手 / 先送り / E-01とセット | YouTube Studio へのコピペが CLI テンプレートに変わるだけ。E-01 (API投稿) とセットでないと実質的効率化にならない |
| 2026-03-30 | S-5 (字幕はみ出し) が最優先の痛点 | S-5 / S-6 / S-2 | ユーザーフィードバック。S-5/S-6 が最も時間がかかる工程 |
| 2026-03-30 | S-6 トピック分析は stdlib 制約内では精度不足 | パターンマッチ / 軽量NLP / やらない | パターンマッチ30-50%、NLP 40-60%+CLAUDE.md違反。LLM アダプター方式に転換予定 |
| 2026-03-30 | B-04 表示幅ベース分割を実装 | 表示幅 / 文字数維持 | 全角=2,半角=1 の display_width で YMM4 字幕はみ出しを事前防止。--display-width, --max-lines, --chars-per-line 追加 |
| 2026-03-30 | S-6 トピック分析を LLM アダプター方式に転換 | LLM / パターンマッチ / やらない | ユーザー指示。コーパス分析ライブラリはレガシー化しており LLM に統一。モデル切替可能なアダプター設計 |
| 2026-03-30 | サムネイルはYMM4テンプレートの文字・画像入れ替え | テンプレート手動 / Python自動生成 / 外部ツールのみ | Python 画像生成は不可。YMM4 テンプレートの手動カスタマイズを基本にし、後続 H-02 の `thumbnail_design` と `thumb.*` slot 限定 patch は successor-lane として許容する。サムネイルは非常に重要 |
| 2026-03-30 | A-04 / D-02 / F-01 / F-02 を quarantined に移す | proposed維持 / hold / quarantined | B-10 混入時の汚染バッチ由来で、個別再審査前に通常 backlog として扱うと再発するため |
| 2026-03-30 | A-04 を done に戻す | quarantined維持 / hold / done | RSS/Atom からタイトル抽出して NotebookLM 検索クエリへ渡す `fetch-topics` は Python のテキスト取得責務に収まり、実装と台帳が一致したため |
| 2026-03-30 | E-02 を hold に移す | proposed維持 / hold / rejected | 価値検証の結果、単体では bottleneck を減らさず、今は進めない方が正確だから |
| 2026-03-30 | C-01 を done ではなく info に整理する | done維持 / info | Python 機能ではなく、確認済みの手動工程だから |
| 2026-03-30 | canonical docs の雛形放置を handoff 不備として扱う | 雛形維持 / 内容補完 | `8a1c710` で docs は追加済みだったが、実内容が薄いままでは resume 時の再アンカー先として機能しない |
| 2026-03-30 | `docs/ai/*.md` を canonical rules として先に読む | helper docs優先 / canonical rules優先 | tool-specific helper docs や prompt より repo 内 canonical rules を先に読む方が再開の一貫性が高い |
| 2026-03-30 | docs-only handoff 用の単一 resume prompt を採用（2026-04-27 に廃止） | promptなし / prompts分散 / 単一resume prompt | 当時は次セッション開始手順を repo 内で完結させるため |
| 2026-03-31 | B-11 S-5 workflow proof を approved frontier にする | S-5 workflow proof / S-6 LLM adapter / hold継続 | ユーザーが S-5 を先に進めると承認。最大 pain に近く、Python の責務境界を壊さずに workflow proof を積めるため |
| 2026-03-31 | B-12 行バランス重視の字幕分割を実装する | proposal packet のみ / `--balance-lines` 実装 | S-5 proof で辞書や timing ではなく改行系 pain が支配的と確認できたため、2行字幕向けの自然改行 heuristics を opt-in で実装 |
| 2026-03-31 | B-13 を次候補として proposal 化する | B-12 継続 / clause-aware split + widow guard | B-12 は手動改行を減らしたが、長文再分割 15 件と 1 文字最終行が残り、次の主 pain が節分割と widow/orphan 回避に絞れたため |
| 2026-03-31 | B-13 節分割 + widow/orphan guard を実装する | proposal のみ / `--balance-lines` 内部改善 | 句読点の少ない長文と 1 文字最終行を減らす最短経路で、既存フラグのまま改善できるため |
| 2026-03-31 | B-14 を次候補として proposal 化する | B-13 継続 / aggressive clause chunking | B-13 で手動改行は 5 まで減ったが、再分割 10 と長い一文 1 字幕問題が残り、より積極的な chunking の要否を切り分ける必要があるため |
| 2026-03-31 | B-14 aggressive clause chunking を実装する | proposal のみ / `--balance-lines` 内部改善 | B-13 のままでは複数文発話の中にある単一長文が展開されず、operator pain の主因が残ったため。先に CLI 側でどこまで崩せるかを確かめる価値があった |
| 2026-03-31 | S-6 LLM 活用は API SDK ではなく GUI LLM (Custom GPT / Claude Project 等) を優先する | API adapter / GUI LLM / やらない | ユーザー希望。API SDK 導入は stdlib 制約緩和 ADR が必要で依存が増える。GUI LLM ならプロンプトテンプレートのみで Python 変更不要 |
| 2026-03-31 | B-15 改行コーパス収集を approved にする | B-14 継続 / corpus 収集 / hold | B-14 で bulk overflow 収束後、残 pain は個別ケース。heuristic 追加より corpus → 傾向化 → ルール化が強い |
| 2026-03-31 | C-07 S-6 演出メモ生成を proposed にする | proposed / hold / skip | GUI LLM でプロンプトテンプレートを作成し、実動画 1 本で workflow proof する方式。Python 変更なし |
| 2026-03-31 | B-15 をコーパス収集からトップダウン改行再設計に拡張する | パッチ (P1/P2) / トップダウン再設計 / hold | 初期コーパスの傾向分析で現行ボトムアップ方式の構造的限界 (2層の噛み合い不良、全体を見ない局所最適) を特定。ユーザー提案のトップダウン方式が実装可能かつ管理可能と判断。パッチ積み増しより根本解決を選択 |
| 2026-03-31 | 以前会話内でリジェクトされたトップダウン型分割アルゴリズム案を再評価・採用する | 再採用 / パッチ維持 / 別方式 | 当時のリジェクト理由は DECISION LOG に未記録。現在のコーパスで構造的問題が実証されたため、たたき台として再検討。仕様を精緻化し `reflow_utterance()` として実装する方針 |
| 2026-03-31 | 視覚系タスク (背景動画・アニメーション・サムネイル) への着手意向を記録 | 記録 / 即着手 / 無視 | ユーザー希望。字幕分割に目処がつけば次のペイン。D-02 quarantined / D-01 rejected のため権利・境界の再整理が前提。当面は字幕分割を優先 |
| 2026-04-01 | B-15 手動検証: 小区切り (漢字→ひらがな、カタカナ→ひらがな) を候補から除去 | 除去 / penalty引上 / 維持 | ユーザーフィードバック。「単/なる」「見間違/った」のような切断が発生する。大区切り (句読点) がない場所では分割しない方針を徹底。文字種境界より行長精度を優先 |
| 2026-04-01 | B-15 手動検証結果: 明らかなバランス偏りは解消、若干の違和感は残存 | 継続改善 / done化 / hold | ユーザー評価。4行またがり解消、漢字/カタカナ途中切断は改善中。次頁区切り(話者行分割)と同一ページ内改行の区別が今後の課題 |
| 2026-04-01 | B-15 を一旦区切り、残課題を B-16 として分離する | 区切り / 続行 | ユーザー判断。ページ間分割は改善されたが、行内折り返し制御には「1行/1ページ最大文字数から逆算する外殻」が必要で別タスク。画像関連が完全停止しているため、プラン再構成を優先 |
| 2026-04-01 | 開発プラン再構成: C-07→視覚系→B-16 の順で進行 | C-07優先 / B-16優先 / 視覚系優先 | C-07 (演出メモ) が最も軽く、視覚系の入口にもなる。C-07 結果を踏まえて D-02 再審査と視覚系の具体策を決定。B-16 は並行進行可能。E-02 は hold 継続 (E-01 とセットでないと価値が出ない判断は変わらず) |
| 2026-04-01 | 視覚系タスクの start gate を C-07 workflow proof 完了後に設定 | C-07後 / 即時 / hold | C-07 の背景キーワード有用性が視覚系の価値経路の入口。成功なら D-02 再審査へ、失敗ならプロンプト改善 or 手動継続 |
| 2026-04-01 | D-02 再審査チェックリストを作成 | 作成 / 後回し | 取得元、権利、取得/受取分離、YMM4受渡、価値経路、既存フローの6項目。C-07 proof 後に実施 |
| 2026-04-01 | C-07 v1 proof 結果: 2/3 OK だが背景候補の方向が違う | 方向転換 / v1維持 | ストック素材検索は価値が低い。実際に必要なのは「茶番劇風アニメーション + 図解アニメーション」の演出指示。4パターン (茶番劇/情報埋め込み/雰囲気演出/黒板型) を基軸にプロンプトを v2 に改善 |
| 2026-04-01 | 視覚系の最大ペインは「何を表示するか」の判断 + 情報不足時の取材 | 判断支援 / 配置自動化 / 素材API | ユーザーフィードバック。配置作業自体よりバランス判断と素材集めが重い。D-02 の方向性を「素材API」から「演出判断支援」に転換 |
| 2026-04-01 | C-07 v3: マクロ演出設計 + 素材調達ガイドを追加 | v2維持 / v3拡張 / 別プロンプト | C-07 v2 はミクロ (発話単位) のみ。ユーザーの最大ペイン (何を表示するか + 素材調達) はマクロ判断。Part 1 (全体設計) + Part 3 (調達ガイド) を追加し二層構造に拡張 |
| 2026-04-01 | D-02 再審査チェックリストを演出判断支援向けに改訂 | 旧チェックリスト維持 / 改訂 | 旧6項目は素材API方向のもの。方向転換により不適合。C-07 v3 統合/スコープ/価値経路/実装形態/ワークフロー位置/proof依存度の6項目に置換 |
| 2026-04-01 | D-02 の演出判断支援は C-07 v3 に暫定統合 | 独立機能 / C-07統合 / 両方 | ミクロ/マクロを流動的に組み替える方針。独立機能にするかは proof 結果で判断 |
| 2026-04-01 | 演出支援を5レイヤー (L-macro/L-micro/L-section/L-research/L-thumbnail) で整理 | レイヤー分離 / フラット | タスク ID に固執せず、機能をレイヤーとして捉え、後から統合・分割しやすい構造にする |
| 2026-04-01 | C-07 v3 proof 完了。D-02 を hold に変更 | hold / proposed / rejected | v3 出力レビューで L-macro + L-research が有用と確認。D-02 は C-07 v3 に吸収完了。独立機能不要 |
| 2026-04-01 | 作業時間実態: 10分動画で約1週間。長尺化で10分あたり約25%減衰 | 記録 | 素材再利用・パターン定着により摩擦が逓減する構造 |
| 2026-04-01 | proof は出力レビューで完了とし、実動画制作を要件としない | 軽量proof / 実動画proof | 実動画制作は重すぎてブロッカーになる。計測より実用を優先 |
| 2026-04-01 | YMM4 自動化の経路: プラグイン API 先行 → ymmp 直接編集を補完 | プラグインのみ / ymmp のみ / 二段階 | プラグイン API (IToolPlugin) が公式経路。タイムライン操作可否は未検証のため spike で確認。不可なら ymmp 編集を主経路に切替 |
| 2026-04-01 | YMM4 以外の動画制作パイプラインは検討対象外 | YMM4専念 / 代替検討 | ユーザー指示。ffmpeg/MoviePy 等での独自レンダリングは除外 |
| 2026-04-01 | アニメーション自動化 (G-01~G-04) を最優先フロンティアに設定 | アニメ自動化 / YT自動化 / 字幕改善 | S-6 が制作時間の70%以上を占める。ユーザーが「重い上にまだ何もできていない」と指摘 |
| 2026-04-01 | NotebookLM 自動化は NLMYTGen 外。台本入手後の工程に専念 | NLMYTGen内 / 別システム | 台本入手は折衷案 (前処理自動化 + NLM は読解/音声化のみ) で、動画制作が回り始めてから別途構築 |
| 2026-04-01 | G-01~G-04 を FEATURE_REGISTRY に proposed として登録 | 登録 / 保留 | 調査完了。実装承認は spike 結果を踏まえて判断 |
| 2026-04-01 | YMovieHelper を発見。CSV→ymmp 生成 (表情+動画切替対応) の既存ツール | 自前構築 / 既存ツール活用 | 自前でゼロから構築するより既存ツールと接続する方が現実的 |
| 2026-04-01 | G-01 (IToolPlugin spike) の優先度を最下位に変更 | 最優先維持 / 最下位 | タイムライン操作 API が非公開。.NET 環境構築の投資対効果が不明。YMovieHelper 連携で不十分な場合の代替経路 |
| 2026-04-01 | G-02 を YMovieHelper 詳細調査に再定義し最優先に | G-01先行 / G-02先行 | YMovieHelper が既に背景/表情/動画切替を実現しているため、入力仕様を把握して NLMYTGen と接続するのが最短経路 |
| 2026-04-01 | G-05 (build-ymh) を新規追加 | 追加 / 不要 | C-07 v3 の演出メモ → YMovieHelper 入力形式に変換する Python サブコマンド。G-02 の結果が前提 |
| 2026-04-01 | ymmp 直接編集は控える。完成品の解析研究のみ | 編集許可 / 研究のみ | 過去にデッドファイルが積み上がった経験。研究に没頭して開発から逸れるリスク |
| 2026-04-01 | テンプレート資産蓄積戦略を採用 | テンプレート / 毎回手動 | 制作者がテンプレートを用意→汎用素材化→リソース積み上げ。C-07 v3 がテンプレート選定を提案、build-ymh が仮組立。NLMYTGen は提案と仮組立まで、素材の完全自動生成には踏み込まない |
| 2026-04-01 | ドリフト防止ルールを INVARIANTS に固定 | 記録 | テスト目的化禁止、proof 軽量化、研究2ブロック制限。INTERACTION_NOTES にも開発ドリフト回避セクション追加 |
| 2026-04-01 | YMovieHelper を主軸から参照実装に格下げ (第三次改訂) | 主軸維持 / 参照実装 / 完全除外 | サービス終了済み Web アプリ (Docker+WSL+Go+TS)。CLI ではない。メンテナンス停止。設計思想の回収のみ。ツール依存は作らない |
| 2026-04-01 | 自動化の中核を「演出 IR + テンプレート資産」に転換 | ツール依存 / IR 中心 | 特定ツールに依存せず、NLMYTGen 独自の演出中間表現を定義。LLM は意味ラベルのみ出力し、座標変換はテンプレート定義側で解決 |
| 2026-04-01 | G カテゴリ再定義: G-02=IR語彙定義, G-05=IR出力プロンプト, G-06=接続方式決定 | 再定義 / 据置 | G-01/G-03 は hold。G-02 を YMovieHelper 調査 → IR 語彙定義に変更。build-ymh (旧G-05) は廃止し、IR 出力プロンプト (新G-05) に置換 |
| 2026-04-01 | YMovieHelper に言及する際のルール: 「使う」「接続する」ではなく「参考にする」「観察する」と書く | 記録 | 今後のドキュメントでの勘違い防止 |
| 2026-04-01 | G-02 演出 IR 語彙定義 v1.0 完了 | 完了 | `docs/PRODUCTION_IR_SPEC.md` 作成。9フィールド (template/face/bg/bg_anim/slot/motion/overlay/se/transition)、Macro+Micro 二層構造、JSON/CSV 二重表現、carry-forward ルール。S-6 の6手動工程を全カバー |
| 2026-04-02 | 正本ドキュメント5件を演出IR主軸に更新 | 修正 | README/CLAUDE.md/WORKFLOW/AUTOMATION_BOUNDARY/INVARIANTS から「CSV変換専用ツール」旧理解を除去。再開時の旧理解引き戻しを構造的に防止 |
| 2026-04-02 | G-05 C-07 v4 IR 出力プロンプト作成 | 完了 (proof待ち) | `docs/S6-production-memo-prompt.md` v4 セクション。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の Macro+Micro IR JSON を出力するプロンプト。v3 (自然文) との切替可能。proof はユーザーが Custom GPT で実施 |
| 2026-04-02 | ymmp 後処理の実機検証: 表情パーツ差し替えが動作することを確認 | 実証済み | Python で ymmp JSON のパーツパスを書き換え→YMM4で正常に開ける。音声・字幕は台本読込で確保済みのまま維持。二段階方式 (台本読込→ymmp後処理) が実現可能と確定 |
| 2026-04-03 | YMM4 テンプレートは独立ファイルではなく ItemSettings.json 内の Templates 配列に保存 | 実測確定 | テンプレートの Items 構造は ymmp Items と同一。Adapter ロジック再利用可能。エフェクト・VoiceCache もテンプレートに完全保持 |
| 2026-04-03 | Custom GPT v4 proof 完了 | 実証済み | 28 utterances / 5 sections / 全語彙チェック PASS / Macro-Micro 整合OK。carry-forward は全件フル指定 (省略なし) |
| 2026-04-03 | Custom GPT v4 の IR 出力は 2オブジェクト連結形式 (Macro + Micro) | 実測確定 | load_ir() で単一 JSON と連結形式の両方に対応。CLI patch-ymmp で動作確認済み |
| 2026-04-03 | production-slice patch-ymmp proof 完了、ただし full E2E は実制作 ymmp 不在で未閉塞 | 実証済み / 要再確認 | `samples/test - marisaFX.ymmp` に実IR先頭11発話を適用し face 13 / bg 2 変更を確認。`samples/v4_re.ymmp` は current workspace で未確認のため、28発話 full E2E は次ブロックへ持ち越し |
| 2026-04-03 | Template Registry は visual-review 前提。`extract-template` は棚卸し補助であって意味ラベル推定器ではない | 運用確定 | 表情ラベルは YMM4 上で見え方を確認して人間が命名する。現行 `patch-ymmp` のフラット `face_map` は単一キャラ proof 向けで、複数キャラ案件の最終形は character-scoped registry が必要 |
| 2026-04-05 | face_map を character-scoped に、bg_map は flat を維持 | 実装確定 | face は同じラベルでもキャラごとにパーツが異なる。bg は scene/preset 責務で話者固有ではない |
| 2026-04-05 | Remark フィールドを extract-template --labeled のラベル源に採用 | 実装確定 | Serif は発話テキスト用。Remark は VoiceItem / TachieItem / TachieFaceItem / ImageItem の全てに存在する空きメタデータ欄 |
| 2026-04-05 | row_start / row_end で IR 意味単位と VoiceItem 粒度差を吸収 | 実装確定 | IR を 60 発話に崩す案 (A) とテキストマッチング (C) を却下。IR の意味単位を保ったまま複数 VoiceItem に適用する方式 (B) を採用 |
| 2026-04-05 | idle_face: IR フィールド追加 + TachieFaceItem 挿入方式 | 実装確定 | TachieItem の表情制御ではなく、IR に idle_face を追加して adapter が non-speaker 側に TachieFaceItem を挿入。既存 face 適用経路を崩さず拡張 |
| 2026-04-05 | bg section 切替 proof 成功 (2 ラベル) | 実証済み | 5 セクションのうち 2 ラベルで背景切替を確認。残りはユーザーが bg_map を拡張するだけ |
| 2026-04-05 | `.claude` 側に常設ガードを追加 | 実装確定 | 毎回 prompt に重い禁止を書き足さず、repo-local 入口と hooks で repo 外逸脱 / broad question 停止 / repeated visual proof を抑止する |
| 2026-04-05 | face サブクエストの completion criteria を固定 | 継続調整 / failure class 固定 | face を未整理な改善ループではなく completed subsystem として扱うため。mechanical failure は class 名で止め、人間判断は creative quality に限定 |
| 2026-04-05 | apply-production は partial face output を書かない | patch 先行 / fail-fast | row-range 不整合、validation error、fatal face patch warning を書き出し前に止め、ymmp 化→手動確認ループを再発させないため |
| 2026-04-05 | Packaging / marketing レイヤーを独立 frontier として backlog 化 | C-08 個別改善 / E-02 再開 / packaging layer 新設 | 台本→タイトル侵食を止め、タイトル / サムネ / 台本の整合を 1 つの central brief で管理するため |
| 2026-04-05 | H-01 Packaging Orchestrator brief schema v0.1 を定義 | backlog のみ / schema 定義 | H-01 を abstract な気づきで終わらせず、C-07/C-08/E-02/H-04 が参照できる正本フィールドへ落とすため |
| 2026-04-06 | H-01 workflow proof packet を整備 | schema のみ / proof packet まで整備 | H-01 を `approved` のまま放置せず、user が 1 本の実台本で drift を観測できる実行単位まで前進させるため |
| 2026-04-06 | H-02 Thumbnail strategy v2 schema v0.1 を定義 | backlog のみ / schema 定義 | H-02 を感覚的な運用メモではなく、C-08 が参照できる specificity-first / banned pattern / rotation policy の正本へ落とすため |
| 2026-04-06 | H-04 Evidence richness score schema v0.1 を定義 | backlog のみ / schema 定義 | H-04 を曖昧な「内容が強いか」ではなく、promise_payoff と evidence category に分解された repair-oriented gate にするため |
| 2026-04-06 | H-04 manual scoring proof packet を整備 | schema のみ / proof packet まで整備 | H-04 を机上定義で終わらせず、warning を script/packaging repair に変換できる実行単位まで前進させるため |
| 2026-04-06 | H-02 は dry proof を先に通し、strict GUI rerun proof と分離して扱う | strict proof 待ち / dry proof 先行 | 既存 artifact だけでも specificity-first / banned pattern / rotation contract が機能するかを確認でき、GUI rerun 待ちで packaging lane 全体を止める必要がないため |
| 2026-04-06 | H-01 はまず repo-local dry proof を通し、strict な GUI rerun proof と分離して扱う | dry proof なし / strict proof 待ち / dry proof 先行 | 既存 artifact だけでも brief が共有契約として機能するかは確認でき、strict な before/after rerun 待ちで packaging lane 全体を止める必要がないため |
| 2026-04-06 | H-03 を packaging lane の最後の未定義ピースとして先に定義し、strict GUI rerun とは分離して進める | GUI rerun 完了待ち / H-03 先行定義 | visual stagnation risk は repo-local brief/cue/script だけでも warning 化できるため、外部 GUI 実行待ちで spec 定義全体を止める必要がないため |
| 2026-04-06 | H-04 AI監視 sample は `acceptable` と判定し、主要 warning を anecdote continuity と late payoff に集約 | 高評価でそのまま通す / vague score に留める / warning を repair に落とす | H-04 の価値は数値化より repair 指示にあるため、包装 promise と本文根拠のズレを具体修正へ還元できる形で残す必要があるため |
| 2026-04-06 | G-11 slot patch hardening を実装完了 | proposed 維持 / 実装完了 | timeline edit を broad manual retry loop にせず、slot を deterministic patch + fail-fast validation の packet として閉じるため |
| 2026-04-06 | G-12 は patch 前に readback harness と route contract 照合を先行実装 | 先に patch / 先に measurement harness | native route を未確定のまま `motion` / `transition` / `bg_anim` の adapter write に進むと、file-format risk と creative judgement が再混線するため |
| 2026-04-06 | G-12 の current contract は `test - marisaFX.ymmp` で通し、`production.ymmp` の `bg_anim` miss を failure class として扱う | gap を黙殺 / warning 扱い / failure class 化 | timeline quality 問題を visual impression に戻さず、route gap を mechanical failure として扱うため |
| 2026-04-06 | G-12 measurement packet を追加し、current corpus で route narrowing を先に完了 | harness のみ / packet 化して route narrowing | `motion` / `bg_anim` は current corpus で狭め、manual frontier を `transition` probe 1 本へ縮めると、operator の判断負荷を最小化できるため |
| 2026-04-06 | fade-family `transition` route を ymmp_measure で回収可能にし、G-12 contract を更新 | `transition` を route 不在扱い / fade-family route を corpus-derived contract 化 | repo-local corpus に既にある fade key を拾えば、手動 probe を増やさずに `transition` の主要 family を mechanical に確定できるため |
| 2026-04-06 | G-13 overlay / se insertion packet を completed として閉じる | overlay/se を broad manual frontier に残す / packet として閉じる | `overlay` は registry + timing anchor から deterministic な `ImageItem` 挿入まで閉じた。当時 `se` は timing までで write route 不在を旧 unsupported failure class で fail-fast（G-18 で挿入まで実装） |
| 2026-04-06 | Phase 1 として B-18 台本機械診断と C-09 refinement プロンプトを実装完了 | 保留 / 実装 | `diagnose-script`・`script_diagnostics.py`・`S1-script-refinement-prompt.md`・GUI 品質タブ・B18 dry proof まで一括 |
| 2026-04-06 | Next roadmap: P01 運用手順、P2A feat ブランチレビュー（一括マージ不採用）、P2B+G-14 production contract、P2C SE 境界、サムネ 1 枚チェックリスト | 未実施 / 実施 | Phase 2/3 の文書・contract 整備を master に反映 |
| 2026-04-05 | サムネイル戦略は抽象煽りより具体数値・固有名詞優先 + rotation 管理 | 定型煽り / 具体性優先 / 各動画場当たり | 本文根拠とクリック訴求を両立し、固定パターン反復による疲労と硬直を避けるため |
| 2026-04-05 | スコアリングは visual density / evidence richness の2軸から着手 | スコアなし / 単一総合点 / 2軸 | 演出不足と内容不足を別々に診断し、制作改善とマーケ改善の接続点を明確化するため |
| 2026-04-06 | assistant 側の subquest を timeline edit まで拡張するが、packet 単位で進める | timeline を一括実装 / packet 分割 / 維持 | face と同様に mechanical scope を failure class / readback / boundary で切り分けないと、YMM4 手動確認ループへ戻るため。G-11 slot patch → G-12 native-template measurement → G-13 overlay/se insertion の順に進める |

---

## Python のスコープ（確定事項 — 2026-03-30）

**許可:**
- テキストファイルの変換（transcript → CSV）
- テキストメタデータの生成（タイトル・説明・タグ等の文字列）
- 入力テキストの検証・分析
- 外部ソースからのテキスト/メディア取得（L1、取得と受け取りを分離する設計で）

**禁止:**
- 画像生成・画像合成（PIL/Pillow 含む）
- .ymmp ゼロ生成・YMM4 台本読込代替（音声ファイル参照・発音情報を外部生成できないため）
- YMM4 native template 資産の Python 生成・YMM4 GUI 万能制御
- YMM4 出力の模倣・Python preview
- 動画レンダリング・音声合成
- 外部 TTS（Voicevox 等）

**根拠:**
YMM4 の .ymmp プロジェクトファイルは音声ファイル（WAV 等）への参照を含む。その音声は YMM4 が台本 CSV を読み込む際に内蔵 TTS で自動合成するもの。NLMYTGen から音声ファイルを生成できないため、完全な .ymmp を外部から作ることは原理的に不可能。ただしこの制約は、台本読込後 `.ymmp` に対する限定 patch、repo-tracked YMM4 template source の placement、thumbnail `thumb.*` slot patch、audit/readback/compact review artifact を禁止しない。

---

## IDEA POOL

FEATURE_REGISTRY.md に統合済み。機能候補は FEATURE_REGISTRY で管理する。

| ID | 旧アイデア | 移行先 |
|----|----------|--------|
| IP-02 | Web UI 化 | CLAUDE.md スコープ外 |
| IP-03 | YouTube 自動アップロード | FEATURE_REGISTRY E-01 (hold) |

---

## HANDOFF SNAPSHOT (2026-05-29 RSS cleanup decision)

- Branch/remote: continue on `master` and pull latest `origin/master` before work. This decision builds on cleanup handoff commit `f6db81e`.
- RSS cleanup decision: user accepted deletion for all failed-feed categories from the audit (`http_404`, `parse_or_non_feed`, `ssl_error`, `timeout`, and `http_403`) because RSS feed resources do not need strict completeness and the sample count is sufficient.
- Committed decision record: `docs/verification/RSS-FAILED-FEED-CLEANUP-DECISION-2026-05-29.md`. It contains only counts, categories, and policy; it does not include feed URLs, raw OPML, tokens, article titles, or article bodies.
- Duplicate handling: duplicate feed URL remains `0`; duplicate title remains `1` and stays `manual_review` because no specific duplicate-title action was supplied.
- Post-cleanup validation state: Inoreader-side changed count is unknown, and the local OPML export has not been refreshed after the deletion decision. Do not rerun post-cleanup smoke as proof until a fresh OPML export replaces `_local/rss/feeds.opml.xml`.
- Next safe restart move: ask for or wait for a fresh OPML export at `_local/rss/feeds.opml.xml`, then rerun `list-feed-sources` and `rss-smoke` with sanitized evidence only. Do not use Inoreader API or tokens unless explicitly re-scoped.

## HANDOFF SNAPSHOT (2026-05-28 RSS cleanup handoff)

- Branch/remote: `master` is pushed to `origin/master`; restart with `cd C:\Users\PLANNER007\NLMYTGen && git fetch --all --prune && git checkout master && git pull --ff-only origin master`. The cleanup audit commit immediately before this handoff is `b98afac`; after pulling, use the latest `origin/master` commit and read this snapshot.
- RSS OPML status: RSS UI comparison matched NLMYTGen's OPML view at `147` sources and `7` categories, so the ignored OPML export can be treated as the current operational source of truth until the reader list changes.
- Committed RSS evidence to read first: `docs/verification/RSS-LIVE-SMOKE-EVIDENCE-2026-05-28.md` for the smoke/diagnostic baseline, then `docs/verification/RSS-FAILED-FEED-CLEANUP-SUMMARY-2026-05-28.md` for the cleanup audit summary. `docs/runtime-state.md` has the active top-line state.
- Local-only artifacts: `_local/rss/feeds.opml.xml` is the raw OPML input and must stay uncommitted. `_tmp/rss_failed_feed_cleanup_candidates.md` and `_tmp/rss_failed_feed_cleanup_candidates.json` contain the detailed failed-feed titles/URLs for human Inoreader UI cleanup and must also stay uncommitted.
- Latest local cleanup audit: status counts were `fetched=121`, `empty=0`, `error=26`, `listed=0`; error breakdown was `http_404=2`, `parse_or_non_feed=15`, `ssl_error=2`, `timeout=3`, `http_403=4`. Prior live diagnostics varied around `31/32` errors, so treat exact failure count as live-network variable and use categories for cleanup planning.
- Cleanup order for the human UI pass: review `http_404` first, then `parse_or_non_feed`, `ssl_error`, `timeout`, and `http_403`. Delete/replace/keep decisions happen in Inoreader manually; repo code and OPML files are not mutated by this audit.
- Duplicate handling: duplicate feed URL count is `0`; duplicate title count is `1` and remains `manual_review`. Do not auto-merge or auto-delete the duplicate title.
- Boundaries not crossed: Inoreader API, token use, subscription mutation, DB/background sync, G-27 carrier work, Baseball, Thumbnail, GUI work, NotebookLM API, video generation, and YouTube posting were not run.
- Validation before handoff: CLI help smoke for `rss-smoke`, `list-feed-sources`, and `fetch-topics` passed; `git diff --check` passed; added committed lines had no URL/token/raw OPML marker hits. The ignored local files remain outside git.
- Next safe restart choices: `Verify` the local-only failed-feed list in Inoreader UI and rerun `rss-smoke` after manual cleanup; `Audit` the one duplicate title manually; or `Advance` source category representative selection so categorized entries can appear in the shown sample. Do not start Inoreader live API smoke without an explicit new instruction.

## HANDOFF SNAPSHOT (2026-05-27 update)

- Branch / remote state: `master`. Pull latest `origin/master`; expected sync check is `git rev-list --left-right --count "HEAD...@{u}" = 0 0`. Working tree may still show pre-existing untracked local files `.claude/worktrees/` and `samples/2026-05-16.ymmp`; they are not part of this handoff.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. `runtime-state.md` is the live frontier authority.
- Closed diagnostic slice: `samples/_probe/g24/layout_instruction_proof.ymmp` now has machine readback pass and user-side YMM4 v4.52.0.8 GUI proof pass. The visible issues found in the first GUI pass (bottom-looking title alignment, no title/grid gap, unstable labels) were corrected by `4631f89 fix(g27): stabilize layout instruction proof spacing`.
- Current proof facts: `layout_instruction_proof_readback.json` reports `status=passed`, 17 items, hard_fail=0, violations=[], `title_grid_gap_visible=pass`, and `region_labels_clear_major_items=pass`. Narrow checks run: `node scripts\build_g27_layout_instruction_proof.js --write`, `node scripts\build_g27_layout_instruction_proof.js`, `node scripts\render_g27_layout_instruction_proof_html.js`, and `git diff --check`.
- Boundary: this is a diagnostic layout/slot proof only. It is not a render, creative acceptance, production carrier replacement, slot-fill readiness, or production readiness claim.
- Next frontier: return to the `G27_PublicVsBrokerDB` carrier / slot-fill path. Do not design an anchored slot contract or implement slot-fill before a human-authored carrier exists. After carrier receipt, assistant should read back required `G27PBD_*` item names, short Remarks, fixed card counts, `G27PBD_Arrow` existence, and geometry-free patch feasibility.

---

## HANDOFF SNAPSHOT (2026-05-14 update)

- Branch / remote state: `codex/g24-nod-sync-adoption`; pull the latest branch and expect the active project changes to be committed. Confirm with `git status --short --branch` and `git rev-list --left-right --count HEAD...'@{u}'`.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. The live `next_action` is waiting for a human-authored `G27_PublicVsBrokerDB` YMM4 carrier, not a scene-generation or render slice.
- Current decision: G-27 direct dense `ShapeItem` / `TextItem` scene generation is stopped as a production route. Existing visual proxy v2/v2.1, minimal probe, micro scene, and micro scene visibility outputs are diagnostic-only and must not be promoted into stable carriers.
- New handoff artifact: `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`. It tells the human exactly what to create in YMM4: 16:9 / 1920x1080 carrier, 5% outer safe margin, bottom 10-15% caption safe area, left public panel, right broker/private DB panel, center lock/threshold, fixed 2 public cards, fixed 3 broker cards, optional `G27PBD_Arrow`, short `G27PBD_*` item names, short Remarks, and no provenance in item names/Remarks.
- User should return: carrier `.ymmp` path, preview screenshot, timeline screenshot, representative item property screenshots for `G27PBD_PublicPanel`, `G27PBD_PublicCard1`, `G27PBD_BrokerPanel`, and `G27PBD_Lock`, light/dark stage choice, and a short note that the caption safe area is clear.
- Assistant next after receiving carrier: read back required item names, duplicate/missing items, short Remarks, fixed card counts, `G27PBD_Arrow` existence, and whether text / visibility / timing / sidecar provenance can be patched without touching geometry, anchors, colors, font hierarchy, or layout grid. Only then prepare an anchored slot contract.
- Not done: no `.ymmp` carrier was created, no slot-fill contract was written, no patch script was implemented, no raw geometry was generated, no render, no production timing, no creative acceptance, no G-26, no `sports_news`, no INT-02e, no publishing, no master integration, no new gate, and no broad roadmap.
- Local note: `docs/WritingPage.code-workspace` is an unrelated untracked editor workspace file with sibling-project references; do not commit it as NLMYTGen handoff context.

---

## HANDOFF SNAPSHOT (2026-05-13 update)

- Branch / remote state: `codex/g24-nod-sync-adoption`; pull the latest branch and expect a clean working tree. Confirm with `git status --short --branch` and `git rev-list --left-right --count HEAD...'@{u}'`.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. The live `next_action` is the G-27 primitive visibility calibration GUI readback wait; this snapshot only preserves the executable handoff context.
- Current G-27 artifact: `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp`, generated by `scripts/build_g27_primitive_visibility_calibration_probe.js`.
- Companion artifacts: `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_readback.json` and `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe_report.md`.
- Calibration scope: this is a drawing-semantics calibration probe, not a video scene. It uses one light-stage tonal system, `ShapeItem` / `TextItem` only, 11 items, a full-screen BG, a 920x560 `Main Panel`, panel-contained title/body text, center/TL/BR anchor markers, and one thick connector.
- Machine readback: `status=passed`, `ShapeItem=6`, `TextItem=5`, `missing_item_count=0`, `malformed_item_count=0`, `item_name_length_failures=0`, `remark_length_failures=0`, `suspicious_default_item_count=0`, `carrier_modified_in_place=false`, `render_performed=false`, and `creative_acceptance_performed=false`.
- Previous micro scene status: `real_estate_dx_micro_scene_visibility_probe.ymmp` opens and has machine/timeline pass, but user GUI review found preview visibility, visual composition, and scene adequacy insufficient. Do not add more labels/cards/beats or create another micro scene variant before the calibration GUI review passes.
- Verification chain: `node --check scripts/build_g27_primitive_visibility_calibration_probe.js`; `node scripts/build_g27_primitive_visibility_calibration_probe.js --write`; `node scripts/build_g27_primitive_visibility_calibration_probe.js`; `git diff --check`.
- Not done: no minimal render smoke, no production timing, no creative acceptance, no external assets, no TTS, no URL fetch, no publishing, no `sports_news`, no G-26, no INT-02e, no master integration, no new gate/policy/roadmap/dry-run/visual atlas.
- Next concrete move: open `samples/_probe/g24/real_estate_dx_primitive_visibility_calibration_probe.ymmp` in YMM4 and return whether the large panel is visible, title/body text are inside the panel, anchor markers are where expected, connector is visible, item names/Remarks are manageable, plus preview screenshot, one selected panel item property screenshot, and one selected text item property screenshot. Only after this GUI review passes should calibrated geometry/visibility grammar be applied back to the 4-beat micro scene.

---

## HANDOFF SNAPSHOT (2026-05-12 update)

- Branch / remote state: `codex/g24-nod-sync-adoption` at `21ef759 docs: refresh g27 handoff snapshot`; probe generation commit is `3411413 feat(g27): generate minimal ymmp probe`; `HEAD...origin/codex/g24-nod-sync-adoption = 0 0` at handoff. Working tree should be clean after pulling this branch.
- Restart path: read `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. Current frontier is `runtime-state.md` `next_action`; this snapshot only preserves the executable handoff context.
- Current G-27 artifact: `samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp` generated from `samples/_probe/g24/real_estate_dx_ymmp_compact_patch_review.json` by `scripts/build_g27_minimal_ymmp_probe.js`.
- Machine readback: `samples/_probe/g24/real_estate_dx_minimal_patched_probe_readback.json` / `.md` reports `status=passed`, `ShapeItem=14`, `TextItem=7`, `candidate_ids_found=7/7`, `layer_values_found=[7,8,9]`, `missing_item_count=0`, `malformed_item_count=0`, `carrier_modified_in_place=false`, and `next_slice_can_safely_proceed_to_YMM4_GUI_readback_preview=true`.
- Candidate scope: only `RE-02-beginning`, `RE-02-development`, `RE-06-beginning`, `RE-06-development`, `RE-06-turn`, `RE-07D-beginning`, and `RE-07D-development` are in the probe. `RE-02-turn` remains blocked outside the output; `RE-07D-turn` remains deferred outside the output.
- Verification chain: `node --check scripts/build_g27_minimal_ymmp_probe.js`; `node scripts/build_g27_minimal_ymmp_probe.js --write`; `node scripts/build_g27_minimal_ymmp_probe.js`; Python openability guard with `success=True`, `is_project_canvas=True`, `item_count=21`; `node scripts/build_g27_ymmp_compact_patch_review.js`; `node scripts/build_g27_adapter_ir_dry_run.js`; `node scripts/check_g27_adapter_route_preflight.js`; `node scripts/check_g27_adapter_authorization_gate.js`; `git diff --check`.
- Not done: no render, no YMM4 GUI preview capture, no production timing, no creative acceptance, no TTS, no URL fetch, no publishing, no `sports_news`, and no pipeline hardening.
- Next concrete move: open or capture `samples/_probe/g24/real_estate_dx_minimal_patched_probe.ymmp` in YMM4 for GUI readback / preview. Treat PASS as file-openability / visible-placement evidence only; short render is a later slice after GUI readback succeeds.

## HANDOFF SNAPSHOT (2026-04-26 update)

- Shared Focus: **G-24 template-analyzed placement after raw clone readback**. The v1 source contains all five templates and `--skit-group-only` can insert exact/fallback cues, but raw clone output is not production acceptance because user visual feedback found spacing/composition too rough. The current shared cycle is no longer motion authoring, alias planning, or user hand placement; it is adding template analyzer + placement planner so reusable YMM4 templates become generated production placement. Canonical current state: [runtime-state.md](runtime-state.md) slice / next_action.
- Restart Governance Delta: **2026-04-27** normal restart read budget is now capped at `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`. Protected/canonical docs remain sources of truth, but they are not all full-read requirements. Read `project-context` HANDOFF / DECISION LOG, FEATURE ID, invariant, ledger, workflow, interaction failure class, or AI gate only when the current decision needs that section. Full re-anchoring is an exception, not the default.
- Interaction Governance Delta: **2026-04-27** template formalism is now a structural failure class. Obsolete prompts, archived packets, and superseded roadmap/setup docs remain deleted; `INTERACTION_NOTES.md` treats interaction failures as project risks, and now explicitly blocks prompt/checklist/OK-NG templates from replacing task connectivity. Manual/shared actions must state open target, created artifact, source object, actor, owner artifact, acceptance meaning, and replan condition before using short result codes.
- Roadmap Prep Delta: **2026-04-27** G-24 planned author/export is closed at the v1 set (`enter_from_left` / `surprise_oneshot` / `nod` / `deny_oneshot` / `exit_left`). [PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md](verification/PRE-PLAN-LANES-AND-CORE-DEV-2026-04-09.md) and [P02-production-adoption-proof.md](verification/P02-production-adoption-proof.md) now point to production-use validation rather than another cautious authoring gate.
- Implementation Delta: **2026-04-27** user completed `delivery_deny_oneshot_v1` and `delivery_exit_left_v1`. Repo inspection found the two target samples use plain body/face `ImageItem` children and no `TachieItem`; `deny_oneshot` is a short X-axis one-shot sway, and `exit_left` uses a leftward OUT `InOutMoveEffect`. `skit_group.intent.deny_oneshot` / `skit_group.intent.exit_left` are now `direct_proven`.
- Validation Delta: **2026-04-27** repo-probe production-use validation PASS. `audit-skit-group` on `samples/canonical.ymmp` + `samples/_probe/skit_01/skit_01_ir.json` returned `exact=5 / fallback=0 / manual_note=0`. No confirmation `.ymmp` was generated.
- Gap Classification Delta: **2026-04-27** production-like gap classification PASS. IR A returned `exact=3 / manual_note=1`; IR B returned `exact=1 / manual_note=3`; this was followed by alias registration for `surprise_jump` and `deny_shake`.
- Safe Next Frontier Packet: **The next concrete move is template analyzer + placement planner for real-estate DX skit_group placement**. Entry route stays `patch-ymmp --skit-group-only`, but raw template clone must be treated as transport proof only. The next proof should show an analyzed placement plan, patched `.ymmp` readback, and no hand-placed cue correction.
- Active Artifact: NLM transcript → YMM4 CSV → Writer IR → Template Registry → YMM4 Adapter → 動画制作ワークフロー効率化
- Artifact Surface: CLI → CSV → YMM4 台本読込 → IR (Custom GPT) → Registry (JSON) → Adapter (patch-ymmp) → 演出設定 → レンダリング
- Last Change Relation: **2026-04-28** G-24 raw clone placement and image-path readback PASS, followed by user correction that placement spacing/composition must be generated from template analysis rather than fixed by user hand placement.
- Handoff Focus (next): Resume from template analyzer + placement planner. Keep `panic_shake` out of normal Part 2 JSON vocabulary; do not request template reauthoring unless diagnostics prove source data is missing.
- Evidence: Production E2E remains proven, v1 G-24 planned templates are PASS / `direct_proven`, repo-tracked template source is 5/5, and raw clone placement readback inserted the expected Layer 9 cues. That readback is transport proof, not production acceptance.
- 案件モード: CLI artifact
- 現在の主レーン: 方向転換中 (実制作bottleneck直接軽減へ移行)
- 成熟段階: Level 1 (限定変換器) 到達済み、Level 2 (演出IR適用エンジン) 形成中 → Level 3 接近
- Current Trust Assessment:
  - trusted: B-01~B-17 全字幕スタック（実装+検証済み）
  - trusted: G-02 IR 語彙 v1.0、G-02b ymmp 構造解析、G-06 patch-ymmp 実機検証
  - trusted: extract-template (face_map/bg_map 自動抽出)
  - trusted: G-05 v4 proof 完了。Custom GPT が PRODUCTION_IR_SPEC v1.0 準拠の IR を正常出力
  - trusted: load_ir Multi-Object 対応 (2オブジェクト連結形式の読み込み)
  - trusted: face completion hardening (`PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_PROMPT_PALETTE_*` / `FACE_LATENT_GAP`)
  - trusted: G-11 slot patch hardening (`SLOT_UNKNOWN_LABEL` / `SLOT_REGISTRY_GAP` / `SLOT_CHARACTER_DRIFT` / `SLOT_DEFAULT_DRIFT` + TachieItem X/Y/Zoom patch + `off` hide)
  - trusted: G-12 readback harness (`measure-timeline-routes` で `motion` / `transition` / `bg_anim` candidate route を抽出し、`--expect` / `--profile` で route contract miss を検出)
  - trusted: G-12 packet narrowing (`motion=TachieItem.VideoEffects`、`bg_anim=ImageItem.X/Y/Zoom`、effect-bearing bg=`ImageItem.VideoEffects` まで current corpus で狭め済み)
  - trusted: repo-local `.ymmp` 16 本の corpus audit により fade-family `transition` route は観測済み、`template` route は 0 件と確認済み
  - trusted: G-13 overlay insertion (`OVERLAY_*` validation + deterministic `ImageItem` patch)
  - trusted: G-13/G-18 `se` (`SE_*` validation + G-18 `AudioItem` 挿入、`PatchResult.se_plans` = 挿入数)
  - trusted: H-02 done (dry proof + strict GUI rerun proof pass 2026-04-06)
  - trusted: H-03/H-04 done — `score-visual-density` / `score-evidence` CLI + tests (`test_visual_density_score.py`, `test_evidence_score.py`)
  - trusted: H-05 done — `score-thumbnail-s8`（手動採点 JSON の機械集約、`thumbnail_s8_score.py`、`test_thumbnail_s8_score.py`）
  - trusted: B-18 `diagnose-script` + C-09 `docs/S1-script-refinement-prompt.md`（`test_script_diagnostics.py`）
  - resolved (G-14): `production.ymmp` はタイムラインに ImageItem 無しのため bg_anim 未観測。`production_ai_monitoring_lane` で motion/transition のみ required とし contract pass。背景アニメ patch は ImageItem 含有 ymmp で別パケット
  - needs re-check: non-fade / template-backed `transition` の ymmp route は repo 内 sample 不在のため未固定。新しい sample が入ったときだけ再測定する
  - resolved (G-18): `se` の `AudioItem` 挿入は `samples/AudioItem.ymmp` + コード内骨格で固定。運用で YMM4 バージョン差が出たら readback のみ再確認
  - needs re-check: face label inventory そのものが creative quality として十分かは最終制作物で見る
- Recovered Canonical Context:
  - Python はテキスト変換 + 演出 IR 定義 + ymmp 限定後段適用
  - 視覚配置 IR が中心課題。C-07 系が主系統、D-02 は従属的補助論点
  - patch-ymmp は Level 1 限定変換器。ゼロからの ymmp 生成とは区別する
  - 「未実装」は「境界外」ではない。motion/transition/overlay は正式スコープ内の frontier
  - YMM4 テンプレートは独立ファイルではなく ItemSettings.json の Templates 配列に JSON 保存
  - Custom GPT v4 は 2オブジェクト連結形式 (Macro + Micro) で IR を出力する。load_ir() で対応済み
- Authority Return Items:
  - YMM4 大版本更新時: `AudioItem` 構造差分が出たら readback のみ再確認（G-18）
  - E-02: 旧 standalone template は hold 継続。H-01/H-02/H-04 を入力にした metadata draft は successor-lane として別起票可
  - F-01/F-02: quarantined 継続
- What Not To Do Next:
  - spec/proof 整備をさらに積み増さない (一巡済み。実制作の手間軽減が先)
  - 再スタート時に保護 docs / canonical docs を全部読む運用へ戻さない。通常再開は 3 点 + 必要節だけ
  - interaction failure を個人的な反応ラベルへ戻さない。対話メモは、再質問・停止・手動検証押し戻し・価値経路 drift を防ぐための failure class として保守する
  - Prompt / checklist / `OK/NG` 返却テンプレを、開く対象・作る対象・元 object・判定主体の説明の代替にしない
  - done 件数で進捗を測らない (35件だが実制作カバレッジは限定的)
  - D-02 を主軸として扱わない (従属的補助論点)
  - quarantined 項目を通常候補としてそのまま spec 化しない
  - face 問題を broad な visual retry loop として再開しない
  - E-01/旧 E-02 standalone を制作パイプラインへ自動注入しない（metadata draft は integration point 明示の successor-lane で扱う）
- Expansion Risk: なし

## B-11 workflow proof chronicle (archive)

OPERATOR の workflow proof 節から移した観測メモ。現行条件は [OPERATOR_WORKFLOW.md](OPERATOR_WORKFLOW.md)。

- 2026-04-06: 既存サンプル `samples/AI監視が追い詰める生身の労働.txt` について取込前記録（stats・overflow 警告・111 行 CSV 出力）を [verification/B11-workflow-proof-ai-monitoring-labor.md](verification/B11-workflow-proof-ai-monitoring-labor.md) に固定。取込後表は YMM4 通し確認待ち。
- 2026-03-31 の初回観測では、辞書登録 0 / タイミングのみ 0 に対して、手動改行・再分割したい長文が約 30 箇所と支配的だった。次の L2（Python変換工程）改善は読みではなく字幕改行のバランス改善を優先する。
- 2026-03-31 の B-12 再観測では、手動改行 10 / 再分割したい長文 15 / 不自然な単語分割 5。`。` での改行は効いたが、句読点の少ない長文と 1 文字最終行が残り、次の主 pain は clause-aware split と widow/orphan guard だと判明した。
- 2026-03-31 の B-13 実装では、`--balance-lines` の内部改善として clause-aware split fallback と widow/orphan guard を追加した。sample dry-run では 57 発話 → 62 行に再編され、次に必要なのは YMM4 取込後の fresh visual evidence である。
- 2026-03-31 の B-13 再観測では、手動改行 5 / 再分割したい長文 10 / 不自然な単語分割 5。減りはしたが「まだ多い」という operator judgement で、特に長い一文が 1 字幕に残るケースは未解決だった。次の主 pain は aggressive clause chunking に移った。
- 2026-03-31 の B-14 実装では、複数文発話の中にある単一長文も sentence ごとに再展開し、通常候補が尽きた残り長文には aggressive clause chunking fallback を追加した。sample dry-run では 57 発話 → 95 行、overflow candidates は 3 件まで減少したため、次に必要なのは YMM4 上で「再分割負荷が減ったか」と「細かく切れすぎていないか」を同時に見る post-import visual evidence である。
- 2026-03-31 の追加観測では、`、` 起点の分割強化により長すぎる行はかなり減り、全字幕が 3 行以内には収まる水準まで改善した。残課題は bulk overflow ではなく、`ー`、カギ括弧 `「」`、数値や記号を含む `202/4` のような折り返しなど、個別ケースの良し悪しを集めて傾向化する段階に移った。ここから先は rule の複雑化が急速に進むため、heuristic を足し続ける前に「改行すべき/すべきでない例」の corpus を集める value path が強い。
- 2026-03-31 の B-15 初期コーパス収集では、`AI監視が追い詰める生身の労働_balance_lines_ymm4.csv` から 14 件 (bad-split 10, good 4) を抽出した。傾向パターン: P1=閉じ括弧直後+助詞で不自然分割 (5件)、P2=左側が極端に短い (3件)。P1/P2 はいずれもルール候補 (3件以上)。対策案と初期コーパスの妥当性について手動検証待ち。
- 2026-04-01 の B-15 第1回手動検証: ユーザーが YMM4 取込後に確認。報告: 漢字途中切断 (`事情は完/全に`, `身体的限/界`)、カタカナ途中 (`評価スコ/アが`)、単語途中 (`働/き続ける`, `路上/へと`)、次頁区切りの違和感 (`ロックオン/して`)。原因は小区切り(文字種境界)の誤発動と候補不足時の強制切断。修正: 大区切り限定方式に変更、漢字連続を禁止位置に追加。
- 2026-04-01 の B-15 第2回手動検証: 第1回報告の7パターン全て解消。4行またがりなし。若干の違和感は残るが「明らかなバランス偏りはなくなっている」。追加フィードバック: 漢字→ひらがな境界の小区切りは外すべき (`単/なる`, `見間違/った` 類)。文字種境界より行長精度を優先する方針を確認。小区切り候補から文字種境界を除去。
- 2026-04-01 の B-15 第3回手動検証: ページ間分割はだいぶ改善。行内折り返し (YMM4自動折り返し) の違和感は残存。「1行/1ページの最大文字数から逆算する外殻」が必要で、B-16 として分離。B-15 done。
- 2026-04-01 の C-07 v1 proof: セクション分割 OK、作業時間削減 OK、背景候補 NG。ストック素材検索は方向が違う。必要なのは茶番劇アニメ+図解の演出指示。
- 2026-04-01 の C-07 v2 proof: 4演出パターン (茶番劇/情報埋め込み/雰囲気演出/黒板型) + 発話単位指示 + 表示情報抽出 + 要調査明示。3基準全て OK。C-07 done。
- 画像例から言語化したオペレータ意図（立ち絵＋フキダシ・ゆっくり顔差し替え、リソース列挙、地図/黒板整理、雰囲気ストック）の正本: [C07-visual-pattern-operator-intent.md](C07-visual-pattern-operator-intent.md)。
- 2026-04-03 の production-slice patch-ymmp proof では、実IR先頭11発話を既存 ymmp に適用して face 13 / bg 2 変更を確認した。一方で 11 VoiceItem 中 4 件は `TachieFaceParameter` を持たず、face 差し替え対象外だった。full E2E 前に、台本読込後 ymmp の対象キャラ発話が表情パラメータを保持していることを operator 側で確認する必要がある。
- 2026-04-05 の face completion hardening で、この種の partial apply は `VOICE_NO_TACHIE_FACE` として mechanical failure に昇格した。以後は broad な visual retry loop ではなく、failure class に応じて対処する。
- 2026-04-06 の H-02 dry proof で、C-08 は `Specificity Ledger` と `Brief Compliance Check` を返す契約になった。strict GUI rerun proof は同日 pass で閉じた (4/5案が preferred_specifics 使用、banned pattern なし)。コピー品質の実用改善は別課題として残る。

## 2026-04-05 Structural Linebreak Redesign Note

- B-17 reflow v2 was reworked around structural major/minor boundaries instead of phrase-specific word lists.
- Page carry-over and in-page line breaks are now evaluated separately: page planning prefers major boundaries first, then falls back to minor boundaries only when necessary.
- Inline break scoring now strongly penalizes breaks inside short hiragana connector tails and around quoted/bracketed labels followed by explanatory nouns.
- Short comma-led intro lines are now penalized by width so that later particle/phrase breaks win when they keep the page visually denser.
- Close-bracket/content fallback candidates and major-vs-all page-plan comparison were added, reducing earlier failures around quoted labels and explanatory nouns.
- Emergency inner-break candidates inside long quoted labels were added as a last resort; remaining residuals are now mostly small 41-48 width overruns rather than gross structural breaks.
- Single-hiragana tails after quoted terms are now scored separately, improving `...最適化」 / と聞くと` type boundaries while keeping `」` at the next-line head suppressed.
- Sample proof on `samples/AI監視が追い詰める生身の労働.txt` improved several screen-facing failures (`では / なく`, `）」 / という`, `） / 」`, `19 / 億`) while leaving a smaller residual cluster around `XというY` and quoted explanatory phrases that still need another structural pass.
- Carry-over scoring is now explicitly separated from in-page line breaks: `close+tail` boundaries and extra-page exact plans are allowed to win when they eliminate overflow without creating sparse fragment pages.
- Exact page-count comparisons now use a target-specific ideal page width instead of reusing the base target, which fixed the `完璧に計算されたアルゴリズムが生身の / 人間という...` class by allowing one more page in the surrounding multi-sentence utterance.
- Current sample residuals are down to 2 mechanical frontier cases in `_tmp_structural_balance.csv`: `誰の汗とリスクを動力にして回り始めるのかを / 解剖していくということですね。` and `自発的にリスクを取らせる罠のようなものです。 / データによると、`. Further automatic tightening risks over-fragmenting page flow more than it helps.
