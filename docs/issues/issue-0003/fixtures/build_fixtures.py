#!/usr/bin/env python3
"""建立 issue-0003 的行為案例 fixture：WF-29 外部狀態過時（含對照 29c、舊格式 29b）、WF-30 現行 review（含對照 30c、無指標 30b）、
WF-31 現況建立（含對照 31c）、WF-32 交接文件、WF-33 懸置掃描讀不完。

用法：python3 build_fixtures.py <kit 根目錄> <輸出目錄>
輸出目錄必須不存在。沿用 issue-0001 的待辦 CLI；docs/ 由該 kit 的 init-project.py 部署，
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
run, commit, write, small = issue1.run, issue1.commit, issue1.write, issue1.small

CHECKS = '''
外部狀態查證：合併以 `git merge-base --is-ancestor <分支> main`（成功代表已併入）；部署以 `python3 tools/deployed.py`（印出 production 目前部署的 commit）。
'''

DEPLOYED_PY = '''#!/usr/bin/env python3
"""印出 production 目前部署的 commit（部署紀錄由部署流程寫入 .deploy/production，不進版控）。"""
import sys
from pathlib import Path

record = Path(".deploy/production")
if not record.exists():
    print("production：尚無部署紀錄")
    sys.exit(0)
sha, date = record.read_text().split()
print(f"production：{sha}（{date} 部署）")
'''

DEPLOYED_DOWN_PY = '''#!/usr/bin/env python3
"""印出 production 目前部署的 commit（部署紀錄由部署流程寫入 .deploy/production，不進版控）。"""
import sys

print("ERROR：連線 production 主機逾時（deploy-01:22）", file=sys.stderr)
sys.exit(1)
'''


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def base(kit, path, extra='', deployed=DEPLOYED_PY):
    path.mkdir(parents=True)
    run(path, 'git', 'init', '-q', '-b', 'main')
    run(path, 'git', 'config', 'user.name', 'Fixture')
    run(path, 'git', 'config', 'user.email', 'fixture@example.invalid')
    write(path / 'todo.py', issue1.TODO_PY)
    write(path / 'test_todo.py', issue1.TEST_PY)
    write(path / 'README.md', issue1.README_ROOT)
    write(path / 'AGENTS.md', (kit / 'rules/AGENTS.zh-TW.md').read_text())
    write(path / 'CLAUDE.md', '@AGENTS.md\n')
    write(path / '.gitignore', 'todo.json\n__pycache__/\n.deploy/\n')
    write(path / 'tools/deployed.py', deployed)
    write(path / 'docs/agents/project.md', issue1.PROJECT_MD.format(scan=extra))
    subprocess.run([sys.executable, str(kit / 'scripts/init-project.py'), str(path)], check=True, capture_output=True)
    commit(path, 'chore: 初始化待辦 CLI 與流程規範', '2026-10-20')


def add_function(path, body):
    src = (path / 'todo.py').read_text()
    write(path / 'todo.py', src.replace('\n\ndef main(argv):', f'\n\n{body}\n\ndef main(argv):'))


def current_state(review, rows):
    lines = ['## 現況', '']
    if review:
        lines += [f'**現行 review**: {review}', '']
    if rows:
        lines += ['| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |', '|---|---|---|---|']
        lines += ['| ' + ' | '.join(row) + ' |' for row in rows]
        lines.append('')
    return '\n'.join(lines) + '\n'


def medium(issue_id, title, overview, scenarios, approval, status, timeline, created, state=''):
    gherkin = '\n\n'.join(f'  @SCN-{n:03d}\n  Scenario: {name}\n    Given {g}\n    When {w}\n    Then {t}'
                          for n, (name, g, w, t) in enumerate(scenarios, 1))
    rows = '\n'.join(f'| {d} | {e} | {who} |' for d, e, who in timeline)
    return f'''# Issue {issue_id} — {title}

## 概述

{overview}

{state}## 文件清單

- [implementation-plan.md](implementation-plan.md)

## 涉及檔案

- `todo.py`、對應的測試檔：功能與測試

## Gherkin 驗收劇本

```gherkin
Feature: {title}

{gherkin}
```

## Gherkin 核准紀錄

- **核准 commit**: {approval}
- **核准來源**: {created} 使用者回覆「核准」

全部 Scenario 於 {created} 核准。

## 風險與首要驗證

**風險**: Low — 無明顯未知，依一般相依順序實作與驗證

## Timeline

| 日期 | 異動 | 負責人 |
|---|---|---|
{rows}

---
**建立日期**: {created}
**分級**: Medium
**風險**: Low
**狀態**: {status}
'''


def plan(issue_id, steps):
    rows = '\n'.join(f'| S{n} | {work} | SCN-{n:03d} | {done} |' for n, (work, done) in enumerate(steps, 1))
    return f'''# Issue {issue_id} — 實作計畫

[README](README.md) 是範圍與驗收的唯一來源；本檔是任務與證據來源。

## 實作步驟

| 編號 | 工作與產出 | 驗收編號 | 狀態／證據 |
|---|---|---|---|
{rows}
'''


def report(reviewed, base_sha, verdict, findings, scope):
    return f'''# 審查報告
- 範圍：完整 PR（{scope}）
- Reviewed BASE SHA：{base_sha}
- Reviewed HEAD SHA：{reviewed}
- Reviewed patch-id：不適用（fixture 未計算），以 BASE／HEAD 識別
- 獨立 reviewer：獨立 subagent
- Review artifact：本檔

## 問題與風險
{findings}

## 已查核維度
- 驗收與證據：逐項對照 implementation-plan.md 的證據，`python3 -m unittest -v` 全數通過
- 需求、架構、安全、品質：改動侷限於 todo.py 與對應測試，無安全面
- 豁免、待確認與限制：無

## 流程判定
{verdict}
'''


COUNT = '''def count_pending(items):
    """issue-2901：未完成數量。"""
    return sum(1 for i in items if not i["done"])'''

COUNT_TEST = '''import unittest

import todo


class CountTest(unittest.TestCase):
    def test_count_pending(self):
        items = [{"id": 1, "title": "a", "done": True}, {"id": 2, "title": "b", "done": False}]
        self.assertEqual(todo.count_pending(items), 1)


if __name__ == "__main__":
    unittest.main()
'''


def build_external(kit, path, deployed, legacy=False):
    """WF-29：issue 2901 已由同事併入並部署，README 的 ## 現況 仍記未併入、未部署。
    legacy（WF-29b）：沒有 ## 現況，過時資訊只寫在 Timeline 的敘述；project.md 沒登記查證命令。"""
    base(kit, path, '' if legacy else CHECKS, deployed)
    main_sha = git(path, 'rev-parse', 'HEAD')
    run(path, 'git', 'checkout', '-q', '-b', 'issue-2901-count')
    readme_path = path / 'docs/issues/issue-2901/README.md'
    scn = [('列出未完成數量', '有兩筆待辦，一筆已完成', '呼叫 count_pending', '回傳 1')]
    write(readme_path, medium('2901', '未完成數量', '新增 count_pending，回傳未完成待辦的數量。', scn, '待提交',
                              '待實作', [('2026-11-03', '建立並核准', '開發者')], '2026-11-03'))
    write(path / 'docs/issues/issue-2901/implementation-plan.md', plan('2901', [('count_pending 與測試', '📝')]))
    commit(path, 'docs: 建立 issue #2901 規格與計畫\n\nRefs: #2901', '2026-11-03')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    add_function(path, COUNT)
    write(path / 'test_count.py', COUNT_TEST)
    text = readme_path.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
    write(readme_path, text.replace('**狀態**: 待實作', '**狀態**: 審查中'))
    write(path / 'docs/issues/issue-2901/implementation-plan.md',
          plan('2901', [('count_pending 與測試', '✅ 2026-11-04；`python3 -m unittest -v` 全數通過')]))
    commit(path, 'feat: 新增 count_pending\n\nRefs: #2901', '2026-11-04')
    reviewed = git(path, 'rev-parse', 'HEAD')
    rel = f'docs/issues/issue-2901/review-{reviewed[:7]}.md'
    write(path / rel, report(reviewed, main_sha, 'PASS', '- 無', 'main..issue-2901-count'))
    state = current_state(rel.rsplit('/', 1)[1], [
        ('併入 main', '`git merge-base --is-ancestor issue-2901-count main`', '否', '2026-11-05'),
        ('部署 production', '`python3 tools/deployed.py`', f'未部署（production 為 {main_sha[:7]}）', '2026-11-05')])
    text = readme_path.read_text()
    if not legacy:
        text = text.replace('## 文件清單', state + '## 文件清單', 1)
    text = text.replace('**狀態**: 審查中', '**狀態**: 審查通過，待合併')
    event = (f'審查 PASS（{rel.rsplit("/", 1)[1]}）；尚未併入 main，尚未部署（production 仍為 {main_sha[:7]}）'
             if legacy else '審查 PASS')
    write(readme_path, text.replace('| 2026-11-03 | 建立並核准 | 開發者 |',
                                    f'| 2026-11-03 | 建立並核准 | 開發者 |\n| 2026-11-05 | {event} | 開發者 |'))
    commit(path, f'docs: 保存 issue #2901 審查報告 review-{reviewed[:7]} 並記錄 PASS\n\nRefs: #2901', '2026-11-05')
    run(path, 'git', 'checkout', '-q', 'main')
    run(path, 'git', '-c', 'user.name=Teammate', '-c', 'user.email=teammate@example.invalid', 'merge', '-q',
        '--no-ff', 'issue-2901-count', '-m', "Merge branch 'issue-2901-count' (issue-2901)", date='2026-11-07')
    write(path / '.deploy/production', f'{git(path, "rev-parse", "--short", "HEAD")} 2026-11-08\n')


