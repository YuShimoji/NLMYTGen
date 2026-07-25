# Runtime Doctor / Private Artifact Ingest — 2026-07-25 JST

Classification: `runtime_doctor_private_ingest_ready`

Source:
`codex/nlmytgen-electron-43-compatibility-v1` at
`21194b60f6824eaedaddacf05bb920e1a324936a`

Outcome: resolve the exact commit from the tip of
`origin/codex/nlmytgen-runtime-doctor-private-ingest-v1`.

## 結論

別端末のruntimeとprivate artifact readinessを、履歴receiptの存在だけに依存せず
一つのread-only commandで判定できるようになった。

```powershell
uv run python -m src.cli.main doctor-runtime --profile all --deep --format json
```

出力schemaは`nlmytgen.runtime_doctor_result.v1`。`code`、`review`、`render`、
`regenerate`を独立に返し、各decisive checkにstatus、evidence validity、
observed result、consumer effect、authority sourceを含む。通常の`all`はprivate
profile不在だけではnonzeroにならない。`--require-profile X`を指定したときだけ
Xがunavailableならexit 1、invalid inputはexit 2になる。

## Before → After

Beforeはtoolchain、Electron、YMM4、accepted media、source assets、manifest、
provenanceが複数のauthorityと端末固有前提に分散していた。過去receiptがaccepted
identityを示しても、現在の端末にlive bytesがあるか、hashが同じか、どのconsumerが
開始可能かを一度に区別できなかった。

Afterはdoctorがtracked lockと実runtimeを読み、live locatorまたは
`--artifact-root`のstaging rootを検証する。receiptはidentity/lineage authorityに
限定され、対応するlive fileがなければ`receipt_only_no_live_file`になる。
private dataをcopy、replace、delete、extract、hardlink、symlinkしない。

## Readiness profiles

| Profile | 必須証拠 | Thank端末 | Tracked-only checkout |
| --- | --- | --- | --- |
| `code` | Python/uv、`uv.lock`、CLI import、Node/npm、npm lock、Electron 43.2.0、Git safety、deep smoke | ready | ready |
| `review` | accepted MP4 exact、receipt agreement、video/audio ffprobe | ready | unavailable |
| `render` | code、YMM4 compatible、source project、nine assets、ffmpeg/ffprobe/.NET、silent policy | ready | unavailable |
| `regenerate` | render、manifest/provenance/protected input agreement、existing episode pipeline | ready | unavailable |

Thank端末ではsource project、generated project、accepted MP4、nine real-media
assetsの全12点がdeclared SHA-256に一致した。YMM4は4.54.0.1のProductVersionを
読み取っただけで起動していない。accepted MP4はffprobe metadataを読み、再生して
いない。

tracked-only short-path checkoutは`uv sync --extra dev --locked`と
`npm --prefix gui ci`で復元し、Electron 43.2.0、hidden/silent smoke、tracked-clean
Gitを確認した。private bytesは一切持ち込まず、12点すべてが
`receipt_only_no_live_file`になった。`code` readyを維持したまま、review/render/
regenerateだけがavailability不足としてunavailableになった。

## Private artifact contract

正本:
`production_pilots/yukkuri_newsroom_content_spine_002/external_editorial_input/new_banknote_security_notebooklm_001/auto_video_pipeline/new_banknote_private_artifact_ingest_contract.json`

schema `nlmytgen.private_artifact_ingest_contract.v1`はaccepted run
`new_banknote_real_media_review_v1`について次を固定する。

- source YMM4 project 1点
- generated YMM4 project 1点
- accepted internal-review MP4 1点
- real-media source 9点
- 12点それぞれのartifact ID、expected SHA-256、bundle-relative source、
  repo-relative destination、required consumer、sensitivity、rights class
- source → generated project → accepted media → human acceptanceのlineage
- `mutable=false`、`overwrite=false`、production/publication/upload false
- validation-only default、copy/apply authorization false

contractとsanitized receipt/reportにはusername、drive-qualified private path、
credential、private source bytesを含めていない。

## Staging-root negative proof

空のstaging rootでは12点すべてが`receipt_only_no_live_file`、
`ingest_ready=false`になった。これによりhistorical receiptがlive availabilityへ
昇格しないことを確認した。

