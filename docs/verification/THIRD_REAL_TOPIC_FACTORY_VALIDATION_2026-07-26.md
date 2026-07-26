# 第3実トピック Factory Validation 監修AI向け現状報告

日付: 2026-07-26 JST

Project-State-ID: `nlmytgen-third-real-topic-gui-render-validated-v1`

Product-State: `three-distinct-real-topics-through-one-clean-gui-and-video-pipeline`

Product-Gate: `factory-contract-v2-extraction`

Recommended-Next: `derive-factory-contract-v2-from-three-observed-topics`

## 結論

第3実トピック「AIによる職場モニタリングと働く人への影響」を、5 cues、
2 scenes、れいむ2 / まりさ3、26.77秒という既存2件とは異なるshapeで、
clean tracked checkpointからstandard Electron GUIとreal YMM4 render経路へ通した。

doctor 4/4、protected input 10/10、write-free dry-run、normal primary action、
real render、project readback、MP4 validation、full decode、5 cue visual inspection、
completed-run no-op resume、semantic-drift negativeはすべてpassした。manual YMM edit、
Computer Use、SendKeys、keyboard/mouse injection、readiness bypass、render test doubleは
使っていない。

これにより、new-banknote、REINS、AI職場モニタリングという3つの観測済み実トピックが、
互いに異なるcue / scene / speaker / duration / media countで同じpipeline contractを
通ったことを示した。証明範囲はこの3件に限る。universal arbitrary-topic compatibility、
production readiness、rights approval、REINS / AI職場モニタリングのhuman creative
acceptance、publication authorityは示していない。

## Gitと保護境界

- source branch:
  `codex/nlmytgen-three-run-operator-repeatability-v1`
- exact source HEAD:
  `fe6672686625d401a7d2dd77fa9d9935e6036e0a`
- source remote parity at start: `0/0`
- target branch:
  `codex/nlmytgen-third-real-topic-factory-v1`
- target remote at start: absent
- decisive GUI dispatch: tracked clean
- protected local files: `.playwright-mcp/`、`artifacts/`、既存PNGを不変更で保持
- private/ignored roots:
  `source_cache/`、`source_extracts/`、`auto_video_runs/`

target以外のbranchへのpush、PR、merge、master mutation、deployment、release、
publication、access changeは行わない。

## Official sourceとclaim support

採用したprimary source surfaceは3件である。

