# Runtime State — NLMYTGen

Project-State-ID: new-banknote-content-lineage-sealed-yymm4-batch-ready-v1
State-Revision: 2026-07-17.1
Updated: 2026-07-17 JST
Product-State: new-banknote-human-approved-script-lineage-sealed-operator-batch-ready
Product-Gate: manual-yymm4-import-observation
Recommended-Next: run-one-new-banknote-yymm4-operator-batch
External-State: public-repo-feature-branch
Handoff-Commit: 5d46a7389334626eb713ea5f9681288ac9b25b63
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

## Current Slice

- **Human approval sealed**: explicit user option A approval fixes commit
  `b05eb3867caabda496fb9a0070d230a4e81aea01`, eight approved file
  hashes, nine cue texts/order, scene allocation 2/4/3, Reimu/Marisa 3/6,
  canonical/derived CSV text, and current claim/source traceability.
- **Raw-to-approved lineage consolidated**: T00–T07 distinguish NotebookLM
  upstream generation, immutable intake, the 11-title freeze, official-source
  adjudication of all 182 claims, supported-only rewrite, editorial
  convergence, human approval, and mechanical YMM4 projection.
- **Cue lineage complete at meaning-unit granularity**: all nine cues connect
  raw claim IDs/fingerprints to 15 adopted verified-primary claims, four
  official sources, 20 factual units, and 21 evidence edges. Editorial
  connective and character-voice phrasing are explicitly non-quotational
  inferred units; token-level authorship is not claimed.
- **No-silent-change lock active**: any approved text, order, speaker, scene,
  claim, evidence edge, CSV, approval receipt, or lineage drift invalidates the
  approval and stops preflight. A later editorial, semantic, or upstream
  change requires a new revision, visible diff, and successor human approval
  receipt.
- **Manual YMM4 batch prepared**: the five-action user-operated batch verifies
  hashes before launch and again before collection, leaves counting to the
  collector, records mapping status and pronunciation/clipping notes through
  ignored UTF-8 JSON, and returns at most three items.
- **Headless checks passed**: deterministic lineage and operator generation,
  approval-drift rejection, 9/3/6/text/order/timing collector fixtures,
  PowerShell syntax, privacy boundaries, and worker-safe `-PreflightOnly`
  passed without inspecting or launching YMM4.
- **Cross-device handoff refreshed**: the public feature branch, validated
  commit, remote parity, clean tracked state, ignored evidence disposition,
  minimal read order, and exact manual gate are recorded in tracked state and
  project context. No hidden conversation context is required to resume.

## Product Position

The submitted transcript's influence is now inspectable without treating it as
factual authority: claim fingerprints show what entered the process, official
primary evidence shows what could survive, and the cue matrix separates facts
from Worker-authored connective, voice, and structure. The approved script
itself is unchanged.

This state is ready for one user-controlled YMM4 import observation. It is not
pronunciation acceptance, render approval, production, public release, rights
approval, or master integration.

## Exact Next Action

From the repository root, the user may run exactly:

`powershell -NoProfile -ExecutionPolicy Bypass -File ".\production_pilots\yukkuri_newsroom_content_spine_002\external_editorial_input\new_banknote_security_notebooklm_001\yymm4_operator_batch\run_new_banknote_yymm4_batch.ps1"`

Stop on an unrelated/unsaved project, mapping or update dialog, wrong
character, changed save target, parse error, changed text/order, or any request
to render or publish. The collector, not the user, verifies the nine
VoiceItems, 3/6 characters, exact text/order, and timing.

## Evidence and Access

- Primary lineage surface:
  `production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/README_CONTENT_LINEAGE.md`
- Approval and transformation evidence beside it:
  `human_script_approval_receipt.json`,
  `content_transformation_ledger.json`, `cue_lineage_matrix.json`,
  `content_change_summary.md`, and `content_lineage_readback.json`.
- Operator surface:
  `yymm4_operator_batch/README_OPERATOR_BATCH.md` and
  `yymm4_operator_batch/run_new_banknote_yymm4_batch.ps1`.
- Reusable acceptance contract:
  `docs/CONTENT_TRANSFORMATION_PROVENANCE.md`.

## Active Boundaries

- No approved script, claim, source, traceability, or CSV content changed.
- No NotebookLM access, web fetch, Computer Use, YMM4 launch/inspection,
  render, production, publication, rights action, or master integration
  occurred.
- Raw transcript, source bodies, local YMM4 project, batch state, operator
  observation/result, private path, NotebookLM link, and UUID remain ignored
  or absent from tracked artifacts.
- Remaining review debt is limited to token-level authorship unavailability,
  true Audio Overview speaker identity, unresolved S04 generation-time/S05
  exact-document identity, and H1 pronunciation/rhythm observation.

## Maintenance Note

Keep this capsule within 160 lines. Durable implementation evidence belongs in
the tracked lineage package, focused tests, and Git history.
