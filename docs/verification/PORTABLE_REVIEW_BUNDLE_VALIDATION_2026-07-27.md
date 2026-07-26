# Portable Review Bundle and Recipient-Open Validation — 2026-07-27

## Outcome

exact source `3556c8b73e635f87d867a0003cf4187b19075e88`から
`codex/nlmytgen-portable-review-bundle-v1`を作成した。従来はignoredなrepo-local
directoryにしか存在しなかったFood Expiry `cue_002` packetを、source packetを
再生成・変更せず、自己完結したversioned directoryとdeterministic ZIPへ変換した。

bundleはrepository checkout、private source、server、network、accountを必要と
しない。`index.html`からexact excerpt、render frame、materialized source view、
README、manifests、checksums、recipient templateを開ける。一方、ここで証明した
のはtechnical portabilityだけで、named terminal delivery、human open、content
decision、creative acceptance、rights、production、publicationではない。

outcome commitは`resolved-by-current-branch-tip`で解決する。commit後のcanonical
Regression Integrityは一度だけ実行し、その結果とexact remote parityは最終
handoffに記録する。

## Source identity and preservation

入力は
`production_pilots/factory_canaries/food_expiry_labels_001/auto_video_runs/food_expiry_labels_internal_review_v4/content_review_packets/cue_002_queue_derivative_v1/`
の5 filesで、tracked authority receipt SHAは
`f45957e4c0fe8ac13125fd31a4b4eb01b53f641212ba0742e4601fd8ff509363`、
packet manifest SHAは
`e06cdbd49d2e954850359aebb090c30eea8a103e43258dab72e0ac836fca83a1`
である。

| Source packet file | SHA-256 | Bytes |
| --- | --- | ---: |
| `README_REVIEW.md` | `ccdd8e0b18db06ff4625fbed58338fafff4686376aa7838bd20fee05e14b8b44` | 821 |
| `cue_002_materialized_source_view.png` | `62a5e9daecd79e048df4bed8ced3a4880ee871ce862965a6a19f8a5c0d5b6163` | 413,062 |
| `cue_002_render_frame.png` | `686e76e7b204cac56fd9427e6458f32b5f676e8ea75a3a85b08bd4c89dacfa20` | 485,008 |
| `cue_002_review_excerpt.mp4` | `2703e4e881baea3958310194e3700678e54552705c66eddc007494e881c3977d` | 361,665 |
| `packet_manifest.json` | `e06cdbd49d2e954850359aebb090c30eea8a103e43258dab72e0ac836fca83a1` | 5,221 |

packageは`food_expiry_labels_001`、cueは`cue_002` / scene `S1`、intervalは
`[373,816)` / 443 frames / 60 fps / `[6.2166666667,13.6)`、canonical text
SHAは`edea41f9...c0c`である。descriptor、content、source project、
generated project、source MP4、source ID、original/materialized source、
crop `[0.04,0.34,0.62,0.23]` / `cover`をreceiptとmanifest間でexact照合した。
実行前後の5 file SHA / size / mtime mismatchは0で、regenerationとmutationは0。
既存content-thread packetはbundleせず、read-only境界を維持した。
original `packet_manifest.json`内のrepo-relative lineage stringsはbyte preservation
のため履歴identityとして保持したが、portable manifest / indexはそれらをlocator
として解決しない。username、drive、absolute private path、credentialは0である。

## Contracts and public commands

`nlmytgen.portable_review_bundle.v1`はbundle/version、packet/package/cue、
source identities、immutable inventory、portable relative paths、MIME、
offline entrypoint、各state、retention/no-overwrite、archive policyを分離する。

`nlmytgen.review_bundle_recipient_open.v1`は次のclockを独立に保持する。

- transport: `not_started | completed | failed`
- identity: `unknown | valid | invalid`
- machine open: `unverified | verified | failed`
- human open: `unverified | verified | failed`
- content decision: `none | pending | recorded`

machine-openからhuman-openを、human-openからacceptを、acceptからrights /
publicationを推論しない。`delivery_complete`はexact artifact/version/recipientの
transport、identity、human-openが揃うまでfalseである。

公開CLIは`build-portable-review-bundle`と
`validate-portable-review-bundle`である。builderはsource receipt/manifestと
descriptorをexactに検証し、no-overwrite、no-network、no-playbackでdirectoryと
ZIPを同時生成する。validatorはdirectory/ZIP双方のinventory、path、checksums、
manifest、offline indexを検証し、`--check-machine-open`では再生せず
ffprobe/full decodeとPNG decodeを行う。

## Accepted bundle identity

ignored/local output:

- directory:
  `production_pilots/factory_canaries/food_expiry_labels_001/review_delivery_bundles/cue_002_portable_review_bundle_v1/`
- ZIP:
  `production_pilots/factory_canaries/food_expiry_labels_001/review_delivery_bundles/cue_002_portable_review_bundle_v1.zip`
- archive SHA:
  `cba54b31c510e8b35ab57a1fd188ea5ff466bd229aaeee3c100bb75168c528ca`
- archive bytes: 1,275,584
- manifest SHA:
  `24037ea26a79cdbb49d6347002fd33fe89fb578d1f1800de1357b0807008c106`
- semantic identity:
  `5bdb52e0abf4bff420e69ca847edd8ac870e5ee0c40ce20777b7f24d26d63287`

