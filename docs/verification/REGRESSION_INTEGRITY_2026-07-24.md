# 回帰整合性三モード実行報告 — 2026-07-24

## 結論

`REGRESSION_GATE_SURFACE_DIVERGENCE` は閉じた。canonical 16モジュールは
independent clean-room、evidence-rich same-machine、tracked-only linked
worktreeの全てでfailure 0 / error 0になった。pass/skip数の差は、宣言済み
private locatorが実際に存在するかどうかだけに対応する。

同時に、real-media版の内部review cutを
`human_real_media_cut_acceptance_receipt.json`でexact MP4／generated projectへ
結合した。speech、wording/order、cue timing、subtitle timing、line breaks、
real-media visual treatmentは`stable_internal_cut`として受理済みで、再renderは
不要である。rights、production、publication、upload、release、master mergeは
引き続きfalseである。

## 修正した因果

- pilot directoryを`shutil.copytree`で再帰複製するfixtureを廃止し、
  exact Git revisionのsubtreeを`git archive`から展開する共通helperへ置換した。
  ignored media、browser profile、local outputはarchiveへ入らない。
- portable product contractはtracked authority snapshotで検証し、private evidenceは
  `requires_local_evidence:<class>:missing=<repo-relative-locator>`を持つテストだけが
  live checkoutをread-onlyで参照するように分離した。
- `git check-ignore`／`git ls-files`はactual worktree rootからのrepo-relative pathへ
  統一した。存在しないignored directoryのrule検査は、その配下のsentinel pathで
  評価するため、`.git`がfileのlinked worktreeでも同じ意味になる。
- runnerはunclassified skip、absolute private locator、欠損JUnit、Git三面変化、
  JUnit temp未回収をgreenにしない。

canonical module listは従来の16件を維持し、runner自身のfocused testはcanonical
totalへ追加していない。

## 三モード結果

| mode | passed | failed | errors | skipped | 解釈 |
| --- | ---: | ---: | ---: | ---: | --- |
| independent clean-room | 161 | 0 | 0 | 9 | tracked sourceのみ。9件は欠けたprivate locator |
| evidence-rich same-machine | 166 | 0 | 0 | 4 | 存在するhistorical YMM4/layout証跡5件は実行 |
| tracked-only linked worktree | 161 | 0 | 0 | 9 | `.git` file、private evidenceなし |

全modeで実行前後の`git status --porcelain`、`git diff --no-ext-diff`、
`git diff --cached --no-ext-diff`はbyte-exactで不変だった。temp workspaceと
JUnit directoryは回収済みで、列挙確認した禁止directoryは0件だった。

clean-room checkoutはWindowsのhash固定を維持するため
`core.autocrlf=false`、深いpilot pathを扱うため`core.longpaths=true`で構築した。
これらはrepository contentの変更ではなく、Git objectのLF identityをそのまま
materializeする条件である。

機械可読結果は
`docs/verification/REGRESSION_INTEGRITY_2026-07-24.json`を正本とする。

## 残る境界

この結果でdependency lockの可搬性、Electron security upgrade、rights、
production、publication、PR、merge、master integrationは成立しない。次の開発laneは
ignoredの`uv.lock`／`gui/package-lock.json`を含むdependency reproducibility方針と、
Electron major upgradeの互換検証である。受理済みcutのcreative dimensionは再度開かない。
