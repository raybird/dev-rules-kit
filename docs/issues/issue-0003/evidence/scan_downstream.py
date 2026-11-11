#!/usr/bin/env python3
"""唯讀統計記帳章節整段凍結與表格判定對下游 README 的影響。

用法：python3 scan_downstream.py <README 路徑清單檔>

清單每行一個 README 路徑；不存在的路徑略過，內容相同的檔案只算一次。分類方式：
- 同段落凍結的行：analyse() 回傳的 'paragraph' 項目，也就是因為與凍結內容同一段落而凍結的記帳行。
  同一記帳章節裡到下一個 'end' 為止算同一段；段裡有一行是 `---` 時算檔尾 metadata 段落。
- 含凍結列的表格：'table' 項目逐列記一次，以（檔案、章節、表頭）去重後算張數。
- 不合範本形狀的表格：記帳章節裡以 `|` 開頭、下一行像分隔列（以 `|` 開頭，只含 `|`、`-`、`:`、空白且有 `-`），
  starts_table() 卻不承認的表頭，照段落處理；其中表頭所在段落含凍結內容的另計。
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location('verify', ROOT / 'skills/review/scripts/verify-artifact.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)
SECTIONS = ('Timeline', '待確認事項', 'Gate 豁免紀錄', '現況')
LOOSE_DELIMITER = re.compile(r'^\|[|: \t-]*-[|: \t-]*$')


def main():
    seen, missing = set(), 0
    footer = other = paragraphs = 0
    other_files, rows, tables, odd, odd_frozen = set(), 0, set(), [], 0
    for name in (line.strip() for line in open(sys.argv[1]) if line.strip()):
        path = Path(name)
        if not path.exists():
            missing += 1
            continue
        text = path.read_text(errors='replace')
        if text in seen:
            continue
        seen.add(text)
        frozen = verify.analyse(text, SECTIONS)[0]
        group, frozen_lines = [], {entry[2] for entry in frozen if entry[1] == 'paragraph'}
        for entry in frozen + [(None, 'end', None)]:
            if entry[1] == 'paragraph':
                group.append(entry[2])
                continue
            if group and (entry[1] in ('end', 'table') or entry[0] not in SECTIONS):
                if any(line.strip() == '---' for line in group):
                    footer += len(group)
                else:
                    other += len(group)
                    paragraphs += 1
                    other_files.add(name)
                group = []
            if entry[1] == 'table':
                rows += 1
                tables.add((name, entry[0], entry[2]))
        lines = verify.LINE_END.split(text)
        section = None
        for index, line in enumerate(lines[:-1]):
            heading = verify.HEADING.match(line)
            if heading:
                section = heading.group(1)
            elif section in SECTIONS and line.startswith('|') and LOOSE_DELIMITER.match(lines[index + 1]) \
                    and not verify.starts_table(line, lines[index + 1]):
                odd.append((name, section, line))
                odd_frozen += line in frozen_lines
    print(f'略過不存在的路徑 {missing} 個；不重複的 README {len(seen)} 份')
    print(f'同段落凍結的行：檔尾 metadata 段落 {footer} 行；其他 {len(other_files)} 份 {paragraphs} 段 {other} 行')
    print(f'含凍結列的表格：{len({t[0] for t in tables})} 份 {len(tables)} 張，凍結列 {rows} 列')
    print(f'不合範本形狀、照段落處理的表格：{len({o[0] for o in odd})} 份 {len(odd)} 張，其中 {odd_frozen} 張所在段落含凍結內容')


if __name__ == '__main__':
    main()
