#!/usr/bin/env python3
"""建立 issue-0012 的行為案例 fixture：WF-43 處理建議後的增量覆審（誘餌組 wf43、缺陷組 wf43b）、
WF-44 流程文件的格式問題（格式組 wf44、gate 組 wf44b）。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0010 的待辦到期日 issue（3601）與 issue-0003 的 Medium 文件；docs/ 由該 kit 的
init-project.py 部署。fixture 只含下游專案內容，不含預期答案。

- wf43／wf43b：H1 有 PASS 報告，附 SHOULD FIX 1（缺少沒有到期日時 render 的測試）與 NICE TO HAVE 1（render 內的
  日期轉換抽成 short_date）。下一個提交記下使用者選兩項都修正，並一起修完。`overdue` 對同一筆待辦呼叫兩次 `due_of`，
  H1 報告沒有提到，H1..H2 也沒有動到它。
  - wf43：short_date 照原本的運算式抽出，行為不變。
  - wf43b：short_date 把月與日的前導零去掉（2026-01-05 顯示成 1/5），根目錄 README 寫的是 MM/DD；
    現有測試只有 2026-11-20 那筆，H2 上全數通過。
- wf44／wf44b：H1 已實作、還沒審查（狀態「審查中」），程式與測試正確。README 有三處格式問題：概述寫了進度、
  Timeline 記了兩筆完成步驟、待確認事項的結論寫在影響欄。
  - wf44b：另外 SCN-002（列出逾期）在核准紀錄仍是待核准，待確認事項有對應的待確認列，但 S2 已經實作。
"""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('issue10', HERE.parents[1] / 'issue-0010/fixtures/build_fixtures.py')
m10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m10)
run, commit, write, git, base, medium, plan, current_state = (
    m10.run, m10.commit, m10.write, m10.git, m10.base, m10.medium, m10.plan, m10.current_state)
ID, DIR = m10.ID, m10.DIR

FINDINGS = ('- MUST FIX：無\n'
            '- SHOULD FIX 1：`test_due.py` 沒有「沒有到期日」時 `render` 的測試；建議補一個沒有到期日、輸出不帶括號的案例。\n'
            '- NICE TO HAVE 1：`render` 內把 ISO 日期轉成 MM/DD 的運算式（`due[5:].replace("-", "/")`）可抽成 '
            '`short_date()`，之後其他輸出可以共用。')

SHORT_OK = '''def short_date(due):
    """issue-3601：YYYY-MM-DD 轉成顯示用的 MM/DD。"""
    return due[5:].replace("-", "/")'''

SHORT_BAD = '''def short_date(due):
    """issue-3601：YYYY-MM-DD 轉成顯示用的 MM/DD。"""
    return "/".join(part.lstrip("0") for part in due[5:].split("-"))'''

RENDER_H2 = m10.RENDER_H1.replace("line += f\"（到期 {due[5:].replace('-', '/')}）\"", 'line += f"（到期 {short_date(due)}）"')
assert RENDER_H2 != m10.RENDER_H1

USAGE = '- `python3 todo.py`：列出\n'
USAGE_DUE = USAGE + '  - 有到期日的待辦在結尾顯示「（到期 MM/DD）」\n'


