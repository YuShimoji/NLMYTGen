# Runtime State — NLMYTGen

Project-State-ID: nlmytgen-derived-review-packet-batch-execution-validated-v1
State-Revision: 2026-07-27.3
Updated: 2026-07-27 JST
Product-State: content-independent-technical-factory-with-real-derived-artifact-change-set
Product-Gate: cross-terminal-review-artifact-delivery
Recommended-Next: build-versioned-portable-review-bundle-and-recipient-open-contract
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-derived-review-packet-batch-v1
Handoff-PR: none
Required-Base: 8a78eb2c6c33c9638dcfb7f8517ccea9f953478a
Implementation-Checkpoint: resolved-by-current-branch-tip
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

## Current Slice

- executor contractへ`effect_class=derived_artifact`と
  `operation=review_packet_generation`を追加した。
- Food Expiry `cue_002`のone-entry change-setをstandard GUIでplan / executeし、
  one-shot authority 1、backend dispatch 1、journal succeeded 1を確認した。
- outputはrendered packageを入力にするignored versioned packetで、lifecycleは
  `rendered → rendered`、content / project / MP4 identityは不変である。
- cueはcanonical script、unique VoiceItem、ImageItem、cue readback、run receipt、
  source provenanceからframe `[373,816)` / 60 fpsへ解決する。
- Electron restart後に同じjournalをopenしてresumeし、dispatch delta 0、
  authority delta 0、packet SHA / size / mtime mismatch 0を確認した。
- tracked-onlyはprivate source不在を`derived_artifact_source_unavailable`で返し、
  dispatch、YMM4、render、private copyを行わない。

## Product Position

technical factoryはcontent-thread完了を待たず、既存rendered evidenceからreview
artifactを作れる。content-thread decisionsはoptional asynchronous successor
inputであり、technical completionのgateではない。

実GUIのreal effect、one-shot authority、append-only journal、restart-safe resume、
tracked-only fail-closedまで一つのbounded operationとして証明した。packetはhuman
reviewの開始資料で、human acceptance、rights、production、publication authorityを
付与しない。

## Exact Next Action

packet manifest、5 output identities、source-availability statusをversioned portable
bundleへまとめ、別端末でrecipientが安全にopenできるcontractを作る。bundleは
private absolute pathを含めず、accepted identityとlive availabilityを分離する。

開始条件:

- current packet manifestと全5 output SHAをexactに入力へ束縛する
- private sourceをbundleへ暗黙複製しない
- recipient openはmachine deliveryとhuman open confirmationを別stateにする
- content/creative/rights/production判断をdelivery成功から推論しない
- current Food Expiry packetを再生成せず、versioned successorへ出力する

## Residual Work

### Portable review bundle and recipient-open contract

- Purpose: generated packetをprivate source依存なしで別端末へ届ける。
- Effect: delivery identity、availability、recipient-openを監査可能にする。
- Requirements: packet SHA inventory、portable locator、no-secret scan、
  recipient-open receipt schema、no-overwrite versioning。
- State: local packet生成、decode、manifest、GUI resumeはvalidated。cross-terminal
  deliveryとrecipient openは未実施。
- Owner: technical delivery operator / recipient。
- Next move: current packetを入力にportable bundle v1とopen receipt contractを作る。

### Creative, rights, and public gates

- Purpose: technical packet deliveryとeditorial/creative/legal/public判断を分離する。
- Effect: artifact availabilityから採用・公開判断が暗黙継承されない。
- Requirements: optional content-thread result、human acceptance、rights、
  production/publication owner判断。
- State: content/visual変更、human acceptance、rights/public actionは0。
- Owner: content supervisor / human reviewer / rights / production owners。
- Next move: recipientがpacketを開いた後、必要なownerが独立に判断する。

## Evidence and Re-entry

- Builder: `src/pipeline/cue_review_packet.py`
- Change set: `production_pilots/factory_queues/food_expiry_cue002_review_packet_change_set_v1.json`
- Tracked receipt: `production_pilots/factory_canaries/food_expiry_labels_001/cue_002_queue_review_packet_receipt.json`
- Report: `docs/verification/QUEUE_DERIVED_REVIEW_PACKET_VALIDATION_2026-07-27.md`
- Machine receipt: `docs/verification/QUEUE_DERIVED_REVIEW_PACKET_VALIDATION_2026-07-27.json`

Re-enter by fetching the handoff branch, requiring `HEAD...@{upstream}=0/0` and
tracked clean, then reading `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → this file。
Restore with `uv sync --extra dev --locked` and `cd gui; npm ci` if dependencies
are absent。Start from the tracked receipt and packet manifest; do not execute the
consumed authority again。

## Active Boundaries

- package descriptors、predecessor queues、canonical content、source/generated
  projects、source MP4、existing content-thread packet、locksはimmutable。
- packet extractionのffmpeg encode 1とsource-view copy 1だけを実施した。
  YMM4、render driver、full render、playback、volume operationは0。
- next workはdelivery/portabilityであり、content reviewやanother topicではない。
- human acceptance、rights、production、publication、upload、release、PR、merge、
  master mutation、tag、deploymentは未実施。

## Maintenance Note

Keep this capsule within 160 lines. Resolve the outcome commit from the current
remote branch tip. Final post-commit canonical regression and parity evidence
belongs in the supervising handoff response, not a second implementation commit.
