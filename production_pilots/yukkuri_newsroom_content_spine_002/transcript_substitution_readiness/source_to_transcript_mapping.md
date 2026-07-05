# Source To Transcript Mapping

| Source / transcript item | Regenerated field | Status |
|---|---|---|
| content spine selected_candidate_id | regenerated_episode_bridge.selected_candidate_id / regenerated_writer_ir_candidate.video_id | preserved |
| content spine source_boundary | regenerated_episode_bridge.source_boundary / regenerated_writer_ir_candidate.source_boundary | preserved |
| source_seed_reference seed-origin fields | source_context_reference.seed_origin_fields | preserved when present |
| source_seed_reference inherited defaults | source_context_reference.inherited_template_defaults | separated when present |
| source_seed_reference dry-run placeholders | source_context_reference.dry_run_placeholders | separated when present |
| source_seed_reference required real inputs | source_context_reference.required_real_inputs | separated and expected null before production |
| ir_bridge generated outputs | source_context_reference.generated_ir_csv_outputs | preserved when present |
| transcript_source_probe.selected_transcript_path | regenerated_episode_bridge.transcript_substitution.selected_transcript_path | mapped |
| transcript fixture/drop-zone | source_context_reference.transcript_placeholders | separated |
| normalized transcript rows | regenerated_episode_bridge.draft_dialogue / regenerated_writer_ir_candidate.utterances / regenerated_draft_yymm4.csv | mapped |
| transcript boundary fields | regenerated_episode_bridge.transcript_substitution.transcript_boundary | preserved |
| audio timing | row_start/row_end and YMM4 VoiceItem timing | pending |
| YMM4 base project | validate-ir/apply-production inputs | pending |

## Current Input Reality

- source_mode: `sample_fixture_generated`
- transcript_status: `sample_fixture_not_real`
- sample_fixture_used: `True`
- selected_candidate_id: `factory_seed_dry_run_002`
