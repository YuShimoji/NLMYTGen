"""元 ymmp と user GUI 編集後 ymmp の VoiceItem を比較し、追加/変更フィールドを特定."""
import json
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ORIG = 'samples/characterAnimSample/haitatsuin_2026-04-12.ymmp'
EDITED = 'samples/_probe/b2/haitatsuin_1utt_preset_2026-04-17.ymmp'


def load(path):
    with open(path, encoding='utf-8-sig') as f:
        return json.load(f)


def _json(v):
    return json.dumps(v, ensure_ascii=False)


def walk_diff(a, b, path=''):
    """辞書/リストを再帰比較して差分箇所を yield."""
    if type(a) is not type(b):
        yield (path, 'TYPE_CHANGE', a, b)
        return
    if isinstance(a, dict):
        akeys = set(a.keys())
        bkeys = set(b.keys())
        for k in akeys - bkeys:
            yield (f'{path}.{k}', 'REMOVED', a[k], None)
        for k in bkeys - akeys:
            yield (f'{path}.{k}', 'ADDED', None, b[k])
        for k in akeys & bkeys:
            yield from walk_diff(a[k], b[k], f'{path}.{k}')
    elif isinstance(a, list):
        if len(a) != len(b):
            yield (path, 'LEN_CHANGE', len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk_diff(x, y, f'{path}[{i}]')
    else:
        if a != b:
            yield (path, 'VALUE_CHANGE', a, b)


def main():
    a = load(ORIG)
    b = load(EDITED)

    print('=== ROOT レベル diff (全 ymmp) ===')
    total = 0
    seen_paths = {}
    for path, kind, av, bv in walk_diff(a, b):
        total += 1
        # Items[i] のアイテム単位ではまとめて集計
        key = path.split('[')[0] if '[' in path else path
        seen_paths.setdefault(key, []).append((path, kind, av, bv))
    print(f'total diff entries: {total}')
    print(f'unique top paths: {len(seen_paths)}')
    for key, entries in list(seen_paths.items())[:30]:
        print(f'  {key} : {len(entries)} entries')

    print()
    print('=== 最初の 60 個の差分 (Items 以外を優先) ===')
    shown = 0
    for path, kind, av, bv in walk_diff(a, b):
        if shown >= 60:
            break
        # Items 内差分は件数多いので別枠
        if '.Items[' in path:
            continue
        shown += 1
        print(f'  {kind:14s} {path}')
        if kind in ('ADDED', 'VALUE_CHANGE'):
            print(f'    new: {_json(bv)[:220]}')
        if kind in ('REMOVED', 'VALUE_CHANGE'):
            print(f'    old: {_json(av)[:220]}')

    print()
    print('=== Items 内差分サンプル (最大 30 件) ===')
    shown = 0
    for path, kind, av, bv in walk_diff(a, b):
        if shown >= 30:
            break
        if '.Items[' not in path:
            continue
        shown += 1
        print(f'  {kind:14s} {path}')
        if kind in ('ADDED', 'VALUE_CHANGE'):
            print(f'    new: {_json(bv)[:220]}')
        if kind in ('REMOVED', 'VALUE_CHANGE'):
            print(f'    old: {_json(av)[:220]}')


if __name__ == '__main__':
    main()
