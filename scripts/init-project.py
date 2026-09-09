#!/usr/bin/env python3
"""部署下游專案文件；先檢查全部衝突，保留既有客製內容。"""
import argparse
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='已存在的下游專案根目錄')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='只顯示待部署文件')
    mode.add_argument('--check', action='store_true', help='唯讀比對文件是否與本 kit 一致')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    project = args.project.resolve()
    if not project.is_dir():
        parser.error('專案根目錄必須已存在')
    files = [Path('docs/AGENTS.md')]
    for folder in ('agents', '_templates'):
        files.extend(p.relative_to(root) for p in sorted((root / 'docs' / folder).glob('*.md')))
    missing, conflicts = [], []
    for rel in files:
        target = project / rel
        # 客製目錄的 symlink 也要先攔住，避免寫到指定專案之外。
        chain = [target, *list(target.parents)[:len(rel.parts) - 1]]
        if any(p.is_symlink() for p in chain):
            conflicts.append(rel)
        elif any(p.exists() and not p.is_dir() for p in chain[1:]):
            conflicts.append(rel)
        elif not target.exists():
            missing.append(rel)
        elif not target.is_file() or target.read_bytes() != (root / rel).read_bytes():
            conflicts.append(rel)
    for rel in conflicts:
        print(f'衝突：{rel}（請依客製邊界人工合併，保留專案內容）')
    for rel in missing:
        print(f'待部署：{rel}')
    if conflicts:
        print('未寫入任何文件；解決衝突後重新執行。')
        return 1
    if args.check:
        if missing:
            return 1
        print('OK：專案文件與本 kit 一致；客製後的語意相容性需依核心層齊備性檢查確認。')
        return 0
    if args.dry_run:
        print('dry-run：未寫入任何文件。')
        return 0
    for rel in missing:
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, target)
    print(f'OK：部署 {len(missing)} 份文件，既有相同文件保持原樣。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
