# dev-rules-kit

[繁體中文](README.md) | English

Empower AI coding agents with a verifiable, evidence-based development workflow: clarify requirements upfront, prove completion with real test outputs, and conduct independent code reviews—leaving an auditable trace at every step.

Supports **Codex**, **Claude Code**, **OpenCode**, **Antigravity**, and **Cursor**.

## What It Does for You

- **Clarify Requirements Upfront**: High-level prompts are transformed into structured, approvable acceptance criteria. The agent only asks questions that impact the outcome—batching independent questions together, isolating major trade-offs, and providing recommended options so you can simply reply "use recommendations" to proceed.
- **Evidence-Based Completion**: Behavior changes require failing tests first, followed by implementations that turn them green. Tasks cannot be marked done without genuine test execution outputs.
- **Independent Code Review**: Pull requests are reviewed by an independent reviewer role without implementation bias, generating archived review reports. If independent review capability is unavailable in the environment, it honestly reports limitations rather than faking compliance.
- **Cross-Session Continuity**: Development state and verification evidence are recorded in issue documents and Git history. Simply say "continue issue 101" in a new session to resume exactly where you left off.
- **Lightweight for Quick Tasks**: Everyday trivial changes bypass the heavy process. Full workflows are only enforced for tracked issues. If you are in a rush, explicit workflow exemptions are respected and documented.
- **Preserve Project Customizations**: Project-specific configurations reside in `docs/agents/project.md` and are never overwritten during kit updates.

## Quick Start

### Let Your AI Agent Install It (Recommended)

Open your AI coding agent in your project directory and send:

```text
Please install dev-rules-kit following https://github.com/raybird/dev-rules-kit/blob/main/INSTALL.md and initialize this project.
```

The agent will follow [INSTALL.md](INSTALL.md) to fetch the kit, install skills, and initialize project documents—showing you dry-run diffs before applying any changes. If the agent lacks Internet access, clone the repository to `~/Tools/dev-rules-kit` first, then instruct the agent to read `INSTALL.md` from that local directory.

### Manual Installation

Prerequisites: `git`, `bash`, and `python3`:

```bash
git clone https://github.com/raybird/dev-rules-kit.git ~/Tools/dev-rules-kit
bash ~/Tools/dev-rules-kit/scripts/install.sh                          # Install skills into detected platforms
python3 ~/Tools/dev-rules-kit/scripts/init-project.py /path/to/project  # Initialize project documents
```

Both commands support `--dry-run` to inspect actions beforehand. Optional general behavior rules can be installed as described in [rules/README.md](rules/README.md).

## Daily Workflow

Start a new agent session after installation and drive the process naturally:

| What you want to do | What to say to the agent |
|---|---|
| Create a new issue | `/new-issue issue:101 topic:Fix empty string validation content:Empty string should show required error` |
| Progress automatically | `/dev-cycle 101` or "Continue working on issue 101" |
| Check progress only (read-only) | "Where is issue 101 at?" |
| Review current changes | `/review` |
| Answer agent questions | "Use recommendations" (or answer question by question) |
| Speed up for this run | "Skip Gherkin this time", "No need to write tests first" |

`dev-cycle` chains the workflow together, pausing to report when human decisions, merges, or external acceptance are needed:

```text
new-issue → decompose (Large issues only)
          → execute-task (Test, implement, refine)
          → create-commit → create-pr → review
                                          └─ On rejection: return to execute-task and re-review
```

Each skill can also be executed individually. For full workflows and detailed skill descriptions, see the [Usage Guide](docs/usage.md).

## Updates

Simply tell your agent: `"Please update dev-rules-kit according to INSTALL.md"`. It will pull the latest version, update skills and project documents, and summarize highlights from [CHANGELOG.md](CHANGELOG.md).

For manual updates:

```bash
git -C ~/Tools/dev-rules-kit pull
bash ~/Tools/dev-rules-kit/scripts/install.sh
python3 ~/Tools/dev-rules-kit/scripts/init-project.py /path/to/project --update
```

Updates only overwrite unmodified core documents; if local modifications exist, the operation halts with a conflict report rather than partially writing. Copied global rules are not auto-updated. Check CHANGELOG for Major versions.

## Learn More

| Topic | Reference |
|---|---|
| Complete workflow, queries & waiting states, PR & review | [docs/usage.md](docs/usage.md) |
| Behavior rules installation & Claude Code mounting | [rules/README.md](rules/README.md) |
| Skills directory & target platform paths | [skills/README.md](skills/README.md) |
| Companion tools: Serena, GitNexus; Superpowers (optional) | [docs/setup/tools.md](docs/setup/tools.md) |
| Downstream document specifications (Tiers, approvals, verification, review) | [docs/AGENTS.md](docs/AGENTS.md) |
| Maintaining this kit | [AGENTS.md](AGENTS.md) |

## License

MIT © Raybird
