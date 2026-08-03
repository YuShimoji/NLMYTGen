# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-yukkuri-benchmark-families-loop-v1
State-Revision: 2026-08-04.2
Updated: 2026-08-04 JST
Product-State: science-family-import-pack-ready-yymm4-operator-state-parked
Product-Gate: continue
Recommended-Next: resume-isolated-science-family-yymm4-import
External-State: local-feature-branch-current-slice-not-pushed
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: science-family-original-script-source-ledger-and-92-row-yymm4-csv-ready
Prior-Outcome-Commit: dcd0cbfede633c6a1fbc263b309c7076c44ca100
Remote-Parity: prior tip dd97ec2 matched origin; current slice remains local-only because push was not requested
Tracked-Worktree: current slice checkpointed on its named paths; unrelated untracked and ignored artifacts preserved

## Current Slice

- user directionにより、既存のnamed-terminal portable bundle laneは破棄せずparkし、
  別artifact identityで6種類のゆっくり解説benchmark loopを開始した。
- `yukkuri-benchmark-families-v1-20260804`に、現地物件tour、土木case、
  歴史chronology、科学concept、事故再構成、奇書・文献批評の6 familyと
  対応する6 channel identityを固定した。
- 10観測軸、exact channel/evidence URL、original episodeの進行状態、
  script / branding / thumbnail / audio / frame / illustrationのno-copy境界を
  machine-readable contractにした。
- validatorはexactly 6、channel/family unique、YouTube identity URL、10観測軸、
  no-copy境界、`local_viewable_verified`時のexact artifact receiptをfail-closedで検証する。
- science familyは公開channel surfaceのtitle / 09:12 durationを観測し、full-timeline
  frame/audio未検証を明示した。original 32-turn台本、NIST/NASA source registry、
  92-row YMM4 CSV（霊夢54 / 魔理沙38、SHA-256 `67d533d9...98aa4`）まで作成した。
- YMM4 4.54.0.1を起動したが、別案件の未保存台本
  `不動産DX_魔法の鍵とキュレーション_ymm4.csv*`を検出したため、save/discard/overwrite
  せず保全した。isolated empty windowは作成済みだが、target CSV import、timeline add、
  playback、renderは0。exact resume receiptはepisode `execution_state.json`に固定した。
- focused pytest 4 passed、validator CLI passed、compileall、`git diff --check` passed。
  現時点のfully viewable reproductionは0/6であり、完了とは扱わない。

## Parked Prior Slice

- Food Expiry `cue_002` portable bundle / recipient registry laneはcommit
  `dcd0cbf`でpush/readback済みのままparkした。bundle、quarantine、human-open、
  rights/production/publicationの状態は新benchmark laneへ伝播させない。

## Product Position

technical factoryはcontent-thread completionから独立したまま、repo-local ignored
packetをrepository-independent review artifactへ配送準備できる。accepted
identity、live availability、transport、machine-open、human-open、content decision、
rights/production/publicationは別clockである。

現在のbundleはhuman review starting artifactであり、creative acceptanceでも
production assetでもない。isolated local transportはnamed cross-terminal
deliveryではない。actual human-open、content decision、rights、production、
publicationはunverified / falseのまま。

## Active Design Quarantine

exact full-episode bundle v1の背景systemは、human reviewでquarantine
`NLMYTGEN-FEL-FULL-DQ-ALL-TEXT-RAPID-SWITCH-20260728-01`がactive。全4 cueの
readable document text、短い切替、subtitleとの同時reading taskが対象。release /
supersession evidenceはなく、cue_002 portable bundleや他authorityへ伝播しない。

## Exact Next Action

isolated empty YMM4 windowを選び、science episodeのexact CSVを開いて先頭行が
`今夜は、宇宙の距離を`であることを確認してからtimelineへ追加する。別案件の未保存台本は
save/discard/overwriteしない。その後、YMM4 native voice/subtitleを保持したproduction
projectとinternal-review MP4を作り、full decode、manifest、SHA-256、caption/readback、
local review entrypointを同一receiptに閉じた時だけ`local_viewable_verified`へ進める。

