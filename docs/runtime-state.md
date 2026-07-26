# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-bounded-factory-queue-render-on-change-validated-v1
State-Revision: 2026-07-26.5
Updated: 2026-07-26 JST
Product-State: lifecycle-aware-four-package-queue-with-complete-package-no-rerender-policy
Product-Gate: advance-prepared-package-to-source-project-ready
Recommended-Next: advance-food-expiry-package-to-source-project-ready-through-queue
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-bounded-factory-queue-v1
Handoff-PR: none
Required-Base: 88db8b84e8863aed366fd1683ddcfcc548a0b2a6
Implementation-Checkpoint: 88db8b84e8863aed366fd1683ddcfcc548a0b2a6
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- `nlmytgen.factory_queue.v1`とhard maximum 32を追加した。実queueは
  explicit maximum 4、4 entries、priority-descending / order-ascendingで安定する。
- queue entryはrepo-relative descriptor、expected package / content /
  render-settings / completed-output identityを保持する。
- mixed v2.0 / v2.1を同じlifecycle-aware validatorでnormalizeする。
- duplicate package ID、unmarked duplicate content、target collision、
  private/absolute path、unknown version、unstable orderをfail closedにする。
- pure render-on-change policyはrun-local fieldsを除外し、technical decision、
  live availability、recorded identity、semantic drift、owner authorityを分離する。
- live queueではnew-banknote / REINS / AI-monitoringが`verified_noop`、
  food-expiryだけが`source_project_generation_required`。
- live countsはno-op 3、source-project candidate 1、render candidate 0、
  blocked / invalid 0、render schedule / execution set 0。
- tracked-onlyでは完了3件が`recorded_complete_no_live_file`。
  private output不在から`render_required`を推論しない。
- safe-stage modeはexisting dry-run 3、pre-render plan 1、identity 4/4 exact。
  YMM4 / Electron / render / encode / playback / volume / product writeは0。
- deterministic live / tracked-only / safe-stageは各2 runs raw exact。
- queue固有31/31、v2.0 / v2.1 / queue / episode focused 97/97 pass。

## Product Position

4 package queueは実行可能なread-only planning surfaceである。completed packageは
live exactなら`verified_noop`、live fileが別端末で無ければ
`recorded_complete_no_live_file`となり、automatic rerender対象にならない。

food-expiryは唯一のsource-project candidateだが、technical next stageと
execution authorityは別である。今回のqueueはsource-project generationやrenderの
権限を持たない。

これはbounded four-package compatibilityである。generic distributed scheduler、
universal scheduling compatibility、production readinessを証明しない。

## Exact Next Action

ownerの明示許可後、queueで選ばれたfood-expiry 1件だけを同じcontent identityから
source projectへmaterializeし、exact repository-relative locator / SHAを追加して
`source_project_ready`へ進める。

開始条件:

- queue evaluationが4 contracts valid、source candidate 1、render candidate 0
- new-banknote / REINS / AI-monitoringはno-opのまま
- content / render-settings / queue baseline identity exact
- source-project generation authorityを1 packageへ明示
- YMM4 render、playback、public actionはまだ行わない
- semantic drift時は既存artifactを変更せず停止する

## Residual Work

### Food-expiry source-project promotion

- Purpose: prepared packageを最初の実materialization stageへ進める。
- Effect: queue decisionを`source_project_generation_required`から
  `render_required` planへ進められる。
- Requirements: owner許可、同じcontent identity、exact project readback / SHA。
- State: ready for separately authorized execution。
- Owner: production operator。
- Next move: food-expiry 1件だけをsource-project-readyへ進める。

### Post-render and external gates

- Purpose: rendered / accepted lifecycleとpublic authorityを実証する。
- Effect: technical render validity、human decision、rights/public clocksを分離できる。
- Requirements: render許可、exact render receipt、human review、各owner record。
- State: open。`FACTORY_CONTRACT_POST_RENDER_LIFECYCLE_OVERFIT` remains。
- Owner: production owner / human reviewer / rights and public authority owners。
- Next move: source-project gate完了後に別missionで判断する。

## Evidence and Re-entry

- Queue schema: `schemas/factory_queue_v1/factory_queue_v1.schema.json`
- Queue engine: `src/pipeline/factory_queue.py`
- Queue descriptor:
  `production_pilots/factory_queues/four_package_lifecycle_queue_v1.json`
- Report:
  `docs/verification/BOUNDED_FACTORY_QUEUE_VALIDATION_2026-07-26.md`
- Machine receipt:
  `docs/verification/BOUNDED_FACTORY_QUEUE_VALIDATION_2026-07-26.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
Restore with `uv sync --extra dev --locked`. Evaluate with
`evaluate-factory-queue --queue <descriptor> --check-live --format json`.

## Active Boundaries

- Existing v2.0 / v2.1 schemas, descriptors, manifests, projects, MP4s,
  receipts, decisions, media, run directories, locks, and ignored evidence are immutable.
- Receipt-only completion is historical identity evidence, not live availability.
- Technical next stage cannot grant execution, human, rights, production, or public authority.
- Source-project generation、YMM4、Electron、render、encode、playback、fifth topic、
  PR、merge、master mutation、deployment、publication、upload、release、
  access change、public exposure were not performed.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
