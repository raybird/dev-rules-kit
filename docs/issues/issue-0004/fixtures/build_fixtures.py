#!/usr/bin/env python3
"""issue-0004 的 WF-32 fixture：沿用 issue-0003 的 build_handover，審查報告加上 review 技能範本的 PASS 提醒。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('issue3', HERE.parents[1] / 'issue-0003/fixtures/build_fixtures.py')
issue3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(issue3)


def pass_note(kit):
    """從 kit 的 review 技能範本取出 PASS 提醒，fixture 與範本保持同一句。"""
    text = (kit / 'skills/review/SKILL.md').read_text()
    match = re.search(r'（PASS 時照抄下一行）\n(.+)\n', text)
    assert match, 'review 技能範本缺少 PASS 提醒'
    return match.group(1)


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    issue3.PASS_NOTE = pass_note(kit)
    issue3.build_handover(kit, out / 'wf32')
    print('wf32', issue3.git(out / 'wf32', 'rev-parse', '--short', 'HEAD'))


if __name__ == '__main__':
    main()
