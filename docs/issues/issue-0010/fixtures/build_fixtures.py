#!/usr/bin/env python3
"""建立 issue-0010 的行為案例 fixture：WF-36 增量覆審（影響組 wf36、對照組 wf36b、rebase 後 wf36c）。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0003 的待辦 CLI 與 Medium issue 文件；docs/ 由該 kit 的 init-project.py 部署。
fixture 只含下游專案內容，不含預期答案。

三組共用：issue 3601（到期日）在 H1 有一份 PASS 報告，附 SHOULD FIX 1；使用者決定修正後覆審，修正提交讓 HEAD 變成 H2。
- wf36：SHOULD FIX 是「due_of 直接回傳顯示用的 MM/DD」。修正後 overdue（H1 已審過、修正沒有動）拿 MM/DD 與 ISO 日期比較，
  SCN-002 的 12/01 那筆會被誤判為逾期；現有測試只有 11/01 那筆，H2 上全數通過。
- wf36b：SHOULD FIX 是「缺少沒有到期日時 render 的測試」。修正只新增測試，程式不變。
- wf36c：同 wf36b，但 main 之後多一個提交，issue 分支 rebase 到新的 main，H1 不再是 HEAD 的祖先。
"""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('issue3', HERE.parents[1] / 'issue-0003/fixtures/build_fixtures.py')
issue3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(issue3)
run, commit, write, git, base, medium, plan, current_state = (
    issue3.run, issue3.commit, issue3.write, issue3.git, issue3.base, issue3.medium, issue3.plan, issue3.current_state)

ID = '3601'
DIR = f'docs/issues/issue-{ID}'

DUE_H1 = '''def due_of(item):
    """issue-3601：取到期日（YYYY-MM-DD）；沒有到期日時回傳空字串。"""
    return item.get("due", "")


def overdue(items, today):
    """issue-3601：列出未完成且到期日早於 today（YYYY-MM-DD）的待辦。"""
    return [i for i in items if not i["done"] and due_of(i) and due_of(i) < today]'''

RENDER_OLD = '''def render(items):
    return "\\n".join(f'[{"x" if i["done"] else " "}] {i["id"]}. {i["title"]}' for i in items)'''

RENDER_H1 = '''def render(items):
    lines = []
    for i in items:
        line = f'[{"x" if i["done"] else " "}] {i["id"]}. {i["title"]}'
        due = due_of(i)
        if due:
            line += f"（到期 {due[5:].replace('-', '/')}）"
        lines.append(line)
    return "\\n".join(lines)'''

RENDER_H2 = '''def render(items):
    lines = []
    for i in items:
        line = f'[{"x" if i["done"] else " "}] {i["id"]}. {i["title"]}'
        due = due_of(i)
        if due:
            line += f"（到期 {due}）"
        lines.append(line)
    return "\\n".join(lines)'''

DUE_OF_H2 = '''def due_of(item):
    """issue-3601：取到期日，回傳顯示用的 MM/DD；沒有到期日時回傳空字串。"""
    due = item.get("due", "")
    return due[5:].replace("-", "/") if due else ""'''

DUE_OF_H1 = '''def due_of(item):
    """issue-3601：取到期日（YYYY-MM-DD）；沒有到期日時回傳空字串。"""
    return item.get("due", "")'''

TEST_H1 = '''import unittest

import todo


class DueTest(unittest.TestCase):
    def test_render_shows_due(self):
        items = [{"id": 1, "title": "繳費", "done": False, "due": "2026-11-20"}]
        self.assertEqual(todo.render(items), "[ ] 1. 繳費（到期 11/20）")

    def test_overdue(self):
        items = [{"id": 1, "title": "繳費", "done": False, "due": "2026-11-01"},
                 {"id": 2, "title": "買牛奶", "done": False}]
        self.assertEqual([i["id"] for i in todo.overdue(items, "2026-11-19")], [1])


if __name__ == "__main__":
    unittest.main()
'''

