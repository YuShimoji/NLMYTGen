# Content Transformation Provenance Contract

この contract は、入力された原稿・transcript・source material が review 済み artifact と機械出力へ変わるまでを、後から検査できる product artifact にするための受入条件です。生成 Worker の権限や会話履歴を正本にせず、tracked artifact、hash、visible diff、human approval を正本にします。

## 受入に必要な stage record

内容を変える、選ぶ、除外する、並べ替える、言い換える、または機械形式へ射影する各 stage は、次を記録します。

| 記録要素 | 必要な内容 | 受入を止める例 |
| --- | --- | --- |
| Stage identity | 安定した stage ID、type、順序、status | 同名 stage の上書き、順序不明 |
| Input / output identity | repo-relative path、SHA-256、必要なら immutable Git commit | hash 不明、private absolute path の追跡 |
| Actor class | user、NotebookLM、Worker_mechanical、Worker_source_verification、Worker_editorial、human_approval | 「AI」だけで編集主体が判別できない |
| Change class | M / E / S / U のいずれか。複合時は主分類と副分類 | editorial change を mechanical と記録 |
| Affected IDs | claim、cue、meaning unit、source ID | 変更範囲が narrative だけ |
| Meaning / evidence impact | factual meaning と evidence identity を別々に判定 | 言い換えを理由に factual removal を隠す |
| Approval impact | 維持、失効、または renewed approval 待ち | post-approval edit を silent に採用 |
| Before / after | 数量、短い要約、visible rationale | 「品質改善」の一語だけ |
| Rejection / omission retention | 非採用理由と、後から再検討できる retained lane | rejected claim を消去 |
| Current approval status | receipt ID と hash validation 結果 | 会話上の承認だけに依存 |

raw body や source body を追跡する必要はありません。identity receipt、line fingerprint、bounded paraphrase、claim ID、official support location で十分な場合は、private/raw content を埋め込まない方を優先します。

## 変更 class と gate

| Class | 対象 | 自動処理 | Human approval |
| --- | --- | --- | --- |
| `M_MECHANICAL` | encoding、serialization、speaker alias、hash、path-independent packaging | 内容 hash が同一で、ledger に記録される場合だけ可 | 内容 hash 不変なら既存 approval を維持可能 |
| `E_EDITORIAL_EVIDENCE_PRESERVING` | reword、shorten、order、connective、voice、compression | approval 前でも visible lineage が必要 | approval 後は新 revision、visible diff、renewed approval 必須 |
| `S_SEMANTIC` | factual addition/removal、causal implication、judgment、statistic、claim adoption | source evidence と visible diff が必要 | 常に明示承認が必要 |
| `U_UPSTREAM` | source set、NotebookLM regeneration、replacement transcript | 新 upstream snapshot が必要 | milestone authorization と successor approval が必要 |

複数 class が同時に発生する stage は、より強い gate を主分類にします。例えば claim を発話から外しつつ文章を短くする変更は、editorial polish だけでなく `S_SEMANTIC` として扱います。

## Cue-level lineage

最終 cue は clause / meaning-unit 粒度で次を分けます。

- submitted input へ戻る claim ID、line ordinal、line fingerprint
- adopted verified claim と official source/support location
- factual paraphrase unit
- source quotationではない editorial connective
- source quotationではない character-voice phrasing
- structural role と最後に内容を変えた stage
- omitted verified claim の retained lane
- approval receipt ID と現在の validity

既存 evidence が token authorship を記録していない場合、token-by-token origin を推定しません。`unknown` や package-level precision は欠陥の隠蔽ではなく、証拠境界の正確な表現です。

## Approval receipt と silent-change rejection

approval receipt は approved commit、file hashes、cue/order/scene/speaker contract、claim/evidence contract、permission boundary、invalidation rules を固定します。receipt 自身を自己 hash せず、下流 manifest が receipt hash を固定します。

approval 後に content または structure を変える場合は、既存 receipt を上書きしません。新 revision ID、visible diff、updated transformation ledger、失効した prior receipt への参照、renewed human approval を持つ successor receipt を作ります。validator や operator preflight は、approved file、receipt、lineage のいずれかが drift した時点で停止し、script や CSV をその場で再生成して修復してはいけません。

## Artifact-family acceptance

artifact family は、stage coverage、cue/claim/unit/edge coverage、hash consistency、approval validity、privacy boundary、deterministic second pass がすべて通ったときだけ受け入れます。operator や serialization package がある場合は、実行直前と result collection 直前の両方で同じ lock を再検証します。
