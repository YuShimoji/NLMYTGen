# NLMYTGen Project Cockpit

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

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[BOUNDED_FACTORY_QUEUE_VALIDATION_2026-07-26.md](verification/BOUNDED_FACTORY_QUEUE_VALIDATION_2026-07-26.md)、
機械可読結果は
[BOUNDED_FACTORY_QUEUE_VALIDATION_2026-07-26.json](verification/BOUNDED_FACTORY_QUEUE_VALIDATION_2026-07-26.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

mixed v2.0 / v2.1の4 packageを一度に評価し、完了3件を再renderせず、
food-expiryだけを次のsource-project候補として返すbounded queueが動く。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Queue | `nlmytgen.factory_queue.v1` | declared 4 / hard max 32 |
| Ordering | priority desc / explicit order asc | 2 runs raw exact |
| Live complete | 3 `verified_noop` | render schedule 0 |
| Tracked-only complete | 3 `recorded_complete_no_live_file` | missingはrerender理由でない |
| Food-expiry | `source_project_generation_required` | authority false |
| Render candidates | 0 | execution set 0 |
| Safe stages | dry-run 3 / pre-render plan 1 | launch / write 0 |
| Tests | queue 31/31、combined 97/97 | drift / corruption fail closed |
| Public authority | human / rights / production / public false | technical stateと分離 |

## 次の入口

新しいtopicやqueue設計を追加せず、ownerが明示許可したfood-expiry 1件だけを
同じcontent identityでsource-project-readyへ進める。source projectのexact
locator / SHAとreadbackを追加し、renderは別gateに残す。

## 公開・実行境界

現在の成果はbounded four-package planning evidenceである。generic distributed
scheduler、universal compatibility、production readiness、source-project generation、
render、human acceptance、rights、publication、upload、release、PR、merge、
master mutation、deployment、access change、public exposureは未実施・未承認。
