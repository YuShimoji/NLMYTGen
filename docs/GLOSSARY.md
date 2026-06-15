# Glossary

This is the vendor-neutral glossary for NLMYTGen workflow abbreviations. Link
this file whenever a doc uses S-n, L-n, or the three-layer responsibility
vocabulary.

## Production Steps

| ID | Name | What gets blocked when it stalls |
| --- | --- | --- |
| S-0 | YMM4 template construction | All video work lacks a reusable project base. |
| S-1 | NotebookLM source intake | There is no upstream material for the script. |
| S-2 | Script text retrieval | S-3 cannot receive text input. |
| S-3 | NLMYTGen CSV conversion | YMM4 cannot ingest the script or synthesize voices. |
| S-4 | YMM4 script import and voice synthesis | The YMM4 timeline does not exist. |
| S-5 | Voice/subtitle review | Reading errors or subtitle overflow remain. |
| S-6 | Background and direction setup | Visual quality remains unfinished. |
| S-7 | Final preview and rendering | No completed video file exists. |
| S-8 | Thumbnail production | The video lacks a publishing-facing click surface. |
| S-9 | YouTube publishing | The work does not reach viewers. |

## Pipeline Layers

L1-L4 describes where work runs in the video production pipeline.

| ID | Name | What gets blocked when it stalls |
| --- | --- | --- |
| L1 | Input acquisition outside NLMYTGen | Source material is missing. |
| L2 | Python conversion inside NLMYTGen | CSV, diagnostics, IR, registry, and adapter artifacts cannot be produced. |
| L3 | YMM4 internal production | Voice synthesis, preview, layout judgement, and rendering cannot complete. |
| L4 | Output and publishing | The completed video does not reach the distribution surface. |

## Three-Layer Responsibility Model

This vocabulary is independent from L1-L4. It describes how IR design and
adapter work are split inside the production-support architecture.

| ID | Name | Responsibility |
| --- | --- | --- |
| Layer 1 | Writer IR | High-level direction labels generated from the script. |
| Layer 2 | Template Registry | Reusable asset/template dictionaries, YMM4 native template names, maps, slots, and fallbacks. |
| Layer 3 | YMM4 Adapter | The bridge from IR + registry into post-import `.ymmp` patching. |

## Responsibility Shortcut

Human ownership means final creative judgement, source/rights approval, and
YMM4-only operations that have no proven adapter route. It does not mean humans
must perform every generation, placement, readback, or gap-classification step.
When a repo-approved adapter, registry, CLI, GUI, or script can generate or
place the artifact safely, the assistant/tool should do that work and return a
reviewable result.
