# Failure Class 診断マトリクス

`validate-ir` / `apply-production` で出力される ERROR / WARNING の一覧と対処法。

## 読み方

| 深刻度 | 意味 | 対応 |
|--------|------|------|
| **ERROR** | `validate-ir` で検出。IR を修正するまで先に進めない | IR JSON または registry を修正して再実行 |
| **FATAL WARNING** | `patch-ymmp` 実行時に検出。パッチ適用を中断する | map / template / IR を修正して再実行 |
| **ADVISORY** | パッチは続行するが品質リスクあり | 許容判断して続行、または IR / map を改善 |

## 診断フロー

```
1. validate-ir を実行
   ├─ ERROR あり → IR or registry を修正 → 1 に戻る
   └─ ERROR なし → 2 へ

2. apply-production --dry-run を実行
   ├─ FATAL WARNING あり → map or template を修正 → 2 に戻る
   └─ FATAL WARNING なし → 3 へ

3. apply-production -o out.ymmp を実行
   ├─ ADVISORY WARNING あり → 許容判断。必要なら map/IR を改善
   └─ 完了 → YMM4 で目視確認
```

---

## ERROR 一覧（validate-ir）

| Class | 発生条件 | 直すもの |
|-------|---------|---------|
| `IR_EMPTY` | utterance が 0 件 | IR JSON に utterance を追加 |
| `FACE_UNKNOWN_LABEL` | face/idle_face が palette にない | face_map を更新、または IR の face を修正 |
| `PROMPT_FACE_DRIFT` | face が Custom GPT prompt 契約にない | prompt contract を更新、または IR を修正 |
| `FACE_ACTIVE_GAP` | キャラに必要な face が palette に未定義 | palette に face を追加 |
| `SLOT_UNKNOWN_LABEL` | slot が registry にない | slot_map に追加 |
| `OVERLAY_UNKNOWN_LABEL` | overlay が registry にない | overlay_map に追加 |
| `OVERLAY_INVALID_TYPE` | overlay の型が不正（文字列/配列/null 以外） | IR の overlay フィールドを修正 |
| `SE_UNKNOWN_LABEL` | se が registry にない | se_map に追加 |
| `SLOT_REGISTRY_GAP` | キャラの default_slot が slot registry にない | slot_map の slots に追加 |
| `BODY_ID_UNKNOWN` | body_id が face_map_bundle にない | bundle にbody を追加、または IR を修正 |
| `BG_ANIM_UNKNOWN_LABEL` | bg_anim が許可値以外 | `none/pan_left/pan_right/zoom_in/zoom_out/ken_burns` のみ |
| `TRANSITION_UNKNOWN_LABEL` | transition が許可値以外 | `none/fade` のみ |
| `MOTION_UNKNOWN_LABEL` | motion が許可値以外 | `none/pop_in/slide_in/shake_small/shake_big/bounce/fade_in/fade_out` |
| `MOTION_MAP_UNKNOWN_LABEL` | motion が --motion-map にない | motion_map にラベルを追加 |
| `GROUP_MOTION_INVALID_TYPE` | group_motion が文字列でない | IR を修正 |
| `GROUP_TARGET_INVALID_TYPE` | group_target が文字列でない | IR を修正 |
| `GROUP_TARGET_EMPTY` | group_target が空文字/空白のみ | 削除するか有効な値を設定 |
| `GROUP_TARGET_SURROUNDING_WHITESPACE` | group_target の前後に空白 | 空白を除去 |
| `GROUP_TARGET_NEWLINE` | group_target に改行を含む | 改行を除去 |
| `GROUP_MOTION_UNKNOWN_LABEL` | group_motion が registry にない | group_motion_map に追加 |
| `ROW_RANGE_OVERLAP` | row_start が前の utterance の row_end と重複 | row range を修正 |

---

## FATAL WARNING 一覧（patch-ymmp）

これらが 1 件でも出るとパッチ適用が中断される。

