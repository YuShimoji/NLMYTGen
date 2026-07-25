# 第2実トピック Factory Validation — 監修AI向け現状報告

日付: 2026-07-25 JST
対象branch: `codex/nlmytgen-second-real-topic-factory-v1`
required base: `02e5464c0f7d0ce90a198e788a336cb201682e9b`
Project-State-ID: `nlmytgen-second-real-topic-gui-render-validated-v1`

## 結論

第2実トピック`REINSと不動産情報流通の仕組み`は、tracked package作成から
Electron 43 GUI、deep runtime doctor、write-free dry-run、実YMM4 render、
MP4 normalization、media validation、結果readbackまで完走した。

本結果により、new-banknoteとREINSという2つの異なる実題材が同じ標準制作契約を
通過した。NLMYTGenは単一デモ専用状態を越え、
`two-distinct-real-topics-through-one-gui-and-video-pipeline`へ到達した。

ただしREINS動画は`internal_factory_canary_not_human_accepted`である。技術検証の
成功は、人のcreative acceptance、素材権利、production、publication、external
upload、release、PR、merge、master integrationを承認しない。

## Gitと保全状態

- source branch exact tipから対象branchを作成した。source parityは作業開始時`0/0`。
- original G-27 candidate
  `samples/_probe/g24/real_estate_dx_csv_import_base.ymmp`はSHA-256
  `748f67e4da63728b3fb6f855924a7c3d7a60780bf31472e41a743e69ae76b3ba`
  のまま。
- pre-existing untracked `.playwright-mcp/`、`artifacts/`、
  `phase-e-01-contact-acquired*.png`は変更・stage・削除していない。
- source media、source project、render runs、GUI screenshotsはignored local
  evidenceのまま。public Gitにはtracked contractとsanitized receiptだけを置く。
- PR、merge、master mutation、release、deployment、public uploadは実行していない。

## 第2トピックの入力形状

| 項目 | REINS canary | accepted new-banknote |
| --- | ---: | ---: |
| cues | 7 | 9 |
| scenes | 4 | 3 |
| speaker distribution | Reimu 4 / Marisa 3 | Reimu 3 / Marisa 6 |
| timeline | 2725 frames | 4415 frames |
| nominal duration | 45.4167秒 | 73.5833秒 |
| real media | 7 raster assets | 9 real-media assets |
| run identity | `real_estate_reins_internal_review_v1` | `new_banknote_real_media_review_v1` |

この差分により、2本目は同じ件数・同じscene構造を複製したcanaryではない。

## Sourceと内容変換

raw inputは`不動産DX_魔法の鍵とキュレーション.txt`、segment/risk discoveryは
G-27 review packetを使用した。両者は事実正本ではない。

発話事実は以下4 surfaceまでに限定した。

1. 東日本不動産流通機構 `レインズってなに？`
2. 東日本不動産流通機構 `媒介契約制度`
3. 東日本不動産流通機構 `売却依頼主様向け説明ページ`
4. 国土交通省 `レインズの機能強化`売主向け資料

canonical scriptは7 cues、4 scenes、Reimu 4 / Marisa 3。質問cueを除く6 factual
cuesは全てclaim IDとprimary source IDを持つ。unsupported spoken factual unitは0。
rawに含まれたVIP比喩、全物件一元化、portal subset、非公開理由の断定、悪意・
犯罪・税務・定量予測は除外した。

tracked package:

- `canonical_script.json` / `.txt`
- `canonical_yymm4.csv` / `derived_yymm4_import.csv`
- `source_claim_registry.json`
- `source_support_edges.json`
- `transformation_ledger.json`
- `real_estate_reins_media_provenance.json`
- `real_estate_reins_episode_manifest.json`
- `technical_validation_receipt.json`

## Real media

公式surfaceから7 raster capturesを作成し、各cueへ1対1で結合した。source hashは
7件すべて異なり、SVG参照は0。asset recordはsource ID、capture範囲、SHA-256、
rights state、production/publication falseを持つ。

素材は内部技術レビュー用であり、再利用許諾を示すものではない。source mediaは
Git追跡対象外の`auto_video_runs/source_media_real_estate_reins_v1/`に保持する。

## YMM4 source projectと自動化

YMM4 4.54.0.1を実起動し、speaker combo、セリフ入力、row add、voice generationを
Windows UI Automation patternで実行した。source projectは7 VoiceItems、2725 frames、
4/3 speaker splitを持つ。

driverのportable/automation修正:

