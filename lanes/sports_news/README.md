# sports_news lane

`sports_news` is a text/data/source-driven lane for clean sports news and sports reaction videos inside NLMYTGen.

Its value is speed, source discipline, factual structure, reaction digesting, original broadcast/data cards, and YMM4-compatible output.

This is a large sidequest lane. It does not replace the main NLMYTGen flow for Yukkuri explainer video production, and it must be explicitly started with `docs/prompts/baseball-sidequest-lane-prompt.md` when worked as a separate task.

## Authority split

This lane separates three decisions that must not collapse into one another:

- **Core design**: card hierarchy, readability, animation state, and renderer behavior.
- **Provenance**: where source facts, reactions, and non-data visual materials came from.
- **Publish gate**: whether an episode packet is ready for release after provenance and claim/source checks.

Rights/provenance documents do not veto core HTML/CSS/React design work. They are read when an episode imports materials or prepares for publication.

## Why this belongs in NLMYTGen

`sports_news` follows the NLMYTGen shape:

```text
structured sources -> source ledger -> fact ledger -> reaction digest
-> script / scene plan -> original broadcast/data cards -> YMM4-compatible output
```

It is **not** a ClipPipeGen-style workflow. ClipPipeGen remains the right boundary for video/audio cutting, EDL, highlight editing, or licensed footage workflows.

## MVP

The first MVP is a baseball-style sports news screen / episode format:

- 3 minutes or shorter.
- Structured YAML/JSON source input.
- Screen plan first: script segment -> card sequence -> information budget -> YMM4 placement type.
- Original scoreboard, stat, pitch-event, trend, timeline, and watch-point cards.
- Reactions represented as sourced digest cards.
- Ambient backdrops may support atmosphere when their provenance is recorded before asset ingest or publication.

The current visual reference is the repo-local `BaseballInfoGraphics/` draft design source. It is a design reference only, not a production renderer or proof artifact.

## File groups

| Path | Purpose |
| --- | --- |
| `schemas/` | Minimal machine-readable contracts for source, fact, reaction, publish-gate, and episode packets. |
| `examples/` | Placeholder sample data, screen plan samples, and sample-only provenance notes. |
| `docs/` | Visual language and screen template notes. |
| `templates/cards/` | YAML card specs for original broadcast/data UI modules. |

## Publish gate

Publication checks happen at the episode packet boundary, not during card design. A publish gate may block or request review when:

- a claim or reaction lacks a source reference;
- a non-data visual material lacks provenance or usage-stage notes;
- the episode relies on a material without an owner decision for publication;
- the thumbnail promise does not match the body.

The gate should report missing records, not infer broad design bans from asset categories.
