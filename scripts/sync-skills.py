#!/usr/bin/env python3
import os
import re
import shutil
import sys


def find_pairs(project_root):
    """掃描 skills 目錄，回傳 (skill 名稱, SKILL.md 路徑, workflow 目標路徑) 清單"""
    skills_dir = os.path.join(project_root, 'skills')
    workflows_dir = os.path.join(project_root, 'workflows', 'shared')
    pairs = []
    for item in sorted(os.listdir(skills_dir)):
        skill_file = os.path.join(skills_dir, item, 'SKILL.md')
        if os.path.isfile(skill_file):
            pairs.append((item, skill_file, os.path.join(workflows_dir, f"{item}.md")))
    return pairs


def sync_skills(project_root):
    workflows_dir = os.path.join(project_root, 'workflows', 'shared')
    os.makedirs(workflows_dir, exist_ok=True)

    synced_count = 0
    for name, skill_file, target_file in find_pairs(project_root):
        try:
            shutil.copy2(skill_file, target_file)
            print(f"Synced: {os.path.relpath(skill_file, project_root)} -> {os.path.relpath(target_file, project_root)}")
            synced_count += 1
        except Exception as e:
            print(f"Error syncing {name}: {e}")

    print(f"\nSuccessfully synced {synced_count} skills to workflows/shared.")


def check_sync(project_root):
    """檢查所有配對是否同步，有漂移則回傳錯誤清單"""
    errors = []
    pairs = find_pairs(project_root)
    skill_names = set()

    for name, skill_file, target_file in pairs:
        skill_names.add(name)
        if not os.path.isfile(target_file):
            errors.append(f"缺少對應工作流：workflows/shared/{name}.md（請執行 sync-skills.py）")
            continue
        with open(skill_file, encoding='utf-8') as f1, open(target_file, encoding='utf-8') as f2:
            if f1.read() != f2.read():
                errors.append(f"內容漂移：skills/{name}/SKILL.md != workflows/shared/{name}.md（請執行 sync-skills.py）")

    # 反向檢查：shared 中不該有沒有對應 skill 的孤兒檔
    workflows_dir = os.path.join(project_root, 'workflows', 'shared')
    for fname in sorted(os.listdir(workflows_dir)):
        if fname.endswith('.md') and fname[:-3] not in skill_names:
            errors.append(f"孤兒工作流：workflows/shared/{fname} 沒有對應的 skill（skill 已改名或刪除？）")

    return errors


def read_frontmatter_name(skill_file):
    """取出 SKILL.md frontmatter 中的 name，找不到回傳 None"""
    with open(skill_file, encoding='utf-8') as f:
        lines = f.read().splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line.startswith('name:'):
            return line[len('name:'):].strip()
    return None


def check_skill_names(project_root):
    """檢查每個 SKILL.md 的 frontmatter 具備 name: 且與資料夾名一致

    OpenCode 與 Antigravity 要求 frontmatter 具備 name:，缺少時整份 skill 會
    靜默不載入（2.4.0 修過一次）；此檢查防止同一問題回歸。
    """
    errors = []
    for name, skill_file, _ in find_pairs(project_root):
        fm_name = read_frontmatter_name(skill_file)
        if fm_name is None:
            errors.append(f"skills/{name}/SKILL.md 的 frontmatter 缺少 name:（OpenCode / Antigravity 會靜默不載入）")
        elif fm_name != name:
            errors.append(f"skills/{name}/SKILL.md 的 name: 為「{fm_name}」，必須等於資料夾名「{name}」")
    return errors


def read_agents_md_version(project_root):
    """取出 docs/AGENTS.md 檔尾的 `**文件版本**: X.Y`，找不到回傳 None"""
    path = os.path.join(project_root, 'docs', 'AGENTS.md')
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        content = f.read()
    m = re.findall(r'\*\*文件版本\*\*:\s*([0-9]+\.[0-9]+)', content)
    return m[0] if m else None


