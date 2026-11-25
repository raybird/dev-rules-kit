#!/usr/bin/env python3
"""建立 issue-0017 的行為案例 fixture：WF-45 新開 issue 的核准紀錄、WF-46 修訂後重新核准、
WF-47 讀核准紀錄判斷下一步、WF-48 PASS 之後補記 README 與發現凍結內容寫錯。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0010、issue-0012 的待辦到期日 issue（3601）；docs/ 由該 kit 的 init-project.py 部署。
fixture 只含下游專案內容，不含預期答案。

- wf45：只有 main，還沒有 issue 文件；使用者在對話中提出需求。
- wf46：SCN-001 已核准、S1 已完成；SCN-002 因 TBD-1（今天到期算不算逾期）改為待重新核准，核准表兩列。
- wf47：wf46 的修訂已核准，核准表已收回單行；Timeline 與已解決的 TBD-1 提過待重新核准；S2 還沒做。
- wf47b：SCN-002 仍待核准（TBD-1 待確認），核准表兩列；S2 還沒做。
- wf48、wf48b：H1 有 PASS 報告（沒有建議），報告與 `## 現況` 已提交；H1 改了根目錄 README.md，
  issue README 的「涉及檔案」只寫 todo.py 與測試檔。
"""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, HERE.parents[1] / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m10 = load('issue10', 'issue-0010/fixtures/build_fixtures.py')
m12 = load('issue12', 'issue-0012/fixtures/build_fixtures.py')
run, commit, write, git, base, medium, plan, current_state = (
    m10.run, m10.commit, m10.write, m10.git, m10.base, m10.medium, m10.plan, m10.current_state)
ID, DIR = m10.ID, m10.DIR
OVERVIEW = '待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦。'

APPROVED_ALL = '全部 Scenario 於 2026-11-16 核准。'
SOURCE_OLD = '- **核准來源**: 2026-11-16 使用者回覆「核准」'
SOURCE_1 = '- **核准來源**: 2026-11-16 使用者回覆「核准」（SCN-001、SCN-002）'
SOURCE_2 = SOURCE_1 + '；2026-11-19 依 TBD-1 重新核准 SCN-002'
TABLE = ('| Scenario | 核准日期 | 狀態 |\n|----------|---------|------|\n'
         '| SCN-001 | 2026-11-16 | 已核准 |\n| SCN-002 | {d2} | {s2} |')
TBD_HEAD = '## 待確認事項\n\n| 編號 | 事項 | 狀態 | 影響 |\n|---|---|---|---|\n'
TBD1_OPEN = ('| TBD-1 | SCN-002 的邊界：到期日是今天的未完成待辦算不算逾期。建議不算：到期日早於今天才算逾期，'
             '今天到期的使用者當天還來得及處理 | 待確認 | SCN-002 |\n')
TBD1_DONE = ('| TBD-1 | SCN-002 的邊界：到期日是今天的未完成待辦算不算逾期 | 已解決：2026-11-19 使用者選「不算，'
             '到期日早於今天才算逾期（建議）」；SCN-002 補上今天到期不列入的情況 | SCN-002 |\n')
_OVERDUE_TEST = m10.TEST_H1[m10.TEST_H1.index('    def test_overdue'):m10.TEST_H1.index('\n\nif __name__')]
TEST_S1 = m10.TEST_H1.replace('\n' + _OVERDUE_TEST, '')
assert 'overdue' not in TEST_S1 and 'test_render_shows_due' in TEST_S1
SCN_REVISED = m10.SCN[:1] + [('列出逾期', '今天是 2026-11-19，未完成的待辦到期日分別為 2026-11-01、2026-11-19 與 2026-12-01',
                              '呼叫 overdue', '只回傳到期日為 2026-11-01 的那一筆')]


def spec_and_s1(kit, path, scenarios, approval_block, source, tbd, timeline, s2_state='📝'):
    """main、issue 分支的規格提交與 S1 提交；SCN-002 的狀態由 approval_block 決定。回傳規格提交的短 SHA。"""
    base(kit, path)
    run(path, 'git', 'checkout', '-q', '-b', f'issue-{ID}-due')
    readme = path / DIR / 'README.md'
    text = medium(ID, '到期日', OVERVIEW, scenarios, '待提交', '實作中', timeline, '2026-11-16')
    assert text.count(APPROVED_ALL) == 1 and text.count(SOURCE_OLD + '\n') == 1
    text = text.replace(APPROVED_ALL, approval_block).replace(SOURCE_OLD + '\n', source + '\n')
    text = text.replace('## Timeline', TBD_HEAD + tbd + '\n## Timeline', 1)
    write(readme, text)
    write(path / DIR / 'implementation-plan.md', plan(ID, [('顯示到期日', '📝'), ('列出逾期', s2_state)]))
    commit(path, f'docs: 建立 issue #{ID} 規格與計畫\n\nRefs: #{ID}', '2026-11-16')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    src = (path / 'todo.py').read_text()
    assert m10.RENDER_OLD in src
    write(path / 'todo.py', src.replace(m10.RENDER_OLD, m10.DUE_OF_H1 + '\n\n\n' + m10.RENDER_H1))
    write(path / 'test_due.py', TEST_S1)
    write(readme, readme.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}'))
    write(path / DIR / 'implementation-plan.md', plan(ID, [
        ('顯示到期日', '✅ 2026-11-17；`python3 -m unittest -v` 全數通過（test_render_shows_due）'), ('列出逾期', s2_state)]))
    commit(path, f'feat: 待辦顯示到期日\n\nRefs: #{ID}', '2026-11-17')
    return spec


