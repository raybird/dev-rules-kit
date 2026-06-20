#!/usr/bin/env python3
import os
import shutil

def sync_skills():
    # 獲取專案根目錄（腳本所在目錄的上一層）
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = os.path.join(project_root, 'skills')
    workflows_dir = os.path.join(project_root, 'workflows', 'shared')

    if not os.path.exists(skills_dir):
        print(f"Error: skills directory not found at {skills_dir}")
        return

    os.makedirs(workflows_dir, exist_ok=True)
    
    synced_count = 0
    # 掃描 skills 目錄下所有子資料夾
    for item in sorted(os.listdir(skills_dir)):
        item_path = os.path.join(skills_dir, item)
        if os.path.isdir(item_path):
            skill_file = os.path.join(item_path, 'SKILL.md')
            if os.path.exists(skill_file):
                target_file = os.path.join(workflows_dir, f"{item}.md")
                try:
                    shutil.copy2(skill_file, target_file)
                    print(f"Synced: {os.path.relpath(skill_file, project_root)} -> {os.path.relpath(target_file, project_root)}")
                    synced_count += 1
                except Exception as e:
                    print(f"Error syncing {item}: {e}")

    print(f"\nSuccessfully synced {synced_count} skills to workflows/shared.")

if __name__ == '__main__':
    sync_skills()