| Class | 発生条件 | 直すもの |
|-------|---------|---------|
| `VOICE_NO_TACHIE_FACE` | VoiceItem に TachieFaceParameter がない | YMM4 ���ンプレを修正（立ち絵付きにする） |
| `FACE_MAP_MISS` | face が face_map にない | face_map.json にラベルを追加 |
| `IDLE_FACE_MAP_MISS` | idle_face が face_map にない | face_map.json にラベルを追加 |
| `ROW_RANGE_MISSING` | row_start/row_end が VoiceItem 範囲外 | row range を確認。`--csv` + `annotate-row-range` |
| `ROW_RANGE_INVALID` | row_start < 1 または row_end < row_start | row range の値を修正 |
| `SLOT_CHARACTER_DRIFT` | 同キャラが複数の slot を使用 | IR で slot を統一 |
| `SLOT_DEFAULT_DRIFT` | slot が registry の default_slot と不一致 | IR を修正、または slot_map の default を変更 |
| `SLOT_REGISTRY_MISS` | slot が slot_map にない | slot_map.json に追加 |
| `SLOT_NO_TACHIE_ITEM` | TachieItem が存在しない | YMM4 テンプレに TachieItem を追加 |
| `SLOT_VALUE_INVALID` | slot の x/y/zoom が数値でない | slot_map.json の値を修正 |
| `MOTION_MAP_MISS` | motion が tachie_motion_map にない | map にラベルを追加 |
| `MOTION_NO_TACHIE_ITEM` | TachieItem がない（motion 適用不可） | テンプレに TachieItem を追加 |
| `GROUP_MOTION_NO_GROUP_ITEM` | GroupItem が存在しない | テンプレに GroupItem を追加 |
| `GROUP_MOTION_TARGET_MISS` | group_target が GroupItem の Remark と不一致 | YMM4 で Remark を確認して揃える |
| `GROUP_MOTION_TARGET_AMBIGUOUS` | group_target 省略だが GroupItem が複数 | group_target を明示指定 |
| `OVERLAY_MAP_MISS` | overlay が overlay_map にない | overlay_map.json に追加 |
| `OVERLAY_NO_TIMING_ANCHOR` | タイミング解決不可 | utterance index と VoiceItem の対応を確認 |
| `OVERLAY_SPEC_INVALID` | path 不足 / anchor 不正 / length 不正 | overlay_map のエントリを修正 |
| `SE_MAP_MISS` | se が se_map にない | se_map.json に追加 |
| `SE_NO_TIMING_ANCHOR` | タイミング解決不可 | utterance index と VoiceItem の対応を確認 |
| `SE_SPEC_INVALID` | path 不足 / anchor 不正 / length 不正 | se_map のエントリを修正 |

---

## ADVISORY WARNING 一覧

パッチは続行する。品質改善のために確認を推奨。

| Class | 発生条件 | 対応 |
|-------|---------|------|
| `FACE_SERIOUS_SKEW` | serious が全発話の 40% 超 | 表情を多様化（LLM に指示） |
| `FACE_RUN_LENGTH` | 同じ face が 4 発話以上連続 | 表情にバリエーションを追加 |
| `FACE_LATENT_GAP` | palette の face が IR で未使用 | 任意: IR で使うか palette から削除 |
| `FACE_PROMPT_PALETTE_GAP` | prompt 許可だが palette に未登録 | palette を拡張 |
| `FACE_PROMPT_PALETTE_EXTRA` | palette にあるが prompt 未許可 | prompt contract を更新 |
| `IDLE_FACE_MISSING` | idle_face が IR に含まれない | 任意: idle_face を追加 |
| `BG_MISSING` | macro に default_bg がない | macro.sections に背景を定義 |
| `ROW_RANGE_INFO` | row_range も CSV も指定されていない | `--csv` or `annotate-row-range` を使用 |
| `GROUP_MOTION_DRIFT` | 同 target に複数の group_motion | IR で統一 |
| `GROUP_MOTION_MAP_MISS` | group_motion が map にない（patch 時） | group_motion_map に追加 |
| `GROUP_MOTION_VALUE_INVALID` | x/y/zoom が非数値 | map の値を修正 |
| `BG_ANIM_MAP_MISS` | bg_anim が adapter map にない | bg_anim_map に追加 |
| `BG_ANIM_SPEC_INVALID` | video_effect が不正 | map エントリを修正 |
| `BG_ANIM_UNKNOWN` | bg_anim が patch 未対応 | スキップされる。将来対応待ち |
| `BG_NO_TIMING_ANCHOR` | 背景タイミング解決不可 | section 境界を確認 |
| `BG_SPAN_OVERLAP` | 背景スパンが重複 | section 境界を調整 |
| `MOTION_SPEC_INVALID` | motion の video_effect が不正 | motion_map を修正 |
| `TRANSITION_MAP_MISS` | transition が map にない | transition_map に追加 |

---

## よくあるシナリオと対処

### 「全部 FACE_MAP_MISS で止まる」

**原因**: face_map が古い。palette を変更した後に `extract-template` を再実行していない。

**対処**:
```bash
uv run python -m src.cli.main extract-template --labeled palette.ymmp -o face_map.json
```

### 「ROW_RANGE_MISSING が大量に出る」

**原因**: IR に row_start/row_end がない、かつ `--csv` を指定していない。

**対処**:
```bash
uv run python -m src.cli.main annotate-row-range ir.json --csv script.csv -o ir_annotated.json
```

### 「GROUP_MOTION_TARGET_MISS」

**原因**: IR の `group_target` が GroupItem の `Remark` と一致していない。

**対処**: YMM4 でテンプレの GroupItem の Remark を確認し、IR の `group_target` を揃える。

### 「VOICE_NO_TACHIE_FACE」

**原因**: YMM4 テンプレの VoiceItem に TachieFaceParameter が設定されていない（立ち絵なしテンプレ）。

**対処**: YMM4 でキャラクターに立ち絵を割り当ててからテンプレを再保存。

### 「OVERLAY_NO_TIMING_ANCHOR / SE_NO_TIMING_ANCHOR」

**原因**: IR の utterance index と ymmp の VoiceItem の対応が取れていない。

**対処**: `--csv` オプションで行番号ベースのアンカリングを使用するか、IR の index を VoiceItem の出現順に合わせる。
