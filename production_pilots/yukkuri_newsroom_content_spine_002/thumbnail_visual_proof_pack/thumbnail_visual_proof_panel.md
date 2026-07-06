# Thumbnail Visual Proof Pack

- artifact_id: episode_002_thumbnail_visual_proof_v1
- episode: factory_seed_dry_run_002
- variants: 3
- recommended variant: `headline_driven` because it has the clearest small-size hierarchy and makes the dry-run boundary visible.
- reviewer should judge: title hierarchy, thumbnail legibility, and which visual direction deserves later hook refinement.
- forbidden/deferred: no external media, no production thumbnail approval, no public upload, no YMM4 import/render.
- source_index: `source_index.json`

## At A Glance

| label | value |
|---|---|
| Proof only | true |
| No external media | true |
| Not production thumbnail | true |
| CSV context | 9 rows / headerless |
| validation_noise | validation_noise_nonblocking |

## Variants

| variant_id | headline | visual structure | proof output | recommendation | note |
|---|---|---|---|---|---|
| headline_driven | DRY RUN FACTORY CHECK | Large left headline with a compact right-side proof stack and closed-gate labels. | `variants/headline_driven.svg` | recommended | High legibility, but less character warmth. |
| speaker_contrast | SECOND SEED? | Two abstract speaker badges face a central proof label; no character art or external media. | `variants/speaker_contrast.svg` | alternate | More playful, but the abstract badges need reviewer judgment. |
| newsroom_diagram | TEMPLATE -> CSV -> PROOF | Diagram-like pipeline cards with a highlighted proof endpoint and closed gates. | `variants/newsroom_diagram.svg` | alternate | Most informative, but busier than the recommended headline variant. |

## Contact Sheet

- HTML panel: `thumbnail_visual_proof.html`
- SVG contact sheet: `thumbnail_contact_sheet.svg`

## Next Safe Local Action

Review thumbnail_visual_proof.html and select one direction for later title hook refinement; do not treat any variant as production thumbnail approval.
