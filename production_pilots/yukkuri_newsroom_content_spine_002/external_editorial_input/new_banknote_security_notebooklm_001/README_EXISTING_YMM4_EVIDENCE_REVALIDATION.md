# Existing YMM4 Evidence Revalidation

> **READ-ONLY REVALIDATION — INTERNAL IMPORT OBSERVATION — NON-PRODUCTION**

このpackageは、既存のignored YMM4 project、operator result、batch stateを
削除・移動・上書きせず、現在のhuman approvalとT00–T07 content lineageへ
再接続したsanitized successor evidenceです。YMM4は再実行していません。

## 結論

- status: `accepted`
- mode: `read_only_non_overwriting`
- VoiceItems: `9`
- ゆっくり霊夢 / ゆっくり魔理沙: `3 / 6`
- exact text / order: `true`
- missing / duplicate / reordered: `0 / 0 / false`
- fps / frames / duration: `60 / 4415 / 73.583333`
- source evidence before/after: `unchanged`

既存resultとcurrent parserのproject readbackは、project hash、9 VoiceItems、3/6、
本文、順序、timingで一致しました。approved script、CSV、claim/source、lineageは
変更していません。

## 音声品質の境界

pronunciationは`unknown`、clippingは
`unknown`、rhythmは`unknown`です。
構造的なimport成功から音声品質を推定せず、acceptanceは主張しません。

## Version warning

existing YMM4は`4.54.0.1+76b177dd451f9d162816dabc4ac658180e869582`、profile observationは
`4.53.0.9`です。差分はwarning debtであり、
現在のhash/text/order compatibilityを自動で失敗にはしません。

## 読む順序

1. `existing_yymm4_evidence_revalidation_receipt.json` — current lockとexisting evidenceの受入正本
2. `existing_yymm4_evidence_revalidation_readback.json` — checksとmetricの短いreadback
3. `existing_yymm4_evidence_current_lineage_traceability.json` — approval/lineage/cue接続
4. `existing_yymm4_evidence_limitations.md` — 未解消境界

## 次のgate

次は分岐したnew-banknote successor branchesのintegration auditです。このpackageは
branch integration、visual route選択、render、production、rights、publication、
master integrationを承認しません。
