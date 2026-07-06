# IR Bridge Review Checklist

- selected_candidate_id: factory_seed_dry_run_002
- source_seed_reference_present: True
- status: dry-run/local review package only

## Required Checks

- Confirm `source_content_spine_reference.json` separates seed origin, inherited defaults, dry-run placeholders, required real inputs, and generated IR/CSV outputs.
- Confirm `required_real_inputs` are still null before any real transcript, YMM4 import, rights, render, or publication work.
- Confirm `draft_yymm4.csv` is a headerless two-column draft preview only.
- Confirm `episode_bridge.json`, `writer_ir_candidate.json`, and `cue_packet_candidate.json` all preserve the source boundary.
- Confirm `source_artifact_index.json` lists source content-spine inputs and generated bridge outputs.

## Closed Gates

- no real transcript
- no YMM4 GUI/import/render
- no production `.ymmp` generation
- no external media/live fetch/OAuth/payment
- no rights/legal/public-ready acceptance
- no public upload
