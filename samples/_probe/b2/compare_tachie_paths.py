"""TachieItem (layer 5/6) と VoiceItem の Tachie 系パスを完全一致検査。"""
import json
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PART_KEYS = ['Eyebrow', 'Eye', 'Mouth', 'Hair', 'Complexion',
             'Body', 'Back1', 'Back2', 'Back3', 'Etc1', 'Etc2', 'Etc3']

def main():
    data = json.load(open('samples/characterAnimSample/haitatsuin_2026-04-12.ymmp', encoding='utf-8-sig'))
    items = data['Timelines'][0]['Items']

    ti_paths_by_char = {}
    for it in items:
        if 'TachieItem' in it.get('$type', ''):
            name = it.get('CharacterName', '?')
            tip = it.get('TachieItemParameter', {}) or {}
            ti_paths_by_char[name] = {k: tip.get(k) for k in PART_KEYS}

    # 全 VoiceItem の各パーツ値を集計
    vi_paths_by_char = {n: {k: Counter() for k in PART_KEYS} for n in ti_paths_by_char}
    for it in items:
        if 'VoiceItem' in it.get('$type', ''):
            name = it.get('CharacterName', '?')
            if name not in vi_paths_by_char:
                continue
            tfp = it.get('TachieFaceParameter', {}) or {}
            for k in PART_KEYS:
                vi_paths_by_char[name][k][tfp.get(k)] += 1

    print('=== TachieItem vs VoiceItem パス比較 ===')
    for name, ti_parts in ti_paths_by_char.items():
        print(f'--- {name!r} ---')
        for k in PART_KEYS:
            ti_val = ti_parts[k]
            vi_counter = vi_paths_by_char[name][k]
            most = vi_counter.most_common(1)
            vi_val = most[0][0] if most else None
            vi_n = most[0][1] if most else 0
            match = '==' if ti_val == vi_val else '!='
            print(f'  {k}: TI={ti_val!r} {match} VI[top]={vi_val!r} (n={vi_n})')
            if len(vi_counter) > 1:
                print(f'    VI variants: {dict(vi_counter)}')
            if ti_val is not None and vi_val is not None and ti_val != vi_val:
                # バイト単位で比較
                print(f'    bytes TI: {ti_val.encode("utf-8")}')
                print(f'    bytes VI: {vi_val.encode("utf-8")}')

if __name__ == '__main__':
    main()
