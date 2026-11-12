"""唯讀統計：issue README 的 **狀態** 值與待確認事項狀態欄的值。參數：README 路徑清單檔。"""
import re, sys, hashlib, collections
from pathlib import Path
paths = [Path(l.strip()) for l in open(sys.argv[1]) if l.strip()]
seen, st, tbd, tbdfiles = set(), collections.Counter(), collections.Counter(), collections.defaultdict(set)
n = 0
for p in paths:
    if not p.is_file(): continue
    t = p.read_text(errors='replace'); h = hashlib.sha1(t.encode()).hexdigest()
    if h in seen: continue
    seen.add(h); n += 1
    m = re.findall(r'^\*\*狀態\*\*[:：]\s*(.+?)\s*\\?\s*$', t, re.M)
    if m: st[m[-1]] += 1
    else: st['(無狀態欄)'] += 1
    sec = re.search(r'^## 待確認事項\s*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
    if not sec: continue
    rows = [r for r in sec.group(1).splitlines() if r.startswith('|')]
    if len(rows) < 3: continue
    head = [c.strip() for c in rows[0].strip('|').split('|')]
    if '狀態' not in head: continue
    i = head.index('狀態')
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip('|').split('|')]
        if len(cells) <= i: continue
        v = cells[i]
        key = next((k for k in ('待確認', '已解決', '不影響本次交付') if v == k or v.startswith(k + '：') or v.startswith(k + ':') or v.startswith(k + '（')), None)
        key = key or ('其他：' + v[:30])
        tbd[key] += 1; tbdfiles[key].add(h)
print(f'不重複 README {n} 份')
print('## **狀態** 值（前 25）')
for k, v in st.most_common(25): print(f'{v:5d}  {k[:60]}')
print(f'（共 {len(st)} 種）')
std = sum(v for k, v in tbd.items() if not k.startswith('其他'))
oth = {k: v for k, v in tbd.items() if k.startswith('其他')}
print('## 待確認事項狀態欄')
for k in ('待確認', '已解決', '不影響本次交付'): print(f'{tbd[k]:5d} 列 {len(tbdfiles[k]):4d} 份  {k}')
print(f'規定以外：{sum(oth.values())} 列 {len(set().union(*[tbdfiles[k] for k in oth]) if oth else set())} 份，{len(oth)} 種；前 30：')
for k, v in sorted(oth.items(), key=lambda x: -x[1])[:30]: print(f'{v:5d}  {k}')
