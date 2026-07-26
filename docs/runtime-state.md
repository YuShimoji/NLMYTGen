# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-portable-review-bundle-machine-open-validated-v1
State-Revision: 2026-07-27.4
Updated: 2026-07-27 JST
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
- tracked-onlyはschema/descriptor/receiptを読める一方、private packet不在を
  `source_bundle_unavailable`で返し、fallback生成を行わない。

## Product Position

technical factoryはcontent-thread completionから独立したまま、repo-local ignored
packetをrepository-independent review artifactへ配送準備できる。accepted
identity、live availability、transport、machine-open、human-open、content decision、
rights/production/publicationは別clockである。

現在のbundleはhuman review starting artifactであり、creative acceptanceでも
production assetでもない。isolated local transportはnamed cross-terminal
deliveryではない。actual human-open、content decision、rights、production、
publicationはunverified / falseのまま。

## Exact Next Action

複数のportable bundleを`bundle_id + version + archive SHA + recipient ID`で登録し、
recipient-side ingestがduplicate、version conflict、revoked/superseded artifact、
missing local archiveをfail closedに扱うregistryを作る。そのregistryを使い、
実在するnamed terminalが利用可能になった時だけone exact artifactのdeliveryを
検証する。

開始条件:

- current bundle schema/descriptor/machine receiptをimmutable inputにする
- registry entryからprivate repo pathを除外する
- named recipient identityとtransport authorityを明示する
- machine-openとhuman-openを統合しない
- missing bundleからpacket regeneration、render、network fallbackを行わない
- current bundle/ZIPをoverwriteせず、変更はversioned successorにする

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
- State: single bundleのisolated transport/machine-openはvalidated。実在recipient
  へのtransportは未実施。
- Owner: technical delivery operator / named recipient。
- Next move: registry/ingestを先に実装し、recipient存在時にnamed deliveryを行う。

### Human and content review

- Purpose:機械openと人間によるopen/採否を分離する。
- Effect:レビュー状態をexact bundle SHAへ束縛し、誤ったaccept推論を防ぐ。
- Requirements: named recipient、human-open receipt、artifact-bound decision。
- State: `human_open=unverified`、`content_decision=none`。
- Owner: recipient / content supervisor / human reviewer。
- Next move: named delivery後、必要な人間が独立receiptを返す。

### Creative, rights, production, and publication

- Purpose: technical deliveryをcreative/legal/public authorityから隔離する。
- Effect: portable artifactの存在だけでproduction/publicationへ進まない。
- Requirements: creative judgement、rights clearance、production authority、
  publication authority。
- State: all false / unperformed。
- Owner: creative、rights、production、publication owners。
- Next move: content decision後も各ownerが別々に判断する。

## Evidence and Re-entry

- Builder: `src/pipeline/portable_review_bundle.py`
- Schemas: `schemas/review_bundle_v1/`
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

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
