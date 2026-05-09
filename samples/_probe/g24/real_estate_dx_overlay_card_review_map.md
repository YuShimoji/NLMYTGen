# Real Estate DX Overlay/Card Review Map

Status: reviewer-facing map for `overlay_only_compact_review`

This file is the human review layer for the generated compact review. It is intentionally a list/table view because the HTML artifact is useful as a visual preview but too scroll-heavy to explain why each card exists.

## Why This Map Exists

| problem found in review handoff | correction in this map | effect |
|---|---|---|
| HTML preview appeared as a finished answer without the process behind it. | Each segment lists intent, granularity, and rationale. | Reviewer can judge the design path, not only the final-looking surface. |
| JSON/readback was too close to internal wiring. | JSON is treated only as machine proof. | Reviewer is not asked to infer judgement from raw data. |
| Alternative plans were not visible enough to judge whether they were real options or strawmen. | Each row has a `why this instead of alternatives` field. | Missing or weak rationale can be called out directly. |
| Scroll-heavy review makes list-level comparison hard. | The primary review surface is this compact table. | Reviewer can scan all segments before opening the HTML. |
| Work surfaces are scattered across JSON / HTML / docs. | This map is the temporary review workbench until a GUI can unify the process. | Review happens on one table instead of many raw artifacts. |

## Review Contract

