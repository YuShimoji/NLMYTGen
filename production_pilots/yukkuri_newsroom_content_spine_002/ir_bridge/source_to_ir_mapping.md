# Source To IR Mapping

| Source field | Bridge / IR field | Status |
|---|---|---|
| topic_candidates.selected.candidate_id | episode_bridge.selected_candidate_id / writer_ir.video_id | mapped |
| source_boundary | episode_bridge.source_boundary / writer_ir.source_boundary | preserved |
| content_spine_dry_run_manifest.boundary_status | episode_bridge.boundary_status / bridge_manifest.boundary_status | preserved when present |
| source_seed_reference.seed_origin_fields | source_content_spine_reference.seed_origin_fields | preserved when present |
| source_seed_reference.inherited_template_defaults | source_content_spine_reference.inherited_template_defaults | separated when present |
| source_seed_reference.dry_run_placeholders | source_content_spine_reference.dry_run_placeholders | separated when present |
| source_seed_reference.required_real_inputs | source_content_spine_reference.required_real_inputs | separated and expected null before production |
| yukkuri_profile.explainer_role/listener_role | draft_dialogue.speaker / writer_ir.utterances.speaker | mapped |
| yukkuri_profile.hook | draft_dialogue row 2 / writer_ir utterance 2 | mapped |
| yukkuri_profile.beat_outline | draft_dialogue beat rows / writer_ir utterances | mapped as draft dialogue |
| thumbnail_profile.visual_motif | writer_ir.recurring_motif | mapped as planning cue |
| generated bridge outputs | source_content_spine_reference.generated_ir_csv_outputs / source_artifact_index.generated_outputs | indexed |
| final transcript timing | row_start/row_end | pending |
| YMM4 base project | apply-production input | pending |
