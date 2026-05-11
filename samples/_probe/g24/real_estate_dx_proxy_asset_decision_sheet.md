# Real Estate DX Proxy / Asset Compact Decision Sheet

Scope: only rows from `real_estate_dx_proxy_asset_classification.json` where
`user_decision_needed != none`.

Boundary: this sheet is not G-27 v3 proof, not a scene decision packet, not an
asset-proxy gap report, not YMM4 conversion, not render, not production timing,
and not creative acceptance. It exists only to collect short prerequisite
decisions before those downstream artifacts can be made.

## Decision Rows

| beat id | meaning payload | current proxy visual | required production representation | current representation type | blocker / user decision needed | assistant default | user choices |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RE-02-beginning` | REINS sits behind normal consumer search and creates an access gap. | Smartphone search UI, dim broker DB room behind glass, lock emphasis. | Non-official public-search proxy facing a closed professional database proxy; must avoid looking like a real REINS screenshot. | `new abstract proxy` | Abstract REINS/search proxy is not approved yet. User must approve abstract proxy or require reference-accurate asset route. | **Approve abstract proxy.** Keep it generic and non-official; do not trigger rights review. | `abstract proxy`: approve current direction / `real asset`: require real UI-reference route / `rights review`: needed if real UI or REINS-like screenshot is requested / `defer`: hold RE-02 until source representation is decided |
| `RE-02-development` | Professional DB has more inventory than the public portal output. | Large broker DB terminal, small public portal card, property cards flowing outward. | Reusable broker DB panel plus reduced public-output card, without official branding/screenshots. | `new abstract proxy` | Needs a named reusable DB/public-output component. User must choose abstract DB/public proxy versus real/reference UI treatment. | **Approve abstract DB/public portal proxy.** It is enough for production planning and avoids official UI dependency. | `abstract proxy`: approve broker DB panel + public card / `real asset`: ask for real/reference UI treatment / `rights review`: required if real screen, logo, or service-like UI is used / `defer`: wait until REINS representation policy is settled |
| `RE-02-turn` | Information asymmetry: visible public information versus hidden raw data. | Public card versus hidden data bundle behind translucent wall. | Split information plane with public listing card, hidden data stack, and controllable occlusion wall. | `new abstract proxy` | Needs a reusable hidden-data / occlusion proxy instead of a one-off proof drawing. User must approve this metaphor. | **Approve abstract occlusion proxy.** This is low-risk and YMM4-friendly enough for the next classification stage. | `abstract proxy`: approve hidden-data wall / `YMM4 primitive`: implement later as cards + mask/wall + dimming, after gates / `real asset`: unnecessary unless a concrete document set is required / `defer`: hold if the wall metaphor feels too security-like |
| `RE-06-turn` | The value is editorial judgment and 納得感, not just a smaller list. | Lens narrows many candidates into one coherent property recommendation. | Real-estate-specific curation lens or editorial-frame proxy tied to property documents, not a generic strategy diagram. | `new abstract proxy` | Lens motif is readable but generic. User must approve it or request a concrete property-document proxy. | **Revise to property-document proxy, not pure lens.** Keep the curation idea, but anchor it in property sheets. | `abstract proxy`: approve lens with property-card texture / `new abstract proxy`: replace lens with editorial desk/property sheet comparison / `defer`: hold if curation value is still too abstract / `cut`: remove if this beat duplicates RE-06-development |
| `RE-07D-development` | AI match score misses invisible real-estate risks. | Boundary line, inheritance nodes, neighborhood markers behind property. | Approved risk-marker taxonomy for boundary, inheritance, neighborhood, and similar risks. | `new abstract proxy` | Risk markers are plausible, but reusable taxonomy is missing. User must approve abstract markers or require real document/map references. | **Approve abstract risk-marker taxonomy.** Use boundary / inheritance / neighborhood markers as symbolic production proxies. | `abstract proxy`: approve current risk marker set / `real asset`: require actual map/document references / `rights review`: required if real maps, registry docs, or identifiable documents are used / `defer`: hold until risk categories are narrowed |
| `RE-07D-turn` | Human specialist mediates between AI data and interpersonal risk. | Specialist silhouette connects AI panel to human relationship nodes. | Approved specialist/human-relationship representation, either abstract silhouettes or production character/template assets. | `blocked` | Specialist/cast representation is unresolved. User must choose abstract silhouettes, real specialist/cast asset, or cut/reframe. | **Defer by default.** Do not pass this beat downstream until the human/specialist representation policy is chosen. | `abstract proxy`: approve neutral silhouettes / `real asset`: require specialist/cast template or licensed person asset / `rights review`: required for real/person-like asset route / `defer`: keep blocked / `cut`: remove or reframe if human representation creates too much asset load |

## Short Return Format

User can answer with one compact list:

```text
RE-02-beginning: abstract proxy
RE-02-development: abstract proxy
RE-02-turn: abstract proxy
RE-06-turn: property-document proxy
RE-07D-development: abstract proxy
RE-07D-turn: defer
```

Those answers would only unlock the next planning artifact selection. They would
not by themselves authorize G-27 v3 proof, scene decision packet, asset-proxy
gap report, YMM4 conversion, render, production timing, or creative acceptance.
