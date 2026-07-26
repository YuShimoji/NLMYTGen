# NLMYTGen Project Cockpit

Project-State-ID: nlmytgen-factory-contract-v2-validated-v1
State-Revision: 2026-07-26.3
Updated: 2026-07-26 JST
Product-State: three-topic-evidence-extracted-into-versioned-executable-factory-contract
Product-Gate: fourth-topic-out-of-sample-validation
Recommended-Next: run-fourth-topic-through-factory-contract-v2-with-unobserved-input-axis
External-State: public-repo-feature-branch
Development-Audio-Policy: silent_by_default
Handoff-Branch: codex/nlmytgen-factory-contract-v2-v1
Handoff-PR: none
Required-Base: aad0043d1218cdfae8027160cd57651b04fec2ef
Implementation-Checkpoint: aad0043d1218cdfae8027160cd57651b04fec2ef
Outcome-Commit: resolved-by-current-branch-tip
Remote-Parity: 0/0 required after handoff push
Tracked-Worktree: tracked clean required after handoff; protected and ignored artifacts preserved

短期正本は[runtime-state.md](runtime-state.md)、詳細証跡は
[FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.md](verification/FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.md)、
機械可読結果は
[FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.json](verification/FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.json)、
判断履歴は[project-context.md](project-context.md)。

## いまの一文

3実トピックの既存証拠を、tracked-onlyでも実行できるversioned Factory Contract v2へ
抽出し、live identityと同一v1 pipeline dry-runを分離して再検証した。

## 判断に使える現在地

| 対象 | 現在状態 | 境界 |
| --- | --- | --- |
| Contract | `nlmytgen.factory_package.v2` | observed 3 packages限定 |
| Inventory | 50 fields / 7 classifications | sourceとconsumerを各行に記録 |
| Descriptors | new-banknote / REINS / AIの3本 | v1 authority exact SHA binding |
| Determinism | 2 repeats、3/3 exact | known topic ID coupling 0 |
| Live profile | 9/9 identity hash exact | availabilityを別clockで評価 |
| Tracked-only | 3/3 pass、9 receipt-only | private file不存在はcontract failureにしない |
| Pipeline bridge | 3/3 dry-run、content identity exact | render / YMM4 / Electron 0 |
| Tests | Python 51/51、Node 7/7 | negative contract coverage 16 axes |
| Human authority | new-banknoteのみaccepted exact | REINS / AIは未accept |
| Public authority | rights / production / publication false | technical passから継承しない |

## 次の入口

既存3件に無い入力軸を持つ第4トピックをFactory Contract v2へ通し、
out-of-sample validationを行う。source / claim / media / rights境界、
validator、tracked-only、live profile、dry-runを先に通し、owner許可がある場合だけ
normal production loopへ進む。

## 公開・実行境界

現在の成果はbounded technical factory-contract evidenceである。universal
compatibility、REINS / AI human acceptance、rights、production、publication、
upload、release、PR、merge、master mutation、deployment、access change、
public exposureは未承認・未実施。
