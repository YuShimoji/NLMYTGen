# Episode Factory Template Registry Usage

- artifact_id: episode_factory_template_registry_001
- selected_candidate_id: sports_pitch_sequence_p05
- seed_sample: `next_episode_seed_sample.json`
- deterministic_generation_path: true

## Regenerate

```bash
python -m src.cli.main build-episode-factory-template-registry --package production_pilots/yukkuri_newsroom_content_spine_001
```

## Use For Next Episode

1. Open `next_episode_seed_sample.json`.
2. Replace required inputs with a reviewed local topic/source packet and real transcript path.
3. Keep `sample_fixture_not_real`, `draft_offline`, `rights_boundary`, `public_upload_closed`, and `yymm4_render_closed` visible until real gates are satisfied.
4. Rerun downstream packages only after the relevant local inputs exist.

## Closed Gates

- YouTube upload/publication/visibility change
- OAuth/API keys/payment
- rights/legal/public-ready acceptance
- live scraping/media download
- external image/media download or embedded copyrighted media
- YMM4 GUI launch/import/render
- production .ymmp generation
- cross-repo or destructive git

## Next Safe Local Action

Review template_usage.md and next_episode_seed_sample.json; then provide a real local topic/source packet and transcript before any YMM4 import, render, rights, or public work.
