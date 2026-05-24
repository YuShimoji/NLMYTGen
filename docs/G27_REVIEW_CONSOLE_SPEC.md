# G-27 Review Console Spec

G-27 Real Estate DX の制作判断を Electron GUI の `デザインレビュー`
タブに集約するための v1.2 仕様。Markdown / HTML / chat は補助に降格し、
判断結果は JSON として repo に戻す。

v1.2 の主な修正点は、`デザインレビュー`を既存制作ウィザードへ載せた
カード一覧ではなく、全幅のタイムライン型 Review Workbench として扱うこと。
動画全体の流れから segment を選び、台本文脈・演出意図・次工程への影響を
同じ画面で確認してから判断を保存する。

User-facing review must happen in the GUI timeline; HTML/PNG/JSON are
evidence artifacts, not independent review surfaces.

ユーザー向けレビューはGUIタイムラインに集約する。HTML/PNG/JSONは証跡であり、
独立した判断面にしない。

## Responsibility Split

| surface | role |
| --- | --- |
| GUI `デザインレビュー` | primary review surface。全幅 Review Workbench として、動画全体の概略、横タイムライン、選択 segment の台本抜粋、判断ペインを見せて判断を受け、保存する |
| `review_packet.json` | GUI が読む判断単位。episode context、story outline、segment、選択肢、source refs、gate を持つ |
| `review_decisions.json` | GUI が保存する差し戻し伝票。次の scene decision packet / gap report の入力 |
| `*_review_map.md` | 根拠ログ。通常レビューでは読ませない |
| compact HTML / proof PNG / readback JSON | GUI に取り込まれる evidence / proof / machine-readable artifact。ユーザーへ個別レビューを要求する判断面ではない |
| YMM4 | validator 通過後、または明示 creative acceptance の時だけ使う |

v1 は G-27 専用であり、F-01 / F-03 の復活ではない。YMM4 画面再現、
Python 画像生成、動画生成、素材自動取得は含めない。

## Production Design Spine

NotebookLM から YMM4 へ渡る制作設計は、次の背骨に従属させる。各 artifact は
自分の工程だけを完璧にするための独立成果物ではなく、GUI timeline で判断できる
可逆的な設計図の一部として扱う。

| layer | responsibility | user review role |
| --- | --- | --- |
| NotebookLM script | 元台本。発話、論旨、前後文脈の原典 | GUI が抜粋と構成として見せる。ユーザーに原文全体レビューを要求しない |
| Script Beat IR | 脚本、時間軸、segment、beat、narration cue、登場要素、主張、前後文脈を可逆的に保持する | GUI timeline / beat table の入力。画面座標や見た目を持たせない |
| Visual Direction Contract | 映像密度、色、モチーフ、人物表現、UI表現、抽象度、字幕領域の方針を定義する | GUI が要点と例外を表示する |
| Shot Layout Plan | 16:9 frame の主被写体、背景、視線誘導、文字量、proxy visual、字幕クリアランスを定義する | GUI の selected beat / frame detail で確認する |
| Motion Beat Plan | beginning / development / turn の変化、台本 cue との対応、動きの狙いを定義する | GUI の beat table で確認する |
| Proof PNG / HTML | render/openability/readback の evidence。視覚証跡として GUI に取り込む | 単体レビュー対象にしない |
| Review Decisions | GUI で保存する判断・コメント・分類 | 次の scene decision packet / gap report の入力 |
| YMM4 Adapter Output | validator 通過後に YMM4 へ渡す変換出力 | blocked 中は生成しない。creative acceptance と production timing の代替にしない |

## Script Beat IR Boundary

Script Beat IR は脚本家側の可逆地図であり、次だけを持つ:

- script line / CSV row / time span.
- segment / beat / narration cue.
- 登場要素、主張、前後文脈、論旨上の役割。

Script Beat IR は次を持たない:

- 画面座標、safe area、色、サイズ、CSS/HTML表現。
- YMM4 配置、template 名、motion parameter。
- proof PNG / HTML の都合に合わせた見た目。

脚本家の責務は脚本と時間地図まで。画面構成は Director / Shot Layout の責務に
分離する。

## Director / Shot Layout Boundary

Director / Shot Layout は一枚絵のアーティストではなく、破綻しない映像設計の
鋳型を作る工場長として扱う。責務は次の通り:

- 画面構成、主被写体、背景、視線誘導、文字量、字幕領域を決める。
- proxy visual、人物 / UI / 資料の相対比率、beat 内の変化を決める。
- 既存 HTML plate の微修正ではなく、Frame Contract に従う production frame を設計する。
- 検証メタ情報を production frame 内へ混ぜず、sidecar / GUI inspector 側へ隔離する。

