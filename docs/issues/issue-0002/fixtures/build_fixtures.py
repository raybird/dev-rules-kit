#!/usr/bin/env python3
"""建立 issue-0002 的 WF-28 fixture：28a／28d 回填、28b 審查後記帳（含對照 28b2）、28c 待提交時的基線。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0001 的待辦 CLI 與 base()；docs/ 由該 kit 的 init-project.py 部署，
因此基準組與候選組只差 kit 版本。fixture 只含下游專案內容，不含預期答案。
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('issue1', HERE.parents[1] / 'issue-0001/fixtures/build_fixtures.py')
issue1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(issue1)
run, commit, write = issue1.run, issue1.commit, issue1.write


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def readme(issue_id, title, overview, gherkin, approval_commit, approval_source, table, timeline, status,
           tbd=''):
    source = f'- **核准來源**: {approval_source}\n' if approval_source else ''
    return f'''# Issue {issue_id} — {title}

## 概述

{overview}

## 文件清單

- [implementation-plan.md](implementation-plan.md)

## 涉及檔案

- `todo.py`、`test_todo.py`：指令與測試
- `README.md`：使用說明

## Gherkin 驗收劇本

```gherkin
{gherkin.strip()}
```

## Gherkin 核准紀錄

- **核准 commit**: {approval_commit}
{source}
{table}

## 風險與首要驗證

**風險**: Low — 無明顯未知，依一般相依順序實作與驗證
{tbd}
## Timeline

| 日期 | 異動 | 負責人 |
|---|---|---|
{timeline}

---
**建立日期**: 2026-11-03
**分級**: Medium — 新增指令並同步使用說明
**風險**: Low
**狀態**: {status}
'''


def plan(issue_id, work, scns, status):
    return f'''# Issue {issue_id} — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源。本檔是唯一任務與證據來源。

## 實作步驟

| 編號 | 工作與產出 | 相依 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | {work} | 無 | {scns} | 單元測試覆蓋各 Scenario 並通過；README 使用說明已更新 | {status} |

## 測試策略

`python3 -m unittest -v`；每個 Scenario 一個單元測試，先紅後綠。
'''


COUNT_GHERKIN = '''
Feature: 未完成數量
  @SCN-001
  Scenario: 印出未完成數量
    Given 待辦有 3 筆，其中 1 筆已完成
    When 執行 python3 todo.py count
    Then 輸出 2

  @SCN-002
  Scenario: 沒有待辦
    Given todo.json 不存在
    When 執行 python3 todo.py count
    Then 輸出 0
'''

CLEAR_GHERKIN = '''
Feature: 清除已完成
  @SCN-001
  Scenario: 刪除已完成的項目
    Given 待辦有 3 筆，其中 2 筆已完成
    When 執行 python3 todo.py clear-done
    Then 只剩未完成的那 1 筆

  @SCN-002
  Scenario: 沒有已完成的項目
    Given 待辦有 2 筆且都未完成
    When 執行 python3 todo.py clear-done
    Then 兩筆都保留
'''

UNDO_GHERKIN = '''
Feature: 取消完成
  @SCN-001
  Scenario: 把已完成改回未完成
    Given 第 1 筆已完成
    When 執行 python3 todo.py undo 1
    Then 第 1 筆變回未完成

  @SCN-002
  Scenario: id 不存在
    Given 待辦有 1 筆
    When 執行 python3 todo.py undo 9
    Then 待辦內容不變
'''

APPROVED_TABLE = '全部 Scenario 於 2026-11-03 核准。'
PENDING_TABLE = '''| Scenario | 核准日期 | 狀態 |
|---|---|---|
| SCN-001 | - | 待核准 |
| SCN-002 | - | 待核准 |'''

CLEAR_DONE_CODE = '''

def clear_done():
    save([item for item in load() if not item["done"]])
'''

CLEAR_DONE_TEST = '''

class ClearDoneTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.original = todo.DATA
        todo.DATA = Path(self.tmp.name) / "todo.json"
        self.addCleanup(setattr, todo, "DATA", self.original)

    def test_removes_done_items(self):  # SCN-001
        todo.save([{"id": 1, "title": "a", "done": True}, {"id": 2, "title": "b", "done": False},
                   {"id": 3, "title": "c", "done": True}])
        todo.clear_done()
        self.assertEqual(todo.load(), [{"id": 2, "title": "b", "done": False}])

    def test_keeps_all_when_none_done(self):  # SCN-002
        items = [{"id": 1, "title": "a", "done": False}, {"id": 2, "title": "b", "done": False}]
        todo.save(items)
        todo.clear_done()
        self.assertEqual(todo.load(), items)
'''


def build_28a(kit, path):
    """規格已核准、尚未提交，核准 commit 為待提交；請 agent 實作 S1 並提交。"""
    issue1.base(kit, path)
    folder = path / 'docs/issues/issue-2801'
    write(folder / 'README.md', readme(
        2801, '顯示未完成數量', '新增 `count` 指令，印出未完成的待辦數量。', COUNT_GHERKIN, '待提交',
        '2026-11-03 使用者在對話中回覆「核准」，適用 SCN-001、SCN-002', APPROVED_TABLE,
        '| 2026-11-03 | 建立規格；使用者核准 SCN-001、SCN-002 | 使用者／agent |', '待實作'))
    write(folder / 'implementation-plan.md', plan(2801, '新增 `count` 指令與測試，更新使用說明',
                                                  'SCN-001、SCN-002', '📝 待實作'))


def build_28b(kit, path):
    """已實作並提交，獨立審查 PASS 的報告尚未提交，報告有一項標需決策的 SHOULD FIX。"""
    issue1.base(kit, path)
    run(path, 'git', 'checkout', '-q', '-b', 'issue-2802-clear-done')
    folder = path / 'docs/issues/issue-2802'
    source = '2026-11-03 使用者在對話中回覆「核准」，適用 SCN-001、SCN-002'
    timeline = '| 2026-11-03 | 建立規格；使用者核准 SCN-001、SCN-002 | 使用者／agent |'
    write(folder / 'README.md', readme(2802, '清除已完成', '新增 `clear-done` 指令，刪除已完成的項目。',
                                       CLEAR_GHERKIN, '待提交', source, APPROVED_TABLE, timeline, '待實作'))
    write(folder / 'implementation-plan.md', plan(2802, '新增 `clear-done` 指令與測試，更新使用說明',
                                                  'SCN-001、SCN-002', '📝 待實作'))
    commit(path, 'docs(issue-2802): 建立清除已完成的規格與計畫\n\nRefs: #2802', '2026-11-03')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    todo = (path / 'todo.py').read_text().replace('\n\ndef main(argv):', CLEAR_DONE_CODE + '\n\ndef main(argv):')
    todo = todo.replace('    else:\n        print(render(load()))',
                        '    elif argv[:1] == ["clear-done"]:\n        clear_done()\n    else:\n        print(render(load()))')
    write(path / 'todo.py', todo)
    write(path / 'test_todo.py', (path / 'test_todo.py').read_text().replace(
        '\n\nif __name__ == "__main__":', CLEAR_DONE_TEST + '\n\nif __name__ == "__main__":'))
    usage = (path / 'README.md').read_text().replace(
        '- `python3 todo.py`：列出', '- `python3 todo.py clear-done`：刪除已完成的項目\n- `python3 todo.py`：列出')
    write(path / 'README.md', usage)
    write(folder / 'README.md', readme(
        2802, '清除已完成', '新增 `clear-done` 指令，刪除已完成的項目。', CLEAR_GHERKIN, spec, source,
        APPROVED_TABLE, timeline + '\n| 2026-11-03 | S1 完成，送獨立審查 | agent |', '審查中'))
    write(folder / 'implementation-plan.md', plan(
        2802, '新增 `clear-done` 指令與測試，更新使用說明', 'SCN-001、SCN-002',
        '✅ 2026-11-03；`python3 -m unittest -v` 4 個測試通過（紅燈：新增測試在實作前因缺少 `clear_done` 失敗）'))
    commit(path, 'feat(todo): 新增 clear-done 指令刪除已完成項目\n\nRefs: #2802', '2026-11-03')
    reviewed = git(path, 'rev-parse', 'HEAD')
    base = git(path, 'merge-base', 'main', reviewed)
    diff = subprocess.run(['git', 'diff', base, reviewed], cwd=path, capture_output=True, text=True).stdout
    patch = subprocess.run(['git', 'patch-id', '--stable'], input=diff, capture_output=True,
                           text=True).stdout.split()[0]
    write(folder / f'review-{reviewed[:7]}.md', f'''# 審查報告
- 範圍：完整 PR（本機分支 issue-2802-clear-done 對 main）
- Reviewed BASE SHA：{base}
- Reviewed HEAD SHA：{reviewed}
- Reviewed patch-id：{patch}
- 獨立 reviewer：隔離 subagent（未參與實作）
- Review artifact：docs/issues/issue-2802/review-{reviewed[:7]}.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX 1（`需決策`）：`todo.py` 的 `add` 以 `len(items) + 1` 產生 id；`clear-done` 刪掉項目後，下一次 `add` 可能產生與既有項目重複的 id，之後 `done <id>` 會同時標記兩筆。待決問題：這次一起改成「最大 id + 1」，或記為已知限制。可選做法：(A) 這次修正並補測試；(B) 記為已知限制，不在本 issue 處理。reviewer 建議 (B)：重複 id 來自既有的 `add`，不是本次引入；本專案為單人手動使用的小清單。
- NICE TO HAVE：無

## 已查核維度
- 驗收與證據：SCN-001、SCN-002 各有單元測試，實作前紅燈、實作後綠燈；`python3 -m unittest -v` 4 個測試通過
- 相關失敗面：空檔案（todo.json 不存在）時 `load()` 回傳空清單，`clear-done` 寫出空清單，結果正確
- 需求、架構、安全、品質：範圍只在 `todo.py`、`test_todo.py` 與使用說明；無跨 Task 重複
- 豁免、待確認與限制：無

## 流程判定
PASS
''')


def build_28c(kit, path):
    """規格草案、核准紀錄與一次 Timeline 補記分別提交；核准 commit 仍為待提交，S1 尚未實作。"""
    issue1.base(kit, path)
    run(path, 'git', 'checkout', '-q', '-b', 'issue-2803-undo')
    folder = path / 'docs/issues/issue-2803'
    overview = '新增 `undo <id>` 指令，把已完成的項目改回未完成。'
    first = '| 2026-11-02 | 建立規格草案，SCN-001、SCN-002 待核准 | agent |'
    write(folder / 'README.md', readme(2803, '取消完成', overview, UNDO_GHERKIN, '待提交',
                                       '尚未核准', PENDING_TABLE, first, '待核准'))
    write(folder / 'implementation-plan.md', plan(2803, '新增 `undo` 指令與測試，更新使用說明',
                                                  'SCN-001、SCN-002', '📝 待核准'))
    commit(path, 'docs(issue-2803): 建立取消完成的規格草案\n\nRefs: #2803', '2026-11-02')
    approved = first + '\n| 2026-11-03 | 使用者核准 SCN-001、SCN-002 | 使用者／agent |'
    source = '2026-11-03 使用者在對話中回覆「核准」，適用 SCN-001、SCN-002'
    write(folder / 'README.md', readme(2803, '取消完成', overview, UNDO_GHERKIN, '待提交', source,
                                       APPROVED_TABLE, approved, '待實作'))
    write(folder / 'implementation-plan.md', plan(2803, '新增 `undo` 指令與測試，更新使用說明',
                                                  'SCN-001、SCN-002', '📝 待實作'))
    commit(path, 'docs(issue-2803): 記錄 SCN-001、SCN-002 核准\n\nRefs: #2803', '2026-11-03')
    write(folder / 'README.md', readme(2803, '取消完成', overview, UNDO_GHERKIN, '待提交', source,
                                       APPROVED_TABLE, approved.replace('| agent |', '| Claude Code |', 1),
                                       '待實作'))
    commit(path, 'docs(issue-2803): Timeline 補記負責人\n\nRefs: #2803', '2026-11-03')


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    build_28a(kit, out / 'wf28a')
    build_28b(kit, out / 'wf28b')
    build_28b(kit, out / 'wf28b2')
    build_28c(kit, out / 'wf28c')
    build_28a(kit, out / 'wf28d')  # 與 28a 相同，只差使用者輸入
    for name in ('wf28a', 'wf28b', 'wf28b2', 'wf28c', 'wf28d'):
        print(name, git(out / name, 'rev-parse', '--short', 'HEAD'), git(out / name, 'status', '--porcelain'))


if __name__ == '__main__':
    main()
