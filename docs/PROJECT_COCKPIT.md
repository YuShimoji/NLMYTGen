# Project Cockpit

This navigation sheet records the current local/offline episode 002 readiness
surface. It is not a production gate, a prompt, or a source of product rules.

## Current Route

| Checkpoint | State | Review path | Boundary |
|---|---|---|---|
| Episode 002 content spine | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/` | dry-run fixture, not real/source-reviewed content |
| Episode 002 IR/CSV bridge | draft_offline | `production_pilots/yukkuri_newsroom_content_spine_002/ir_bridge/` | Writer IR, cue packet, and CSV are draft candidates only |
| Episode 002 transcript readiness | sample_fixture_not_real | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/` | no real transcript; sample fixture is explicit |
| Episode 002 dashboard readiness ingest | ready | `production_pilots/yukkuri_newsroom_content_spine_002/dashboard_readiness_ingest/` | read-only status package; no YMM4 import/render or public gate crossed |
| Episode 002 GUI dashboard panel | ready | `production_pilots/yukkuri_newsroom_content_spine_002/gui_dashboard_panel/` | one-surface local HTML/JSON review; validation noise is nonblocking |
| Episode 002 YMM4 import preview pack | ready_context_synced | `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_import_preview_pack/` | local/offline import-prep inventory; not imported to YMM4; thumbnail proof is context only |
| Episode 002 thumbnail visual proof pack | ready_context | `production_pilots/yukkuri_newsroom_content_spine_002/thumbnail_visual_proof_pack/` | static/local SVG+HTML proof; contextual only for import preview; not production thumbnail approval |
| Episode 002 surface alignment pack | ready | `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_pack/` | local/offline cross-surface review story; no YMM4 or production gates crossed |
| Episode 002 surface alignment reviewer packet | source_record | `production_pilots/yukkuri_newsroom_content_spine_002/surface_alignment_review_packet/` | source record; label/next-action drift repaired at packet readback level; source surfaces unchanged |
| Episode 002 focused review brief | source_record | `production_pilots/yukkuri_newsroom_content_spine_002/focused_review_brief/focused_review_brief.html` | prior focused surface; preserved as secondary source record |
| Episode 002 compact review cockpit | weak_pass_prototype | `production_pilots/yukkuri_newsroom_content_spine_002/review_cockpit_compact/review_cockpit.html` | evaluated prototype; dark/bounded but not the final information architecture |
| Episode 002 review layout research | ready | `production_pilots/yukkuri_newsroom_content_spine_002/review_layout_research/layout_research_report.md` | pattern benchmark and wireframe packet; selects guided decision flow as the next UI target |
| Episode 002 guided decision flow prototype | ready | `production_pilots/yukkuri_newsroom_content_spine_002/guided_decision_flow_prototype/guided_decision_flow.html` | current local review entry; starts from user situation and recommends one current path |
| Episode 002 layout second-pass benchmark | ready | `production_pilots/yukkuri_newsroom_content_spine_002/review_layout_second_pass/split_view_benchmark.md` | split-view benchmark; treats guided flow as weak-pass and selects split-view decision rail plus evidence pane |
| Validation drift triage | nonblocking | `docs/verification/VALIDATION_DRIFT_VELOCITY_RECOVERY_V1_2026-07-06.md` | full-suite drift is classified; product work can continue |
| Real transcript replacement | blocked_by_real_input | `production_pilots/yukkuri_newsroom_content_spine_002/transcript_substitution_readiness/real_input/` | requires verified local transcript input |

## Symbolic Bars

