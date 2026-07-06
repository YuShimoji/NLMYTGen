# Limitations

This package is a local/offline planning checkpoint. It is useful for review, GUI/dashboard consumption, and deciding whether a candidate deserves CSV/Writer IR work.

It does not perform or approve:

- YouTube upload/publication/visibility change
- OAuth/API keys/payment
- rights/legal/public-ready acceptance
- live scraping/media download
- YMM4 GUI launch/render
- cross-repo or destructive git
- final thumbnail image generation
- final YMM4 production candidate creation

Local progress should not be blocked by these public/production gates, but those gates remain mandatory before external release.

## Factory Seed Dry-Run Boundary

- source_seed_package_dir: production_pilots\yukkuri_newsroom_content_spine_001\factory_seed_dry_run_002
- This package uses synthetic dry-run seed input only.
- Required real inputs are still null in `source_seed_reference.json`.
- It does not run transcript substitution, IR bridge, YMM4 import/render, production `.ymmp`, external media, or publication.
