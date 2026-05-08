# sports_news lane

`sports_news` is a text/data/source-driven lane for clean sports news and sports reaction videos inside NLMYTGen.

This lane does **not** produce highlight or cutout videos. It does not ingest match footage, official videos, official screenshots, website screenshots, X/Twitter screenshots, news photos, AI-generated athlete images, or fabricated fan reactions.

Its value is speed, source discipline, factual structure, reaction digesting, and original information graphics.

## Why this belongs in NLMYTGen

`sports_news` follows the NLMYTGen shape:

```text
structured sources -> source ledger -> fact ledger -> reaction digest
-> script / scene plan -> self-made visual cards -> YMM4-compatible output
```

It is **not** a ClipPipeGen-style workflow. ClipPipeGen remains the right boundary for video/audio cutting, EDL, highlight editing, official/broadcast footage ingestion, or licensed footage workflows.

## Non-negotiable boundaries

- No match footage.
- No official video footage, screenshots, or audio.
- No website, news site, official site, or X/Twitter screenshots.
- No third-party photo assets in the initial MVP.
- No AI-generated public-facing athlete images, realistic people, fake sports scenes, fake fan faces, or meme assets.
- No fabricated comments or unsourced reaction claims.
- No Content ID-based strategy.
- No team logos or official marks as decorative assets unless explicitly reviewed later.
- No external image/icon packs unless explicitly reviewed and licensed.

Backend AI may be used only for editorial assistance such as translation drafts, source summarization, reaction clustering, title brainstorming, script outline assistance, and consistency checks.

## MVP

The first MVP is a baseball-style sports news screen / episode format:

- 3 minutes or shorter.
- Structured YAML/JSON source input.
- Self-made broadcast/data UI cards only.
- Reactions represented as digest cards, not screenshots.
- Data shown through original scoreboard, stat, pitch-event, trend, timeline, and watch-point cards.

The current visual reference is the repo-local `BaseballInfoGraphics/` draft design source. It is a design reference only, not a production renderer or proof artifact.

## File groups

| Path | Purpose |
| --- | --- |
| `schemas/` | Minimal machine-readable contracts for source, fact, reaction, rights, and episode packets. |
| `examples/` | Placeholder sample data with no real copyrighted assets. |
| `docs/` | Closed topics, visual language, and screen template notes. |
| `templates/cards/` | YAML card specs for self-made broadcast UI modules. |

## Publish gate

Publication must be rejected when any of these are true:

- unlicensed footage is referenced as a visual or audio asset
- any screenshot is used
- any public-facing AI visual is used
- any reaction lacks a source reference
- any claim lacks a source reference
- thumbnail promise does not match the body
- official footage or site images are used
- Content ID is relied on as a strategy
