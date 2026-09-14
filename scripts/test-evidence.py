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


if __name__ == '__main__':
    unittest.main()