hash-mismatch fixtureではdeclared accepted-MP4 locatorへ空のsynthetic fileだけを
置いた。対象は`present_hash_mismatch`、`review` unavailable、
`--require-profile review`はexit 1。fixtureにreal private mediaはなく、検証後に
回収した。両fixtureともcopy/overwrite/delete/archive extractionはfalse。

contract pathはrelative-onlyで、traversal、absolute path、source/destination
duplicate、resolved-root escapeを拒否する。staging root側だけでなく、既存
repo destinationがroot外へresolveする場合もunsafeとして扱う。

## Hidden Electron capability

deep modeは既存の`smoke:electron-compatibility`を再利用し、代替demo windowを
作っていない。actual main/renderer/production preloadをhidden/offscreen、
silent policy、mute-audioで実行した。Electron 43.2.0 exact、console errorなし、
cleanup passを確認し、doctorが作ったproject-owned smoke outputだけを回収した。
visible window、focus takeover、persistent profile、public network、user-owned
process mutation、audio/video playbackはない。

## Validation

- modified Python compile: pass
- doctor/private-ingest focused tests: 17 pass / failure 0 / error 0
- Electron 43 focused contract tests: 6 pass / failure 0 / error 0
- dependency authorityの現行適用可能なtests: 5 pass / failure 0 / error 0
- tracked-only locked restore / deep doctor: pass
- project-state sync、JSON parse、Markdown checks、`git diff --check`: pass
- outcome commit後のcanonical Regression Integrity: failure 0 / error 0、
  declared-locator skip contract valid、Git三面不変、temporary workspace回収

dependency authority testのうち2件はElectron 35 checkpoint時のmanifest hash /
35.7.5 current lockを直接期待する旧assertionであり、Electron 43 branchの現行
candidate authorityとは一致しない。現行candidate/rollback両identityは
`tests/test_electron_43_compatibility_contract.py`で固定されている。

## Identity and preservation

- Electron current candidate: 43.2.0、lock SHA-256
  `095706aba72687058863d8bca16c5a9a9f7d4e45cde3397dda3197a528d0f047`
- Electron rollback: 35.7.5、source commit
  `2e11987ff0732d21df4a5da83d1ea557614991ac`、lock SHA-256
  `81b060f37fd2c7c4151fcf6fc402b554476d4ea6785022c8eef01aaaa9ff4a73`
- `uv.lock`: SHA-256
  `40e64f793775f0b0181f5ba8972c17842717dbe14bc8c0a6c0cabd14442435d0`
- accepted MP4: SHA-256
  `423553e0aff40619ffb0fd88bcc80344417788aa6128f0a8778aefbdd19ca476`
- generated project: SHA-256
  `244c05ae6fe6179e9dace4b569cd5f3f9f496cfe70d46ac16ac459e787712611`

accepted speech、wording/order、cue/subtitle timing、line breaks、real-media visual
treatmentはclosedのまま。`.playwright-mcp/`、`artifacts/`、
`phase-e-01-contact-acquired*.png`、`.venv/`、`gui/node_modules/`、private media、
YMM4 projects、browser profiles、frames、run archivesをstage・削除・変更していない。

## 監修判断と条件付き長期目標

現在の唯一のproduct gateは
`named-private-artifact-delivery-or-standard-production-loop-gui`。次の一手は
destination terminalでdoctorを実行し、必要consumerを選ぶこと。

1. Private deliveryを選ぶ場合、named recipient、artifact set、transport method、
   transfer authorityを別途確定する。delivery後は`--artifact-root`で検証し、
   apply/copyは別承認にする。
2. Review consumerを選ぶ場合、exact accepted MP4を復元してreview profileを
   requireする。新しいcreative reviewやaccepted cutの再承認は目的に含めない。
3. Render/regenerate consumerを選ぶ場合、source projectと9素材をexactに復元し、
   doctor pass後にだけ別のrender authorityを判断する。doctor自身は実行しない。
4. Private deliveryを選ばない場合、standard production-loop GUIをthin feature
   sliceとして設計し、doctorのprofile/resultを入口にする。
5. その先のrights clearance、production acceptance、publication/upload/releaseは
   それぞれ独立したowner・証拠・明示承認を持つ条件付きgateとする。

actual cross-terminal transport、YMM4 launch、render、media playback、system-volume
change、rights action、production、publication、upload、release、PR、merge、
master integrationは今回実施していない。
