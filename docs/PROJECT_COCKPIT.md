# NLMYTGen Project Cockpit

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

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[FACTORY_CONTRACT_V2_1_LIFECYCLE_VALIDATION_2026-07-26.md](verification/FACTORY_CONTRACT_V2_1_LIFECYCLE_VALIDATION_2026-07-26.md)、
機械可読結果は
[FACTORY_CONTRACT_V2_1_LIFECYCLE_VALIDATION_2026-07-26.json](verification/FACTORY_CONTRACT_V2_1_LIFECYCLE_VALIDATION_2026-07-26.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

Factory Contract v2.1が4 lifecycleを区別し、実在する第四トピックを
render evidenceなしの`package_prepared`としてlive / tracked-onlyの両方で
検証できる。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Contract | `nlmytgen.factory_package.v2.1` | v2.0 bytes exact |
| Lifecycle | prepared → source-ready → rendered → accepted | evidenceは条件付き |
| Fourth package | 4 cues / 1 scene / 霊夢4 | `package_prepared`限定 |
| Sources / media | official 2 / raster 2 / mapping 4 | rights approvalなし |
| Live | raster 2/2 exact | availability clock |
| Tracked-only | v2.1 1/1、v2.0 3/3 pass | rasterはreceipt-only |
| Determinism | descriptor / normalized / content 2 repeats exact | run-local除外 |
| Pre-render plan | source-project生成前に正常停止 | launch / write 0 |
| Tests | focused Python 66/66 | lifecycle negative coverage |
| Public authority | five clocks false | technical passから継承しない |

## 次の入口

v2.0 / v2.1を混在して読むbounded queueとrender-on-change decisionを作る。
`rendered` / `human_accepted` packageはverified no-opにし、未完了packageだけへ
必要な次stageを返す。source-project generationとrenderはownerの別許可を待つ。

## 公開・実行境界

現在の成果はbounded pre-render lifecycle evidenceである。post-render fourth-topic
fit、universal compatibility、human acceptance、rights、production、publication、
upload、release、PR、merge、master mutation、deployment、access change、
public exposureは未承認・未実施。
