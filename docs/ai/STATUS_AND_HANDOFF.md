# STATUS_AND_HANDOFF.md
Ruleset-Version: v20
Status: canonical

## Feature status semantics
Keep priority separate from status.

### Priority
Priority answers: “How worth looking at is this item compared with others?”
Examples: high / medium / low, or a ranked list.

### Status
Status answers: “What lifecycle state is this item in now?”
Use these meanings strictly:
- `proposed`: value is still being validated or the spec is incomplete
- `approved`: specification and scope are defined enough for implementation to start, and the user has approved that move
- `hold`: not rejected, but not the current move due to prerequisites, weak value path, timing, or other blockers
- `rejected`: should not be pursued within the current product/workflow scope
- `quarantined`: potentially contaminated or unauthorized batch-derived item; do not treat as a normal candidate until re-reviewed

Selection of a `proposed` item for deeper review does **not** upgrade it to `approved`.

## FEATURE_REGISTRY discipline
For each feature candidate, keep at least:
- short description
- priority
- status
- rationale
- integration point / value path note
- actor / owner note when relevant

`approved` requires all of the following:
- clear input/output or scope boundary
- no unresolved boundary violation
- value path is stated
- user approval for implementation is explicit

If an unauthorized item appears in a proposal batch, quarantine the whole batch by default until individually re-reviewed.

## Canonical context fields to surface in reports
Use these report fields whenever relevant:
- Non-Negotiables
- Reused Canonical Context
- New Fossils
- Backlog Delta
- Current Trust Assessment

## Current Trust Assessment
When a thread has become noisy or risky, classify changes into:
- trusted
- needs re-check
- dangerous / rollback candidate
State why.

## Handoff minimum
A robust handoff should preserve:
- shared focus
- non-negotiables
- current trust assessment
- active artifact and bottleneck
- recovered canonical context
- feature/backlog status with strict semantics
- safe next-thread plan
- what not to do next
- new fossils created in the current thread

## Closeout chain minimum
Final responses should not merely summarize activity; they should make the next move executable.
Do not force fixed section names, but preserve the logical chain:
- summary: what is complete and what was deliberately not changed
- evidence: validation, readback, or why validation was not run
- risk: residual uncertainty, stale evidence, or judgement still needed
- next owner: assistant, user, or both
- assistant next: what the assistant will inspect, generate, or fix after any user-owned return

If user action is the next blocker, explain why the assistant is blocked or what can still run in parallel. A response that ends with only "please check" or "continue from here" is incomplete unless the exact user action and assistant follow-up are already clear.

## User-owned artifact handoff
When the next blocker is a user-owned action, the handoff must be concrete enough to execute without a follow-up clarification.
Do not say only "place materials", "run the GUI", or "return the outputs".
Include:
- whether the assistant is blocked or can continue in parallel
- exact required artifacts and their target paths
- optional artifacts and the condition that makes each one necessary
- the operation sequence, especially GUI tabs/buttons when GUI is the route
- success outputs and NG return files/text
- what the assistant will inspect or generate immediately after the user returns

## No progress laundering
Do not claim progress merely because:
- a doc was created during refresh
- a framework-compliant report was produced
- a low-friction helper feature was specified
Report what became easier, safer, or more real for the actual artifact path.