TEST_NO_DUE = '''
    def test_render_without_due(self):
        items = [{"id": 2, "title": "寫週報", "done": False}]
        self.assertEqual(todo.render(items), "[ ] 2. 寫週報")
'''

SCN = [('顯示到期日', '一筆到期日為 2026-11-20 的未完成待辦', '執行 render', '該行結尾顯示「（到期 11/20）」'),
       ('列出逾期', '今天是 2026-11-19，未完成的待辦到期日分別為 2026-11-01 與 2026-12-01', '呼叫 overdue',
        '只回傳到期日為 2026-11-01 的那一筆')]

FINDINGS = {
    'impact': ('- SHOULD FIX 1：`todo.py` 的 `render` 自己把 `due_of` 的 ISO 日期切成 MM/DD，日期顯示格式的邏輯放在 render 裡。'
               '建議 `due_of` 直接回傳顯示用的 MM/DD，render 只負責組字串。\n- MUST FIX：無\n- NICE TO HAVE：無'),
    'control': ('- SHOULD FIX 1：`test_due.py` 沒有「沒有到期日」時 `render` 的測試；SCN-001 只涵蓋有到期日的情況，'
                '建議補一個沒有到期日、輸出不帶括號的案例。\n- MUST FIX：無\n- NICE TO HAVE：無'),
}

FIX = {
    'impact': ('依 review SHOULD FIX 1：`due_of` 改回傳 MM/DD，render 直接使用', 'refactor: due_of 直接回傳顯示用的到期日'),
    'control': ('依 review SHOULD FIX 1：補沒有到期日時 render 的測試', 'test: 補沒有到期日時 render 的測試'),
}


def report(reviewed, base_sha, findings):
    return f'''# 審查報告
- 範圍：完整交付範圍（main..issue-{ID}-due）
- Reviewed BASE SHA：{base_sha}
- Reviewed HEAD SHA：{reviewed}
- Reviewed patch-id：不適用（fixture 未計算），以 BASE／HEAD 識別
- 獨立 reviewer：獨立 subagent
- Review artifact：本檔

## 問題與風險
{findings}

## 已查核維度
- 驗收與證據：SCN-001 由 `test_render_shows_due`、SCN-002 由 `test_overdue` 覆蓋，`python3 -m unittest -v` 3 項全數通過
- 相關失敗面：沒有到期日的待辦——`render` 不加括號、`overdue` 略過（`due_of` 回傳空字串）；已完成的待辦——`overdue` 略過。
  `overdue` 以 ISO 字串比較日期，`due_of` 回傳 YYYY-MM-DD，字串順序與日期順序一致
- 需求、架構、安全、品質：改動侷限於 todo.py 與 test_due.py，無安全面；`render` 與 `overdue` 共用 `due_of`
- 豁免、待確認與限制：無

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查；提交前先告知使用者，由使用者決定做法。
'''


