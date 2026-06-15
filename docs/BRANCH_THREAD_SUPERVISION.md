# Branch / Thread / Supervision Routing

This note exists to prevent mainline work, Baseball sidequest work, and
supervision prompts from being mixed across terminals or AI sessions.

## Current Routing Model

| Layer | Mainline | Baseball sidequest |
| --- | --- | --- |
| Repository | `https://github.com/YuShimoji/NLMYTGen.git` | Same repository |
| Remote branch | `origin/master` | `origin/codex/baseball-bn02-visual-data` |
| Local development thread | Mainline NLMYTGen thread | Baseball sidequest development thread |
| Supervisor thread | Mainline supervisor prompt | Baseball sidequest supervisor prompt |
| Default docs | `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`, `docs/runtime-state.md` | Those docs plus `docs/BASEBALL_NEWS_PIPELINE_SPEC.md`, `lanes/sports_news/docs/baseball_infographic_backlog.md`, and Baseball handoff docs |

The repository is shared. The branch, development thread, and supervisor prompt
are separated by lane.

## Branch Rule

Do not assume `master` when working inside a sidequest checkout. Before writing,
committing, or pushing, verify:

```powershell
git remote -v
git status --short --branch
git branch --show-current
git rev-list --left-right --count "HEAD...@{u}"
```

For Baseball sidequest work, the expected branch is:

```text
codex/baseball-bn02-visual-data
```

and the expected upstream is:

```text
origin/codex/baseball-bn02-visual-data
```

Push to the current lane branch. Do not push Baseball work to `master` unless
the user explicitly asks for a mainline integration / merge / cherry-pick.

## Thread Rule

The Baseball development thread is not the mainline development thread. A
future Codex session working on Baseball should treat Baseball as an explicitly
started sidequest and keep its artifact path inside:

- `docs/BASEBALL_NEWS_PIPELINE_SPEC.md`
- `lanes/sports_news/docs/`
- `BaseballInfoGraphics/`
- `samples/_probe/baseball/`
- Baseball rows in `docs/PROJECT_OVERVIEW.md`,
  `docs/PROGRESS_SCREENSHOT_INDEX.md`, and
  `docs/TURN_BASED_DEVELOPMENT_PLAN.md`

It should not silently replace the mainline `runtime-state.md` `next_action`,
revive G-27, start RSS / NotebookLM work, or merge branch state into `master`.

## Supervisor Prompt Rule

A supervisor prompt is for reviewing a Codex report. It is not a prompt for the
next Codex implementation session.

When the report is about Baseball sidequest work, label the prompt as:

```text
監修役AIに渡すPrompt（Baseball sidequest報告レビュー用。実装指示ではありません）
```

The reusable supervisor prompt is [BASEBALL_SUPERVISOR_REVIEW_PROMPT.md](BASEBALL_SUPERVISOR_REVIEW_PROMPT.md).
That file is allowed as a report-review aid. It is separate from the banned
pattern of creating a dedicated implementation-restart prompt file for the next
Codex session.

The prompt should ask the supervisor to check:

- whether the report stayed on the Baseball branch and did not assume
  `origin/master`;
- whether multiple commits are reported separately by purpose, touched files,
  and untouched boundaries;
- whether Baseball work remained a sidequest and did not replace mainline
  `runtime-state.md` authority;
- whether screenshots, frame exports, manifests, and YMM4 placement evidence
  are placed under the Baseball artifact paths;
- whether the report separates human final judgement from assistant/tool
  candidate generation, placement preparation, readback, and gap reports;
- whether commit / push / clean state and local build results are stated against
  the Baseball branch;
- whether mainline `master` integration remains a separate explicit human
  decision.

Use a separate label only when a prompt is meant for a future implementation
agent:

```text
次Codex用Prompt（Baseball sidequest実装再開用）
```

Do not use an unnamed handoff-prompt label. Name the recipient and purpose.

## Current Caveat

The documentation cleanup commit `25b74f8 docs: prune legacy claude entrypoints`
is currently on `codex/baseball-bn02-visual-data`. It is not automatically a
mainline `master` change. If that cleanup should become mainline policy, do a
separate explicit integration decision.
