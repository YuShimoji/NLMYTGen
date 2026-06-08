# G-28 Real Estate YMM4 Probe Human Review - 2026-06-07

This record captures the human GUI review result for the self-contained YMM4
diagnostic probe of the G-28 `real_estate_information_gap` Lecture Diagram
Carrier.

This is a diagnostic review result only. It is not production carrier approval,
creative final acceptance, render approval, rights approval, publishing approval,
or permission to set `production_candidate=true`.

## Reviewed Artifact

| Field | Value |
| --- | --- |
| probe artifact id | `g28_lecture_diagram_carrier_real_estate_information_gap_ymmp_probe_v1` |
| source artifact id | `g28_lecture_diagram_carrier_real_estate_information_gap_v1` |
| variant id | `g28_ldc_real_estate_information_gap` |
| YMM4 probe | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe.ymmp` |
| readback | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_readback.json` |
| report | `samples/_probe/g28/lecture_diagram_carrier_real_estate_information_gap_ymmp_diagnostic_probe_report.md` |
| readback status | `passed` |
| readback classification | `pass_probe_polished` |
| diagnostic_only | `true` |
| production_candidate | `false` |

## Human Review Result

```text
openability: pass
notes: YMM4で開ける。probeとして成立。

focal_chain_readability: pass
notes: 元付情報 -> ポータル掲載 -> 借主判断 の流れは読める。

caption_reserve: pass
notes: 下部20%の予約帯は概ね確保されている。

callout_readability: pass_partial
notes: 情報遅延 / 掲載粒度の欠落 / 仲介インセンティブ は読めるが、全体の洗練度はまだ改善余地あり。

host_role: pass
notes: hostは主役化していない。

alignment_and_polish: partial
notes: 黄色い線の処理、矩形内テキストの整列、微妙な視覚ズレが気になる。構造破綻ではないが、動画としての認知摩擦をさらに下げる余地がある。

real_service_or_property_look: safe
notes: 実在サービス・実在物件感は強くない。

diagnostic_boundary: clear
notes: production完成品ではなく、診断用probeとして理解可能。

overall_decision: revise_probe
production_boundary_acknowledged: true
```

## Decision Interpretation

The probe passes as a diagnostic review surface:

- YMM4 openability is confirmed.
- The focal chain reads as `元付情報 -> ポータル掲載 -> 借主判断`.
- The bottom caption reserve is broadly preserved.
- The lower-corner hosts do not become focal.
- The surface does not strongly resemble a real service or real property.
- The diagnostic-only boundary is clear.

The probe is not accepted as production-ready. The human decision is
`revise_probe`, with the revision target limited to visual polish and alignment:

- yellow connector line treatment
- text alignment inside rectangles
- small visual offsets that create recognition friction
- callout polish while preserving 2-3 callouts and avoiding table/list density

## Allowed Next Slice

The next safe artifact is a bounded diagnostic polish revision of this same
YMM4 probe. It may adjust primitive geometry, connector treatment, text
centering, and callout spacing while preserving:

- `variant_id=g28_ldc_real_estate_information_gap`
- `diagnostic_only=true`
- `production_candidate=false`
- frame `1920x1080 / 16:9`
- bottom 20% caption reserve
- focal chain `元付情報 -> ポータル掲載 -> 借主判断`
- callouts `情報遅延`, `掲載粒度の欠落`, `仲介インセンティブ`
- non-focal host role
- `dense_table=false`
- `indexed_whiteboard=false`
- no external image, URL, raw reference, source footage, audio, TTS, render, or
  production approval

If revised, the builder/readback/report should keep the diagnostic boundary
visible and report the same safety counts. A revision may either update the
existing diagnostic probe output in place or create a clearly versioned v2 probe,
as long as the report states that the previous human result was `revise_probe`
and the new output remains diagnostic-only.

## Bounded Polish Revision Generated

The bounded diagnostic polish revision was generated in place after this
`revise_probe` result. The updated builder/readback/report classify the revised
probe as `pass_probe_polished`.

Revision scope:

