"""唯讀統計 issue README 的 `**狀態**` 與待確認事項狀態欄（issue #7，2026-11-12）。

參數：README 路徑清單檔（每行一個路徑）。內容相同的 README 只算一次。
只輸出計數與開頭詞（最多 4 個字），不輸出下游原文。
"""
import collections
import hashlib
import re
import sys
from pathlib import Path

SPECIAL = ('等待外部驗收窗', '不修復', '已完成')
TBD = ('待確認', '已解決', '不影響本次交付')


def strip_marks(text):
    while text and not text[0].isalnum():
        text = text[1:]
    return text


seen, missing = set(), 0
status, tbd, tbd_files, prefixes = collections.Counter(), collections.Counter(), collections.defaultdict(set), collections.Counter()
kinds = set()
for line in open(sys.argv[1]):
    path = Path(line.strip())
    if not line.strip():
        continue
    if not path.is_file():
        missing += 1
        continue
    text = path.read_text(errors='replace')
    digest = hashlib.sha1(text.encode()).hexdigest()
    if digest in seen:
        continue
    seen.add(digest)
    values = re.findall(r'^\*\*狀態\*\*[:：]\s*(.+?)\s*\\?\s*$', text, re.M)
    if not values:
        status['沒有狀態欄'] += 1
    else:
        kinds.add(values[-1])
        value = strip_marks(values[-1])
        status[next((f'以 {s} 開頭' for s in SPECIAL if value.startswith(s)), '其他（自由描述）')] += 1
    section = re.search(r'^## 待確認事項[ \t]*$(.*?)(?=^## |\Z)', text, re.M | re.S)
    rows = [r.strip() for r in section.group(1).splitlines() if r.strip().startswith('|')] if section else []
    if len(rows) < 3:
        continue
    head = [c.strip() for c in rows[0].strip('|').split('|')]
    if not head[0].startswith('編號') or '狀態' not in head:
        continue
    index = head.index('狀態')
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip('|').split('|')]
        if len(cells) <= index:
            continue
        raw = cells[index]
        if raw.startswith(TBD):
            kind = 'A 以規定值開頭'
        elif strip_marks(raw).startswith(TBD):
            kind = 'B 去掉粗體、反引號或符號後以規定值開頭'
        else:
            kind = 'C 規定以外'
            prefixes[re.split(r'[（(：:\s]', strip_marks(raw), maxsplit=1)[0][:4] or '（空白或符號）'] += 1
        tbd[kind] += 1
        tbd_files[kind].add(digest)

print(f'略過不存在的路徑 {missing} 個；不重複的 README {len(seen)} 份')
print(f'`**狀態**` 共 {len(kinds)} 種寫法：')
for key, count in status.most_common():
    print(f'  {key}：{count} 份')
print('待確認事項狀態欄：')
for key in sorted(tbd):
    print(f'  {key}：{tbd[key]} 列 {len(tbd_files[key])} 份')
print('C 類開頭詞（前 12，最多 4 個字）：' + '、'.join(f'{k} {v}' for k, v in prefixes.most_common(12)))
