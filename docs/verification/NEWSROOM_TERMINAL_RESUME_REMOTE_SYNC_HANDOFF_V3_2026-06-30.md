# Newsroom Terminal Resume Remote Sync Handoff v3

This handoff records the latest PLANNER007 NLMYTGen restart context after
`84f4406 docs: add offline rss fixture v2 capsule`. It exists so another
terminal can resume from `origin/master` without relying on chat-only memory.

## Current Remote State

The active worktree is:

`C:\Users\PLANNER007\NLMYTGen`

Before this handoff edit, it was fetched, clean, on `master`, and aligned with
`origin/master`:

- latest synced commit before handoff: `84f4406 docs: add offline rss fixture v2 capsule`
- branch relation before handoff: `HEAD...origin/master = 0 0`
- normal restart entry: `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`

## Latest Product Context

The latest product slice is
`newsroom-offline-rss-like-topic-fixture-v2-to-mini-episode-capsule-v1`.

That slice strengthened the previous offline RSS-like topic route by creating:

| Path | Role |
| --- | --- |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json` | stronger offline topic fixture |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json` | fixture v2 schema contract |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json` | fixture-to-five-beat capsule readback |
| `docs/verification/NEWSROOM_OFFLINE_RSS_LIKE_TOPIC_FIXTURE_V2_TO_MINI_EPISODE_CAPSULE_V1_2026-06-30.md` | human-readable verification |
| `src/pipeline/newsroom_offline_rss_like_topic_fixture_v2.py` | deterministic builder |
| `tests/test_newsroom_offline_rss_like_topic_fixture_v2.py` | focused regression test |

The route classification is `current_partial`: diagnostic-only, reusable
fixture candidate, stronger than v1, not blocked, and still synthetic because
source URL, freshness, and rights remain explicit placeholders.

## Restart Procedure

From another terminal:

```powershell
cd C:\Users\PLANNER007\NLMYTGen
git fetch origin
git checkout master
git pull --ff-only origin master
git status --short --branch
git rev-list --left-right --count HEAD...origin/master
```

Expected result after pull:

- branch: `master`
- relation: `HEAD...origin/master = 0 0`
- tracked worktree: clean except ignored `_tmp`
- next default axis: `newsroom-rss-topic-fixture-route-hardening-v1`

## What To Read First

Read in this order:

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`
4. `docs/project-context.md`
5. this handoff if more detail is needed

For the latest product slice, read:

| Path | Why |
| --- | --- |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2.json` | fixture v2 field values and placeholders |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_schema_contract_v1.json` | required/recommended field contract |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_to_mini_episode_capsule_v1.json` | beat mapping, route assessment, next axis |
| `docs/verification/NEWSROOM_OFFLINE_RSS_LIKE_TOPIC_FIXTURE_V2_TO_MINI_EPISODE_CAPSULE_V1_2026-06-30.md` | readable verification |

## Local Evidence Not To Commit

Relevant ignored local YMM4 probes on PLANNER007:

| Local path | Size | State |
| --- | ---: | --- |
| `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v1.ymmp` | 267302 | ignored local-only diagnostic project |
| `_tmp/newsroom_manual_probe/offline_topic_mini_episode_capsule_materialized_v2_readable_text.ymmp` | 267097 | ignored local-only readable preview target |

`git check-ignore -v` resolves both through `.gitignore:37:_tmp/`. Other
historical probe media/projects may also exist under `_tmp/newsroom_manual_probe`;
they are local evidence only and must not be staged or committed.

## Boundaries

This handoff does not claim or perform:

- Agent-side YMM4 launch,
- render/export proof,
- `.ymmp` creation/modification/stage/commit,
- media/audio/TTS generation,
- live RSS/news or external media fetch,
- card redesign or production subtitle/card design,
- animation tuning,
- production/public readiness,
- audience/order acceptance.

## Next Safe Moves

| Axis | Use When |
| --- | --- |
| `newsroom-rss-topic-fixture-route-hardening-v1` | default next move; add deterministic fixture validation and placeholder hardening |
| `newsroom-episode-capsule-route-hardening-v1` | use if beat contract generation becomes the dominant ambiguity |
| `newsroom-live-rss-boundary-plan-v1` | use only after offline fixture validation is strong enough and live-source boundary planning is the real blocker |

## Validation

This is repository-context handoff work. The latest product slice already
passed `uv run pytest tests/test_newsroom_offline_rss_like_topic_fixture_v2.py`
with `7 passed`.

Handoff validation should cover:

- fetch/branch relation,
- JSON parse for `terminal_resume_remote_sync_handoff_v3.json`,
- `git diff --check`,
- `git diff --cached --check`,
- staged forbidden-file scan for `.ymmp`, media, audio, TTS, or render outputs,
- commit and push to `origin/master`,
- final clean `master...origin/master` state.