## GUI Unification Rule

次の proof 以降、PNG / HTML / JSON を生成しても、ユーザー向けレビューは GUI 上で
行う。GUI には proof image、beat table、sidecar warnings、review controls を表示する。
未実装の段階では、slice 完了条件に「GUIで見える」または「GUI read-only ingest path が
定義されている」を含める。

通常フローでユーザーに raw JSON、HTML、単体 PNG の直接確認を要求しない。必要な場合は
debug / evidence として提示できるが、判断結果は GUI timeline と `review_decisions.json`
へ戻す。9-frame proof 単体の HTML 確認は完了扱いにしない。

## Data Contracts

`review_packet` は次を必須にする。

- `version`
- `episode_id`
- `review_scope`
- `default_decision_path`
- `source_refs`
- `gates`
- `episode_context`
- `story_outline[]`
- `segments[]`
- `overall_actions[]`

`episode_context` の最小必須項目:

- `title`
- `source_script`
- `script_line_count`
- `duration_sec`
- `thesis_ja`
- `audience_ja`
- `ending_question_ja`
- `review_scope_note`

`story_outline[]` の最小必須項目:

- `id`
- `title`
- `role_ja`
- `summary_ja`
- `line_start`
- `line_end`
- `time_start_sec`
- `time_end_sec`

`segments[]` の最小必須項目:

- `id`
- `title`
- `summary_ja`
- `scene_role_ja`
- `script_span`
- `script_excerpt_ja`
- `previous_context_ja`
- `next_context_ja`
- `decision_prompt`
- `risk`
- `options[]`
- `next_effect`

`options[]` は `label`、`classification_hint`、`next_effect` を持つ。
`classification_hint` は G-27 の `production_template_exists` /
`accepted_proxy` / `cut_from_plan` / `needs_revision` / `defer` /
`unselected` のいずれかに寄せる。

`review_decisions` は次を必須にする。

- `version`
- `episode_id`
- `review_scope`
- `source_packet`
- `saved_at`
- `overall_action`
- `overall_comment`
- `decisions[]`

`decisions[]` の最小必須項目:

- `segment_id`
- `decision`
- `comment`
- `classification_hint`

## Default Artifacts

| artifact | path |
| --- | --- |
| review packet | `samples/_probe/g24/real_estate_dx_review_packet.json` |
| decision output | `samples/_probe/g24/real_estate_dx_review_decisions.json` |
| detailed evidence | `samples/_probe/g24/real_estate_dx_overlay_card_review_map.md` |
| compact preview | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html` |
| compact preview screenshot | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_screenshot.png` |
| compact preview screenshot readback | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_screenshot_readback.json` |
| visual storyboard proof | `samples/_probe/g24/real_estate_dx_visual_storyboard_proof.png` |
| visual storyboard proof readback | `samples/_probe/g24/real_estate_dx_visual_storyboard_proof_readback.json` |
| visual treatment proof sidecar | `samples/_probe/g24/real_estate_dx_visual_treatment_proof.json` |
| visual treatment proof image | `samples/_probe/g24/real_estate_dx_visual_treatment_proof.png` |
| visual treatment proof HTML | `samples/_probe/g24/real_estate_dx_visual_treatment_proof.html` |
| visual treatment proof readback | `samples/_probe/g24/real_estate_dx_visual_treatment_proof_readback.json` |
| GUI treatment ingest screenshot | `samples/_probe/g24/real_estate_dx_gui_treatment_detail_screenshot.png` |
| GUI treatment ingest screenshot readback | `samples/_probe/g24/real_estate_dx_gui_treatment_detail_screenshot_readback.json` |
| validator authority | `samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json` |

## Workflow

1. GUI loads the default `review_packet` and renders episode context, story
   outline, and the RE-01〜RE-07E timeline.
2. User selects one timeline segment, reads its local script context, then records
   a decision and optional comment in the decision inspector.
3. GUI saves `review_decisions` to the default decision path.
4. Assistant reads `review_decisions` and creates the G-27 scene decision packet
   plus asset/proxy gap report.
5. Only after scenes are classified and the revised blueprint is ready may the
   validator path continue.

While the validator is `blocked`, forbidden next actions remain
`cast_motion_ir`, `ymm4_creative_acceptance`, and `production_timing`.

## Compact Preview Screenshot

Browser Use may reject local `file://` HTML. The stable developer-owned visual
evidence route is Electron capture:

```powershell
npm --prefix gui run capture:g27-overlay-review
```

