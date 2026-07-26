# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-factory-contract-v2-1-prerender-out-of-sample-validated-v1
State-Revision: 2026-07-26.4
Updated: 2026-07-26 JST
Product-State: lifecycle-aware-factory-contract-with-real-prerender-out-of-sample-package
Product-Gate: bounded-multi-episode-queue-and-render-on-change-policy
Recommended-Next: build-queue-over-v2-lifecycle-without-rerendering-complete-packages
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-factory-contract-v2-lifecycle-v1
Handoff-PR: none
Required-Base: ab960978ab1c29fc8ea5d59d69dc185ddc0d257a
Implementation-Checkpoint: ab960978ab1c29fc8ea5d59d69dc185ddc0d257a
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- Factory Contract v2を後方互換v2.1へ拡張した。
  `package_prepared`、`source_project_ready`、`rendered`、
  `human_accepted`の4 lifecycleを明示する。
- v2.1 schema / inventoryはgenerated project、render evidence、human decisionを
  lifecycle条件付きにし、存在しない証拠のdummy objectを許容しない。
- v2.0 schema / inventory / 3 descriptorsはbyte exact。read-only normalizerで
  new-banknoteを`human_accepted`、REINSとAI-monitoringを`rendered`へ写像する。
- fixed fourth topic「賞味期限と消費期限の違い」をtracked
  `package_prepared` packageとして追加した。
- fourth shapeは4 cues、1 scene、霊夢4、official source 2、real raster 2、
  4/4 media mapping、同一assetの異なるcrop再利用、planned 24.0秒。
- source projectはplanned / absent。generated project、render receipt、MP4、
  human decisionはabsent。rights / production / publication / upload /
  releaseはfalse。
- live profileはraster 2/2 exact。tracked-only profileはv2.1 1/1とv2.0
  3/3 passし、ignored rasterは`receipt_only_no_live_file`。
- descriptor / normalized / content identityは2 repeatでexact。
- existing CLIのpre-render planは`source_project_generation`前に正常停止。
  YMM4 / Electron / render driver / ffmpeg encode / playback / volume / writeは0。
- focused Pythonはv2.1 23/23、v2.0 24/24、episode込み66/66 pass。

## Product Position

実在するsource / claims / media provenanceを持つpre-render packageを、
render evidenceを捏造せずversioned contractへ入れられる。observed 3 completed
packagesは変更せず同じlifecycle viewから扱える。

これはfourth topicの`package_prepared` out-of-sample evidenceである。
post-render lifecycle fit、universal arbitrary-topic compatibility、
human acceptance、rights、production、publication、upload、releaseは未証明・
未承認である。

## Exact Next Action

v2.0 / v2.1 packageを混在して読むbounded multi-episode queueを作る。
normalized lifecycleとcontent identityから必要な次stageだけを返し、
`rendered` / `human_accepted` packageを再render対象にしない。

開始条件:

- bounded input、stable ordering、duplicate identity rejection
- planning phaseはread-only、YMM4 / Electron / render / playback 0
- `package_prepared`と`source_project_ready`だけを未完了候補にする
- run-local差を除外しsemantic driftをfail closedにする
- owner許可前はsource-project generationとrenderを行わない
- fourth packageを進める場合も同じcontent identityを保持する

## Residual Work

`FACTORY_CONTRACT_POST_RENDER_LIFECYCLE_OVERFIT`

- Purpose: 同じfourth packageが後続lifecycleでもidentityを保つか確認する。
- Effect: 現在利用できる範囲はqueue intake / pre-render planningまで。
- Requirements: owner許可、exact project / render evidence、独立human decision。
- State: open。今回の正常停止点は`package_prepared`。
- Owner: production owner / human reviewer / rights and public authority owners。
- Next move: queueとrender-on-change decision layerを先に実装する。

## Evidence and Re-entry

- Schema: `schemas/factory_contract_v2_1/factory_package_v2_1.schema.json`
- Inventory: `schemas/factory_contract_v2_1/field_inventory.json`
- Validator: `src/pipeline/factory_contract_v2_1.py`
- Fourth descriptor:
  `production_pilots/factory_canaries/food_expiry_labels_001/factory_package_v2_1.json`
- Report:
  `docs/verification/FACTORY_CONTRACT_V2_1_LIFECYCLE_VALIDATION_2026-07-26.md`
- Machine receipt:
  `docs/verification/FACTORY_CONTRACT_V2_1_LIFECYCLE_VALIDATION_2026-07-26.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
Restore with `uv sync --extra dev --locked`. Validate the fourth descriptor with
`validate-factory-package --require-lifecycle package_prepared --check-live`;
the tracked contract also passes when ignored media is absent.

## Active Boundaries

- v2.0 schema、inventory、descriptors、prior rendered artifacts remain immutable.
- A receipt proves recorded identity; it does not prove current live availability.
- Technical lifecycle state cannot grant human, rights, production, or public clocks.
- GUI、YMM4、source-project generation、render、playback、fifth topic、PR、merge、
  master mutation、deployment、publication、upload、release、access change、
  public exposure were not performed.

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
