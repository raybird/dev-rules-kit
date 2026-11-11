#!/usr/bin/env python3
"""唯讀驗證 PASS 之後的提交是否仍沿用原審查；不判斷報告內容的審查品質。

流程契約 2.4 起的 2.x，被審查提交之後只新增該報告、只改該 issue README 記帳區段時沿用；
2.5 起 `## 現況` 也是記帳區段，節內的 `**現行 review**` 欄位可改值。
讀不到契約、低於 2.4 或其他 major 時，維持只接受一個「只新增該報告」提交的現行判定。
記帳區段內看起來像標題、code fence 或粗體欄位的非範本寫法（含巢狀清單與引用裡的寫法）、
HTML 標籤與未在同一行關閉的 HTML 註解一律視為凍結內容，避免藏住或偽造凍結章節。
"""
import argparse
from pathlib import PurePosixPath
import re
import subprocess
import sys

BOOKKEEPING_SECTIONS = ('Timeline', '待確認事項', 'Gate 豁免紀錄')
BOOKKEEPING_FIELDS = ('狀態', '核准 commit')
# 引用與清單容器可以多層巢狀（`> - 1. `），裡面的標題、fence 與粗體一樣會渲染。
CONTAINER = r'^[ \t]*(?:(?:>|(?:[-*+]|\d+[.)])(?=[ \t]))[ \t]*)*'
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})')
LOOSE_FENCE = re.compile(CONTAINER + r'(`{3,}|~{3,})')
HEADING = re.compile(r'^## (?!#)(.*?)\s*$')
LOOSE_HEADING = re.compile(CONTAINER + r'#{1,6}(?:\s|$)')
SETEXT = re.compile(r'^ {0,3}(?:=+|-+)\s*$')
NOT_PARAGRAPH = re.compile(r'^\s*(?:[|>]|[-*+]\s|\d+[.)]\s)')
FIELD = re.compile(CONTAINER + r'\*\*([^*\n]+?)\*\*\s*[:：]\s*(.*?)\s*\\?\s*$')
BOLD_LINE = re.compile(CONTAINER + r'(?:\*\*|__)')
# 會渲染成標題、程式區塊、粗體或能折疊後續內容的標籤；`<br>`、`<sha>` 這類佔位字不在內。
HTML_TAG = re.compile(r'</?(?:h[1-6]|pre|strong|b|details|summary|div|table|thead|tbody|tfoot|tr|td|th|section|'
                      r'article|aside|header|footer|nav|main|blockquote|figure|figcaption|dl|dt|dd|ul|ol|li|p|'
                      r'center|script|style|textarea|iframe|object|embed|form|fieldset|template|noscript|hr)'
                      r'(?=[\s>/])', re.I)
# CommonMark 的 HTML 區塊：獨佔一行的任意標籤、處理指令、宣告與 CDATA，會延續到空行或結束標記。
HTML_BLOCK = re.compile(CONTAINER + r'(?:<[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?>\s*$|</[A-Za-z][A-Za-z0-9-]*\s*>\s*$'
                        r'|<\?|<![A-Za-z]|<!\[CDATA\[)')
CONTRACT = re.compile(r'\*\*流程契約\*\*\s*[:：]\s*(\d+)\.(\d+)')
SHA = re.compile(r'^`?([0-9a-fA-F]{7,40})`?$')
ADDABLE_SECTIONS = ('待確認事項', 'Gate 豁免紀錄')
CURRENT_STATE = '現況'
CURRENT_REVIEW = '現行 review'


class Invalid(ValueError):
    pass


def make_git(repo):
    def git(*args, check=True):
        result = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True)
        if check and result.returncode:
            raise subprocess.CalledProcessError(result.returncode, args, result.stdout, result.stderr)
        return result
    return git


def issue_dir(path):
    parts = PurePosixPath(path).parts
    if len(parts) < 3 or parts[:2] != ('docs', 'issues') or not parts[2].startswith('issue-'):
        raise Invalid(f'無法辨認 issue 目錄：{path}')
    return '/'.join(parts[:3])


