# Real Estate DX YMM4 Compact Patch Review

Source: `samples/_probe/g24/real_estate_dx_adapter_ir_dry_run.json`

This is a compact review of intended YMM4 patch items. It does not write or modify a `.ymmp` file and does not render.

## Rollup

- Candidates reviewed: `7`
- Ready for actual `.ymmp` patch output: `7`
- Minimal patched `.ymmp` can be produced next: `true`
- Candidate blocked/deferred: `0` / `0`
- Excluded blocked/deferred: `1` / `1`

## Review Table

| candidate | item type | layer | start frame | duration | primitive | placeholder | visible effect | patch readiness | blocked reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RE-02-beginning` | ShapeItem + TextItem | 7, 8, 9 | `0` | `360`f / `6`s | abstract_ui_public_search_vs_broker_db | generic_public_search_panel + broker_db_shadow_panel | A public search panel dims while a generic broker DB panel appears behind it; no official REINS UI is shown. | `ready` | none |
| `RE-02-development` | ShapeItem + TextItem | 7, 8, 9 | `390` | `360`f / `6`s | abstract_ui_broker_db_public_portal_property_flow | broker_db_panel + public_portal_card + property_card_flow | Many generic property cards flow from the broker DB panel into a smaller public portal card. | `ready` | none |
| `RE-06-beginning` | ShapeItem + TextItem | 7, 8, 9 | `780` | `360`f / `6`s | property_card_overload_cluster | property_card_overload_cluster | A dense cluster of simple property cards crowds the upper frame while the subtitle band stays clear. | `ready` | none |
| `RE-06-development` | ShapeItem + TextItem | 7, 8, 9 | `1170` | `360`f / `6`s | selected_property_sheet_with_drawback_marker | selected_property_sheet + drawback_marker | Noisy cards fade back while one selected property sheet and a drawback marker remain visible. | `ready` | none |
| `RE-06-turn` | ShapeItem + TextItem | 7, 8, 9 | `1560` | `360`f / `6`s | property_document_editorial_comparison | property_document_editorial_comparison | A property-document comparison frame makes the recommendation feel editorial, not just a generic lens. | `ready` | none |
| `RE-07D-beginning` | ShapeItem + TextItem | 7, 8, 9 | `1950` | `360`f / `6`s | abstract_ai_recommendation_panel_property_card | abstract_ai_recommendation_panel + property_card | An abstract AI recommendation panel highlights a property card as a confident match without product branding. | `ready` | none |
| `RE-07D-development` | ShapeItem + TextItem | 7, 8, 9 | `2340` | `360`f / `6`s | abstract_real_estate_risk_marker_set | boundary_inheritance_neighborhood_risk_markers | Boundary, inheritance, and neighborhood risk markers appear behind the matched property card. | `ready` | none |

## Excluded Items

| candidate | readiness | blocking reason |
| --- | --- | --- |
| `RE-02-turn` | `blocked` | Accepted-with-adjustment proxy is not in the 7 adapter IR dry-run candidates; the opacity-layer adjustment must be reflected before compact patch review. |
| `RE-07D-turn` | `deferred` | Specialist / cast / silhouette representation policy remains undecided; no compact patch review item is planned for this beat. |
