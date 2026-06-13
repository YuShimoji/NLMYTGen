# Live Repo Status JSON Producer Design - 2026-06-13

This is a docs-only design slice for
`live_repo_status_json_producer_design_001`.

It defines the contract for a future machine-collected live repo status JSON
producer that can feed preflight, orchestrator preview, and operator review
surfaces. It does not implement a producer, does not run a real worker, and does
not create runtime artifacts.

## Purpose

The producer should replace a bare human assertion such as
`--repo-status-clean` with a structured, machine-collected status object.

The status object answers:

- which checkout was inspected
- which Git commands and filesystem checks produced the result
- whether branch, HEAD, upstream parity, dirty state, untracked state, runtime
  artifact state, and needs-human state are known
- which parts are repo-specific adapter policy rather than common-core policy
- whether the object is a usable preflight input candidate

It does not answer whether Codex may execute. It is evidence for preflight and
operator review only.

## Explicit Non-Goals

This slice does not:

- implement real `codex exec`
- add `subprocess.run`
- pipe prompt content to stdin
- create a runtime worker loop
- add external notification
- write `.agent/reports/`, `.agent/logs/`, or `.agent/needs_human.json`
- add a main/master auto-push path
- write repo-external files
- store API keys, tokens, or credentials
- touch G-28, G-27, Newsroom, ClipPipeGen, RSS, OPML, Inoreader, NotebookLM,
  `.ymmp`, render, rights, production, or publishing paths

## Producer Role

The future producer is an observer and serializer.

It may perform read-only Git and filesystem checks, then emit a JSON object. The
default future implementation should prefer stdout. If a later slice adds file
output for `--repo-status-json`, the path must be explicit, repo-local,
traversal-safe, and outside runtime report/log/needs-human paths unless a
separate artifact policy authorizes it.

The producer must not:

- grant execution permission
- set `safe_to_start_real_runner=true`
- modify `.agent/state.json`
- change adapter policy
- write reports, logs, notifications, or needs-human state
- treat a clean result as approval to start a runner

## Required Top-Level Fields

The future JSON should be a single object with these fields:

| Field | Meaning | Common core or adapter |
| --- | --- | --- |
| `schema_version` | Status JSON contract version. | Common core |
| `producer_id` | Stable producer name. | Common core |
| `adapter_id` | Repo adapter id, such as `nlmytgen`. | Adapter-selected value |
| `repo_root` | Absolute path inspected by the producer. | Common core field, adapter verifies expected root |
| `branch` | Current branch name. | Common core |
| `head_commit` | Current HEAD hash and optional subject. | Common core |
| `upstream_ref` | Resolved upstream ref, or explicit missing state. | Common core |
| `ahead_behind` | Left/right count and interpreted parity state. | Common core |
| `tracked_dirty` | Tracked working-tree changes. | Common core |
| `staged_dirty` | Staged changes. | Common core |
| `untracked_entries` | Untracked entries from live status. | Common core |
| `known_untracked_allowlist_match` | Match/unknown split against adapter allowlist. | Adapter policy applied to common field |
| `runtime_artifacts_state` | `.agent` runtime report/log/needs-human presence summary. | Common field, adapter supplies paths |
| `needs_human_present` | Whether the configured needs-human state file exists. | Common field, adapter supplies path |
| `inspected_paths` | Repo-relative or absolute paths inspected. | Common core |
| `commands_used` | Command provenance with exit codes and redacted summaries. | Common core |
| `generated_at` | Timestamp when collection completed. | Common core |
| `source_provenance` | Machine-collected vs human assertion and policy sources. | Common core |
| `confidence` | Trust level and reason list. | Common core |
| `status` | `collected`, `needs_human`, or `blocked`. | Common core |
| `reasons` | Stable reason strings for operator/preflight use. | Common core |

Use `collected` instead of `pass`; a repo status object is an input candidate,
not an approval result.

## Field Contract

### `repo_root`

Must be the resolved absolute checkout path. If it does not match the expected
repo root passed by the orchestrator or adapter, the producer result is
`blocked`.

### `branch`

Must be a parsed branch name. Missing, detached, empty, or parse failure is
`needs_human` for preview and must block any future real-runner preflight.

### `head_commit`

Should include at least:

```json
{
  "short": "66be70d",
  "full": "optional full hash if collected",
  "subject": "docs: add G-28 chat-first review protocol"
}
```