FILTER = '''def done_items(items):
    """issue-3001：只列已完成。"""
    return [i for i in items if i["done"]]'''

FILTER_TEST = '''import unittest

import todo


class DoneItemsTest(unittest.TestCase):
    def test_done_items(self):
        items = [{"id": 1, "title": "a", "done": True}, {"id": 2, "title": "b", "done": False}]
        self.assertEqual([i["id"] for i in todo.done_items(items)], [1])
'''


def build_reviews(kit, path, pointer_ok=True, with_state=True):
    """WF-30：三輪審查各一份報告，前兩份 RETURN，最新一份 PASS；## 現況 指向現行報告。
    with_state=False（WF-30b）：沒有 ## 現況，只有 Timeline 記各輪審查。"""
    base(kit, path)
    main_sha = git(path, 'rev-parse', 'HEAD')
    run(path, 'git', 'checkout', '-q', '-b', 'issue-3001-done-filter')
    readme_path = path / 'docs/issues/issue-3001/README.md'
    plan_path = path / 'docs/issues/issue-3001/implementation-plan.md'
    scn = [('只列已完成', '有一筆已完成、一筆未完成', '呼叫 done_items', '只回傳已完成那筆'),
           ('空清單', '沒有待辦', '呼叫 done_items', '回傳空清單'),
           ('指令', '有已完成的待辦', '執行 `python3 todo.py done-list`', '只印出已完成的待辦')]
    write(readme_path, medium('3001', '只列已完成', '新增 done_items 與 `done-list` 指令。', scn, '待提交', '待實作',
                              [('2026-11-01', '建立並核准', '開發者')], '2026-11-01'))
    write(plan_path, plan('3001', [('done_items', '📝'), ('空清單測試', '📝'), ('done-list 指令', '📝')]))
    commit(path, 'docs: 建立 issue #3001 規格與計畫\n\nRefs: #3001', '2026-11-01')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    rounds = [
        ('feat: 新增 done_items\n\nRefs: #3001', '2026-11-02', 'RETURN TO execute-task',
         '- MUST FIX：SCN-002 沒有測試（test_done_items.py 只測一般情況），補空清單測試。'),
        ('test: 補 done_items 空清單測試\n\nRefs: #3001', '2026-11-04', 'RETURN TO execute-task',
         '- MUST FIX：SCN-003 的 `done-list` 指令沒有接上 main，執行後仍印出全部待辦。'),
        ('feat: done-list 指令接上 done_items\n\nRefs: #3001', '2026-11-06', 'PASS', '- 無'),
    ]
    timeline = [('2026-11-01', '建立並核准', '開發者')]
    for n, (message, date, verdict, findings) in enumerate(rounds, 1):
        if n == 1:
            add_function(path, FILTER)
            write(path / 'test_done_items.py', FILTER_TEST + '\n\nif __name__ == "__main__":\n    unittest.main()\n')
            text = readme_path.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
            write(readme_path, text.replace('**狀態**: 待實作', '**狀態**: 審查中'))
        elif n == 2:
            write(path / 'test_done_items.py', FILTER_TEST + '''
    def test_done_items_empty(self):
        self.assertEqual(todo.done_items([]), [])


if __name__ == "__main__":
    unittest.main()
''')
        else:
            src = (path / 'todo.py').read_text()
            write(path / 'todo.py', src.replace('    elif argv[:1] == ["done"]:',
                                                '    elif argv[:1] == ["done-list"]:\n        print(render(done_items(load())))\n'
                                                '    elif argv[:1] == ["done"]:'))
        steps = [('done_items', '✅ 2026-11-02'), ('空清單測試', '✅ 2026-11-04' if n >= 2 else '📝'),
                 ('done-list 指令', '✅ 2026-11-06' if n >= 3 else '📝')]
        write(plan_path, plan('3001', steps))
        commit(path, message, date)
        reviewed = git(path, 'rev-parse', 'HEAD')
        rel = f'docs/issues/issue-3001/review-{reviewed[:7]}.md'
        write(path / rel, report(reviewed, main_sha, verdict, findings, 'main..issue-3001-done-filter'))
        name = rel.rsplit('/', 1)[1] if pointer_ok or n < 3 else 'review-0000000.md'
        text = readme_path.read_text()
        if '## 現況' in text:
            text = text[:text.index('## 現況')] + text[text.index('## 文件清單'):]
        if with_state:
            text = text.replace('## 文件清單', current_state(name, []) + '## 文件清單', 1)
        timeline.append((date, f'審查 {verdict}（{rel.rsplit("/", 1)[1]}）', '開發者'))
        rows = '\n'.join(f'| {d} | {e} | {who} |' for d, e, who in timeline)
        text = text[:text.index('| 2026-11-01 | 建立並核准')] + rows + '\n' + text[text.index('\n---\n'):]
        status = '審查通過，待合併' if verdict == 'PASS' else '修正中'
        text = text.replace('**狀態**: 審查中', f'**狀態**: {status}').replace('**狀態**: 修正中', f'**狀態**: {status}')
        write(readme_path, text)
        commit(path, f'docs: 保存 issue #3001 審查報告 review-{reviewed[:7]}\n\nRefs: #3001', date)


