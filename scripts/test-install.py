#!/usr/bin/env python3
"""在暫存副本測試安裝與初始化，不存取真實平台設定。"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dev-rules-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'kit'
        for name in ('scripts', 'skills', 'rules', 'docs'):
            shutil.copytree(ROOT / name, self.repo / name)
        # 僅替換平台根路徑變數；保留安裝程式本身的參數解析與複製行為。
        script = self.repo / 'scripts/install.sh'
        script.write_text(script.read_text().replace('$HOME', '$INSTALL_TEST_ROOT'))
        self.platform_root = self.base / 'platform settings'
        self.env = dict(os.environ, INSTALL_TEST_ROOT=str(self.platform_root))
        self.project = self.base / 'downstream project'
        self.project.mkdir()

    def install(self, *args):
        return subprocess.run(['bash', str(self.repo / 'scripts/install.sh'), *args],
                              env=self.env, capture_output=True, text=True)

    def init(self, *args):
        return subprocess.run(['python3', str(self.repo / 'scripts/init-project.py'),
                               str(self.project), *args], capture_output=True, text=True)

    def test_install_and_upgrade_all_platforms(self):
        platforms = ('claude', 'antigravity', 'opencode', 'cursor')
        targets = ('.claude/skills', '.gemini/config/skills',
                   '.config/opencode/skills', '.cursor/skills')
        result = self.install(*platforms)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        source = self.repo / 'skills/create-commit/SKILL.md'
        old = source.read_bytes()
        for target in targets:
            folder = self.platform_root / target
            self.assertEqual((folder / 'create-commit/SKILL.md').read_bytes(), old)
            (folder / 'personal').mkdir()
            (folder / 'personal/SKILL.md').write_text('personal content')
        source.write_text('新版測試技能')
        for _ in range(2):
            result = self.install(*platforms)
            self.assertEqual(result.returncode, 0, result.stderr)
        for target in targets:
            folder = self.platform_root / target
            self.assertEqual((folder / 'create-commit/SKILL.md').read_text(), '新版測試技能')
            self.assertFalse((folder / 'create-commit/create-commit').exists())
            self.assertEqual((folder / 'personal/SKILL.md').read_text(), 'personal content')
        self.assertFalse((self.platform_root / '.gemini/config/global_workflows').exists())

    def test_retire_legacy_workflows(self):
        legacy = {'antigravity': '.gemini/config/global_workflows',
                  'opencode': '.config/opencode/commands',
                  'cursor': '.cursor/commands'}
        for folder in legacy.values():
            path = self.platform_root / folder
            path.mkdir(parents=True)
            (path / 'new-issue.md').write_text('舊版工作流程')
            (path / 'personal.md').write_text('personal workflow')
        removed = self.platform_root / legacy['antigravity'] / 'fix-webview-conflict.md'
        removed.write_text('已移除的工作流程')
        self.assertEqual(self.install(*legacy, '--dry-run').returncode, 0)
        self.assertTrue((self.platform_root / legacy['opencode'] / 'new-issue.md').is_file())
        for _ in range(2):
            result = self.install(*legacy)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in legacy.values():
            path = self.platform_root / folder
            self.assertFalse((path / 'new-issue.md').exists())
            backups = list(path.glob('new-issue.md.bak-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), '舊版工作流程')
            self.assertEqual((path / 'personal.md').read_text(), 'personal workflow')
        self.assertFalse(removed.exists())

    def test_windsurf_not_supported(self):
        windsurf = self.platform_root / '.codeium/windsurf'
        (windsurf / 'global_workflows').mkdir(parents=True)
        (windsurf / 'global_workflows/new-issue.md').write_text('舊版工作流程')
        (self.platform_root / '.claude').mkdir()
        self.assertNotEqual(self.install('windsurf').returncode, 0)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.platform_root / '.claude/skills/new-issue/SKILL.md').is_file())
        self.assertFalse((windsurf / 'skills').exists())
        self.assertEqual((windsurf / 'global_workflows/new-issue.md').read_text(), '舊版工作流程')

    def test_install_dry_run_and_invalid_platform(self):
        self.assertEqual(self.install('claude', '--dry-run').returncode, 0)
        self.assertFalse(self.platform_root.exists())
        self.assertNotEqual(self.install('unknown').returncode, 0)
        self.assertFalse(self.platform_root.exists())

    def test_rules_backup(self):
        target = self.platform_root / '.config/opencode/AGENTS.md'
        target.parent.mkdir(parents=True)
        target.write_text('custom rules')
        self.assertEqual(self.install('opencode', '--with-rules').returncode, 0)
        backups = list(target.parent.glob('AGENTS.md.bak-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'custom rules')
        self.assertEqual(target.read_bytes(), (self.repo / 'rules/AGENTS.zh-TW.md').read_bytes())

    def test_init_check_dry_run_and_repeat(self):
        self.assertNotEqual(self.init('--check').returncode, 0)
        self.assertEqual(self.init('--dry-run').returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(self.init().returncode, 0)
        expected = ['docs/AGENTS.md', 'docs/agents/document-types.md',
                    'docs/agents/readme-templates.md', 'docs/agents/issue-checklist.md',
                    'docs/_templates/architecture-template.md',
                    'docs/_templates/domain-template.md', 'docs/_templates/changelog-template.md']
        for rel in expected:
            self.assertEqual((self.project / rel).read_bytes(), (self.repo / rel).read_bytes())
        stamp = (self.project / 'docs/AGENTS.md').stat().st_mtime_ns
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual((self.project / 'docs/AGENTS.md').stat().st_mtime_ns, stamp)
        self.assertEqual(self.init('--check').returncode, 0)

    def test_init_conflict_has_no_partial_writes(self):
        target = self.project / 'docs/agents/issue-checklist.md'
        target.parent.mkdir(parents=True)
        target.write_text('custom checklist')
        self.assertNotEqual(self.init().returncode, 0)
        self.assertFalse((self.project / 'docs/AGENTS.md').exists())
        self.assertEqual(target.read_text(), 'custom checklist')

    def test_init_rejects_symlink_and_file_parent(self):
        outside = self.base / 'outside'
        outside.mkdir()
        docs = self.project / 'docs'
        docs.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.init().returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])
        docs.unlink()
        docs.write_text('existing file')
        self.assertNotEqual(self.init().returncode, 0)
        self.assertEqual(docs.read_text(), 'existing file')


if __name__ == '__main__':
    unittest.main()
