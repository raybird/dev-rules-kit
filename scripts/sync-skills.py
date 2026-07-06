#!/usr/bin/env python3
import os
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
        errors = check_sync(project_root) + check_rules_parity(project_root)
        if errors:
            for e in errors:
                print(f"FAIL: {e}")
            sys.exit(1)
        print("OK: 所有 skill/workflow 配對已同步，雙語規則章節數一致。")
    else:
        sync_skills(project_root)
