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
