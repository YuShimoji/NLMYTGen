# Project Lanes

This compact lane map keeps GUI review loops from blocking product progress.
It is a navigation artifact, not a production gate or roadmap expansion.

| Lane | Purpose | Effect | Requirement | Current state | Owner | Next move |
|---|---|---|---|---|---|---|
| Output / Video Layer | Move fastest toward video deliverables and production-surface proof. | Keeps rendering, preview, and package proof work independent from GUI polish. | Verified local input or an explicit output-layer slice. | Blocked by real input for Episode 002. | NLMYTGen downstream adapter. | Return here after the Japanese graphical console is reviewable. |
| Input / API Hub | Handle RSS, API hub, external resource connection, and source/transcript intake. | Supplies verified material without forcing UI work to solve ingest. | Clear upstream source packet or local transcript/source files. | Real input is absent; sample fixture remains explicit. | Upstream/source-intake lane, then NLMYTGen intake adapter. | Prepare verified local source/transcript material. |
| GUI / IA / i18n | Bound Japanese display, layout, and review-surface work. | Improves reviewability without holding output indefinitely. | Human rejection or a scoped UI review target. | Current slice is Japanese graphical review console. | NLMYTGen review UI lane. | Stop after this console is reviewable unless the user rejects the direction. |
| Integrity / Triage | Isolate full pytest drift, fixture drift, generated artifact policy, and heavy constraints. | Prevents validation cleanup from swallowing product slices. | Explicit integrity task or a failing narrow gate. | Full-suite drift is nonblocking for this slice. | Integrity/triage lane. | Use targeted checks only here. |
| Editing / YMM4 Feature Design | Explore edit operations, timing, import observation, and YMM4-related feature design. | Keeps YMM4 GUI/import/render gates explicit and separate. | Human selects YMM4 observation or an editing-design task. | YMM4 GUI/import/render are closed. | Editing/YMM4 design lane. | Do not launch/import/render in the review-console slice. |
| Deep Research | Study app form, UI model, Docker capabilities, video trends, and production-process reverse engineering. | Feeds later product strategy without delaying current output. | Explicit research lane and bounded question. | Deferred. | Research lane. | Do not run deep external research in this slice. |

## Stop Rule

After the Japanese graphical console is reviewable, return to the product lane
unless the user rejects the UI direction.
