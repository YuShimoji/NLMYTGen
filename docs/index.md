# Local Markdown Browser Guide

このページは、リポジトリ内の Markdown をブラウザのツリーペインで閲覧し、Chrome / Edge / DeepL などのページ翻訳で一時確認しやすくするための入口です。既存の Markdown 正本を翻訳・要約・再構成するものではありません。

## 主な導線

- [Markdown Inventory](markdown-inventory.md): 除外ディレクトリを避けて列挙した `.md` 一覧。分類は配置・ファイル名・冒頭見出しからの実用的な推定です。
- [Project Overview](project-overview.md): 機能台帳、進捗、項目別実装、証跡、今後の入口をどこで見るかの早見表です。
- [Visual Proof Index](visual-proof-index.md): すぐ確認できるスクリーンショット、proof PNG、HTML review surface の索引です。
- [Turn-Based Development Map](turn-based-development-map.md): 日付ではなく、次の数ターンでどの判断を進めるかを見るための補助マップです。
- [Document Map](NAV.md): 既存のリポジトリ内ドキュメント案内。日常の読み順や正本の所在を確認する入口です。
- [Runtime State](runtime-state.md): 現在位置や次の安全な作業入口を確認する文書です。
- [Repo Local Rules](REPO_LOCAL_RULES.md): このリポジトリでの作業ルールと報告・検証の境界です。

## Common Foundation Cockpit

- [Common Foundation Cockpit](dashboard/index.html): common-foundation の現在状態、次アクション、artifact access、topic status を確認する master 上の review surface です。
- [Dashboard Access Guide](dashboard/README.md): `scripts/operator/open_dashboard.ps1` を使う開き方と fallback を確認できます。
- [Project Status JSON](dashboard/project-status.json): dashboard が読む repo-relative status registry です。
- [Feature Index](features/index.md) / [Workflow Index](workflows/index.md) / [Decision Index](decisions/index.md): common-foundation 関連の補助索引です。

## ローカル起動

PowerShell で、リポジトリ直下から次のどちらかを使います。

```powershell
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format source
uvx --from mkdocs-material mkdocs serve --dev-addr 127.0.0.1:8000
```

または、通常の Python 環境へ入れる場合:

```powershell
python -m pip install mkdocs-material
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format source
mkdocs serve --dev-addr 127.0.0.1:8000
```

ブラウザで `http://127.0.0.1:8000/` を開くと、左側のナビゲーションから主要文書を移動できます。ページ翻訳はブラウザ側の一時的な読解補助として使い、翻訳結果をこのリポジトリの正本として保存しないでください。

`_local/mkdocs-src` は MkDocs 用の一時ミラー、`_local/mkdocs-site` はビルド出力です。どちらも正本ではなく、`.gitignore` によりコミット対象外です。

## 再生成

Markdown 配置が変わったら、nav 候補や全件索引を再生成できます。既定では標準出力に出すだけで、既存ファイルは更新しません。

```powershell
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format nav
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format inventory
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format source
```

索引ファイルを更新する場合だけ、出力先を明示します。

```powershell
powershell -ExecutionPolicy Bypass -File tools/generate-doc-nav.ps1 -Format inventory -OutputPath docs/markdown-inventory.md
```
