# Task Completion

- Run the sync check command:
  ```bash
  for n in code-simplify create-commit create-pr decompose new-issue review execute-task; do
    diff -qw "skills/$n/SKILL.md" "workflows/shared/$n.md"
  done
  ```
- Ensure no diff exists for the modified files.
- Commit all changes to the git repository.