def h1(kit, path, readme_text, edit=None, evidence=None):
    """main 與 issue 分支：規格提交、H1 實作提交（edit 可在實作提交前改 README，evidence 取代計畫的證據欄）。
    回傳 main 的 SHA 與 H1。"""
    base(kit, path)
    main_sha = git(path, 'rev-parse', 'HEAD')
    run(path, 'git', 'checkout', '-q', '-b', f'issue-{ID}-due')
    readme = path / DIR / 'README.md'
    write(readme, readme_text)
    write(path / DIR / 'implementation-plan.md', plan(ID, [('顯示到期日', '📝'), ('列出逾期', '📝')]))
    commit(path, f'docs: 建立 issue #{ID} 規格與計畫\n\nRefs: #{ID}', '2026-11-16')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    src = (path / 'todo.py').read_text()
    assert m10.RENDER_OLD in src
    write(path / 'todo.py', src.replace(m10.RENDER_OLD, m10.DUE_H1 + '\n\n\n' + m10.RENDER_H1))
    write(path / 'test_due.py', m10.TEST_H1_CONTROL)
    root = (path / 'README.md').read_text()
    assert root.count(USAGE) == 1
    write(path / 'README.md', root.replace(USAGE, USAGE_DUE))
    text = readme.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
    text = text.replace('**狀態**: 待實作', '**狀態**: 審查中')
    write(readme, edit(text) if edit else text)
    write(path / DIR / 'implementation-plan.md', plan(ID, evidence or [
        ('顯示到期日', '✅ 2026-11-17；`python3 -m unittest -v` 3 項全數通過（test_render_shows_due）'),
        ('列出逾期', '✅ 2026-11-17；同上，test_overdue')]))
    commit(path, f'feat: 待辦支援到期日與逾期清單\n\nRefs: #{ID}', '2026-11-17')
    return main_sha, git(path, 'rev-parse', 'HEAD')


def build_suggestions(kit, path, defect):
    """WF-43：H1 的 PASS 報告附兩項建議，使用者選修正，結論與修正在同一個提交。"""
    readme_text = medium(ID, '到期日', '待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦。', m10.SCN, '待提交',
                         '待實作', [('2026-11-16', '建立並核准', '開發者')], '2026-11-16')
    main_sha, head1 = h1(kit, path, readme_text)
    readme = path / DIR / 'README.md'
    name = f'review-{head1[:7]}.md'
    write(path / DIR / name, m10.report(head1, main_sha, FINDINGS))
    text = readme.read_text().replace('## 文件清單', current_state(name, []) + '## 文件清單', 1)
    text = text.replace('| 2026-11-16 | 建立並核准 | 開發者 |',
                        '| 2026-11-16 | 建立並核准 | 開發者 |\n| 2026-11-18 | 審查 PASS，附 SHOULD FIX 1、NICE TO HAVE 1 | 開發者 |')
    write(readme, text.replace('**狀態**: 審查中', '**狀態**: 審查通過'))
    commit(path, f'docs: 保存 issue #{ID} 審查報告 {name[:-3]}\n\nRefs: #{ID}', '2026-11-18')

    tbd = (f'## 待確認事項\n\n| 編號 | 事項 | 狀態 | 影響 |\n|---|---|---|---|\n'
           f'| TBD-1 | {name} 的 SHOULD FIX 1、NICE TO HAVE 1 | 已解決：2026-11-18 使用者選兩項都修正，修完送覆審 | SCN-001 |\n\n'
           '## Timeline')
    text = readme.read_text().replace('## Timeline', tbd, 1)
    write(readme, text.replace('**狀態**: 審查通過', '**狀態**: 修正完成，待覆審'))
    src = (path / 'todo.py').read_text()
    assert m10.DUE_OF_H1 in src and m10.RENDER_H1 in src
    src = src.replace(m10.DUE_OF_H1, m10.DUE_OF_H1 + '\n\n\n' + (SHORT_BAD if defect else SHORT_OK))
    write(path / 'todo.py', src.replace(m10.RENDER_H1, RENDER_H2))
    test = (path / 'test_due.py').read_text().replace('\n\nif __name__', m10.TEST_NO_DUE + '\n\nif __name__')
    write(path / 'test_due.py', test)
    write(path / DIR / 'implementation-plan.md', plan(ID, [
        ('顯示到期日', '✅ 2026-11-17；`python3 -m unittest -v` 3 項全數通過（test_render_shows_due）'),
        ('列出逾期', '✅ 2026-11-17；同上，test_overdue'),
        ('依 review 建議：補沒有到期日時 render 的測試，日期轉換抽成 short_date',
         '✅ 2026-11-18；`python3 -m unittest -v` 4 項全數通過')]).replace('SCN-003', 'SCN-001'))
    commit(path, f'refactor: 依審查建議抽出 short_date，補沒有到期日的測試\n\nRefs: #{ID}', '2026-11-18')
    return head1, git(path, 'rev-parse', 'HEAD'), m10.run_tests(path)


