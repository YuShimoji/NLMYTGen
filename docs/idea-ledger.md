# Idea Ledger — Generic Static Layout Probe

ここには現在sliceから意図的に残した次の判断候補だけを書く。未承認の案を実装済み
として扱わない。

| Seed | Purpose | Effect | Prerequisite | State | Owner | Next move |
| --- | --- | --- | --- | --- | --- | --- |
| H1 subtitle safe-area observation | 共通layout floorをruntimeで確認 | C0 subtitle gateの判断材料 | userがprepared projectを開く | ready / unobserved | human visual reviewer | question 1を返す |
| H1 Image crop/anchor observation | static ImageItemの再利用性を確認 | Image placementはC2のまま | 同じH1 project | ready / unobserved | human visual reviewer | question 2を返す |
| H1 Text wrap/anchor observation | independent TextItemの安全な短文配置を確認 | Text placementはC2のまま | 同じH1 project | ready / unobserved | human visual reviewer | question 3を返す |
| Cross-machine portability | local absolute asset pathの移送可否を確認 | same-machine boundaryを更新 | 別端末で再materialize | deferred | YMM4 integration owner | portability taskを起こす |
| Second-topic C5 reuse | generic coreの異種topic適用を確認 | C5=0を再評価する材料 | H1成功と別topic入力 | deferred | episode-factory owner | H3でdata/config-only smoke |

## Closed / rejected in this slice

- Route A scene、ShapeItem、fade、transform、motion、render、rights/publication、master
  integrationはこのidea ledgerのactive seedではない。
- Synthetic CollectOnly resultはvalidation transportであり、visual observationやcapability
  regradeのseedにはしない。
