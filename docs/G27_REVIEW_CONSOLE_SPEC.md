# G-27 Review Console Spec

G-27 Real Estate DX の制作判断を Electron GUI の `デザインレビュー`
タブに集約するための v1.2 仕様。Markdown / HTML / chat は補助に降格し、
判断結果は JSON として repo に戻す。

v1.2 の主な修正点は、`デザインレビュー`を既存制作ウィザードへ載せた
カード一覧ではなく、全幅のタイムライン型 Review Workbench として扱うこと。
動画全体の流れから segment を選び、台本文脈・演出意図・次工程への影響を
同じ画面で確認してから判断を保存する。

## Responsibility Split

| surface | role |
| --- | --- |
| GUI `デザインレビュー` | primary review surface。全幅 Review Workbench として、動画全体の概略、横タイムライン、選択 segment の台本抜粋、判断ペインを見せて判断を受け、保存する |
| `review_packet.json` | GUI が読む判断単位。episode context、story outline、segment、選択肢、source refs、gate を持つ |
| `review_decisions.json` | GUI が保存する差し戻し伝票。次の scene decision packet / gap report の入力 |
| `*_review_map.md` | 根拠ログ。通常レビューでは読ませない |
| compact HTML / readback JSON | proof / preview。最終品質や production timing の承認ではない |
| YMM4 | validator 通過後、または明示 creative acceptance の時だけ使う |

v1 は G-27 専用であり、F-01 / F-03 の復活ではない。YMM4 画面再現、
Python 画像生成、動画生成、素材自動取得は含めない。

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
validator result. This is `visual_proxy_proof`; it is still not creative
acceptance and does not unlock cast motion IR or production timing.

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
