# Episode 002 local edit-slice execution

This local edit-slice execution pack turns the completed editing operations readiness package into a queue for the next local-only edit slice. It does not replace real input, launch YMM4, render, approve rights, approve final thumbnail output, or publish.

Primary review file: `production_pilots/yukkuri_newsroom_content_spine_002/local_edit_slice_execution_pack/local_edit_execution_preview.html`

## Queue

- 1. set_scene_duration: Creates a stable provisional timing pass for each scene.
- 2. align_voice_subtitle: Keeps cue order and voice/subtitle ownership explicit.
- 3. split_or_wrap_subtitle: Separates local wrap intent from final YMM4 linebreak acceptance.
- 4. assign_visual_scene_template: Connects each scene to an existing template slot.
- 5. place_citation_overlay: Allocates citation placeholders while real source wording stays gated.
- 6. transfer_thumbnail_motif: Reuses thumbnail motifs as local scene language without final approval.
- 7. validate_operation_pack: Checks all generated files and closed gate claims.

## Scene Plan

- S1: Opening hook and topic promise / 6 local steps
- S2: Main explanation: Factory seed dry-run placeholder for a second yukkuri newsroom episode / 6 local steps
- S3: Viewer watch point and production boundary / 6 local steps

## Closed Gate Readback

- actual_yymm4_import: False
- yymm4_rendered: False
- production_ymmp_written: False
- real_input_replacement_executed: False
- real_transcript_exists: False
- rights_accepted: False
- public_ready: False
- final_thumbnail_approval: False
- live_fetch_performed: False
- external_media_downloaded: False
- oauth_or_api_used: False
- youtube_uploaded: False
