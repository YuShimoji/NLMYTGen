# Episode 002 one-shot YMM4 Operator Batch

このバッチは、headless準備済みの内部確認パイロットを一度だけYMM4で取り込み・書き出しする手動gateです。

- PCの操作主体はユーザーです。
- CodexはGUI、mouse、keyboard、window focusを操作しません。
- 生成物は `INTERNAL REVIEW / NOT FINAL / LOCAL EVIDENCE PILOT` であり、本番・公開・権利承認ではありません。
- まずYMM4内の未保存作業を解消し、このpilot以外が表示されていない状態で始めてください。

## 実行

このディレクトリで次を一度だけ実行します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_yymm4_operator_batch.ps1
```

起動前の確認だけなら、YMM4を起動しない次のコマンドを使えます。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_yymm4_operator_batch.ps1 -PreflightOnly
```

render後にterminalやcollectorだけが中断した場合は、YMM4を起動せずproject／renderを再生成しない次の回収専用routeを使います。既存の成功済み `operator_result.json` がある場合はbyte-for-byteで保持します。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_yymm4_operator_batch.ps1 -CollectOnly -OperatorConfirmedClean
```

## 手動アクション（5件）

1. Run run_yymm4_operator_batch.ps1 once from a clean terminal.
2. In YMM4 create/confirm a new empty project and empty timeline, then use Tools > Script Import, select the derived CSV, confirm no mapping/error or character mismatch, add it to the timeline, and use Project Save As to save the exact .local.ymmp import-base target (never the .mp4 target).
3. Return to the terminal and enter READY so the script generates the local internal-review project.
4. Open that generated project, confirm it opens without error and shows the three internal/non-final labels, then use Video Output/Export (not Project Save As) exactly once to the specified .mp4 target and close safely.
5. Return to the terminal and enter COLLECT so the script writes operator_result.json.

YMM4では最初に新規の空project／空timelineであることを確認し、既存itemがあれば停止します。その後 `ツール` → `台本読み込み` から `derived_yymm4_import.csv` を選び、対応表やerrorが出ず、霊夢／魔理沙の割り当てが正しい場合だけ `タイムラインに追加` します。手で件数やhashを計算する必要はありません。

保存操作は次の2種類を混同しないでください。

- **Project Save As -> `.local.ymmp`**: import base projectを保存する操作です。`.mp4` pathを入力してはいけません。
- **Video Output/Export -> `.mp4`**: 動画を書き出す操作です。Project Save Asを使ってはいけません。project JSONが`.mp4`名で保存されるためです。

## Stop conditions

- unexpected unsaved project
- project other than the intended pilot
- YMM4 update requirement
- mapping dialog or character mismatch
- parse or open error
- render asks for production, public, or upload action
- output path differs unexpectedly
- a Project Save As dialog is being used for the .mp4 video-output target
- an exact pilot output target already exists from an earlier run
- unrelated user work is visible

## Prohibited actions

- upload
- publication
- production .ymmp
- external media download
- source replacement
- rights approval
- final thumbnail approval
- default-branch mutation
- deleting unrelated user files

## 返却

`operator_return_template.md`どおり最大3項目だけ返してください。failure screenshotは任意です。