- content_spine_002: `[#####--]` local draft package exists.
- ir_bridge_002: `[#####--]` draft IR/CSV bridge exists.
- transcript_substitution_002: `[####---]` sample fixture readiness exists, real transcript missing.
- dashboard_ingest_002: `[######-]` read-only ingest generated and validated.
- gui_dashboard_panel_002: `[######-]` static HTML/JSON panel generated and validated.
- yymm4_import_preview_pack_002: `[######-]` CSV/cue/Writer IR import-prep inventory generated and thumbnail context synced; YMM4 not launched/imported/rendered.
- thumbnail_visual_proof_002: `[######-]` 3 static SVG variants plus HTML/contact sheet generated and validated.
- surface_alignment_002: `[######-]` GUI/import/thumbnail surfaces aligned into one review story; stale next-action labels recorded.
- surface_reviewer_packet_002: `[#####--]` prior 8 drift rows classified as 5 resolved and 3 accepted_nonblocking; now a source record for the focused brief.
- focused_review_brief_002: `[#####--]` prior dark-mode decision-first surface preserved as a source record.
- review_cockpit_compact_002: `[#####--]` compact bounded dark review cockpit generated and validated, now classified as weak_pass_prototype for information architecture.
- review_layout_research_002: `[#####--]` layout benchmark packet generated; Candidate B guided decision flow selected as the next UI target.
- guided_decision_flow_002: `[######-]` guided local prototype generated and validated; current default recommendation is hold/review later because real input is absent and YMM4 observation is not selected.
- review_layout_second_pass_002: `[######-]` split-view benchmark generated and validated; next implementation target is decision rail plus evidence/preview pane.
- validation_drift_triage: `[#####--]` current drift classified as nonblocking for episode 002 product work.
- real_transcript_input: `[#------]` drop-zone exists, real input absent.

## Product Return Path

Completed/current slice: episode 002 layout second-pass split-view benchmark.
The current research checkpoint is
`review_layout_second_pass/split_view_benchmark.md`, with low-fidelity
wireframes at `review_layout_second_pass/candidate_wireframes_second_pass.html`
and machine readback at `review_layout_second_pass/validation_readback.json`.
The guided decision flow remains available at
`guided_decision_flow_prototype/guided_decision_flow.html`, but it is now an
evaluated weak-pass prototype rather than the final UI direction. The
second-pass benchmark compares split view, spine-detail, service entry,
wizard, current card/drawer guided flow, and command-center cockpit. It selects
exactly one next implementation target:
`candidate_a_split_view_decision_evidence_pane`. The next UI implementation
should use a decision rail plus evidence/preview pane so trust evidence stays
visible beside the active recommendation instead of being hidden in a generic
drawer. Real input replacement requires verified local material; actual YMM4
import observation requires an explicit human choice and still excludes
render/public claims. The validation drift is currently classified as older
newsroom generated-artifact noise, host/path drift, stale metadata, and fixture
snapshot drift rather than a blocker for this split-view research line.

## Regeneration

```bash
python -m src.cli.main build-dashboard-readiness-ingest --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_dashboard_readiness_ingest_v1
python -m src.cli.main build-gui-dashboard-panel --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id content_spine_002_gui_dashboard_panel_v1
python -m src.cli.main build-yymm4-import-preview-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_yymm4_import_preview_pack_v1
python -m src.cli.main build-thumbnail-visual-proof-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_thumbnail_visual_proof_v1
python -m src.cli.main build-surface-alignment-pack --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_surface_alignment_across_gui_import_thumbnail_v1
python -m src.cli.main build-surface-reviewer-packet --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_surface_alignment_repair_and_reviewer_packet_v1
python -m src.cli.main build-focused-review-brief --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_focused_review_brief_dark_surface_v1
python -m src.cli.main build-review-cockpit-compact --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_review_cockpit_compact_v1
python -m src.cli.main build-review-layout-research --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_review_layout_research_and_pattern_benchmark_v1
python -m src.cli.main build-guided-decision-flow-prototype --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_guided_decision_flow_prototype_v1
python -m src.cli.main build-review-layout-second-pass --package production_pilots/yukkuri_newsroom_content_spine_002 --artifact-id episode_002_layout_second_pass_split_view_benchmark_v1
```

Primary machine readback:

```text
production_pilots/yukkuri_newsroom_content_spine_002/review_layout_second_pass/validation_readback.json
```

Primary human review file:

```text
production_pilots/yukkuri_newsroom_content_spine_002/review_layout_second_pass/split_view_benchmark.md
```

## Closed Gates

- No YouTube upload, publication, scheduling, or visibility change.
- No OAuth, API keys, payment, or paid service use.
- No rights/legal/public-ready acceptance.
- No live scraping, RSS fetch, external image/media download, or embedded copyrighted media.
- No YMM4 GUI launch, import, render, production `.ymmp`, audio generation, or timing acceptance.
- Baseball hash residue is outside this surface-alignment slice.
