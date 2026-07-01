# Newsroom Terminal Resume Remote Sync Handoff v4

This handoff records the latest PLANNER007 NLMYTGen restart context after
`28940f8 newsroom: harden episode capsule boundaries`. It exists so another
terminal can resume from `origin/master` without relying on chat-only memory.

## Current Remote State

The active worktree is:

`C:\Users\PLANNER007\NLMYTGen`

Before this handoff edit, it was fetched, clean, on `master`, and aligned with
`origin/master`:

- latest synced commit before handoff: `28940f8 newsroom: harden episode capsule boundaries`
- previous context commit: `1dee1f2 newsroom: add rss topic fixture route hardening`
- previous terminal handoff commit: `b12e55d docs: add terminal resume handoff v3`
- branch relation before handoff: `HEAD...origin/master = 0 0`
- normal restart entry: `AGENTS.md` -> `docs/REPO_LOCAL_RULES.md` -> `docs/runtime-state.md`

## Latest Product Context

The latest product slice is
`newsroom-episode-capsule-route-hardening-v1`.

That slice hardened the prior fixture-to-capsule route by creating:

| Path | Role |
| --- | --- |
| `samples/_probe/newsroom_handoff/episode_capsule_route_hardening_v1.json` | route-level hardening proof and recommendation |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_hardened_episode_capsule_v1.json` | hardened five-beat capsule readback |
| `docs/verification/NEWSROOM_EPISODE_CAPSULE_ROUTE_HARDENING_V1_2026-06-30.md` | human-readable verification |
| `src/pipeline/newsroom_episode_capsule_route_hardening.py` | deterministic builder |
| `tests/test_newsroom_episode_capsule_route_hardening.py` | focused regression test |

The route is diagnostic-only and reusable offline. The hardened capsule carries
fixture validation status, `production_blocker_count=6`,
`explicit_placeholder_count=5`, source/rights/freshness/attribution summaries,
excluded-claims summary, and beat-level can-use flags. Every beat carries
excluded claims, rights/freshness/attribution status, diagnostic production
status, not-accepted scope, and `production_claim_allowed=false`.

The source-boundary warning beat explicitly names the offline fixture,
placeholder source URL/timestamp, rights/freshness/attribution not being
production-approved, and excluded claims not being assertable. Readback keeps
`production_script_ready=false` and `live_boundary_plan_ready=false`.

## Restart Procedure

From another terminal:

```powershell
cd C:\Users\PLANNER007\NLMYTGen
git fetch origin
git checkout master
git pull --ff-only origin master
git status --short --branch
git rev-list --left-right --count HEAD...origin/master
git log -1 --oneline
```

Expected result after pull:

- branch: `master`
- relation: `HEAD...origin/master = 0 0`
- tracked worktree: clean except ignored `_tmp`
- latest context entry: `Newsroom terminal resume remote sync handoff v4 completed`
- next default axis: `newsroom-source-boundary-adversarial-fixtures-v1`

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
| `samples/_probe/newsroom_handoff/episode_capsule_route_hardening_v1.json` | route-hardening decision, readback, and next axis |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_hardened_episode_capsule_v1.json` | capsule-level and beat-level propagated boundaries |
| `docs/verification/NEWSROOM_EPISODE_CAPSULE_ROUTE_HARDENING_V1_2026-06-30.md` | readable proof of the hardening slice |
| `samples/_probe/newsroom_handoff/rss_topic_fixture_route_hardening_v1.json` | upstream fixture-route validation |
| `samples/_probe/newsroom_handoff/offline_rss_like_topic_fixture_v2_validation_v1.json` | field validation and placeholder classification |

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
| `newsroom-source-boundary-adversarial-fixtures-v1` | default next move; exercise missing, invalid, and unmarked placeholder cases across validator and capsule route |
| `newsroom-live-rss-boundary-plan-v1` | use after adversarial offline cases are stable; this is boundary planning only, not live fetch implementation |
| `newsroom-episode-capsule-route-hardening-v2` | use only if adversarial cases reveal beat-level boundary propagation gaps |
| `newsroom-rss-topic-fixture-route-hardening-v2` | use only if adversarial cases reveal fixture validator schema or placeholder-classification gaps |

## Validation

This is repository-context handoff work. The latest product slice already
passed:

```powershell
uv run pytest tests/test_newsroom_episode_capsule_route_hardening.py tests/test_newsroom_rss_topic_fixture_route_hardening.py tests/test_newsroom_offline_rss_like_topic_fixture_v2.py
```

with `21 passed`.

Handoff validation should cover:

- fetch/branch relation,
- JSON parse for `terminal_resume_remote_sync_handoff_v4.json`,
- `git diff --check`,
- `git diff --cached --check`,
- staged forbidden-file scan for `.ymmp`, media, audio, TTS, or render outputs,
- commit and push to `origin/master`,
- final clean `master...origin/master` state.
