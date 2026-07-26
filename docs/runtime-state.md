# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-food-expiry-source-project-ready-v1
State-Revision: 2026-07-26.6
Updated: 2026-07-26 JST
Product-State: four-package-queue-with-single-prepared-package-promoted-to-source-project-ready
Product-Gate: authorize-food-expiry-single-render
Recommended-Next: render-food-expiry-only-through-queue-after-explicit-render-authority
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-food-expiry-source-project-ready-v1
Handoff-PR: none
Required-Base: 7c9ee4a9879e855911434b72105c04bb216d7088
Implementation-Checkpoint: 7c9ee4a9879e855911434b72105c04bb216d7088
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- `advance-factory-package`はplan-onlyが既定で、queue唯一候補、exact package、
  lifecycle、authority ID、predecessor/content/CSV/shape identityを検査してからだけ
  source-project generationを許可する。
- food-expiry source projectはpackage-local ignored locatorに1件存在する。
  SHA `4f8dc1...bdbf`、449,804 bytes、VoiceItems 4、霊夢4、1 scene、
  1335 frames / 60fps / 22.25秒、canonical text/order 4/4 exact。
- ToolStates、LayoutXml、private absolute path、unrelated project itemは0。
  YMM4 `4.54.0.1`。2 attempts中1 success、repairable UIA failure 1、
  owned process residue 0。
- package-prepared descriptorとqueue-v1はbyte-exact。successor descriptorと
  queue-v2はappend-onlyで、content identity `27165f...5c6`を保持する。
- live queue-v2はcompleted 3件`verified_noop`、food-expiry
  `source_project_live_exact` / `render_required`。render candidate 1はplanのみで、
  scheduled / execution set / blocked / invalidは0。
- tracked-onlyはcompleted 3件`recorded_complete_no_live_file`、food-expiry
  `source_project_recorded_only` / `render_required`。private absenceからdemotion、
  regeneration、render executionを推論しない。
- 同一promotionは`verified_noop`、YMM4/build launch 0、project SHA/size/mtime、
  successor descriptor不変。追加2 runsもtracked/local identities exact。
- focused 137/137、dotnet 0 warning / 0 error。

## Product Position

4 package queueはsource-project lifecycleまで進んだ。completed packageは
live exactなら`verified_noop`、別端末でprivate fileが無ければ
`recorded_complete_no_live_file`となり、automatic rerender対象にならない。

food-expiryのtechnical next stageはrenderだが、queue-v2はexecution authorityを
持たない。source-project readinessはrender、human、rights、public authorityを
付与しない。

これはbounded four-package compatibilityである。generic distributed scheduler、
universal scheduling compatibility、production readinessを証明しない。

## Exact Next Action

別missionのexplicit render authority後、queue-v2でfood-expiry 1件だけをrenderし、
generated project、technical render receipt、MP4 identityを
`rendered` successorへappend-onlyで記録する。

開始条件:

- queue-v2 evaluationが4 contracts valid、source candidate 0、render candidate 1
- new-banknote / REINS / AI-monitoringはno-opのまま
- source project / content / render-settings / queue baseline identity exact
- render authorityをfood-expiry 1 packageへ明示
- playback、human decision、rights/public actionはまだ行わない
- semantic drift時は既存artifactを変更せず停止する

## Residual Work

### Food-expiry single render

- Purpose: exact source projectをtechnical rendered lifecycleへ進める。
- Effect: generated project / MP4 / technical receiptをexact identityへ束縛する。
- Requirements: separate render authority、queue-v2 live exact、silent policy。
- State: plan-only candidate。execution authority false。
- Owner: production operator。
- Next move: food-expiry 1件だけをqueue経由でrenderする。

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
  `production_pilots/factory_queues/four_package_lifecycle_queue_v2.json`
- Report:
  `docs/verification/FOOD_EXPIRY_SOURCE_PROJECT_PROMOTION_2026-07-26.md`
- Machine receipt:
  `docs/verification/FOOD_EXPIRY_SOURCE_PROJECT_PROMOTION_2026-07-26.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
Restore with `uv sync --extra dev --locked`. Evaluate with
`evaluate-factory-queue --queue <descriptor> --check-live --format json`.

## Active Boundaries

- Existing v2.0 / v2.1 schemas, descriptors, manifests, projects, MP4s,
  receipts, decisions, media, run directories, locks, and ignored evidence are immutable.
- Receipt-only completion is historical identity evidence, not live availability.
- Technical next stage cannot grant execution, human, rights, production, or public authority.
- Source-project generationだけをexplicit authorityで実施した。render、
  generated project、MP4、encode、playback、human decision、fifth topic、PR、
  merge、master mutation、deployment、publication、upload、release、access change、
  public exposureは未実施。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
