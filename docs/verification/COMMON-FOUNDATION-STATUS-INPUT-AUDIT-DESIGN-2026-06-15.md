# Common Foundation Status Input Audit Design - 2026-06-15

This is a docs-only design slice for
`common_foundation_status_input_audit_design_001`.

It refines
`docs/verification/LIVE-REPO-STATUS-JSON-PRODUCER-DESIGN-2026-06-13.md`
by defining the audit-facing status object that preflight, gate, and operator
surfaces can read without depending on old chat logs. It does not implement a
producer, does not start a runner, does not run `codex exec`, does not add
`subprocess.run`, does not pipe stdin, does not create a worker loop, does not
send notifications, and does not create runtime artifacts.

## Live Preconditions Observed For This Design

These values were observed before writing this docs slice. They are evidence
for this design note, not a durable current-status source.

| Check | Observed value |
| --- | --- |
| Branch | `master` |
| Tracked status | clean by `git status --porcelain=v1 -uno` |
| All porcelain status | `.claude/worktrees/`, `samples/2026-05-16.ymmp` |
| Fetch / pull | `git fetch --prune origin`; `git pull --ff-only origin master` returned already up to date |
| HEAD before this docs edit | `4746d81 docs: design live repo status producer` |
| Upstream parity | `0 0` by `git rev-list --left-right --count "HEAD...@{u}"` |
| Unstaged tracked diff | none by `git diff --name-only` |
| Staged diff | none by `git diff --cached --name-only` |
| Runtime reports | `.agent/reports/` contained only `.gitkeep` |
| Runtime logs | `.agent/logs/` contained only `.gitkeep` |
| Needs-human state | `.agent/needs_human.json` absent |

The earlier assumption that latest HEAD was
`66be70d docs: add G-28 chat-first review protocol` is stale in this checkout.
The stale assumption did not block this slice because the live branch,
upstream parity, tracked diff, staged diff, known untracked residue, and runtime
artifact state were still explainable from current repo evidence.

## Purpose

The status object is an observed input for common-foundation review. Its job is
to make repo state reconstructable from live Git/filesystem checks and
repo-local authority docs.

It is not execution authority. It must not grant a runner permission to start,
must not mark real execution approved, and must not turn an eligibility signal
such as `safe_to_start_real_runner` into permission. A downstream preflight or
gate may read the object, but any future real-runner consumption needs a
separate authorized slice.

## Status Object Common Core Fields

The common core field names are stable across repos. Repo adapters may supply
policy values, but they should not rename these fields.

| Field | Meaning | Fail-closed expectation |
| --- | --- | --- |
| `schema_version` | Integer contract version. | Missing or unsupported version blocks consumption. |
| `observer_mode` | `docs_only`, `preflight_preview`, or `runner_consumption_future`. | Any mode implying real execution in this slice is blocked. |
| `observed_at` | Timestamp when live checks completed. | Missing or stale timestamp becomes `needs_human` for preview and blocks future real execution. |
| `repo_adapter_id` | Adapter id, such as `nlmytgen`. | Missing, unknown, or mismatched adapter blocks consumption. |
| `branch` | Current branch name from `git branch --show-current`. | Empty, detached, or unparsable branch blocks future real execution. |
| `head_commit` | Current HEAD hash and subject from `git log -1 --oneline`. | Missing or unparsable HEAD is blocked. |
| `upstream` | Resolved upstream identity or structured missing state. | Missing upstream is `needs_human` for preview and blocks future real execution. |
| `remote_parity` | Ahead/behind counts from `git rev-list --left-right --count "HEAD...@{u}"`. | Nonzero ahead/behind, command failure, or parse failure fails closed. |
| `porcelain_status_tracked` | Raw tracked-only status from `git status --porcelain=v1 -uno`. | Any entry is `needs_human`; future real execution blocks. |
| `porcelain_status_all` | Raw full porcelain status from `git status --porcelain=v1`. | Unknown untracked entries are `needs_human`; future real execution blocks. |
| `known_untracked_matches_allowlist` | Adapter allowlist result for untracked entries. | Unknown entries fail closed until removed, ignored by policy, or allowlisted in a separate change. |
| `dirty_state` | Normalized summary of tracked, staged, unstaged, and untracked state. | Any unexplainable dirty state blocks consumption. |
| `staged_diff` | Staged file list from `git diff --cached --name-only`. | Any staged diff blocks slices that expect no staged changes. |
| `unstaged_diff` | Unstaged tracked file list from `git diff --name-only`. | Any unexpected tracked diff is `needs_human`. |
| `runtime_artifact_state` | `.agent` report/log runtime residue summary. | Runtime entries outside expected placeholders are `needs_human`. |
| `needs_human_state` | Presence/readability of configured needs-human file. | Unexpected presence is `needs_human`. |
| `authority_docs_checked` | Authority docs read and whether any were missing or contradictory. | Missing or contradictory authority docs fail closed. |
| `execution_policy_snapshot` | Read-only snapshot of execution policy, including `codex_exec_enabled`. | `codex_exec_enabled=false` blocks any attempted real runner consumption. |
| `fail_closed_reasons` | Stable reason strings explaining any non-consumable state. | Empty only when all required checks are known and parseable. |
| `source_provenance` | Machine-collected vs operator assertion and policy sources. | Operator-only assertions must be visibly lower trust than live collection. |
| `command_provenance` | Commands, cwd, exit codes, and redacted summaries. | Required command failure blocks any field that depends on it. |

