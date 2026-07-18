# NLMYTGen Project Cockpit

Project-State-ID: new-banknote-successor-integration-audited-selective-ready-v1
State-Revision: 2026-07-19.2
Updated: 2026-07-19 JST
Product-State: new-banknote-successor-integration-audited-selective-ready
Product-Gate: new-banknote-successor-selective-integration
Recommended-Next: integrate-audited-new-banknote-successor-artifacts
External-State: public-repo-feature-branch
Handoff-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0
Tracked-Worktree: clean; intentional ignored evidence retained

このページは public repository で現在地を読むための追跡済み Markdown です。
短期 capsule は [runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task 経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipeline は
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd) にあります。

## いまの一文

primary `5e50ff7`とcandidate `833717f`の7対13 commit／77 path unionをread-firstで
監査し、approved contentを変えずに構築できるexact selective integration contractを
固定しました。両source branchは未統合、Route Aは推奨のまま未選択です。

## 判断に使える現在地

| 対象 | 監査結果 | later integrationの扱い |
| --- | --- | --- |
| Approval | primary 8/8 exact、candidate 7/8 exact | candidateのapproved README variantを除外しprimary byteを保持 |
| Content lineage | primary T00–T07がcurrent authority | candidate D00–D10はsecondary deep audit |
| YMM4 evidence | 同一project/result、9/3/6、60 fps、4415 frames、73.583333秒 | primary revalidationをcurrent、candidate observationをhistoricalに配置 |
| Operator Batch | module/testを含むadd/add conflict | primary five-action familyを保持、candidate four-action toolingを除外 |
| Visual A/B/C | 9 cues・2/4/3と互換、Route A `recommended_not_selected` | proposal packageのみ統合しhuman choiceはH2へ残す |
| State | 5 documentsがmerge conflict | successorで一つに再生成。proseをmechanical mergeしない |
| Coverage | 20 commits、84 side-path entries、77 union paths、未分類0 | 27 integrate / 2 historical / 8 regenerate / 14 exclude |

Primary surface:
[`NEW_BANKNOTE_SUCCESSOR_BRANCH_INTEGRATION_AUDIT.md`](verification/NEW_BANKNOTE_SUCCESSOR_BRANCH_INTEGRATION_AUDIT.md)

## 次の入口

`new-banknote-successor-selective-integration-v1`が、exact primary baseからaudit JSONの
accepted candidate pathsだけをmaterializeします。primary approval、T00–T07、YMM4
revalidation、Operator Batchはbyte-exactで保持し、provenance authority 3面とcurrent
stateを再生成します。A/B/Cの選択は行いません。

## 公開・実行境界

このauditではmerge/rebase/cherry-pick、approved content edit、visual selection、YMM4、
render/media、production、public/rights action、master mutationを行っていません。
発音・creative quality・rights・publicationの承認ではありません。