The capture opens `real_estate_dx_overlay_only_compact_review.html` through
Electron `BrowserWindow.loadFile`, validates the overlay readback, compares
remaining blockers against the validator result, counts DOM segments/cards,
and writes a full-page PNG plus screenshot readback JSON. This is still visual
proof of placeholder visibility only. It is not creative acceptance, not
cast motion IR, and not production timing.

## Visual Storyboard Proof

The compact preview proves generation and DOM transport, but it is not enough
to judge video-like rhythm or cognitive load. For that, use the separate visual
proxy proof:

```powershell
npm --prefix gui run capture:g27-visual-storyboard
```

The storyboard generator reads the compact review manifest, then writes a 3×4
contact sheet PNG with one 16:9 proxy keyframe per RE-01〜RE-07E segment.
It renders proxy visuals for people, property documents, SNS screens, contracts,
warning UI, AI panels, gates, and curation tables instead of plain text cards.
The readback must confirm overlay readback `passed`, 11 storyboard segments,
11 keyframes, 24 placeholder/proxy objects, and remaining blockers matching the
validator result.

This artifact is diagnostic output only. `real_estate_dx_visual_storyboard_proof.png`
belongs to the Evidence Layer and may be used to verify segment count, placeholder
count, proxy visibility, and readback/blocker consistency. It must not be used as
a production input, production template, YMM4 source, render source, production
timing source, or creative acceptance substitute. Its current presentation-card
look is explicitly not the intended production visual direction.

## Visual Direction / Shot Layout Contract

The next visual work is not a refinement of the existing diagnostic contact
sheet. It is a new Visual Direction Layer plus Shot Layout Layer that designs
actual 16:9 production frames before any YMM4 conversion, render, or production
timing work.

Shot Layout Layer の **実装手順 (composition grid / visual role / element primitives) は
[`SCENE_COMPOSITION_SCHEMA.md`](SCENE_COMPOSITION_SCHEMA.md) (Scene Composition Schema v0.1)
を正本とする。** 本節の Frame Contract / 3-beat treatment は SCS に対する案件固有 (Real Estate DX)
の適用例として読む。SCS は 5 つの composition type (`split` / `center-focal` / `chain` /
`reveal` / `mediator`) と visual role vocabulary、element primitive rules を定義し、
`indexed whiteboard` / `grid-overload` / `drawing-semantics calibration` を anti-pattern として
明示する。

Layer responsibilities:

| layer | purpose | allowed output | must not do |
| --- | --- | --- | --- |
| Evidence Layer | Prove artifact generation, readback, segment counts, placeholder counts, and blocker consistency | diagnostic screenshots/readback JSON | Provide production composition |
| Visual Direction Layer | Define screen density, color, motif, character/UI abstraction, and visual hierarchy | design notes and treatment proof | Reuse diagnostic plate styling as production direction |
| Shot Layout Layer | Define production-frame composition per beat | 16:9 frame treatment / still proof | Mix validation metadata into the picture |
| Motion / Timing Layer | Map narration beats to beginning/development/turn motion ideas | beat plan only while validator is blocked | Start production timing, cast motion IR, or YMM4 creative acceptance |

Production-frame contract:

| item | contract |
| --- | --- |
| canvas | 16:9 production frame, planned at 1920x1080 even if proofs render smaller |
| safe area | Keep primary subjects and readable text inside the central 90%; avoid critical content in the outer 5% on each edge |
| subtitle clearance | Reserve the lower 18-22% of every frame for subtitles; UI proxy, characters, documents, and important labels must not collide with it |
| text on frame | Use at most 2 labels per frame and keep total in-frame label text within 30 Japanese characters |
| explanatory text | If the idea needs explanatory prose, split the shot or move the explanation to narration; do not pack prose into the frame |
| font floor | Plan for smartphone viewing: primary label 42px+ at 1080p, secondary label 32px+; avoid tiny metadata-like text |
| metadata isolation | Do not place `source`, `review`, `blocker`, segment IDs, validator status, readback counts, or other verification metadata inside production frames |
| exception sidecar | If text amount, safe area, or subtitle clearance must be broken, record the exception reason in a sidecar artifact rather than silently normalizing it |
| visual density | Prefer one main subject, one supporting object/UI, and one accent/risk marker per beat |

Each 3-beat visual treatment must include:

- `narration cue`: the script phrase or line range the beat answers.
- `visual subject`: what appears on screen as the main readable subject.
- `spatial composition`: where the subject, support object, and negative space sit.
- `text on frame`: exact planned labels, or `none`.
- `motion hint`: the visible change from the prior beat.
- `subtitle clearance`: where the lower 18-22% reserved area remains open.
- `risk`: why the beat could still fail visually or semantically.

