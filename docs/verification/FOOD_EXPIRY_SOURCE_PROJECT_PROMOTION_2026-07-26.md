# Food-expiry Source-project Promotion — 2026-07-26

`food_expiry_labels_001`をbounded four-package queueの唯一候補として
`package_prepared`から`source_project_ready`へ進めた技術検証記録。
authorityは
`supervisor-food-expiry-source-project-materialization-2026-07-26`に限定した。

## Before → After

- Before: queue-v1は完了3件を`verified_noop`、food-expiryだけを
  `source_project_generation_required`として返した。source project、
  generated project、MP4、render evidence、human decisionは無かった。
- After: ignored local YMM4 source project 1件、tracked structural readback、
  promotion receipt、append-only successor descriptor、queue-v2が存在する。
  queue-v2は完了3件をno-op、food-expiryを`render_required` planとして返すが、
  render scheduleとexecution setは0である。

## Exact source project

- locator:
  `production_pilots/factory_canaries/food_expiry_labels_001/local_outputs/food_expiry_labels_source.local.ymmp`
- SHA-256: `4f8dc13976cb4ef56ea582d75e1ff92ae9d2780fff4cf53c13923d561955bdbf`
- size: 449,804 bytes
- structural identity:
  `10fa9fefac7ebc68ba3ace7af9f24e47a74eedf55be853fa05d5a4fb674183ff`
- YMM4: `4.54.0.1`
- VoiceItems: 4
- speaker: `ゆっくり霊夢赤縁` 4
- scene contract: 1
- timeline: 1,335 frames / 60fps / 22.25 seconds
- canonical text/order: 4/4 exact
- ToolStates / LayoutXml / private absolute path / unrelated item: 0

predecessor content identity
`27165fad6fadaee2e5c247a86758a505c7f5f5797eb7b386d174585622a585c6`
はsuccessorでも同一である。canonical CSV
`00ade6...855`、derived CSV `b4b4bb...2256`、scene/speaker/media/
render-settings authority、rights/public clocksは変更していない。

## Append-only lifecycle evidence

predecessor descriptor
`factory_package_v2_1.json`のSHAは
`18e078f6f6c5b6e17808ec9378d8476a9cd8ce426cd1281563c833ae21acf329`
のまま。successor
`factory_package_v2_1_source_project_ready.json`は
`4017f7d1591dc229f1163aecaf85f91e14d1d0eb919b03a3d1945e29d604688c`。

queue-v1は
`2cfbdab4bf3bfb765afa8909b54212311155ba85c3838078a1e0aac77a11375f`
のまま。queue-v2
`four_package_lifecycle_queue_v2.json`は
`4f0fe080a56697720409791e68c922655428f2832a604525e276bd3ee156554d`。
最初の3 entryとpolicyは同一で、food-expiryのdescriptor locatorだけをsuccessorへ
進めた。

## Queue evidence

live evaluation
`b782b2854e53b93a996e8498200c122f18532c9df14025df10ef2743dba52b53`
はno-op 3、render candidate 1、scheduled 0、execution 0、blocked/invalid 0。
food-expiryは`source_project_live_exact` / `render_required` /
`execution_eligible=false`。

index-only checkoutにはprivate projectをコピーしていない。successor evaluation
`af8e67f4e58b5098eaf33f1fd0da8ad042fbca27a7c954f793b4ade2f7f031f4`
は完了3件を`recorded_complete_no_live_file`、food-expiryを
`source_project_recorded_only` / `render_required`として保持した。
private file不在はdemotion、regeneration、render executionの理由にならない。

## Idempotence and repair history

actual YMM4 launchは2 attempts。1回目はblank projectのUIA element virtualizationで
`ElementNotAvailableException`となり、owned processを全て終了し、partial projectを
ignored failure evidenceとして保持した。stale element再取得をgeneric driverへ追加し、
2回目で成功した。成功後の同一promotionは`verified_noop`、YMM4/build launch 0、
project SHA/size/mtimeとsuccessor descriptor不変。さらに2回再生成検証し、tracked
artifactsとlocal projectはexactだった。process residueは0。

## Validation and boundaries

dotnet buildは0 warning / 0 error。promotion negative、Factory Contract v2.0/v2.1、
queue、episode、generic CSV/source paths、second/third topic preservationを合わせて
137 tests passed。negative coverageはcandidate/authority/lifecycle/identity/CSV/
speaker/cue/output collision/corrupt project/private path/package-rootを含む。

YMM4 render、generated visual project、MP4、ffmpeg、preview/speech playback、
system volume、manual interaction、Computer Use、input injection、human creative
decision、rights、production、publication、upload、release、PR、merge、master
mutationは実施していない。次の段階は別authorityによるfood-expiry 1件だけのrenderで
あり、queue再設計や第5 topicではない。
