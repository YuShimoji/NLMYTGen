# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-yukkuri-benchmark-families-loop-v1
State-Revision: 2026-08-05.1
Updated: 2026-08-05 JST
Product-State: science-family-local-viewable-verified-human-review-pending
Product-Gate: continue
Recommended-Next: measure-civil-engineering-family-while-science-review-is-parked
External-State: implementation-commit-pushed-authority-closeout-pending
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: science-family-330s-original-visual-carrier-successor-and-exact-render-receipt
Prior-Outcome-Commit: b4f5ff9e4c36c6e8f1139be5418f92277215f7b0
Remote-Parity: implementation commit b4f5ff9 matched origin with 0/0 before this authority closeout
Tracked-Worktree: implementation committed and pushed on named paths; authority closeout is local-only; unrelated dirty, untracked, and ignored artifacts preserved

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
- YMM4 4.54.0.1で別案件の未保存台本をoriginal-byte backup後に現行sampleへ保存し、
  pre-existing pending speaker remapを破棄せず保全した。そのsampleはunrelated dirty pathとして
  stage対象外。science CSV 92行をisolated windowへ読み込み、霊夢／魔理沙2 layer、
  5:30.11、19,807 frameのtimelineと6 MB YMMPを作成した。
- YMM4 native FFmpeg出力はH.264/AAC、1920x1080/60fps、330.116016秒、
  419,660,609 bytes、SHA-256 `95165c94...493e6`。全尺video/audio decodeはpassした。
- verified baselineへ6 scene / 6 original SVGのnetwork-free carrierを適用。92 VoiceItem SHA
  `fdfb0cc9...a437`はsourceと一致、ImageItem 6、19,807 frame、project SHA `0e19982f...a154`。
- YMM4 4.54.0.1 successor MP4はH.264/AAC、1920x1080/60fps、330.116016秒、419,660,118 bytes、SHA `472f54ab...93ef`。全尺decode pass。
- 2/90/210/320秒はcarrier 4/4、字幕可読4/4、black-only 0。90秒の地球label下端はhuman-review watchpoint。
- pytest 8、registry module CLI、scoped diff check pass。scienceはlocal-viewable 1/6、human acceptance / rights / production / publicationは未確認/false。

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

science successor `science-light-distance-001-visual-v002`をexact SHAのままStorage FB taskで
human review待ちにparkする。即時bounded repairが返らない限り、別artifact identityで
civil-engineering familyのrepresentative measurementとoriginal authoringを開始する。

## Parked Prior Exact Next Action

実在named terminal、recipient identity、transport authorityが同時に得られた時だけ
immutable bundleで再開する。missing archiveからのfallback生成は行わない。

## Conditional Roadmap

- New active lane: science reviewをparkし、measure -> original authoring -> local render -> exact receiptを残り5 familyで反復。
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
- YMM4 4.54.0.1の分離windowでsuccessor YMMP open、native FFmpeg MP4 render、
  full decode、4-frame reviewを実施。preview playback、system volume変更、cloud/external
  transferは0。pre-existing unrelated unsaved scriptは別windowに保持し、sample CSVはstageしない。
- named recipient delivery、human open、content/creative decision、rights、
  production、publication、upload、release、PR、merge、master mutation、tag、
  deploymentは未実施。
- full-episode background quarantineはmachine check、cue-local acceptance、
  technical deliveryからreleaseしない。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
