"""face_map_bundles/haitatsuin.json を palette 由来 6 表情に拡張.

方針:
- 既存 3 表情 (neutral/smile/serious) は **保持** (user 修正値を上書きしない)
- palette.ymmp 由来の 6 表情 (angry/sad/serious/smile/surprised/thinking) のうち、
  既存に無いラベル (angry/sad/surprised/thinking) を新規追加
- パスは `D:\\MovieCreationWorkspace\\` → `..\\Mat\\` に変換
- palette に Other/Back 系は抽出されないため、既存 neutral の値を踏襲
- 霊夢は palette に surprised 無し → skip (FACE_ACTIVE_GAP の data-side gap としてそのまま)
- 実在性を全件検証
"""
import json
import pathlib
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

REPO = pathlib.Path('.').resolve()
FACE_MAP = REPO / 'samples' / 'face_map_bundles' / 'haitatsuin.json'
PALETTE_FACE_MAP = REPO / 'samples' / '_probe' / 'b2' / 'palette_extract' / 'face_map.json'
BACKUP = REPO / 'samples' / '_probe' / 'b2' / 'haitatsuin_face_map_pre_expand.json'
YMMP_BASE = REPO / 'samples' / 'characterAnimSample'  # ymmp 相対の基点

BS = chr(92)
OLD_PREFIX = f'D:{BS}MovieCreationWorkspace{BS}'
NEW_PREFIX = f'..{BS}Mat{BS}'


def convert_path(p: str) -> str:
    if isinstance(p, str) and p.startswith(OLD_PREFIX):
        return NEW_PREFIX + p[len(OLD_PREFIX):]
    return p


def verify(rel: str) -> bool:
    return (YMMP_BASE / rel.replace(BS, '/')).exists()


def main():
    shutil.copy2(FACE_MAP, BACKUP)
    print(f'backup: {BACKUP}')

    existing = json.loads(FACE_MAP.read_text(encoding='utf-8'))
    palette = json.loads(PALETTE_FACE_MAP.read_text(encoding='utf-8'))

    added = []
    missing = []
    for char, palette_faces in palette.items():
        if char not in existing:
            print(f'WARN: palette に {char!r} があるが existing に無い。skip')
            continue
        # neutral の値を Other/Back1 参考に使う
        neutral_parts = existing[char].get('neutral', {})
        existing_labels = set(existing[char].keys())
        for face_label, parts in palette_faces.items():
            if face_label in existing_labels:
                continue  # 既存を保持
            new_parts = {}
            for part_key, palette_path in parts.items():
                new_parts[part_key] = convert_path(palette_path)
            # Other / Back1 を neutral から継承 (palette に無いパーツキー)
            for extra_key in ('Other', 'Back1'):
                if extra_key not in new_parts and extra_key in neutral_parts:
                    new_parts[extra_key] = neutral_parts[extra_key]
            # 実在チェック
            for part_key, path in new_parts.items():
                if not verify(path):
                    missing.append((char, face_label, part_key, path))
            existing[char][face_label] = new_parts
            added.append((char, face_label, list(new_parts.keys())))

    # 書き戻し
    FACE_MAP.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'\n=== ADDED ({len(added)}) ===')
    for char, fl, keys in added:
        print(f'  {char} / {fl}: {keys}')

    print(f'\n=== MISSING ({len(missing)}) ===')
    for char, fl, pk, pt in missing:
        print(f'  {char} / {fl} / {pk}: {pt}')

    return 0 if not missing else 2


if __name__ == '__main__':
    sys.exit(main())
