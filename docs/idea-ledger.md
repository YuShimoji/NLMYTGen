# Idea Ledger — Generic Static Layout Probe

ここには現在sliceから意図的に残した次の判断候補だけを書く。未承認の案を実装済み
として扱わない。

| Seed | Purpose | Effect | Prerequisite | State | Owner | Next move |
| --- | --- | --- | --- | --- | --- | --- |
| H1 subtitle safe-area observation | 共通layout floorをruntimeで確認 | exact profile/layoutの可読性根拠 | completed batch/result validation | completed / pass | human visual reviewer | tracked receiptをcurrent evidenceに使う |
| H1 Image crop/anchor observation | static ImageItemの再利用性を確認 | exact 640x360 asset/zoneの可視性根拠 | completed batch/result validation | completed / pass | human visual reviewer | bounded combination条件を維持する |
| H1 Text wrap/anchor observation | independent TextItemの安全な短文配置を確認 | exact short label/zoneの可視性根拠 | completed batch/result validation | completed / pass | human visual reviewer | longer/different textへ一般化しない |
| Cross-machine portability | local absolute asset pathの移送可否を確認 | same-machine boundaryを更新 | 別端末で再materialize | deferred | YMM4 integration owner | portability taskを起こす |
| Alternate Image/Text conditions | 別size/anchor/style/longer textを確認 | exact composite外の使用条件を広げる | 実layoutが条件変更を要求 | deferred | visual system owner | 変更された1条件だけを再観測する |
| Motion/effects/transitions | dynamic primitiveを限定確認 | static floorから必要な演出だけを追加 | selected routeが必要性を示す | deferred | motion integration owner | 一つのbounded primitiveを選ぶ |
| Second-topic C5 reuse | generic coreの異種topic適用を確認 | C5=0を再評価する材料 | 別topic入力とcore hash freeze | deferred | episode-factory owner | data/config-only smokeを行う |
| New-banknote visual route | A/B/Cとflow/risk/restraintを人間決定 | selected-route diagnostic planningを解禁 | authoritative provenance branch | queued / unselected | human visual reviewer | separate successor laneで最新boardをreview |

## Closed / rejected in this slice

- Route A/B/C選択、selected-route project、render、rights/publication、master
  integrationはこのgeneric intake sliceの実装対象ではない。
- Synthetic CollectOnly resultはvalidation transportであり、visual observationやcapability
  regradeのseedにはしない。
