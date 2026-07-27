# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-portable-review-bundle-machine-open-validated-v1
State-Revision: 2026-07-28.1
Updated: 2026-07-28 JST
Product-State: repository-independent-versioned-review-bundle-with-recipient-open-contract
Product-Gate: multi-bundle-recipient-registry-and-named-delivery
Recommended-Next: build-recipient-side-review-bundle-registry-and-validate-named-terminal-delivery
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: resolved-by-current-branch-tip
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md](verification/PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md)、
機械可読結果は
[PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.json](verification/PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.json)。

## いまの一文

exact `cue_002` packetを変更せず、repository-independentな10-file
directory/deterministic ZIPとrecipient-open contractへ変換し、isolated recipientの
Electron machine-openまで無通信・無再生で検証した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Source packet | exact 5 files / mismatch 0 | regenerated/modified false |
| Bundle | v1 / 10 files / self-contained | ignored local, no overwrite |
| ZIP | SHA `cba54b31...28ca` | deterministic stored archive |
| Offline entry | `index.html` | plain document, server不要 |
| Directory / ZIP | semantic identity一致 | path-safety violations 0 |
| Media | H.264/AAC + PNG 2 decode pass | transcode/playback 0 |
| Transport | isolated recipient completed | named external deliveryではない |
| Machine open | Electron 43 / 10 focus / error 0 | hidden/muted/no network |
| Human open | unverified | machine-openから推論しない |
| Content decision | none | human-openから推論しない |
| Full-episode background | active quarantine | exact ZIP/MP4 human reviewに束縛 |
| Rights / production / publication | false | technical successから継承しない |
| Tracked-only | `source_bundle_unavailable` | fallback/regeneration 0 |

## Active design quarantine

`food_expiry_full_episode_review_bundle_v1`の背景systemは
`NLMYTGEN-FEL-FULL-DQ-ALL-TEXT-RAPID-SWITCH-20260728-01`でactive quarantine。
4 cueすべてがreadable document text中心で、短い切替とsubtitleが同時reading
taskを作るため、全編がaudiovisual explanationではなくtext surfaceの連続になる。
release / supersession evidenceはない。cue_002 portable bundle、canonical content、
rights、production、publicationの判断とは別clock。

## 次の入口

`bundle_id + version + archive SHA + recipient ID`をkeyにしたrecipient-side
registry/ingestを作り、duplicate、version conflict、missing archive、
supersessionをfail closedに扱う。実在するnamed terminalとauthorityが揃った時だけ
one exact artifactのdelivery validationへ進む。

その後のhuman-open receipt、artifact-bound content decision、creative、rights、
production、publicationは独立clockであり、自動的には進めない。

## 公開・実行境界

YMM4、render driver、full render、transcode、playback、system volume、network、
cloud upload、external communicationは0。named recipient delivery、human open、
creative acceptance、rights、production、publication、upload、release、PR、merge、
master mutation、tag、deploymentは未実施・未承認。
