# Real Estate DX YMM4 Adapter Planning Candidate List

Source: `samples/_probe/g24/real_estate_dx_asset_proxy_gap_report.json`

This is a planning candidate list only. It does not create YMM4 adapter output,
YMM4 patch files, render output, production timing, or creative acceptance.

## Adapter-Planning-Ready Candidates

| beat | representation | proxy type | rights risk | required note |
| --- | --- | --- | --- | --- |
| `RE-02-beginning` | abstract proxy | public-search vs broker-database access-gap proxy | low | Use generic non-official search UI and broker-database abstraction. No real REINS screenshot, logo, or service-identifiable UI. |
| `RE-02-development` | abstract proxy | broker DB panel / public portal card / property-card flow | low | Plan generic broker DB and public portal panels with selected property-card flow. Avoid official branding and real/reference UI unless separately reviewed. |
| `RE-06-beginning` | abstract proxy | property-card overload | none | Plan simplified property cards, density control, and subtitle-safe lower band. No real listing photo or external asset is required. |
| `RE-06-development` | abstract proxy | selected property sheet plus drawback marker | none | Plan selected property sheet and drawback marker as abstract UI/document shapes. Do not introduce real listing screenshots. |
| `RE-06-turn` | property-document proxy | property sheet / editorial comparison / document-backed recommendation | none | Anchor curation value in property-document structure. Avoid pure lens, strategy diagram, or generic consulting visual treatment. |
| `RE-07D-beginning` | abstract proxy | AI recommendation panel plus property card | none | Use abstract AI panel and property card only. No real AI product UI, logos, model screenshots, or identifiable recommendation services. |
| `RE-07D-development` | abstract proxy | boundary / inheritance / neighborhood risk-marker set | low | Plan symbolic risk markers for boundary, inheritance, and neighborhood issues. Do not use real maps, registry documents, or identifiable records unless later rights-reviewed. |

## Excluded From Adapter Planning

| beat | status | representation | required note | reason |
| --- | --- | --- | --- | --- |
| `RE-02-turn` | adjustment required | abstract proxy | Replace wall / gate / locked-room / security-facility / conspiracy-coded occlusion language with transparent layer contrast. | Accepted meaning still needs representation adjustment before adapter planning. |
| `RE-07D-turn` | deferred item blocks adapter planning | defer | Do not include until user chooses abstract silhouettes, real/cast asset, cut/reframe, or keeps it deferred. | `asset_proxy_readiness=deferred` and `YMM4_adapter_readiness=still blocked`. This is distinct from the gap report's `blocked=0`; the item is deferred, and that defer state blocks adapter planning. |

## Planning Boundary

Proceed only to adapter planning for:

- `RE-02-beginning`
- `RE-02-development`
- `RE-06-beginning`
- `RE-06-development`
- `RE-06-turn`
- `RE-07D-beginning`
- `RE-07D-development`

Do not include:

- `RE-02-turn` until the opacity-layer adjustment is reflected.
- `RE-07D-turn` because the deferred item blocks adapter planning.

Forbidden actions:

- YMM4 adapter output
- YMM4 patch
- Render
- Production timing
- Creative acceptance