## Parked Prior Exact Next Action

実在named terminal、recipient identity、transport authorityが同時に得られた時だけ
immutable bundleで再開する。missing archiveからのfallback生成は行わない。

## Conditional Roadmap

- New active lane: measure -> original authoring -> local render -> exact receiptを6 familyで反復。
- Parked lane: named-recipient authorityが得られた場合だけimmutable bundleを配送。
- 共通境界: technical passからhuman acceptance、rights、production、publicationを推論しない。

## Residual Work

### Recipient-side registry and named delivery

- Purpose: one-off isolated proofを複数bundle/recipientの再現可能なintakeへ拡張。
- Effect: exact artifactの所在、attempt、conflict、supersessionを追跡できる。
- Requirements: registry schema、append-only receipt、recipient authority、
  no-overwrite、tracked-only failure、named terminal。
- State: registry/authority/ingest API・CLI、fail-closed duplicate/conflict、明示resumeが実装済み。
  exact existing transportだけをreconcileし、extra/missing/tampered/symlinkは登録しない。
  24 passed、CLI help、py_compile、`git diff --check`成功。commit dcd0cbf、push/readback済み。実在recipient transportは未実施。
- Owner: Codex runtime owner / technical delivery operator / named recipient。
- Next move: named terminal、recipient identity、transport authorityが同時に得られた場合だけone exact artifactでnamed deliveryを行う。

### Human and content review

- Purpose:機械openと人間によるopen/採否を分離する。
- Effect:レビュー状態をexact bundle SHAへ束縛し、誤ったaccept推論を防ぐ。
- Requirements: named recipient、human-open receipt、artifact-bound decision。
- State: cue_002 portable bundleは`human_open=unverified`、
  `content_decision=none`。別identityのfull-episode background quarantineはactive。
- Owner: recipient / content supervisor / human reviewer。
- Next move: portable bundleはnamed delivery後に独立receiptを返す。full-episode
  successorを作る場合はversioned identityで両quarantineへのnon-matchを示し、
  全編human reviewを再実施する。

### Creative, rights, production, and publication

- Purpose: technical deliveryをcreative/legal/public authorityから隔離する。
- Effect: portable artifactの存在だけでproduction/publicationへ進まない。
- Requirements: creative judgement、rights clearance、production authority、
  publication authority。
- State: all false / unperformed。
- Owner: creative、rights、production、publication owners。
- Next move: content decision後も各ownerが別々に判断する。

## Evidence and Re-entry

- Builder/registry/ingest: `src/pipeline/portable_review_bundle.py`
- Public CLI: `src/cli/main.py`
- Focused tests: `tests/test_portable_review_bundle.py`
- Existing immutable schemas: `schemas/review_bundle_v1/`
- Descriptor:
  `production_pilots/factory_canaries/food_expiry_labels_001/cue_002_portable_review_bundle_descriptor.json`
- Machine receipt:
  `production_pilots/factory_canaries/food_expiry_labels_001/cue_002_portable_review_bundle_machine_receipt.json`
- Report: `docs/verification/PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.md`
- Machine report: `docs/verification/PORTABLE_REVIEW_BUNDLE_VALIDATION_2026-07-27.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file。
Restore with `uv sync --extra dev --locked` and `cd gui; npm ci` only when
dependencies are absent。Do not rebuild the accepted v1 output in place。

## Active Boundaries

- source packet、content-thread packet、canonical content、package/queue descriptors、
  source/generated projects、source MP4、crops、provenance、dependency locksは不変。
- YMM4 4.54.0.1 launchとisolated empty window作成のみ実施。target import、timeline add、
  render driver、full render、transcode、playback、system volume、cloud/external transferは0。
- named recipient delivery、human open、content/creative decision、rights、
  production、publication、upload、release、PR、merge、master mutation、tag、
  deploymentは未実施。
- full-episode background quarantineはmachine check、cue-local acceptance、
  technical deliveryからreleaseしない。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
