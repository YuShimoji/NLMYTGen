# Episode Run Pack v1

1本通しの「ゆっくり劇場風」pilot制作を、入力・中間成果物・確認結果ごとに混ぜないための作業パック。

## Reporting Contract

- assistant status: GUI側に `Episode Pack Root` を選ばせ、CSV/IR検証/適用結果をpack内の既定pathへ保存する。
- user action: 修復後は `source script`、base `.ymmp`、Production IR、必要mapをpackへ置き、GUIボタンを上から押す。
- assistant next: NG時は保存済みJSONまたはGUIパネル文面を受け取り、機械側で原因を切り分ける。

## Directory

`init-episode-run --episode-id <episode_id>` は `_tmp/episode_runs/<episode_id>/` に以下を作る。

| Directory | Role |
|---|---|
| `csv/` | source script、YMM4 CSV、CSV生成ログ |
| `ir/` | Production IR、`validate-ir` 結果 |
| `maps/` | face/bg/skit_group map、必要時のみ overlay/se/motion/bg_anim map |
| `ymmp/` | base `.ymmp`、Dry Run/Apply結果、patched `.ymmp` |
| `review/` | YMM4確認メモ、未実装演出・GUI gap |
| `manifest/` | pack manifest、session manifest、再現コマンド |

## GUI Hands-On

1. `start-gui.bat` を起動する。
2. `演出適用` タブで `Episode Pack Root` を押し、`_tmp/episode_runs/<episode_id>/` を選ぶ。
3. `CSV 変換` タブで `csv/<episode_id>.txt` を選び、`Build CSV` を押す。
4. 成功すると `csv/<episode_id>.csv` が作られ、`演出適用` タブの `CSV (row-range)` に自動反映される。
5. YMM4でCSVを読み込み、base projectを `ymmp/<episode_id>_base.ymmp` として保存する。
6. `演出適用` タブで `Production .ymmp` に `ymmp/<episode_id>_base.ymmp` を選ぶ。
7. `IR JSON` に `ir/<episode_id>_production_ir.json` を選ぶ。貼り付け保存する場合もpack選択済みなら同pathが既定になる。
8. 必要なmapだけを選ぶ。標準候補は `maps/bg_map.json`、`maps/skit_group_registry.json`、`samples/templates/skit_group/delivery_v1_templates.ymmp`。
9. `Validate IR` を押す。結果は `ir/<episode_id>_validate.json` に保存される。
10. `Dry Run` を押す。結果は `ymmp/<episode_id>_dry_run.json` に保存される。
11. `Apply Production` を押す。結果は `ymmp/<episode_id>_apply.json`、patched本体は `ymmp/<episode_id>_patched.ymmp` に保存される。
12. patched `.ymmp` をYMM4で一度だけ通し確認し、`review/ymm4_acceptance.md` を埋める。
13. `manifest/session_manifest.command.txt` を実行し、`manifest/session_manifest.md` を作る。

## NG Return

- Validate IR NG: `ir/<episode_id>_validate.json` と対象IR/mapを返す。
- Dry Run NG: `ymmp/<episode_id>_dry_run.json` を返し、YMM4確認へ進まない。
- Apply Production NG: `ymmp/<episode_id>_apply.json` を返し、patched出力を手編集しない。
- YMM4 visual NG: `wrong motion`、`screen spacing`、`body-face drift`、`too subtle`、`missing演出` のどれかに分類して `review/gaps.md` に残す。

## Acting Rule

- 初回標準入力は `face`、`idle_face`、`bg`、`skit_group`。
- `nod_clear_v2` は full-body nod baseline、`nod_head_v1` は head-only nod candidate としてpilot内で使用可。
- `overlay`、`se`、`motion`、`bg_anim` は台本上で必要箇所が明確になった場合だけ追加する。
- GUI未露出mapを使った場合は標準化せず、次のGUI補完候補として `review/gaps.md` に記録する。
- accepted library昇格やG-24 production常時接続はpilot後の別判断に分離する。
