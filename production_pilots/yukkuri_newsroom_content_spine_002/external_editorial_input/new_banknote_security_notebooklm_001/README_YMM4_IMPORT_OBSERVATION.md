# 新紙幣 YMM4 import observation

> **INTERNAL REVIEW / NOT FINAL / NON-PUBLIC / NON-PRODUCTION**

ユーザー操作で保存されたlocal YMM4 projectをheadlessに再解析し、CSV import
gateの構造的成功を確認したsanitized review surfaceです。local project、result、
batch stateはignoredのままbyte-preservedで、ここにはrepo-relative identity、
basename、hash、size、mtime、検証値だけを記録します。

## 結果

- operator result: `success` / failed checks `0`
- project: `new_banknote_yymm4_import_observation.local.ymmp`
- VoiceItems: `9`
- characters: ゆっくり霊夢 `3` / ゆっくり魔理沙 `6`
- text/order: exact / missing `0` / duplicate `0`
- timing: `60 fps` / `4415 frames` / `73.583333 seconds`
- project SHA-256: `beee7eab59196453c8d36b8889343cc82e876ea69e2bb00f5576bf17987eaa54`
- result SHA-256: `e4ecb1bf5e4b5780990a00094804dd871d66068a917000015f9fecfd83e8ddfa`

## Evidence boundary

CSV import gateはpassedです。mapping/error/update/character mismatchがなかったことは
operator observationであり、project構造・本文・順序・timingはmachine verifiedです。
音声のリズム・発音、字幕の読みやすさ、visual effectiveness、render、production、
rights、publicationは未検証です。import gateではImageItem、独立TextItem、renderを
要求していません。

## Next review

Route A / B / C と推奨S1/S2/S3 spineは
`visual_scene_decision/README_VISUAL_SCENE_DECISION.md`から確認します。推奨は選択済みを
意味せず、visual YMM4 projectの作成はまだ許可されていません。
