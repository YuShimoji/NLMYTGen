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
Do not force fixed section names or emit internal labels. Preserve the logical chain in normal language: what is complete, what was deliberately not changed, what changed for the workflow or decision space, what evidence supports it, what uncertainty remains, who moves next, and what happens after any return from the user.

File paths, line numbers, commits, and test names are evidence, not explanation. Put the user-readable meaning first, then cite files as support. Do not wait for the user to ask for "details" or "steps" before explaining what the change means and what happens next.

If the next blocker depends on operator input, explain why work is waiting or what can still run in parallel. A response that ends with only "please check" or "continue from here" is incomplete unless the exact required input and follow-up work are already clear.

## User-owned artifact handoff
When the next blocker is a user-owned action, the handoff must be concrete enough to execute without a follow-up clarification.
Do not say only "place materials", "run the GUI", or "return the outputs".
Include:
- whether the assistant is blocked or can continue in parallel
- exact required artifacts and their target paths
- the current state of each artifact: already exists, missing/user-authored, or generated later by a GUI/YMM4 step
- what each artifact is, how it is created or selected, and which GUI button/command consumes it
- optional artifacts and the condition that makes each one necessary
- the operation sequence, especially GUI tabs/buttons when GUI is the route
- success outputs and NG return files/text
- what the assistant will inspect or generate immediately after the user returns

Docs, README files, and manifests may support the handoff, but they do not replace the handoff. If the user must place files, operate the GUI, or check YMM4, the response body must be executable on its own. Phrases like "the procedure source of truth is <file>.md:<line>" are invalid when they are used to avoid restating required files, exact paths, operation order, outputs, NG returns, and follow-up work.

Bare placement bullets such as `put: <path>` / `置く: <path>` are invalid unless the same line or its immediate continuation explains `state`, `what`, `create`, and `used by`. Do not describe a downstream artifact as an initial placement merely because it is required later; for example, an Episode Pack base `.ymmp` is normally created after `Build CSV` by importing the generated CSV into YMM4 and saving the project.

Script handoffs need the same clarity. Do not say only "prepare a new script" / `新しい台本を用意してください`. State whether an existing completed script can be used, what the script is, accepted format, why it must match the episode, and which build step consumes it.

Background skit handoffs need an additional scene-bible gate. Do not present `skit_group` / 茶番劇 as narrator aitenote, line-by-line reactions, or a cue table that merely nods/jumps on script phrases. Before creative acceptance or production-quality review, state the independent scene bible: parallel layer / not aitenote / script line range / time budget / cast continuity / screen placement / visual situation / story logic / assets or templates / mechanical proof path. If that is absent, the handoff is invalid and any `.ymmp` output is transport/readback evidence only.

Background skit explanation closeouts need to become design work, not only concept acknowledgement. If the answer says the whole structure is still undetermined, it must also state that the assistant-owned next action is to produce `background_skit_blueprint.json` and run `validate-background-skit-blueprint` before IR/YMM4 placement. The artifact must separate characters, placement, backgrounds, props, existing templates, missing templates/assets, owner, and proof path. For IR-like direction, field names and numeric tables are not enough: `total duration`, `mm:ss`, `duration sec`, density thresholds/audit, and script maturity must contain actual values that are recomputed into validator `derived_metrics`, or a `TIMETABLE_BLOCKED_*` code with exact missing source. Otherwise the response is `BACKGROUND_SKIT_UNDERSPECIFIED_ACK` or `BACKGROUND_SKIT_TIMETABLE_BYPASS`: useful as recognition, but incomplete as a next-step handoff.

Self-contained background skit design answers must include script line ranges and block-level proof paths, not only block names and percentages. They must also separate IR intent from template names: `enter_from_left` is an intent, while `delivery_enter_from_left_v1` is a template name. Do not claim the design can go directly to IR/YMM4 review; the next assistant-owned step is validator-backed blueprint + gap report + template/proxy classification, then revised IR and compact review only after validator `passed`.

Closeout reports that mention all checks passing and untracked/new files must also state who acts next and what happens next. Otherwise the report is only an activity log: the user still cannot tell whether to review, stage, commit, or return a specific artifact.

## No progress laundering
Do not claim progress merely because:
- a doc was created during refresh
- a framework-compliant report was produced
- a list of changed files was shown
- a low-friction helper feature was specified
Report what became easier, safer, or more real for the actual artifact path.

## Forward-looking report contract (workspace-wide, set 2026-05-11)

Substantive work reports (commits, push events, hotfix delivery, slice progress, feature additions) must do more than log activity. Include:

- **Diff focus**: what was touched and deliberately left untouched.
- **Position vs final form / North Star**: where this delta lands relative to the project's end state, derived backwards from the goal — not chronological "after step N".
- **Evidence**: readback, tests, smoke runs, push/sync state.
- **Residual risk and unsettled judgement**: stale evidence, deferred decisions, areas needing user confirmation.
- **Recommended next hook**: the most natural assistant-owned next move.
- **Branching options**: 2–3 meaningfully different next directions, not a single linear next-step.
- **Next owner**: assistant / user / both.

At slice boundaries, handoffs, or explicit closeouts, also include a **feature status table** — implemented / in-progress / unimplemented / parked — scoped to the current slice or relevant feature-registry section. Keep the table tight (slice scope, not the whole registry).

This is the expected default for substantive reports across the workspace, not a mechanical template. Short Q&A, lookups, and exploratory direction questions remain terse. The goal is to give enough forward-looking context that the next move is obvious without re-prompting. A fixed audit form remains an anti-pattern; the minimum reporting contract is the floor — this contract raises the default density when the work is non-trivial.

### Drift / overfitting self-check

At slice boundaries, handoffs, and closeouts, self-diagnose against these failure modes and surface any that fire — with the next-step implication, not as a passive aside:

- **case overfitting**: aesthetic tuning that fits one episode/script/asset but does not generalize.
- **local optimization**: polishing within-stage artifacts while drifting from the North Star.
- **docs-only loop**: contracts/specs/READMEs accumulating without returning to implementation smoke, GUI ingest, or YMM4 readback.
- **standalone artifact completion**: treating a one-off HTML / PNG / JSON / fixture as "done" without next-stage integration or proof path.
- **user-as-governor dependency**: requiring the user to detect every direction shift before progress can resume.
- **next-artifact continuity**: whether the next-stage artifact, its consumer, and any blocked reasons are explicit.

If none fire, say so briefly. Silent self-checks do not count.

### Recommended default path

When listing 2–3 branching options, mark one as the assistant's **recommended default** and state why in one line (typically: shortest path to North Star, smallest blast radius, unblocks the most downstream work, or matches a standing user preference). Split the next moves into:

- **assistant-owned**: what the assistant can advance without further user input under standing approvals.
- **user-owned**: what requires user judgement, creative authorship, or external action (GUI / YMM4 / external tool).

Do not present options as an undifferentiated menu that punts the choice back to the user.

### Cross-project scope declaration

For cross-project work, declare scope in one line at the top of the report, e.g. `Scope: NLMYTGen / WritingPage / ClipPipeGen`. Keep it minimal — just enough to satisfy the guardrails cross-project pattern. Do not re-justify the cross-project context every report once it is established.
