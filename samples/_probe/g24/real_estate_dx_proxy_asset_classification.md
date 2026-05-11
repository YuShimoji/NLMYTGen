# Real Estate DX Proxy / Asset Classification

Scope: G-27 RE-02 / RE-06 / RE-07D 9-frame visual treatment proof.

Source proof:

- `samples/_probe/g24/real_estate_dx_visual_treatment_proof.json`
- `samples/_probe/g24/real_estate_dx_visual_treatment_proof_readback.json`

Boundary: this is classification only. It is not G-27 v3 proof, scene decision
packet, asset-proxy gap report, YMM4 conversion, render, production timing, or
creative acceptance.

Schema: `docs/PROXY_ASSET_CLASSIFICATION_SCHEMA.md`

## Classification Table

| segment / beat | meaning payload | current proxy visual | required production representation | representation type | asset category | rights risk | YMM4 feasibility | blocker reason | user decision needed | next consumer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RE-02 / beginning | REINS exists behind ordinary consumer search, creating an access gap. | Smartphone search UI, dim broker DB room behind glass, lock emphasis. | Non-official public-search proxy facing a closed professional database proxy. | new abstract proxy | UI / background / motion | low | medium | Abstract REINS/public-search proxy vocabulary is not yet approved. | Approve abstract REINS/search proxy, or require reference-accurate asset route with rights review. | asset-proxy gap report |
| RE-02 / development | Professional database access contains more inventory than public output. | Large broker DB terminal, small public portal card, property cards flowing outward. | Reusable broker database panel plus reduced public-output card. | new abstract proxy | UI / property card / document / motion | low | medium | Production proxy needs a named reusable DB/public-output component. | Choose abstract DB/public portal proxy versus real/reference UI treatment. | asset-proxy gap report |
| RE-02 / turn | Visible public information is much smaller than hidden raw data. | Public card vs hidden data bundle behind translucent wall. | Split information plane with public listing card, hidden data stack, and occlusion wall. | new abstract proxy | UI / document / property card / motion | none | medium | Needs a reusable hidden-data / occlusion proxy. | Approve hidden-data wall metaphor as the production proxy. | asset-proxy gap report |
| RE-06 / beginning | Too many property choices overload the viewer. | Dense property cards around a small viewer silhouette. | Generic property-card overload proxy with controlled density. | existing proxy | property card / character / motion / background | none | easy | none | none | scene decision packet |
| RE-06 / development | Curation removes noise and keeps reason plus drawback visible. | Selected property sheet, drawback badge, dimmed noisy cards. | Selected property sheet with honest drawback marker. | existing proxy | property card / risk marker / document / motion | none | easy | none | none | scene decision packet |
| RE-06 / turn | The value is editorial judgment and納得感, not only a smaller list. | Lens narrows candidates into one recommendation. | Real-estate-specific curation lens or editorial-frame proxy tied to property documents. | new abstract proxy | property card / UI / character / motion | none | medium | Lens motif is readable but still generic. | Approve curation-lens proxy, or request a concrete property-document proxy. | asset-proxy gap report |
| RE-07D / beginning | AI presents an overconfident perfect-match recommendation. | AI recommendation panel, green confidence state, property card. | Abstract AI recommendation panel plus property card. | existing proxy | UI / property card / motion | none | easy | none | none | scene decision packet |
| RE-07D / development | Data-only recommendation misses invisible real-estate risks. | Boundary line, inheritance nodes, neighborhood markers behind property. | Approved risk-marker taxonomy for boundary, inheritance, neighborhood, and similar risks. | new abstract proxy | risk marker / map / document / property card / motion | low | medium | Needs reusable risk-marker taxonomy before adapter planning. | Approve abstract risk markers, or require real document/map references. | asset-proxy gap report |
| RE-07D / turn | A human specialist mediates between AI data and interpersonal risk. | Specialist silhouette connects AI panel to human relationship nodes. | Approved specialist/human-relationship representation. | blocked | character / UI / risk marker / motion | low | unknown | Depends on unresolved cast/proxy template decisions. | Decide abstract silhouettes vs real specialist/cast asset vs cut/reframe. | asset-proxy gap report |

## Rollup

Assistant can later advance without another proxy/asset decision:

- `RE-06-beginning`
- `RE-06-development`
- `RE-07D-beginning`

Needs user proxy/asset decision before downstream work:

- `RE-02-beginning`
- `RE-02-development`
- `RE-02-turn`
- `RE-06-turn`
- `RE-07D-development`
- `RE-07D-turn`

Blocked for downstream work:

- `RE-07D-turn`: specialist/human representation is not yet decided.

No rows are routed directly to `YMM4 adapter`. The current classifier only
prepares beat routing; it does not unlock YMM4 conversion.
