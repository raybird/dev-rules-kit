#!/usr/bin/env python3
"""判斷平台上已安裝的技能是哪一版 kit，或有本地修改（issue #9）。

歷代雜湊清單 scripts/skill-hashes.txt 由 build-skill-hashes.py 從 Git 歷史產生，
每行：sha256、技能內的相對路徑、最早與最晚出現的版本。沒有 Git 歷史的安裝
（例如 get.sh 下載的壓縮檔）靠這份清單分辨「舊版 kit」與「使用者改過」。

用法：
  skill_state.py classify <kit 根目錄> <平台技能目錄>
      每個 kit 技能輸出一行：名稱<TAB>狀態<TAB>說明
      狀態：new（未安裝）、same（與本 kit 相同）、kit（某一版 kit）、modified（本地修改）
"""
import hashlib
import os
from pathlib import Path
import re
import sys

HASHES = Path('scripts/skill-hashes.txt')


def skipped(rel):
    parts = rel.split('/')
    return '__pycache__' in parts or rel.endswith('.pyc')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version_key(version):
    return tuple(int(x) for x in version.lstrip('v').split('.'))


def changelog_version(root):
    changelog = Path(root) / 'CHANGELOG.md'
    if changelog.is_file():
        match = re.search(r'^## \[(\d+\.\d+\.\d+)\]', changelog.read_text(encoding='utf-8'), re.M)
        if match:
            return 'v' + match.group(1)
    return None


def tree_files(root):
    """回傳 {相對路徑: sha256}，略過 __pycache__ 與 .pyc。

    跟進指向目錄的 symlink：install.sh 覆蓋時會寫穿連結，裡面改過的檔案要先判斷、備份。
    同一個實體目錄只走一次，避免循環連結；指向不存在目標的連結不是檔案，略過。
    """
    root = Path(root)
    files, seen = {}, set()
    for folder, dirs, names in os.walk(root, followlinks=True):
        real = os.path.realpath(folder)
        if real in seen:
            dirs[:] = []
            continue
        seen.add(real)
        for name in names:
            path = Path(folder) / name
            rel = path.relative_to(root).as_posix()
            if path.is_file() and not skipped(rel):
                files[rel] = digest(path)
    return dict(sorted(files.items()))


def skill_files(skills_root):
    """回傳 {技能/相對路徑: sha256}；skills/ 第一層的檔案（例如 README.md）不是技能。"""
    return {rel: sha for rel, sha in tree_files(skills_root).items() if '/' in rel}


def load_hashes(root):
    """回傳 {(sha256, 相對路徑): (最早版本, 最晚版本)}。"""
    known = {}
    path = Path(root) / HASHES
    if not path.is_file():
        return known
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        sha, rest = line.split(None, 1)
        rel, first, last = rest.rsplit(None, 2)
        known[(sha, rel)] = (first, last)
    return known


def describe(ranges):
    first = max((r[0] for r in ranges), key=version_key)
    last = min((r[1] for r in ranges), key=version_key)
    if version_key(first) > version_key(last):
        return '多個版本混合'
    return first if first == last else f'{first}～{last}'


def classify(kit_root, target_root):
    kit_root, target_root = Path(kit_root), Path(target_root)
    kit = skill_files(kit_root / 'skills')
    known = load_hashes(kit_root)
    current = changelog_version(kit_root) or '版本不明'
    rows = []
    for skill in sorted({rel.split('/', 1)[0] for rel in kit}):
        folder = target_root / skill
        if not folder.is_dir():
            rows.append((skill, 'new', ''))
            continue
        installed = {f'{skill}/{rel}': sha for rel, sha in tree_files(folder).items()}
        owned = [rel for rel in kit if rel.startswith(f'{skill}/')]
        modified = [rel for rel in owned if rel in installed
                    and installed[rel] != kit[rel] and (installed[rel], rel) not in known]
        if modified:
            rows.append((skill, 'modified', ','.join(r.split('/', 1)[1] for r in modified)))
        elif all(installed.get(rel) == kit[rel] for rel in owned):
            rows.append((skill, 'same', current))
        else:
            ranges = [known[(installed[rel], rel)] for rel in owned
                      if rel in installed and (installed[rel], rel) in known]
            rows.append((skill, 'kit', describe(ranges) if ranges else '版本不明'))
    return rows


def missing_hashes(kit_root):
    """目前技能檔中，沒有列在清單、或最晚版本不是 CHANGELOG 最新版的檔案。"""
    known = load_hashes(kit_root)
    current = changelog_version(kit_root)
    problems = []
    for rel, sha in skill_files(Path(kit_root) / 'skills').items():
        entry = known.get((sha, rel))
        if entry is None or (current and entry[1] != current):
            problems.append(rel)
    return problems


if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] != 'classify':
        sys.exit(__doc__)
    for row in classify(sys.argv[2], sys.argv[3]):
        print('\t'.join(row))
