# Newsroom Terminal Resume Remote Sync Handoff v2

This handoff records the current NLMYTGen restart context before reflecting the
local mainline-slot worktree to `origin/master`. It is a repository-context
handoff only: it does not change product behavior, generated media, YMM4
projects, dependencies, or external contracts.

## Current Remote State

The active worktree is:

`C:\Users\thank\Storage\Media Contents Projects\NLMYTGen-mainline-slot-linkage`

Before this handoff, it was fetched, clean, on `master`, and aligned with
`origin/master`:

- latest completed commit before handoff: `3e81daa docs: add rss dry-run animated beat proof`
- branch relation before handoff: `HEAD...origin/master = 0 0`
- normal restart entry: `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`

## What This Handoff Preserves

The current active context is the RSS dry-run animated explanation beat proof.
The previous v2 visible-integration preview passed with boundaries: the user
saw one visible plain explanation `TextItem` and the character animation accent
in the same YMM4 scene, with no card-like designed overlay. That is a bounded
visual integration pass, not production subtitle/card design acceptance.

The latest content-flow proof turns one offline RSS-like diagnostic topic into
one animated explanation beat with:

- a topic-derived explanation line,
- a plain `TextItem` role,
- a source-boundary role,
- the frozen minimal animation accent,
- no live RSS/news fetch,
- no card redesign,
- no animation tuning,
- no render or audio/TTS.

The restart artifacts to read if the runtime entry is not enough are:

| Path | Role |
| --- | --- |
| `samples/_probe/newsroom_handoff/rss_dry_run_topic_to_animated_explanation_beat_v1.json` | machine-readable topic-to-beat proof |
| `samples/_probe/newsroom_handoff/rss_dry_run_animated_explanation_beat_contract_v1.json` | contract/readback boundary |
| `docs/verification/NEWSROOM_RSS_DRY_RUN_TO_ANIMATED_EXPLANATION_BEAT_V1_2026-06-30.md` | human-readable proof |
| `samples/_probe/newsroom_handoff/terminal_resume_remote_sync_handoff_v2.json` | machine-readable handoff snapshot |

## Local Evidence Not To Commit

These ignored local review targets exist on this authoring host:

| Local path | State |
| --- | --- |
| `_tmp/newsroom_manual_probe/rss_dry_run_animated_explanation_beat_v1.ymmp` | current RSS dry-run animated beat review target |
| `_tmp/newsroom_manual_probe/minimal_animated_explanation_beat_mainline_v2_visible_integration.ymmp` | prior visible-integration proof target |

Both are intentionally untracked. `git check-ignore -v` resolves them through
`.gitignore` rule `_tmp/`, so another terminal should treat them as same-host
review evidence, not as tracked remote artifacts.

## Next Default Axis

`newsroom-rss-dry-run-animated-explanation-beat-preview-operator-instruction-v1`

The next work should prepare a bounded operator instruction for opening the
current ignored local RSS dry-run `.ymmp` and checking only whether the
topic-derived `TextItem` and the frozen animation accent support the explanation
beat. Do not turn this into an animation tuning loop, card polish loop, render
loop, live RSS/news fetch, or production/public acceptance claim.

## Boundaries

This handoff does not claim:

- Agent-side YMM4 launch,
- render/export proof,
- `.ymmp` committed to git,
- media/audio/TTS generation,
- live RSS/news or external media fetch,
- card redesign or production subtitle/card design,
- animation tuning,
- production/public readiness,
- audience/order acceptance.

Adjacent workspace note: `C:\Users\thank\Storage\Media Contents Projects\NLMYTGen`
is a separate checkout on `codex/baseball-bn08-script-beat-linkage` and was
observed clean. `C:\Users\thank\Storage\Media Contents Projects\ClipPipeGen`
has pre-existing local modifications and was not touched or pushed in this
NLMYTGen handoff.

## Validation

This is docs/context-only handoff work, so no pytest is required by the
repo-local rules. The relevant validation is git/readback:

- fetch `origin/master`,
- confirm `HEAD...origin/master = 0 0` before handoff edits,
- confirm the ignored local `.ymmp` targets exist and are ignored,
- parse the handoff JSON,
- run `git diff --check`,
- run `git diff --cached --check`,
- scan staged files for forbidden `.ymmp`, media, audio, TTS, or render outputs,
- commit and push the handoff to `origin/master`,
- verify `master...origin/master` is clean after push.
