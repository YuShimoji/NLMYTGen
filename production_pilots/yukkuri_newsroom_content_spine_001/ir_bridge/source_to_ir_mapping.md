# Source To IR Mapping

| Source field | Bridge / IR field | Status |
|---|---|---|
| topic_candidates.selected.candidate_id | episode_bridge.selected_candidate_id / writer_ir.video_id | mapped |
| source_boundary | episode_bridge.source_boundary / writer_ir.source_boundary | preserved |
| yukkuri_profile.explainer_role/listener_role | draft_dialogue.speaker / writer_ir.utterances.speaker | mapped |
| yukkuri_profile.hook | draft_dialogue row 2 / writer_ir utterance 2 | mapped |
| yukkuri_profile.beat_outline | draft_dialogue beat rows / writer_ir utterances | mapped as draft dialogue |
| thumbnail_profile.visual_motif | writer_ir.recurring_motif | mapped as planning cue |
| final transcript timing | row_start/row_end | pending |
| YMM4 base project | apply-production input | pending |
