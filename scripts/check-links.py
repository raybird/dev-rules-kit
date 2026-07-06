#!/usr/bin/env python3
"""檢查 repo 內所有 Markdown 檔的相對連結是否指向存在的檔案（不檢查外部網址）。"""
import os
import re
import sys

LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
SKIP_DIRS = {'.git', '.serena', '.claude'}


def iter_markdown_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith('.md'):
                yield os.path.join(dirpath, fname)


def check_file(md_path, root):
    errors = []
    with open(md_path, encoding='utf-8') as f:
        content = f.read()
    # 移除程式碼區塊，避免把範例當成連結
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    for target in LINK_RE.findall(content):
        target = target.split('#')[0].strip()
        if not target or '://' in target or target.startswith('mailto:'):
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(md_path), target))
        if not os.path.exists(resolved):
            errors.append(f"{os.path.relpath(md_path, root)}: 連結目標不存在 -> {target}")
    return errors


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors = []
    for md_path in iter_markdown_files(root):
        errors.extend(check_file(md_path, root))
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print("OK: 所有 Markdown 相對連結皆有效。")
