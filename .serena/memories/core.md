# Core Map

- Project Type: Markdown templates kit for development rules, workflows, and skills.
- Key Directories:
  - `rules/`: Static agent behavior rules.
  - `workflows/`: Actionable commands and workflows.
  - `skills/`: Claude skills (`SKILL.md` files).
- Key Invariants:
  - `skills/<name>/SKILL.md` and `workflows/shared/<name>.md` are twin copies and must be synchronized on any change. Refer to `mem:conventions` for details.