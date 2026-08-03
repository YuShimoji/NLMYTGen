# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-yukkuri-benchmark-families-loop-v1
State-Revision: 2026-08-04.1
Updated: 2026-08-04 JST
Product-State: six-channel-benchmark-registry-validated-first-render-pending
Product-Gate: continue
Recommended-Next: measure-and-render-first-original-family-episode
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: six-channel-registry-validator-4-focused-tests-pass
Prior-Outcome-Commit: dcd0cbfede633c6a1fbc263b309c7076c44ca100
Remote-Parity: 0/0 after fetch; HEAD matched origin by ls-remote readback
Tracked-Worktree: tracked clean; protected untracked and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、6 family contractは
[benchmark_families.json](../production_pilots/yukkuri_benchmark_families_001/benchmark_families.json)。
park済みportable bundle証跡は
[PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md](verification/PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md)。

## いまの一文

6つの公開ゆっくり解説channelを異なるformat familyとして固定し、observable
mechanicsだけをoriginal episodeへ移すregistryとfail-closed validatorを実装した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Channel identities | 6/6 fixed | current public URLs, checked 2026-08-04 |
| Format families | 6/6 unique | observable mechanics only |
| Contract axes | 10 per family | measurement pending |
| No-copy boundary | 6 protected expression classes | all enforced true |
| Registry validation | 4 focused tests + CLI pass | full suite not run |
| Fully viewable reproductions | 0/6 | first render is next slice |
| Prior portable lane | parked at `dcd0cbf` | identity/state not inherited |
| Rights / production / publication | false | technical successから継承しない |

## Active design quarantine

`food_expiry_full_episode_review_bundle_v1`の背景systemは
`NLMYTGEN-FEL-FULL-DQ-ALL-TEXT-RAPID-SWITCH-20260728-01`でactive quarantine。
4 cueすべてがreadable document text中心で、短い切替とsubtitleが同時reading
taskを作るため、全編がaudiovisual explanationではなくtext surfaceの連続になる。
release / supersession evidenceはない。cue_002 portable bundle、canonical content、
rights、production、publicationの判断とは別clock。

## 次の入口

最初のfamilyで代表動画のobservable mechanicsを測定し、original script / licensed
or original assetsだけでepisodeをrenderする。MP4 full decode、manifest/SHA、caption
readback、local review entrypointが閉じた時だけ1/6を`local_viewable_verified`にする。

## 公開・実行境界

YMM4、render driver、full render、transcode、playback、system volume、network、
cloud upload、external communicationは0。named recipient delivery、human open、
creative acceptance、rights、production、publication、upload、release、PR、merge、
master mutation、tag、deploymentは未実施・未承認。