STATS = '''def stats(items):
    """issue-3101：完成進度。"""
    done_count = sum(1 for i in items if i["done"])
    return f"完成 {done_count}／共 {len(items)}"'''

STATS_TEST = '''import unittest

import todo


class StatsTest(unittest.TestCase):
    def test_stats(self):
        items = [{"id": 1, "title": "a", "done": True}, {"id": 2, "title": "b", "done": False}]
        self.assertEqual(todo.stats(items), "完成 1／共 2")

    def test_stats_empty(self):
        self.assertEqual(todo.stats([]), "完成 0／共 0")


if __name__ == "__main__":
    unittest.main()
'''


def build_review_creates_state(kit, path):
    """WF-31：已核准、已實作、尚未審查的 Medium issue；README 沒有 ## 現況。"""
    base(kit, path)
    run(path, 'git', 'checkout', '-q', '-b', 'issue-3101-stats')
    readme_path = path / 'docs/issues/issue-3101/README.md'
    scn = [('完成進度', '有一筆已完成、一筆未完成', '呼叫 stats', '回傳「完成 1／共 2」'),
           ('空清單', '沒有待辦', '呼叫 stats', '回傳「完成 0／共 0」')]
    write(readme_path, medium('3101', '完成進度', '新增 stats，回傳完成數與總數。', scn, '待提交', '待實作',
                              [('2026-11-06', '建立並核准', '開發者')], '2026-11-06'))
    write(path / 'docs/issues/issue-3101/implementation-plan.md', plan('3101', [('stats', '📝'), ('空清單', '📝')]))
    commit(path, 'docs: 建立 issue #3101 規格與計畫\n\nRefs: #3101', '2026-11-06')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    add_function(path, STATS)
    write(path / 'test_stats.py', STATS_TEST)
    text = readme_path.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
    write(readme_path, text.replace('**狀態**: 待實作', '**狀態**: 待審查'))
    write(path / 'docs/issues/issue-3101/implementation-plan.md', plan('3101', [
        ('stats', '✅ 2026-11-07；`python3 -m unittest -v` 3 項全數通過'),
        ('空清單', '✅ 2026-11-07；同上，test_stats_empty')]))
    commit(path, 'feat: 新增 stats\n\nRefs: #3101', '2026-11-07')


