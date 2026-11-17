#!/usr/bin/env python3
"""在暫存副本測試安裝與初始化，不存取真實平台設定。"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
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
        shutil.copy2(ROOT / 'CHANGELOG.md', self.repo / 'CHANGELOG.md')
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

    def get(self, *args):
        # get.sh 以 file:// 讀本機的假 release，不連網；HOME 指向暫存平台根目錄。
        env = dict(self.env, HOME=str(self.platform_root),
                   DEV_RULES_KIT_REPO_URL=(self.base / 'remote').as_uri())
        env.pop('XDG_DATA_HOME', None)
        env.pop('DEV_RULES_KIT_HOME', None)
        return subprocess.run(['bash', str(self.repo / 'scripts/get.sh'), *args],
                              env=env, capture_output=True, text=True)

    def make_release(self, version, broken=False):
        archive = self.base / 'remote/archive/refs/tags' / f'{version}.tar.gz'
        archive.parent.mkdir(parents=True, exist_ok=True)
        if broken:
            archive.write_bytes(b'not a tarball')
            return archive
        with tarfile.open(archive, 'w:gz') as tar:
            tar.add(self.repo, arcname=f'dev-rules-kit-{version.lstrip("v")}')
        return archive

    def tree(self, root):
        return sorted(str(p.relative_to(root)) for p in root.rglob('*')) if root.exists() else []

    def init(self, *args):
        return subprocess.run(['python3', str(self.repo / 'scripts/init-project.py'),
                               str(self.project), *args], capture_output=True, text=True)

    def test_past_project_templates_registered(self):
        # issue #7 review-92c1f63：改 project.md 範本時漏加舊雜湊，下游收不到「仍是範本原文」提醒。
        import importlib.util
        spec = importlib.util.spec_from_file_location('init_project', ROOT / 'scripts/init-project.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        log = subprocess.run(['git', '-C', str(ROOT), 'log', '--format=%H', '--', 'docs/agents/project.md'],
                             capture_output=True, text=True)
        shallow = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--is-shallow-repository'],
                                 capture_output=True, text=True).stdout.strip()
        if log.returncode or not log.stdout.strip() or shallow != 'false':
            self.skipTest('讀不到 kit 的完整 Git 歷史（淺層 clone 需 fetch-depth: 0）')
        current = hashlib.sha256((ROOT / 'docs/agents/project.md').read_bytes()).hexdigest()
        missing = []
        for sha in log.stdout.split():
            shown = subprocess.run(['git', '-C', str(ROOT), 'show', f'{sha}:docs/agents/project.md'], capture_output=True)
            if shown.returncode:
                continue
            digest = hashlib.sha256(shown.stdout).hexdigest()
            if digest != current and digest not in module.PAST_TEMPLATES:
                missing.append(f'{sha[:7]} {digest}')
        self.assertEqual(missing, [], '歷代 project.md 範本的雜湊沒有加進 PAST_TEMPLATES')

    def test_install_and_upgrade_all_platforms(self):
        platforms = ('codex', 'claude', 'antigravity', 'opencode', 'cursor')
        targets = ('.codex/skills', '.claude/skills', '.gemini/config/skills',
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
            self.assertEqual((folder / 'review/scripts/verify-artifact.py').read_bytes(),
                             (self.repo / 'skills/review/scripts/verify-artifact.py').read_bytes())
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

    def test_modified_skill_backed_up_before_overwrite(self):
        # issue #9 SCN-003、007：不屬於任何一版 kit 的技能先整個備份到技能目錄外，再覆蓋。
        self.assertEqual(self.install('claude').returncode, 0)
        skills = self.platform_root / '.claude/skills'
        target = skills / 'create-commit/SKILL.md'
        target.write_text('使用者自己改的內容')
        (skills / 'create-commit/notes.md').write_text('使用者加的檔案')
        dry = self.install('claude', '--dry-run')
        self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
        self.assertIn('會備份 create-commit（本地修改：SKILL.md）', dry.stdout)
        self.assertNotIn('會備份 new-issue', dry.stdout)
        self.assertFalse((self.platform_root / '.claude/skill-backups').exists())
        self.assertEqual(target.read_text(), '使用者自己改的內容')
        result = self.install('claude')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        backups = list((self.platform_root / '.claude/skill-backups').glob('create-commit.bak-*'))
        self.assertEqual(len(backups), 1, result.stdout)
        self.assertEqual((backups[0] / 'SKILL.md').read_text(), '使用者自己改的內容')
        self.assertEqual((backups[0] / 'notes.md').read_text(), '使用者加的檔案')
        self.assertIn(str(backups[0].relative_to(self.platform_root)), result.stdout)
        self.assertEqual(target.read_bytes(), (self.repo / 'skills/create-commit/SKILL.md').read_bytes())
        self.assertEqual(len(list((self.platform_root / '.claude/skill-backups').iterdir())), 1)
        again = self.install('claude')
        self.assertEqual(again.returncode, 0)
        self.assertEqual(len(list((self.platform_root / '.claude/skill-backups').iterdir())), 1)

    def test_previous_kit_version_overwritten_without_backup(self):
        # issue #9 SCN-002：內容屬於某一版 kit（列在歷代雜湊清單）就直接覆蓋，不備份。
        import hashlib
        old = '舊版 kit 的 create-commit\n'
        digest = hashlib.sha256(old.encode()).hexdigest()
        hashes = self.repo / 'scripts/skill-hashes.txt'
        with hashes.open('a') as f:
            f.write(f'{digest}  create-commit/SKILL.md  v4.0.0  v4.0.0\n')
        target = self.platform_root / '.claude/skills/create-commit/SKILL.md'
        target.parent.mkdir(parents=True)
        target.write_text(old)
        result = self.install('claude')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(target.read_bytes(), (self.repo / 'skills/create-commit/SKILL.md').read_bytes())
        self.assertFalse((self.platform_root / '.claude/skill-backups').exists())

    def test_get_failure_leaves_no_partial_state(self):
        # issue #9 風險：下載或解壓失敗時，平台目錄、current 與資料目錄都不留半套。
        (self.platform_root / '.claude').mkdir(parents=True)
        data = self.platform_root / '.local/share/dev-rules-kit'
        self.make_release('v9.0.0')
        self.assertEqual(self.get('--version', 'v9.0.0').returncode, 0)
        before_platform = self.tree(self.platform_root / '.claude')
        before_data = self.tree(data)
        self.assertEqual(os.readlink(data / 'current'), 'v9.0.0')
        self.make_release('v9.1.0', broken=True)
        for args in (('--version', 'v9.9.9'), ('--version', 'v9.1.0')):
            with self.subTest(args=args):
                result = self.get(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.tree(self.platform_root / '.claude'), before_platform)
                self.assertEqual(self.tree(data), before_data)
                self.assertEqual(os.readlink(data / 'current'), 'v9.0.0')

    def state_module(self, root):
        import importlib.util
        spec = importlib.util.spec_from_file_location('skill_state', root / 'scripts/skill_state.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_skill_hashes_must_cover_current_files(self):
        # issue #9 SCN-006：改了技能檔卻沒重產雜湊清單時，check-kit 用的判斷要指出該檔。
        module = self.state_module(self.repo)
        self.assertEqual(module.missing_hashes(self.repo), [])
        source = self.repo / 'skills/create-commit/SKILL.md'
        source.write_text(source.read_text() + '\n新版內容\n')
        self.assertEqual(module.missing_hashes(self.repo), ['create-commit/SKILL.md'])
        changelog = self.repo / 'CHANGELOG.md'
        source.write_bytes((ROOT / 'skills/create-commit/SKILL.md').read_bytes())
        changelog.write_text(changelog.read_text().replace('---\n', '---\n\n## [99.0.0] - 2099-01-01\n', 1))
        self.assertIn('create-commit/SKILL.md', module.missing_hashes(self.repo))

    def test_skill_hashes_cover_released_versions(self):
        # issue #9 SCN-006：每個 v* tag 的技能檔都要在歷代雜湊清單裡，否則舊版會被當成本地修改。
        module = self.state_module(ROOT)
        shallow = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--is-shallow-repository'],
                                 capture_output=True, text=True).stdout.strip()
        tags = subprocess.run(['git', '-C', str(ROOT), 'tag', '-l', 'v*'], capture_output=True, text=True)
        if shallow != 'false' or tags.returncode or not tags.stdout.split():
            self.skipTest('讀不到 kit 的完整 Git 歷史與 tag（淺層 clone 需 fetch-depth: 0）')
        known = module.load_hashes(ROOT)
        missing = []
        for tag in tags.stdout.split():
            listing = subprocess.run(['git', '-C', str(ROOT), 'ls-tree', '-r', '--name-only', tag, '--', 'skills'],
                                     capture_output=True, text=True).stdout.split()
            for path in listing:
                rel = path.split('/', 1)[1]
                if '/' not in rel or module.skipped(rel):
                    continue
                blob = subprocess.run(['git', '-C', str(ROOT), 'show', f'{tag}:{path}'], capture_output=True).stdout
                if (hashlib.sha256(blob).hexdigest(), rel) not in known:
                    missing.append(f'{tag}:{rel}')
        self.assertEqual(missing, [])

    def test_get_install_update_and_init(self):
        # issue #9 SCN-001、002：get.sh 安裝、重跑更新，init-project.py 用 current 路徑。
        (self.platform_root / '.claude').mkdir(parents=True)
        data = self.platform_root / '.local/share/dev-rules-kit'
        skills = self.platform_root / '.claude/skills'
        self.make_release('v9.0.0')
        result = self.get('--version', 'v9.0.0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((data / 'v9.0.0/scripts/install.sh').is_file())
        self.assertEqual(os.readlink(data / 'current'), 'v9.0.0')
        for path in (self.repo / 'skills').rglob('*'):
            if path.is_file() and path.parent != self.repo / 'skills' and '__pycache__' not in path.parts:
                rel = path.relative_to(self.repo / 'skills')
                self.assertEqual((skills / rel).read_bytes(), path.read_bytes(), str(rel))
        init = subprocess.run(['python3', str(data / 'current/scripts/init-project.py'), str(self.project)],
                              capture_output=True, text=True)
        self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
        source = self.repo / 'skills/create-commit/SKILL.md'
        source.write_text(source.read_text() + '\n新版內容\n')
        self.make_release('v9.1.0')
        result = self.get('--version', 'v9.1.0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((skills / 'create-commit/SKILL.md').read_bytes(), source.read_bytes())
        self.assertFalse((self.platform_root / '.claude/skill-backups').exists(), result.stdout)
        self.assertEqual(os.readlink(data / 'current'), 'v9.1.0')
        self.assertTrue((data / 'v9.0.0/scripts/install.sh').is_file())

    def test_get_dry_run_writes_nothing(self):
        # issue #9 SCN-004：dry-run 不寫入資料目錄與平台目錄，並列出會備份的技能。
        (self.platform_root / '.claude').mkdir(parents=True)
        self.make_release('v9.0.0')
        before = self.tree(self.platform_root)
        result = self.get('--dry-run', '--version', 'v9.0.0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('v9.0.0', result.stdout)
        self.assertEqual(self.tree(self.platform_root), before)
        self.assertEqual(self.get('--version', 'v9.0.0').returncode, 0)
        (self.platform_root / '.claude/skills/review/SKILL.md').write_text('使用者改的')
        self.make_release('v9.1.0')
        before = self.tree(self.platform_root)
        result = self.get('--dry-run', '--version', 'v9.1.0')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('會備份 review（本地修改：SKILL.md）', result.stdout)
        self.assertEqual(self.tree(self.platform_root), before)
        self.assertEqual((self.platform_root / '.claude/skills/review/SKILL.md').read_text(), '使用者改的')

    def test_get_check_and_latest_unreachable(self):
        # issue #9 SCN-005：--check 唯讀；取不到最新 release 時照實說明，其餘照常列出。
        (self.platform_root / '.claude').mkdir(parents=True)
        result = self.get('--check')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('尚未以 get.sh 安裝', result.stdout)
        self.assertIn('取不到', result.stdout)
        before = self.tree(self.platform_root)
        result = self.get()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('取不到最新版本', result.stderr)
        self.assertEqual(self.tree(self.platform_root), before)
        self.make_release('v9.0.0')
        self.assertEqual(self.get('--version', 'v9.0.0').returncode, 0)
        (self.platform_root / '.claude/skills/review/SKILL.md').write_text('使用者改的')
        before = self.tree(self.platform_root)
        result = self.get('--check', 'claude')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('目前版本：v9.0.0', result.stdout)
        self.assertIn('review：本地修改（SKILL.md）', result.stdout)
        self.assertIn('new-issue：與本 kit 相同', result.stdout)
        self.assertEqual(self.tree(self.platform_root), before)

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

    def test_codex_auto_detect_and_rules(self):
        codex = self.platform_root / '.codex'
        codex.mkdir(parents=True)
        result = self.install('--with-rules')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((codex / 'skills/new-issue/SKILL.md').read_bytes(),
                         (self.repo / 'skills/new-issue/SKILL.md').read_bytes())
        self.assertEqual((codex / 'AGENTS.md').read_bytes(),
                         (self.repo / 'rules/AGENTS.zh-TW.md').read_bytes())

    def test_init_check_dry_run_and_repeat(self):
        self.assertNotEqual(self.init('--check').returncode, 0)
        self.assertEqual(self.init('--dry-run').returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(self.init().returncode, 0)
        expected = ['docs/AGENTS.md', 'docs/agents/document-types.md',
                    'docs/agents/readme-templates.md', 'docs/agents/issue-checklist.md',
                    'docs/agents/acceptance.md', 'docs/agents/verification.md',
                    'docs/agents/review-evidence.md', 'docs/agents/project.md']
        for rel in expected:
            self.assertEqual((self.project / rel).read_bytes(), (self.repo / rel).read_bytes())
        # issue #8：常青文件範本隨 execute-task 技能安裝，不再部署到下游 repo。
        self.assertFalse((self.project / 'docs/_templates').exists())
        manifest = json.loads((self.project / 'docs/.dev-rules-kit.json').read_text())
        self.assertEqual(sorted(manifest['files']), sorted(r for r in expected if r != 'docs/agents/project.md'))
        stamp = (self.project / 'docs/AGENTS.md').stat().st_mtime_ns
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual((self.project / 'docs/AGENTS.md').stat().st_mtime_ns, stamp)
        result = self.init('--check')
        self.assertEqual(result.returncode, 0)
        self.assertIn('project.md 仍是初始化範本原文', result.stdout)

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

    def test_update_preserves_project_customization(self):
        self.assertEqual(self.init().returncode, 0)
        project_rules = self.project / 'docs/agents/project.md'
        project_rules.write_text('# 本地規範\n測試：make check\n')
        source = self.repo / 'docs/agents/issue-checklist.md'
        source.write_text(source.read_text() + '\n新版檢查\n')
        target = self.project / 'docs/agents/issue-checklist.md'
        old = target.read_bytes()
        self.assertEqual(self.init('--update', '--dry-run').returncode, 0)
        self.assertEqual(target.read_bytes(), old)
        self.assertEqual(self.init('--update').returncode, 0)
        self.assertEqual(target.read_bytes(), source.read_bytes())
        self.assertEqual(project_rules.read_text(), '# 本地規範\n測試：make check\n')
        result = self.init('--check')
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('project.md 仍是初始化範本原文', result.stdout)

    def test_update_from_baseline_with_templates(self):
        # issue #8：v4.12.0 以前的部署基線列有 docs/_templates/，舊檔留在原處、不再追蹤。
        self.assertEqual(self.init().returncode, 0)
        manifest = self.project / 'docs/.dev-rules-kit.json'
        data = json.loads(manifest.read_text())
        old = {}
        for name in ('architecture-template.md', 'domain-template.md', 'changelog-template.md'):
            rel = f'docs/_templates/{name}'
            target = self.project / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f'# v4.12.0 部署的 {name}\n')
            old[rel] = target.read_bytes()
            data['files'][rel] = hashlib.sha256(old[rel]).hexdigest()
        manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
        before = manifest.read_bytes()
        def tree():
            return sorted(str(p.relative_to(self.project)) for p in self.project.rglob('*'))
        listing = tree()
        self.assertEqual(self.init('--update', '--dry-run').returncode, 0)
        self.assertEqual(tree(), listing)
        self.assertEqual(manifest.read_bytes(), before)
        self.assertEqual(self.init('--update').returncode, 0)
        for rel, content in old.items():
            self.assertEqual((self.project / rel).read_bytes(), content)
        files = json.loads(manifest.read_text())['files']
        self.assertEqual([rel for rel in files if rel.startswith('docs/_templates/')], [])
        self.assertEqual(self.init('--check').returncode, 0)

    def test_check_reports_outdated_core_separately(self):
        self.assertEqual(self.init().returncode, 0)
        source = self.repo / 'docs/agents/issue-checklist.md'
        source.write_text(source.read_text() + '\n新版檢查\n')
        for args in (('--check',), ('--dry-run',), ()):
            result = self.init(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('落後本 kit：docs/agents/issue-checklist.md', result.stdout)
            self.assertNotIn('衝突', result.stdout)
        target = self.project / 'docs/agents/issue-checklist.md'
        target.write_text(target.read_text() + '\n本地修改\n')
        result = self.init('--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('衝突：docs/agents/issue-checklist.md', result.stdout)

    def test_update_rejects_edited_core_without_partial_writes(self):
        self.assertEqual(self.init().returncode, 0)
        target = self.project / 'docs/AGENTS.md'
        target.write_text('本地修改過的核心')
        new = self.repo / 'docs/agents/new-reference.md'
        new.write_text('新參考資料')
        self.assertNotEqual(self.init('--update').returncode, 0)
        self.assertEqual(target.read_text(), '本地修改過的核心')
        self.assertFalse((self.project / 'docs/agents/new-reference.md').exists())

    def test_update_rejects_manifest_symlink(self):
        self.assertEqual(self.init().returncode, 0)
        manifest = self.project / 'docs/.dev-rules-kit.json'
        manifest.unlink(missing_ok=True)
        outside = self.base / 'outside-manifest'
        outside.write_text('{}')
        manifest.symlink_to(outside)
        self.assertNotEqual(self.init('--update').returncode, 0)
        self.assertEqual(outside.read_text(), '{}')

    def test_update_rejects_hardlinks_without_partial_writes(self):
        for rel in ('docs/AGENTS.md', 'docs/.dev-rules-kit.json'):
            with self.subTest(path=rel):
                self.assertEqual(self.init().returncode, 0)
                target = self.project / rel
                outside = self.base / 'outside-linked-file'
                os.link(target, outside)
                old = outside.read_bytes()
                source = self.repo / 'docs/agents/issue-checklist.md'
                source.write_text(source.read_text() + '\n上游更新\n')
                before = (self.project / 'docs/agents/issue-checklist.md').read_bytes()
                self.assertNotEqual(self.init('--update').returncode, 0)
                self.assertEqual(outside.read_bytes(), old)
                self.assertEqual((self.project / 'docs/agents/issue-checklist.md').read_bytes(), before)
                outside.unlink()
                self.assertEqual(self.init('--update').returncode, 0)


if __name__ == '__main__':
    unittest.main()
