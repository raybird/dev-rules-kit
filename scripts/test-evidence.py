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

    def verify(self, *, artifact=True, issue=None):
        command = ['python3', str(ROOT / 'skills/review/scripts/verify-artifact.py'),
                   '--repo', str(self.repo), '--reviewed', self.reviewed,
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

    def test_report_only_still_valid(self):
        self.add_report()
        self.commit('report')
        self.assertValid(self.verify())

    # --- 無效：凍結內容、核准 commit 與歷史 ---

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

    def test_inserted_heading_cannot_swallow_frozen_text(self):
        self.add_report()
        self.edit('## 概述\n', '## 概述\n\n## Timeline\n')
        self.commit('swallow overview')
        self.assertInvalid(self.verify(), '概述')

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
        for value in (orphan, 'deadbeef', '尚未決定'):
            with self.subTest(value=value):
                self.git('reset', '-q', '--hard', self.reviewed)
                self.git('clean', '-qfd')
                self.add_report()
                self.edit('- **核准 commit**: 待提交', f'- **核准 commit**: {value}')
                self.commit('bad backfill')
                self.assertInvalid(self.verify(), '核准 commit')

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


class LegacyBookkeepingTests(BookkeepingTests):
    """流程契約 2.3：維持只新增報告的現行判定；無效時不承諾指出違規位置。"""
    CONTRACT = '2.3'

    def assertInvalid(self, result, *mentions):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def assertNeeds24(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('2.4', result.stderr)

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


class NoContractBookkeepingTests(LegacyBookkeepingTests):
    """讀不到 docs/AGENTS.md：同樣維持現行判定。"""
    CONTRACT = None


if __name__ == '__main__':
    unittest.main()
