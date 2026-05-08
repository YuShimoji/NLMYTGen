# Real Estate DX Background Skit Blueprint Validation (2026-05-06)

## Meaning

不動産DXの背景茶番劇を、説明メモではなく `background_skit_blueprint.json` と validator result に落とした。

この結果は **IR / YMM4 production timing へ進める許可ではない**。機械的な行範囲・尺・密度の整合は取れたが、実制作に必要な人物 template / props / RE-07 小節分割が未解決なので、現在の状態は `blocked` である。

## Inputs

| item | value |
|---|---|
| source script | `samples/不動産DX_魔法の鍵とキュレーション.txt` |
| script line count | `152` |
| script sha256 | `f3c2fab2e4ecd965e85795dcf908cfffe1f4c3364c94962f7b9c7ad407af8fb9` |
| timing source | `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` |
| fps | `60` |
| total duration | `1049.533333 sec` |
| duration formula | `max(Frame + Length) / fps` |

## Artifacts

| artifact | role |
|---|---|
| `samples/_probe/g24/real_estate_dx_background_skit_blueprint.json` | source-backed blueprint artifact |
| `samples/_probe/g24/real_estate_dx_background_skit_blueprint_validate.json` | validator result |
| `samples/_probe/g24/real_estate_dx_background_skit_gap_report.json` | RE-07 sub-beat split and template/proxy classification |
| `samples/_probe/g24/real_estate_dx_row_time_map.json` | script line → CSV row → VoiceItem time map |
| `samples/_probe/g24/real_estate_dx_script_maturity_diagnostic.json` | script maturity / ideal-script delta diagnostic |
| `samples/_probe/g24/real_estate_dx_overlay_card_placeholder_map.json` | overlay/card placeholder map for safe compact review planning |
| `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html` | generated overlay-only compact review artifact for human integration review |
| `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp` | ShapeItem-only YMM4 carrier for machine readback; not creative acceptance |
| `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.json` | compact review manifest |
| `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_readback.json` | compact review readback result |

## Validator Result

| field | value |
|---|---|
| status | `blocked` |
| errors | `[]` |
| warnings | `[]` |
| active visual coverage | `70.0%` |
| intentional rest duration | `314.86 sec` |
| unexplained empty duration | `0 sec` |
| visual states per minute | `0.400178` |
| resolved blockers | `SCRIPT_BLOCKED_RE07_TOO_BROAD` |
| remaining blockers | `ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING`, `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING` |
| allowed next actions | `overlay_only_compact_review` |
| forbidden next actions | `cast_motion_ir`, `ymm4_creative_acceptance`, `production_timing` |

The validator exited with code `2`, which is the expected `blocked` result. It is now a **narrow blocked** state: script timing authority is resolved, while production cast/props remain blocked.

## Row-To-Time Map

`real_estate_dx_row_time_map.json` resolves the source script to the actual imported YMM4 timeline:

| field | value |
|---|---|
| status | `passed` |
| script lines | `152` |
| CSV rows consumed | `352 / 352` |
| VoiceItems matched | `352 / 352` |
| mapping basis | normalized source line text → one or more CSV rows → sorted VoiceItem ordinal |

The RE-07 sub-beat timings were corrected from line-count estimates to actual VoiceItem timings:

| sub-beat | lines | CSV rows | start-end sec |
|---|---:|---:|---:|
| RE-07A | `83-102` | `186-226` | `531.7-653.716667` |
| RE-07B | `103-113` | `227-252` | `653.716667-730.25` |
| RE-07C | `114-129` | `253-296` | `730.25-864.116667` |
| RE-07D | `130-143` | `297-331` | `864.116667-979.95` |
| RE-07E | `144-152` | `332-352` | `979.95-1049.533333` |

## Script Maturity Result

`real_estate_dx_script_maturity_diagnostic.json` keeps the distinction between script maturity and YMM4 readiness:

| result | value |
|---|---|
| overall status | `blocked_for_cast_motion_ir_overlay_only_can_continue` |
| overlay placeholder map | allowed |
| cast motion IR | blocked |
| YMM4 creative acceptance | blocked |

The script is strong enough for an overlay/card compact review because each block has a thesis, causality, and visual anchor. It is not ready for cast-motion IR because the real-estate cast templates are missing and the old cue list was line-reaction shaped.

## Overlay/Card Placeholder Map

`real_estate_dx_overlay_card_placeholder_map.json` defines `24` placeholder items in normalized screen coordinates. It intentionally avoids delivery-template cast reuse.

The first safe review scope is **overlay/card-only compact review**:

- cards, doors, QR/status boards, warnings, and final criteria cards may be shown as placeholders,
- consumer / gatekeeper / curator body motion remains blocked,
- `delivery_v1_templates.ymmp` remains reserved for the delivery mini scene or explicit movement proxy only,
- this map is not creative acceptance by itself.

## Overlay-Only Compact Review Generation

The permitted next action was executed without advancing into cast motion IR, YMM4 creative acceptance, or production timing.