- CSVの任意行数を2-column row builderとして処理。
- `SendKeys`とkeyboard/mouse injectionを完全除去。
- output mode/audio bitrateはExpandCollapse / SelectionItem patternで選択。
- ComboBoxのWPF peer再生成、generic label、子Text labelを扱う。
- 64 KiB未満のMP4 headerを完成扱いせず、10秒安定まで待つ。
- project filenameが2秒安定して表示されるまでrender開始を待つ。
- character-settings差分dialogは`現在の設定で上書き`を選択し、端末の現在設定を
  変更しない。
- Tachie object構造は維持し、rooted local pathだけをbasenameへportable化。
- YMM4、ffmpeg、Electronのproject-owned process残留は0。

source project SHA-256:
`ed2773ce87a41936dd82d16d666d253f8bdba8763fc11bfa829d4818cb1b3ec9`

## Electron GUI実行

実Electron 43.2.0 main/renderer/preloadをhidden・silentで起動した。

通過した経路:

1. `自動動画生成`を既定surfaceとして表示
2. REINS manifestをaccepted-manifest probe overrideで読込
3. deep runtime doctorを実行
4. protected inputs 9/9 exactを表示
5. 実`build-episode-video --dry-run`をwrite-freeでpass
6. real render jobを開始
7. YMM4 render、normalization、validation、receiptまで完了
8. `生成済み・人の採用判断前`を結果表示
9. 1280x720 / 1920x1080の横overflowなし
10. console / preload / security / renderer error 0

実装中はtracked worktreeがdirtyなのでdoctorはreviewだけready、codeは
`git_tracked_worktree`、render/regenerateはdependency chainでunavailableだった。
通常GUIのfail-closed動作は変えず、probe modeかつ
`NLMYTGEN_STANDARD_LOOP_REAL_RENDER=1`の場合だけreal-render bridgeを許可した。

GUI probe receiptはstatus `passed`、全check true。

## 生成物と検証

generated project:

- SHA-256:
  `ea4bc001068cf0f398d428072b2b94a6b3b1f4beed5ba0efb2b04f0d040e4da8`
- VoiceItems 7 / ImageItems 7
- speaker 4/3
- timeline 2725 frames
- exact text/order
- only-run-directory absolute paths
- protected path leak 0 / SVG 0

final internal-review MP4:

- SHA-256:
  `4c99feed4e487743e5243074c3eca6aad51a7b16392f7f405ce158f038cb5c75`
- 57,508,191 bytes
- H.264 Main / AAC-LC stereo 48 kHz
- 1920x1080 / 60 fps
- 45.416016秒 / 2725 video frames
- overall bitrate 10,130,028 bps
- ISO-BMFF `ftyp` / `moov` / `mdat` pass
- ffprobe pass
- full-file decode pass
- decode前後SHA不変

frame extractionはfirst/middle/lastと7 cueの計10枚、unique SHA count 10。
7 cue frameは全て別SHAで、目視でも公式page/diagram、字幕、speaker labelを確認した。
既存YMM4 character setting由来の大きい赤/黄keyword emphasisは見えるため、
final aesthetic acceptanceはhuman gateに残す。

## Repeatabilityと失敗からの収束

fresh real runを2回行い、次の4 artifactは2回とも同一SHAだった。

- generated project
- final normalized MP4
- local real-media manifest
- cue visual readback

上書きは行わず、途中試行は次のignored siblingへrecoverableに退避した。

- probe root collision
- generated project absolute-path readback failure
- output ComboBox選択 failure
- ComboBox peer-state failure
- empty/one-frame project attempt
- probe修正前の成功run

主な収束:

- probe receiptをrun directory外へ移し、run overwrite refusalを維持。
- null Tachie化を撤回し、object構造を保持してpathだけportable化。
- UIA candidate labelを子Textから読み、input injectionを除去。
- 2 KiB MP4 headerをcompletionと誤認しない下限と安定時間を追加。
- character settings modalとproject-load raceを明示処理。
- 長い実render logからcommand先頭が落ちても、pipeline receiptそのものをGUI
  completion evidenceとして読む。
- existing runのresumeでlocal asset manifest driftを検出した。これはfail-openせず
  fresh runへ切り替えた。resume driftの原因分離は将来のrepeatability sliceに残る。

## 既存accepted cutのidentity保護

作業後にnew-banknoteの4 identityを再計算し、全て既存正本と一致した。

- source project:
  `beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54`
- generated project:
  `244c05ae6fe6179e9dace4b569cd5f3f9f496cfe70d46ac16ac459e787712611`
- accepted MP4:
  `423553e0aff40619ffb0fd88bcc80344417788aa6128f0a8778aefbdd19ca476`
- human acceptance receipt:
  `cd0b4f02fb54cb0b0dbf8625a5baed6db3952b0a7342257c5456d1426e23f4b8`

REINS canaryはnew-banknoteのhuman acceptanceを継承しない。

