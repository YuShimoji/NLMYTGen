# Newsroom Terminal Resume Remote Sync Handoff v1

This handoff records the current restart context before reflecting the local
checkout to `origin/master`. It is a repository-context slice only: it does not
change product behavior, generated media, YMM4 projects, dependencies, or
external contracts.

## What This Handoff Preserves

The local checkout was clean and aligned with `origin/master` at `6b66f03`
before this slice. The active context remains the newsroom yukkuri v3
tempo-fix preview gate. The prior v2 preview improved anchor continuity and
connected motion; the remaining actionable issue is slow tempo. The v3 local
probe keeps the v2 shared-anchor and neutral-facing fixes, halves beats from
360 frames / 6 seconds to 180 frames / 3 seconds, and shortens the probe to
900 frames / 15 seconds.

The ignored local review target exists on this authoring host:

`_tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp`

It is intentionally not committed. `git check-ignore -v` resolves it through
`.gitignore` rule `_tmp/`, so a future terminal should treat it as host-local
evidence, not a missing remote artifact.

## Remote Sync Boundary

This handoff adds only tracked context:

| Tracked path | Why it matters for restart |
| --- | --- |
| `docs/runtime-state.md` | Keeps the next reader's first current-state stop at the very top of the canonical runtime file. |
| `docs/project-context.md` | Adds a decision-log entry so the handoff is visible from the project history surface. |
| `samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v1.json` | Gives a compact machine-readable readback of branch, remote, ignored local probe, next axis, and validation plan. |
| `docs/verification/NEWSROOM_TERMINAL_RESUME_REMOTE_SYNC_HANDOFF_V1_2026-06-29.md` | Gives a human-readable restart note for another terminal. |

No Agent-side YMM4 launch, render/export pass, `.ymmp` stage/commit,
media/audio/TTS generation, dense script continuation, real RSS/news fetch,
external reference-video fetch, production/public readiness claim, or
audience/order acceptance claim occurred in this slice.

## Resume Path

On another terminal, start with `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, and the
top of `docs/runtime-state.md`. Read this verification note only if the runtime
entry is not enough.

The next default axis remains:

`newsroom-yukkuri-animation-primitive-v3-preview-operator-instruction-v1`

That next slice should prepare the operator-facing instruction for reviewing
the ignored local v3 tempo-fix probe, without turning the local `.ymmp` into a
tracked artifact and without claiming render readiness unless a render gate is
explicitly run.

## Validation

No pytest is required for this handoff because it is docs/context only and does
not change an executable contract. The relevant validation is git-side:

- `git status --short --branch` before staging showed `master` aligned with
  `origin/master`.
- `git check-ignore -v -- _tmp/newsroom_manual_probe/yukkuri_animation_primitive_probe_v3_tempo_fix.ymmp`
  confirmed the v3 probe is ignored through `_tmp/`.
- After commit, push, and remote verification, `git status --short --branch`
  should show `master` aligned with `origin/master`.