| field | value |
|---|---|
| compact review artifact | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html` |
| YMM4 shape carrier | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.ymmp` |
| manifest | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.json` |
| readback | `samples/_probe/g24/real_estate_dx_overlay_only_compact_review_readback.json` |
| segments | `11` |
| placeholder items rendered | `24` |
| YMM4 carrier item types | `ShapeItem=24` |

Closeout literal keys:

- artifact path: `samples/_probe/g24/real_estate_dx_overlay_only_compact_review.html`
- readback result: `status=passed`, `segments=11`, `placeholder_items_rendered=24`, `YMM4 carrier ShapeItem=24`
- allowed_next_actions: `[overlay_only_compact_review]`
- forbidden_next_actions: `[cast_motion_ir, ymm4_creative_acceptance, production_timing]`
- remaining blockers: [`ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING`, `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING`]
- not creative acceptance

Readback guarantees:

- The compact review is **not creative acceptance**.
- The compact review is **not production timing**.
- The compact review uses **no cast motion IR**.
- The YMM4 carrier contains only `ShapeItem` placeholders.
- The YMM4 carrier contains no `skit_group:` remarks and no `delivery_` template reuse.

## Block Timetable

| block | lines | start-end | duration sec | purpose |
|---|---:|---:|---:|---|
| RE-01 自力検索 | `1-12` | `00:00-01:53` | `112.933333` | consumer search / smartphone key |
| RE-02 REINS-VIPクラブ | `13-24` | `01:53-03:21` | `88.066667` | private database barrier |
| RE-03 保護理由 | `25-36` | `03:21-04:36` | `75.033333` | legitimate shields plus shadow |
| RE-04 囲い込み | `37-48` | `04:36-05:43` | `66.6` | double-agency blocking |
| RE-05 QR透明化 | `49-60` | `05:43-06:48` | `65.466667` | status transparency turn |
| RE-06 キュレーション | `61-82` | `06:48-08:52` | `123.6` | card sorting / defect disclosure |
| RE-07 AI後の人間価値 | `83-152` | `08:52-17:30` | `517.833333` | AI/SNS cards plus human stop-card payoff |

This table now uses the passed row-to-time map, not the earlier scene-bible percentage estimate.

## Blockers

- `ASSET_BLOCKED_REAL_ESTATE_CAST_TEMPLATES_MISSING`: consumer / gatekeeper / curator production templates are not available.
- `ASSET_BLOCKED_REAL_ESTATE_PROPS_MISSING`: VIP door, REINS PC, QR/status board, card-sorting, SNS/AI/risk cards are missing or placeholder-only.

Resolved by validator-visible subbeats:

- `SCRIPT_BLOCKED_RE07_TOO_BROAD_FOR_PRODUCTION_TIMING`: `RE-07A`-`RE-07E` are now embedded in the blueprint and recognized by `validate-background-skit-blueprint`.

## RE-07 Sub-Beat Split

| sub-beat | lines | actual start-end sec | purpose |
|---|---:|---:|---|
| RE-07A Z世代ライフスタイルとSNS信頼 | `83-102` | `531.7-653.716667` | SNS/推しスペース/アクセントウォールカードで条件軸の変化を見せる |
| RE-07B SNS集客のグレーゾーン | `103-113` | `653.716667-730.25` | SNSカードの裏に免許なし警告・おとり広告リスクを出す |
| RE-07C 2030年問題と攻めのDX | `114-129` | `730.25-864.116667` | 空き家/ハザード/相続カードとAIコンシェルジュを並べる |
| RE-07D AI逆説と見えないリスク | `130-143` | `864.116667-979.95` | AI推薦の前に専門家が境界紛争/相続/感情調整カードを差し出す |
| RE-07E 選び方の基準と最後の問い | `144-152` | `979.95-1049.533333` | 専門的キュレーター/リスク管理者/買ってはいけない理由カードを残して締める |

This split now uses the passed CSV / VoiceItem row-to-time map. The earlier scene-bible percentage estimate is superseded and retained only in JSON as historical estimate fields.

## Legacy Cue Disposition

| old cue | disposition | replacement |
|---|---|---|
| `index 1 enter_from_left` | transport only | RE-01 consumer search setup and smartphone/property-card emergence |
| `index 15 nod` | invalid as REINS explanation reaction | RE-02 VIP door/PC barrier and outside consumer composition |
| `index 35 surprise_jump` | invalid as darkness reaction | RE-03 shield cards with shadow/fee-bag overlay |
| `index 39 deny_shake` | invalid as double-agency explanation reaction | RE-04 gatekeeper blocks seller/buyer route and stamps deal-pending sign |
| `index 104 panic_shake` | still unresolved manual note | RE-07B SNS risk warning card/license badge |
| `index 143 exit_left` | not allowed as delivery actor exit for gatekeeper | RE-07D gatekeeper shadow recedes while curator stands next to consumer |

## Consequence

The old `samples/_probe/g24/real_estate_dx_skit_group_patched.ymmp` remains only transport/readback proof. It must not be promoted to creative acceptance.

The validator-authorized overlay-only compact review has been generated and read back. The next step is user-side integration review and stage/commit separation, not YMM4 creative acceptance.

Current authority chain:

1. RE-07 is split into source-backed subbeats inside the blueprint.
2. `validate-background-skit-blueprint` resolves `SCRIPT_BLOCKED_RE07_TOO_BROAD`.
3. `allowed_next_actions` contains `overlay_only_compact_review`.
4. `forbidden_next_actions` still blocks `cast_motion_ir`, `ymm4_creative_acceptance`, and `production_timing`.

The first safe scope was overlay/card-only compact review using the placeholder map, and it is now represented by `real_estate_dx_overlay_only_compact_review.html` plus the ShapeItem-only YMM4 carrier. Cast motion remains blocked until real-estate actor templates or accepted reskin proxies exist.