- yellow connector alignment
- rectangle text centering through existing TextItem top-left conventions
- callout slot spacing and readability
- small visual offsets only

Preserved boundary:

- `diagnostic_only=true`
- `production_candidate=false`
- no render, production approval, creative final acceptance, rights automation,
  source footage, audio, TTS, image, URL, raw reference, slot-fill, G-27 revival,
  ClipPipeGen access, RSS work, or NotebookLM work

## Human GUI Re-review Result After Polish

```text
openability: pass
notes: YMM4で開ける。probeとして成立。

focal_chain_readability: pass
notes: 元付情報 -> ポータル掲載 -> 借主判断 の流れは読める。

caption_reserve: pass
notes: 下部20%の字幕帯は概ね確保されている。

yellow_connector_treatment: pass_partial
notes: 以前よりかなり直っている。線の長さ・位置・太さは改善しているが、座標規則が定式化されているかは不明。

rectangle_text_alignment: pass_partial
notes: 前回よりかなり改善しているが、矩形内テキストの中心位置が font / box / window size に基づく計算式で安定しているかは未確認。目分量の微調整に見える懸念がある。

callout_readability: pass
notes: callout は読みやすくなっている。過密感は大きくない。

host_role: pass
notes: hostは主役化していない。

real_service_or_property_look: safe
notes: 実在サービス・実在物件感は強くない。

diagnostic_boundary: clear
notes: production完成品ではなく診断用probeとして理解できる。

overall_decision: accept_as_diagnostic_gui_probe_with_layout_contract_followup
production_boundary_acknowledged: true
```

## Re-review Interpretation

The polished probe is accepted as a diagnostic GUI probe, not as production
approval. The human review confirms that openability, focal-chain readability,
caption reserve, callout readability, host role, real-service/property safety,
and diagnostic boundary are sufficient for probe use.

The remaining concern is not another few-pixel polish pass. The next safe action
is a layout contract audit that makes the reusable placement rules explicit:

- rectangle text centering formula
- connector positioning formula
- callout slot layout rule
- manual offset registry
- tolerance readback
- decision after audit: Review Console ingest versus one bounded layout-system
  revision

No `.ymmp` regeneration, builder change, new variant, render, production
approval, creative final acceptance, rights automation, source footage, audio,
TTS, external image, URL, raw reference, G-27 revival, ClipPipeGen access, RSS
work, or NotebookLM work is approved by this re-review.

## Human GUI Recheck Result After Layout Contract

```text
openability: pass
focal_chain_readability: pass
connector_treatment: pass
caption_reserve: pass
callout_readability: pass
host_role: pass
rectangle_text_alignment: partial
layout_metrics_trust: partial
overall_decision: revise_probe_again_narrow_right_node_text_alignment
production_boundary_acknowledged: true
```

Interpretation:

- The probe still opens in YMM4 and remains valid as a diagnostic probe.
- The focal chain, connector treatment, caption reserve, callouts, and host role
  all pass.
- The only remaining GUI concern is the right-side node label `借主判断`,
  which appears optically off-center inside its rectangle.
- The existing readback reported `text_center_error_px=0`, so the mismatch is
  between registered placement metrics and rendered YMM4 optical perception.

## Narrow Right-Node Alignment Fix

The diagnostic builder was updated after the recheck with
`g28_real_estate_information_gap_right_node_alignment_v1`.

Result:

- classification: `pass_right_node_alignment_fixed`
- target label: `G28_LDC_Node_Right_Label`
- target text: `借主判断`
- previous registered offset: `{ x: 0, y: -4 }`
- new registered offset: `{ x: 4, y: -4 }`
- scope: right-node label only
- no common text-centering formula change
- no other node label, callout, connector, host, caption reserve, production, or
  external-material change

Readback caveat:

`text_center_error_px=0` now means the right label was placed exactly at the
registered offset. It does not claim rendered YMM4 glyph-pixel optical proof;
human GUI review remains the authority for final visual centering.

## Human GUI Target Correction After Right-Node Fix

