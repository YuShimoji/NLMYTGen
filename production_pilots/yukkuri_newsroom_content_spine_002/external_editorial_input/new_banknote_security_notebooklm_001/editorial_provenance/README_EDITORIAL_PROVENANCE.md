# New-banknote Editorial Provenance

> **CURRENT SCRIPT FROZEN — INTERNAL REVIEW — NO FUTURE SILENT EDIT AUTHORITY**

この page は、primary T00–T07 content lineageを現在の正本に保ちながら、candidate D00–D10をsecondary deep-audit evidenceとして読む統合surfaceです。raw NotebookLM Audio Overview transcriptはclaim discoveryに使われましたが事実正本ではなく、最終文面はofficial sourceに支えられたparaphraseとWorkerの会話構造・接続・圧縮・voiceの組合せです。

## Authority

- approved content: primary explicit option A receipt `new-banknote-script-option-a-approval-v1` と8 hashesがsole current authority
- content lineage: primary T00–T07がcurrent、candidate D00–D10はsecondary deep audit
- YMM4: primary existing-evidence revalidationがcurrent structural authority、candidate observationはhistorical predecessor
- Operator Batch: primary five-action approval/lineage-aware familyがcurrent、candidate four-action familyはexcluded
- visual: A/B/Cはproposal-only、Route Aは`recommended_not_selected`でhuman selection未実施

## 現在分かること

| 問い | repo証拠からの回答 | 境界 |
| --- | --- | --- |
| どの入力を使ったか | user-submitted Audio Overview transcript の fingerprintから182 claimsを整理し、15 adopted claims / 20 factual unitsを4 official sourcesへ接続 | raw bodyは追跡しない |
| どの工程が本文を変えたか | D06 canonical generation とD07 editorial convergence | operationとauthorityをcue別に記録 |
| どの程度変わったか | pre-editorial draftの9 cue中、byte同一は1 cue。ordered normalized overlapは279 characters / 263 tokens | similarityであり著者比率ではない |
| 誰が承認したか | primary human approval receiptがoption Aと8 file hashesを固定 | 将来のsilent editは未許可 |
| 以前のuser scriptを使ったか | `not_proven_from_available_repo_evidence` | repoに候補がないことは不使用の証明ではない |
| historical YMM4 local bytesのavailability | `present_and_hash_matched_same_machine_non_authoritative` | 3 expected identitiesはsame-machine local bytesとhash一致。current authorityはprimary revalidationのまま |

## 変換量の読み戻し

- attributed substantive units: 38 / 38
- surface coverage: 40 non-overlapping segments / 425 characters
- unresolved / unattributed substantive units: 0 / 0
- single-source paraphrase units: 19
- multi-source synthesis units: 1
- editorial bridge / character voice units: 9 / 9
- omitted verified claims: 4
- pre-editorial→current speaker reassignment / scene movement: 0 / 0
- style/rhetoric-only adjudication outcomes excluded from factual adoption: 52

## 読む順序

1. `cue_transformation_matrix.json` — 9 cueのclaim、fingerprint、operation、authority、approval
2. `stage_decision_ledger.json` — D00〜D10のinput/outputと判断権限
3. `authorial_contribution_readback.json` — overlapと変換量、方法上の限界
4. `prior_user_script_usage_audit.json` — prior user scriptのbounded audit
5. `content_lock_receipt.json` — downstreamが参照する不変identity
6. `future_change_contract.md` — 次回変更時のvisible delta条件
7. `provenance_validation_readback.json` — 決定性、privacy、coverage検証

## 次の gate

この統合surfaceからA/B/Cのvisual directionを人が選びます。Route Aは推奨のままで、まだ選択・実装されていません。script、YMM4、render、production、publication、rights actionはこの統合で変更していません。
