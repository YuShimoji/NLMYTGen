# REINS information-flow factory canary

This package is the second real-topic technical canary for the standard
production loop. It reduces the existing real-estate DX material to seven
source-backed cues about REINS registration, search, and seller-side status
confirmation.

The raw script and G-27 review packet are discovery and transformation inputs.
They are not factual authority. Spoken claims are limited to the four official
surfaces in `source_claim_registry.json`.

Content boundary: `internal_factory_canary_not_human_accepted`. The package and
its local render are not creative acceptance, rights approval, production
approval, publication approval, or upload authority.

## Local paths

- episode manifest:
  `auto_video_pipeline/real_estate_reins_episode_manifest.json`
- ignored source media:
  `auto_video_runs/source_media_real_estate_reins_v1/`
- ignored source project:
  `auto_video_runs/source_projects/real_estate_reins_source.local.ymmp`
- ignored run:
  `auto_video_runs/real_estate_reins_internal_review_v1/`
- machine-readable technical receipt:
  `technical_validation_receipt.json`

The source project is generated automatically from
`derived_yymm4_import.csv`: a blank clone of the inspected G-27 project
structure is opened by the project-owned Windows UI Automation driver, YMM4
performs its own speaker selection, row addition, and voice generation. The
driver uses UI Automation patterns only; it does not inject keyboard or mouse
input. The original G-27 project remains byte-unchanged.

## Operator path

```powershell
uv run python -m src.cli.main build-episode-video `
  --episode production_pilots/factory_canaries/real_estate_reins_transparency_001/auto_video_pipeline/real_estate_reins_episode_manifest.json `
  --dry-run
```

Final generation is started from the Electron 43 `自動動画生成` surface after
deep runtime doctor and the write-free dry-run pass. Audio and preview playback
remain disabled.
