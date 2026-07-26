# Food Expiry Queue Render Verification — 2026-07-26

Food Expiry packageをqueue-v2の唯一のrender候補として実行し、Factory Contract
v2.1の`rendered` lifecycleとqueue-v3のcomplete no-op policyを実証した。

## Result

- authority:
  `supervisor-food-expiry-single-render-2026-07-26`
- package: `food_expiry_labels_001`
- final run: `food_expiry_labels_internal_review_v4`
- content identity:
  `27165fad6fadaee2e5c247a86758a505c7f5f5797eb7b386d174585622a585c6`
- generated project:
  `f0b03e67565bbe340fad7e689c30b519184735ac10e701cbd5da344f4c014f88`
- MP4:
  `95558db7488a882b4d22a9ea68f302bcc81e23800dfed9687274fe8944d3daec`
- rendered descriptor:
  `bcbafe344f7a6efbbb03b4ace7a83e955c71d8d235381d4acafc861cd7b5975f`
- queue-v3:
  `214d5e99b3a201c0afc216753410d16a52ef8ec6994e854e2fee2473405bd927`

## Generated project and media

Generated projectはVoiceItems 4、ImageItems 4、霊夢4、scene 1、
1335 frames / 60fps。source VoiceItemsはsemantic exact、private path leakと
SVG referenceは0。normalized structural identityは
`4993bb5f...ece88`。

MP4は28,023,236 bytes、H.264/AAC、1920×1080、60fps、22.25秒。
ISO-BMFF、bitrate、duration、full-file audio/video decode、source unchanged、
7 frame / 7 distinct hashを通過した。

cue_001からcue_004までの抽出PNGを実画像として確認した。各cueはexact subtitle、
対応するofficial raster crop、可読表示を持ち、黒画面、欠落、clipping、
SVG/abstract proxy、production/public claimは0。

## Causal repair and preserved attempts

最初のpreflightはv2.1 reusable-crop provenanceと既存episode pipelineの表現差を
検出し、YMM4起動前に停止した。runtime-only provenance adapterを追加した。

v2は字幕transition直後のrepresentative frame、v3は同一asset IDの異なるcropを
一枚へ集約する互換性欠陥とinput-side seekを検出した。両runとreceiptを
ignored evidenceとして保存した。episode pipelineをcue別materializationと
accurate output seekへ修正し、v4で合格した。

YMM4/render-driver launchは失敗runを含め合計3、final valid renderは1。
manual YMM4、Computer Use、SendKeys、input injection、playback、system volume
operationは0。各attempt後のproject-owned residueは0。

## Queue and repeatability

live queue-v3は4件`verified_noop`、render/source candidate、scheduled、
execution set、blocked、invalidがすべて0。

tracked-only projectionではprivate source/generated project/MP4が0のまま、
4件すべて`recorded_complete_no_live_file`、render candidate 0。
queue-v1/v2/v3とFood Expiryの3 lifecycle descriptorはすべてvalid。

同一render requestの再実行は`verified_noop`。generated project、MP4、
media validation、pipeline receipt、render readback、promotion receipt、
descriptor、queueのSHA/size/mtime mismatchは0。YMM4、render driver、
ffmpeg encode起動とoutput rewriteは0。

## Validation

render promotionの負例・contract testは23件、render前のfocused regressionは
136件、render後に関連10 moduleを束ねたfocused regressionは170件すべて合格。
cue別crop materializationとaccurate output seekの回帰testを2件追加した。
canonical regression integrityはoutcome commit後に一度だけ実行する。

## Authority boundary

これはtechnical internal-review render evidenceである。human creative
acceptance、rights、production、publication、upload、release、PR、merge、
master mutation、deploymentは実施も付与もしていない。