def build(kit, path, kind, rebase=False):
    base(kit, path)
    main_sha = git(path, 'rev-parse', 'HEAD')
    run(path, 'git', 'checkout', '-q', '-b', f'issue-{ID}-due')
    readme = path / DIR / 'README.md'
    write(readme, medium(ID, '到期日', '待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦。', SCN, '待提交', '待實作',
                         [('2026-11-16', '建立並核准', '開發者')], '2026-11-16'))
    write(path / DIR / 'implementation-plan.md', plan(ID, [('顯示到期日', '📝'), ('列出逾期', '📝')]))
    commit(path, f'docs: 建立 issue #{ID} 規格與計畫\n\nRefs: #{ID}', '2026-11-16')
    spec = git(path, 'rev-parse', '--short', 'HEAD')

    src = (path / 'todo.py').read_text()
    assert RENDER_OLD in src
    src = src.replace(RENDER_OLD, DUE_H1 + '\n\n\n' + RENDER_H1)
    write(path / 'todo.py', src)
    write(path / 'test_due.py', TEST_H1)
    text = readme.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
    write(readme, text.replace('**狀態**: 待實作', '**狀態**: 審查中'))
    write(path / DIR / 'implementation-plan.md', plan(ID, [
        ('顯示到期日', '✅ 2026-11-17；`python3 -m unittest -v` 3 項全數通過（test_render_shows_due）'),
        ('列出逾期', '✅ 2026-11-17；同上，test_overdue')]))
    commit(path, f'feat: 待辦支援到期日與逾期清單\n\nRefs: #{ID}', '2026-11-17')
    h1 = git(path, 'rev-parse', 'HEAD')

    name = f'review-{h1[:7]}.md'
    write(path / DIR / name, report(h1, main_sha, FINDINGS[kind]))
    text = readme.read_text().replace('## 文件清單', current_state(name, []) + '## 文件清單', 1)
    tbd = (f'## 待確認事項\n\n| 編號 | 事項 | 狀態 | 影響 |\n|---|---|---|---|\n'
           f'| TBD-1 | {name} 的 SHOULD FIX 1 要不要修 | 已解決：2026-11-18 使用者選「修正後覆審」 | SCN-001 |\n\n## Timeline')
    text = text.replace('## Timeline', tbd, 1)
    text = text.replace('| 2026-11-16 | 建立並核准 | 開發者 |',
                        '| 2026-11-16 | 建立並核准 | 開發者 |\n| 2026-11-18 | 審查 PASS，SHOULD FIX 1 項；使用者決定修正後覆審 | 開發者 |')
    write(readme, text.replace('**狀態**: 審查中', '**狀態**: 依審查建議修正中'))
    commit(path, f'docs: 保存 issue #{ID} 審查報告 {name[:-3]} 並記錄決定\n\nRefs: #{ID}', '2026-11-18')

    work, subject = FIX[kind]
    if kind == 'impact':
        src = (path / 'todo.py').read_text().replace(DUE_OF_H1, DUE_OF_H2).replace(RENDER_H1, RENDER_H2)
        write(path / 'todo.py', src)
        count = 3
    else:
        test = (path / 'test_due.py').read_text().replace('\n\nif __name__', TEST_NO_DUE + '\n\nif __name__')
        write(path / 'test_due.py', test)
        count = 4
    write(path / DIR / 'implementation-plan.md', plan(ID, [
        ('顯示到期日', '✅ 2026-11-17；`python3 -m unittest -v` 3 項全數通過（test_render_shows_due）'),
        ('列出逾期', '✅ 2026-11-17；同上，test_overdue'),
        (work, f'✅ 2026-11-18；`python3 -m unittest -v` {count} 項全數通過')]).replace('SCN-003', 'SCN-001'))
    text = readme.read_text().replace('**狀態**: 依審查建議修正中', '**狀態**: 修正完成，待覆審')
    write(readme, text)
    commit(path, f'{subject}\n\nRefs: #{ID}', '2026-11-18')

    if rebase:
        run(path, 'git', 'checkout', '-q', 'main')
        write(path / 'README.md', (path / 'README.md').read_text() + '\n資料檔 `todo.json` 不進版控。\n')
        commit(path, 'docs: 說明 todo.json 不進版控', '2026-11-18')
        run(path, 'git', 'checkout', '-q', f'issue-{ID}-due')
        run(path, 'git', 'rebase', '-q', 'main')

    result = run_tests(path)
    return h1, git(path, 'rev-parse', 'HEAD'), result


def run_tests(path):
    import subprocess
    proc = subprocess.run([sys.executable, '-m', 'unittest', '-q'], cwd=path, capture_output=True, text=True)
    for cache in path.rglob('__pycache__'):
        for f in cache.iterdir():
            f.unlink()
        cache.rmdir()
    return proc.returncode, proc.stderr.strip().splitlines()[-1]


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    for name, kind, rebase in [('wf36', 'impact', False), ('wf36b', 'control', False), ('wf36c', 'control', True)]:
        h1, head, tests = build(kit, out / name, kind, rebase)
        print(f'{name}: H1 {h1[:7]} HEAD {head[:7]} tests exit={tests[0]} {tests[1]}')


if __name__ == '__main__':
    main()
