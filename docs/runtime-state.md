# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-recipient-registry-ingest-validated-pending-git-sync-v1
State-Revision: 2026-07-30.1
Updated: 2026-07-30 JST
Product-State: recipient-registry-ingest-contract-validated-pending-git-sync
Product-Gate: git-sync-then-named-terminal-delivery
Recommended-Next: commit-and-push-then-authorized-named-terminal-validation
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-portable-review-bundle-v1
Handoff-PR: none
Required-Base: 3556c8b73e635f87d867a0003cf4187b19075e88
Implementation-Checkpoint: registry-ingest-validated-by-focused-tests
Outcome-Commit: pending-current-branch-tip
Remote-Parity: pre-commit branch 0/0 after `git fetch --prune`; post-push readback pending
Tracked-Worktree: four task-owned tracked paths modified; existing untracked and ignored artifacts preserved

## Current Slice

- exact queue-derived Food Expiry `cue_002` packetを再生成せず、byte-exactな
  5 packet filesと5 control filesをself-contained directory / deterministic
  ZIPへまとめた。
- portable schema、recipient-open schema、descriptor、reusable builder/validator、
  public build/validate CLI、sanitized machine receiptを追加した。
- directoryとZIPは10-file semantic inventory一致、archive byte determinism、
  no-overwrite、path safety、media/image full decodeに合格した。
- isolated recipientへbyte-exact transport/extractし、Electron 43 hidden runtimeで
  PNG 2/2、video metadata、10/10 focus、無通信・無再生・横溢れ0を確認した。
- tracked-onlyはprivate packet不在を`source_bundle_unavailable`で返し、fallback生成を行わない。
- `bundle_id + version + archive SHA + recipient ID` registry、exact ingest authority、
  duplicate/version conflict/revoked/superseded/missing archiveのfail-closed APIとCLIを実装した。
- named-terminal modeはauthorityと同一のlive terminal IDが実行時に渡るまでtransportしない。
  focused pytestは23 passed、ingest CLI help起動と`git diff --check`も成功。commit/push/readbackは保留中。

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

検証済みのregistry/authority/ingest変更とruntime-stateを、今回所有する4 tracked
pathだけcommit・normal push・readbackする。commit後はnamed terminal、recipient identity、
transport authorityが同時に得られた場合だけone exact artifactでnamed-terminal pathを
検証する。

その後、実在named terminal、recipient identity、transport authorityが同時に得られた
場合だけone exact artifactでnamed-terminal pathを検証する。current bundle schema、
descriptor、receipt、bundle/ZIPはimmutableであり、missing archiveからregeneration、
render、network fallbackを行わない。machine-open、human-open、content decision、
delivery completionは独立状態のまま。

## Conditional Roadmap

1. Recipient registry / ingest:
   multiple bundle identity、local availability、recipient、delivery attemptを
   append-onlyに管理し、duplicate/conflict/resumeを検証する。
2. Named terminal delivery:
   明示されたrecipientとauthorityがある場合だけbyte-exact transport、
   extraction、machine-open receiptをartifact/versionへ束縛する。
3. Human-open confirmation:
   recipient本人の独立receiptで`human_open=verified`へ進める。machine proofや
   file existenceから推論しない。
4. Artifact-bound content decision:
   accept/repair/rejectとcue-specific noteをexact manifest SHAへ束縛する。
   acceptanceはrights、production、publicationへ伝播させない。
5. Multi-package review operations:
   queue、registry、named delivery、human receiptsをresume-safeに接続し、
   partial failureとsupersessionを監査可能にする。
6. Production governance:
   creative、rights、production、publicationの各owner authorityが揃ったartifact
   だけを別missionでrelease candidateへ昇格する。

各段階は前段のtechnical successから自動承認しない。named recipientが不在でも
registry/ingestのtechnical workは進められ、human/owner clockを待たない。

## Residual Work

### Recipient-side registry and named delivery

- Purpose: one-off isolated proofを複数bundle/recipientの再現可能なintakeへ拡張。
- Effect: exact artifactの所在、attempt、conflict、supersessionを追跡できる。
- Requirements: registry schema、append-only receipt、recipient authority、
  no-overwrite、tracked-only failure、named terminal。
- State: registry/authority/ingest API・CLIとfail-closed testsは実装済み。静的診断は
  23 passed、CLI help、git diff --checkが成功。Git同期はcommit/push/readback待ちで、
  実在recipient transportは未実施。
- Owner: Codex runtime owner / technical delivery operator / named recipient。
- Next move: 今回所有する4 tracked pathをcommit/push/readbackし、その後だけnamed deliveryを行う。

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
- YMM4、render driver、full render、transcode、playback、system volume、network、
  cloud/external transferは0。
- named recipient delivery、human open、content/creative decision、rights、
  production、publication、upload、release、PR、merge、master mutation、tag、
  deploymentは未実施。
- full-episode background quarantineはmachine check、cue-local acceptance、
  technical deliveryからreleaseしない。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
