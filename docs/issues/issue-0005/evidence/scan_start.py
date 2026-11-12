#!/usr/bin/env python3
"""唯讀統計：下游 README 記帳章節裡，含凍結內容的段落前接的是什麼。

用法：python3 scan_start.py <README 路徑清單檔>

清單每行一個 README 路徑，與 issue #3 的 scan_downstream.py 用同一份；不存在的路徑略過，內容相同的檔案只算一次。
前接「表格列」的段落，在 GFM 渲染成表格的一列；這些文件之後在該處補空行，檢查器會判需重審。
"""
import collections
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location('verify', ROOT / 'skills/review/scripts/verify-artifact.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)
SECTIONS = ('Timeline', '待確認事項', 'Gate 豁免紀錄', '現況')


def main():
    seen, missing, starts, files = set(), 0, collections.Counter(), collections.defaultdict(set)
    for name in (line.strip() for line in open(sys.argv[1]) if line.strip()):
        path = Path(name)
        if not path.exists():
            missing += 1
            continue
        text = path.read_text(errors='replace')
        if text in seen:
            continue
        seen.add(text)
        for entry in verify.analyse(text, SECTIONS)[0]:
            if entry[1] == 'start':
                starts[entry[2]] += 1
                files[entry[2]].add(name)
    print(f'略過不存在的路徑 {missing} 個；不重複的 README {len(seen)} 份')
    for kind, count in starts.most_common():
        print(f'含凍結內容的段落前接「{kind}」：{len(files[kind])} 份 {count} 段')


if __name__ == '__main__':
    main()
