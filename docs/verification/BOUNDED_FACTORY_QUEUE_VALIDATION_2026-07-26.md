# Bounded Factory Queue and Render-on-change Validation

Date: 2026-07-26 JST

Source:
`codex/nlmytgen-factory-contract-v2-lifecycle-v1` at
`88db8b84e8863aed366fd1683ddcfcc548a0b2a6`

Target:
`codex/nlmytgen-bounded-factory-queue-v1`

Mission:
`bounded-factory-queue-render-on-change-v1`

Audio:
`silent_by_default`

## 結論

4 packageを個別に検証してcallerが次stageを手動判断していた状態から、
mixed v2.0 / v2.1 descriptorを一度にnormalizeし、technical decisionと
execution authorityを分離して返すbounded queueへ進んだ。

live Thank-terminalではnew-banknote、REINS、AI-monitoringが
`verified_noop`、food-expiryだけが
`source_project_generation_required`になった。render候補、render schedule、
execution setはすべて0である。

tracked-only checkoutでは完了3件のprivate outputが無くても
`recorded_complete_no_live_file`となり、`render_required`へ昇格しない。
food-expiryは`package_prepared`を維持し、唯一のsource-project候補である。

safe-stage modeは既存episode dry-run 3件とpre-render plan 1件だけを実行した。
YMM4、Electron、render driver、ffmpeg encode、playback、system volume、
source-project generation、product write、private copyは0である。

## Queue contract

| Field | Value |
| --- | --- |
| Schema | `nlmytgen.factory_queue.v1` |
| Version | `1.0` |
| Queue ID | `four_package_lifecycle_queue_v1` |
| Declared maximum | 4 |
| Hard maximum | 32 |
| Observed packages | 4 |
| Ordering | priority descending, then explicit order ascending |
| Duplicate package ID | reject |
| Duplicate content identity | reject unless one immutable reference is explicit |
| Target collision | reject |
| Default execution | plan only |

Schema SHA:
`2266c033463be721827d82746483d9008dac48a36224e5c8d0a5a932eff81e36`

Queue descriptor SHA:
`2cfbdab4bf3bfb765afa8909b54212311155ba85c3838078a1e0aac77a11375f`

各entryはdescriptor locatorだけでなく、expected package ID、semantic content
identity、render-settings identity、completed output identityを保持する。
これにより現在のdescriptor自体が内部整合していても、queue baselineからの
semantic driftを検出できる。

run ID、timestamp、PID、elapsed time、local directory、machine pathは
semantic change判定から除外する。

## Live four-package decision

| Package | Lifecycle | Live state | Technical decision | Execution |
| --- | --- | --- | --- | --- |
| new-banknote | `human_accepted` | completed output exact | `verified_noop` | false |
| REINS | `rendered` | completed output exact | `verified_noop` | false |
| AI-monitoring | `rendered` | completed output exact | `verified_noop` | false |
| food-expiry | `package_prepared` | prepared inputs exact | `source_project_generation_required` | false |

Live evaluation SHA:
`52149bc8f1f3793586bc1d59dd31839d3dabb79266b7f7023339b9582a826229`

Counts:

- verified no-op: 3
- recorded-complete unavailable: 0
- source-project candidates: 1
- render candidates: 0
- blocked / invalid: 0
- scheduled render: 0
- execution set: 0

food-expiryのtechnical next stageは明示されるが、
`source_project_generation_authorized=false`である。
technical capabilityはowner authorityを付与しない。

## Render-on-change rules

### `human_accepted`

- exact live artifact: `verified_noop`
- receipt only: `recorded_complete_no_live_file`
- semantic / render-settings drift: `blocked_identity_drift`
- hash mismatch / corrupt output: `blocked_corrupt_output`
- accepted artifactを上書きまたは自動再renderしない

### `rendered`

- exact live output: `verified_noop`
- receipt only: `recorded_complete_no_live_file`
- semantic or render-settings change: `render_required`というplanだけ
- corrupt output: `blocked_corrupt_output`
- render authorityは別clock

### `source_project_ready`

- valid source projectとrender不存在: `render_required`
- completed output exact: `verified_noop`
- recorded sourceだけの別端末状態でもsource projectを自動再生成しない

### `package_prepared`

- source project absent: `source_project_generation_required`
- `render_required`へ直接昇格しない
- queue authority falseの間はexecution setへ入れない

