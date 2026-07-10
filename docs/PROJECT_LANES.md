# Project Lanes

This compact lane map keeps review and maintenance loops from blocking product
progress. It is a navigation artifact, not a production gate or roadmap
expansion. Current state is mirrored in `docs/PROJECT_COCKPIT.md`.

| Lane | Purpose | Effect | Requirement | Current state | Owner | Next move |
|---|---|---|---|---|---|---|
| Output / Video Layer | Move toward an observed Episode 002 project and later video deliverables. | Keeps product proof independent from status/UI polish. | Five-point YMM4 import observation, then verified local input. | Observation package is ready; actual import/render has not happened. | Human operator for YMM4 signal, then NLMYTGen adapter. | Return the five observations; fix the adapter only if evidence requires it. |
| Input / API Hub | Receive verified source/transcript material without taking over upstream selection. | Enables replacement of the explicit sample fixture. | Source or transcript, provenance/rights note, stable identity, and cue alignment. | Required contract exists; candidate count is zero. | Upstream/source-intake lane, then NLMYTGen intake adapter. | Build a validated local receipt after material is supplied. |
| GUI / IA / i18n | Improve visible surfaces without restarting a long prototype chain. | Makes layout, language, color/type, and motion choices cheap to correct. | A new visible slice or explicit rejection of an accepted direction. | Prior Japanese console is a source record, not the current development slice. | NLMYTGen review UI lane. | Run a 2–3 direction low-fi check before the next high-fidelity build. |
| Integrity / Triage | Isolate full pytest drift, fixture drift, generated artifact policy, and heavy constraints. | Prevents validation cleanup from swallowing product slices. | Explicit integrity task or a failing narrow gate. | Full-suite drift is nonblocking for this slice. | Integrity/triage lane. | Use targeted checks only here. |
| Editing / YMM4 Feature Design | Observe import behavior and correct deterministic editing routes. | Separates actual GUI evidence from speculative adapter work. | Human performs the bounded import observation. | Five-point observation is ready; all five results remain unobserved. | Human observation + assistant readback/fix. | Use the observation sheet; do not broaden to render/publication. |
| Deep Research | Study app form, UI model, Docker capabilities, video trends, and production-process reverse engineering. | Feeds later product strategy without delaying current output. | Explicit research lane and bounded question. | Deferred. | Research lane. | Do not run deep external research in this slice. |

## Stop Rule

Maintenance work returns to the product lane after its focused checks pass. A
new visible product direction gets one low-cost comparison before high-fidelity
work; an accepted direction is not reopened by ordinary polish.