| key | value |
|---|---|
| artifact path | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html` |
| readback result | `status=passed`, `segments=11`, `placeholder_items_rendered=24`, `ShapeItem=24` |
| allowed_next_actions | `[overlay_only_compact_review]` |
| forbidden_next_actions | `[cast_motion_ir, ymm4_creative_acceptance, production_timing]` |
| remaining blockers | `ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING`, `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING` |
| not creative acceptance | `true` |

## Surface Roles

| surface | role | not a substitute for |
|---|---|---|
| this map | reviewer-facing report and segment judgement table | final GUI workbench |
| HTML compact review | visual preview surface | rationale / alternative comparison |
| JSON manifest | source-linked machine wiring | manager-facing report |
| readback JSON | generated-artifact proof | creative acceptance |
| future GUI | ideal single kitchen/workbench for review and validation | current blocked cast/prop readiness |

## Plan Selection Logic

| plan | what it would do | merit | why it is not the current plan |
|---|---|---|---|
| Dense card-per-detail plan | Turn most script claims into individual cards. | High coverage; easy to trace every claim. | Too many cards for user-side review; recreates raw-data overload in visual form. |
| One headline per script block | Use only broad title cards for each major topic. | Very quick to scan. | Hides the point that needs judgement: which visible ideas, risks, or transitions should appear. |
| Motion/prop-ready skit plan | Treat each segment as cast acting, props, and screen choreography. | Closest to eventual production staging. | Forbidden now because cast templates and real-estate props are still blocked. |
| Overlay-only compact plan | Use a small number of source-tied overlay/card placeholders per segment. | Reviewable without pretending creative acceptance is complete. | Chosen for this lane because validator only allows `overlay_only_compact_review`. |

Chosen plan: overlay-only compact plan.

Selection rationale: it is the only plan that keeps the current `blocked` validator state honest while still giving the reviewer a real design surface. The other plans are not fake options: dense cards may become useful for source audit, headline-only may become useful for a one-page executive summary, and motion/prop staging may become useful after cast/prop blockers are resolved. They are not the right current plan because this artifact is integration review material, not production staging.

## Granularity Ladder

| granularity | use when | review risk |
|---|---|---|
| single visual claim | One idea should land cleanly, often at a warning or final thesis. | May hide supporting context if overused. |
| compact set of visible claims | A segment needs 2-4 related visible ideas to preserve causality. | Can become a mini-slide deck if every phrase becomes a card. |
| dense detail cards | Source audit or evidence review needs item-by-item traceability. | Not suitable as the first manager-facing review surface. |
| motion/prop choreography | Cast, props, and templates are available and accepted. | Forbidden in this lane until blockers are cleared. |

## How To Judge This Review

| review question | pass means | fail means |
|---|---|---|
| What do we want to put on screen? | The card/overlay expresses one visible idea that helps the script. | The card is decorative, redundant, or not tied to the script. |
| Is the granularity right? | The segment is neither a raw data dump nor a vague mood board. | Too many micro-cards, or one card hides several ideas. |
| Why this plan over alternatives? | The chosen card is more readable or source-safe than the alternatives. | The alternative was only a strawman or the choice rationale is missing. |
| Can a manager review it quickly? | The list below is enough to judge direction before opening the HTML. | The reviewer must inspect raw JSON or scroll the whole HTML to understand intent. |

## Candid Review Rule

| review stance | what to do |
|---|---|
| If intent is unclear | Mark the segment `revise` and ask for a clearer `what to show`. |
| If granularity is wrong | Mark `reduce` or `split`, even if the HTML looks polished. |
| If rationale is weak | Mark `rationale missing`; do not accept a plan because it is the only rendered option. |
| If the surface is hard to review | Mark `report packaging failure`; do not treat raw JSON or scroll-heavy HTML as sufficient. |
| If it looks production-ready | Still keep `not creative acceptance` until cast/props blockers are resolved. |

## Segment Decision Map

| segment | source range | what to show | granularity choice | why this instead of alternatives | reviewer check |
|---|---:|---|---|---|---|
| RE-01 自力検索 | lines 1-12 | スマホ=魔法の鍵; 物件カード増殖; 遠景の閉じた扉 | compact set of visible claims | consumer access metaphor; future gatekeeper foreshadow; search results | accept / reduce / replace / needs source-backed prop |
| RE-02 REINS-VIPクラブ | lines 13-24 | REINS / VIPクラブ; 生データDB; 一般ポータル（一部情報） | compact set of visible claims | inside information; outside partial information; private database barrier | accept / reduce / replace / needs source-backed prop |
| RE-03 保護理由 | lines 25-36 | プライバシー / リスク / 秩序; 背後の利益の影 | compact set of visible claims | dark-side hint; legitimate protection reasons | accept / reduce / replace / needs source-backed prop |
| RE-04 囲い込み | lines 37-48 | 売主 ⇄ 業者 ⇄ 買主; 商談中; 他社ルート閉鎖 | compact set of visible claims | blocked alternative path; double-agency relationship; route blocking sign | accept / reduce / replace / needs source-backed prop |
| RE-05 QR透明化 | lines 49-60 | QR / 公開ステータス; 半分開いた扉 | compact set of visible claims | barrier opening; transparency state change | accept / reduce / replace / needs source-backed prop |
| RE-06 キュレーション | lines 61-82 | 候補を整理するテーブル; 欠点も見せるカード; 少ないが意味のある候補 | compact set of visible claims | curated shortlist; curation process; honest defect disclosure | accept / reduce / replace / needs source-backed prop |
| RE-07A Z世代ライフスタイルとSNS信頼 | lines 83-102 | タイパ / 推し活 / TVなし; SNSで顔が見える信頼 | compact set of visible claims | Gen-Z condition shift; influencer trust setup | accept / reduce / replace / needs source-backed prop |
| RE-07B SNS集客のグレーゾーン | lines 103-113 | 無免許 / おとり広告リスク | single visual claim | SNS gray-zone warning | accept / reduce / replace / needs source-backed prop |
| RE-07C 2030年問題と攻めのDX | lines 114-129 | 空き家 / ハザード / 相続; AIコンシェルジュ | compact set of visible claims | DX customer experience; specialist risk domains | accept / reduce / replace / needs source-backed prop |
| RE-07D AI逆説と見えないリスク | lines 130-143 | AIの100%マッチ物件; 境界紛争 / 相続 / 感情調整 | compact set of visible claims | AI recommendation thesis; invisible human risk | accept / reduce / replace / needs source-backed prop |
| RE-07E 選び方の基準と最後の問い | lines 144-152 | 専門的キュレーター / リスク管理者 / 買ってはいけない理由 | single visual claim | final guide criteria | accept / reduce / replace / needs source-backed prop |

## Non-Negotiable Boundaries

- This map is not `cast_motion_ir`.
- This map is not `ymm4_creative_acceptance`.
- This map is not `production_timing`.
- JSON/readback files are machine proof, not a sufficient manager-facing review report by themselves.
- The HTML artifact is a preview surface; this list is the primary reviewer-facing overview.

## Reviewer Reply Shape

```text
integration review result: pass / revise / blocked

segment decisions:
- RE-xx: accept / reduce / replace / needs source-backed prop — reason

plan rationale concerns:
- missing why-this-plan rationale: RE-xx
- possible strawman alternative: RE-yy

do not advance:
- cast_motion_ir
- ymm4_creative_acceptance
- production_timing
```
