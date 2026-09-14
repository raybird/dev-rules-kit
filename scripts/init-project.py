#!/usr/bin/env python3
"""初始化或更新下游規範；保留 project.md，核心更新需可信部署基線。"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

MANIFEST = Path('docs/.dev-rules-kit.json')
CUSTOM = Path('docs/agents/project.md')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(project, rel):
    target = project / rel
    chain = [target, *list(target.parents)[:len(rel.parts) - 1]]
    return (not any(p.is_symlink() for p in chain)
            and not any(p.exists() and not p.is_dir() for p in chain[1:])
            and (not target.exists() or (target.is_file() and target.stat().st_nlink == 1)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='已存在的下游專案根目錄')
    parser.add_argument('--update', action='store_true', help='依部署基線更新未被客製的核心')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='只顯示待部署／更新文件')
    mode.add_argument('--check', action='store_true', help='唯讀檢查核心一致性與客製檔存在')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    project = args.project.resolve()
    if not project.is_dir():
        parser.error('專案根目錄必須已存在')
    if args.update and args.check:
        parser.error('--update 與 --check 請分開執行')
    files = [Path('docs/AGENTS.md')]
    for folder in ('agents', '_templates'):
        files.extend(p.relative_to(root) for p in sorted((root / 'docs' / folder).glob('*.md')))
    if not safe_path(project, MANIFEST):
        print(f'衝突：{MANIFEST} 不是安全的一般檔案路徑；未寫入任何文件。')
        return 1
    manifest = project / MANIFEST
    previous = {}
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text())
            if data.get('format') != 1 or not isinstance(data.get('files'), dict):
                raise ValueError('未知部署基線格式')
            previous = data['files']
        except (ValueError, AttributeError, OSError) as error:
            print(f'衝突：無法讀取部署基線：{error}；未寫入任何文件。')
            return 1
    pending, conflicts = [], []
    for rel in files:
        target = project / rel
        if not safe_path(project, rel):
            conflicts.append(rel)
        elif not target.exists():
            pending.append(rel)
        elif rel == CUSTOM:
            continue
        elif digest(target) != digest(root / rel):
            if args.update and previous.get(str(rel)) == digest(target):
                pending.append(rel)
            else:
                conflicts.append(rel)
    for rel in conflicts:
        print(f'衝突：{rel}（核心有本地變更或無部署基線，請先人工合併）')
    for rel in pending:
        print(f'待部署／更新：{rel}')
    if conflicts:
        print('未寫入任何文件；保留客製內容，解決衝突後重新執行。')
        return 1
    if args.check:
        if pending:
            return 1
        print('OK：核心與本 kit 一致，project.md 已存在；客製語意另行覆核。')
        return 0
    if args.dry_run:
        print('dry-run：未寫入任何文件。')
        return 0
    for rel in pending:
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, target)
    # Only successful preflight and deployment establish a new baseline.
    data = {'format': 1, 'files': {str(rel): digest(project / rel)
                                 for rel in files if rel != CUSTOM}}
    serialized = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if not manifest.exists() or manifest.read_text() != serialized:
        manifest.write_text(serialized)
    print(f'OK：部署／更新 {len(pending)} 份文件，既有 project.md 保持原樣。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