def build_new(kit, path):
    """WF-45：只有 main。"""
    base(kit, path)
    return git(path, 'rev-parse', 'HEAD'), git(path, 'rev-parse', 'HEAD'), m10.run_tests(path)


def build_reapprove(kit, path):
    """WF-46：SCN-002 待重新核准，等 TBD-1 的決定。"""
    timeline = [('2026-11-16', '建立並核准 SCN-001、SCN-002', '開發者'),
                ('2026-11-18', 'SCN-002 改為待重新核准：今天到期算不算逾期沒有定義（TBD-1）', '開發者')]
    spec_and_s1(kit, path, m10.SCN, TABLE.format(d2='-', s2='待重新核准'), SOURCE_1, TBD1_OPEN, timeline, '⏸️ 等 TBD-1')
    head = git(path, 'rev-parse', 'HEAD')
    return head, head, m10.run_tests(path)


def build_collapsed(kit, path):
    """WF-47：修訂已核准、核准表已收回單行，S2 還沒做。"""
    timeline = [('2026-11-16', '建立並核准 SCN-001、SCN-002', '開發者'),
                ('2026-11-18', 'SCN-002 改為待重新核准：今天到期算不算逾期沒有定義（TBD-1）', '開發者'),
                ('2026-11-19', '規格修訂：依 TBD-1 修訂 SCN-002 並重新核准，原基線見提交歷史', '開發者')]
    spec_and_s1(kit, path, SCN_REVISED, '全部 Scenario 於 2026-11-19 核准。', SOURCE_2, TBD1_DONE, timeline)
    head = git(path, 'rev-parse', 'HEAD')
    return head, head, m10.run_tests(path)


def build_pending(kit, path):
    """WF-47b：SCN-002 仍待核准，S2 還沒做。"""
    timeline = [('2026-11-16', '建立；核准 SCN-001，SCN-002 等 TBD-1', '開發者')]
    spec_and_s1(kit, path, m10.SCN, TABLE.format(d2='-', s2='待核准'),
                '- **核准來源**: 2026-11-16 使用者回覆「SCN-001 核准，SCN-002 等我想清楚逾期的邊界」', TBD1_OPEN, timeline)
    head = git(path, 'rev-parse', 'HEAD')
    return head, head, m10.run_tests(path)


def build_pass(kit, path):
    """WF-48：H1 有 PASS 報告（沒有建議），報告與 ## 現況 已提交；H1 改了根目錄 README.md。"""
    readme_text = medium(ID, '到期日', OVERVIEW, m10.SCN, '待提交', '待實作', [('2026-11-16', '建立並核准', '開發者')],
                         '2026-11-16')
    main_sha, head1 = m12.h1(kit, path, readme_text)
    assert 'README.md' in git(path, 'diff', '--name-only', main_sha, head1).split()
    readme = path / DIR / 'README.md'
    name = f'review-{head1[:7]}.md'
    write(path / DIR / name, m10.report(head1, main_sha, m10.FINDINGS['clean']))
    text = readme.read_text().replace('## 文件清單', current_state(name, []) + '## 文件清單', 1)
    text = text.replace('| 2026-11-16 | 建立並核准 | 開發者 |',
                        '| 2026-11-16 | 建立並核准 | 開發者 |\n| 2026-11-18 | 審查 PASS，沒有建議 | 開發者 |')
    write(readme, text.replace('**狀態**: 審查中', '**狀態**: 審查通過'))
    commit(path, f'docs: 保存 issue #{ID} 審查報告 {name[:-3]}\n\nRefs: #{ID}', '2026-11-18')
    return head1, git(path, 'rev-parse', 'HEAD'), m10.run_tests(path)


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    cases = [('wf45', build_new), ('wf46', build_reapprove), ('wf47', build_collapsed), ('wf47b', build_pending),
             ('wf48', build_pass), ('wf48b', build_pass)]
    for name, make in cases:
        first, head, tests = make(kit, out / name)
        print(f'{name}: H1 {first[:7]} HEAD {head[:7]} tests exit={tests[0]} {tests[1]}')


if __name__ == '__main__':
    main()