Missing or unparsable HEAD is `blocked`.

### `upstream_ref` and `ahead_behind`

`upstream_ref` should be the resolved upstream, such as `origin/master`, or a
structured missing state. `ahead_behind` should preserve both raw and parsed
values:

```json
{
  "raw": "0\t0",
  "ahead": 0,
  "behind": 0,
  "in_sync": true
}
```

Missing upstream, command failure, or parse failure is not pass. It is
`needs_human` for preview and blocks future real execution.

### `tracked_dirty` and `staged_dirty`

Each field should include both a boolean and the file list:

```json
{
  "present": false,
  "entries": []
}
```

Tracked or staged entries produce `needs_human` in the status object. A future
real-runner preflight must treat them as blocking.

### `untracked_entries`

This should preserve the raw untracked entries as repo-relative paths, normalized
with forward slashes for matching. It should not hide unknown entries.

### `known_untracked_allowlist_match`

The producer applies the adapter allowlist to `untracked_entries` and reports:

```json
{
  "source": ".agent/repo_adapter.json#known_untracked_allowlist",
  "all_untracked_known": true,
  "matched_entries": [".claude/worktrees/", "samples/2026-05-16.ymmp"],
  "unknown_entries": []
}
```

Unknown untracked entries produce `needs_human`. A future real-runner preflight
must block until the entry is removed, ignored by repo policy, or explicitly
allowlisted by the adapter in a separate authorized change.

### `runtime_artifacts_state`

The producer should inspect the adapter-configured runtime artifact paths. For
NLMYTGen, those paths are:

- `.agent/reports/`
- `.agent/logs/`
- `.agent/needs_human.json`

The state should distinguish tracked placeholders from runtime residue:

```json
{
  "reports_dir": {
    "path": ".agent/reports",
    "expected_only": [".gitkeep"],
    "unexpected_entries": []
  },
  "logs_dir": {
    "path": ".agent/logs",
    "expected_only": [".gitkeep"],
    "unexpected_entries": []
  },
  "needs_human": {
    "path": ".agent/needs_human.json",
    "present": false
  }
}
```

Unexpected runtime reports, logs, or needs-human state produce `needs_human`.
This does not delete or clean anything.

### `commands_used`

Each command entry should record provenance without leaking raw secrets:

```json
{
  "label": "upstream_parity",
  "argv": ["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"],
  "cwd": "C:/Users/thank/Storage/Media Contents Projects/NLMYTGen",
  "exit_code": 0,
  "stdout_summary": "0\t0",
  "stderr_summary": "",
  "started_at": "2026-06-13T00:00:00+09:00",
  "ended_at": "2026-06-13T00:00:00+09:00"
}
```

Command failure is `blocked` if it prevents parsing a required field. Non-empty
stderr with exit code 0 should be surfaced in `confidence.reasons`; the producer
must not silently discard it.

### `source_provenance`

The producer must say how the object was made:

```json
{
  "kind": "machine_collected_live_repo_status",
  "adapter_source": ".agent/repo_adapter.json",
  "state_source": ".agent/state.json",
  "operator_assertion_used": false
}
```

A human assertion such as `--repo-status-clean` is not equivalent to a live
status JSON object. If a future compatibility path converts such an assertion
into JSON, `source_provenance.kind` must say `operator_assertion`, and
`confidence.level` must not be `high`.

### `confidence`

Use a small vocabulary:

- `high`: required commands and filesystem checks succeeded and parsed.
- `degraded`: required fields parsed but warnings or stale/partial metadata are
  present.
- `blocked`: one or more required fields are missing, untrusted, failed, or
  unparsable.

High confidence means "usable as preflight input evidence"; it does not mean
safe to run a real worker.

## Suggested JSON Shape