def check_agents_md_declarations(project_root):
    """檢查引用 docs/AGENTS.md 的 skill 都宣告了依據版本，且與該檔當前版本一致

    「核心層齊備性檢查」需要兩端的版本才能比對：docs/AGENTS.md 檔尾一端，
    skill 的宣告一端。缺 skill 那端時該檢查無法執行（1.13 的缺口）。
    """
    errors = []
    current = read_agents_md_version(project_root)
    if current is None:
        return ['無法從 docs/AGENTS.md 讀出 `**文件版本**`，skill 版本宣告無從比對']

    for name, skill_file, _ in find_pairs(project_root):
        with open(skill_file, encoding='utf-8') as f:
            body = f.read()
        if 'docs/AGENTS.md' not in body:
            continue  # 未引用規範的 skill 不需宣告
        m = re.search(r'本 skill 依據 `docs/AGENTS\.md` \*\*([0-9]+\.[0-9]+)\*\*', body)
        if not m:
            errors.append(
                f"skills/{name}/SKILL.md 引用了 docs/AGENTS.md 但未宣告依據版本"
                f"（需於 frontmatter 後加「本 skill 依據 `docs/AGENTS.md` **{current}**」，"
                f"否則核心層齊備性檢查無法比對兩端）")
        elif m.group(1) != current:
            errors.append(
                f"skills/{name}/SKILL.md 宣告依據 docs/AGENTS.md {m.group(1)}，"
                f"但該檔目前為 {current}（改動規範後需同步更新各 skill 的宣告）")
    return errors


def read_description(skill_file):
    """取出 SKILL.md frontmatter 中的 description，找不到回傳 None"""
    with open(skill_file, encoding='utf-8') as f:
        lines = f.read().splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line.startswith('description:'):
            return line[len('description:'):].strip()
    return None


def first_sentence(text):
    """取第一句（以全形句號斷句，去除結尾句號）；無句號則整段視為首句"""
    return text.split('。')[0].strip()


def check_workflow_readme(project_root):
    """檢查 workflows/README.md 的 Shared Workflows 清單是否與各 SKILL.md 的 description 首句一致

    workflows/README.md 不在 sync-skills 的逐位元組複製範圍內，描述文字容易單邊漂移，
    因此約定：清單中每條描述必須等於對應 SKILL.md description 的第一句。
    """
    errors = []
    readme = os.path.join(project_root, 'workflows', 'README.md')
    if not os.path.isfile(readme):
        return [f"缺少 workflows/README.md"]

    with open(readme, encoding='utf-8') as f:
        lines = f.read().splitlines()

    # 只解析 "## Shared Workflows" 到下一個 "## " 之間的清單
    listed = {}
    in_section = False
    for line in lines:
        if line.startswith('## '):
            in_section = line.strip() == '## Shared Workflows'
            continue
        if in_section:
            m = re.match(r'^- \*\*(?P<name>[\w-]+)\.md\*\* - (?P<desc>.+?)\s*$', line)
            if m:
                listed[m.group('name')] = m.group('desc')

    expected = {}
    for name, skill_file, _ in find_pairs(project_root):
        desc = read_description(skill_file)
        if desc is None:
            errors.append(f"skills/{name}/SKILL.md 的 frontmatter 缺少 description")
            continue
        expected[name] = first_sentence(desc)

    for name in sorted(set(expected) - set(listed)):
        errors.append(f"workflows/README.md 漏列 {name}.md（Shared Workflows 清單需與 skills/ 一一對應）")
    for name in sorted(set(listed) - set(expected)):
        errors.append(f"workflows/README.md 多列 {name}.md，但沒有對應的 skill（已改名或刪除？）")
    for name in sorted(set(expected) & set(listed)):
        if listed[name] != expected[name]:
            errors.append(
                f"workflows/README.md 的 {name}.md 描述與 SKILL.md description 首句不一致\n"
                f"       README: {listed[name]}\n"
                f"       應為  : {expected[name]}")

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


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if '--check' in sys.argv:
        errors = (check_sync(project_root)
                  + check_skill_names(project_root)
                  + check_agents_md_declarations(project_root)
                  + check_workflow_readme(project_root)
                  + check_rules_parity(project_root))
        if errors:
            for e in errors:
                print(f"FAIL: {e}")
            sys.exit(1)
        print("OK: 所有 skill/workflow 配對已同步，frontmatter name 一致，skill 的 docs/AGENTS.md 版本宣告一致，workflows/README.md 描述一致，雙語規則章節數一致。")
    else:
        sync_skills(project_root)
