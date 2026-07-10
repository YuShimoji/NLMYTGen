# Thread Registry

Compact registry for parallel Episode 002 lanes. This is a routing snapshot,
not a governance document or roadmap.

| Thread | Lane | State | Current note |
|---|---|---|---|
| gui-i18n-episode002-console | GUI_IA_I18N | reported | Visual acceptance pending. |
| output-video-proof-episode002 | OUTPUT_VIDEO | accepted/close-ready | Output proof package exists. |
| output-template-episode002 | OUTPUT_VIDEO | accepted/close-ready | Output template readiness package exists. |
| input-intake-episode002 | INPUT_API_HUB | accepted/close-ready | Real input intake readiness package exists. |
| editing-ops-episode002 | EDITING_FEATURES | accepted/close-ready | Editing operations readiness package exists. |
| local-edit-slice-episode002 | EDITING_FEATURES_LOCAL_EXECUTION | accepted/close-ready | Local edit-slice execution queue exists. |
| ymm4-import-ready-episode002 | OUTPUT_VIDEO_EDITING / YMM4_CSV_ADAPTER | alias-ready/reobservation-pending | Explicit 4.53.0.9 character profile, derived 9-row CSV, strict coverage, and CSV-vs-diagnostic responsibility contract are validated. |
| ymm4-import-ready-ja-review-episode002 | GUI_IA_I18N | accepted/close-ready | Japanese-first import-ready review surface exists; no YMM4 import/render/.ymmp. |
| verified-real-input-prep-episode002 | INPUT_API_HUB / VERIFIED_REAL_INPUT_PREP | accepted/close-ready | Real-input replacement readiness pack exists; required local inputs defined; candidate input count is 0. |
| ymm4-observation-readback-episode002 | OUTPUT_VIDEO_EDITING / YMM4_CSV_ADAPTER | blocked/existing-unsaved-project-preserved | Derived CSV re-observation was not attempted because YMM4 restored an existing unsaved project. CSV gate remains pending; diagnostic `.ymmp` is separately `not_authorized / not_attempted`. |
| integrity-triage | INTEGRITY_TRIAGE | paused | Full-suite drift remains nonblocking for targeted slices. |
| control-boundary-correction | INTEGRITY_TRIAGE | completed/return-to-product | Repo-side supervisor control plane remains removed; product work has advanced through the YMM4 five-point observation. |
| cross-device-restart-handoff | INTEGRITY_TRIAGE | completed/remote-seal | Current restart context points to the actual-observation branch and the evidence-backed adapter-correction gate. |