| Bundle file | SHA-256 | Bytes |
| --- | --- | ---: |
| `README_OPEN.md` | `0e949c356bfb2c0dd10c65d3268ee0eeac3eee10e7f390c00f4bcfa3d6430f0c` | 636 |
| `checksums.sha256` | `284bdb39b0b430ffd5accaed71bcb03c8748fad1f75cd448749884b00958c150` | 849 |
| `index.html` | `9b7c8727fd04c89ebb9694eae26c49a20feaf2afe65b3d95c3c1b12b3ada26b0` | 2,403 |
| `packet/README_REVIEW.md` | `ccdd8e0b18db06ff4625fbed58338fafff4686376aa7838bd20fee05e14b8b44` | 821 |
| `packet/cue_002_materialized_source_view.png` | `62a5e9daecd79e048df4bed8ced3a4880ee871ce862965a6a19f8a5c0d5b6163` | 413,062 |
| `packet/cue_002_render_frame.png` | `686e76e7b204cac56fd9427e6458f32b5f676e8ea75a3a85b08bd4c89dacfa20` | 485,008 |
| `packet/cue_002_review_excerpt.mp4` | `2703e4e881baea3958310194e3700678e54552705c66eddc007494e881c3977d` | 361,665 |
| `packet/packet_manifest.json` | `e06cdbd49d2e954850359aebb090c30eea8a103e43258dab72e0ac836fca83a1` | 5,221 |
| `portable_bundle_manifest.json` | `24037ea26a79cdbb49d6347002fd33fe89fb578d1f1800de1357b0807008c106` | 3,899 |
| `recipient_open_receipt.template.json` | `0b0af76e11f38aae83a26f9ab73eb9e774fd1cd634ba7689e47e740bdb98032c` | 714 |

独立assembly 2回のdirectory payloadとZIP byteは一致し、ZIP timestampは
`1980-01-01T00:00:00Z`へ正規化した。directoryとZIPのsemantic inventoryは
10/10一致した。absolute/traversal/duplicate/symlink/hardlink/encryption/
executable/nested archiveは各0。H.264/AAC、1920×1080、60 fps、48 kHz stereoの
video/audio full decodeとPNG 2/2 decodeに合格し、transcode、playback、audio
outputは0だった。

最初のpre-acceptance candidateは、video fallback linkがvideo control内に
nestedし、そのlinkだけが独立focusできないため不合格とした。source packetを
変えず、nested fallbackだけを除去し、別のMP4 linkは保持した。不合格candidateは
authority artifactにせず、accepted outputへのoverwriteは0である。

## Isolated transport and machine-open

runtimeで生成したshort isolated recipient rootは作成前absentだった。ZIPを
byte-exact copyし、source/destination SHA一致、archive mismatch 0を確認してから
新規directoryへextractした。extracted 10 filesのsemantic identityは
`5bdb52e0...63287`で、repository lookup、private full source/project/MP4 copy、
overwrite、external transferは各0だった。tracked evidenceにはsanitized
recipient ID `isolated-machine-recipient-v1`だけを保存し、受領先pathは残して
いない。inspection後はlocal machine receiptsを保持し、temporary recipient root
とbrowser profileを削除した。

Electron 43.2.0 / Chromium 150.0.7871.129のhidden 1280×720 windowで、extracted
`index.html`を`file:`として開いた。

- PNG load: 2/2、1920×1080
- video: 1、metadata readyState 4、7.383333秒、paused、currentTime 0
- autoplay false、muted true、controls true
- focusable surfaces 10/10 reachable
- local references 12、external reference/request 0
- console/security/load error 0、window open 0
- playback event 0、audio output 0
- horizontal overflow 0 px
- owned Electron process / temporary profile residue 0 / 0

結果stateは`transport=completed`、`identity_check=valid`、
`machine_open=verified`、`human_open=unverified`、
`content_decision=none`、`delivery_complete=false`である。これはnamed
cross-terminal deliveryや人間による可読性・採否を意味しない。

## Tracked-only and fail-closed behavior

staged tracked treeから`src`、schemas、descriptor、source authority receipt、
machine receiptだけを隔離展開した。ignored source packetとbundleは存在しない。
schema hash、builder import、descriptor、machine receipt、embedded recipient-open
stateはすべて検証可能だった。

同checkoutでbuild commandを実行するとexit 1 /
`source_bundle_unavailable`となり、output directory/ZIPは作られなかった。
regeneration、YMM4、render driver、network、private copyは各0で、missing
private packetからfallback生成やGitへのpacket bytes混入を行わなかった。

## Validation and boundaries

- portable bundle focused tests: 18 passed
- cue review packet nearest regressions: 21 passed
- modified Python compile: passed
- deterministic assembly、directory/ZIP validation、media/image decode: passed
- isolated copy/extract/machine-open/tracked-only: passed
- JSON / Markdown / HTML parse、state sync、`git diff --check`: passed
- canonical Regression Integrity: outcome commit後に一度だけ実行

negative testsはsource hash/file/manifest contradiction、absolute/traversal/
duplicate/symlink/size ceiling、foreign destination/overwrite、archive/file hash、
offline entrypoint、external resource/autoplay、source mutation、state inference、
recipient mismatch、tracked-only fallbackをfail closedにする。

YMM4、render driver、full render、transcode、playback、system volume、network、
cloud upload、external communicationは0。canonical content、descriptor、queue、
source/generated project、source MP4、content-thread packet、dependency lockは
変更していない。named recipient delivery、human open、content/creative decision、
rights、production、publication、upload、release、PR、merge、master mutation、
deploymentは未実施・未承認である。

次のtechnical gateは、複数bundleをartifact/version/recipientで引ける
recipient-side registry/ingestと、実在するnamed terminalがある場合の
independent delivery validationである。その後もhuman-open receipt、artifact-bound
content decision、rights/production/publication authorityは独立clockとして進める。
