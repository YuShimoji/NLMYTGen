# Factory Contract v2.1 Pre-render Lifecycle Validation

Date: 2026-07-26 JST
Launch-Set: `nlmytgen-factory-contract-lifecycle-2026-07-26`
Mission: `factory-contract-v2-prerender-lifecycle-out-of-sample-v1`
Source: `codex/nlmytgen-factory-contract-v2-v1` at
`ab960978ab1c29fc8ea5d59d69dc185ddc0d257a`
Target: `codex/nlmytgen-factory-contract-v2-lifecycle-v1`
Audio: `silent_by_default`

## 結論

Factory Contract v2を後方互換のv2.1へ拡張し、packageがrender後でなくても
実在するsource、claim、canonical、media provenance、episode planを持つ
`package_prepared`として検証できるようにした。

固定された第4トピック「賞味期限と消費期限の違い」は、4 cues、1 scene、
霊夢のみ4 cues、official primary source 2、real raster asset 2、異なるcropを
使う4/4 cue-media mapping、24秒のplanned timelineを持つ。
source projectはplanned、生成物・render receipt・MP4・human decisionは存在しない。

live profileでは2/2 raster assetがexact SHA、tracked-only profileでは同じ2件を
`receipt_only_no_live_file`として扱い、contract validityとlive availabilityを
分離した。既存CLI経路のpre-render planはsource-project generation前に正常停止し、
YMM4、Electron、render driver、ffmpeg encode、playback、system volume操作、
tracked/private artifact writeを行っていない。

この結果は第四トピックのpre-render lifecycleだけを証明する。
post-render lifecycleの第四トピック適合、任意トピックへの普遍互換性、
human acceptance、rights、production、publication、upload、releaseは証明しない。

## 変更の目的と効果

v2.0は観測済み3 packageがすべてrender後だったため、generated project、
technical render receipt、MP4 identity、human decision objectをroot contractへ
常に要求していた。この形では、正当なpre-render packageを表すためにdummy evidenceを
作るか、contract validationをrender後まで遅らせる必要があった。

v2.1はlifecycleを次の4状態へ明示化した。

1. `package_prepared`
2. `source_project_ready`
3. `rendered`
4. `human_accepted`

各状態の証拠は条件付きで要求する。存在しない段階のgenerated project、
render receipt、human decisionは省略し、placeholderやdummy objectを許容しない。
rights、production、publication、upload、releaseはlifecycleから独立したclockを
維持する。

## Schema change table

| Rule | v2.0 | v2.1 | 因果 | 主なconsumer | Migration / rollback |
| --- | --- | --- | --- | --- | --- |
| lifecycle明示 | 完了済みrender packageを前提 | 4状態を順序付きで宣言 | pre-renderの真の状態が必要 | intake / queue / render-on-change | v2.0をread-only normalize。rollbackはv2.1追加物を外す |
| generated project条件化 | 常に必須 | `rendered`以降だけ必須 | project生成前にもcontractを検証する | queue / source-project stage | v2.0 identityは変更しない |
| render evidence条件化 | 常に必須 | `rendered`以降だけ必須 | contract作成がrenderを強制しない | dry-run / render planner | v2.0 receiptをexactに保持 |
| human decision条件化 | 未accept placeholderも常在 | `human_accepted`だけexact receipt必須 | evidence不在をdecisionに偽装しない | review / release | v2.0未acceptは`rendered`へnormalize |
| shape一般化 | 観測3件は2 speakers中心 | 1 speaker以上、asset再利用可 | 観測shapeを普遍要件にしない | package / media planner | v2.0 shapeを書き換えない |
| public authority独立 | 5 clocksを分離 | lifecycleから継承禁止を維持 | technical maturityは公開権限ではない | rights / production / release | v2.0 clockをread-only copy |

Versioned inventoryはv2.0の50 rowsをexact baseとして参照し、v2.1 deltaを
16 rows、schema changeを6 rows記録する。

## v2.0 backward compatibility

変更前のbytesを再hashし、次の値がsource revisionと一致した。

| Artifact | SHA-256 |
| --- | --- |
| v2.0 JSON Schema | `d0e831c60ceba17a83c6fe106bf1fa574cfa3881976934c3fb4571a59bb8dfbb` |
| v2.0 field inventory | `8bc3a669e0b77b2dcc68f59f0f5bcf03fe6eaaaaf8aec3bad4fb3b814f6490d4` |
| new-banknote descriptor | `80f1130711a46c3f3a77f2ec1da391fd338569d9aaf0385deeb96a2a698333f7` |
| REINS descriptor | `21e0052011b1d55f7ff27bf63af5c4f79dbc3932762df86375cdca86e59d63db` |
| AI-monitoring descriptor | `866f03c7cff7570e1ad9d1b22525598a99084e9aa0b5227c4c2d31cea528eeb4` |

