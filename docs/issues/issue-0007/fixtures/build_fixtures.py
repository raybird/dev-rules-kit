#!/usr/bin/env python3
"""建立 issue-0007 的行為案例 fixture：WF-34 懸置掃描遇到規定以外的待確認事項狀態。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0003 的 base（待辦 CLI，docs/ 由該 kit 的 init-project.py 部署）。
fixture 只含下游專案內容，不含預期答案。
"""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('issue3', HERE.parents[1] / 'issue-0003/fixtures/build_fixtures.py')
issue3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(issue3)
issue1 = issue3.issue1

SCAN = '\n懸置掃描：issue 目錄 `docs/issues/`；未登記掃描命令；未登記平台查詢命令；未設掃描起點。\n'
ISSUES = [
    ('3401', '匯出待辦為 CSV', '已定案（2026-11-05）：照建議，欄位用逗號分隔', '2026-11-04'),
    ('3402', '依到期日排序', '**已解決**（2026-11-06）：照建議，沒有到期日的排最後', '2026-11-05'),
    ('3403', '刪除前確認', '已解決（2026-11-07）：照建議，加 --yes 跳過確認', '2026-11-06'),
]


def build(kit, path):
    issue3.base(kit, path, extra=SCAN)
    for issue_id, title, status, created in ISSUES:
        readme = issue1.small(
            issue_id, title, '實作中',
            acs=[('AC-1', f'{title}，以單元測試驗證')],
            steps=[('⏳', f'**AC-1：{title}** — 驗證方式：`python3 -m unittest -v`')],
            tbd=[('TBD-1', '做法要照建議還是另議', status, 'AC-1')],
            timeline=[(created, '建立'), (created, '使用者核准 AC-1')],
            created=created)
        issue1.write(path / f'docs/issues/issue-{issue_id}/README.md', readme)
        issue1.commit(path, f'docs(issue-{issue_id}): 規劃{title}', created)


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
    if out.exists():
        sys.exit(f'輸出目錄已存在：{out}')
    build(kit, out / 'wf34')


if __name__ == '__main__':
    main()