## Initial 3-Beat Visual Treatments

These are design treatments for the first small visual proof only. They cover
three important segments, not all 11 segments, and do not authorize YMM4 work,
rendering, production timing, or creative acceptance.

### RE-02 — REINS / VIPクラブ

| beat | narration cue | visual subject | spatial composition | text on frame | motion hint | subtitle clearance | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| beginning | Lines 13-14: `レインズっていう言葉。これ要するに何なんですか?` | Consumer-facing search screen facing a closed professional database beyond a glass partition | Viewer/consumer device on left foreground; dark database room in upper-right background; empty lower band reserved | `REINS?` | Search results dim while the database silhouette becomes visible | Bottom 20% stays empty except subtitle; no UI panels cross it | Could still feel like a security-system metaphor instead of a data-access gap |
| development | Lines 15-19: `プロだけが入れる...巨大な物件データベース` / `一部の情報に過ぎない` | Professional REINS terminal as main subject, with public portal as a smaller filtered output | Large REINS monitor centered above subtitle-safe band; small public portal card to the right; character silhouettes stay small | `業者DB` / `公開ポータル` | Data cards flow from the central DB to a reduced public card | Lower 18-22% remains a plain dark gradient behind subtitle | VIP imagery can overstate exclusivity if the terminal is drawn as a luxury club |
| turn | Lines 20-23: `なんで...隠されているんですか?` / `情報の非対称性` | Gap between visible portal card and hidden raw data stack | Split screen: left public listing card; right stacked raw-data cards behind translucent wall; question mark near consumer silhouette | `見える情報` / `見えない情報` | Wall opacity increases and the public card shrinks, making the asymmetry legible | Subtitle band is uninterrupted across the full width | Too many data cards can recreate the dense presentation-card problem |

### RE-06 — キュレーション

| beat | narration cue | visual subject | spatial composition | text on frame | motion hint | subtitle clearance | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| beginning | Lines 61-64: `選択肢が多すぎること` | Overloaded property-choice grid | Dense but blurred property cards occupy top and side areas; one confused viewer silhouette sits center-left above subtitle band | `多すぎる選択肢` | Cards slide in from both sides until the center feels crowded | Bottom 20% remains clear; no card titles descend into subtitle space | Overcrowding is intentional but can still exceed readable density if labels are added |
| development | Lines 65-75: `ノイズを排除` / `デメリット...包み隠さず提示` | Curated shortlist with honest drawback badge | Three noisy cards fade into one large selected property sheet at center; drawback badge sits upper-right; curator hand/pointer on left | `選ぶ理由` / `注意点` | Noise cards desaturate and collapse into one clean sheet; drawback badge appears last | Selected sheet stops above subtitle band; badge stays in upper half | The badge can look like an ad warning unless the property sheet remains calm and editorial |
| turn | Lines 78-81: `独自の視点を買う` / `タイパと納得感` | Editorial lens transforming listings into meaning | Main frame shows a simple lens/curation table over one property; viewer silhouette on right nods toward selected option | `編集力` / `納得感` | Lens narrows the scene from many options to one coherent recommendation | Lower 22% left as a quiet floor/gradient for subtitles | Abstract lens motif may feel generic unless tied to property documents visually |

### RE-07D — AI逆説と見えないリスク

| beat | narration cue | visual subject | spatial composition | text on frame | motion hint | subtitle clearance | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| beginning | Lines 130-132: `あなたに100%マッチする物件はこれです` | AI recommendation panel with a perfect-match property | Large AI panel upper-left; property card upper-right; human silhouette small and centered, not blocking subtitles | `100%マッチ` | AI panel snaps to a confident green match state | Bottom 20% remains empty; no AI chat text enters subtitle area | Can look like AI promotion if the next beat does not clearly reveal what is missing |
| development | Lines 133-136: `データだけではない` / `目に見えないリスク` | Hidden risk layer under the recommended property | Property card remains visible above; below it, but above subtitle band, faint boundary dispute and inheritance relationship icons emerge | `見えないリスク` | Green match glow dims; risk icons fade in from behind the property card | Risk icons stay above the subtitle band; bottom reserved area remains blank | Risk icons can become too symbolic or horror-like if overdramatized |
| turn | Lines 137-143: `対人コミュニケーション` / `キュレーターとリスク管理のプロ` | Human specialist mediating between AI data and people | Specialist silhouette center-left connecting AI panel and two human silhouettes; risk icons reduce to small managed markers | `調整するプロ` | Specialist line/gesture connects the AI panel to people; risk markers settle instead of disappearing | Subtitle band remains a clean dark strip across the bottom | Must avoid implying AI is useless; the picture should show complementarity, not rejection |

