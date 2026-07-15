# Decision Log — Generic Static Layout Probe

このファイルは、現在のgeneric static-layout sliceに必要な判断だけを短く保持する。
詳細な履歴や実行ログは `docs/project-context.md`、current stateは
`docs/runtime-state.md`、実行入口は `samples/visual_composition_lab/runtime_probe/`
を正本とする。

## 2026-07-14 — H0 probe close

- **Scope**: linked-subtitle safe areaをprimary targetにし、ImageItem 1件と独立TextItem
  1件だけを後続user observationへ渡す。Shape/fade/opacity/zoom/transform/motion/
  transition/render/Route A/C3以上はこのsliceから除外。
- **Carrier**: neutral tracked sampleをread-onlyで解析し、VoiceItemと対応Character/
  linked-subtitle設定だけを採用。source SHA-256は
  `9f89a982caba90cc4c241acaaa5c4df50d92c4a38d09270a04aeb3df4e09a524`。
  source Image/Tachie/GUI state/private pathsはoutputへ持ち込まない。
- **Layout**: 1920x1080 canvasでImage upper-left、`PROBE LABEL` upper-right、
  linked subtitle bottom reserve。zoneはcontract上pairwise non-overlap。TextItemは
  YMM4のtop-left-like stored anchoringを前提にする。
- **Evidence**: project parse、determinism、source/Voice invariance、exact counts、
  safe-mode、privacy、state syncをverified。visual readability/crop/anchor/wrapは
  H1 user observation待ち。capability matrixはregradeしない。
- **Validation**: focused/direct 116 passed + state-sync 8 passed = 124 passed。
  旧178/186表現は推測で再構成せず、`docs/visual_system/validation_scope_receipt.json`
  の非重複commandsをauthorityにする。
- **Delivery**: branch `codex/generic-visual-static-layout-probe-v1`、artifact outcome commit
  `7f71c72a7f0bca16b13a75216f4787791da909df`、remote parity 0/0。handoff docsのfollow-up
  commit後もnormal Operator Batchは未実行。次はuser-operated H1 observationだけ。

## 2026-07-15 — H1 exact-composite observation pass

- **Local result**: ignored `operator_result.json`はnon-fixture、`status=pass`、
  `observed_by_operator`で、subtitle readability/non-overlap、Image visibility/crop/anchor、
  Text visibility/wrapping/anchorのexact 3 keysがすべてpass。result SHA-256は
  `a881c5e6bfd8be167b32c8aa7b232d0c4ed31b494563e192091aba119419dd03`。
- **Identity**: project SHA-256
  `100d4ebcd31e1665db90cc688492efec211d899e579d013e751c9643cc98eebc`、79,303 bytes、
  mtimeはbatch stateと一致。asset SHA-256
  `ad1f93bf29d07372a955645326129127a96f989786db642969ef77aad84b00b9`もH0と一致。
- **Evidence separation**: structural facts/identityはmachine-verified、3 visual answersは
  human operator-observed。WorkerはYMM4/Computer Useを使わず、local ignored evidenceは
  byte-for-byte保持した。
- **Capability decision**: 38 capability rowsにexact 1 Voice / 1 Image / 1 Text compositeの
  unique rowはないためglobal rowをregradeしない。`bounded_static_layout_safe_area_probe`
  combinationだけをC3 `bounded_runtime_observed_pass`として追加し、class totalsとC0-C5は不変。
- **Boundary**: no save、screenshot evidence、render、motion/effect、alternate layout、
  cross-machine、C4/C5、Route A/B/C、production/right/publication claim。次のhuman gateは
  authoritative provenance branch上のnew-banknote visual-direction selection。
- **Delivery**: validated outcome commitは
  `81b9092cb44d45924c87965907e6065d63189ba4`、remote branchは
  `origin/codex/generic-visual-static-layout-observation-intake-v1`。remote handoff sealは
  product判断を変更せず、別端末のrestart order、tracked/ignored境界、live parity checkを
  current docsへ固定する。
