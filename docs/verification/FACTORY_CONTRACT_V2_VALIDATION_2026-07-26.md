# Factory Contract v2 Validation — 2026-07-26

## 結論

`nlmytgen.factory_package.v2` を、観測済みの new-banknote、REINS、
AI workplace-monitoring の3 packageから抽出した。契約はJSON Schema、機械可読
field inventory、descriptor-driven read-only validator、3本のpackage descriptor、
CLIから成る。3件とも既存v1 authorityを変更せずにvalidateと同一v1 pipelineの
dry-runを通過した。

この結果が証明する範囲は「観測済み3件の証拠を一つのversioned executable
contractで表現し、決定的に再検証できる」までである。第4トピック、
universal arbitrary-topic compatibility、production readiness、rights、
publication、releaseは未検証または未承認である。

機械可読な正本は
`docs/verification/FACTORY_CONTRACT_V2_VALIDATION_2026-07-26.json`。

## 取得元と実行境界

- source branch: `codex/nlmytgen-third-real-topic-factory-v1`
- exact source HEAD: `aad0043d1218cdfae8027160cd57651b04fec2ef`
- target branch: `codex/nlmytgen-factory-contract-v2-v1`
- target remote: 開始時点では不存在
- source tracked state: clean、upstream parity 0/0
- 実行した処理: tracked JSON / YMMP authorityの読取り、validator、
  pipeline dry-run、focused tests
- 実行していない処理: Electron GUI、YMM4、render、media playback、
  network access、private media transfer、第4トピック、public operation
- audio policy: `silent_by_default`

## 契約面

| 面 | 実装 | 読み手への効果 |
| --- | --- | --- |
| package schema | `schemas/factory_contract_v2/factory_package_v2.schema.json` | required sectionとunknown field拒否を固定 |
| field inventory | `schemas/factory_contract_v2/field_inventory.json` | 50 fieldsをrequired / variable / optional / forbidden / topic-extension / run-local / evidence-onlyへ分類 |
| validator | `src/pipeline/factory_contract_v2.py` | field-level errorとconsumer effectを返し、v1 authorityをread-only検証 |
| validation CLI | `validate-factory-package` | tracked-onlyとlive hash profileを同じ入口から確認 |
| pipeline bridge | `build-episode-video --factory-package ... --dry-run` | 新しいrender経路を作らず既存v1 pipelineへ接続 |
| descriptors | 各packageの`factory_package_v2.json` | v1 manifest / claims / canonical / provenance / receiptをexact SHAで結合 |

契約sectionは source intake、claim support、canonical content、shape、
media provenance、episode execution、source project、generated project、
render validation、content identity、resume identity、human decision、
rights / production / publication / upload authority、namespaced extensionsに分離した。

field inventoryの分類数は required 19、variable 10、optional 5、
forbidden 7、topic-extension 2、run-local 3、evidence-only 4。各行にsource
artifact、observed value、consumer、migration rule、validation rule、
absence可否、content/run/authority clockへの影響を記録した。

## 3 packageの決定的identity

| package | cues / scenes | descriptor SHA | normalized SHA | content identity |
| --- | ---: | --- | --- | --- |
| new-banknote | 9 / 3 | `80f113...33f7` | `64c5c0...d32` | `50772a...4cf0` |
| REINS | 7 / 4 | `21e005...3db` | `3faccd...e4ac` | `15375b...5c06` |
| AI monitoring | 5 / 2 | `866f03...eb4` | `125bef...081` | `dfb6ad...485cf` |

各descriptorを2回ずつvalidateし、descriptor SHA、normalized SHA、
content identityが3/3 exactだった。shared validator内のknown topic IDは0で、
topic固有差分はdescriptorとnamespaced extensionへ閉じた。

## Live / tracked-only / pipeline dry-run

live profileは3 packageのsource project、generated project、MP4を合計9件
rehashし、9/9が`live_file_hash_exact`だった。before / afterのSHA、size、
mtime mismatchは0である。

proposed indexだけをGit metadataなし・`node_modules`なしの短い隔離rootへ2948件
展開したtracked-only profileでも3/3 passed。private/ignored実体が存在しない
9 identityは契約不成立にせず、すべて`receipt_only_no_live_file`と明示した。
receiptは過去のexact identityを証明し、現在のlive availabilityは主張しない。

3 descriptorを`build-episode-video --factory-package ... --dry-run`へ渡し、
既存`run_episode_video`経路で3/3 passed。content identityは3/3 exact、
`render_requested=false`、render stage 0、YMM4 / Electron launch 0、
playback 0、network 0、v1 tracked mutation 0だった。factory-package入力で
`--render`、`--resume`、`--force`、明示run-idを要求するとfail closedする。

## Negative coverage

focused Python suiteは51/51、standard-loop Node contractは7/7 passed。
Factory Contract固有24 testsは、必須section欠落、unknown/unversioned field、
absolute/private path、accepted decisionの別artifact継承、authority record欠落、
receipt-onlyからのlive claim、cue-media gap、factual-claim partition gap、
run-local値のcontent identity混入、unnamespaced extension、authority hash drift、
live hash drift、topic coupling、v1 mutation、render要求、unobserved-axis
overclaimを決定的に拒否する。

一度だけ既存Job Object testがPIDファイルの生成直後の空文字を読み、
整数変換で失敗した。同一testの単独再試行とfocused suite全体の再実行はpassし、
Factory Contract変更に対応する再現障害は確認されなかった。

## Human / rights / production authority

new-banknoteだけが既存のexact human decision receiptとexact MP4に結合された
`stable_internal_cut`である。REINSとAI monitoringは
`internal_factory_canary_not_human_accepted`のままであり、new-banknoteの判断を
継承できない。

rights、production、publication、upload、releaseは独立clockである。
falseは技術成功から変更されず、trueへ進むには対象artifactに結合したexact
authority recordが必要になる。技術validatorは人の創作判断、権利判断、
production判断、公開判断を代行しない。

## Migration / rollback

移行は既存v1 packageへdescriptorを1本追加し、既存authority pathとSHAを参照する
read-only adapter方式である。v1 manifest、canonical、claim edges、provenance、
source/generated project、technical receiptのschemaやbytesは変更していない。
新規packageはv2 descriptorを先に作り、field-level validationを通した後に
dry-runへ進める。

rollbackは3 descriptor、schema、inventory、validator module、CLI subcommand /
factory-package bridgeを取り除けばよい。既存
`build-episode-video --episode ...`の契約は保持され、既存rendered artifactを
restoreまたはrerenderする必要はない。v2の削除はhuman / rights / production /
publication authorityを変更しない。

## 次のゲート

Project-State-IDは`nlmytgen-factory-contract-v2-validated-v1`。
Product-Gateは`fourth-topic-out-of-sample-validation`。

次は、既存3件に無い入力軸を最低1つ持つ第4トピックを選び、
`nlmytgen.factory_package.v2`へ適合させる。実行前にsource/claim/media/rights
境界を用意し、validator → dry-run → owner-authorized production loopの順で進める。
第4トピックの成功後もuniversal claimは自動成立せず、観測した新しい軸だけを
inventoryと契約へ還元する。
