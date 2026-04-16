"""haitatsuin ymmp の layer 構造と CharacterName / TachieFaceParameter を調査."""
import json
import pathlib
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BS = chr(92)

def main():
    data = json.load(open('samples/characterAnimSample/haitatsuin_2026-04-12.ymmp', encoding='utf-8-sig'))
    items = data['Timelines'][0]['Items']

    cn = Counter()
    parts_by_cn = {}
    for it in items:
        t = it.get('$type', '')
        if 'VoiceItem' in t:
            name = it.get('CharacterName', '?')
            cn[name] += 1
            if name not in parts_by_cn:
                tfp = it.get('TachieFaceParameter', {})
                parts_by_cn[name] = tfp

    print('=== CharacterName 分布 (VoiceItem) ===')
    for n, c in cn.most_common():
        print(f'  {n!r}: {c}')

    print()
    print('=== TachieFaceParameter の詳細 (キャラごと 1 件) ===')
    base = pathlib.Path('samples/characterAnimSample')
    for name, tfp in parts_by_cn.items():
        print(f'--- CharacterName: {name!r} ---')
        for k, v in tfp.items():
            if isinstance(v, str) and ('.png' in v or BS in v):
                rel = v.replace(BS, '/')
                p = base / rel if not rel.startswith('C:') else pathlib.Path(rel)
                mark = 'OK' if p.exists() else 'MISS'
                print(f'  {k}: {v!r}  [{mark}]')
            elif isinstance(v, str) and v == '':
                print(f'  {k}: (empty string)')
            elif not isinstance(v, dict):
                print(f'  {k}: {v!r}')

    print()
    print('=== TachieItem (レイヤー別・全フィールド) ===')
    for it in items:
        t = it.get('$type', '')
        if 'TachieItem' in t:
            name = it.get('CharacterName', '?')
            print(f'  layer={it.get("Layer")} name={name!r} frame={it.get("Frame")} length={it.get("Length")} muted={it.get("IsMuted")}')
            for k, v in it.items():
                if k in ('$type', 'CharacterName', 'Layer', 'Frame', 'Length', 'IsMuted'):
                    continue
                if isinstance(v, dict):
                    print(f'    {k}: <dict {len(v)}キー>')
                    for k2, v2 in v.items():
                        s = json.dumps(v2, ensure_ascii=False) if isinstance(v2, (dict, list)) else repr(v2)
                        print(f'      {k2}: {s[:180]}')
                else:
                    s = json.dumps(v, ensure_ascii=False) if isinstance(v, list) else repr(v)
                    print(f'    {k}: {s[:200]}')

    print()
    print('=== VoiceItem [2] 全フィールド (文字列系だけ、フィルターなし) ===')
    for i, it in enumerate(items):
        t = it.get('$type', '')
        if 'VoiceItem' in t:
            for k, v in it.items():
                if isinstance(v, dict):
                    continue
                s = json.dumps(v, ensure_ascii=False) if isinstance(v, list) else repr(v)
                print(f'  {k}: {s[:180]}')
            print('  --- TachieFaceParameter 全キー (値省略なし) ---')
            tfp = it.get('TachieFaceParameter', {}) or {}
            for k, v in tfp.items():
                s = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else repr(v)
                print(f'    {k}: {s[:200]}')
            break

if __name__ == '__main__':
    main()
