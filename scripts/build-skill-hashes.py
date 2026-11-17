#!/usr/bin/env python3
"""從 Git 歷史產生 scripts/skill-hashes.txt（issue #9）。

收錄每個 v* tag 與目前工作區的技能檔：sha256、技能內的相對路徑、最早與最晚出現的版本。
工作區的內容標為 CHANGELOG 最上面的版本。修改 skills/ 或發布新版前重新執行，check-kit 會檢查。
"""
import subprocess
from pathlib import Path
import re
import hashlib

import skill_state

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, check=True).stdout


def main():
    seen = {}

    def add(sha, rel, version):
        first, last = seen.get((sha, rel), (version, version))
        seen[(sha, rel)] = (min(first, version, key=skill_state.version_key),
                            max(last, version, key=skill_state.version_key))

    tags = sorted((t for t in git('tag', '-l', 'v*').decode().split()
                   if re.fullmatch(r'v\d+\.\d+\.\d+', t)), key=skill_state.version_key)
    blobs = {}
    for tag in tags:
        for line in git('ls-tree', '-r', tag, '--', 'skills').decode().splitlines():
            meta, path = line.split('\t', 1)
            _, kind, blob = meta.split()
            rel = path.split('/', 1)[1]
            if kind != 'blob' or '/' not in rel or skill_state.skipped(rel):
                continue
            if blob not in blobs:
                blobs[blob] = hashlib.sha256(git('cat-file', 'blob', blob)).hexdigest()
            add(blobs[blob], rel, tag)
    current = skill_state.changelog_version(ROOT)
    for rel, sha in skill_state.skill_files(ROOT / 'skills').items():
        add(sha, rel, current)
    lines = ['# 由 scripts/build-skill-hashes.py 產生，請勿手動修改。',
             '# sha256  技能內的相對路徑  最早版本  最晚版本']
    lines += [f'{sha}  {rel}  {first}  {last}'
              for (sha, rel), (first, last) in sorted(seen.items(), key=lambda i: (i[0][1], i[1][0], i[0][0]))]
    (ROOT / skill_state.HASHES).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'OK：{len(seen)} 筆，涵蓋 {len(tags)} 個 tag 與工作區（{current}）。')


if __name__ == '__main__':
    main()
