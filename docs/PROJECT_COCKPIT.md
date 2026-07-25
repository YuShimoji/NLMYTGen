# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-second-real-topic-gui-render-validated-v1
State-Revision: 2026-07-25.5
Updated: 2026-07-25 JST
Product-State: two-distinct-real-topics-through-one-gui-and-video-pipeline
Product-Gate: third-topic-variation-or-three-run-operator-repeatability
Recommended-Next: run-third-topic-with-new-input-shape-or-measure-three-consecutive-operator-runs
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-second-real-topic-factory-v1
Handoff-PR: none
Required-Base: 02e5464c0f7d0ce90a198e788a336cb201682e9b
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; ignored/private runs preserved

短期正本は [runtime-state.md](runtime-state.md)、詳細証跡は
[SECOND_REAL_TOPIC_FACTORY_VALIDATION_2026-07-25.md](verification/SECOND_REAL_TOPIC_FACTORY_VALIDATION_2026-07-25.md)、
判断履歴は [project-context.md](project-context.md)。

## いまの一文

new-banknoteとREINSの2つの実トピックが、同じElectron 43標準画面から
manifest、doctor、dry-run、YMM4生成、MP4検証、結果readbackまで完走した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| 第2実トピック | REINS、7 cues / 4 scenes / 4・3 / 45.416秒 | internal canary |
| Source | official 4 surfaces、factual cue 6/6 supported | raw/G-27は発見入力 |
| Real media | raster 7件、cue frame 7件すべて別SHA | rights unresolved、ignored |
| YMM4 | UIA-only row生成・output、7 Voice / 7 Image | keyboard/mouse injectionなし |
| GUI | Electron 43.2.0、doctor・dry-run・real render pass | dirty-worktree probeだけ狭い例外 |
| MP4 | H.264/AAC、1920x1080、60fps、45.416秒、full decode pass | human未採用 |
| Repeatability | fresh run 2回のproject/MP4/media manifest/readback SHA一致 | 3連続operator proofは未実施 |
| Existing cut | new-banknote source/project/MP4/acceptance全てexact | accepted identity不変 |

## 次の入口

既定は第三トピックを異なるcue/scene/speaker/time shapeで通す。運用安定性を先に
測る場合は、REINSを新しいrun IDへ3回連続実行し、手動介入0、残留process 0、
artifact SHA一致、GUI receipt passを要求する。

## 公開・実行境界

REINS結果はtechnical internal-review evidenceであり、creative acceptance、
rights、production、publication、upload、release、PR、merge、master mutationを
承認しない。accepted new-banknoteのbytesと人間判断は変更しない。