## Tracked-only result

proposed indexを`C:\nq1`へ一時展開し、検証後に削除した。
machine-readable receiptにはこのabsolute pathを含めていない。

- proposed-index files: 2977
- Git metadata: absent
- `node_modules`: absent
- private MP4: 0
- private absolute path in queue output: false
- package contracts: 4/4 valid
- completed decisions:
  `recorded_complete_no_live_file` 3
- source-project candidates: 1
- render candidates / schedule / execution set: 0
- evaluation SHA:
  `8a7e88e63ba064b3ddb51080e165cadc8851e24ed3ee4a4fc68852cb6482a7a1`

tracked-only evaluationは2回raw exactだった。live file absenceはavailabilityの低下であり、
contract failureやregeneration authorityではない。

## Safe-stage result

`evaluate-factory-queue --check-live --execute-safe-stages`を2回実行した。

- existing episode pipeline dry-run: 3
- pre-render stage plan: 1
- content identity exact: 4/4
- product writes: 0
- controlled process launches: 0
- raw output repeat exact: true
- safe-stage SHA:
  `12ba7071c8a41095023b4cbeb548b77b40efcfcf363aec203f953168dac8be58`

safe-stage outputはusername、drive letter、private absolute path、credentials、
private media、process command lineを含まない。

## Negative evidence

queue固有31 testsは次をfail closedまたは明示no-opとして確認した。

- duplicate package ID
- duplicate content identity
- queue maximum exceeded
- duplicate / non-contiguous order
- private absolute descriptor path
- unknown queue version
- unknown package schema
- contradictory lifecycle flags
- accepted semantic identity drift
- rendered live output hash mismatch
- run-local-only difference
- package-prepared direct render promotion
- receipt-only completed rerender
- technical action without execution authority
- known topic-ID coupling
- no-op entry in execution set
- safe-stage product write

Factory Contract v2.0 / v2.1、queue、episode dry-runを合わせたfocused setは
97/97 passした。

## Preservation

開始時と検証後で次のbytesは一致した。

| Artifact | SHA-256 |
| --- | --- |
| v2.0 schema | `d0e831c60ceba17a83c6fe106bf1fa574cfa3881976934c3fb4571a59bb8dfbb` |
| v2.0 inventory | `8bc3a669e0b77b2dcc68f59f0f5bcf03fe6eaaaaf8aec3bad4fb3b814f6490d4` |
| v2.1 schema | `5f9e84c115ac8a7618f57714a8df3722b2cdb83371711c40efb77caf2bd12d44` |
| v2.1 inventory | `fdf17bac964941c8c879595b8ec2003fcd9c959f1dbe105b4b1a13b1276b35f3` |
| new-banknote descriptor | `80f1130711a46c3f3a77f2ec1da391fd338569d9aaf0385deeb96a2a698333f7` |
| REINS descriptor | `21e0052011b1d55f7ff27bf63af5c4f79dbc3932762df86375cdca86e59d63db` |
| AI-monitoring descriptor | `866f03c7cff7570e1ad9d1b22525598a99084e9aa0b5227c4c2d31cea528eeb4` |
| food-expiry descriptor | `18e078f6f6c5b6e17808ec9378d8476a9cd8ce426cd1281563c833ae21acf329` |

existing manifests、scripts、projects、MP4s、receipts、media、accepted decisions、
run directories、dependency locks、ignored evidenceは変更していない。
pre-existing untracked 18 filesも保持した。

## State and next bounded stage

Project-State-ID:
`nlmytgen-bounded-factory-queue-render-on-change-validated-v1`

Product-State:
`lifecycle-aware-four-package-queue-with-complete-package-no-rerender-policy`

Product-Gate:
`advance-prepared-package-to-source-project-ready`

Recommended-Next:
`advance-food-expiry-package-to-source-project-ready-through-queue`

次は新しいtopicやqueue再設計ではなく、ownerが明示許可した1件の
food-expiry source project generationである。同じcontent identityを維持し、
source project path / SHAをexactに追加して`source_project_ready`へ進める。

その後のrender、human creative acceptance、rights、production、publication、
upload、releaseは独立した未承認gateである。今回の成果はgeneric distributed
schedulerやuniversal / production-ready schedulingを証明しない。
