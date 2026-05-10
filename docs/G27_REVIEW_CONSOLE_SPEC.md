# G-27 Review Console Spec

G-27 Real Estate DX の制作判断を Electron GUI の `デザインレビュー`
タブに集約するための v1.1 仕様。Markdown / HTML / chat は補助に降格し、
判断結果は JSON として repo に戻す。

v1.1 の主な修正点は、局所的な overlay/card 判断だけでなく、台本全体の
概略、RE-01〜RE-07E の構成、各 segment の台本抜粋と前後文脈を GUI に
載せること。ユーザーに演出カードだけを見せて演技指導を求める状態にしない。

## Responsibility Split

| surface | role |
| --- | --- |
| GUI `デザインレビュー` | primary review surface。動画全体の概略、構成、短い日本語カード、台本抜粋を見せて判断を受け、保存する |
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
| validator authority | `samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json` |

## Workflow

1. GUI loads the default `review_packet` and renders episode context, story
   outline, local script context, and segment cards.
2. User selects a decision per segment and may add comments.
3. GUI saves `review_decisions` to the default decision path.
4. Assistant reads `review_decisions` and creates the G-27 scene decision packet
   plus asset/proxy gap report.
5. Only after scenes are classified and the revised blueprint is ready may the
   validator path continue.

While the validator is `blocked`, forbidden next actions remain
`cast_motion_ir`, `ymm4_creative_acceptance`, and `production_timing`.

## Completion Gate

This Review Console slice is complete when:

- `FEATURE_REGISTRY.md`, `GUI_MINIMUM_PATH.md`, and `runtime-state.md` name the
  GUI Review Console as the G-27 primary review surface.
- GUI loads `review_packet` from a repo-relative path.
- GUI displays episode context, story outline, each segment's script span,
  script excerpt, previous context, next context, and scene role.
- `scripts/check_g27_review_packet.js` passes. The check must fail when
  user-facing Japanese fields contain `???`, Unicode replacement characters,
  or too few Japanese characters for the field.
- `gui/review_console_dom_smoke.js` passes under Electron. The smoke must
  confirm `review-episode-context` and `review-story-outline` are visible,
  segment cards render for all 11 segments, and the review tab text contains
  no `???` or `�`.
- GUI saves `review_decisions` to a repo-relative path and rejects path
  traversal or absolute paths.
- `review_map.md` remains only as evidence/fallback detail.
