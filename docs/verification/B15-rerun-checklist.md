# B-15 Rerun Checklist

更新後 packet を外部 GPT / Automation に再投入するときの最短 checklist。

## 使うファイル

- packet: `samples/*_cue_packet.md`
- proof log: `samples/*_cue_workflow_proof.md`
- 前回の実レスポンス: `samples/*_cue_memo_received.md`

## 手順

1. 更新後の `*_cue_packet.md` を開く
2. 外部 GPT / Automation に packet 全文を渡す
3. 次の 1 文だけ追加する

```text
この packet の constraints と response_preferences を守って、output contract に沿う cue memo だけを返してください。
```

4. 返ってきた cue memo を前回のものと見比べる
5. `*_cue_workflow_proof.md` に差分メモを書く

## 今回見るポイント

- section 数が増えすぎていないか
- `primary_background` が 1 つに絞られているか
- `supporting_visual` が補助に留まっているか
- `sound_cue_optional` が本当に optional 扱いになっているか
- `operator_todos` が長すぎないか

## OK の目安

- 前回より背景候補が絞られている
- SE の押し付け感が薄い
- cue memo を見たときに「何を採用するか」が前回より速く決められる

## NG の目安

- まだ背景候補が多すぎる
- sound cue が section ごとに必ず出てくる
- section 数が増えすぎて、逆に選択コストが上がる
