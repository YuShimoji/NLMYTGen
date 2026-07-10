# G-28 Reference Input-Wait Handoff — 2026-06-04

This is a durable handoff for the G-28 parking state. It preserves the user
context that should survive terminal changes without turning `AGENTS.md` or
`REPO_LOCAL_RULES.md` into a long operations manual.

Normal restart still starts from `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` ->
`docs/runtime-state.md`. Read this file only when the next task touches G-28,
G-27 retirement, or ChatGPT copy-block reporting.

## Current Boundary

- Repo: `C:\Users\PLANNER007\NLMYTGen`
- Branch: `master`
- Prior expected HEAD before this handoff refresh:
  `4b46b02 docs: supersede G-27 with reference-driven screen carrier`
- G-27 is no longer the active blocker or a production carrier waiting loop.
- G-27 remains retained evidence: Real Estate DX diagnostic carrier, Review
  Console work, SCS lessons, and proof artifacts are not deleted.
- G-27 diagnostic carrier is not promoted to production.
- Missing `samples/_probe/g24/real_estate_dx_review_decisions.json` remains a
  G-27-specific handback gap, not a G-28 blocker.
- G-28 `Reference-Driven Generic Screen Carrier` is proposed and parked until
  human reference input arrives.

## Active And Parked Lanes

- Active NLMYTGen frontiers:
  - downstream adapter intake from a newsroom-produced packet, transcript,
    ScriptIR, VisualIR, or export bundle
  - G-28 reference-driven generic screen carrier refinement after reference
    input is supplied
- Parked lane:
  - G-28 waits for 3-7 human-supplied reference images plus per-image notes
    describing what to learn from each image.
- Out of active NLMYTGen scope:
  - RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack
    selection
  - G-27 production carrier waiting, unless explicitly reopened by the user
  - YMM4 `.ymmp` zero generation, render, production timing, or creative final
    acceptance for G-28 before reference input

## Human Input Required For G-28

G-28 can resume when the human supplies 3-7 reference images and a short memo
for each image. The images are not production materials. They are principle
sources for extracting screen grammar:

- composition
- negative space
- information density
- color hierarchy
- eye path
- dashboard / database / gated-information feel
- YouTube explainer / news infographic readability

Do not commit image files, image URLs, unclear-copyright images, private data,
personal information, source notes, or article body text to the repo.

Recommended user input shape:

```text
G-28 参照画像入力

画像1:
- 参考対象:
- 使いたい理由:
- 避けたい要素:

画像2:
- 参考対象:
- 使いたい理由:
- 避けたい要素:

画像3:
- 参考対象:
- 使いたい理由:
- 避けたい要素:

全体方針:
- light / dark の希望:
- 情報密度:
- YouTube解説感:
- DB / dashboard 感:
- lock / gated information 感:
- 最初に試したい題材:
  - 不動産DX
  - newsroom explainer
  - AI monitoring
  - baseball / sports news
  - その他
```

## Agent Work When G-28 Resumes

When valid input arrives:

1. Do not copy the reference images.
2. Create a reference style brief.
3. Create an SCS mapping.
4. Create a generic carrier archetype.
5. Create a YMM4 item / group structure proposal.
6. If useful, create the next prompt for Codex or ChatGPT.
7. Keep the first output as text / JSON-ready design artifacts.
8. Do not proceed to `.ymmp` generation, rendering, production timing, or
   creative final acceptance.

## First Restart Checks

If this context is used in a new terminal:

1. Open the repo.
2. Check tracked dirty state:
   - `git status --short --branch`
   - `git status --porcelain=v1 -uno`
3. If tracked files are dirty, stop before pull, docs edits, commit, or push,
   and report a dirty stop.
4. If tracked clean:
   - `git fetch --all --prune`
   - `git checkout master`
   - `git pull --ff-only origin master`
   - `git rev-list --left-right --count HEAD...origin/master`
   - `git log -1 --oneline`
5. Read only the necessary authority docs:
   - `AGENTS.md`
   - `docs/REPO_LOCAL_RULES.md`
   - `docs/runtime-state.md`
6. For G-28 work, then read:
   - `docs/FEATURE_REGISTRY.md`
   - `docs/REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md`
   - `docs/SCENE_COMPOSITION_SCHEMA.md`
   - `docs/project-context.md`
   - `docs/INVARIANTS.md`

## Explicit Non-Actions In This Parking State

- Do not return G-27 to active blocker status.
- Do not promote the G-27 diagnostic carrier to production.
- Do not treat G-27 `review_decisions.json` absence as a G-28 blocker.
- Do not start material/image acquisition.
- Do not commit reference image binaries or URLs.
- Do not commit raw OPML, tokens, article bodies, private data, or unclear
  copyright material.
- Do not generate images with Python or compose images with PIL/Pillow.
- Do not generate YMM4 `.ymmp` from zero.
- Do not render, time production output, or claim creative acceptance.
- Do not return to RSS / OPML / Inoreader / topic clustering / NotebookLM
  source-pack selection inside NLMYTGen.
- Do not turn docs-only refinement into progress after the parking state is
  clear.
- Do not enlarge `AGENTS.md`.
- Do not perform destructive operations, large deletion, history rewrite, or
  force push.

## Meta-Review Trigger

Run a meta-review instead of continuing normal work if any of these appear:

- the same blocker appears two or more times
- human-side work keeps expanding
- proof / docs / readback grows, but the active artifact does not advance
- a case-specific task is drifting into generic capability without saying so
- the agent repeatedly reports input-wait / cannot-do / safe-stop
- old artifacts or old lanes keep reappearing as active candidates
- repo responsibilities are mixed

The meta-review should decide whether to continue, narrow, supersede, retire,
migrate, or request authority. If an old task is useful, keep it as reference
evidence rather than deleting it.

## ChatGPT Copy-Block Requirement

When the user asks for the historical ChatGPT-supervised handoff, its former
copy block is no longer present in the active tree. Recover the exact record
only with `git show 99477a0:docs/USER_COPYPASTE_BLOCKS.md`.

The block must make these facts clear:

- G-28 is parked / input-wait, not implementation-complete.
- the next human input is 3-7 reference images plus per-image notes.
- images and URLs are not committed.
- G-27 remains retained evidence and is not active blocker.
- RSS / OPML / Inoreader / topic clustering / NotebookLM source-pack selection
  are not resumed in NLMYTGen.
- no `.ymmp`, render, production timing, or creative final acceptance is part
  of the parking state.
