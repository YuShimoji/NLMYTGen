# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-runtime-doctor-private-ingest-ready-v1
State-Revision: 2026-07-25.3
Updated: 2026-07-25 JST
Product-State: electron-43-portable-runtime-with-consumer-profile-doctor-and-private-ingest-contract
Product-Gate: named-private-artifact-delivery-or-standard-production-loop-gui
Recommended-Next: use-runtime-doctor-to-select-private-artifact-delivery-or-gui-production-loop
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-runtime-doctor-private-ingest-v1
Handoff-PR: none
Required-Base: 21194b60f6824eaedaddacf05bb920e1a324936a
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required and verified after handoff push on 2026-07-25 JST
Tracked-Worktree: tracked state clean after handoff; pre-existing ignored/private state preserved

短期正本は [runtime-state.md](runtime-state.md)、判断履歴は
[project-context.md](project-context.md)、runtime診断の詳細は
[RUNTIME_DOCTOR_PRIVATE_INGEST_2026-07-25.md](verification/RUNTIME_DOCTOR_PRIVATE_INGEST_2026-07-25.md)
です。

## いまの一文

accepted stable internal cutとElectron 43.2.0を維持したまま、code/review/render/
regenerate readinessとprivate artifactのlive availabilityをone-commandで可視化した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| `code` | tracked-only clean checkoutでready | private bytes不要 |
| `review` | Thank端末のaccepted MP4 exact / ffprobe pass | playbackなし |
| `render` | YMM4 4.54.0.1、source project、9素材exact | YMM4起動・renderなし |
| `regenerate` | manifest / provenance / protected inputs agree | pipeline未実行 |
| Private contract | 12 artifact、hash、lineage、destinationを固定 | validation-only |
| Empty root | 全12件receipt-only、ingest false | receiptをlive扱いしない |
| Mismatch root | synthetic MP4をhash mismatch判定 | copy/overwriteなし |
| Electron | exact 43.2.0 hidden/silent smoke pass | 35.7.5 rollback維持 |
| Accepted cut | exact receipt / creative locks不変 | 再render不要 |

## 次の入口

`origin/codex/nlmytgen-runtime-doctor-private-ingest-v1`へ同期し、locked setup後に
`uv run python -m src.cli.main doctor-runtime --profile all --deep --format json`
を実行する。named consumerを選び、private deliveryが必要ならrecipientと別transfer
authorityを確定してstaging rootを検証する。deliveryを選ばない場合はstandard
production-loop GUIを独立sliceとして開始する。

## 公開・実行境界

doctorはprivate artifactのcopy/applyを認可しない。YMM4起動、render、音声・動画
再生、rights、production、publication、upload、release、PR、merge、master
integrationは未実施。actual transportはnamed recipientと別transfer authorityを要する。
