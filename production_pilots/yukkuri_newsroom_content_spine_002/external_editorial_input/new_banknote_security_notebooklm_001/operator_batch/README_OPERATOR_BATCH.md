# 新紙幣9-cue YMM4 import Operator Batch

> **INTERNAL IMPORT OBSERVATION ONLY — NOT FINAL — NON-PRODUCTION**

このbatchは、承認済み9行CSVをユーザー自身がYMM4へ一度だけimportし、
保存したlocal projectをheadless collectorで検証するためのものです。
CodexはGUI、mouse、keyboard、window focusを操作しません。render、production
save、upload、publication、rights approvalも行いません。

## 事前確認

- YMM4の未保存・無関係なprojectを安全に閉じてください。
- 実行対象は ../derived_yymm4_import.csv だけです。
- 保存先は ../local_outputs/new_banknote_yymm4_import_observation.local.ymmp
  だけです。
- mapping/error/update dialog、違うcharacter、既存itemが見えたら停止します。

YMM4を起動しないpreflight:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_import_batch.ps1 -PreflightOnly

自動検出できない場合だけ、表示されたとおり -Ymm4Exe を付けます。

## 4 manual actions

1. このdirectoryで次を一度だけ実行します。
   powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_import_batch.ps1
2. 新規の空project / 空timelineで、表示されたderived CSVを台本読み込みし、
   mapping/error/update/character mismatchがない場合だけ、表示された
   .local.ymmp へ Project Save As します。
3. YMM4をrenderせず安全に閉じます。
4. 待機中terminalへ戻り、COLLECT と入力します。

件数、character 3/6、本文、順序、missing/duplicate、fps/frames/durationは
collectorが確認します。ユーザーが9件を手作業で数える必要はありません。

## Stop conditions

- YMM4がすでに起動中、または未保存・無関係な作業がある
- exact local project / result / batch-state targetが既にある
- 空でないproject/timeline、mapping dialog、error、update要求
- ゆっくり霊夢 / ゆっくり魔理沙以外へのbinding
- 保存先が表示された .local.ymmp と違う
- render、production、upload、publication、rights actionを要求される

## Recovery without YMM4 launch

manual save後にterminalだけ中断した場合は、YMM4を安全に閉じてから:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_import_batch.ps1 -CollectOnly -OperatorConfirmedNoMappingError

既存resultや失敗証拠を消さずに再実行したい場合は、operator directoryから
次を実行して、ignored local_outputs/archive/<timestamp>/ へ先に退避します。

    $archive = Join-Path ..\local_outputs ("archive\" + (Get-Date -Format "yyyyMMdd-HHmmss"))
    New-Item -ItemType Directory -Path $archive -Force
    Get-ChildItem -LiteralPath ..\local_outputs -File | Move-Item -Destination $archive

## Return

terminalの最大3項目だけを返します。actual YMM4 importが終わるまでは、
このtracked packageだけでmapping、sound、timing、subtitle appearance、
character behaviorの成功を主張しません。
