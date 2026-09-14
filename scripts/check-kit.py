#!/usr/bin/env python3
"""檢查 kit 自身的一致性：skill frontmatter、流程契約相容性、雙語規則章節數、install.sh 安裝路徑"""
import os
import re
import sys


def find_skills(project_root):
    """掃描 skills 目錄，回傳 (skill 名稱, SKILL.md 路徑) 清單"""
    skills_dir = os.path.join(project_root, 'skills')
    skills = []
    for item in sorted(os.listdir(skills_dir)):
        skill_file = os.path.join(skills_dir, item, 'SKILL.md')
        if os.path.isfile(skill_file):
            skills.append((item, skill_file))
    return skills


def read_frontmatter(skill_file, key):
    """取出 SKILL.md frontmatter 中指定欄位的值，找不到回傳 None"""
    with open(skill_file, encoding='utf-8') as f:
        lines = f.read().splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line.startswith(f'{key}:'):
            return line[len(key) + 1:].strip()
    return None


def check_skill_names(project_root):
    """檢查每個 SKILL.md 的 frontmatter 具備 description:，以及與資料夾名一致的 name:

    OpenCode 與 Antigravity 要求 frontmatter 具備 name:，缺少時整份 skill 會
    靜默不載入（2.4.0 修過一次）；此檢查防止同一問題回歸。
    """
    errors = []
    for name, skill_file in find_skills(project_root):
        fm_name = read_frontmatter(skill_file, 'name')
        if fm_name is None:
            errors.append(f"skills/{name}/SKILL.md 的 frontmatter 缺少 name:（OpenCode / Antigravity 會靜默不載入）")
        elif fm_name != name:
            errors.append(f"skills/{name}/SKILL.md 的 name: 為「{fm_name}」，必須等於資料夾名「{name}」")
        if not read_frontmatter(skill_file, 'description'):
            errors.append(f"skills/{name}/SKILL.md 的 frontmatter 缺少 description:（agent 靠它判斷何時載入）")
    return errors


def read_agents_md_version(project_root):
    """讀取流程契約；文件編輯版本不參與技能相容性。"""
    path = os.path.join(project_root, 'docs', 'AGENTS.md')
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        match = re.search(r'^\*\*流程契約\*\*:\s*([0-9]+\.[0-9]+)\s*$', f.read(), re.M)
    return match.group(1) if match else None


def check_agents_md_declarations(project_root):
    """檢查最低契約需求：同 major，專案 minor 不低於 skill。"""
    current = read_agents_md_version(project_root)
    if current is None:
        return ['docs/AGENTS.md 缺少有效的流程契約版本']
    available = tuple(map(int, current.split('.')))
    errors = []
    for name, skill_file in find_skills(project_root):
        with open(skill_file, encoding='utf-8') as f:
            body = f.read()
        if 'docs/AGENTS.md' not in body:
            continue
        match = re.search(r'本 skill 需要 `docs/AGENTS\.md` \*\*流程契約 ([0-9]+\.[0-9]+)\*\*', body)
        if not match:
            errors.append(f'skills/{name}/SKILL.md 缺少最低流程契約宣告')
            continue
        required = tuple(map(int, match.group(1).split('.')))
        if available[0] != required[0] or available[1] < required[1]:
            errors.append(f'skills/{name}/SKILL.md 需要流程契約 {match.group(1)}，專案為 {current}')
    return errors


def check_rules_parity(project_root):
    """檢查中英版規則檔的 ## 章節數是否一致，防止單邊修改造成漂移"""
    counts = {}
    for fname in ('AGENTS.md', 'AGENTS.zh-TW.md'):
        path = os.path.join(project_root, 'rules', fname)
        with open(path, encoding='utf-8') as f:
            counts[fname] = sum(1 for line in f if line.startswith('## '))
    if counts['AGENTS.md'] != counts['AGENTS.zh-TW.md']:
        return [f"雙語規則章節數不一致：rules/AGENTS.md 有 {counts['AGENTS.md']} 節，"
                f"rules/AGENTS.zh-TW.md 有 {counts['AGENTS.zh-TW.md']} 節（兩檔必須同步修改）"]
    return []


def check_install_paths(project_root):
    """檢查 scripts/install.sh 的目標路徑與兩份 README 安裝表格中該平台那一列一致

    路徑的真相來源是兩份 README，install.sh 是它們的可執行副本。單邊改動會讓
    腳本裝到錯的位置且不會報錯（settings.local.json 曾殘留 Antigravity 遷移前的
    舊路徑）。比對限定在表格中該平台的那一列——全文比對會被「舊版路徑為 ...」
    這類遷移說明矇混過去。本檢查為單向：README 有而腳本沒有的平台不會被抓出來。
    """
    display_names = {
        'claude': 'Claude Code',
        'antigravity': 'Antigravity',
        'opencode': 'OpenCode',
        'cursor': 'Cursor',
    }

    errors = []
    script = os.path.join(project_root, 'scripts', 'install.sh')
    if not os.path.isfile(script):
        return ['缺少 scripts/install.sh']

    with open(script, encoding='utf-8') as f:
        content = f.read()

    # 取出各 README 安裝表格中「| **平台** | ... |」的那一列
    readmes = {}
    for kind, rel in (('rules', 'rules/README.md'),
                      ('skills', 'skills/README.md')):
        rows = {}
        with open(os.path.join(project_root, rel), encoding='utf-8') as f:
            for line in f:
                if not line.startswith('|'):
                    continue
                for platform, display in display_names.items():
                    if f'**{display}**' in line:
                        rows[platform] = line.strip()
        readmes[kind] = (rel, rows)

    # targets_for() 中每個平台一行：platform) echo "<rules>|<skills>" ;;
    parsed = re.findall(r'^\s*(\w+)\)\s+echo "([^"]*\|[^"]*)" ;;', content, re.M)
    if not parsed:
        return ['無法從 scripts/install.sh 的 targets_for() 解析出平台路徑（格式是否改過？）']

    for platform, spec in parsed:
        if platform not in display_names:
            errors.append(f"scripts/install.sh 有未知平台「{platform}」，check_install_paths 不知道它在 README 的表格名稱")
            continue
        targets = spec.split('|')
        if len(targets) != 2:
            errors.append(f"scripts/install.sh 的 {platform} 路徑應為「<rules>|<skills>」兩欄，實際為 {len(targets)} 欄")
            continue
        for kind, target in zip(('rules', 'skills'), targets):
            if target == '-':
                continue  # 該平台不以檔案方式安裝這類內容
            expected = target.replace('$HOME', '~')
            rel, rows = readmes[kind]
            if platform not in rows:
                errors.append(f"{rel} 的安裝表格找不到 **{display_names[platform]}** 那一列，無從比對 install.sh 的路徑")
            elif expected not in rows[platform]:
                errors.append(
                    f"scripts/install.sh 的 {platform} {kind} 路徑「{expected}」"
                    f"與 {rel} 表格不符（路徑異動時兩邊必須一起改）\n"
                    f"       README: {rows[platform]}")
    return errors


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors = (check_skill_names(project_root)
              + check_agents_md_declarations(project_root)
              + check_rules_parity(project_root)
              + check_install_paths(project_root))
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print("OK: skill frontmatter 完整且 name 一致，skill 的最低流程契約相容，雙語規則章節數一致，install.sh 安裝路徑與 README 一致。")
