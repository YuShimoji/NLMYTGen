# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-yukkuri-benchmark-families-loop-v1
State-Revision: 2026-08-04.3
Updated: 2026-08-04 JST
Product-State: science-family-playable-baseline-verified-visual-carrier-repair-required
Product-Gate: continue
Recommended-Next: add-original-science-visual-carrier-and-rerender
External-State: local-feature-branch-current-slice-not-pushed
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: science-family-330s-yymm4-playable-baseline-and-exact-render-receipt
Prior-Outcome-Commit: dcd0cbfede633c6a1fbc263b309c7076c44ca100
Remote-Parity: origin tip dd97ec2; prior local checkpoint 9d22d39 is ahead 1 and current slice remains unpushed
Tracked-Worktree: current slice on named paths; unrelated saved sample CSV plus protected untracked and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、6 family contractは
[benchmark_families.json](../production_pilots/yukkuri_benchmark_families_001/benchmark_families.json)。
park済みportable bundle証跡は
[PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md](verification/PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md)。

## いまの一文

6つの公開ゆっくり解説channelを異なるformat familyとして固定し、最初のscience familyを
YMM4で330秒の再生可能MP4まで出力したが、visual carrier不在のため再現完了とは扱わない。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Channel identities | 6/6 fixed | current public URLs, checked 2026-08-04 |
| Format families | 6/6 unique | observable mechanics only |
| Contract axes | 10 per family | measurement pending |
| No-copy boundary | 6 protected expression classes | all enforced true |
| Registry validation | 4 focused tests + CLI pass | full suite not run |
| Playable YMM4 baselines | 1/6 | science MP4 full decode and exact SHA verified |
| Fully viewable reproductions | 0/6 | black-background subtitle baseline is not a reproduction |
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

science episodeのverified YMMPへoriginal visual carrierを加え、voice/subtitle順序を保持して
successor MP4を再出力する。full decodeと複数frame reviewでblack-only状態が解消した時だけ
1/6を`local_viewable_verified`にする。

## 公開・実行境界

YMM4 target import、timeline add、YMMP save、native FFmpeg render、full decode、
sampled-frame reviewを実施。preview playback、system volume変更、network、cloud upload、
external communicationは0。named recipient delivery、human open、
creative acceptance、rights、production、publication、upload、release、PR、merge、
master mutation、tag、deploymentは未実施・未承認。
