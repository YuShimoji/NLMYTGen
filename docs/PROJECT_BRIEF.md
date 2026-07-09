# Project Brief

## Project name

NLMYTGen

## Purpose

Convert NotebookLM-style transcript material and newsroom downstream packets
into YMM4-facing CSV, IR, review packs, and machine-readable validation
readbacks.

## Primary users

- The local operator preparing YMM4 import/review work.
- Codex/assistant agents continuing bounded BUILD slices.
- Human reviewers checking Japanese review surfaces before any explicit YMM4,
  real-input, rights, or publication gate opens.

## User language

Japanese is the primary user language. Machine-readable JSON keys may stay
English when they are part of an existing schema.

## Core value

Keep the production path moving through reversible local evidence: generated
HTML/JSON/Markdown review packs, focused tests, and explicit closed-gate
readbacks.

## Product surface

- Python CLI under `src/cli/main.py`.
- Electron desktop GUI under `gui/`.
- Generated review packages under `production_pilots/`.
- Repo-local docs and verification ledgers under `docs/`.

## Non-goals

- Upstream source selection, RSS/OPML/Inoreader/topic clustering, or NotebookLM
  source-pack selection unless explicitly reopened.
- Actual YMM4 GUI launch/import/render/export or production `.ymmp` writing
  without an explicit gate.
- Live fetch/scraping, external media download, OAuth/API key work, payment,
  upload/publication, or rights/public-ready acceptance.

## Current product hypothesis

The next useful progress is not broader planning. It is a narrow evidence slice
around either verified real-input replacement prep, explicit YMM4 import
observation readback, or screenshot-backed review-surface QA for the current
Episode 002 Japanese import-ready pack.

## Re-kickstart rule

This project prioritizes material evidence over report volume. BUILD turns must
produce implementation, validation, screenshot, generated artifact, or
reproducible probe evidence.
