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

## 開発ドリフト回避
- 新しい自動化経路を提案する際は、既存の YMovieHelper 連携経路 (G-02/G-05) との比較を必須とする。「面白そうだから」で経路を増やさない
- 研究 (ymmp 解析、プラグイン API 調査等) と開発 (build-ymh 実装等) を混同しない。研究に2ブロック以上費やす場合は一度止まって開発に戻る
- テスト設計やテストフレームワーク整備が開発の主活動になっていないか定期確認する。テストは成果物の検証手段