v2.1 dispatcherはv2.0 validatorをそのまま呼び、結果をread-onlyでnormalizeする。
new-banknoteは`human_accepted`、REINSとAI-monitoringは`rendered`へ写像した。
shared validator内のknown topic IDは0である。

## 第四package

Package:
`production_pilots/factory_canaries/food_expiry_labels_001/`

| Axis | Observed value |
| --- | --- |
| Lifecycle | `package_prepared` |
| Cue / scene | 4 / 1 |
| Speaker | `ゆっくり霊夢赤縁`: 4 |
| Source / asset | 2 / 2 |
| Cue-media binding | 4/4 |
| Asset reuse | CAAとMAFF各1 rasterを異なるcropで2回使用 |
| Timeline | 1440 frames、60fps、24.0秒 planned |
| Source project | planned、path / SHAはnull |
| Generated / render / MP4 | absent |
| Human decision | absent |
| Rights / production / publication / upload / release | false |

Descriptor identity:

- file SHA:
  `18e078f6f6c5b6e17808ec9378d8476a9cd8ce426cd1281563c833ae21acf329`
- normalized SHA:
  `5bfebe8c93d18dc546a8fe675de7ad303219ff5654b362c0950e371a6093a234`
- content identity:
  `27165fad6fadaee2e5c247a86758a505c7f5f5797eb7b386d174585622a585c6`
- 2回のread-only validationで3 identityすべてrepeat exact

## Source and claim evidence

取得はlogin、credentials、playbackを使わず、根拠が揃ったofficial surface 2件で
停止した。

1. 消費者庁「期限表示（消費期限・賞味期限）」:
   <https://www.caa.go.jp/policies/policy/food_labeling/food_sanitation/expiration_date/>
   および公式PDF:
   <https://www.caa.go.jp/policies/policy/food_labeling/food_sanitation/expiration_date/assets/food_labeling_cms204_250331_01.pdf>
2. 農林水産省九州農政局「賞味期限と消費期限の違い」:
   <https://www.maff.go.jp/kyusyu/seiryuu/syokuhin/recycle/attach/pdf/251023-4.pdf>

4 spoken factual cuesは4/4 supported、unsupported factual unitは0。
取得PDFと抽出text、rasterはignored local evidenceでありGitへ含めない。
tracked registryはURL、PDF SHA、使用page、support範囲を保持する。

## Media mapping

| Cue | Source / asset | Crop |
| --- | --- | --- |
| cue_001 | CAA / `fel_caa_expiration_definitions` | `[0.04, 0.14, 0.62, 0.18]` |
| cue_002 | CAA / same asset | `[0.04, 0.34, 0.62, 0.23]` |
| cue_003 | MAFF / `fel_maff_expiry_conditions` | `[0.05, 0.08, 0.90, 0.35]` |
| cue_004 | MAFF / same asset | `[0.05, 0.84, 0.90, 0.14]` |

live asset SHAはCAA
`2c06e90c629a3be96b2ce973e81900f128ea63d3a07124714607232166f04517`、
MAFF
`931b2232c9ff611a1ce2d793b98687d606c422c4627e8a76b0acba22afa05e79`。
両方を目視し、定義・条件・開封後の注意を含むofficial PDF pageであることを確認した。
これはrights approvalやpublic-use approvalではない。

## Validation profiles

### Live

- v2.1 package: pass、required lifecycle `package_prepared`
- live raster: 2/2 `live_file_hash_exact`
- protected tracked inputs: 9/9 exact
- source project: `planned_not_generated`
- generated / render: `not_applicable_before_rendered`
- human decision: `not_applicable_before_human_accepted`

### Tracked-only

proposed indexをGit metadataと`node_modules`のない短い隔離checkoutへ展開した。

- isolated tracked files: 2970
- v2.1 fourth package: pass
- v2.0 three descriptors: 3/3 pass through compatibility normalizer
- ignored raster: 2/2 `receipt_only_no_live_file`
- source project: `planned_not_generated`
- tracked contract validity: true

### Pre-render stage plan

既存`build-episode-video --factory-package ... --dry-run` entrypointを使用した。

- status: `pre_render_plan_complete`
- completed video dry-run: false
- successful stop: before `source_project_generation`
- YMM4 / Electron / render driver / ffmpeg encode / playback launch: 0
- system volume operation: 0
- source / generated project、rendered media、tracked/private write: 0