FORMAT_OVERVIEW = '待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦。目前 S1、S2 都已完成，測試全數通過，等待審查。'
FORMAT_TIMELINE = [('2026-11-16', '建立並核准', '開發者'), ('2026-11-17', '完成 S1', '開發者'),
                   ('2026-11-17', '完成 S2', '開發者')]
# 2026-11-24 第一次實跑後補完整的紅綠重構證據，見 expected.md「第一次實跑後重跑 wf44、wf44b」
FORMAT_EVIDENCE = [
    ('顯示到期日', '✅ 2026-11-17。單迴圈合併：`render` 的回傳值就是 CLI 列出的輸出，`test_render_shows_due` 直接斷言整行字串，'
     '沒有另一層整合責任。紅燈：先加 test_due.py，`python3 -m unittest test_due.DueTest.test_render_shows_due` exit 1，'
     'AssertionError，輸出少了「（到期 11/20）」。綠燈：加入 `due_of` 與 `render` 的到期日後 `python3 -m unittest -v` exit 0，'
     'Ran 3 tests OK（被測內容即 H1 的 todo.py）。重構：no-op，`render` 只多一段判斷，沒有可抽出的重複'),
    ('列出逾期', '✅ 2026-11-17。單迴圈合併：`overdue` 是函式層級的驗收（SCN-002 的 When 是「呼叫 overdue」）。'
     '紅燈：先放回傳 `[]` 的 `overdue`，`python3 -m unittest test_due.DueTest.test_overdue` exit 1，AssertionError `[] != [1]`。'
     '綠燈：實作後 `python3 -m unittest -v` exit 0，Ran 3 tests OK。重構：no-op，只有一行 list comprehension')]
FORMAT_TBD = ('## 待確認事項\n\n| 編號 | 事項 | 狀態 | 影響 |\n|---|---|---|---|\n'
              '| TBD-1 | 沒有到期日的待辦要不要顯示「（無到期日）」 | 已解決：2026-11-16 | 使用者選不顯示，維持原本的輸出；SCN-001 |\n')
GATE_TBD = '| TBD-2 | SCN-002 逾期要以今天還是明天為界，等使用者確認 | 待確認 | SCN-002 |\n'
APPROVED_ALL = '全部 Scenario 於 2026-11-16 核准。'
APPROVAL_TABLE = ('| Scenario | 核准日期 | 狀態 |\n|----------|---------|------|\n'
                  '| SCN-001 | 2026-11-16 | 已核准 |\n| SCN-002 | - | 待核准 |')


def build_format(kit, path, gate):
    """WF-44：H1 已實作、等待第一次審查；README 有格式問題，gate 組另有待核准卻已實作的 Scenario。"""
    text = medium(ID, '到期日', FORMAT_OVERVIEW, m10.SCN, '待提交', '待實作', FORMAT_TIMELINE[:1], '2026-11-16')
    assert text.count(APPROVED_ALL) == 1
    if gate:
        text = text.replace(APPROVED_ALL, APPROVAL_TABLE)
    tbd = FORMAT_TBD + (GATE_TBD if gate else '')
    text = text.replace('## Timeline', tbd + '\n## Timeline', 1)
    rows = '\n'.join(f'| {d} | {e} | {who} |' for d, e, who in FORMAT_TIMELINE)
    _, head1 = h1(kit, path, text, lambda t: t.replace('| 2026-11-16 | 建立並核准 | 開發者 |', rows), FORMAT_EVIDENCE)
    return head1, head1, m10.run_tests(path)


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    cases = [(n, lambda p, d=d: build_suggestions(kit, p, d)) for n, d in [('wf43', False), ('wf43b', True)]]
    cases += [(n, lambda p, g=g: build_format(kit, p, g)) for n, g in [('wf44', False), ('wf44b', True)]]
    for name, make in cases:
        first, head, tests = make(out / name)
        print(f'{name}: H1 {first[:7]} HEAD {head[:7]} tests exit={tests[0]} {tests[1]}')


if __name__ == '__main__':
    main()