## 実装前commitのfocused gate

- Python: second-topic static contract、episode pipeline、standard GUI tests
  合計20件pass
- Node: standard production loop contract 6件pass
- .NET Release build: warning 0 / error 0
- GUI real smoke: pass
- JS syntax: pass
- `git diff --check`: pass

outcome commit後のcanonical regressionはrepo-local ruleどおり1回だけ実行し、
最終監修handoffで結果を報告する。

## 残作業

### 第三トピック variation proof

目的はtopic-specific hard-codeの残存を検出すること。効果は3種類目の入力形状に
対するfactory一般性の証明。前提はrightsを未承認のまま扱えるofficial sourceと
新run ID。現在は未着手。次は7/9 cues、3/4 scenes、4/3・3/6以外のshapeを選ぶ。

### 3連続 operator repeatability

目的は一度限りの成功と運用可能性を分離すること。効果はmanual intervention、
process cleanup、artifact SHA、elapsed timeの実測。前提はrun IDを毎回変える
delete-free procedure。現在はfresh 2回のartifact一致まで。次は3回連続のGUI receiptを
1つのaggregate receiptへ束ねる。

### Resume drift原因分離

目的はsafe resumeの再生成物差分を説明可能にすること。効果は中断復旧の信頼性向上。
前提は現成功runの不変copyとlocal manifest field-by-field diff。現在はfail-closed検出済み。
次はtimestamp、path、materialization metadataをcontent identityから分離する。

### Human aesthetic review

目的は字幕、keyword emphasis、source pageの可読性を人が採否判断すること。効果は
technical canaryからcreative candidateへの昇格可否。前提はexact MP4 SHA固定と通し視聴。
現在はmachine/spot visual passのみ。次はcue ID付きでaccept/repair/rejectを返す。

### Rights and production replacement

目的はofficial page captureの内部技術利用と公開利用を分離すること。効果はproduction
assetとして扱える権利台帳。前提は権利者・利用条件の人間判断。現在は全asset
production/publication false。次は許諾済み素材または自作再構成へ置換し、新SHAで再reviewする。

## 条件付き長期目標

### Goal 1 — 第三形状または3連続運用

現Product-Gateを閉じる。variation routeとrepeatability routeのどちらを先に選んでも、
既存2本のidentity不変、manual interventionの記録、private artifact非追跡を必須にする。

### Goal 2 — Factory contract v2

3本の実例から共通schemaとtopic-specific extensionを分離する。source registry、
claim edge、canonical script、media provenance、YMM4 project、GUI receiptの必須fieldを
versioned contractにする。

### Goal 3 — Recoverable operator loop

run plan、collision、resume、fresh rerun、failed attempt archive、process cleanupを
1つのoperator procedureへ統合する。deleteやforceを通常手順に含めず、各runの
identityと失敗地点をreceiptで追えるようにする。

### Goal 4 — Cross-topic quality corpus

3本以上のaccepted/repair/reject結果をcue-level corpusへまとめる。字幕可読性、
source crop、情報密度、emphasis、scene variationをmachine checkとhuman judgementに
分離し、次topicのpreflightへフィードバックする。

### Goal 5 — Rights-cleared production candidates

技術canaryとは別identityで、許諾済み/自作素材、production registry、human creative
acceptanceを揃える。素材差し替えは新SHA・新review identityとして扱う。

### Goal 6 — Bounded batch operation

単一job所有、silent policy、resource limit、queue、cancel、restartを維持したまま、
複数episodeの内部レビュー生成をbounded batchとして扱う。失敗runは他episodeへ
波及させない。

### Goal 7 — Release candidate governance

code、dependency、security、content、rights、human acceptanceを独立gateとして束ねる。
technical greenだけでproduction/publicationを昇格しないrelease checklistを作る。

### Goal 8 — Controlled publication integration

明示的なpublication authorityが与えられた場合だけ、upload credential、metadata、
dry-run、private preview、rollbackを別sliceで実装する。現branchの成功はこの権限を
与えない。

### Goal 9 — Operational observability

topic数、成功率、manual intervention、平均render時間、resume率、drift率、
human repair率を個人情報やprivate sourceを含めず集計する。異常をtopic/cue/runへ
遡れるようにする。

### Goal 10 — 継続運用品質

YMM4/Electron/Node/Python更新ごとにcompatibility branchで検証し、accepted artifactを
再生成せずrollback可能にする。dependency/security更新とcreative changeを同じ
commitへ混ぜない。

## 監修判断

技術的には第2実トピックfactory validationをclose可能。次の製品判断は
`third-topic-variation-or-three-run-operator-repeatability`のどちらを先に実行するか。
human acceptance、rights、production、publicationは明示的な別判断が必要である。