def contract_of(git, sha):
    shown = git('show', f'{sha}:docs/AGENTS.md', check=False)
    match = CONTRACT.search(shown.stdout) if shown.returncode == 0 else None
    return (int(match.group(1)), int(match.group(2))) if match else None


def check_report(git, reviewed, head, artifact):
    tree = git('ls-tree', head, '--', artifact).stdout
    if not tree.startswith('100644 blob '):
        raise Invalid('報告必須為一般非執行檔案，不能是 symlink')
    body = git('show', f'{head}:{artifact}').stdout
    if not re.search(r'^- Reviewed HEAD SHA[：:]\s*`?' + re.escape(reviewed) + r'`?\s*$', body, re.M):
        raise Invalid('報告缺少相符的 Reviewed HEAD SHA')


def legacy(git, reviewed, head, artifact, note):
    """流程契約 2.4 之前：只接受一個只新增該報告的提交。"""
    if artifact is None:
        if head == reviewed:
            return 'OK：目前 HEAD 就是被審查提交；原 review 可依其真實判定沿用。'
        raise Invalid('被審查提交之後有新提交；需重新審查' + note)
    parents = git('rev-list', '--parents', '-n', '1', head).stdout.split()
    if parents != [head, reviewed]:
        raise Invalid('只接受被審查提交之後的一個非 merge 報告提交' + note)
    changes = git('diff', '--no-renames', '--name-status', '-z', reviewed, head, '--').stdout
    if changes != 'A\0' + artifact + '\0':
        raise Invalid('後續差異不只新增該報告；需重新審查' + note)
    check_report(git, reviewed, head, artifact)
    return 'OK：只有新增本次報告；原 review 可依其真實判定沿用。'


def closes(line, fence, loose):
    marker = (LOOSE_FENCE if loose else FENCE).match(line)
    return bool(marker) and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) \
        and not line[marker.end():].strip()


def html(line):
    """會改變其後內容渲染方式的 HTML：標籤、獨佔一行的 HTML 區塊，或同一行沒有關閉的註解。"""
    return bool(HTML_TAG.search(line) or HTML_BLOCK.match(line)) or line.rfind('<!--') > line.rfind('-->')


def analyse(text, bookkeeping_sections):
    """回傳 (凍結內容, 記帳欄位, 各記帳章節內容, 章節標題順序)。凍結內容逐項保留所在章節與種類。"""
    frozen, fields, sections, headings = [], [], {}, []
    section, fence, loose, previous = '（標題前）', None, False, ''
    for raw in text.splitlines():
        line = raw.rstrip()
        if fence:
            frozen.append((section, 'fence', line))
            if closes(line, fence, loose):
                fence = None
            continue
        marker = FENCE.match(line) or LOOSE_FENCE.match(line)
        if marker:
            fence, loose = marker.group(1), not FENCE.match(line)
            frozen.append((section, 'fence', line))
            continue
        heading = HEADING.match(line)
        if heading:
            section = heading.group(1)
            headings.append(section)
            if section in bookkeeping_sections:
                sections.setdefault(section, [])
            else:
                frozen.append((section, 'heading', line))
            previous = ''
            continue
        if LOOSE_HEADING.match(line):
            frozen.append((section, 'heading', line))
            previous = line
            continue
        if html(line):
            frozen.append((section, 'html', line))
            previous = line
            continue
        if SETEXT.match(line) and previous.strip() and not NOT_PARAGRAPH.match(previous):
            if section in bookkeeping_sections and sections[section][-1:] == [previous]:
                sections[section].pop()
                frozen.append((section, 'heading', previous))
            frozen.append((section, 'heading', line))
            previous = line
            continue
        previous = line
        field = FIELD.match(line)
        if field and section == CURRENT_STATE and section in bookkeeping_sections \
                and field.group(1).strip() == CURRENT_REVIEW:
            sections[section].append(line)
            continue
        if field and field.group(1).strip() in BOOKKEEPING_FIELDS:
            name = field.group(1).strip()
            fields.append((name, field.group(2)))
            frozen.append((section, 'field', f'**{name}**'))
            continue
        if field or BOLD_LINE.match(line):
            frozen.append((section, 'field', line))
            continue
        if not line.strip():
            continue
        if section in bookkeeping_sections:
            sections[section].append(line)
        else:
            frozen.append((section, 'line', line))
    return frozen, fields, sections, headings