## Tests and fail-closed behavior

- `tests/test_factory_contract_v2_1_lifecycle.py`: 23/23
- `tests/test_factory_contract_v2.py`: 24/24
- v2.0 + v2.1 + episode pipeline focused set: 66/66
- third-topic、standard GUI contract、state syncを含むexpanded Python: 82/82
- standard production loop Node contract: 7/7

negative casesはrendered状態でgenerated projectが無い場合、render receiptが無い場合、
human acceptedにexact receiptが無い場合、rights record欠落、cue provenance gap、
unsupported factual unit、run-local identity混入、private absolute path、
unknown field、lifecycle contradiction、known topic ID coupling、
universal compatibility overclaimをfield-level errorで拒否する。

## Preservation and authority boundary

- v2.0 schema、inventory、3 descriptorsはbyte exact。
- accepted new-banknote、REINS、AI-monitoringの既存render artifactは変更していない。
- `auto_video_runs`を作成していない。
- protected untracked 18 entriesと既存ignored artifactを変更していない。
- YMM4、Electron、render、encode、playback、system volumeを操作していない。
- PR、merge、master mutation、deployment、publication、upload、releaseを行っていない。

## Residual blocker

`FACTORY_CONTRACT_POST_RENDER_LIFECYCLE_OVERFIT`

- Purpose: pre-renderで追加した条件付きevidenceが、実際のsource-project /
  rendered / human-accepted遷移でも同じpackage identityを保つか確認する。
- Effect: 現在はqueue intakeとpre-render planningまで使用できる。第四packageの
  render済み互換性やproduction readinessは主張できない。
- Requirements: ownerの生成・render許可、同じcontent identity、exact source /
  generated project identity、technical receipt、必要なら独立human decision。
- State: open。今回のmissionは`package_prepared`で正常停止した。
- Owner: source-project / renderはproduction owner、human acceptanceはhuman reviewer、
  rightsとpublic clocksは各authority owner。
- Next move: lifecycle-aware queueを先に作り、完了packageを再renderしないpolicyを
  pure planning evidenceで検証する。

## Conditional roadmap

### G1 — bounded multi-episode queue

v2.0/v2.1 descriptorsを混在して読み、normalized lifecycle、content identity、
required next stageだけを返すbounded queueを作る。既存`rendered` /
`human_accepted` packageのrender actionは0にする。

完了条件:

- queue inputは明示リストまたはbounded tracked discovery
- stable orderingとduplicate identity拒否
- `package_prepared`はsource-project候補、`source_project_ready`はrender候補
- `rendered`と`human_accepted`はverified no-op
- planning testはYMM4 / Electron / writes 0

### G2 — render-on-change policy

content identity、render settings、source / generated project identityを比較する
pure decision layerを作る。run-id、timestamp、machine pathは変更判定から除外し、
semantic driftだけをfail closedにする。

完了条件:

- unchanged complete packageは`verified_noop`
- incomplete packageは不足stageと不足evidenceを列挙
- semantic driftは既存outputを上書きせず拒否
- decision receiptはlaunch前に固定

### G3 — authorized lifecycle promotion

ownerが明示許可した場合だけ、同じ第四packageを
`source_project_ready`へ進める。source projectのpath / SHAをexactに追加し、
generated project、render receipt、human decisionはまだ作らない。

### G4 — authorized render transition

production ownerが別途許可した場合だけ、queueが選んだchanged item 1件をrenderし、
`rendered` conditional evidenceとresume identityを検証する。
技術passからhuman acceptanceやrightsを継承しない。

### G5 — independent human and public gates

human reviewerがexact artifactへ`ADOPT / REVISE / REJECT`相当の判断を行う。
rights、production、publication、upload、releaseはそれぞれ独立記録がある場合だけ
clockを進める。これらのgate完了前にpublic exposureを行わない。

## Re-entry

1. target branchをfetchし、`HEAD...@{upstream}=0/0`とtracked cleanを確認する。
2. `AGENTS.md` → `docs/REPO_LOCAL_RULES.md` → `docs/runtime-state.md`を読む。
3. `uv sync --extra dev --locked`で依存を復元する。
4. fourth descriptorを`--require-lifecycle package_prepared --check-live`で検証する。
5. `build-episode-video --factory-package ... --dry-run`が
   `source_project_generation`前で停止することを確認する。
6. 次の実装はG1だけ。render、source-project generation、第五トピック追加は
   別の明示missionまで開始しない。
