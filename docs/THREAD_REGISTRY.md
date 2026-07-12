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
| ymm4-import-ready-episode002 | OUTPUT_VIDEO_EDITING / YMM4_CSV_ADAPTER | accepted/csv-gate-passed | YMM4 4.53.0.9 imported the derived CSV without a mapping dialog: 9 VoiceItems, Reimu 3 / Marisa 6, linked text/order preserved, 2790 frames / 46.50 seconds. |
| ymm4-import-ready-ja-review-episode002 | GUI_IA_I18N | accepted/close-ready | Japanese-first import-ready review surface exists; no YMM4 import/render/.ymmp. |
| verified-real-input-prep-episode002 | INPUT_API_HUB / VERIFIED_REAL_INPUT_PREP | accepted/close-ready | Real-input replacement readiness pack exists; required local inputs defined; candidate input count is 0. |
| ymm4-observation-readback-episode002 | OUTPUT_VIDEO_EDITING / YMM4_DIAGNOSTIC_PROJECT | accepted/diagnostic-proof-observed | The separately authorized diagnostic project reopened in YMM4 with 9 VoiceItems and linked subtitles, 3 ImageItems, 3 independent TextItems, and readable S1/S2/S3 non-final labels; no render/export. |
| episode-002-verified-local-evidence-render-v1 | REAL_INPUT_INTERNAL_PILOT / HEADLESS_RENDER_FINALIZATION | accepted/internal-render-validated | Fixed audited subject `d8e959c`: ignored local project/render evidence remains hash-bound, machine-validated, internal/non-final, and unchanged. |
| episode-002-milestone-integration-audit-v1 | INTEGRATION_COORDINATOR / MILESTONE_AUDIT | accepted/integration-ready | All 44 commits and 448 paths were classified; merge-tree conflicts, secret/current-authority blockers, and local-media leaks are zero. Recommendation is `fast_forward_after_approval`; no default mutation occurred. |
| integrity-triage | INTEGRITY_TRIAGE | paused | Full-suite drift remains nonblocking for targeted slices. |
| control-boundary-correction | INTEGRITY_TRIAGE | completed/return-to-product | Repo-side supervisor control plane remains removed; the audited milestone is now at the explicit default-branch integration decision. |
| cross-device-restart-handoff | INTEGRITY_TRIAGE | completed/remote-seal | Resume on `codex/episode-002-milestone-integration-audit-v1`, state `episode-002-milestone-integration-audited-ready-v1`, and read the dated integration audit before any approved H1 mutation. |
