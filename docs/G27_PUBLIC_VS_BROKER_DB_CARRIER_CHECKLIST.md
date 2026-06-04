# G27_PublicVsBrokerDB Carrier 作成チェックリスト

このチェックリストは、人間が YMM4 で `G27_PublicVsBrokerDB` の stable carrier `.ymmp` を作るための最小仕様です。  
これは template-first / slot-fill へ移行するための carrier 作成指示であり、slot contract、patch script、render、production readiness ではありません。

> Current status: this checklist is retained as G-27 case-specific reference
> evidence. Active generic screen-carrier work is superseded by
> [REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md](REFERENCE_DRIVEN_SCREEN_CARRIER_SPEC.md).
> The diagnostic G-27 carrier remains diagnostic-only unless a future operator
> explicitly reopens this case-specific path.

## 目的と境界

- 目的は、公開ポータルと業者 / private DB の情報差を、安定した二面構図として YMM4 上に固定すること。
- 初回 carrier は美麗さより安定性を優先する。
- 既存 visual proxy / micro scene / minimal probe は diagnostic-only であり、この carrier の代替にしない。
- agent は後続で carrier の実 item を readback してから、carrier に従属した slot contract を作る。
- carrier 未作成のまま、抽象 slot contract や raw geometry 生成へ進まない。

## 構図設計の理論的根拠

本 carrier は [`docs/SCENE_COMPOSITION_SCHEMA.md`](SCENE_COMPOSITION_SCHEMA.md) (Scene Composition Schema v0.1) の **`split` composition type** に該当する。
具体的な対応は次のとおり:

- §1 Composition Grid: 下記「画面比率レイアウト」と一致。outer safe band 5% / title band 8-12% / main canvas / caption safe area 18-22% をすべて満たす。
- §2.1 `split` composition type: 左 public panel (focal_anchor) / 中央 boundary (lock) / 右 broker panel (focal_anchor) の 3 領域構造。
- §3 Visual Role: `G27PBD_PublicCard1` 等の focal_anchor / supporting / boundary / label / decoration の割当を後段 sidecar に出す。
- §5.1 ShapeItem: `ShapeParameter.SizeMode=WidthHeight` 固定。`SizeAspect` + `Size=100` の anti-pattern は G-27 micro_scene_probe v1 で確認済みの失敗原因。
- §9 Adapter Patch Boundary: 「agent が patch してよい / してはいけない」項目と SCS §9 が一対一で対応。

## 画面前提

- フレームは 16:9 / 1920x1080。
- stage は light か dark のどちらか一系統に固定し、混在させない。
- 外周 safe margin は画面端から 5% 以上を目安にする。
- 下部 10–15% は caption safe area として空ける。
- 長い説明文は置かず、画面上のテキストは title / label / card text / badge だけにする。

## 画面比率レイアウト

| 領域 | 目安 | 役割 |
| --- | --- | --- |
| title band | 上 8–12% | 全体タイトル `G27PBD_Title` を置く |
| left public panel | `x=0.06〜0.08`, `y=0.18`, `w=0.38〜0.42`, `h=0.60` 前後 | 公開ポータル側。public card 2枚を入れる |
| center lock / boundary | `x=0.46〜0.52`, `w=0.06〜0.10` | 情報の境界 / lock / threshold を表す |
| right broker panel | `x=0.56〜0.58`, `y=0.18`, `w=0.36〜0.40`, `h=0.60` 前後 | 業者 / private DB 側。broker card 3枚を入れる |
| bottom caption safe area | 下 10–15% | 字幕・caption 用。carrier item を置かない |

YMM4 内の座標やサイズ値は、上記比率に近い見た目になるよう人間が調整する。agent は後で panel geometry、anchor、layout grid を変更しない。

## 必須 item name

初回 carrier ではカード数を増減しない。public card は 2 枚、broker card は 3 枚に固定する。

