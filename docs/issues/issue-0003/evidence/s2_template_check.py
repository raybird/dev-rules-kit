"""以 readme-templates.md 的 ## 現況 原文建 2.5 fixture，審查後更新現況，確認 verify-artifact 判有效；2.4 判無效。"""
import re, subprocess, sys, tempfile
from pathlib import Path
kit = Path(sys.argv[1])
tpl = (kit / 'docs/agents/readme-templates.md').read_text()
block = tpl[tpl.index('## 現況\n'):tpl.index('## 快速導覽\n')]
def run(contract):
    with tempfile.TemporaryDirectory() as d:
        g = lambda *a: subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, text=True).stdout.strip()
        g('init', '-q', '-b', 'main'); g('config', 'user.name', 'F'); g('config', 'user.email', 'f@example.invalid')
        Path(d, 'docs/issues/issue-9').mkdir(parents=True)
        Path(d, 'docs/AGENTS.md').write_text(f'**流程契約**: {contract}\n')
        readme = Path(d, 'docs/issues/issue-9/README.md')
        readme.write_text('# Issue 9\n\n## 概述\n說明。\n\n' + block + '## Timeline\n\n| 日期 | 異動 | 負責人 |\n|---|---|---|\n\n---\n**狀態**: 審查中\n')
        g('add', '-A'); g('commit', '-qm', 'reviewed'); r = g('rev-parse', 'HEAD')
        rep = f'docs/issues/issue-9/review-{r[:7]}.md'
        Path(d, rep).write_text(f'- Reviewed HEAD SHA：{r}\nPASS\n')
        t = readme.read_text()
        t = t.replace('{現行報告的 repo-relative 路徑或平台連結}', rep)
        t = t.replace('| {例如：併入主幹} | {可重跑的查證命令} | {查證結果} | YYYY-MM-DD |', '| 併入主幹 | git merge-base --is-ancestor HEAD main | 是 | 2026-11-10 |')
        readme.write_text(t); g('add', '-A'); g('commit', '-qm', 'report and current state')
        out = subprocess.run(['python3', str(kit / 'skills/review/scripts/verify-artifact.py'), '--repo', d, '--reviewed', r, '--head', 'HEAD', '--artifact', rep], capture_output=True, text=True)
        print(f'## 流程契約 {contract}\nexit={out.returncode}\n{out.stdout}{out.stderr}')
for c in ('2.5', '2.4'):
    run(c)
