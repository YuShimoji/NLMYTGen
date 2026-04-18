# WORKFLOWS_AND_PHASES.md
Ruleset-Version: v18
Status: canonical

## Recommended read order on resume / continue / refresh

**注:** 以下は **resume / continue / refresh** 向け（`docs/ai` から入るサブセット）。**新規の再アンカリング・境界ルールの確認**は [AGENTS.md](../../AGENTS.md) の手順全体（`docs/REPO_LOCAL_RULES.md` を含む）を正とする。関係の整理は AGENTS の「Read order の関係（正本）」を参照。

1. `docs/ai/CORE_RULESET.md`
2. `docs/ai/DECISION_GATES.md`
3. `docs/ai/STATUS_AND_HANDOFF.md`
4. `docs/ai/WORKFLOWS_AND_PHASES.md`
5. `docs/INVARIANTS.md`
6. `docs/USER_REQUEST_LEDGER.md`
7. `docs/OPERATOR_WORKFLOW.md`
8. `docs/INTERACTION_NOTES.md`
9. runtime / context / registry / boundary docs

## Resume / Continue / Refresh
### Resume
Recover project-local canonical context first, then identify the active artifact and bottleneck.
If a prompt file, chat summary, or handoff note disagrees with `runtime-state` / `project-context` / `FEATURE_REGISTRY`, trust the repo docs.

### Continue
Do not rely on momentum. Re-check whether the current block still matches the bottleneck, actor, and value path.

### Refresh / Reanchor / Scan
これらは **user が当該 phase 名を明示宣言したブロック** でのみ read-only として扱う。assistant が自己発火させない。宣言済ブロック内では user が明示 mutation を依頼しない限り書き込みを避ける。
Do not auto-fill newly initialized project docs and commit them as “refresh work”.
Initialization may be prepared, but long-lived writes belong to an explicit write block.

## Prompt hygiene
- Resume prompts in `prompts/` are convenience entrypoints, not canonical state stores.
- Prompts must avoid embedding stale backlog status or outdated next steps when those belong in project docs.
- When a prompt and repo docs differ, update the prompt or ignore it; do not override repo docs with prompt text.

## Task-scout requirements
A scout pass should include, when relevant:
- active artifact and bottleneck
- stale evidence / visual evidence freshness
- user-carried constraints
- re-ask risk
- canonical coverage
- value path risk
- bottleneck substitution risk
- actor risk

## Manual verification pattern
- Put verification items in normal text, not inside the ask field.
- Ask only for `OK / NG` or a short result code.
- Ask for next direction separately.

## Option generation
Each major option should show:
- lane (`Advance`, `Audit`, `Excise`, `Unlock` or another justified lane)
- actor
- owner artifact
- bottleneck addressed
- what becomes possible if done

Avoid options whose main meaning is merely commit / not commit / cleanup only / end.

## Workflow-proof examples
Good workflow-proof tasks:
- validate that the human-authoring path runs once end-to-end
- confirm the operator can use the designed toolchain without improvising new steps
- move a verification target into a debug harness instead of using main content as the experiment bed

## Interaction safety
Do not compress unrelated intents into one ask.
Do not use markdown tables in a short ask field.
Do not present broad re-explanation prompts when canonical context already exists.

## Commit and push hygiene

### 次方向選択肢として single-commit 単独提示禁止
Commit/push は次方向の主選択肢にしない。「コミットするか否か」を options の軸にしない。strategy / frontier / bottleneck を軸に選ぶ。

### ブロック完了後の follow-through として commit を行う
正当化されたブロックが完了したあとは、follow-through として commit / push を行う。次方向を選ぶ段では主軸にしないが、ブロック内の仕上げ手順としては標準。