1. [OECD — Algorithmic Management in the Workplace](https://www.oecd.org/en/publications/algorithmic-management-in-the-workplace_287c13c4-en.html)
   - PDF SHA-256:
     `3080f2d54ecc1ecf540cc7101280399b8a0a9d9b4a23a3ea5361ba23ab37a981`
   - 仕事の割当、進捗測定、評価、意思決定支援のclaimを支える。
2. [EU-OSHA — Artificial intelligence for worker management](https://healthy-workplaces.osha.europa.eu/en/publications/artificial-intelligence-worker-management-implications-occupational-safety-and-health)
   - PDF SHA-256:
     `6008d7a981c3f82afc3a1e8d492c8ab7ac7cdea97883293bc318691dd72becec`
   - autonomy、workload、transparency、worker participationのclaimを支える。
3. [ILO — Algorithmic management of work and its implications in different contexts](https://www.ilo.org/publications/algorithmic-management-work-and-its-implications-different-contexts)
   - PDF SHA-256:
     `eb28f489f5bdb78b34a8f82ea3cda6cd1feece8dc483c1648b912227de85e7a5`
   - cross-checkとcontextual supportに使う。

login、credentials、source audio/video playbackは不要だった。spoken factual
unitsは4、support edgeはすべてadjudicatedされ、unsupported factual unitは0。
2つの問いかけcueはnonfactualとして明示した。

正本:

- `source_registry.json`
- `claim_adjudication.json`
- `source_support_edges.json`
- `transformation_ledger.json`

## Canonical scriptと入力shape

| Cue | Speaker | Scene | Text role |
| --- | --- | --- | --- |
| 1 | れいむ | S1 | モニタリング対象を問うnonfactual導入 |
| 2 | まりさ | S1 | 割当・進捗測定・評価を説明 |
| 3 | まりさ | S1 | skill matchingとdecision informationを説明 |
| 4 | れいむ | S2 | autonomyと負担の確認を問うnonfactual転換 |
| 5 | まりさ | S2 | autonomy・workload・transparency・participationを結ぶ |

tracked canonical artifacts:

- `canonical_script.json`
- `canonical_script.txt`
- `canonical_yymm4.csv`
- `derived_yymm4_import.csv`

canonicalとderived CSVは既存generic arbitrary-row import contractへ適合する。
手入力やtopic-specific row builderは追加していない。

## Real media

5 cueすべてにofficial PDFから抽出した別のraster PNGを割り当てた。

| Cue | Source surface | Asset SHA-256 |
| --- | --- | --- |
| 1 | OECD cover | `bcd2322bb57b5a5397afff44591fd3252c220d41dac0c2961f66f617e3c9e4b3` |
| 2 | OECD uses table | `b2fd6f49801705fa5285c724089f926e30255434416b505f222b6cfb9697ffc0` |
| 3 | OECD decision findings | `0b6e1d224c38423452cc485820fcff5e07b604a392e10185af2e2cd890214b34` |
| 4 | EU-OSHA impacts | `46f13954bc3031a2d2c2793c775e30cc10356b75bb908dc7e2e5242e112f562d` |
| 5 | EU-OSHA participation | `1d72ec2b44d6c79e17fa69ce2bbc23e9e77dfff9fe1307dc5adbd55236c4a501` |

5 selected pagesとILO backup 2 pagesを使用前にvisual inspectionした。
cue provenance 5/5、unique source SHA 5、SVG 0、AI-generated visual 0。
source mediaはGitへ追跡せず、`real_media_provenance.json`でlocator、hash、
source page、usage boundaryを固定した。reuse rightsは未承認であり、productionと
publicationを許可しない。

## Source YMM4自動生成

既存REINS sourceをread-only blank-template sourceとして利用し、timeline itemを
mechanically除去した後、既存の
`Ymm4RenderAutomation import-script` generic arbitrary-row pathで5行をimportした。

- actual YMM4: `4.54.0.1`
- driver: Windows UI Automation
- imported rows: 5/5
- VoiceItems: 5
- speaker distribution: ゆっくり霊夢赤縁2 / ゆっくり魔理沙黄縁3
- scenes: 2
- canvas: 1920x1080
- fps: 60
- timeline: 1606 frames / 26.766667 sec
- source project SHA:
  `2585c0994ca56a6665ae834b71866ab3c92bc5bc9c59ca7f5a76c9128e7d0e12`
- preview playback: false
- speaker playback: false
- process cleanup: true

REINS source project SHA
`ed2773ce87a41936dd82d16d666d253f8bdba8763fc11bfa829d4818cb1b3ec9`
は使用後もexactだった。

## Pre-render focused gate

- Python focused:
  `tests/test_third_real_topic_factory_canary.py`、
  `tests/test_episode_video_pipeline.py`、
  `tests/test_standard_production_loop_gui.py` — 27 passed
- Node standard loop contract — 7 passed
- .NET Release build — warnings 0 / errors 0
- write-free CLI dry-run — passed
  - content identity:
    `dfb6ad91822b9aa69a5be3b511bfe7b9d395f051d7c33aaf4e5a2384495485cf`
  - protected inputs: 9/9 exact
  - tracked clean: true
  - VoiceItems 5、real media 5/5、SVG 0

最初のfocused testで、tracked-text scanがignored `source_cache` PNGをUTF-8
textとして読もうとするtest-only failureを1件検出した。package-local ignored
3 rootsをscan対象から外し、再実行でpassした。product bytesは変更していない。

## Actual Electron GUI normal path

actual local Electron 43.2.0のmain / renderer / preloadをhidden/offscreenかつ
silentで起動し、standard automated video production surfaceから実行した。

- GUI receipt SHA:
  `7a378ce87c8137eeb1ab519e5662232616391d28cc48db7f1a215a1aef6ed66c`
- deep doctor: code / review / render / regenerate = 4/4 ready
- protected inputs: 10/10 exact
- actual dry-run: passed
- generation control: enabled primary action
- actual real YMM4 render: passed
- readiness bypass: false
- render test double: false
- tracked clean at dispatch: true
- manual intervention: 0
- Computer Use: 0
- keyboard/mouse injection: 0
- SendKeys: 0
- preview/speaker playback: 0
- mute audio switch: true
- console/security/load/renderer/preload errors: 0
- total GUI workflow: 147.1044 sec

以前の保存ダイアログ停止原因であった、filename欄とSave buttonの識別経路を
通過しており、address valueをfilenameへ入力して待機する挙動は再発していない。

## Generated YMM4 project

- SHA-256:
  `47a68b940df29937f735876fcf272bcfb403b1efe692e2cd0a153d2756c78d9d`
- size: 966,920 bytes
- normalized structural SHA:
  `d7b4a4b096cd97f82a26cdc803107502613dbbdcc9166ec23187955b48c15306`
- VoiceItems: 5
- ImageItems: 5
- scenes: 2
- speakers: 2 / 3
- timeline: 1606 frames
- text/order: canonical exact
- source VoiceItems: unchanged
- absolute path: run directory内のみ
- path leak: 0
- SVG: 0

## MP4 technical validation

- SHA-256:
  `f39297c9888fb59e0260676c1810430f06145949d99a8c3b46dea5d606d80e8d`
- size: 33,762,259 bytes
- container: ISO-BMFF
- top-level boxes: `ftyp` / `moov` / `free` / `mdat`
- video: H.264 Main、yuv420p、1920x1080、60fps、1606 frames
- audio: AAC-LC、48kHz、stereo
- duration: 26.766016 sec
- overall bitrate: 10,091,082 bps
- full-file decode: passed
- decode後のsource hash: unchanged
- extracted frames: 8、unique 8
- cue frames: 5/5 inspected

5 cue framesはすべて異なるofficial pageを表示し、cue labelとsubtitleを識別できた。
technical/spot visual gateはpassとした。

human review上の残差として、既存YMM4 character settingsが生成する大きい赤/黄の
keyword emphasisが一部cueでsubtitleへ重なる。読み取り可能性とartifact identityは
維持しているが、美的受容は自動継承しない。exact MP4 SHAを対象にhuman reviewerが
cue単位で`accept`、`repair`、`reject`を判断する。

## Completed-run resumeとdrift negative

canonical runの22 filesをSHA / size / mtimeでsnapshotした後、CLI
`build-episode-video --render --resume`を1回だけ実行した。

- status: `verified_noop`
- elapsed: 0.269496 sec
- outputs rewritten: false
- YMM4 launched: false
- render driver launched: false
- SHA / size / mtime mismatch: 0
- aggregate identity before/after:
  `ac3b450260433e7ac39c7b4a95db750b9f3ec1d2091fcd114496d4b53d3a046a`

isolated ignored copyではmanifestの
`render_settings.video_bitrate_kbps`だけを10000から9999へ変え、resumeが
`resume_artifact_drift`でfail-closedすることを確認した。canonical runに変更はない。

## Prior identity preservation

live rehash 20件は20/20 exactだった。

- accepted new-banknote:
  source project、generated project、MP4、human acceptance receipt
- prior REINS:
  source project、generated project、MP4、GUI receipt
- REINS repeatability v3:
  run 01 / 02 / 03のproject、MP4、pipeline receipt、GUI receipt

new-banknote、prior REINS、repeatability v3 3 runsのdry-runを各1回、合計5回実行し、
5/5 passした。prior rerenderは0。

## 3 topic variation

| Topic | Cues | Scenes | Speaker split | Frames | Duration | Real media |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| New banknote | 9 | 3 | 3 / 6 | 4415 | 73.58 sec | 9 |
| REINS | 7 | 4 | 4 / 3 | 2725 | 45.42 sec | 7 |
| AI workplace monitoring | 5 | 2 | 2 / 3 | 1606 | 26.77 sec | 5 |

3件で共通して観測したもの:

- `nlmytgen.episode_manifest.v1`
- `nlmytgen.real_media_provenance.v1`
- 1920x1080 / 60fps source-project profile
- standard Electron GUI
- deep runtime doctor
- protected input hash lock
- write-free dry-run
- real YMM4 render
- ISO-BMFF H.264/AAC validation
- full-file decode
- `silent_by_default`
- internal-review boundary

この表から読み取れるのは、観測済み3 shapeが共通pipelineを通ったことだけである。
未観測の話者数、極端な長短、別media type、source欠損、locale差、大規模batchを
含む任意topicへの一般化はしていない。

## 残作業

### Factory Contract v2 extraction

- purpose: 3 packageに実在する共通contractとtopic-variable fieldを固定する。
- effect: topic-specific hard-codeと偶然一致を、4件目の制作前に検出できる。
- requirements: 3 manifest、provenance、claim edge、source/generated project、
  receiptsのread-only比較。
- state: input evidence complete、contract未抽出。
- owner: implementation AI、supervising AI review。
- next move: required / variable / optional / forbiddenのschema matrixを作る。

### Three-fixture v2 revalidation

- purpose: v2 contractが既存3件のidentityを壊さず表現できることを証明する。
- effect: migrationをrender品質から分離し、accepted/prior outputsを保護する。
- requirements: v2 schema、adapterまたはmigration、fixture validator。
- state: unstarted。
- owner: implementation AI。
- next move: rerenderなしで3 packagesをvalidatorへ通し、identity exactを再確認する。

### AI-monitoring human aesthetic decision

- purpose: keyword emphasisとsubtitle overlapをcreative judgementで判定する。
- effect: internal technical canaryをhuman-accepted cutへ進めるか決められる。
- requirements: exact MP4 SHAと5 cue frames。
- state: open。technical/spot visual pass、human acceptance false。
- owner: human creative reviewer。
- next move: cue単位のaccept / repair / rejectを返す。

### Media rights

- purpose: official PDF capturesのreuse条件を制作・公開用途に照らして確定する。
- effect: production/publication gateを正当に判断できる。
- requirements: rights ownerまたは法務判断、使用範囲、表示・引用条件。
- state: unapproved。
- owner: rights/legal owner。
- next move: exact source URLs、page、SHA、intended useを用いたrights review。

### Fourth-topic out-of-sample validation

- purpose: v2 contractが3件の記述に閉じていないか検証する。
- effect: bounded generalization evidenceを1段広げる。
- requirements: v2 extractionと3-fixture revalidation完了、新しいshape。
- state: intentionally deferred。
- owner: supervising AI selects scope、implementation AI executes。
- next move: v2未観測変数を狙ったofficial-source topicを1件選ぶ。

## 可能な限り先の条件付き目標

1. **Factory Contract v2** — observed contractをversion化し、3 fixturesを
   no-rerenderでpassさせる。
2. **Source and claim contract separation** — source discovery、claim adjudication、
   support edge、media provenanceを独立schema/validatorにする。
3. **Recovery identity contract** — resume、collision、force archive、semantic drift、
   output immutabilityをversioned operational contractにする。
4. **Fourth-topic out-of-sample** — v2の未観測shapeを通し、failureをcontractへ還元する。
5. **Cue-quality corpus** — subtitle overlap、keyword emphasis、page legibility、
   framingをcue-level human decision corpusとして蓄積する。
6. **Rights-cleared production assets** — exact review identityとrights identityを結び、
   media差替え時は新しいhuman review identityを要求する。
7. **Bounded multi-episode queue** — one-active-job semanticsを維持しながら、
   queue、retry、cancellation、receipt aggregationを観測可能にする。
8. **Dependency and compatibility lanes** — Electron、Node、YMM4、ffmpeg、Pythonの
   compatibility/security remediationを制作contractから分離して検証する。
9. **Release governance** — technical green、creative acceptance、rights、
   production approval、publication approvalを別々のsigned gateにする。
10. **Controlled publication** — ownerの明示承認、exact artifact identity、
    destination、rollback条件が揃った場合だけupload/deploy/releaseへ進む。

各段階は直前gateの成功を前提とする。local technical validationからPR、merge、
release、deployment、public exposureを自動的に導かない。

## 再開時の最短経路

1. `AGENTS.md`
2. `docs/REPO_LOCAL_RULES.md`
3. `docs/runtime-state.md`
4. 本報告
5. `production_pilots/factory_canaries/ai_monitoring_labor_001/three_topic_variation_receipt.json`

次の実装作業はFactory Contract v2 extractionである。private runが利用可能なら
read-only structural comparisonへ使えるが、accepted/prior outputsのrerenderは
開始条件にしない。
