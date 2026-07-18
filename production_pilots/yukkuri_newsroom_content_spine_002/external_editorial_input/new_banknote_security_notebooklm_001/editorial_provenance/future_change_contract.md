# Future substantive script change contract

現在の9 cue、順序、話者、scene、claim/trace、CSV、YMM4観測identity、visual route入力は content lock の対象です。現在のユーザー承認はこの状態で次へ進むためのもので、将来の silent edit を許可しません。

## 自動再生成できる変更

encoding、serialization、hash/readback、相対リンク、同一内容のalias projectionなど、意味・本文・claim・route定義を変えない機械的変更だけが対象です。実行時は command、入力/出力hash、変更理由、検証結果を receipt に残します。

## 事前に delta receipt が必要な変更

本文の言い換え、短縮、追加、削除、並べ替え、bridge、話者、scene、claim採用、evidence edge、visual input timingの変更は substantive change です。次の human review または YMM4 gate より前に、少なくとも次を見える形で残します。

- predecessor lock ID と successor revision ID
- cueごとの before/after hash と human-readable delta
- operation class、actor、authority、変更理由、影響するclaim/source
- semantic impact と evidence impact
- requested-by と approval status
- invalidated artifact hashes と再生成した downstream identities

既存 receipt は上書きせず、successor receipt を作ります。source-backed であることや品質改善は、未記録の本文変更を正当化しません。
