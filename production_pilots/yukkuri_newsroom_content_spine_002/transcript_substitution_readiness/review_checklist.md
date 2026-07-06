# Transcript Substitution Readiness Review Checklist

- selected_candidate_id: factory_seed_dry_run_002
- source_mode: sample_fixture_generated
- transcript_status: sample_fixture_not_real
- sample_fixture_used: True

## Required Checks

- Confirm `source_context_reference.json` separates seed origin, inherited defaults, dry-run placeholders, required real inputs, generated IR/CSV outputs, transcript placeholders, and generated transcript outputs.
- Confirm `required_real_inputs` are still null before any real transcript, YMM4 import, rights, render, or publication work.
- Confirm `transcript_source_probe.json` reports `sample_fixture_not_real` when no verified local transcript is supplied.
- Confirm `regenerated_draft_yymm4.csv` is a headerless two-column preview generated from the transcript-shaped input.
- Confirm `regenerated_episode_bridge.json`, `regenerated_writer_ir_candidate.json`, and `cue_packet_readiness.json` keep public, YMM4, audio, and production gates closed.

## Closed Gates

- no real transcript acceptance
- no YMM4 GUI/import/render
- no production `.ymmp` generation
- no external media/live fetch/OAuth/payment
- no rights/legal/public-ready acceptance
- no public upload

## Source Context

- source_seed_reference_present: True
- ir_bridge_reference_present: True
