# Suggested Commands

- Sync Verification:
  ```bash
  for n in code-simplify create-commit create-pr decompose new-issue review execute-task; do
    diff -qw "skills/$n/SKILL.md" "workflows/shared/$n.md"
  done
  ```