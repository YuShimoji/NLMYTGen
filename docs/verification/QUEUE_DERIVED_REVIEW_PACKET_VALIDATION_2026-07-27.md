# Queue-derived Cue Review Packet Validation — 2026-07-27

## Outcome

source `8a78eb2c6c33c9638dcfb7f8517ccea9f953478a`から
`codex/nlmytgen-derived-review-packet-batch-v1`を作成し、standard Electron GUIの
bounded batchへ`effect_class=derived_artifact` /
`operation=review_packet_generation`を接続した。従来はreal zero-changeまでだった
GUIが、rendered packageを変更せずに一件のcue-level review derivativeを生成できる。
content threadの完了はtechnical executionの前提から外れ、後から利用できる
asynchronous successor inputになった。

outcome commitは`resolved-by-current-branch-tip`で解決する。post-commit canonical
Regression Integrityとremote parityは、commit後に一度だけ実行して最終handoffへ
記録する。

## Exact contract and authority

- queue: `four_package_lifecycle_queue_v3.json`,
  SHA `214d5e99...b927`
- change-set: `food_expiry_cue002_review_packet_change_set_v1.json`,
  SHA `9a99f40e...0f18`、entry 1
- package: `food_expiry_labels_001`
- descriptor: `factory_package_v2_1_rendered.json`,
  SHA `bcbafe34...975f`
- authority:
  `supervisor-food-expiry-cue002-review-packet-generation-2026-07-27`
- edge: `rendered → rendered`
- rule: exact one-shot、no overwrite、content/lifecycle change false

authorityはlocal authority set内でeffect直前に一度だけ`consumed`になった。GUI
plan-onlyは消費0、actual execute後はconsumption 1、restart/resume後も1である。
operationはpackage descriptor、content identity、generated project、source MP4、
cue、source provenance、output rootへexactに束縛される。shared codeにtopic ID
分岐や汎用plugin frameworkは追加していない。

## Cue and immutable source binding

`cue_002`は報告済み時刻に加え、canonical script、unique VoiceItem、
cue visual readback、generated-project ImageItem、run receipt、materialized sourceを
相互照合して解決した。

| Field | Exact value |
| --- | --- |
| scene | `S1` |
| canonical text identity | `edea41f9...c0c` |
| frame interval | `[373, 816)` / 443 frames |
| seconds | `[6.2166666667, 13.6)` |
| fps | 60 |
| context handle | 0 |
| source | `CAA-EXPIRATION-DATE-2025` |
| original source SHA | `2c06e90c...4517` |
| materialized image SHA | `62a5e9da...6163` |
| crop / fit | `[0.04, 0.34, 0.62, 0.23]` / `cover` |

source generated projectはSHA `f0b03e67...f88`、726,654 bytes、source MP4は
SHA `95558db7...aec`、28,023,236 bytesである。実行前後にdescriptor、project、
MP4のSHA・size・mtime driftは0だった。

## Packet output

ignored/local output:

`production_pilots/factory_canaries/food_expiry_labels_001/auto_video_runs/food_expiry_labels_internal_review_v4/content_review_packets/cue_002_queue_derivative_v1/`

| File | SHA-256 | Bytes |
| --- | --- | ---: |
| `cue_002_review_excerpt.mp4` | `2703e4e881baea3958310194e3700678e54552705c66eddc007494e881c3977d` | 361,665 |
| `cue_002_render_frame.png` | `686e76e7b204cac56fd9427e6458f32b5f676e8ea75a3a85b08bd4c89dacfa20` | 485,008 |
| `cue_002_materialized_source_view.png` | `62a5e9daecd79e048df4bed8ced3a4880ee871ce862965a6a19f8a5c0d5b6163` | 413,062 |
| `README_REVIEW.md` | `ccdd8e0b18db06ff4625fbed58338fafff4686376aa7838bd20fee05e14b8b44` | 821 |
| `packet_manifest.json` | `e06cdbd49d2e954850359aebb090c30eea8a103e43258dab72e0ac836fca83a1` | 5,221 |

excerptはH.264/AAC、1920×1080、60 fps、48 kHz stereoで、video/audio full
decodeに合格した。2 PNGもfull decodeに合格した。render frameは既存final MP4
から抽出し、source viewはgenerated projectが参照するmaterialized PNGの
byte-preserving copyである。crop再計算、source-page reraster、YMM4、preview
playbackは行っていない。manifest validationは二回とも同一結果だった。

## Actual GUI execution and resume

Electron 43.2.0のmain/preload/rendererとstandard `バッチ実行` surfaceを使った。
plan identityは`63684cd0...bd9`。planは4 package中1 mutating entryを表示し、
Food Expiryだけをdispatchした。

- actual execute: `succeeded`
- authority consumption / backend dispatch / succeeded: `1 / 1 / 1`
- other package: 3 `verified_noop`、dispatch 0
- journal: 7 events、identity `c4b75b3f...45c8`、prefix `365fce61...bd09`
- runtime restart後: 同じplan identityを再確認し、recent journalを明示open
- GUI resume: prior succeededを維持し、dispatch delta 0、authority delta 0
- output SHA / size / mtime mismatch: 0、rewrite 0、replacement authority 0
- console/security/load/preload/crash/unhandled error: 0
- project-owned process residue: 0

resume結果に見えるcumulative backend count 1は最初のeffectを保持したjournal値で、
resume前後の差分は0である。

## Tracked-only and existing packet

staged treeから必要tracked pathsだけを隔離展開し、ignored
`auto_video_runs`を含めずにactual planを実行した。結果はexit 1 /
`derived_artifact_source_unavailable`で、missing rolesはgenerated project、
source MP4、cue readback、run receipt、materialized sourceだった。dispatch、
YMM4、render driver、private copyはいずれも0であり、欠落からrender予定を
捏造しなかった。

既存`cue_002_content_review_v1`はread-onlyで照合した。package、cue、frame
interval、generated project、source MP4、source ID、materialized image、
crop/fitはcompatibleで、before/after SHA・size・mtime mismatchは0だった。
byte equalityは要件にせず、このtechnical acceptanceは既存packetへ依存しない。
human-openedまたはhuman-acceptedという結論も付与していない。

## Focused validation and boundaries

- Python review/queue/GUI focused: 97 passed
- Python Factory Contract v2/v2.1 nearest regression: 47 passed
- JavaScript batch / standard-loop focused: 16 / 7 passed
- modified Python compile / JavaScript syntax: passed
- media/audio/PNG decode、deterministic manifest validation: passed
- decisive negative cases: package/cue/duplicate/text/frame/source/crop/hash/path/
  collision/overwrite/authority/consumed/lifecycle/content/effect-unknown/resume/
  extra dispatchをfail closed
- JSON / Markdown parse、`git diff --check`: passed

canonical content、script、subtitle、speaker、timing、media selection、crop、
provenance、source/generated project、source MP4、descriptor、predecessor queues、
existing packet、dependency locksは変更していない。YMM4、render driver、
full render、playback、volume操作、human acceptance、rights、production、
publication、upload、release、PR、merge、master mutation、deploymentは0である。

技術上の次gateはversioned portable review bundleとrecipient-open contractである。
creative品質、rights、production、publicationはそれぞれのownerが後続で判断する。
