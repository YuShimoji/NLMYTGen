# Turn-Based Development Plan

This file describes planning bands by turn count, not by date. A "turn" means
one bounded work session or handoff cycle that should produce a reviewable
state, a verified artifact, or a clear stop condition.

This plan is a routing aid. It does not replace [runtime-state.md](runtime-state.md),
[FEATURE_REGISTRY.md](FEATURE_REGISTRY.md), or lane-specific handoff files.

## Turn Bands

| Turn band | Main decision to close | Typical output | Done signal | Avoid |
| --- | --- | --- | --- | --- |
| Turn 1 | Pick the active bottleneck from current docs. | Updated reader map, narrowed next lane, or verified current artifact list. | The next turn can start from one file and one artifact family. | Reading every historical verification file before acting. |
| Turns 2-3 | Close the next visual/review surface. | Screenshot index update, manual review result, frame inspection note, or chat-first review digest. | A human or machine-readable `accept`, `PASS`, `FIX`, `hold`, or blocker classification exists. | Creating more artifacts when the current review surface lacks a decision. |
| Turns 4-6 | Convert an accepted review surface into implementation or transport proof. | Contract/readback/manifest update, focused test, or YMM4-safe placement artifact. | Tests/readbacks pass and boundaries are still explicit. | Claiming render, production, rights, or creative acceptance from transport proof. |
| Turns 7-10 | Harden the route and package evidence. | Repeatable run command, artifact manifest, proof index, and updated owner docs. | Another agent can resume without asking where the proof lives. | Turning docs-only planning into a substitute for smoke/readback evidence. |
| Turns 11+ | Promote only after gates are closed. | Production candidate, source replacement plan, publishing prep, or integration handoff. | Source/provenance, review, and acceptance gates are named and passed. | Advancing to publishing, real source ingest, or broad automation from sample-only proof. |

## Current Lane Choices

| Lane | Use it when | Next turn should produce | Current friction reduced |
| --- | --- | --- | --- |
| Baseball sidequest | The goal is to see the Baseball infographic route advance. | BN-05 YMM4 preview screenshot plus `PASS`/`FIX`, or BN-04 frame inspection result. | Removes uncertainty about crop, readability, and whether frame export is worth turning into clip export. |
| G-28 reference-driven screen carrier | The goal is mainline visual carrier design. | Chat-first digest or review decision for the reference layout prototype pack. | Stops repeating low-value coordinate-generated YMM4 probes and keeps design review visible. |
| Common foundation repo-status observer | The goal is automation safety, not visuals. | Stdout-only producer implementation or hold decision, with no runtime artifacts. | Replaces bare human clean-status claims with observed input while preserving real-runner boundaries. |
| Packaging / quality support | The goal is episode packaging and diagnostic scoring. | Focused H-row extension or proof packet tied to an existing artifact. | Keeps title/thumbnail/evidence checks separate from unapproved media generation. |

## Baseball Default Next Turns

| Turn | Concrete target | Expected result |
| --- | --- | --- |
| Turn 1 | Use [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md), [PROGRESS_SCREENSHOT_INDEX.md](PROGRESS_SCREENSHOT_INDEX.md), and the Baseball backlog to confirm the route. | The project is navigable without opening every historical proof file. |
| Turn 2 | Perform BN-05 manual YMM4 preview, or inspect BN-04 frames if YMM4 is unavailable. | A screenshot plus `PASS`/`FIX`, or a frame inspection decision. |
| Turn 3 | If BN-05 is `FIX`, adjust the placement contract once; if `PASS`, mark the placement route accepted for the next transport step. | One decision-backed placement state. |
| Turns 4-5 | Only after acceptable preview/frame review, decide whether BN-04 needs clip export. | Codec/timing proof or an explicit "frame sequence is enough for now" decision. |
| Turn 6+ | Start real episode/source replacement audit only if sample route and visual review are accepted. | Source/provenance plan before real ingest, not after. |

## Update Rule

Update this file when turn bands, lane choices, or done signals change. Do not
use it as a chronological log. Date-stamped details belong in handoff or
verification files; current working position belongs in `runtime-state.md`.
