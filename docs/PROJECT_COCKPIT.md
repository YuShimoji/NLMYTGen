# NLMYTGen Project Cockpit

Project-State-ID: episode-002-milestone-integrated-default-branch-v1
State-Revision: 2026-07-13.1
Updated: 2026-07-13 JST
Product-State: episode-002-milestone-integrated-on-default-branch
Product-Gate: verified-external-editorial-input-selection
Recommended-Next: select-or-provide-verified-editorial-source
External-State: public-repo-default-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。

## いまの一文

ユーザー承認済みOption Aにより、固定subject `d8e959c`、audit tail `a8b81e4`、
deterministic metadata rebindを含むintegration sealを、通常fast-forwardだけで
`master`へ統合しました。subject・audit・integration branchはprovenanceとして維持しています。

## 統合結果

| 対象 | 結果 | 判断境界 |
| --- | --- | --- |
| graph | audited baseからmasterへlinear fast-forward完了 | history rewrite・merge commitなし |
| provenance | subject `d8e959c`とaudit `a8b81e4`を不変のまま包含 | 各remote branchを維持 |
| metadata | runtime-state依存の3ファイルだけをdeterministic rebind | media/YMMPは非読取・非再生成 |
| invariants | script・claim・CSV・render/project/media identity・audit artifact不変 | human creative qualityは未判定 |
| checks | focused suite、state sync、JSON/privacy/path、merge-tree、diff pass | full pytestは対象外 |
| placement | `public-repo-default-branch` | 公開済み動画・production承認を意味しない |

Primary integration evidence:
`docs/verification/EPISODE_002_DEFAULT_BRANCH_INTEGRATION_2026-07-12.md`

Immutable pre-integration audit:
`docs/verification/EPISODE_002_MILESTONE_INTEGRATION_AUDIT_2026-07-12.md`

## 次の入口

source、provenance/rights context、stable identity、cue alignmentを備えたverified external
editorial sourceを1件選定または提供します。この入口はinternal/non-publicであり、editorial
adoption、human creative acceptance、rights、production、upload/publicationの承認ではありません。

## 残存debt

- human visual/editorial reviewは未完了。
- YMM4 4.53.0.9 profileとobserved 4.54.0.1 environment差、local `.ymmp`
  portabilityは未解決。
- historical user-home pathsとartifact burden、stale secondary docsは開示済み・非blocking。

## 公開・実行境界

No force/non-FF、merge commit、rebase/squash/cherry-pick、PR、branch deletion、YMM4、
Computer Use、media再生成、production、rights/legal、upload/publicationを維持しています。
