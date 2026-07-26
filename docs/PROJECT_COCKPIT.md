# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-third-real-topic-gui-render-validated-v1
State-Revision: 2026-07-26.2
Updated: 2026-07-26 JST
Product-State: three-distinct-real-topics-through-one-clean-gui-and-video-pipeline
Product-Gate: factory-contract-v2-extraction
Recommended-Next: derive-factory-contract-v2-from-three-observed-topics
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-third-real-topic-factory-v1
Handoff-PR: none
Required-Base: fe6672686625d401a7d2dd77fa9d9935e6036e0a
Implementation-Checkpoint: fe6672686625d401a7d2dd77fa9d9935e6036e0a
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[THIRD_REAL_TOPIC_FACTORY_VALIDATION_2026-07-26.md](verification/THIRD_REAL_TOPIC_FACTORY_VALIDATION_2026-07-26.md)、
機械可読結果は
[technical_validation_receipt.json](../production_pilots/factory_canaries/ai_monitoring_labor_001/technical_validation_receipt.json)と
[three_topic_variation_receipt.json](../production_pilots/factory_canaries/ai_monitoring_labor_001/three_topic_variation_receipt.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

new-banknote、REINS、AI職場モニタリングの3実トピックを、異なる入力shapeのまま
同じclean Electron 43 GUIとreal YMM4 video pipelineへ通した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| 第3 topic shape | 5 cues / 2 scenes / speakers 2:3 / 26.77秒 | 既存2件と全shape distinct |
| Sources / claims | OECD・EU-OSHA・ILO、unsupported 0 | official primary 3 surface |
| Real media | raster 5/5、unique SHA 5、SVG 0 | rights未承認 |
| Source YMMP | generic arbitrary-row UIA import、Voice 5 | manual edit / input injection 0 |
| GUI | doctor 4/4、protected 10/10、実render pass | bypass / double false |
| Output | project Voice 5 / Image 5、MP4 H.264/AAC | human aesthetic gate open |
| Resume | CLI 0.269496秒、22 files完全不変 | YMM4 / driver launch 0 |
| Drift | isolated bitrate driftを拒否 | canonical run不変 |
| Preservation | prior identity 20/20、dry-run 5/5 | prior rerender 0 |
| Conclusion | three observed topics pass common pipeline | universal claimなし |

## 次の入口

3 topic packagesからFactory Contract v2を抽出する。required / variable /
optional / forbidden fieldsを分け、manifest、claim support、media provenance、
source project、resume identityのvalidatorをversion化する。既存outputはrerenderせず
3 fixturesを再検証し、その後に第4topicをout-of-sample testとして使う。

## 公開・実行境界

現在の成果はbounded technical internal-review evidenceである。AI職場モニタリングの
human aesthetic acceptance、REINS / AI media rights、production、publication、
upload、release、PR、merge、master mutation、deployment、access change、
public exposureは各ownerの明示判断を待つ。
