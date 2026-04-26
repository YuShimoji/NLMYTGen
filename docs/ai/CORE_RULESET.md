# CORE_RULESET.md
Ruleset-Version: v20
Status: canonical
Audience: Claude Code, Codex, and any adapter that reads project-local AI rules.

## Purpose
This ruleset exists to keep a single vendor-neutral source of truth for AI-assisted development.
Adapters such as `AGENTS.md` and `.claude/CLAUDE.md` (pointer) must stay thin. Repo-local operational rules (Hard Rules, read order, checklists) are canonical in `docs/REPO_LOCAL_RULES.md`. Vendor-neutral rules defer to `docs/ai/*.md` (this file set).

## Source-of-truth policy
- Vendor-neutral canonical rules live in `docs/ai/*.md`.
- Repo-local operational enforcement (Hard Rules, block-start checklist, read order for agents) lives in `docs/REPO_LOCAL_RULES.md`.
- Adapters, prompts, hooks, and helper agents are subordinate.
- Project-local canonical docs (`INVARIANTS`, `USER_REQUEST_LEDGER`, `OPERATOR_WORKFLOW`, `INTERACTION_NOTES`) are factual project memory, not optional decoration.
- If a rule conflicts with project-local canonical docs, first verify whether the docs reflect newer explicit user instruction.

## Core principles
### Artifact-first
Advance the active artifact or its verified delivery path. Docs, cleanup, tests, mocks, and surveys are supporting work unless they clearly unblock the artifact.

### Explain Once Canonicalization
If the user states a durable constraint, workflow pain, invariant, backlog item, or prohibited shortcut, write it into the appropriate canonical doc in the same block. Do not postpone that write to handoff.

### Question Dedup
Before asking, read the relevant canonical rule or project-local canonical section needed for the current decision. Do not expand this into a full-corpus read by default. Summarize what is already known, then ask only for missing deltas. Do not ask the user to re-explain known context.

### Frontier discipline
Do not re-open rejected, boundary-stopped, or quarantined frontiers as normal next steps. User interest in “looking again” is not automatic approval.

### Selection is not approval
If the user chooses a proposed item for deeper review, that means “evaluate/specify this next”, not “approve implementation”. Keep status semantics strict.

### No pendulum compensation
Do not choose work because the previous sessions were “too much X” and therefore the next one should be “not-X”. Choose work based on the current bottleneck.

### Actor/owner discipline
Every major action has an actor and an owner artifact.
- actor = who performs the work now (`user`, `assistant`, `tool`, `shared`)
- owner = who owns the resulting artifact or judgment
Do not silently slide human-owned creative work into assistant execution.

### Read-only audit phases
REFRESH / REANCHOR / SCAN / AUDIT は、**user が現ブロック冒頭で当該 phase 名を明示宣言した場合に限り** read-only として扱う。assistant が自己判断で「これは REFRESH 相当」と解釈して自己発火させない。user 宣言済みブロック内では long-lived repo files への書き込み・commit・push を禁止する。ただし同一ブロック内で user が明示的に mutation を依頼した場合は、その依頼範囲に限り例外。

### Write failure hard stop
If a write fails, a readback mismatch occurs, or the result is uncertain, do not commit, push, or claim completion in that block. Repair or clearly stop.

## Canonical doc roles
- `INVARIANTS.md`: non-negotiables, UX/algorithm invariants, role boundaries, prohibited shortcuts
- `USER_REQUEST_LEDGER.md`: durable requests, backlog deltas, unresolved user corrections
- `OPERATOR_WORKFLOW.md`: human/operator workflow, pain points, quality goals, manual vs assisted steps
- `INTERACTION_NOTES.md`: reporting style, ask hygiene, interaction failure patterns, manual verification conventions

## Evidence discipline
Use visual or artifact evidence whenever relevant. If evidence is stale or unknown, say so. Do not substitute documentation for actual observation when the question is about behavior.

## Terminology and naming discipline

### ペア形式ルール
略称（S-n、L-n、機能ID等）を使うときは、常に `ID（説明名）` のペア形式で書く。裸の略称を禁止する。

- 工程: `S-3（CSV変換工程）` — 裸の `S-3` は不可
- レイヤー: `L2（Python変換工程）` — 裸の `L2` は不可
- 機能ID: セクション内の初出で `B-12（行バランス字幕分割）` と書き、同セクション内の2回目以降は裸でも可

### 二語彙ルール
本プロジェクトには2つの独立した座標系がある。混同しない。

- **L1-L4**: 動画制作パイプライン上の位置（どこで動くか）。正本: `docs/AUTOMATION_BOUNDARY.md`
  - L1（入力取得）/ L2（Python変換）/ L3（YMM4内部）/ L4（配信）
- **第1層-第3層（三層責務構造）**: IR設計の責務分担（誰が設計を持つか）。正本: `PRODUCTION_IR_SPEC.md` セクション6
  - 第1層（Writer IR）/ 第2層（Template Registry）/ 第3層（YMM4 Adapter）

L2（Python変換工程）が停滞すると CSV も IR も生成できず、S-3（CSV変換）以降の全工程が止まる。
第2層（Template Registry）が停滞すると演出自動配置（face/bg）が止まるが、基本的な動画制作（手動演出）は続行できる。

### 因果関係の明示
工程やレイヤーに言及するときは、「進めると何が実現されるか / 止まると何が詰まるか」を可能な限り併記する。
グロサリーの正本は `CLAUDE.md`（プロジェクトルート）の「工程・レイヤー略語の読み方」表。

### 適用範囲
- 適用する: 生きているドキュメント（CLAUDE.md、CORE_RULESET.md、OPERATOR_WORKFLOW.md、GUI_MINIMUM_PATH.md、AUTOMATION_BOUNDARY.md、runtime-state.md）
- 適用しない: docs/verification/* の過去証跡、git 履歴、日付入りジャーナル（ただし今後の追記にはペア形式を適用）
