# docs/verification — 索引と読み方

本ディレクトリは **検証記録・提案ドラフト・実装メモ・オペレータ proof** が混在する。ファイル名の `proposal` / `implementation` / `proof` / `checklist` は目安であり、**現行仕様の正本は下記の固定ドキュメント**を優先する。

## 現行正本（仕様・台帳・いまの位置）

| 用途 | 正本 |
|------|------|
| 機能の全件・ステータス | [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) |
| 演出 IR のフィールドと CLI 適用の対応 | [PRODUCTION_IR_CAPABILITY_MATRIX.md](../PRODUCTION_IR_CAPABILITY_MATRIX.md) |
| 演出 IR 仕様（語彙・構造） | [PRODUCTION_IR_SPEC.md](../PRODUCTION_IR_SPEC.md) |
| 自動化の境界（YMM4 内 / 外） | [AUTOMATION_BOUNDARY.md](../AUTOMATION_BOUNDARY.md) |
| 現在位置・次アクション | [runtime-state.md](../runtime-state.md) |
| 意思決定・handoff | [project-context.md](../project-context.md) |
| 並行作業の手順（オペレータ） | [OPERATOR_PARALLEL_WORK_RUNBOOK.md](../OPERATOR_PARALLEL_WORK_RUNBOOK.md) |

## 本ディレクトリの典型的な文書タイプ

- **`*-proposal.md` / `*-draft-*`**: 採用前の設計案。本文または先頭注記で現行正本への誘導があることが多い。
- **`*-implementation.md` / `*-patch-design.md`**: 実装時の記録。コードと [FEATURE_REGISTRY.md](../FEATURE_REGISTRY.md) が矛盾する場合は **コードと台帳を優先**し、本類は履歴として読む。
- **`*-proof.md` / `*-checklist.md`**: オペレータまたは E2E の検証手順・結果。
- **ファイル名と内容のずれ**: 歴史的経緯で `deferred` 等の名前のまま、本文で「実装済み」と更新されているものがある。**判断は本文先頭と上表の正本**に従う。リネームは参照切れリスクがあるため、原則として先頭注記の更新を優先する。

## アーカイブ方針（運用ルール）

- 新規の検証記録は必要に応じて本ディレクトリに追加する。
- **過去文書を「無効」とする場合は、先頭に日付付きの注記**で現行正本（上表）へ誘導する。フォルダ分けや一括リネームは、リンク維持のコストが大きいため必須としない。
- フル再アンカリングや仕様確認では、まず [AGENTS.md](../../AGENTS.md) → 上表の正本を読み、本ディレクトリは **特定トピック（例: B-11 workflow proof）を追うとき**に限定すると負荷が下がる。
