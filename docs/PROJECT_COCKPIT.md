# NLMYTGen Project Cockpit

Project-State-ID: episode-002-ymm4-diagnostic-placeholder-proof-observed-v1
State-Revision: 2026-07-11.2
Updated: 2026-07-11 JST
Product-State: episode-002-ymm4-diagnostic-placeholder-proof-observed
Product-Gate: supervisor-next-slice-decision
Recommended-Next: decide-real-input-or-integration
External-State: public-repo-feature-branch

このページはpublic repositoryで現在地を読むための追跡済みMarkdownです。
内部capsuleは[runtime-state.md](runtime-state.md)、履歴は
[project-context.md](project-context.md)、task経路は
[THREAD_REGISTRY.md](THREAD_REGISTRY.md)、product pipelineは
[PROJECT_PIPELINE.mmd](PROJECT_PIPELINE.mmd)にあります。これらは状態の保存・案内面であり、
開発セッションのPromptやWorker実行権限を定義しません。

## いまの一文

Episode 002は、derived CSVの自動character bindingと9件のVoiceItem/linked subtitle、
別認可のdiagnostic projectにある3件ずつのImageItem/独立TextItemを、YMM4
`4.53.0.9`で実観測済みです。次のgateは実素材置換またはbranch統合のどちらへ
進むかを決めるsupervisor decisionであり、どちらも自動開始しません。

## 現在の状態

| 対象 | 現在地 | 次に進む条件 | まだ保証しないこと |
| --- | --- | --- | --- |
| speaker identity | canonical `れいむ` / `まりさ`を維持し、explicit profileで`ゆっくり霊夢` 3件 / `ゆっくり魔理沙` 6件へ自動bindingされたことを実観測 | 未定義speakerを追加する場合はprofileを明示更新 | 全YMM4環境のuniversal default |
| derived CSV | mapping dialogなしでclean import、9 VoiceItems、linked text/order維持、2790 frames / 46.50秒 | CSV gateとして追加作業なし | ImageItem/独立TextItemをCSVが生成すること |
| CSV contract | `VoiceItem + linked_subtitle`だけのgateとしてreceipt v2がpassed | 実素材へ進む場合は別のverified inputを受領 | diagnostic projectのproduction適合性 |
| diagnostic project | YMM4 reopenで9 VoiceItems維持、3 ImageItems、3 independent TextItems、S1/S2/S3 non-final labelを観測 | production化ではなく次のsupervisor decisionへ戻る | final design、public-ready、production `.ymmp` |
| portability | local `.ymmp`は絶対asset referenceのためignored。generator、PNG、manifest、readback、GUI receiptを追跡 | portable projectが必要ならYMM4 reference方式を別途解決 | ignored local project自体のportable commit |
| 実素材置換 | intake契約はあるが検証済み候補ゼロ | source / transcript / provenance / rights context / stable identity / cue alignmentを受領 | sample inputをreal inputと扱うこと |

## 次に選べる入口

| 入口 | 解くbottleneck | 選ぶと可能になること |
| --- | --- | --- |
| **Advance** | diagnostic sampleから実素材へ進めない | 必要入力を受領・検証してreal-input replacementを開始できる |
| **Integrate** | feature/default branchの関係が未判断 | 最新diffを監査し、安全な統合方針を選べる |

diagnostic proofの成功は、どちらの入口も自動認可しません。次のstate transitionは
supervisorがreal-inputまたはintegrationを選んだ後にだけ開始します。

## 証拠境界

- CSV gate receipt v2:
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_csv_gate_observation_receipt_2026-07-11.json`
- tracked diagnostic proof:
  `production_pilots/yukkuri_newsroom_content_spine_002/ymm4_diagnostic_placeholder_proof/`
- canonical CSV SHA-256:
  `6FBB4666028DF4EF61F19C29505563141B1A82E932DC8E05BF8168F06347D38C`
- derived CSV SHA-256:
  `5452DE96DC6EF012400A132BA5BAE80B8553C1B1CDD27860D36674C25AF391BC`
- immutable prior receipt SHA-256:
  `DC756D9C4EE9ABDFDDFB284B2B8EC70B227DDEB5E365C1BBB8EE8438D8C9A5B5`
- GUI observation: YMM4 `4.53.0.9`でCSV gateとdiagnostic project reopenが
  passed。screenshotは未取得で、今回の必須gateではない。

## 公開境界

このページにはprivate URL、token、raw source、article body、権利未確認素材、
ローカルuser-home絶対pathを載せません。render、production `.ymmp`、real-input
replacement、rights approval、final thumbnail、upload、default-branch integrationは
対応する証拠と明示的な次slice判断が揃うまで未完了です。
