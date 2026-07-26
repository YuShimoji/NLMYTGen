# NLMYTGen Project Cockpit

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

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[FOOD_EXPIRY_SOURCE_PROJECT_PROMOTION_2026-07-26.md](verification/FOOD_EXPIRY_SOURCE_PROJECT_PROMOTION_2026-07-26.md)、
機械可読結果は
[FOOD_EXPIRY_SOURCE_PROJECT_PROMOTION_2026-07-26.json](verification/FOOD_EXPIRY_SOURCE_PROJECT_PROMOTION_2026-07-26.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

完了3件を再renderせず、food-expiryだけをexact source projectへ進めた。
queue-v2は次のrenderをplanするがexecution authorityを持たない。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Queue | successor `four_package_lifecycle_queue_v2` | original v1 exact |
| Live complete | 3 `verified_noop` | completed rerender 0 |
| Tracked-only complete | 3 `recorded_complete_no_live_file` | private missingはrerender理由でない |
| Food-expiry | `source_project_ready` | source live/receipt境界あり |
| Source project | Voice 4 / Reimu 4 / 22.25s | hash/readback exact |
| Render candidates | plan 1 | scheduled / execution set 0 |
| Idempotence | second + 2 runs `verified_noop` | YMM4/build launch 0 |
| Tests | focused 137/137 | drift / collision / corruption fail closed |
| Public authority | human / rights / production / public false | technical stateと分離 |

## 次の入口

explicit render authority後、queue-v2からfood-expiry 1件だけをrenderする。
exact source/content identityを保持し、generated project / MP4 / technical receiptを
append-only rendered successorへ束縛する。human/rights/public gateは分離する。

## 公開・実行境界

現在の成果はbounded four-package source-project evidenceである。generic distributed
scheduler、universal compatibility、production readiness、render、human acceptance、
rights、publication、upload、release、PR、merge、
master mutation、deployment、access change、public exposureは未実施・未承認。