```json
{
  "schema_version": 1,
  "producer_id": "live_repo_status_json_producer",
  "adapter_id": "nlmytgen",
  "repo_root": "C:/Users/thank/Storage/Media Contents Projects/NLMYTGen",
  "branch": "master",
  "head_commit": {
    "short": "66be70d",
    "full": "",
    "subject": "docs: add G-28 chat-first review protocol"
  },
  "upstream_ref": "origin/master",
  "ahead_behind": {
    "raw": "0\t0",
    "ahead": 0,
    "behind": 0,
    "in_sync": true
  },
  "tracked_dirty": {
    "present": false,
    "entries": []
  },
  "staged_dirty": {
    "present": false,
    "entries": []
  },
  "untracked_entries": [
    ".claude/worktrees/",
    "samples/2026-05-16.ymmp"
  ],
  "known_untracked_allowlist_match": {
    "source": ".agent/repo_adapter.json#known_untracked_allowlist",
    "all_untracked_known": true,
    "matched_entries": [
      ".claude/worktrees/",
      "samples/2026-05-16.ymmp"
    ],
    "unknown_entries": []
  },
  "runtime_artifacts_state": {
    "reports_dir": {
      "path": ".agent/reports",
      "expected_only": [".gitkeep"],
      "unexpected_entries": []
    },
    "logs_dir": {
      "path": ".agent/logs",
      "expected_only": [".gitkeep"],
      "unexpected_entries": []
    },
    "needs_human": {
      "path": ".agent/needs_human.json",
      "present": false
    }
  },
  "needs_human_present": false,
  "inspected_paths": [
    ".git",
    ".agent/repo_adapter.json",
    ".agent/state.json",
    ".agent/reports",
    ".agent/logs",
    ".agent/needs_human.json"
  ],
  "commands_used": [],
  "generated_at": "2026-06-13T00:00:00+09:00",
  "source_provenance": {
    "kind": "machine_collected_live_repo_status",
    "adapter_source": ".agent/repo_adapter.json",
    "state_source": ".agent/state.json",
    "operator_assertion_used": false
  },
  "confidence": {
    "level": "high",
    "reasons": []
  },
  "status": "collected",
  "reasons": []
}
```

The example above is a shape example, not a generated runtime artifact.

## Fail-Closed Semantics

The producer result must not silently pass these cases:

| Condition | Producer status | Future real-runner preflight |
| --- | --- | --- |
| Required command exits nonzero | `blocked` | Block |
| Required output missing or unparsable | `blocked` | Block |
| Repo root mismatch or repo-external path | `blocked` | Block |
| Missing upstream | `needs_human` | Block |
| Tracked dirty files | `needs_human` | Block |
| Staged files | `needs_human` | Block |
| Unknown untracked entries | `needs_human` | Block |
| Unexpected runtime reports/logs | `needs_human` | Block until reviewed |
| `.agent/needs_human.json` present | `needs_human` | Block until reviewed |
| Credential-like value in command metadata | `blocked` or redacted `needs_human` | Block |
| Stale `generated_at` beyond future threshold | `needs_human` | Block |

Preview flows may render `needs_human` status for review. They must not turn it
into runner permission.

## Common Core / Repo Adapter Boundary

Common core owns:

- status JSON schema contract
- field names and result status vocabulary
- fail-closed semantics
- command provenance shape
- redaction rules for credential-like values
- generated timestamp and staleness signaling
- operator readback fields
- no-execution guarantee

Repo adapter owns:

- adapter id
- expected authority docs
- known untracked allowlist
- allowed and blocked paths
- runtime artifact paths
- repo-specific artifact vocabulary
- forbidden automation domains
- mainline resume boundary

NLMYTGen-specific terms such as YMM4, `.ymmp`, G-28, carrier,
`rights_status`, `production_candidate`, diagnostic proof, and visual proof must
stay in the adapter or repo docs. The common core must not require or understand
those terms.

## Operator Surface Mapping

The operator card should eventually show the status object in plain language:

- repo root and adapter id
- branch and HEAD
- upstream parity
- tracked and staged dirty state
- untracked entries and allowlist match result
- runtime artifact state
- needs-human presence
- generated timestamp
- source provenance
- command warnings or failures
- confidence level and reasons
- explicit statement that this status object did not start a runner

If `source_provenance.kind` is `operator_assertion`, the card should label it as
lower trust than machine-collected live status.

## Preflight Consumption Boundary

Preflight may consume this object as evidence. It may derive its own
`safe_to_start_real_runner` only in a separate, explicitly authorized future
runner slice.

The producer itself must not output `safe_to_start_real_runner=true`. If a
compatibility field is ever needed, it must be absent, `false`, or `null`, and
the card must say the field is not execution permission.

## Current Slice Closure

This slice defines the design contract only. The next safe implementation entry,
if separately authorized, is a producer that prints this JSON to stdout and
proves it does not create `.agent/reports`, `.agent/logs`, or
`.agent/needs_human.json`.

Real runner implementation remains closed.
