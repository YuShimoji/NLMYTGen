"""face_map_bundles/haitatsuin.json を samples/Mat/ 基準に書き換える.

ymmp 相対 (samples/characterAnimSample/ から samples/Mat/) で ..\\Mat\\... を出力する.
apply-production が face_map の値をそのまま VoiceItem.TachieFaceParameter に書き込む仕様なので,
face_map の出力値は VoiceItem に埋まる文字列と同じフォーマットでなければならない.
"""
import json
import pathlib
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

REPO = pathlib.Path('.').resolve()
FACE_MAP = REPO / 'samples' / 'face_map_bundles' / 'haitatsuin.json'
BACKUP = REPO / 'samples' / '_probe' / 'b2' / 'haitatsuin_face_map_backup.json'
YMMP_BASE = REPO / 'samples' / 'characterAnimSample'  # ymmp 相対解決の基点
MAT_ROOT = REPO / 'samples' / 'Mat'


# 旧パス → 新パス の書き換え規則 (prefix 置換)
REWRITE_RULES = [
    # haitatsuin/まりさ/... と haitatsuin/れいむ/... は 新まりさ/新れいむ へマージ
    (r'^migrated_tachie\\haitatsuin\\まりさ\\', r'..\\Mat\\新まりさ\\'),
    (r'^migrated_tachie\\haitatsuin\\れいむ\\', r'..\\Mat\\新れいむ\\'),
    # 単純置換
    (r'^migrated_tachie\\', r'..\\Mat\\'),
]

BS = chr(92)


def rewrite_path(p: str) -> str:
    if not isinstance(p, str):
        return p
    for pat, repl in REWRITE_RULES:
        new = re.sub(pat, repl, p)
        if new != p:
            return new
    return p


def verify_exists(rel_path: str) -> bool:
    """ymmp 相対パスを samples/characterAnimSample/ 基準で解決し実在チェック."""
    rel = rel_path.replace(BS, '/')
    p = (YMMP_BASE / rel).resolve()
    return p.exists()


def main():
    if not FACE_MAP.exists():
        print(f'ERROR: {FACE_MAP} が存在しません')
        return 1

    # backup
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FACE_MAP, BACKUP)
    print(f'backup: {BACKUP}')

    data = json.loads(FACE_MAP.read_text(encoding='utf-8'))

    changed = 0
    missing = []
    rewritten = {}
    for char, faces in data.items():
        rewritten[char] = {}
        for face, parts in faces.items():
            rewritten[char][face] = {}
            for part, path in parts.items():
                new_path = rewrite_path(path)
                rewritten[char][face][part] = new_path
                if new_path != path:
                    changed += 1
                if not verify_exists(new_path):
                    missing.append((char, face, part, new_path))

    # 書き戻し
    FACE_MAP.write_text(
        json.dumps(rewritten, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'changed paths: {changed}')
    print(f'total missing files after rewrite: {len(missing)}')
    for m in missing[:20]:
        print(f'  MISS {m[0]} / {m[1]} / {m[2]}: {m[3]}')
    if len(missing) > 20:
        print(f'  ... +{len(missing) - 20} more')
    return 0 if not missing else 2


if __name__ == '__main__':
    sys.exit(main())
