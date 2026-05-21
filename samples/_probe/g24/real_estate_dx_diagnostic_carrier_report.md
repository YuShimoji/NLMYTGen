# Real Estate DX Diagnostic Carrier (SCS §2.1 split)

Diagnostic carrier: `samples/_probe/g24/real_estate_dx_diagnostic_carrier.ymmp`

Diagnostic only. Not a production carrier. Render / creative acceptance / timing adjustment were not performed.

## 1. Composition

- composition_type: `split`
- beat -> composition mapping: `split` from `A is not B (公開ポータル vs 業者DB の情報非対称性)`
- scs spec ref: `docs/SCENE_COMPOSITION_SCHEMA.md (v0.1)`
- carrier checklist ref: `docs/G27_PUBLIC_VS_BROKER_DB_CARRIER_CHECKLIST.md`

## 2. Visual Roles (SCS §3)

- `focal_anchor`: 2 item(s) — `G27PBD_PublicPanel`, `G27PBD_BrokerPanel`
- `supporting`: 5 item(s) — `G27PBD_PublicCard1`, `G27PBD_PublicCard2`, `G27PBD_BrokerCard1`, `G27PBD_BrokerCard2`, `G27PBD_BrokerCard3`
- `boundary`: 2 item(s) — `G27PBD_Lock`, `G27PBD_Lock_Right`
- `connector`: 1 item(s) — `G27PBD_Arrow`
- `risk_marker`: 0 item(s) — (none)
- `decoration`: 1 item(s) — `G27PBD_BG`
- `label`: 3 item(s) — `G27PBD_Title`, `G27PBD_PublicTitle`, `G27PBD_BrokerTitle`

## 3. SCS Compliance Rollup

- element_count: `14` (`pass`)
- reading_order: `G27PBD_PublicPanel` -> `G27PBD_Lock` -> `G27PBD_BrokerPanel`
- shape_size_mode_check: `pass`
- color_format_check: `pass`
- safe_area_check: `pass`
- subtitle_clearance_check: `pass`
- typography_hierarchy_check: `pass`
- in_frame_text_budget_check: `pass` (labels=3, chars=17)

## 4. Composition Violations

- `SCS_3_supporting_per_frame_strict` (`spec_ambiguity`): split composition with 2 focal anchors needs per-focal supporting count limit. SCS v0.1 ambiguity recorded for v0.2 refinement.
- `SCS_4_3_label_budget_strict` (`spec_ambiguity`): split composition needs global title + per-panel title (3 labels). SCS v0.1 ambiguity recorded for v0.2 refinement.

## 5. Item Table

| item_name | role | type | layer | hidden | x,y | width x height (or font) | color |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `G27PBD_BG` | `decoration` | `ShapeItem` | `5` | `false` | `0, 0` | `1920x1080` | `#FFF0F4F8` |
| `G27PBD_Title` | `label` | `TextItem` | `9` | `false` | `0, -443` | `font=64` | `#FF1A2B3C` |
| `G27PBD_PublicPanel` | `focal_anchor` | `ShapeItem` | `8` | `false` | `-499, -49` | `730x620` | `#FF2563EB` |
| `G27PBD_PublicTitle` | `label` | `TextItem` | `10` | `false` | `-499, -310` | `font=48` | `#FFFFFFFF` |
| `G27PBD_PublicCard1` | `supporting` | `ShapeItem` | `11` | `false` | `-499, -150` | `600x130` | `#FFE0EBFE` |
| `G27PBD_PublicCard2` | `supporting` | `ShapeItem` | `11` | `false` | `-499, 30` | `600x130` | `#FFE0EBFE` |
| `G27PBD_Lock` | `boundary` | `ShapeItem` | `12` | `false` | `-20, -49` | `30x400` | `#FFE5A800` |
| `G27PBD_Lock_Right` | `boundary` | `ShapeItem` | `12` | `false` | `20, -49` | `30x400` | `#FFE5A800` |
| `G27PBD_BrokerPanel` | `focal_anchor` | `ShapeItem` | `8` | `false` | `499, -49` | `730x620` | `#FF7C3AED` |
| `G27PBD_BrokerTitle` | `label` | `TextItem` | `10` | `false` | `499, -310` | `font=48` | `#FFFFFFFF` |
| `G27PBD_BrokerCard1` | `supporting` | `ShapeItem` | `11` | `false` | `499, -190` | `600x110` | `#FFEDE9FE` |
| `G27PBD_BrokerCard2` | `supporting` | `ShapeItem` | `11` | `false` | `499, -49` | `600x110` | `#FFEDE9FE` |
| `G27PBD_BrokerCard3` | `supporting` | `ShapeItem` | `11` | `false` | `499, 92` | `600x110` | `#FFEDE9FE` |
| `G27PBD_Arrow` | `connector` | `ShapeItem` | `13` | `true` | `0, 200` | `120x60` | `#FFE5A800` |

## 6. Status

- readback status: `passed`
- carrier modified in place: `false`
- composition hard failures: `0`
- composition violation count (all severities): `2`

## 7. Boundary

- `diagnostic_only`: `true`
- `not_video_scene`: `true`
- `existing_micro_scene_probe_modified`: `false`
- `existing_primitive_visibility_probe_modified`: `false`
- `shape_item_text_item_only`: `true`
- `tonal_system`: `"light-stage"`
- `black_white_background_mix`: `false`
- `external_assets_used`: `false`
- `tts_performed`: `false`
- `url_fetch_performed`: `false`
- `publishing_performed`: `false`
- `render_performed`: `false`
- `timing_adjusted`: `false`
- `creative_acceptance_performed`: `false`
- `production_readiness_claimed`: `false`
- `production_carrier_replaced`: `false`
- `next_user_action`: `"user-authored carrier .ymmp is still required for production slot-fill"`