## Input Audit Rules

`--repo-status-clean` is an operator assertion, not a live Git check. It may
remain useful for a preview-only command, but it must be labeled as assertion
input and must not be upgraded into machine-collected status.

`--repo-status-json` should only be treated as stronger input when all of these
are true:

- the JSON is repo-local and path-normalized;
- the object declares `source_provenance.kind=machine_collected_live_repo_status`;
- command provenance includes the required Git and filesystem checks;
- authority docs and adapter policy sources are named;
- redaction has been applied to credential-like metadata and token-like values;
- no runtime report/log/needs-human artifact was created as a side effect.

If these requirements are not met, the operator surface may still display the
object for review, but future runner consumption must remain blocked.

## NLMYTGen Adapter Values

NLMYTGen is the reference host for this design. It is not the universal common
core.

The NLMYTGen adapter supplies:

- `repo_adapter_id=nlmytgen`;
- authority docs: `AGENTS.md`, `docs/REPO_LOCAL_RULES.md`,
  `docs/runtime-state.md`;
- known untracked allowlist: `.claude/worktrees/`,
  `samples/2026-05-16.ymmp`;
- runtime artifact paths: `.agent/reports/`, `.agent/logs/`,
  `.agent/needs_human.json`;
- execution policy source: `.agent/state.json`;
- adapter policy source: `.agent/repo_adapter.json`;
- forbidden automation domains from `.agent/repo_adapter.json`;
- repo-specific vocabulary that must not leak into common core.

NLMYTGen-specific terms such as YMM4, `.ymmp`, G-28, carrier,
diagnostic proof, rights status, production readiness, and visual proof stay in
adapter policy or NLMYTGen docs. They do not become common status object
requirements.

## Common Core / Repo Adapter Boundary

Common core owns:

- field names and JSON shape;
- observer mode vocabulary;
- command provenance shape;
- status normalization for branch, HEAD, upstream, tracked, staged, unstaged,
  and untracked state;
- fail-closed reason vocabulary;
- redaction requirements;
- timestamp/staleness handling;
- operator readback requirements;
- the rule that status input is not execution authority.

Repo adapter owns:

- expected repo root and adapter id;
- authority doc list;
- known untracked allowlist;
- allowed and blocked path policy;
- runtime artifact paths;
- execution policy source path;
- repo-specific forbidden domains;
- local artifact vocabulary;
- portability notes for other repos.

When porting to another repo, replace the adapter values first. Do not copy
NLMYTGen artifact terms into common core, and do not assume NLMYTGen known
untracked residue is safe elsewhere.

## Fail-Closed Conditions

The status object must produce a non-empty `fail_closed_reasons` list and a
non-consumable status for:

- remote divergence or missing upstream;
- unexpected tracked changes;
- unexpected untracked files outside adapter allowlist;
- staged diff when the slice expects no staged diff;
- runtime artifacts in `.agent/reports/` or `.agent/logs/` outside expected
  placeholders;
