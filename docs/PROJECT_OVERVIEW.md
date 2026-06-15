# Project Overview

This page is a reader-facing orientation map. It does not replace, translate,
summarize away, or weaken the canonical Markdown files. Use it to decide where
to look next, then read the linked owner document for the actual wording.

## Fast Answers

| Question | Best starting point | What it gives | Remaining caution |
| --- | --- | --- | --- |
| Where can past feature implementation be seen? | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) | Itemized feature IDs, status, layer, and notes for A/B/C/D/E/F/G/H areas. | It is a registry, not a quick narrative; dense rows may need follow-up in verification docs. |
| Where can future features and progress be seen? | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md), [runtime-state.md](runtime-state.md), [TURN_BASED_DEVELOPMENT_PLAN.md](TURN_BASED_DEVELOPMENT_PLAN.md) | Registry status (`approved`, `proposed`, `hold`, `rejected`), current slice, and turn-count planning lanes. | `runtime-state.md` is current-position authority, but it is intentionally history-heavy. |
| Are implementation items grouped by topic? | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) and the implementation map below | A-H feature groups plus Baseball sidequest BN slices and common foundation work. | Some verification docs are evidence records, not feature owners. |
| Where are progress screenshots or visual proof images? | [PROGRESS_SCREENSHOT_INDEX.md](PROGRESS_SCREENSHOT_INDEX.md) | Existing proof images, preview screenshots, frame exports, and their source paths. | The BN-05 YMM4 manual preview screenshot is still missing until a human captures it in YMM4. |
| Is future planning split by turn count instead of date? | [TURN_BASED_DEVELOPMENT_PLAN.md](TURN_BASED_DEVELOPMENT_PLAN.md) | Turn bands, lane choices, done signals, and default Baseball next turns. | It is a planning route, not a replacement for `runtime-state.md` or human decisions. |

## Implementation Map

| Area | What is already visible | Future or held work | Where to inspect |
| --- | --- | --- | --- |
| Source intake and upstream material | NotebookLM / text intake and RSS-related work are tracked under A rows. | NotebookLM API and external posting remain held or outside current scope. | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md), [RSS_READER_SYNC_SPEC.md](RSS_READER_SYNC_SPEC.md), verification RSS docs. |
| Script conversion and diagnostics | B-01 through B-18 cover CSV conversion, speaker mapping, line wrapping, reflow, cue packets, diagram briefs, and script diagnostics. | Residual improvements should extend existing B rows or start as proposed registry rows. | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md), [SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md](SCRIPT_QUALITY_DIAGNOSTICS_SPEC.md), B verification docs. |
| YMM4/manual support and prompt surface | C-07 through C-09 are done prompt/helper surfaces; several direct Python/YMM4 generation ideas are rejected or info-only boundaries. | Native YMM4 actions remain human/YMM4-side unless a bounded successor lane is approved. | [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md), [WORKFLOW.md](WORKFLOW.md), [INVARIANTS.md](INVARIANTS.md). |
| GUI and operator surface | F-04 CSV stats display is done; older F-01/F-02 GUI directions are quarantined; F-03 Python preview route is rejected. | GUI revival must be tied to a narrow workflow proof, not broad UI expansion. | [GUI_MINIMUM_PATH.md](GUI_MINIMUM_PATH.md), [AGENT_OPERATOR_SURFACE.md](AGENT_OPERATOR_SURFACE.md), F rows in [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md). |
| Visual/YMM4 automation | G-24 template-first skit group route is done; G-25 property variation probe is done; G-27 is held as case evidence; G-28 is the current reference-driven successor direction. | G-28 needs review surfaces and transfer decisions before production claims. | [REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md](REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md), [TASK_DEVELOPMENT_CYCLE_SPEC.md](TASK_DEVELOPMENT_CYCLE_SPEC.md), G verification docs. |
| Packaging, thumbnail, and quality scoring | H-01 packaging brief is approved; H-02 through H-05 cover thumbnail strategy and scoring support. | Generated thumbnail/media production is still bounded; scoring is diagnostic, not creative acceptance. | [PACKAGING_ORCHESTRATOR_SPEC.md](PACKAGING_ORCHESTRATOR_SPEC.md), [THUMBNAIL_STRATEGY_SPEC.md](THUMBNAIL_STRATEGY_SPEC.md), H verification docs. |
| Baseball sidequest | BN-01 through BN-05 describe the baseball infographic route, visual data contract, static PNG export, frame sequence export, and YMM4 placement proof. | BN-05 manual YMM4 preview screenshot and PASS/FIX note remain the clearest next human proof. | [BASEBALL_NEWS_PIPELINE_SPEC.md](BASEBALL_NEWS_PIPELINE_SPEC.md), [baseball_infographic_backlog.md](../lanes/sports_news/docs/baseball_infographic_backlog.md), [baseball_sidequest_restart_handoff_2026-05-26.md](../lanes/sports_news/docs/baseball_sidequest_restart_handoff_2026-05-26.md). |
| Common foundation / agent orchestration | Recent docs define repo-status input audits, live status JSON producer design, and preflight boundaries. | These are observer/design contracts unless separately authorized for stdout-only implementation. | [runtime-state.md](runtime-state.md), [AGENT_ORCHESTRATION.md](AGENT_ORCHESTRATION.md), common-foundation verification docs. |

## How to Read the Local Docs View

1. Start here for orientation.
2. Open [PROGRESS_SCREENSHOT_INDEX.md](PROGRESS_SCREENSHOT_INDEX.md) when the
   question is visual progress or screenshot placement.
3. Open [TURN_BASED_DEVELOPMENT_PLAN.md](TURN_BASED_DEVELOPMENT_PLAN.md) when
   the question is "what should the next few turns close?"
4. Open [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) for itemized status.
5. Open [runtime-state.md](runtime-state.md) only after that, when you need the
   exact current slice and latest handoff chain.

The MkDocs tree groups files into Overview, Specs, Runtime State, Development
Notes, Artifacts, and Misc. Low-confidence or evidence-only files stay under
Artifacts or Development Notes rather than being promoted to canonical status.

## Current Gaps This Overview Makes Explicit

| Gap | Current state | Best next owner document |
| --- | --- | --- |
| One visual gallery for progress review | Added as [PROGRESS_SCREENSHOT_INDEX.md](PROGRESS_SCREENSHOT_INDEX.md). | Keep image files in `samples/_probe/...`; keep the index as a pointer. |
| Turn-count development plan | Added as [TURN_BASED_DEVELOPMENT_PLAN.md](TURN_BASED_DEVELOPMENT_PLAN.md). | Update it only when planning bands change, not for every status note. |
| BN-05 YMM4 preview screenshot | Not present in repo yet. | Capture beside the Baseball placement proof and link it from [PROGRESS_SCREENSHOT_INDEX.md](PROGRESS_SCREENSHOT_INDEX.md). |
| Dense historical runtime entries | Still dense by design. | Use this page and [FEATURE_REGISTRY.md](FEATURE_REGISTRY.md) before reading `runtime-state.md`. |
