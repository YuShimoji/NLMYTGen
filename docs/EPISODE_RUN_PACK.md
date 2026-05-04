# Episode Run Pack v1

1本通しの「ゆっくり劇場風」pilot制作を、入力・中間成果物・確認結果ごとに混ぜないための作業パック。

## Reporting Contract

- assistant status: GUI側に `Episode Pack Root` を選ばせ、CSV/IR検証/適用結果をpack内の既定pathへ保存する。
- user action: 初回入力は `csv/<episode_id>.txt`、`ir/<episode_id>_production_ir.json`、`ymmp/<episode_id>_base.ymmp` の3つを必須として明示する。必要mapは条件付きで列挙し、`素材投入` の一語で代替しない。
- assistant next: NG時は保存済みJSONまたはGUIパネル文面を受け取り、機械側で原因を切り分ける。
- route rule: 本ファイルは assistant / maintainer が読む pack 定義であり、user handoff の手順本文の代替ではない。`手順の正本は docs/EPISODE_RUN_PACK.md:<line>` のように参照して user action を成立扱いしない。pilot 操作を渡す応答では、必須3点、任意map、GUI順、成功出力、NG返却、assistant next を本文に再掲する。

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

## Initial Input Packet

Episode Pack Root を選んだ直後に必要なものを、必須と条件付きで分ける。

| File | Required | Purpose | Created by / when |
|---|---|---|---|
| `csv/<episode_id>.txt` | yes | 元台本テキスト。`Build CSV` の入力 | NotebookLM / script refinement 後に user が置く |
| `ir/<episode_id>_production_ir.json` | yes | 演出IR。`Validate IR` / `Dry Run` / `Apply Production` の入力 | S-6 Production IR 出力を user が置く、またはGUIで貼り付け保存 |
| `ymmp/<episode_id>_base.ymmp` | yes | YMM4でCSV読込後に保存したbase project | `Build CSV` 後、user が YMM4 でCSV読込して保存 |
| `maps/bg_map.json` | conditional | IR が背景切替 `bg` を使う場合のラベル→画像path解決 | 背景ラベルがあるときだけ user / assistant が用意 |
| `maps/skit_group_registry.json` | conditional | IR が `skit_group` を使う場合のintent解決 | 茶番劇GroupItemを使うときだけ user / assistant が用意 |
| `samples/templates/skit_group/delivery_v1_templates.ymmp` | conditional | `skit_group` placement のtemplate source | repo既存。GUIで template source として選ぶ |
| `maps/face_map.json` / face map bundle | conditional | IR が `face` / `idle_face` を使い、paletteだけで足りない場合 | キャラクター別表情辞書が必要なときだけ用意 |

NG時に返すものは「作業した感想」ではなく保存済み artifact。`*_validate.json`、`*_dry_run.json`、`*_apply.json`、またはGUIパネル文面を返す。

## GUI Hands-On

1. `start-gui.bat` を起動する。
2. `演出適用` タブで `Episode Pack Root` を押し、`_tmp/episode_runs/<episode_id>/` を選ぶ。
3. `csv/<episode_id>.txt` と `ir/<episode_id>_production_ir.json` があることを確認する。
4. `CSV 変換` タブで `csv/<episode_id>.txt` を選び、`Build CSV` を押す。
5. 成功すると `csv/<episode_id>.csv` が作られ、`演出適用` タブの `CSV (row-range)` に自動反映される。
6. YMM4でCSVを読み込み、base projectを `ymmp/<episode_id>_base.ymmp` として保存する。
7. `演出適用` タブで `Production .ymmp` に `ymmp/<episode_id>_base.ymmp` を選ぶ。
8. `IR JSON` に `ir/<episode_id>_production_ir.json` を選ぶ。貼り付け保存する場合もpack選択済みなら同pathが既定になる。
9. 必要なmapだけを選ぶ。標準候補は `maps/bg_map.json`、`maps/skit_group_registry.json`、`samples/templates/skit_group/delivery_v1_templates.ymmp`。
10. `Validate IR` を押す。結果は `ir/<episode_id>_validate.json` に保存される。
11. `Dry Run` を押す。結果は `ymmp/<episode_id>_dry_run.json` に保存される。
12. `Apply Production` を押す。結果は `ymmp/<episode_id>_apply.json`、patched本体は `ymmp/<episode_id>_patched.ymmp` に保存される。
13. patched `.ymmp` をYMM4で一度だけ通し確認し、`review/ymm4_acceptance.md` を埋める。
14. `manifest/session_manifest.command.txt` を実行し、`manifest/session_manifest.md` を作る。

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
