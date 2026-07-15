# New-banknote Editorial Provenance

> **CURRENT SCRIPT FROZEN — INTERNAL REVIEW — NO FUTURE SILENT EDIT AUTHORITY**

この page は、現在の9 cueについて「事実の根拠」と「編集上の著者・判断」を分けて読む primary surface です。raw NotebookLM Audio Overview transcript は claim discovery に使われましたが事実正本ではなく、最終文面は official source に支えられた paraphrase と Worker の会話構造・接続・圧縮・voice の組合せです。

## 現在分かること

| 問い | repo証拠からの回答 | 境界 |
| --- | --- | --- |
| どの入力を使ったか | user-submitted Audio Overview transcript の fingerprintから182 claimsを整理し、15 adopted claims / 20 factual unitsを4 official sourcesへ接続 | raw bodyは追跡しない |
| どの工程が本文を変えたか | D06 canonical generation とD07 editorial convergence | operationとauthorityをcue別に記録 |
| どの程度変わったか | pre-editorial draftの9 cue中、byte同一は1 cue。ordered normalized overlapは279 characters / 263 tokens | similarityであり著者比率ではない |
| 誰が承認したか | current execution contract上、ユーザーは現在の9 cueで継続する状態を承認 | 独立した同時点receiptはなく、将来のsilent editも未許可 |
| 以前のuser scriptを使ったか | `not_proven_from_available_repo_evidence` | repoに候補がないことは不使用の証明ではない |
| YMM4ローカル証跡を再検証したか | `reverified_from_current_local_bytes` | 3 expected identitiesはcurrent local bytesとhash一致。raw bytesはignoredのまま |

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

provenanceを見ながらA/B/Cのvisual directionを人が選びます。Route Aは推奨のままで、まだ選択・実装されていません。script、YMM4、render、production、publication、rights actionはこの来歴retrofitでは変更していません。