```text
openability: pass
focal_chain_readability: pass
connector_treatment: pass
caption_reserve: pass
host_role: pass
previous_target_correction: the actual concern is the lower-right callout, not the right node
callout_label_alignment: partial
target_label: 仲介インセンティブ
layout_metrics_trust: partial
overall_decision: revise_probe_again_narrow_callout_label_alignment
production_boundary_acknowledged: true
```

Interpretation:

- The previous right-node alignment fix was a target-identification miss, but no
  adverse side effect was reported, so it is retained.
- The corrected human target is the lower-right callout label
  `仲介インセンティブ`.
- Other callouts, node labels, connector treatment, host role, and caption
  reserve are treated as acceptable.

## Narrow Callout Label Alignment Fix

The diagnostic builder was updated after the target correction with
`g28_real_estate_information_gap_callout_label_alignment_v1`.

Result:

- classification: `pass_callout_label_alignment_fixed`
- target label: `G28_LDC_CalloutSlot_3_Label`
- target text: `仲介インセンティブ`
- previous registered offset: `{ x: 0, y: -3 }`
- new registered offset: `{ x: 4, y: -3 }`
- previous right-node fix: retained
- scope: lower-right callout label only
- no common callout formula change
- no other node label, callout slot, connector, host, caption reserve,
  production, or external-material change

Readback caveat:

`text_center_error_px=0` now means the callout label was placed exactly at the
registered offset. It does not claim rendered YMM4 glyph-pixel optical proof;
human GUI review remains the authority for final visual centering.

## Human GUI Calibration After Callout Fix

```text
openability: pass
focal_chain_readability: pass
connector_treatment: pass
caption_reserve: pass
host_role: pass
callout_label_alignment:
  status: fail_after_previous_fix
  target_label: 仲介インセンティブ
  current_observed_issue: previous X=289 still reads left-shifted
  human_measured_correct_x: 313.0
overall_decision: apply_one_time_human_calibrated_callout_x_and_record_layout_debt
production_boundary_acknowledged: true
```

Interpretation:

- The lower-right callout label misalignment persisted after the bounded
  `x=289` correction.
- The human-measured correct YMM4 TextItem X is `313.0`.
- This value is a one-time human-calibrated override, not proof that the callout
  label formula is reusable.
- The delta from the previous polished X is `24px`; this is recorded as callout
  text layout system debt.
- If the label still reads off after this calibration, stop individual
  pixel/offset tuning and switch to callout text layout system redesign.

Result:

- revision: `g28_real_estate_information_gap_callout_label_human_calibration_v1`
- classification: `pass_callout_label_human_calibrated`
- target label: `G28_LDC_CalloutSlot_3_Label`
- target text: `仲介インセンティブ`
- computed X before human calibration: `289`
- previous polished X: `289`
- human calibrated X: `313.0`
- calibration delta X: `24`
- no common callout formula success claim
- no other node label, callout slot, connector, host, caption reserve,
  production, or external-material change

## Human GUI Recheck After X=313 Calibration

```text
openability: pass
openability_notes: YMM4で開ける。diagnostic probeとして成立。

callout_label_alignment_仲介インセンティブ: pass
callout_label_alignment_notes: 大きなズレはなく、一旦これで進められる。細かな光学中心の検出精度には不安が残るため、layout metric debt は保持する。

title_position: pass_with_metric_caveat
title_position_notes: 上部タイトルは視認上は問題ない。YMM4上のタイトル位置は y=-474.5。現時点で修正対象ではないが、title anchor / title text center / safe area を後続readback項目として検出できるようにしたい。

host_placeholders: pass_as_diagnostic_placeholder
host_placeholders_notes: 左右下のグレー角丸矩形は host placeholder として診断probe上は正常。ただし production ではこのまま使わず、キャラ素材・AI画像・別表現への置換または非表示判断が必要。

focal_chain_readability: pass
connector_treatment: pass
other_callout_side_effect: none
right_node_side_effect: none
caption_reserve: pass
diagnostic_boundary: clear
overall_decision: accept_for_review_console_ingest_candidate_with_layout_metric_caveat
production_boundary_acknowledged: true
```