## Completion Gate

This Review Console slice is complete when:

- `FEATURE_REGISTRY.md`, `GUI_MINIMUM_PATH.md`, and `runtime-state.md` name the
  GUI Review Console as the G-27 primary review surface.
- GUI loads `review_packet` from a repo-relative path.
- GUI displays episode context, story outline, and a timeline segment for all
  11 sections.
- Review tab hides the left production wizard and expands the review surface
  as the current workbench.
- Selecting a timeline segment displays that segment's script span, script
  excerpt, previous context, next context, scene role, risk, and next effect.
- The decision inspector preserves per-segment decision/comment state and saves
  the existing `review_decisions` schema.
- `scripts/check_g27_review_packet.js` passes. The check must fail when
  user-facing Japanese fields contain `???`, Unicode replacement characters,
  or too few Japanese characters for the field.
- `gui/review_console_dom_smoke.js` passes under Electron. The smoke must
  confirm `review-episode-context` and `review-story-outline` are visible,
  the left wizard is not displayed, timeline segments render for all 11
  sections, the detail/decision panes are visible, and the review tab text
  contains no `???` or `�`.
- GUI saves `review_decisions` to a repo-relative path and rejects path
  traversal or absolute paths.
- Electron compact preview capture passes and writes
  `real_estate_dx_overlay_only_compact_review_screenshot.png` plus
  `real_estate_dx_overlay_only_compact_review_screenshot_readback.json`;
  the readback must confirm overlay HTML readback `passed`, 11 visible segments,
  24 visible placeholders, and remaining blockers matching the validator result.
- Electron visual storyboard capture passes and writes
  `real_estate_dx_visual_storyboard_proof.png` plus
  `real_estate_dx_visual_storyboard_proof_readback.json`; the readback must
  confirm 3×4 contact sheet layout, 16:9 frame units, 11 proxy keyframes,
  24 proxy placeholders, and remaining blockers matching the validator result.
- `review_map.md` remains only as evidence/fallback detail.

For follow-on visual treatment proof slices, completion additionally requires:

- The proof image / HTML / sidecar JSON is visible in the GUI timeline or has a
  defined GUI read-only ingest path before it is treated as user-reviewable.
- The proof carries no production-frame metadata such as `source`, `review`,
  `blocker`, segment ID, validator status, or readback counts inside the frame.
- Standalone HTML/PNG/JSON confirmation is evidence only and does not complete
  the review slice by itself.

The implemented follow-on proof uses `npm --prefix gui run
capture:g27-visual-treatment` to create a 9-frame treatment for RE-02 / RE-06 /
RE-07D. v2 strengthens label-off readability, real-estate texture, and
motion-readiness while remaining a read-only visual treatment proof. The GUI
`デザインレビュー` timeline loads its sidecar, displays the proof image, marks the
three target segments with `3-beat proof`, and shows the selected segment's
beat table, narration cue, sidecar warnings, Frame Contract violation count,
motion primitives, and read-only decision context.

The sidecar must also carry four qualitative checks before the proof is treated
as reviewable in the GUI:

- `label-off check`: if labels are hidden or reduced, the closed database,
  choice overload, and invisible risk should still read from shapes and spatial
  changes.
- `narration competition check`: in-frame text must not compete with narration
  subtitles.
- `real-estate texture check`: real-estate-specific signs such as property cards,
  search UI, defect cards, boundary/inheritance/neighborhood risk, or hidden data
  should be visible without becoming a lecture slide.
- `motion-readiness check`: the three beats should be convertible to appearance,
  movement, and emphasis, not just static slide replacement.

For v2, the expected sidecar statuses are:

- `label_off_check = at_least_partial_pass`
- `narration_competition_check = pass_for_text_amount`
- `real_estate_texture_check = pass_or_strong_partial`
- `motion_readiness_check = pass_or_strong_partial`

These statuses do not authorize production templates, YMM4 conversion, render,
production timing, or creative acceptance. Frame Contract violations may be
zero, but zero violations only means formal contract compliance for this proof.
It is not production readiness.

`Modern_Real_Estate_Strategic_Playbook.pdf` is a user-provided anti-pattern
corpus only. It is not a production asset and not a layout reference. Use it to
avoid drifting back into long-text slides, comparison matrices, dashboards,
flowcharts, and audit/checklist pages.