def describe(entry):
    if entry is None:
        return '（無）'
    section, kind, text = entry
    suffix = {'fence': '（code fence 內容一律凍結）', 'html': '（HTML 標籤與未關閉的註解一律凍結）'}.get(kind, '')
    return f'章節「{section}」的' + (f'「{text}」' if text.strip() else '空行') + suffix


def current_review(lines):
    values = [match.group(2) for match in map(FIELD.match, lines or ()) if match]
    if len(values) > 1:
        raise Invalid(f'## {CURRENT_STATE} 只能有一行 **{CURRENT_REVIEW}**，目前有 {len(values)} 行；需重新審查')
    return values[0] if values else '（無）'


def check_readme(git, reviewed, head, readme, version):
    with_state = version >= (2, 5)
    sections = BOOKKEEPING_SECTIONS + ((CURRENT_STATE,) if with_state else ())
    addable = ADDABLE_SECTIONS + ((CURRENT_STATE,) if with_state else ())
    before = analyse(git('show', f'{reviewed}:{readme}').stdout, sections)
    after = analyse(git('show', f'{head}:{readme}').stdout, sections)
    state = [[entry for entry in result[0] if entry[0] == CURRENT_STATE] for result in (before, after)]
    state_changed = state[0] != state[1] or (CURRENT_STATE in before[3]) != (CURRENT_STATE in after[3])
    note = f'（## {CURRENT_STATE} 列入記帳區段需要流程契約 2.5 以上）' if state_changed and not with_state else ''
    try:
        return compare_readme(git, reviewed, readme, before, after, sections, addable)
    except Invalid as error:
        raise Invalid(f'{error}{note}') from None


def compare_readme(git, reviewed, readme, before, after, sections, addable):
    optional = [name for name in addable if (name in before[3]) != (name in after[3])]
    old_order = [name for name in before[3] if name not in optional]
    new_order = [name for name in after[3] if name not in optional]
    if old_order != new_order or any(after[3].count(name) > 1 for name in addable):
        raise Invalid(f'{readme} 的章節標題或順序與被審查版本不同：被審查版本為「{"／".join(before[3])}」，'
                      f'目前為「{"／".join(after[3])}」；只能整節新增或刪除{"、".join(addable)}；需重新審查')
    old_frozen, new_frozen = before[0], after[0]
    for index in range(max(len(old_frozen), len(new_frozen))):
        old = old_frozen[index] if index < len(old_frozen) else None
        new = new_frozen[index] if index < len(new_frozen) else None
        if old != new:
            raise Invalid(f'{readme} 的凍結內容與被審查版本不同：被審查版本為{describe(old)}，'
                          f'目前為{describe(new)}；需重新審查')
    changed = []
    for (name, old), (_, new) in zip(before[1], after[1]):
        if old == new:
            continue
        if name == '核准 commit':
            sha = SHA.match(new)
            if not old.startswith('待提交') or not sha:
                raise Invalid(f'核准 commit 只能由「待提交」改成被審查提交或其祖先，目前為「{old}」→「{new}」；需重新審查')
            target = git('rev-parse', '--verify', '--quiet', sha.group(1) + '^{commit}', check=False)
            if target.returncode or git('merge-base', '--is-ancestor', target.stdout.strip(),
                                        reviewed, check=False).returncode:
                raise Invalid(f'核准 commit「{new}」不是被審查提交或其祖先；需重新審查')
        changed.append(f'{name}（{old} → {new}）')
    for name in sections:
        if before[2].get(name) != after[2].get(name):
            changed.append(name)
    if CURRENT_STATE in sections:
        old, new = current_review(before[2].get(CURRENT_STATE)), current_review(after[2].get(CURRENT_STATE))
        if old != new:
            changed.append(f'{CURRENT_REVIEW}（{old} → {new}）')
    return changed


