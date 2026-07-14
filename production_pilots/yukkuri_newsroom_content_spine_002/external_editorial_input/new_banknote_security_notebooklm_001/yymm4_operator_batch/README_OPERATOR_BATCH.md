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

    powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_batch.ps1 -PreflightOnly

自動検出できない場合だけ、表示されたとおり -Ymm4Exe を付けます。

## 5 manual actions

1. このdirectoryで次を一度だけ実行します。
   powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_batch.ps1
2. YMM4に未保存の無関係な作業がないことを確認し、新規の空project / 空timelineを開きます。
3. 表示されたderived CSVを台本読み込みし、mapping/error/update/character mismatchが
   ない場合だけ、表示された .local.ymmp へ Project Save As します。
4. 9 cuesを一度previewし、発音または明らかなclippingをcue番号でメモします。
5. renderせずYMM4を安全に閉じ、terminalへ戻ってCOLLECTを入力し、続く1行へメモを入力します。

件数、character 3/6、本文、順序、missing/duplicate、fps/frames/durationは
collectorが確認します。ユーザーが9件を手作業で数える必要はありません。

## Stop conditions

- YMM4がすでに起動中、または未保存・無関係な作業がある
- exact local project / result / batch-state targetが既にある
- 空でないproject/timeline、mapping dialog、error、update要求
- ゆっくり霊夢 / ゆっくり魔理沙以外へのbinding
- 保存先が表示された .local.ymmp と違う
- collectorのparse error、9件/3対6/text/order不一致
- render、production、upload、publication、rights actionを要求される

## Recovery without YMM4 launch

manual save後にterminalだけ中断した場合は、YMM4を安全に閉じてから:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\run_new_banknote_yymm4_batch.ps1 -CollectOnly -OperatorConfirmedNoMappingError

既存のproject/result/batch-state/observationは自動で削除・移動・上書きしません。
再実行する場合は、この4個のoperator-owned fileだけをユーザーが個別に退避し、
同じlocal_outputs内のsalvage evidenceには触れないでください。

## Return

terminalの最大3項目だけを返します。actual YMM4 importが終わるまでは、
このtracked packageだけでmapping、sound、timing、subtitle appearance、
character behaviorの成功を主張しません。
