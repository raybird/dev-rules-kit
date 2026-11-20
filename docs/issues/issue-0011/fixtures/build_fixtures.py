#!/usr/bin/env python3
"""建立 issue-0011 的行為案例 fixture：WF-38 合併前寫好的已完成（未合併 wf38、已合併 wf38b）、
WF-39 審查通過後寫好終態（wf39）。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0010 WF-37 對照組（wf37b）的待辦 CLI、issue 3601 與沒有建議的 PASS 報告，H1 另更新根目錄 README 的使用說明；
docs/ 由該 kit 的 init-project.py 部署。fixture 只含下游專案內容，不含預期答案。

- wf39：H1 有 PASS 報告、沒有任何建議；README 狀態「審查通過」，報告與 ## 現況 已提交，之後沒有其他提交。
- wf38：同 wf39，再多一個記帳提交把狀態寫成「已完成」；分支還沒併入 main。
- wf38b：同 wf38，分支已以 --no-ff 併入 main（merge commit subject 含 issue-3601），工作目錄在 main。
"""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('issue10', HERE.parents[1] / 'issue-0010/fixtures/build_fixtures.py')
issue10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(issue10)
run, commit, write, git, ID, DIR = (
    issue10.run, issue10.commit, issue10.write, issue10.git, issue10.ID, issue10.DIR)


USAGE = '- `python3 todo.py`：列出\n'
USAGE_DUE = USAGE + '  - 有到期日的待辦在結尾顯示「（到期 MM/DD）」\n'


def build_pass(kit, path):
    """issue-0010 build_pass 的 clean 組，另在 H1 更新根目錄 README 的使用說明（fixture project.md 的常青文件觸發），
    避免 agent 停下來詢問與本案例無關的常青文件 gate（WF-37 實跑時兩組都問了）。"""
    base, medium, plan, current_state = issue10.base, issue10.medium, issue10.plan, issue10.current_state
    base(kit, path)
    main_sha = git(path, 'rev-parse', 'HEAD')
    run(path, 'git', 'checkout', '-q', '-b', f'issue-{ID}-due')
    readme = path / DIR / 'README.md'
    write(readme, medium(ID, '到期日', '待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦。', issue10.SCN, '待提交', '待實作',
                         [('2026-11-16', '建立並核准', '開發者')], '2026-11-16'))
    write(path / DIR / 'implementation-plan.md', plan(ID, [('顯示到期日', '📝'), ('列出逾期', '📝')]))
    commit(path, f'docs: 建立 issue #{ID} 規格與計畫\n\nRefs: #{ID}', '2026-11-16')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    src = (path / 'todo.py').read_text()
    assert issue10.RENDER_OLD in src
    write(path / 'todo.py', src.replace(issue10.RENDER_OLD, issue10.DUE_H1 + '\n\n\n' + issue10.RENDER_H1))
    write(path / 'test_due.py', issue10.TEST_H1_CONTROL)
    root = (path / 'README.md').read_text()
    assert root.count(USAGE) == 1
    write(path / 'README.md', root.replace(USAGE, USAGE_DUE))
    text = readme.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
    write(readme, text.replace('**狀態**: 待實作', '**狀態**: 審查中'))
    write(path / DIR / 'implementation-plan.md', plan(ID, [
        ('顯示到期日', '✅ 2026-11-17；`python3 -m unittest -v` 3 項全數通過（test_render_shows_due）'),
        ('列出逾期', '✅ 2026-11-17；同上，test_overdue')]))
    commit(path, f'feat: 待辦支援到期日與逾期清單\n\nRefs: #{ID}', '2026-11-17')
    h1 = git(path, 'rev-parse', 'HEAD')
    name = f'review-{h1[:7]}.md'
    write(path / DIR / name, issue10.report(h1, main_sha, issue10.FINDINGS['clean']))
    text = readme.read_text().replace('## 文件清單', current_state(name, []) + '## 文件清單', 1)
    text = text.replace('| 2026-11-16 | 建立並核准 | 開發者 |',
                        '| 2026-11-16 | 建立並核准 | 開發者 |\n| 2026-11-18 | 審查 PASS | 開發者 |')
    write(readme, text.replace('**狀態**: 審查中', '**狀態**: 審查通過'))
    commit(path, f'docs: 保存 issue #{ID} 審查報告 {name[:-3]}\n\nRefs: #{ID}', '2026-11-18')
    return h1, git(path, 'rev-parse', 'HEAD'), issue10.run_tests(path)


def build(kit, path, kind):
    h1, _, tests = build_pass(kit, path)
    if kind in ('done', 'merged'):
        readme = path / DIR / 'README.md'
        text = readme.read_text()
        assert text.count('**狀態**: 審查通過') == 1
        write(readme, text.replace('**狀態**: 審查通過', '**狀態**: 已完成'))
        commit(path, f'docs: issue #{ID} 審查通過，標記已完成\n\nRefs: #{ID}', '2026-11-18')
    if kind == 'merged':
        run(path, 'git', 'checkout', '-q', 'main')
        run(path, 'git', 'merge', '-q', '--no-ff', f'issue-{ID}-due', '-m', f'Merge issue-{ID}-due：待辦支援到期日與逾期清單')
    return h1, git(path, 'rev-parse', 'HEAD'), tests


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    for name, kind in [('wf38', 'done'), ('wf38b', 'merged'), ('wf39', 'pass')]:
        h1, head, tests = build(kit, out / name, kind)
        branch = git(out / name, 'rev-parse', '--abbrev-ref', 'HEAD')
        merged = run_check(out / name)
        print(f'{name}: H1 {h1[:7]} HEAD {head[:7]} branch={branch} merged_into_main={merged} '
              f'tests exit={tests[0]} {tests[1]}')


def run_check(path):
    import subprocess
    return subprocess.run(['git', 'merge-base', '--is-ancestor', f'issue-{ID}-due', 'main'], cwd=path).returncode == 0


if __name__ == '__main__':
    main()