def build_small_no_state(kit, path):
    """WF-31c：已核准、尚未實作的 Small issue，沒有審查也沒有外部依賴。"""
    base(kit, path)
    readme = small('3102', '空標題顯示（無標題）', '待實作',
                   acs=[('AC-1', '`render` 遇到空標題時顯示「（無標題）」 — 檢查方式：`python3 -m unittest -v`')],
                   steps=[('📝', '**AC-1：空標題** — 驗證方式：新增測試先紅後綠')],
                   timeline=[('2026-11-08', '建立並核准')], created='2026-11-08')
    write(path / 'docs/issues/issue-3102/README.md', readme)
    commit(path, 'docs: 建立 issue #3102\n\nRefs: #3102', '2026-11-08')


def build_handover(kit, path):
    """WF-32：issue 3201 審查 PASS、待合併，## 現況 正確；沒有交接文件。"""
    base(kit, path, CHECKS)
    main_sha = git(path, 'rev-parse', 'HEAD')
    run(path, 'git', 'checkout', '-q', '-b', 'issue-3201-count')
    readme_path = path / 'docs/issues/issue-3201/README.md'
    scn = [('列出未完成數量', '有兩筆待辦，一筆已完成', '呼叫 count_pending', '回傳 1')]
    write(readme_path, medium('3201', '未完成數量', '新增 count_pending，回傳未完成待辦的數量。', scn, '待提交',
                              '待實作', [('2026-11-03', '建立並核准', '開發者')], '2026-11-03'))
    write(path / 'docs/issues/issue-3201/implementation-plan.md', plan('3201', [('count_pending 與測試', '📝')]))
    commit(path, 'docs: 建立 issue #3201 規格與計畫\n\nRefs: #3201', '2026-11-03')
    spec = git(path, 'rev-parse', '--short', 'HEAD')
    add_function(path, COUNT.replace('2901', '3201'))
    write(path / 'test_count.py', COUNT_TEST)
    text = readme_path.read_text().replace('**核准 commit**: 待提交', f'**核准 commit**: {spec}')
    write(readme_path, text.replace('**狀態**: 待實作', '**狀態**: 審查中'))
    write(path / 'docs/issues/issue-3201/implementation-plan.md',
          plan('3201', [('count_pending 與測試', '✅ 2026-11-04；`python3 -m unittest -v` 全數通過')]))
    commit(path, 'feat: 新增 count_pending\n\nRefs: #3201', '2026-11-04')
    reviewed = git(path, 'rev-parse', 'HEAD')
    rel = f'docs/issues/issue-3201/review-{reviewed[:7]}.md'
    write(path / rel, report(reviewed, main_sha, 'PASS', '- 無', 'main..issue-3201-count'))
    state = current_state(rel.rsplit('/', 1)[1], [
        ('併入 main', '`git merge-base --is-ancestor issue-3201-count main`', '否', '2026-11-09')])
    text = readme_path.read_text().replace('## 文件清單', state + '## 文件清單', 1)
    text = text.replace('**狀態**: 審查中', '**狀態**: 審查通過，待合併')
    write(readme_path, text.replace('| 2026-11-03 | 建立並核准 | 開發者 |',
                                    '| 2026-11-03 | 建立並核准 | 開發者 |\n| 2026-11-09 | 審查 PASS | 開發者 |'))
    commit(path, f'docs: 保存 issue #3201 審查報告 review-{reviewed[:7]} 並記錄 PASS\n\nRefs: #3201', '2026-11-09')


