# NLMYTGen の Cloud 開発

CloudではPython変換処理、CLI、Electronのコードを編集し、同梱fixtureによる検証を実行する。YMM4での実画面確認、WPF計測、実音声の評価はWindowsで実施する。

## 環境を準備する

ChatGPTの「設定 → Codex Cloud → 環境」で `Media Contents Projects` を作成し、今回指定された `YuShimoji/NLMYTGen`、`YuShimoji/ClipPipeGen`、`YuShimoji/FastFictionFactory` だけを選ぶ。各タスクの作業対象は明示する。ClipPipeGenからの再利用は既存のCLI subprocess境界を使う。

Cloud準備の版は `codex/cloud-development-20261011`。リポジトリの既定ブランチとは別なので、セットアップ会話でこのブランチを指定し、`git branch --show-current` と `git rev-parse HEAD` を確認してから実行する。

| 項目 | NLMYTGen の設定 |
| --- | --- |
| ランタイム | Python 3.11、Node.js 24、uv |
| Install script | このリポジトリで `bash scripts/codex/setup.sh` |
| Start skill | `AGENTS.md` のread orderを読み、`bash scripts/codex/check.sh` を実行。常駐サービスは不要 |
| ネットワーク | 既存GitHub接続とパッケージ取得に必要な範囲 |
| 秘密情報 | 基本開発では不要 |
| 共有 | Only me |

Install scriptは既存の `uv.lock`、`gui/package-lock.json` を使う。依存の更新、Electronの起動、動画・音声生成は行わない。準備と検証が成功したら「Publish」で環境を保存する。再準備では同じコマンドを使う。

## 実装後の検証

```bash
bash scripts/codex/check.sh
# 変更したモジュールのfocused testも実行する。
.venv/bin/python -B -m pytest tests/<対象のテスト>.py
```

checkはCLIの起動、IR validation、字幕の構造分割禁止、NotebookLM入力契約、portable review bundleのpath/receipt/registry拒否系、GUIのbatch observabilityを確認する。portable review bundleの9テストはignoredのcue_002 source packetを要求するため、既存の `requires_local_evidence` markerで入力locatorを示す。素材なしのcheckoutではskipとして表示し、exact素材があれば実行する。全pytestは既知のartifact/path driftとfixture書換えがあるため既定の完了条件にしない。詳しい判断は `docs/REPO_LOCAL_RULES.md` を使う。

Windowsの隔離checkoutで同じ検証を行う場合:

```powershell
uv sync --locked --extra dev --python 3.11
$env:NLMYTGEN_PYTHON = '.venv/Scripts/python.exe'
& 'C:\Program Files\Git\bin\bash.exe' scripts/codex/check.sh
```

## 素材とレビュー

CloudにはGitで管理されたファイルだけが渡る。`_local/`、ignored output、未保存のYMM4状態、PC内のabsolute locatorをCloudの実在ファイルとして扱わない。exact素材が必要ならその操作を保留し、同梱fixtureで進められる開発を続ける。素材欠落を埋めるためのfetch、音声生成、代替素材採用は別の明示指示が必要。

修正前にユーザー現象と期待結果、原因根拠または判別できる仮説を示す。原因不明の数値調整を反復しない。Cloudの検証結果には、確認した動作とWindowsで残る実画面・実音声確認を対応させる。既存のaccepted/rejected判断はrepo-local正本から読む。

ローカル個人skillはCloudへ自動同期されない。Cloudのエージェントはこのリポジトリの `AGENTS.md` と正本文書を使い、既存のdirty、untracked、ignored素材を保持する。下流から親チャットへの通知・ACK・callbackは追加せず、結果を担当リポジトリへ保存する。

現在のCloud環境作成・Publish手順: [OpenAI公式ガイド](https://learn.chatgpt.com/docs/environments/cloud-environments)。