- unexpected `.agent/needs_human.json` presence;
- any real-runner consumption attempt while `codex_exec_enabled=false`;
- blocked paths or forbidden automation domains detected in policy or changed
  paths;
- credential-like metadata or token-like values detected before redaction;
- missing, unreadable, stale, or contradictory authority docs;
- repo root mismatch;
- command failure or unparsable command output for a required field;
- any status object path outside the repo.

Preview-only surfaces may show the failure details. They must not convert them
into permission to continue.

## Operator Surface Consumption

The operator Markdown card should render the status object as a review input:

- repo root, adapter id, observer mode, and timestamp;
- branch, HEAD, upstream, and remote parity;
- tracked-only porcelain status and full porcelain status;
- tracked/staged/unstaged dirty state;
- untracked allowlist match and unknown untracked entries;
- runtime report/log state and needs-human state;
- authority docs checked and any contradiction;
- execution policy snapshot, especially whether real execution is disabled;
- command provenance warnings or failures;
- fail-closed reasons;
- clear statement: "No runner was started by this status object.";
- next safe action, written as review guidance rather than execution authority.

The card may say that the next safe action is Hold, fix the status input, or
request a separately authorized implementation slice. It must not say that a
clean status object authorizes a real runner.

## Future Runner Consumption Boundary

This slice does not implement runner consumption.

A future runner consumption slice needs separate explicit authorization for at
least:

- a stdout-only live status producer implementation;
- tests or dry-run proof that the producer creates no `.agent/reports`,
  `.agent/logs`, or `.agent/needs_human.json`;
- repo-local path containment for any optional `--repo-status-json` file;
- schema validation for the status object;
- credential/token redaction tests;
- preflight logic that treats `codex_exec_enabled=false` as blocked or
  `needs_human` for real runner consumption;
- a human real-execution authority input separate from status cleanliness;
- notification policy review before any local stub or external notification is
  consumed;
- report path containment if a real runner is later authorized.

Until that separate authorization exists, status object consumption remains
preview/input review only.

## Minimal Example Shape

This example is a shape example, not a generated runtime artifact.

```json
{
  "schema_version": 1,
  "observer_mode": "docs_only",
  "observed_at": "2026-06-15T00:00:00+09:00",
  "repo_adapter_id": "nlmytgen",
  "branch": "master",
  "head_commit": {
    "short": "4746d81",
    "subject": "docs: design live repo status producer"
  },
  "upstream": {
    "ref": "origin/master",
    "state": "present"
  },
  "remote_parity": {
    "raw": "0\t0",
    "ahead": 0,
    "behind": 0,
    "in_sync": true
  },
  "porcelain_status_tracked": {
    "raw": "",
    "entries": []
  },
  "porcelain_status_all": {
    "raw": "?? .claude/worktrees/\n?? samples/2026-05-16.ymmp",
    "entries": [".claude/worktrees/", "samples/2026-05-16.ymmp"]
  },
  "known_untracked_matches_allowlist": {
    "all_untracked_known": true,
    "matched_entries": [".claude/worktrees/", "samples/2026-05-16.ymmp"],
    "unknown_entries": []
  },
  "dirty_state": {
    "tracked_dirty": false,
    "staged_dirty": false,
    "unstaged_tracked_dirty": false,
    "untracked_known_only": true
  },
  "staged_diff": {
    "entries": []
  },
  "unstaged_diff": {
    "entries": []
  },
  "runtime_artifact_state": {
    "reports_unexpected_entries": [],
    "logs_unexpected_entries": []
  },
  "needs_human_state": {
    "path": ".agent/needs_human.json",
    "present": false
  },
  "authority_docs_checked": [
    "AGENTS.md",
    "docs/REPO_LOCAL_RULES.md",
    "docs/runtime-state.md"
  ],
  "execution_policy_snapshot": {
    "source": ".agent/state.json",
    "codex_exec_enabled": false
  },
  "source_provenance": {
    "kind": "machine_collected_live_repo_status",
    "operator_assertion_used": false
  },
  "command_provenance": [],
  "fail_closed_reasons": []
}
```

## Closure

This design records the repo-status input audit contract only. The next safe
action is Hold, or a separately authorized stdout-only producer implementation
that proves it creates no runtime artifacts and still cannot grant real runner
permission.
