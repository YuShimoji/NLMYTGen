# NLMYTGen Project Cockpit

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

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[FOOD_EXPIRY_QUEUE_RENDER_2026-07-26.md](verification/FOOD_EXPIRY_QUEUE_RENDER_2026-07-26.md)、
機械可読結果は
[FOOD_EXPIRY_QUEUE_RENDER_2026-07-26.json](verification/FOOD_EXPIRY_QUEUE_RENDER_2026-07-26.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

queue-v2が選ぶFood Expiry一件をtechnical rendered lifecycleへ進め、
queue-v3は4 packageすべてをcomplete no-opとして扱う。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Queue | `four_package_lifecycle_queue_v3` | v1/v2 exact |
| Live packages | 4 `verified_noop` | render candidate 0 |
| Tracked-only | 4 `recorded_complete_no_live_file` | private absenceからrerenderしない |
| Food Expiry | v2.1 `rendered` | human accepted false |
| Final run | `food_expiry_labels_internal_review_v4` | v1-v3 failure evidence保存 |
| Project | Voice 4 / Image 4 / Reimu 4 / scene 1 | source Voice exact |
| MP4 | H.264/AAC / 1080p60 / 22.25s | full decode pass |
| Cue frames | 4/4 actual image pass | crop/subtitle/black failure 0 |
| Resume | `verified_noop` | launch/rewrite/mismatch 0 |
| Public authority | human / rights / production / public false | technical stateと分離 |

## 次の入口

exact package setと最大件数をauthorityへ束縛したplan-only bounded queue executorを
追加する。既存advancement commandを逐次呼び、completed no-opとstop-on-driftを
保持する。generic schedulerやworker poolへ拡張しない。

## 公開・実行境界

現在の成果はbounded four-package technical render evidenceである。human creative
acceptance、rights、production、publication、upload、release、PR、merge、
master mutation、deployment、access change、public exposureは未実施・未承認。