Interpretation:

- The X=313 human-calibrated lower-right callout label is accepted for moving
  from GUI probe review into Review Console ingest candidate planning.
- This is not actual Review Console ingest, production carrier approval,
  creative final acceptance, render approval, or rights/production automation.
- The title is visually acceptable for the current diagnostic probe, but later
  readback should add title anchor, title text center, and title safe-area
  checks instead of continuing manual YMM4 coordinate tuning.
- The lower-corner host rectangles are diagnostic placeholders only. A later
  production path must decide whether to replace them with character material,
  AI-generated/static visual treatment, another representation, or hide them.
- The callout X=313 remains a human-calibrated override and layout metric debt,
  not a reusable callout text formula success.

Review Console ingest candidate caveats:

- Carry `diagnostic_only=true` and `production_candidate=false` forward.
- Treat YMM4 glyph optical center as not directly measured by current readback.
- Add title anchor / title text center / title safe-area readback before relying
  on this pattern as a reusable Review Console screen input.
- Keep host placeholders as diagnostic-only evidence; do not treat them as
  production-ready character or visual assets.

## Final Human GUI Confirmation - Diagnostic Review Surface Accepted

```text
openability: pass
notes: YMM4で開ける。diagnostic probeとして成立。

focal_chain_readability: pass
notes: 元付情報 -> ポータル掲載 -> 借主判断 の流れは読める。

connector_treatment: pass
notes: 黄色connectorはうまく繋がっている。偶然でなければ高い精度。

callout_label_alignment_仲介インセンティブ: pass
notes: X=313.0 human-calibrated override 後、大きなズレはない。一旦これで進められる。

title_position: pass_with_minor_metric_caveat
notes: 上部タイトルは、見た目としては大きな問題ではないが、ボックス内でやや下揃えっぽく見える。今回は修正対象にせず、title_anchor / title_text_center / safe-area readback debt として残す。

host_placeholders: pass_as_diagnostic_placeholder
notes: 左右下のグレー角丸矩形は host placeholder として diagnostic probe 上は正常。ただし production visual/material ではない。後続の material / AI image / character visual slice で replace / hide / accept を判断する。

caption_reserve: pass
notes: 下部字幕帯の余白は保たれている。

diagnostic_boundary: clear
notes: production完成品ではなく、diagnostic probeとして理解できる。

overall_decision: accept_as_diagnostic_review_surface_with_title_metric_caveat
production_boundary_acknowledged: true
```

Interpretation:

- The `real_estate_information_gap` YMM4 probe is accepted as a diagnostic
  review surface with title metric caveat retained.
- This closes the individual YMM4 pixel-tuning loop for this probe. Do not make
  more one-off title Y, callout, right-node, X/Y, or optical offset corrections
  for this artifact.
- If future visual-centering problems remain material, handle them as a separate
  text/layout system redesign slice instead of continuing per-label offsets.
- The X=313.0 callout position remains a human-calibrated override and layout
  metric debt, not formula success.
- Title positioning is visually acceptable for this diagnostic review surface,
  but `title_anchor`, `title_text_center`, and title safe-area readback remain
  future metric items.
- Lower-corner host rectangles are valid diagnostic placeholders only. They are
  not production character material, AI image material, or final visual assets.
- Existing Review Console ingest evidence remains consistent with this result:
  it is evidence for the read-only diagnostic panel and does not approve
  production, render, rights/public use, or creative final acceptance.

Next safe action:

- Treat the real-estate side evidence as closed for the current diagnostic
  review surface and return to the active runtime-state lane.
- If needed later, open a separate Review Console human confirmation record or
  diagnostic render planning slice only by explicit request.

## Boundaries

- No production carrier approval.
- No creative final acceptance.
- No production render, video, or publishing output.
- No rights automation.
- No real material slot-fill.
- No external image, URL, raw reference, source footage, real service capture, or
  real property material.
- No G-27 revival or G-27 diagnostic carrier promotion.
- No RSS / OPML / Inoreader / NotebookLM source-pack work.
- No ClipPipeGen or cross-repo work.