| item name | 種別の目安 | 役割 |
| --- | --- | --- |
| `G27PBD_BG` | 背景 / Shape / Image | stage 全体 |
| `G27PBD_Title` | Text | 画面上部の短いタイトル |
| `G27PBD_PublicPanel` | Shape / Group | 左 public panel の固定枠 |
| `G27PBD_PublicTitle` | Text | public panel 内の短い見出し |
| `G27PBD_PublicCard1` | Shape / Group / Text | public 側カード 1 |
| `G27PBD_PublicCard2` | Shape / Group / Text | public 側カード 2 |
| `G27PBD_BrokerPanel` | Shape / Group | 右 broker/private DB panel の固定枠 |
| `G27PBD_BrokerTitle` | Text | broker/private DB panel 内の短い見出し |
| `G27PBD_BrokerCard1` | Shape / Group / Text | broker 側カード 1 |
| `G27PBD_BrokerCard2` | Shape / Group / Text | broker 側カード 2 |
| `G27PBD_BrokerCard3` | Shape / Group / Text | broker 側カード 3 |
| `G27PBD_Lock` | Shape / Group / Text | 中央 lock / threshold |
| `G27PBD_Arrow` | Shape / Group | 任意の抽出 arrow。使わない場合も item は残して非表示にする |

複数 item で 1 つのカードや lock を構成する必要がある場合は、可能なら YMM4 側で Group 化し、group item に上記 item name を付ける。Group 化が難しい場合は、主要 item に上記 item name を付け、補助パーツは `G27PBD_PublicCard1_PartA` のような短い派生命名にする。

## Remarks の書き方

- Remark は item name と同じ、または `public panel` / `broker card 1` のような短い用途名だけにする。
- provenance、source path、candidate id、script line、not_creative_acceptance などの長文は Remark に書かない。
- 詳細 provenance は後続の sidecar JSON / readback report に保存する。

## slot marker 命名規則

- slot marker は item name を正とする。
- item name は必ず `G27PBD_*` で始める。
- agent が後で探す対象は、まず item name、次に短い Remark とする。
- 同じ item name を複数 item に重複させない。
- 非表示で保持する optional item も item name は固定する。例: `G27PBD_Arrow`。

## agent が後で patch してよい項目

- Text item の表示文字列。
- item の表示 / 非表示。
- item の開始 frame、長さ、必要最小限の timing。
- sidecar JSON / readback report に保存する provenance id。

## agent が patch してはいけない項目

- panel geometry。
- anchor / center point。
- colors。
- font hierarchy。
- layout grid。
- safe margin。
- caption safe area。
- public card / broker card の枚数。
- lock / boundary の配置。
- stage の light / dark 方針。

## carrier 作成後にユーザーが返す情報

- carrier `.ymmp` path。
- preview screenshot。
- timeline screenshot。
- representative item property screenshot:
  - `G27PBD_PublicPanel`
  - `G27PBD_PublicCard1`
  - `G27PBD_BrokerPanel`
  - `G27PBD_Lock`
- light stage / dark stage のどちらで作ったか。
- YMM4 で開いたときに、下部 caption safe area が空いているかの短いコメント。

## carrier 受領後に assistant が行う readback

- `.ymmp` が JSON として読めるか。
- 必須 item name が全て存在するか。
- item name が短く、`G27PBD_*` 形式になっているか。
- Remarks が短く、provenance を含んでいないか。
- public card が 2 枚、broker card が 3 枚で固定されているか。
- `G27PBD_Arrow` が存在し、使わない場合も非表示 item として保持されているか。
- panel geometry、anchor、colors、font hierarchy、layout grid を agent patch 対象から除外できるか。
- sidecar JSON / readback report に provenance を退避できる構造か。
- human GUI review で `layout preserved` を確認するための比較対象として使えるか。

## 完了の合図

この carrier 作成段階の完了は、carrier `.ymmp` path と指定 screenshot 一式が返された時点。  
その後に初めて、assistant は readback と anchored slot contract の準備に進む。
