# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-derived-review-packet-batch-execution-validated-v1
State-Revision: 2026-07-27.3
Updated: 2026-07-27 JST
Product-State: content-independent-technical-factory-with-real-derived-artifact-change-set
Product-Gate: cross-terminal-review-artifact-delivery
Recommended-Next: build-versioned-portable-review-bundle-and-recipient-open-contract
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-derived-review-packet-batch-v1
Handoff-PR: none
Required-Base: 8a78eb2c6c33c9638dcfb7f8517ccea9f953478a
Implementation-Checkpoint: resolved-by-current-branch-tip
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[QUEUE_DERIVED_REVIEW_PACKET_VALIDATION_2026-07-27.md](verification/QUEUE_DERIVED_REVIEW_PACKET_VALIDATION_2026-07-27.md)、
機械可読結果は
[QUEUE_DERIVED_REVIEW_PACKET_VALIDATION_2026-07-27.json](verification/QUEUE_DERIVED_REVIEW_PACKET_VALIDATION_2026-07-27.json)。

## いまの一文

standard Electron GUIの`バッチ実行`が、rendered packageを不変に保ったまま
Food Expiry `cue_002`のversioned review derivativeをone-shot生成し、
restart/resumeで再dispatchしない。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Default route | `自動動画生成` | 既存standard loopを維持 |
| Batch route | `バッチ実行` | secondary / serial / one active job |
| Queue | queue-v3 SHA exact | GUIからpackage追加なし |
| Change set | Food Expiry entry 1 | `review_packet_generation`だけ |
| Actual GUI execute | succeeded 1 / no-op 3 | dispatch / authority 1 / 1 |
| Lifecycle | `rendered → rendered` | content/project/MP4不変 |
| Cue | `[373,816)` / 60 fps | canonical/project/receipt照合 |
| Packet | 5 files / decode pass | ignored versioned output |
| Authority | exact one-shot consumed | reuse/overwrite禁止 |
| Journal | event 7 / prefix exact | explicit reopen |
| Restart/resume | succeededを維持 | dispatch delta 0 / rewrite 0 |
| Tracked-only | source unavailable | dispatch/YMM4/render 0 |
| Runtime | Electron 43 hidden pass | playback/volume 0 |
| External authority | human / rights / production / public false | technical stateと分離 |

## 次の入口

current packetを再生成せず、manifestと5 output identityを入力にversioned portable
review bundleとrecipient-open contractを作る。accepted identity、live availability、
machine delivery、human open confirmationを別stateとして保持する。

## 公開・実行境界

actual GUIのbounded derived effectは完了した。content/visual change、another topic、
YMM4、render driver、full render、playback、human acceptance、rights、production、
publication、upload、release、PR、merge、master mutation、deployment、public
exposureは未実施・未承認。
