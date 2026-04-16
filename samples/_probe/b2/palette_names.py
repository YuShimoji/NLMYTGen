import json
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

d = json.load(open('samples/palette.ymmp', encoding='utf-8-sig'))
all_items = d['Timelines'][0]['Items']
print(f'total items: {len(all_items)}')
type_c = Counter()
for it in all_items:
    t = it.get('$type', '?').split(',')[0].split('.')[-1]
    type_c[t] += 1
print(f'types: {dict(type_c)}')

# すべての CharacterName 集計
names = Counter()
for it in all_items:
    n = it.get('CharacterName')
    if n:
        names[n] += 1
print(f'names: {dict(names)}')

# TachieItem の CharacterName
print('TachieItems:')
for it in all_items:
    if 'TachieItem' in it.get('$type', ''):
        n = it.get('CharacterName', '?')
        tip = it.get('TachieItemParameter', {}) or {}
        remark = it.get('Remark', '')
        print(f'  name={n!r} remark={remark!r} body={tip.get("Body", "?")!r}')
