# B-16 Rerun Checklist

更新後 packet を外部 GPT / Automation に再投入するときの最短 checklist。

## 使うファイル

- packet: `samples/*_diagram_packet.md`
- rerun prompt: `samples/*_diagram_rerun_prompt.txt`
- proof log: `samples/*_diagram_workflow_proof.md`
- baseline notes: `samples/*_diagram_baseline_notes.md`
- diff template: `samples/*_diagram_rerun_diff_template.md`
- quickstart: `samples/*_diagram_quickstart.md`

## 手順

1. 更新後の `*_diagram_packet.md` を開く
2. 外部 GPT / Automation に packet 全文を渡す
3. `*_diagram_rerun_prompt.txt` の中身をそのまま追加する
4. もし prompt ファイルを使わないなら、次の 1 文だけ追加する

```text
この packet の constraints と response_preferences を守って、output contract に沿う diagram brief だけを返してください。
```

5. 返ってきた diagram brief を見ながら、図にするべき区間と入れる要素をメモする
6. `*_diagram_baseline_notes.md` と見比べて差分だけ確認する
7. `*_diagram_rerun_diff_template.md` に rerun 差分を短く書く
8. `*_diagram_workflow_proof.md` に時間差と所感を書く

## Time Comparison の書き方

- `before`:
  - diagram brief なしで「どの区間を図にするか」「各図に何を入れるか」を決める想定時間
- `after`:
  - 今回の diagram brief を見ながら、同じ判断が終わるまでの実時間または概算
- `delta`:
  - `before - after`

ここでは図版を実際に作る時間までは含めなくてよい。
測る対象はあくまで「diagram planning の白紙時間」と「図に入れる要素を決める時間」。

## 今回見るポイント

- 図に向く区間だけが選ばれているか
- 背景や B-15 cue memo で十分な区間まで diagram 化されていないか
- `goal` が図を作る理由として明確か
- `must_include` が多すぎず少なすぎないか
- `label_suggestions` がそのまま着手の助けになるか
- `avoid_misread` が実際に役立つか

## OK の目安

- 「何を図にするか」を考える時間が減る
- 図に入れる要素が早く決まる
- cue memo と違う役割として使い分けできる

## NG の目安

- 抽象論だけで、図に起こすときの助けにならない
- B-15 cue memo と内容がほぼ同じ
- 図にしなくてもよい section まで機械的に拾ってしまう
- `must_include` や `label_suggestions` が冗長すぎる
