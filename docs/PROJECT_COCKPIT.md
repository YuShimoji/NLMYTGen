# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-standard-production-loop-gui-ready-v1
State-Revision: 2026-07-25.4
Updated: 2026-07-25 JST
Product-State: runtime-doctor-backed-end-to-end-episode-operation-gui
Product-Gate: second-real-topic-factory-validation
Recommended-Next: run-second-real-topic-through-standard-production-loop
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-standard-production-loop-gui-v1
Handoff-PR: none
Required-Base: 55507cb6f8940152f6ffae132186bcbcc0a700b0
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked state clean required after handoff; pre-existing ignored/private state preserved

短期正本は [runtime-state.md](runtime-state.md)、判断履歴は
[project-context.md](project-context.md)。

## いまの一文

Electron 43の既定画面からepisode manifest、deep runtime doctor、実dry-run、
内部レビュー生成dispatch、progress/cancel、accepted output確認までを1本の標準経路にした。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| 既定GUI | `自動動画生成`の5工程縦導線 | 旧4タブは維持 |
| Manifest | accepted実例を直接読込、別manifestもsafe dialog選択 | repo-relative表示 |
| Runtime | code/review/render/regenerateをdeep doctorで独立判定 | receipt-onlyはreadyにしない |
| Dry-run | accepted実manifestで実pipeline dry-run pass | write/render/playbackなし |
| Generation | 実CLI commandへ接続、単一job、bounded log、owned cancel | Missionではtest doubleのみ |
| Result | project/MP4/receipt/acceptanceをidentity別表示 | autoplay/YMM4 launchなし |
| Electron | exact 43.2.0、1280x720 / 1920x1080 hidden smoke pass | silent、no focus takeover |
| Accepted cut | exact media/project SHAとcreative locks不変 | rerender不要 |
| Taste | skill不在、未使用・未取得 | image/SVG/design direction追加なし |

## 次の入口

`npm --prefix gui start`で第2実トピックのmanifestを選び、4 profile ready、
protected inputs exact、dry-run passの順に確認する。次の証明対象は同じGUI/pipelineを
異なる実題材へ再利用できること。rights、creative acceptance、production、
publicationは別gateである。

## 公開・実行境界

accepted cutのscript、voice、timing、subtitle、line break、real-media treatmentは
closedのまま。YMM4 launch、新render、playback、private transfer、rights、
production、publication、upload、release、PR、merge、master mutationは未実施。
