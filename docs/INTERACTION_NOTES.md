# Interaction Notes
# 報告UI・手動確認・質問形式に関する project-local メモ。

## 手動確認の出し方
- 手動確認項目は本文で提示する。
- AskUserQuestion では `OK / NG番号` だけを聞く。
- 手動確認依頼と次アクション選択を同じ質問に混ぜない。

## 禁止パターン
- AskUserQuestion の `question` に Markdown テーブルを入れる
- 選択肢を commit / しない の yes/no で埋める
- 既知文脈を「詳細を教えてください」で再質問する

## ユーザーが嫌う形式
- 進路選択を不必要に狭める二択
- 既知文脈を無視して「詳細を教えてください」と再説明させる問い
- priority と status を曖昧にした提案
- 生成物の価値経路を示さないまま「テンプレートを作る」話に寄ること
- 読みにくい崩れた表や、情報量の多い ask を 1 問に詰め込むこと

## 報告メモ
- BLOCK SUMMARY では、まず bottleneck と trust assessment を示す
- handoff では「何が抜けているか」「次にやってはいけないこと」も残す
- 再開時の repeated context は、まず `docs/ai/*.md` と project-local canonical docs を読んでから扱う
- 字幕改行の報告では、「長すぎる行が減ったか」と「残りが bulk pain か individual judgement か」を分けて伝える。境界ケース段階に入ったら、rule 追加と corpus 収集を混同しない
