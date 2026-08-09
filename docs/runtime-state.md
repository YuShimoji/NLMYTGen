# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-yukkuri-benchmark-families-loop-v1
State-Revision: 2026-08-09.2
Updated: 2026-08-09 JST
Product-State: history-semantic-subtitle-pack-ready-visual-method-human-decision-required
Product-Gate: human-visual-method-decision
Recommended-Next: authorize-official-institutional-stills-and-bind-three-rights-cleared-assets
External-State: history-subtitle-pack-ready-no-eligible-local-visual-assets-other-portfolio-gates-unchanged
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: history-family-original-script-source-registry-overflow-free-import-csv-and-eight-scene-svg-carrier
Prior-Outcome-Commit: b4f5ff9e4c36c6e8f1139be5418f92277215f7b0
Remote-Parity: fresh 0/0 at e7b9a14 before this local slice
Tracked-Worktree: chronological-history authoring paths are owned; unrelated dirty, untracked, ignored, and GUI state remain excluded

## Current Slice

- Human decision supersedes the prior mechanical review state: generated SVG is
  prohibited as footage, background, set flat, static carrier, or rasterized
  derivative. The science, civil, and history SVG-derived videos remain exact
  technical evidence only and are not adoption candidates.
- The exact history render `history_japan_standard_time_001_yymm4_production_v001.mp4`
  is human-rejected. Its subtitle line breaks do not preserve meaning units,
  page changes interrupt utterances unnaturally, and the build failed to reuse
  the existing completed YMM4 subtitle settings. Hash, decode, nonblank, and
  collision checks do not mitigate this rejection.
- `NLM-HISTORY-NONSVG-SUBTITLE-REFRAME-001` identified `samples/palette.ymmp`
  as the exact S-0 template; its task-owned copy is byte-identical and its two
  subtitle-setting objects match `samples/production.ymmp`.
- The task-local history span is ready as 16 complete meaning-unit pages. WPF
  measurement reports 905.08px maximum against the 940px safe limit, and the
  parsed input/output page sequence is identical. The rejected automatic
  28-page result remains evidence of word and dependency splits not to repeat.
- No eligible provenance-complete, history-specific non-SVG local media exists.
  The recommended route is a three-still documentary chronology bound to the
  existing NICT, NAOJ, and Akashi source-registry entries; exact still bytes and
  reuse rights require human authorization before acquisition or render.
- science / civil / historyのscript、source registry、YMM4 input、render identityは
  `docs/project-context.md` に保持するが、SVG-derived visualsは全件不採用である。
- historyの420.716秒MP4はtechnical renderとしてのみ存在し、visual/subtitle methodの
  human rejectionによりproduction progressへ数えない。

## History artifact role
- Role: `E2E_VIDEO_PRODUCTION_BASELINE` / `YMM4_RENDER_PASS` / `TECHNICAL_PLAYBACK_PASS` / `CREATIVE_ACCEPTANCE_REJECTED` / `STANDARD_VISUAL_GRAMMAR_NOT_ESTABLISHED`.
- Evidence retained: exact 97-row import, eight ImageItems, 420.716016-second MP4 SHA-256 `18616f8b...c76a`, full video/audio decode, and start/middle/end playback progression.
- rejectionScope: `visual_method`, `subtitle_method`; direct user statements received 2026-08-09 18:04/18:05 JST prohibit generated-SVG use and reject the history subtitle method; full-length acceptance, pacing, motion density, benchmark alignment, and standard-format adoption remain unestablished.

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

公式機関静止画方式を採用するか一問で決める。採用する場合、source registryの `NICT-JST-HISTORY`、`NAOJ-STANDARD-TIME-HISTORY`、`AKASHI-STANDARD-MERIDIAN` に対応する権利確認済み静止画を1点ずつ供給または取得承認する。その後だけ、byte-identical S-0 template copyへ16-page semantic CSVをimportし、1884→1886→1888の境界へ3点を配置して30〜90秒review sliceをrenderする。

## Parked Prior Exact Next Action

実在named terminal、recipient identity、transport authorityが同時に得られた時だけ
immutable bundleで再開する。missing archiveからのfallback生成は行わない。

## Conditional Roadmap

- New active lane: historyをnon-SVG visual methodと完成subtitle templateで短尺reframeし、採用可能性を先に確認する。
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
- rejected SVG-derived artifacts、既存completed template、共有YMM4の未保存stateを変更しない。
- named recipient delivery、human open、content/creative decision、rights、
  production、publication、upload、release、PR、merge、master mutation、tag、
  deploymentは未実施。
- full-episode background quarantineはmachine check、cue-local acceptance、
  technical deliveryからreleaseしない。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
