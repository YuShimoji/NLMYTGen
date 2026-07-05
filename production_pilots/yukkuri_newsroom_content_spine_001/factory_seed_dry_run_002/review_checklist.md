# Factory Seed Instantiation Dry-Run Review Checklist

- Confirm `seed_instantiation_manifest.json` points to the existing template registry.
- Confirm `episode_seed.json` separates inherited defaults, synthetic dry-run placeholders, and required real inputs.
- Confirm `dry_run_topic_source_packet.json` is marked `dry_run` and `sample_fixture_not_real`.
- Confirm `required_real_inputs.json` has null values for real topic/source, transcript, rights, and human decision fields.
- Confirm `content_spine_input_candidate.json` is a candidate only and was not run downstream.
- Confirm rights, public upload, YMM4 render, production `.ymmp`, OAuth/payment/API, external media, and publication gates remain closed.

## Next Safe Local Action

Review episode_seed.json and required_real_inputs.json; replace the dry-run source packet with a real reviewed local topic/source packet before any downstream content-spine, transcript, YMM4, rights, render, production, or public work.