def bookkeeping(git, reviewed, head, artifact, issue, version):
    """流程契約 2.4 起：淨差異只有該報告與該 issue README 的記帳區段。"""
    if git('merge-base', '--is-ancestor', reviewed, head, check=False).returncode:
        raise Invalid('被審查提交不是目前 HEAD 的祖先（歷史已改寫或分支不同）；需重新審查')
    if git('rev-list', '--merges', f'{reviewed}..{head}').stdout.strip():
        raise Invalid('被審查提交之後含 merge 提交；需重新審查')
    readme = f'{issue}/README.md'
    changes = git('diff-tree', '-r', '--no-renames', '--name-status', '-z', reviewed, head).stdout.split('\0')
    entries = list(zip(changes[0::2], changes[1::2]))
    report_added = False
    for status, path in entries:
        if artifact and path == artifact and status == 'A':
            report_added = True
        elif path == readme and status == 'M':
            continue
        else:
            raise Invalid(f'被審查提交之後變更了 {path}（{status}），不屬於記帳區段；需重新審查')
    if artifact:
        if not report_added:
            raise Invalid(f'被審查提交之後沒有新增報告 {artifact}')
        touched = git('rev-list', f'{reviewed}..{head}', '--', artifact).stdout.split()
        if len(touched) != 1:
            raise Invalid(f'報告 {artifact} 新增後又被修改；需重新審查')
        check_report(git, reviewed, head, artifact)
    changed = check_readme(git, reviewed, head, readme, version) if any(p == readme for _, p in entries) else []
    parts = ([f'新增報告 {artifact}'] if artifact else []) + changed
    summary = '、'.join(parts) if parts else '無變更'
    return f'OK：被審查提交之後只有記帳變更，原 review 可依其真實判定沿用。變更：{summary}'


def verify(repo, reviewed, head, artifact=None, issue=None):
    git = make_git(make_git(repo)('rev-parse', '--show-toplevel').stdout.strip())
    reviewed = git('rev-parse', '--verify', reviewed + '^{commit}').stdout.strip()
    head = git('rev-parse', '--verify', head + '^{commit}').stdout.strip()
    if artifact is None and issue is None:
        raise Invalid('需要 --artifact 或 --issue')
    if artifact is not None:
        path = PurePosixPath(artifact)
        if (len(path.parts) != 4 or path.parts[:2] != ('docs', 'issues')
                or not path.parts[2].startswith('issue-')
                or path.name != f'review-{reviewed[:7]}.md' or str(path) != artifact):
            raise Invalid('artifact 路徑與被審查 SHA 不符')
    target = issue_dir(artifact or issue)
    if artifact is not None and issue is not None and issue_dir(issue) != target:
        raise Invalid('--artifact 與 --issue 指向不同 issue')
    version = contract_of(git, reviewed)
    if version is None or version[0] != 2 or version < (2, 4):
        found = '讀不到流程契約' if version is None else f'流程契約 {version[0]}.{version[1]}'
        return legacy(git, reviewed, head, artifact,
                      f'（{found}；只動記帳區段的放行需要流程契約 2.4 以上的 2.x）')
    return bookkeeping(git, reviewed, head, artifact, target, version)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--reviewed', required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--artifact', help='本機報告的 repo 相對路徑')
    parser.add_argument('--issue', help='報告保存在平台時，指定 docs/issues/issue-{ID}')
    args = parser.parse_args()
    try:
        print(verify(args.repo, args.reviewed, args.head, args.artifact, args.issue))
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f'INVALID：{error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
