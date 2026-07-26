# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-food-expiry-queue-rendered-v1
State-Revision: 2026-07-26.7
Updated: 2026-07-26 JST
Product-State: four-package-lifecycle-queue-with-v2-1-post-render-evidence-and-complete-noop-policy
Product-Gate: bounded-queue-execution-and-change-only-batch
Recommended-Next: add-bounded-queue-executor-that-runs-only-explicitly-authorized-change-set
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-food-expiry-queue-rendered-v1
Handoff-PR: none
Required-Base: f6c088a6c7f0af22f06b44a6a509743d6ff9cc3f
Implementation-Checkpoint: f6c088a6c7f0af22f06b44a6a509743d6ff9cc3f
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- queue-v2の唯一候補`food_expiry_labels_001`をexact authority
  `supervisor-food-expiry-single-render-2026-07-26`で`rendered`へ進めた。
- final runはignored `food_expiry_labels_internal_review_v4`。generated projectは
  Voice 4 / Image 4 / Reimu 4 / scene 1 / 1335 frames、source Voice semantic exact。
- MP4はSHA `95558d...daec`、28,023,236 bytes、H.264/AAC、
  1920x1080 / 60fps / 22.25秒。ISO-BMFF、full decode、7/7 distinct frames pass。
- cue_001..004を実画像検査し、exact subtitle、4 distinct crop mappings、
  black/missing/clipping/SVG proxy 0を確認した。
- v1 preflight、v2/v3 visual inspection failureは上書きせずignored evidenceへ保存。
  reusable-crop provenance、cue別materialization、accurate seekをcausal repairした。
- append-only rendered descriptor SHA `bcbafe...975f`、queue-v3 SHA
  `214d5e...927`。content identity `27165f...5c6`は前後同一。
- live queue-v3は4件`verified_noop`、candidate / scheduled / execution /
  blocked / invalid 0。tracked-onlyは4件`recorded_complete_no_live_file`、
  private artifact 0、automatic regeneration/render 0。
- 同一render requestは`verified_noop`、SHA/size/mtime mismatch 0、
  YMM4/render-driver/ffmpeg encode/output rewrite 0。

## Product Position

4 package queueはFactory Contract v2.1 post-render lifecycleを実証した。
live exact outputはcomplete no-op、private fileの無いtracked-only checkoutでも
recorded lifecycle identityを保持し、再生成を予定しない。

これはbounded four-package technical evidenceである。generic scheduler、
distributed worker pool、production readiness、human acceptance、rights/public
authorityを証明しない。

## Exact Next Action

queue evaluatorのplanとone-shot authority consumptionを使い、明示された
change-setだけを順番に実行するbounded queue executorを追加する。

開始条件:

- input queueと全descriptor identity exact
- explicit authorityがpackage ID、lifecycle edge、最大件数を限定
- default plan-only、completed packageはvalidation-only no-op
- collision、semantic drift、private absenceはfail closed
- execution後にauthorityを残さず、resumeとtracked-only portabilityを保持
- human/rights/production/public actionをexecutorへ含めない

## Residual Work

### Bounded queue executor

- Purpose: explicit change-setだけを既存advancement commandへ渡す。
- Effect: completed no-opを保持しつつ、authorized packageだけを逐次実行できる。
- Requirements: bounded batch authority、stable order、per-package receipt、
  stop-on-drift、no generic worker pool。
- State: queue planningとsingle-package executionは実証済み。batch loopは未実装。
- Owner: pipeline maintainer / supervising AI。
- Next move: maximum件数とexact package setを持つplan-only executorを薄く追加する。

### Creative and external gates

- Purpose: technical outputからcreative、rights、production、public判断を分離する。
- Effect: artifact SHAごとの人間判断とauthority clockを安全に記録できる。
- Requirements: independent human review、rights record、各owner authorization。
- State: Food Expiryはtechnical `rendered`。human decisionと全public clockはfalse。
- Owner: human reviewer / rights / production / publication owners。
- Next move: 各ownerが別missionでexact MP4 identityに判断を束縛する。

## Evidence and Re-entry

- Queue: `production_pilots/factory_queues/four_package_lifecycle_queue_v3.json`
- Descriptor:
  `production_pilots/factory_canaries/food_expiry_labels_001/factory_package_v2_1_rendered.json`
- Render readback:
  `production_pilots/factory_canaries/food_expiry_labels_001/render_readback.json`
- Report: `docs/verification/FOOD_EXPIRY_QUEUE_RENDER_2026-07-26.md`
- Machine receipt: `docs/verification/FOOD_EXPIRY_QUEUE_RENDER_2026-07-26.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file.
Restore with `uv sync --extra dev --locked`. Evaluate queue-v3 with
`evaluate-factory-queue --queue <descriptor> --check-live --format json`.

## Active Boundaries

- package_prepared、source_project_ready、queue-v1/v2、source project、prior topics、
  schemas、inventories、locks、ignored failed runs are immutable.
- Technical rendered evidence cannot grant human, rights, production, publication,
  upload, or release authority.
- Playback、system volume、Computer Use、SendKeys、manual YMM4、fifth topic、PR、
  merge、master mutation、deployment、publication、upload、releaseは未実施。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
