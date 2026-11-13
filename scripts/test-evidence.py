#!/usr/bin/env python3
"""實際 Git fixture 與契約版本負向測試；不代替宿主 agent 行為驗證。"""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import sys
import unittest

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('check_kit', ROOT / 'scripts/check-kit.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='kit-evidence-')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.file = self.repo / 'docs/issues/issue-1/README.md'
        self.file.parent.mkdir(parents=True)
        self.file.write_text('AC-1: original\n')
        self.commit('approved')
        self.approval = self.git('rev-parse', 'HEAD')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-qm', message)

    def test_spec_diff_includes_staged_and_unstaged(self):
        self.file.write_text('AC-1: staged revision\n')
        self.git('add', '.')
        self.file.write_text('AC-1: working revision\n')
        # Run the literal command shipped to agents, with fixture variables.
        command = (ROOT / 'docs/agents/acceptance.md').read_text().split('```bash\n', 1)[1].split('```', 1)[0]
        result = subprocess.run(['bash', '-c', command], cwd=self.repo,
                                env=dict(os.environ, approval_commit=self.approval, issue_id='1'),
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('+AC-1: working revision', result.stdout)
        self.assertEqual(self.git('diff', self.approval + '..HEAD', '--', str(self.file)), '')

    def local_artifact(self, *, extra_change=False, symlink=False):
        (self.repo / 'app.txt').write_text('implementation\n')
        self.commit('implementation')
        reviewed = self.git('rev-parse', 'HEAD')
        rel = f'docs/issues/issue-1/review-{reviewed[:7]}.md'
        if symlink:
            (self.repo / rel).symlink_to('README.md')
        else:
            (self.repo / rel).write_text(f'- Reviewed HEAD SHA：{reviewed}\nPASS\n')
        if extra_change:
            (self.repo / 'app.txt').write_text('unreviewed change\n')
        self.commit('review artifact')
        return reviewed, rel

    def verify(self, reviewed, rel):
        return subprocess.run(['python3', str(ROOT / 'skills/review/scripts/verify-artifact.py'),
                               '--repo', str(self.repo), '--reviewed', reviewed,
                               '--head', self.git('rev-parse', 'HEAD'), '--artifact', rel],
                              capture_output=True, text=True)

    def test_artifact_only_commit_keeps_review_valid(self):
        reviewed, rel = self.local_artifact()
        self.assertNotEqual(reviewed, self.git('rev-parse', 'HEAD'))
        result = self.verify(reviewed, rel)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_artifact_plus_code_change_requires_review(self):
        reviewed, rel = self.local_artifact(extra_change=True)
        self.assertNotEqual(self.verify(reviewed, rel).returncode, 0)

    def test_report_rewrite_requires_review(self):
        reviewed, rel = self.local_artifact()
        # A later commit must not rewrite an already committed verdict.
        (self.repo / rel).write_text(f'- Reviewed HEAD SHA：{reviewed}\nFORGED PASS\n')
        self.commit('rewrite report')
        self.assertNotEqual(self.verify(reviewed, rel).returncode, 0)

    def test_symlink_report_rejected(self):
        reviewed, rel = self.local_artifact(symlink=True)
        self.assertNotEqual(self.verify(reviewed, rel).returncode, 0)

    def test_document_edit_does_not_break_contract(self):
        docs = self.repo / 'docs/AGENTS.md'
        docs.write_text('**文件版本**: 99.0\n**流程契約**: 2.1\n')
        skill = self.repo / 'skills/example/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('本 skill 需要 `docs/AGENTS.md` **流程契約 2.0**')
        self.assertEqual(checks.check_agents_md_declarations(str(self.repo)), [])
        for requirement in ('2.2', '3.0'):
            skill.write_text(f'本 skill 需要 `docs/AGENTS.md` **流程契約 {requirement}**')
            self.assertTrue(checks.check_agents_md_declarations(str(self.repo)))
        skill.write_text('引用 docs/AGENTS.md 但缺契約')
        self.assertTrue(checks.check_agents_md_declarations(str(self.repo)))


FIXTURE_README = '''# Issue 1 — fixture

## 概述

固定的範例需求。

## Gherkin 驗收劇本

```gherkin
Feature: fixture
  @SCN-001
  Scenario: 範例
    Given 已知狀態
    When 執行動作
    Then 看到結果
```

## Gherkin 核准紀錄

- **核准 commit**: 待提交
- **核准來源**: 2026-11-03 使用者回覆「核准」

全部 Scenario 於 2026-11-03 核准。

## 待確認事項

| 編號 | 事項 | 狀態 | 影響 |
|---|---|---|---|
| TBD-1 | 範例決策 | 待確認 | SCN-001 |

## Timeline

| 日期 | 異動 | 負責人 |
|---|---|---|
| 2026-11-03 | 建立 | - |

---
**建立日期**: 2026-11-03
**分級**: Medium
**風險**: High
**狀態**: 實作中
'''


class BookkeepingTests(unittest.TestCase):
    """issue #2：PASS 後只動記帳區段時沿用，其他變更仍需重審。"""
    CONTRACT = '2.4'
    ISSUE = 'docs/issues/issue-1'

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='kit-bookkeeping-')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        if self.CONTRACT:
            self.write('docs/AGENTS.md', f'**文件版本**: 9.9\n**流程契約**: {self.CONTRACT}\n')
        self.write(f'{self.ISSUE}/README.md', FIXTURE_README)
        self.write(f'{self.ISSUE}/implementation-plan.md', '| S1 | 實作 | ✅ |\n')
        self.write('app.txt', 'v1\n')
        self.commit('approved spec')
        self.approval = self.git('rev-parse', 'HEAD')
        self.write('app.txt', 'v2\n')
        self.commit('implementation')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self, message):
        self.git('add', '-A')
        self.git('commit', '-qm', message)

    def write(self, rel, text):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def edit(self, old, new, rel=None):
        path = self.repo / (rel or f'{self.ISSUE}/README.md')
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def add_report(self, sha=None):
        self.write(self.report, f'- Reviewed HEAD SHA：{sha or self.reviewed}\nPASS\n')

    def record_decision(self):
        self.edit('| TBD-1 | 範例決策 | 待確認 | SCN-001 |',
                  '| TBD-1 | 範例決策 | 已解決 | SCN-001；2026-11-03 使用者「照建議」 |')
        self.edit('| 2026-11-03 | 建立 | - |',
                  '| 2026-11-03 | 建立 | - |\n| 2026-11-03 | 審查 PASS，記錄 TBD-1 | - |')

    def verify(self, *, artifact=True, issue=None, repo=None):
        command = ['python3', str(ROOT / 'skills/review/scripts/verify-artifact.py'),
                   '--repo', str(repo or self.repo), '--reviewed', self.reviewed,
                   '--head', self.git('rev-parse', 'HEAD')]
        if artifact:
            command += ['--artifact', self.report]
        if issue:
            command += ['--issue', issue]
        return subprocess.run(command, capture_output=True, text=True)

    def assertValid(self, result, *mentions):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for mention in mentions:
            self.assertIn(mention, result.stdout)

    def assertInvalid(self, result, *mentions):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        for mention in mentions:
            self.assertIn(mention, result.stderr)

    def assertBookkeepingValid(self, result):
        """新增報告以外還有其他變更的有效案例；流程契約 2.3 以下只允許新增報告，由子類別改判。"""
        self.assertValid(result, '新增報告')

    def derive_baseline(self, ref):
        # Run the literal second command shipped in acceptance.md.
        blocks = (ROOT / 'docs/agents/acceptance.md').read_text().split('```bash\n')
        self.assertGreaterEqual(len(blocks), 3, 'acceptance.md 缺少核准基線推導命令')
        command = blocks[2].split('```', 1)[0]
        result = subprocess.run(['bash', '-c', command], cwd=self.repo,
                                env=dict(os.environ, ref=ref, issue_id='1'),
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def test_baseline_derived_from_approval_source(self):
        self.record_decision()
        self.commit('later bookkeeping without touching approval source')
        self.assertEqual(self.derive_baseline('HEAD'), self.approval)
        self.assertEqual(self.derive_baseline(self.reviewed), self.approval)
        self.edit('使用者回覆「核准」', '使用者回覆「核准」；2026-11-04 重新核准')
        self.commit('re-approval')
        self.assertEqual(self.derive_baseline('HEAD'), self.git('rev-parse', 'HEAD'))
        self.assertEqual(self.derive_baseline(self.reviewed), self.approval)

    def test_baseline_ignores_text_mentioning_approval_source(self):
        self.edit('    Then 看到結果', '    Then 看到未核准的結果')
        self.commit('unapproved spec change')
        self.edit('| 2026-11-03 | 建立 | - |',
                  '| 2026-11-03 | 建立 | - |\n| 2026-11-03 | 補記 `**核准來源**` 的說明 | - |')
        self.commit('timeline mentions the field name')
        self.assertEqual(self.derive_baseline('HEAD'), self.approval)

    def test_baseline_missing_without_approval_source(self):
        self.edit('- **核准來源**: 2026-11-03 使用者回覆「核准」\n', '')
        self.commit('drop approval source')
        # The deleting commit is found too; acceptance.md therefore also requires the line at ref.
        self.assertEqual(self.derive_baseline('HEAD'), self.git('rev-parse', 'HEAD'))
        self.assertNotIn('**核准來源**', self.git('show', 'HEAD:docs/issues/issue-1/README.md'))
        self.write('docs/issues/issue-1/README.md', FIXTURE_README.replace(
            '- **核准來源**: 2026-11-03 使用者回覆「核准」\n', ''))
        self.git('checkout', '-q', '--orphan', 'fresh')
        self.commit('spec without approval source')
        self.assertEqual(self.derive_baseline('HEAD'), '')

    # --- 有效：只動記帳區段 ---

    def test_report_and_bookkeeping_in_one_commit(self):
        self.add_report()
        self.record_decision()
        self.edit('**狀態**: 實作中', '**狀態**: 待合併')
        self.edit('- **核准 commit**: 待提交', f'- **核准 commit**: {self.approval[:7]}')
        self.commit('report and bookkeeping')
        self.assertValid(self.verify(), 'Timeline', '待確認事項', '狀態', '核准 commit',
                         f'待提交 → {self.approval[:7]}')

    def test_bookkeeping_across_several_commits(self):
        self.add_report()
        self.commit('report')
        self.record_decision()
        self.commit('record decision')
        self.edit('- **核准 commit**: 待提交', f'- **核准 commit**: `{self.reviewed}`')
        self.commit('backfill')
        self.assertValid(self.verify(), '核准 commit')

    def test_new_gate_waiver_section_allowed(self):
        self.add_report()
        self.edit('## Timeline', '## Gate 豁免紀錄\n\n- 2026-11-03 使用者：「這次不跑 e2e」\n\n## Timeline')
        self.commit('waiver')
        self.assertValid(self.verify(), 'Gate 豁免紀錄')

    def test_platform_report_mode(self):
        self.record_decision()
        self.commit('record decision')
        self.assertValid(self.verify(artifact=False, issue=self.ISSUE), 'Timeline')

    def test_open_items_section_removed_allowed(self):
        text = (self.repo / self.ISSUE / 'README.md').read_text()
        self.add_report()
        self.edit(text[text.index('## 待確認事項'):text.index('## Timeline')], '')
        self.commit('drop resolved open items')
        self.assertValid(self.verify(), '待確認事項')

    def test_report_only_still_valid(self):
        self.add_report()
        self.commit('report')
        self.assertValid(self.verify())

    # --- 無效：凍結內容、核准 commit 與歷史 ---

    def reviewed_with(self, old, new):
        """把被審查提交換成 README 含非範本寫法的版本。"""
        self.edit(old, new)
        self.commit('reviewed variant')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'

    def test_gherkin_change_invalid(self):
        self.add_report()
        self.edit('    Then 看到結果', '    Then 看到另一個結果')
        self.record_decision()
        self.commit('hide spec change')
        self.assertInvalid(self.verify(), 'Gherkin 驗收劇本')

    def test_small_ac_change_invalid(self):
        self.edit('## Gherkin 驗收劇本', '## 驗收條件\n\n- AC-1: 原本的結果\n\n## Gherkin 驗收劇本')
        self.commit('add AC before review')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
        self.add_report()
        self.edit('- AC-1: 原本的結果', '- AC-1: 改過的結果')
        self.commit('change AC')
        self.assertInvalid(self.verify(), '驗收條件')

    def test_approval_record_change_invalid(self):
        self.add_report()
        self.edit('全部 Scenario 於 2026-11-03 核准。', '全部 Scenario 於 2026-11-04 核准。')
        self.commit('change approval record')
        self.assertInvalid(self.verify(), 'Gherkin 核准紀錄')

    def test_approval_source_change_invalid(self):
        self.add_report()
        self.edit('使用者回覆「核准」', '使用者回覆「照做」')
        self.commit('change approval source')
        self.assertInvalid(self.verify(), '核准來源')

    def test_frozen_field_inside_timeline_invalid(self):
        self.add_report()
        self.edit('**風險**: High', '**風險**: Low')
        self.commit('downgrade risk')
        self.assertInvalid(self.verify(), '風險')

    def test_loose_field_forms_frozen(self):
        cases = (('**風險**: High', '**風險:** High', '**風險:** Low'),
                 ('**分級**: Medium', '- **分級：** Medium', '- **分級：** Small'),
                 ('**風險**: High', '__風險__: High', '__風險__: Low'))
        original = self.reviewed
        for template, before, after in cases:
            with self.subTest(after=after):
                self.git('reset', '-q', '--hard', original)
                self.reviewed_with(template, before)
                self.add_report()
                self.edit(before, after)
                self.commit('loose field change')
                self.assertInvalid(self.verify(), before.strip('-* _:：'))

    def test_loose_heading_in_bookkeeping_invalid(self):
        footer = '---\n**建立日期**'
        for heading in (' ## 驗收條件', '##\t驗收條件', '# 驗收條件', '<h2>驗收條件</h2>',
                        '說明\n驗收條件\n===', '說明\n驗收條件\n----------'):
            with self.subTest(heading=heading):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit(footer, f'{heading}\n- AC-9: 新增未審查條件\n\n{footer}')
                self.commit('loose heading')
                self.assertInvalid(self.verify(), '驗收條件')

    def test_loose_fence_in_bookkeeping_invalid(self):
        footer = '---\n**建立日期**'
        for fence in ('> ```gherkin\n> Scenario: 新增\n> ```',
                      '- 補充\n\n    ```gherkin\n    Scenario: 新增\n    ```'):
            with self.subTest(fence=fence):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit(footer, f'{fence}\n\n{footer}')
                self.commit('loose fence')
                self.assertInvalid(self.verify(), 'code fence')

    def test_bookkeeping_headings_keep_order(self):
        tbd = self.repo / self.ISSUE / 'README.md'
        text = tbd.read_text()
        section = text[text.index('## 待確認事項'):text.index('## Timeline')]
        self.add_report()
        self.edit(section, '')
        self.edit('## 概述', section + '## 概述')
        self.commit('move bookkeeping section')
        self.assertInvalid(self.verify(), '標題')
        self.git('reset', '-q', '--hard', self.reviewed)
        self.add_report()
        self.edit('## 待確認事項', '## Timeline\n\n| 2026-11-03 | 另一段 | - |\n\n## 待確認事項')
        self.commit('duplicate timeline')
        self.assertInvalid(self.verify(), '標題')

    def test_inserted_heading_cannot_swallow_frozen_text(self):
        self.add_report()
        self.edit('## 概述\n', '## 概述\n\n## Timeline\n')
        self.commit('swallow overview')
        self.assertInvalid(self.verify(), '概述')

    # --- issue #3 審查：跨行 HTML 區塊、HTML 標籤與巢狀容器不能藏住或偽造凍結內容 ---

    TIMELINE_ROW = '| 2026-11-03 | 建立 | - |'

    def add_to_timeline(self, extra):
        self.edit(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n\n' + extra + '\n')

    def test_html_block_hiding_frozen_text_invalid(self):
        for opener, closer in (('<!--', '-->'), ('<details><summary>舊規格</summary>', '</details>')):
            for across in (False, True):
                with self.subTest(opener=opener, across=across):
                    self.git('reset', '-q', '--hard', self.reviewed)
                    self.add_report()
                    if across:
                        self.edit('## Gherkin 驗收劇本', f'## Gate 豁免紀錄\n\n{opener}\n\n## Gherkin 驗收劇本')
                        self.add_to_timeline(closer)
                    else:
                        self.add_to_timeline(opener)
                    self.commit('html block hides frozen text')
                    # 跨章節的未關閉註解吞掉其後的標題，訊息報成章節順序不同。
                    self.assertInvalid(self.verify(), '需重新審查' if across and opener == '<!--' else opener)

    def test_html_and_nested_forms_frozen_in_bookkeeping(self):
        cases = (('- - ```gherkin\n  - Scenario: 新增\n- 下一項', 'code fence'),
                 ('1. - ```gherkin\n     Scenario: 新增\n2. 下一項', 'code fence'),
                 ('1. **分級**: Small', '分級'),
                 ('> **分級**: Small', '分級'),
                 ('> ## 驗收條件', '驗收條件'),
                 ('說明 <h2>驗收條件</h2>', '驗收條件'),
                 ('<pre>Scenario: 新增</pre>', '<pre>'),
                 ('<strong>分級</strong>: Small', '分級'),
                 ('<b>風險</b>: Low', '風險'),
                 ('<custom-note>', '<custom-note>'))
        for extra, mention in cases:
            with self.subTest(extra=extra):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.add_to_timeline(extra)
                self.commit('frozen form in timeline')
                self.assertInvalid(self.verify(), mention)

    def test_harmless_html_in_bookkeeping_valid(self):
        self.add_report()
        self.edit(self.TIMELINE_ROW, self.TIMELINE_ROW + '\n| 2026-11-04 | 審查 PASS（review-abc1234.md）<br>補記 | - |')
        self.commit('harmless inline html')
        self.assertValid(self.verify(), 'Timeline')

    # --- review-acd488f：標籤改用允許清單、追蹤多行註解、code span 與跳脫不算標籤 ---

    SPLIT_AND_UNLISTED = (('<details\nclass="note">', '<details'),
                          ('<details ', '<details'),
                          ('補記 <details\nclass="n">', '<details'),
                          ('補記 <details>', '<details>'),
                          ('<script', '<script'),
                          ('<style', '<style'),
                          ('<textarea', '<textarea'),
                          ('<pre', '<pre'),
                          ('補記 <title>', '<title>'),
                          ('補記 <dialog>', '<dialog>'),
                          ('補記 <s>', '<s>'),
                          ('補記 <a href="#x">', '<a href'),
                          ('補記 <small>', '<small>'),
                          ('\\`<details>\\`', '<details>'),
                          ('| 2026-11-04 | `x | <details> | y` | - |', '<details>'),
                          ('補記 `開頭\n結尾` <details> `x`', '<details>'),
                          ('| 2026-11-04 | 單獨的 ` 符號 | - |\n結尾` <details> `x`', '<details>'),
                          ('[spec]: https://example.com/new', '[spec]'),
                          ('- 驗收條件已變更\n  ===', '驗收條件已變更'),
                          ('> 驗收條件已變更\n> ---', '驗收條件已變更'),
                          # review-4d0df5c：記帳章節的行含 `<` 就凍結，只放行行中間的 <br>、<wbr>。
                          ('<br>\n`<details>`', '<br>'),
                          ('<wbr>', '<wbr>'),
                          ('</br>', '</br>'),
                          ('<!-- 說明 --> `<details>`', '<!--'),
                          ('補記 `<details>`', '<details>'),
                          ('補記 `|` <details> `|`', '<details>'),
                          ('補記 \\<details>', '<details>'),
                          ('補記 <https://example.com/x>', '<https'),
                          ('補記 a<b', 'a<b'),
                          ('[spec\n]: https://example.com/new', '[spec'),
                          ('- 驗收條件\n      ===', '驗收條件'),
                          ('1234567890. 驗收條件\n===', '驗收條件'),
                          ('<!-- 開頭\n說明 --> <!--\n- **分級**: Small', '<!--'),
                          # review-4e0177a：清單裡行首的換行標籤、引用裡的連結參照定義。
                          ('- <br>', '<br>'),
                          ('> [spec]: https://example.com/new', '[spec]'),
                          ('- [x foo\n]: https://example.com/new', '[x foo'),
                          ('[!NOTE]: https://example.com/new', '[!NOTE]'),
                          # review-ac2183c：任務清單與行內連結的放行不能涵蓋參照定義。
                          ('[x]: https://example.com/new', '[x]'),
                          ('[a\\](b]: https://example.com/new', '[a\\](b]'))

    def test_split_and_unlisted_html_frozen_in_bookkeeping(self):
        for extra, mention in self.SPLIT_AND_UNLISTED:
            with self.subTest(extra=extra):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.add_to_timeline(extra)
                self.commit('split or unlisted html in timeline')
                self.assertInvalid(self.verify(), mention)

    MULTILINE_COMMENT = '<!--\n舊的決策說明\n-->'

    def test_multiline_comment_frozen_until_close(self):
        original = self.reviewed
        changes = (('刪除結尾', lambda: self.edit('舊的決策說明\n-->\n', '舊的決策說明\n')),
                   ('搬移結尾', lambda: (self.edit('舊的決策說明\n-->\n', '舊的決策說明\n'),
                                       self.edit(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n-->\n'))),
                   ('改註解內容', lambda: self.edit('舊的決策說明', '新的決策說明')))
        for name, change in changes:
            with self.subTest(change=name):
                self.git('reset', '-q', '--hard', original)
                self.reviewed_with('| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n',
                                   '| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n\n' + self.MULTILINE_COMMENT + '\n')
                self.add_report()
                change()
                self.commit('touch multiline comment')
                # 少了結尾的註解吞掉 Timeline 標題，訊息報成章節順序不同。
                self.assertInvalid(self.verify(), '需重新審查' if name != '改註解內容' else '決策說明')

    def test_multiline_comment_kept_bookkeeping_valid(self):
        self.reviewed_with('| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n',
                           '| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n\n' + self.MULTILINE_COMMENT + '\n')
        self.add_report()
        self.record_decision()
        self.commit('bookkeeping next to multiline comment')
        self.assertValid(self.verify(), 'Timeline')

    def test_invisible_line_breaks_and_spaces_in_frozen_lines_invalid(self):
        # CommonMark 只以 \n、\r 分行、只把空格與 tab 當空白；NBSP、U+2028、U+0085 不能讓凍結內容換行或關閉 fence。
        cases = (('    Then 看到結果\n```\n', '    Then 看到結果\n```\u00a0\n'),
                 ('## Gherkin 核准紀錄', '\u2028## Gherkin 核准紀錄'),
                 ('全部 Scenario 於 2026-11-03 核准。', '全部 Scenario 於 2026-11-03 核准。\u0085## Gate 豁免紀錄\u0085- 補記'),
                 ('全部 Scenario 於 2026-11-03 核准。', '全部 Scenario 於 2026-11-03 核准。\u2028## Gate 豁免紀錄\u2028- 補記'))
        for old, new in cases:
            with self.subTest(new=new):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit(old, new)
                self.commit('invisible characters in frozen text')
                self.assertInvalid(self.verify(), '需重新審查')

    def test_blank_line_removed_in_frozen_section_invalid(self):
        self.reviewed_with('固定的範例需求。\n', '固定的範例需求。\n\n<div id="b"></div>\n\n補充說明\n')
        self.add_report()
        self.edit('<div id="b"></div>\n\n補充說明', '<div id="b"></div>\n補充說明')
        self.commit('drop blank line in frozen section')
        self.assertInvalid(self.verify(), '空行')

    def test_comment_reopened_after_close_stays_frozen(self):
        self.reviewed_with('| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n',
                           '| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n\n<!-- 開頭\n說明 --> <!--\n舊的說明\n-->\n')
        self.add_report()
        self.edit('舊的說明', '新的說明')
        self.commit('edit text inside reopened comment')
        self.assertInvalid(self.verify(), '說明')

    def test_html_block_closer_without_lt_stays_frozen(self):
        # 處理指令、宣告與 CDATA 的結束字串不含 `<`，跨空行的結束行也要凍結（review-73202f8）。
        base = self.reviewed
        for opener, closer in (('<?php', '?>'), ('<!DOCTYPE x', '>'), ('<![CDATA[', ']]>'), ('<!--', '-->')):
            with self.subTest(opener=opener):
                self.git('reset', '-q', '--hard', base)
                self.reviewed_with(self.TIMELINE_ROW + '\n', f'{self.TIMELINE_ROW}\n\n{opener}\n\n說明 {closer}\n')
                self.add_report()
                self.edit(f'說明 {closer}', '說明')
                self.commit('drop html block closer')
                self.assertInvalid(self.verify(), '說明')

    def test_unclosed_opener_in_frozen_section_named_in_message(self):
        # 凍結章節沒有關閉的 `<?`、`<!` 接字母讓之後全部凍結；錯誤訊息要指出開頭所在的行（review-c6eb117）。
        self.reviewed_with('固定的範例需求。\n', '固定的範例需求。用 `<?php` 開頭。\n')
        self.add_report()
        self.add_to_timeline('| 2026-11-04 | 補記 | - |')
        self.commit('bookkeeping after unclosed opener')
        self.assertInvalid(self.verify(), '固定的範例需求。用 `<?php` 開頭。', '未關閉')

    def test_comment_and_processing_closed_on_same_line(self):
        # `<!-->`、`<!--->`、`<?>` 在 CommonMark 同一行就關閉，之後照常判定。
        base = self.reviewed
        for opener in ('<!-->', '<!--->', '<?>'):
            with self.subTest(opener=opener):
                self.git('reset', '-q', '--hard', base)
                self.reviewed_with('固定的範例需求。\n', f'固定的範例需求。`{opener}` 範例。\n')
                self.add_report()
                self.add_to_timeline('| 2026-11-04 | 補記 | - |')
                self.commit('bookkeeping after closed opener')
                self.assertBookkeepingValid(self.verify())

    def test_reopened_block_across_blank_lines_stays_frozen(self):
        # 同一行關閉後又開新的，跨空行的內容靠追蹤凍結，不靠段落凍結。
        base = self.reviewed
        for opener, closer in (('<!--', '-->'), ('<?x', '?>')):
            with self.subTest(opener=opener):
                self.git('reset', '-q', '--hard', base)
                self.reviewed_with(self.TIMELINE_ROW + '\n',
                                   f'{self.TIMELINE_ROW}\n\n{opener} 開頭 {closer} {opener}\n\n舊的說明\n\n{closer}\n')
                self.add_report()
                self.edit('舊的說明', '新的說明')
                self.commit('edit text inside reopened block')
                self.assertInvalid(self.verify(), '說明')

    def test_inline_span_across_frozen_paragraph_invalid(self):
        # 連結 title、圖片 alt、code span 可以跨行，記帳行能把檔尾 metadata 包進去（review-ac2183c）。
        for opener, closer in (('[補記](https://example.com/x "', '")'), ('![圖', '](https://example.com/a.png)'),
                               ('補記 `', '`')):
            with self.subTest(opener=opener):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.add_to_timeline(opener)
                path = self.repo / f'{self.ISSUE}/README.md'
                path.write_text(path.read_text() + closer + '\n')
                self.commit('inline span swallowing metadata')
                self.assertInvalid(self.verify(), '同一段落')

    def test_backtick_before_frozen_code_span_invalid(self):
        self.reviewed_with(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n\n用 `<details>` 收合舊說明。\n')
        self.add_report()
        self.edit('用 `<details>`', '補記 `\n用 `<details>`')
        self.commit('lone backtick before frozen code span')
        self.assertInvalid(self.verify(), '<details>')

    def test_blank_line_after_frozen_html_in_bookkeeping_invalid(self):
        self.reviewed_with(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n\n<div id="x"></div>\n')
        self.add_report()
        self.edit('<div id="x"></div>\n\n', '<div id="x"></div>\n')
        self.commit('drop blank line after html block')
        self.assertInvalid(self.verify(), '段落結尾')

    def test_append_to_paragraph_with_frozen_line(self):
        self.reviewed_with(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n\n- **補充**：舊說明\n- 第二項\n')
        for extra, valid in (('- 第二項\n- 第三項', False), ('- 第二項\n\n- 第三項', True)):
            with self.subTest(valid=valid):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit('- 第二項', extra)
                self.commit('append after frozen bold line')
                if valid:
                    self.assertBookkeepingValid(self.verify())
                else:
                    self.assertInvalid(self.verify(), '同一段落')

    def test_rows_after_frozen_table_row_valid(self):
        # 表格每一列各自解析行內語法：含 `<` 的列凍結，同一張表的其他列照常記帳。
        frozen_row = '| 2026-11-04 | 改用 `<details>` | - |'
        self.reviewed_with(self.TIMELINE_ROW + '\n', f'{self.TIMELINE_ROW}\n{frozen_row}\n')
        self.add_report()
        self.edit(frozen_row, frozen_row + '\n| 2026-11-05 | 補記 | - |')
        self.commit('append row after frozen row')
        self.assertBookkeepingValid(self.verify())
        # 刪掉分隔列，表格變成段落，含 `<` 的列與其他列合成一段，判需重審。
        self.edit('| 日期 | 異動 | 負責人 |\n|---|---|---|\n', '| 日期 | 異動 | 負責人 |\n')
        self.commit('drop delimiter row')
        self.assertInvalid(self.verify(), '同一段落')

    def test_table_head_frozen_with_frozen_row(self):
        # 表頭與分隔列決定凍結列渲染幾欄、是不是表格（review-20d0847）。
        frozen_row = '| 2026-11-04 | 改用 `<details>` | - |'
        head = '| 日期 | 異動 | 負責人 |\n|---|---|---|'
        self.reviewed_with(self.TIMELINE_ROW + '\n', f'{self.TIMELINE_ROW}\n{frozen_row}\n')
        for new_head in ('|| 日期 | 異動 | 負責人 |\n|---|---|---|', '| 日期 | 異動 |\n|---|---|',
                         '| 日期 | 異動 | 負責人 ||\n|---|---|---|', '| 日期 | 異動 | 負責人 |\n|:---|---|---|'):
            with self.subTest(head=new_head):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit(head, new_head)
                self.edit(frozen_row, '| 2026-11-03 | 補記 ` | - |\n' + frozen_row)
                self.commit('change table head')
                self.assertInvalid(self.verify(), '需重新審查')

    def test_rows_without_gfm_table_freeze_as_paragraph(self):
        # 欄數照 GFM 算（頭尾各去一個 `|`，含 `\|` 不當表格），不是表格或表格緊接在段落後時照段落處理。
        frozen_row = '| 2026-11-04 | 改用 `<details>` | - |'
        head = '| 日期 | 異動 | 負責人 |\n|---|---|---|'
        base = self.reviewed
        for old, new in ((head, '|| 日期 | 異動 | 負責人 |\n|---|---|---|'),
                         (head, '| 日期 | 異動 | 負責人 ||\n|---|---|---|'),
                         (head, '| 日期 \\| 異動 | 負責人 |\n|---|---|---|'),
                         (head, '| 日期 | 異動 | 負責人 |\n|---|---|'),
                         (head, '| 日期 | 異動 | 負責人\n|---|---|---|'),
                         ('## Timeline\n\n' + head, '## Timeline\n\n說明 `<x>`\n' + head)):
            with self.subTest(head=new):
                self.git('reset', '-q', '--hard', base)
                self.edit(self.TIMELINE_ROW + '\n', f'{self.TIMELINE_ROW}\n{frozen_row}\n')
                self.edit(old, new)
                self.commit('reviewed variant')
                self.reviewed = self.git('rev-parse', 'HEAD')
                self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
                self.add_report()
                self.edit(frozen_row, frozen_row + '\n| 2026-11-05 | 補記 | - |')
                self.commit('append row')
                self.assertInvalid(self.verify(), '同一段落')

    def test_fake_table_before_frozen_paragraph_invalid(self):
        # 渲染器不當表格的寫法要和後面的段落一起比對（review-4d7ba1f）：只有一個 `|` 的表頭、tab、U+2028、空白格。
        frozen = '用 `<details>` 收合舊說明。'
        self.reviewed_with(self.TIMELINE_ROW + '\n', f'{self.TIMELINE_ROW}\n\n{frozen}\n')
        for fake in ('|\n|-|', '| 補記 |\n|\t-|', '| 補記\u2028|\n|-|', '|  |\n|-|', '補記 |\n-|'):
            with self.subTest(fake=fake):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit(f'\n\n{frozen}', f'\n\n{fake}\n| ` |\n{frozen}')
                self.commit('fake table joined to frozen paragraph')
                self.assertInvalid(self.verify(), '同一段落')

    def test_blank_line_before_frozen_paragraph_compared(self):
        # 表格後的空行決定凍結段落是不是表格的一列（issue #5 的 V3）：刪掉或補上空行都判需重審，
        # 範本的 `---` 檔尾雖然渲染相同，也不另外辨認。
        frozen = '用 `<details>` 收合舊說明。'
        footer = '\n\n---\n**建立日期**'
        cases = ((f'{self.TIMELINE_ROW}\n\n{frozen}\n', f'{self.TIMELINE_ROW}\n{frozen}\n'),
                 (f'{self.TIMELINE_ROW}\n{frozen}\n', f'{self.TIMELINE_ROW}\n\n{frozen}\n'),
                 (None, (footer, '\n---\n**建立日期**')))
        base = self.reviewed
        for reviewed, change in cases:
            with self.subTest(change=change):
                self.git('reset', '-q', '--hard', base)
                self.reviewed = base
                if reviewed:
                    self.reviewed_with(self.TIMELINE_ROW + '\n', reviewed)
                    change = (reviewed, change)
                else:
                    self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
                self.add_report()
                self.edit(*change)
                self.commit('blank line before frozen paragraph')
                self.assertInvalid(self.verify(), '前接')

    def test_start_message_names_paragraph(self):
        # 同章節有兩段凍結段落時，錯誤訊息要指出是哪一段（review-8d4f21a MUST FIX 1）。
        first, second = '用 `<a>` 標記第一段。', '用 `<b>` 標記第二段。'
        self.reviewed_with(self.TIMELINE_ROW + '\n', f'{self.TIMELINE_ROW}\n\n{first}\n\n| 補 | 記 | - |\n|---|---|---|\n| x | y | - |\n\n{second}\n')
        self.add_report()
        self.edit(f'| x | y | - |\n\n{second}', f'| x | y | - |\n{second}')
        self.commit('drop blank line before second paragraph')
        self.assertInvalid(self.verify(), '前接', second)

    def test_table_head_frozen_when_paragraph_follows_row(self):
        # 表格後面不空行的凍結段落渲染成表格的一列，表頭決定它顯示幾欄（review-8d4f21a SHOULD FIX 1）。
        head = '| 日期 | 異動 | 負責人 |\n|---|---|---|'
        self.reviewed_with(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n**風險**: a | b | c\n')
        self.add_report()
        self.edit(head, '| 日期 |\n|---|')
        self.commit('shrink table head')
        self.assertInvalid(self.verify(), '表頭')

    # --- 待確認事項狀態的提醒（issue #7）：只提醒，不改判定 ---

    TBD_ROW = '| TBD-1 | 範例決策 | 待確認 | SCN-001 |'

    def assertNoReminder(self, result):
        self.assertNotIn('提醒', result.stdout + result.stderr)

    def test_tbd_changed_row_invalid_status_reminded(self):
        self.add_report()
        self.edit(self.TBD_ROW, '| TBD-1 | 範例決策 | 接受為殘餘風險 | SCN-001 |')
        self.commit('nonstandard status')
        result = self.verify()
        self.assertBookkeepingValid(result)
        for mention in ('提醒', 'TBD-1', '接受為殘餘風險', '不影響本次判定'):
            self.assertIn(mention, result.stdout)

    def test_tbd_added_row_invalid_status_reminded(self):
        self.add_report()
        self.edit(self.TBD_ROW, self.TBD_ROW + '\n| TBD-2 | 新事項 | 已確認：照建議 | SCN-001 |')
        self.commit('new nonstandard row')
        result = self.verify()
        self.assertBookkeepingValid(result)
        self.assertIn('TBD-2', result.stdout)
        self.assertNotIn('TBD-1', result.stdout.split('提醒', 1)[-1])

    def test_tbd_formatted_standard_status_not_reminded(self):
        self.add_report()
        self.edit(self.TBD_ROW, '| TBD-1 | 範例決策 | ✅ **已解決**（2026-11-12）：照建議 | SCN-001 |')
        self.commit('formatted standard status')
        result = self.verify()
        self.assertBookkeepingValid(result)
        self.assertNoReminder(result)

    def test_tbd_unchanged_old_invalid_row_not_reminded(self):
        self.reviewed_with(self.TBD_ROW, '| TBD-1 | 範例決策 | 已定案 | SCN-001 |')
        self.add_report()
        self.edit(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n| 2026-11-12 | 補記 | - |\n')
        self.commit('timeline only')
        result = self.verify()
        self.assertBookkeepingValid(result)
        self.assertNoReminder(result)

    def test_tbd_reminder_kept_when_invalid(self):
        self.add_report()
        self.edit(self.TBD_ROW, '| TBD-1 | 範例決策 | 已定案 | SCN-001 |')
        self.write('app.txt', 'v3\n')
        self.commit('code change and nonstandard status')
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('INVALID', result.stderr)
        self.assertIn('TBD-1', result.stdout)

    def test_tbd_escaped_pipe_before_status_not_reminded(self):
        # review-a77b097 NICE TO HAVE 1：跳脫的直線符號不切欄。
        self.add_report()
        self.edit(self.TBD_ROW, '| TBD-1 | 範例 a \\| b | 已解決：照建議 | SCN-001 |')
        self.commit('escaped pipe in item')
        self.assertNoReminder(self.verify())

    def test_tbd_struck_or_bracketed_status_reminded(self):
        # review-a77b097 NICE TO HAVE 2：只去掉粗體、反引號、空白與 ✅ 這類圖示，刪除線與括號不去。
        for status in ('~~待確認~~ 已定案', '（待確認）已定案', '[已解決](x)'):
            with self.subTest(status=status):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.add_report()
                self.edit(self.TBD_ROW, f'| TBD-1 | 範例決策 | {status} | SCN-001 |')
                self.commit('struck status')
                self.assertIn('TBD-1', self.verify().stdout)

    def test_tbd_table_without_status_column_not_reminded(self):
        self.reviewed_with('| 編號 | 事項 | 狀態 | 影響 |\n|---|---|---|---|\n' + self.TBD_ROW,
                           '| 編號 | 事項 | 結論 | 影響 |\n|---|---|---|---|\n' + self.TBD_ROW)
        self.add_report()
        self.edit(self.TBD_ROW, '| TBD-1 | 範例決策 | 已定案 | SCN-001 |')
        self.commit('table without status column')
        result = self.verify()
        self.assertBookkeepingValid(result)
        self.assertNoReminder(result)

    def test_row_appended_before_template_footer_valid(self):
        self.add_report()
        self.edit(self.TIMELINE_ROW + '\n', self.TIMELINE_ROW + '\n| 2026-11-05 | 補記 | - |\n')
        self.commit('append row before footer')
        self.assertBookkeepingValid(self.verify())

    def test_extra_blank_line_in_frozen_section_valid(self):
        # 連續空行渲染相同，合併後比對（review-ac2183c SHOULD FIX 1）。
        self.add_report()
        self.edit('固定的範例需求。\n', '固定的範例需求。\n\n')
        self.commit('extra blank line')
        self.assertBookkeepingValid(self.verify())

    def test_alert_and_link_lines_in_bookkeeping_valid(self):
        self.add_report()
        self.add_to_timeline('> [!NOTE]\n> 補記\n\n- [#4](https://example.com/4) 另開 issue\n- [x]\n- [ ] 待辦')
        self.commit('alert and link lines')
        self.assertValid(self.verify(), 'Timeline')

    def test_safe_html_mentions_in_bookkeeping_valid(self):
        self.add_report()
        rows = ('| 2026-11-04 | 修正 template 元素的生命週期，改用 table 呈現；`x > y` 比較 | - |',
                '| 2026-11-04 | 換行<br/>與<wbr>斷行，<BR >補記 | - |',
                '| 2026-11-04 | 查證 `curl -s https://example.invalid \\| grep -c title` | - |')
        self.edit(self.TIMELINE_ROW, '\n'.join((self.TIMELINE_ROW,) + rows))
        self.add_to_timeline('- [x] 2026-11-04 補記，見 https://example.com/x\n\n---')
        self.commit('safe mentions')
        self.assertValid(self.verify(), 'Timeline')

    def test_current_state_note_only_when_relevant(self):
        self.add_current_state('review-0000000.md')
        self.commit('reviewed with current state')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
        self.add_report()
        self.edit('    Then 看到結果', '    Then 看到其他結果')
        self.commit('gherkin change')
        result = self.verify()
        self.assertInvalid(result, 'Gherkin')
        self.assertNotIn('2.5', result.stderr)

    def test_gherkin_moved_under_timeline_invalid(self):
        text = (self.repo / self.ISSUE / 'README.md').read_text()
        block = text[text.index('```gherkin'):text.index('```\n', text.index('```gherkin') + 3) + 4]
        self.add_report()
        self.edit(block, '')
        self.edit('---\n**建立日期**', block + '\n---\n**建立日期**')
        self.commit('move gherkin')
        self.assertInvalid(self.verify(), 'Gherkin 驗收劇本')

    def test_code_fence_in_timeline_invalid(self):
        self.add_report()
        self.edit('---\n**建立日期**',
                  '```gherkin\n  Scenario: 新增\n    Then 未審查\n```\n\n---\n**建立日期**')
        self.commit('fence in timeline')
        self.assertInvalid(self.verify(), 'code fence')

    def test_other_paths_invalid(self):
        for rel in (f'{self.ISSUE}/implementation-plan.md', f'{self.ISSUE}/evidence/s1.txt',
                    'docs/issues/issue-2/README.md', 'app.txt'):
            with self.subTest(rel=rel):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.git('clean', '-qfd')
                self.add_report()
                self.write(rel, 'changed after PASS\n')
                self.commit('extra change')
                self.assertInvalid(self.verify(), rel)

    def test_report_rewritten_after_added_invalid(self):
        self.add_report()
        self.commit('report')
        self.write(self.report, f'- Reviewed HEAD SHA：{self.reviewed}\nFORGED PASS\n')
        self.commit('rewrite report')
        self.assertInvalid(self.verify(), self.report)

    def test_existing_report_modified_invalid(self):
        old = f'{self.ISSUE}/review-0000000.md'
        self.git('reset', '-q', '--hard', self.approval)
        self.write(old, '- Reviewed HEAD SHA：0000000\nRETURN TO execute-task\n')
        self.write('app.txt', 'v2\n')
        self.commit('implementation with old report')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
        self.add_report()
        self.write(old, '- Reviewed HEAD SHA：0000000\nPASS\n')
        self.commit('rewrite old report')
        self.assertInvalid(self.verify(), old)

    def test_approval_sha_replaced_invalid(self):
        self.git('reset', '-q', '--hard', self.approval)
        self.edit('- **核准 commit**: 待提交', f'- **核准 commit**: {self.approval[:7]}')
        self.write('app.txt', 'v2\n')
        self.commit('implementation with backfill')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
        self.add_report()
        self.edit(f'- **核准 commit**: {self.approval[:7]}', f'- **核准 commit**: {self.reviewed[:7]}')
        self.commit('repoint approval')
        self.assertInvalid(self.verify(), '核准 commit')

    def test_approval_backfill_must_be_ancestor(self):
        orphan = self.git('commit-tree', f'{self.approval}^{{tree}}', '-m', 'orphan')
        for value in (orphan, 'deadbeef', '尚未決定', f'{self.approval[:7]} 另外把 SCN-001 改為不需測試'):
            with self.subTest(value=value):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.git('clean', '-qfd')
                self.add_report()
                self.edit('- **核准 commit**: 待提交', f'- **核准 commit**: {value}')
                self.commit('bad backfill')
                self.assertInvalid(self.verify(), '核准 commit')

    def test_platform_mode_rejects_semantic_change(self):
        self.edit('    Then 看到結果', '    Then 看到另一個結果')
        self.record_decision()
        self.commit('hide spec change')
        self.assertInvalid(self.verify(artifact=False, issue=self.ISSUE), 'Gherkin 驗收劇本')
        self.git('reset', '-q', '--hard', self.reviewed)
        self.git('config', 'diff.relative', 'true')
        self.record_decision()
        self.write('app.txt', 'v3\n')
        self.commit('code change seen from a subdirectory')
        (self.repo / 'lib').mkdir()
        self.assertInvalid(self.verify(artifact=False, issue=self.ISSUE, repo=self.repo / 'lib'), 'app.txt')

    def test_future_major_contract_uses_legacy_rule(self):
        self.write('docs/AGENTS.md', '**文件版本**: 9.9\n**流程契約**: 3.0\n')
        self.commit('contract 3.0')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'
        self.add_report()
        self.record_decision()
        self.commit('report and bookkeeping')
        self.assertInvalid(self.verify(), '2.4')

    def test_merge_in_range_invalid(self):
        self.git('switch', '-q', '-c', 'side')
        self.record_decision()
        self.commit('side bookkeeping')
        self.git('switch', '-q', 'main')
        self.add_report()
        self.commit('report')
        self.git('merge', '-q', '--no-ff', '-m', 'merge side', 'side')
        self.assertInvalid(self.verify(), 'merge')

    def test_reviewed_not_ancestor_invalid(self):
        self.git('reset', '-q', '--hard', self.approval)
        self.write('app.txt', 'v2 rebased\n')
        self.commit('rewritten implementation')
        self.add_report()
        self.commit('report')
        self.assertInvalid(self.verify(), '祖先')

    def test_bad_report_invalid(self):
        self.add_report(sha=self.approval)
        self.commit('wrong sha')
        self.assertInvalid(self.verify(), 'Reviewed HEAD SHA')
        self.git('reset', '-q', '--hard', self.reviewed)
        (self.repo / self.report).symlink_to('README.md')
        self.commit('symlink')
        self.assertInvalid(self.verify(), 'symlink')

    # --- issue #3：## 現況 只在流程契約 2.5 起列入記帳區段 ---

    def add_current_state(self, body=None):
        self.edit('## Gherkin 驗收劇本', current_state(body or self.report.rsplit('/', 1)[1])
                  + '## Gherkin 驗收劇本')

    def test_current_state_section_needs_25(self):
        self.add_report()
        self.add_current_state()
        self.commit('report and current state')
        self.assertInvalid(self.verify(), '現況', '2.5')


def current_state(review, row='| 併入 main | `git merge-base --is-ancestor HEAD main` | 否 | 2026-11-10 |'):
    return ('## 現況\n\n'
            f'**現行 review**: {review}\n\n'
            '| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |\n'
            '|---|---|---|---|\n'
            f'{row}\n\n')


class CurrentStateTests(BookkeepingTests):
    """issue #3：流程契約 2.5 起 ## 現況 可整節增刪、節內可改；夾帶凍結內容仍需重審。"""
    CONTRACT = '2.5'
    OLD_ROW = '| 併入 main | `git merge-base --is-ancestor HEAD main` | 否 | 2026-11-10 |'
    NEW_ROW = '| 併入 main | `git merge-base --is-ancestor HEAD main` | 是 | 2026-11-12 |'

    def reviewed_with_current_state(self):
        """被審查版本已含 ## 現況，指向上一份報告。"""
        self.add_current_state('review-0000000.md')
        self.commit('reviewed with current state')
        self.reviewed = self.git('rev-parse', 'HEAD')
        self.report = f'{self.ISSUE}/review-{self.reviewed[:7]}.md'

    # --- 有效 ---

    def test_current_state_section_needs_25(self):
        self.add_report()
        self.add_current_state()
        self.commit('report and current state')
        self.assertValid(self.verify(), '現況', f'現行 review（（無） → review-{self.reviewed[:7]}.md）')

    def test_current_state_values_updated(self):
        self.reviewed_with_current_state()
        self.add_report()
        self.edit('**現行 review**: review-0000000.md', f'**現行 review**: review-{self.reviewed[:7]}.md')
        self.edit(self.OLD_ROW, self.NEW_ROW)
        self.commit('update current state')
        self.assertValid(self.verify(), '現況', 'review-0000000.md → ')

    def test_current_review_platform_link_forms(self):
        """平台連結寫成一般網址或 Markdown 連結；`<https://…>` 含 `<`，照記帳章節的規則凍結。"""
        original = self.reviewed
        for value, valid in (('https://example.com/o/r/pull/1#pullrequestreview-1', True),
                             ('[PR 審查](https://example.com/o/r/pull/1#pullrequestreview-1)', True),
                             ('<https://example.com/o/r/pull/1#pullrequestreview-1>', False)):
            with self.subTest(value=value):
                self.reset_to(original)
                self.reviewed_with_current_state()
                self.edit('**現行 review**: review-0000000.md', f'**現行 review**: {value}')
                self.commit('platform review link')
                result = self.verify(artifact=False, issue=self.ISSUE)
                if valid:
                    self.assertValid(result, '現行 review')
                else:
                    self.assertInvalid(result, '<https')

    def test_current_state_row_only(self):
        self.reviewed_with_current_state()
        self.edit(self.OLD_ROW, self.NEW_ROW)
        self.commit('recheck external state')
        self.assertValid(self.verify(artifact=False, issue=self.ISSUE), '現況')

    def test_current_state_removed(self):
        self.reviewed_with_current_state()
        self.add_report()
        self.edit(current_state('review-0000000.md'), '')
        self.commit('drop current state')
        self.assertValid(self.verify(), '現況')

    def test_current_state_with_other_bookkeeping(self):
        self.add_report()
        self.add_current_state()
        self.record_decision()
        self.edit('**狀態**: 實作中', '**狀態**: 待合併')
        self.commit('report, current state and decision')
        self.assertValid(self.verify(), '現況', 'Timeline', '待確認事項', '狀態')

    # --- 無效 ---

    def test_frozen_forms_inside_current_state_invalid(self):
        cases = (('### 補充', '補充'),
                 ('```text\nAC-9 新增\n```', 'code fence'),
                 ('**分級**: Small', '分級'),
                 ('**現行 review:** review-1111111.md', '現行 review'),
                 ('**現行 review**: review-1111111.md', '現行 review'),
                 # 未關閉的註解吞掉其後的標題，訊息報成章節順序不同。
                 ('<!--', '需重新審查'),
                 ('<details><summary>舊規格</summary>', '<details>'),
                 # 未關閉的巢狀 fence 會吞到下一個 fence，訊息因此報成章節順序不同。
                 ('- - ```gherkin\n  - Scenario: 新增\n- 下一項', '需重新審查'),
                 ('1. **分級**: Small', '分級'),
                 ('> **分級**: Small', '分級'),
                 ('<pre>AC-9</pre>', '<pre>'),
                 ('<details\nclass="note">', '<details'),
                 ('<script', '<script'),
                 ('補記 <s>', '<s>'),
                 ('[spec]: https://example.com/new', '[spec]'),
                 ('- 驗收條件已變更\n  ===', '驗收條件已變更'),
                 ('<br>\n`<details>`', '<br>'),
                 ('補記 `|` <details> `|`', '<details>'))
        original = self.reviewed
        for extra, mention in cases:
            with self.subTest(extra=extra, mode='整節新增'):
                self.reset_to(original)
                self.add_report()
                self.add_current_state()
                self.edit(self.OLD_ROW + '\n', self.OLD_ROW + '\n\n' + extra + '\n')
                self.commit('new current state with frozen form')
                self.assertInvalid(self.verify(), mention)
            with self.subTest(extra=extra, mode='既有現況'):
                self.reset_to(original)
                self.reviewed_with_current_state()
                self.add_report()
                self.edit(self.OLD_ROW + '\n', self.OLD_ROW + '\n\n' + extra + '\n')
                self.commit('frozen form inside existing current state')
                self.assertInvalid(self.verify(), mention)

    def reset_to(self, sha):
        self.git('reset', '-q', '--hard', sha)
        self.reviewed = sha
        self.report = f'{self.ISSUE}/review-{sha[:7]}.md'

    def test_frozen_text_moved_into_current_state_invalid(self):
        self.reviewed_with_current_state()
        self.add_report()
        self.edit('固定的範例需求。\n', '')
        self.edit(self.OLD_ROW + '\n', self.OLD_ROW + '\n\n固定的範例需求。\n')
        self.commit('move overview into current state')
        self.assertInvalid(self.verify(), '概述')

    def test_inserted_current_state_cannot_swallow_frozen_text(self):
        self.add_report()
        self.edit('## 概述\n', '## 概述\n\n## 現況\n')
        self.commit('swallow overview into current state')
        self.assertInvalid(self.verify(), '概述')

    def test_duplicate_current_state_invalid(self):
        self.add_report()
        self.add_current_state()
        self.add_current_state()
        self.commit('two current state sections')
        self.assertInvalid(self.verify(), '標題')

    def test_current_review_outside_section_invalid(self):
        footer = '---\n**建立日期**'
        self.add_report()
        self.edit(footer, f'**現行 review**: review-{self.reviewed[:7]}.md\n\n{footer}')
        self.commit('current review outside current state')
        self.assertInvalid(self.verify(), '現行 review')
        self.reset_to(self.approval)
        self.write('app.txt', 'v2\n')
        self.edit(footer, f'**現行 review**: review-0000000.md\n\n{footer}')
        self.commit('reviewed with current review outside current state')
        self.reset_to(self.git('rev-parse', 'HEAD'))
        self.add_report()
        self.edit('**現行 review**: review-0000000.md', f'**現行 review**: review-{self.reviewed[:7]}.md')
        self.commit('change current review outside current state')
        self.assertInvalid(self.verify(), '現行 review')


class LegacyBookkeepingTests(BookkeepingTests):
    """流程契約 2.3：維持只新增報告的現行判定；無效時不承諾指出違規位置。"""
    CONTRACT = '2.3'

    def assertInvalid(self, result, *mentions):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def assertNeeds24(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('2.4', result.stderr)

    def assertBookkeepingValid(self, result):
        self.assertNeeds24(result)

    def test_report_and_bookkeeping_in_one_commit(self):
        self.add_report()
        self.record_decision()
        self.commit('report and bookkeeping')
        self.assertNeeds24(self.verify())

    def test_bookkeeping_across_several_commits(self):
        self.add_report()
        self.commit('report')
        self.record_decision()
        self.commit('record decision')
        self.assertNeeds24(self.verify())

    def test_new_gate_waiver_section_allowed(self):
        self.add_report()
        self.edit('## Timeline', '## Gate 豁免紀錄\n\n- 2026-11-03 使用者：「這次不跑 e2e」\n\n## Timeline')
        self.commit('waiver')
        self.assertNeeds24(self.verify())

    def test_platform_report_mode(self):
        self.record_decision()
        self.commit('record decision')
        self.assertNeeds24(self.verify(artifact=False, issue=self.ISSUE))

    def test_open_items_section_removed_allowed(self):
        text = (self.repo / self.ISSUE / 'README.md').read_text()
        self.add_report()
        self.edit(text[text.index('## 待確認事項'):text.index('## Timeline')], '')
        self.commit('drop resolved open items')
        self.assertNeeds24(self.verify())

    def test_harmless_html_in_bookkeeping_valid(self):
        self.add_report()
        self.edit(self.TIMELINE_ROW, self.TIMELINE_ROW + '\n| 2026-11-04 | 審查 PASS<br>補記 <!-- 備註 --> | - |')
        self.commit('harmless inline html')
        self.assertNeeds24(self.verify())

    def test_multiline_comment_kept_bookkeeping_valid(self):
        self.reviewed_with('| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n',
                           '| TBD-1 | 範例決策 | 待確認 | SCN-001 |\n\n' + self.MULTILINE_COMMENT + '\n')
        self.add_report()
        self.record_decision()
        self.commit('bookkeeping next to multiline comment')
        self.assertNeeds24(self.verify())

    def test_alert_and_link_lines_in_bookkeeping_valid(self):
        self.add_report()
        self.add_to_timeline('> [!NOTE]\n> 補記')
        self.commit('alert line')
        self.assertNeeds24(self.verify())

    def test_safe_html_mentions_in_bookkeeping_valid(self):
        self.add_report()
        self.edit(self.TIMELINE_ROW, self.TIMELINE_ROW + '\n| 2026-11-04 | 修正 template 元素 | - |')
        self.commit('safe mentions')
        self.assertNeeds24(self.verify())


class NoContractBookkeepingTests(LegacyBookkeepingTests):
    """讀不到 docs/AGENTS.md：同樣維持現行判定。"""
    CONTRACT = None


if __name__ == '__main__':
    unittest.main()
