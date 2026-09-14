#!/usr/bin/env python3
"""唯讀驗證本機 review 的單一報告提交例外；不判斷報告內容的審查品質。"""
import argparse
from pathlib import PurePosixPath
import re
import subprocess
import sys


def verify(repo, reviewed, head, artifact):
    def git(*args):
        return subprocess.run(['git', '-C', repo, *args], check=True,
                              capture_output=True, text=True).stdout
    reviewed = git('rev-parse', '--verify', reviewed + '^{commit}').strip()
    head = git('rev-parse', '--verify', head + '^{commit}').strip()
    path = PurePosixPath(artifact)
    if (len(path.parts) != 4 or path.parts[:2] != ('docs', 'issues')
            or not path.parts[2].startswith('issue-')
            or path.name != f'review-{reviewed[:7]}.md' or str(path) != artifact):
        raise ValueError('artifact 路徑與被審查 SHA 不符')
    parents = git('rev-list', '--parents', '-n', '1', head).split()
    if parents != [head, reviewed]:
        raise ValueError('只接受被審查提交之後的一個非 merge 報告提交')
    changes = git('diff', '--no-renames', '--name-status', '-z', reviewed, head, '--')
    if changes != 'A\0' + artifact + '\0':
        raise ValueError('後續差異不只新增該報告；需重新審查')
    tree = git('ls-tree', head, '--', artifact)
    if not tree.startswith('100644 blob '):
        raise ValueError('報告必須為一般非執行檔案，不能是 symlink')
    body = git('show', head + ':' + artifact)
    if not re.search(r'^- Reviewed HEAD SHA[：:]\s*`?' + re.escape(reviewed) + r'`?\s*$', body, re.M):
        raise ValueError('報告缺少相符的 Reviewed HEAD SHA')
    return 'OK：只有新增本次報告；原 review 可依其真實判定沿用。'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--reviewed', required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--artifact', required=True)
    args = parser.parse_args()
    try:
        print(verify(args.repo, args.reviewed, args.head, args.artifact))
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f'INVALID：{error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
