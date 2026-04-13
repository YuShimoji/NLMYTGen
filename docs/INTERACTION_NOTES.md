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
- `判断をお願いします` `何が足りないか教えてください` のような broad question で停止する
- 同じ確認点の YMM4 visual proof を繰り返し要求する

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

## face サブクエスト報告
- face 問題は `FACE_UNKNOWN_LABEL` / `PROMPT_FACE_DRIFT` / `FACE_ACTIVE_GAP` / `ROW_RANGE_*` / `FACE_MAP_MISS` / `IDLE_FACE_MAP_MISS` / `VOICE_NO_TACHIE_FACE` の failure class 名で報告する
- 「何が足りないですか」「どこを見ればよいですか」の broad question では止まらず、failure class ごとの next action を先に提示する
- failure class が mechanical に確定しているときは、同じ趣旨の YMM4 visual proof を追加で要求しない

## timeline サブクエスト報告
- timeline 問題は 1 つの broad frontier として報告せず、`slot patch` / `native-template measurement` / `overlay-se insertion` の packet 名で分けて報告する
- mechanical failure と creative judgement を混ぜない。前者は registry gap / write route / readback mismatch として示し、後者は見た目・テンポ・密度の判断として分離する
- timeline packet でも repeated visual proof を要求しない。初回 proof または最終 creative judgement に必要な場合だけ visual check を使う
- timeline packet の completion 報告では、visual impression ではなく dry-run/readback の結果を先に根拠として示す。コード変更がないときにテストを回さない

## 開発ドリフト回避
- 新しい自動化経路を提案する際は、現行ロードマップ (YMM4-AUTOMATION-RESEARCH.md セクション4) の段階構成との整合を示すこと
- 研究 (ymmp 解析、プラグイン API 調査、外部ツール評価等) と開発 (IR 定義、プロンプト改訂等) を混同しない。研究に2ブロック以上費やす場合は一度止まって開発に戻る
- テスト設計が主活動になっていないか確認する。テストはコード変更時のみ。ドキュのみでは回さない。completion で pytest を示すのも `src/` / `gui/` ロジック変更ブロックのみ（REPO_LOCAL_RULES と同じ）
- 外部ツール (YMovieHelper 等) を「主軸」として採用する提案には、運用依存軸 (保守性、メンテナンス状況) の評価を必須とする。サービス終了済み・更新停止ツールへの依存設計は避ける

## 常設ガード (2026-04-05)
- `docs/REPO_LOCAL_RULES.md` に block-start checklist を置き（正本）、毎ブロックの判断を強制する（`.claude/CLAUDE.md` は入口）
- `.claude/hooks/guardrails.py` で repo 外 project / memory / docs 参照、broad question による停止、反復 visual proof 要求を reject する