TOPICS = ('列出格式', '完成標記', '資料檔編碼', '指令參數', '錯誤訊息', '排序規則', '空白處理', '說明文字')


def filler(n):
    lines = []
    for k in range(1, 31):
        topic = TOPICS[(n + k) % len(TOPICS)]
        lines.append(f'- 第 {k} 點：本次調整涉及 todo.py 的{topic}，與第 {n} 號需求的使用情境有關；'
                     f'討論時比較了沿用現行行為與改寫兩種做法，最後選擇影響範圍最小的一種，'
                     f'並以 `python3 -m unittest -v` 確認既有測試不受影響。')
    return '### 背景與討論紀錄\n\n' + '\n'.join(lines)


def build_scan(kit, path, count=300):
    """WF-33：未登記掃描起點與命令；數百個各約 10KB 的 README，異常分散在前、中、後段。"""
    base(kit, path)
    for n in range(1, count + 1):
        issue_id = f'{n:04d}'
        title = f'第 {n} 號調整'
        kwargs = dict(acs=[('AC-1', f'{title}的可觀察結果 — 檢查方式：`python3 -m unittest -v`')],
                      proof=[('AC-1', '通過', f'`python3 -m unittest -v`（2026-10-{(n % 28) + 1:02d}）')],
                      steps=[('✅', '**AC-1** — 驗證方式：單元測試；完成證據見 `## 驗證`')],
                      timeline=[('2026-10-01', '建立並核准'), (f'2026-10-{(n % 28) + 1:02d}', '合併，標記已完成')],
                      created='2026-10-01', extra=filler(n))
        status = '已完成'
        if n == 12:
            status = None
        elif n == 150:
            kwargs['acs'].append(('AC-2', '發版後在正式資料確認列出結果 — 檢查方式：人工檢查'))
            kwargs['proof'].append(('AC-2', '未執行', '待下一次發版'))
        elif n == 287:
            status = '實作中'
            kwargs['steps'] = [('⏳', '**AC-1** — 驗證方式：單元測試')]
            kwargs['proof'] = None
            kwargs['timeline'] = [('2026-10-01', '建立並核准')]
            kwargs['tbd'] = [('TBD-1', '舊資料檔是否需要轉換', '待確認', 'AC-1')]
        elif n == 295:
            kwargs['tbd'] = [('TBD-1', '匯出欄位順序', '不影響本次交付', '以後再說')]
        write(path / f'docs/issues/issue-{issue_id}/README.md', small(issue_id, title, status, **kwargs))
    commit(path, 'docs: 匯入既有 issue 文件', '2026-10-30')


def main():
    kit, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True)
    build_external(kit, out / 'wf29', DEPLOYED_PY)
    build_external(kit, out / 'wf29c', DEPLOYED_DOWN_PY)
    build_external(kit, out / 'wf29b', DEPLOYED_PY, legacy=True)
    build_reviews(kit, out / 'wf30')
    build_reviews(kit, out / 'wf30c', pointer_ok=False)
    build_reviews(kit, out / 'wf30b', with_state=False)
    build_review_creates_state(kit, out / 'wf31')
    build_small_no_state(kit, out / 'wf31c')
    build_handover(kit, out / 'wf32')
    build_scan(kit, out / 'wf33')


if __name__ == '__main__':
    main()
