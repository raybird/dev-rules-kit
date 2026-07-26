# Superpowers 選用整合實作計畫

> **For agentic workers:** When available, prefer `subagent-driven-development` or `executing-plans`; otherwise execute this plan task-by-task with the same checkpoints. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 讓 dev-rules-kit 在未安裝 Superpowers 時仍以本地規則執行完整 BDD + TDD 硬性閉環。

**Architecture:** 本地 skills 擁有 gate 的權威定義，Superpowers 僅作為已安裝時的優先流程實作。README 說明推薦能力與平台安裝入口，shared workflows 仍由同步腳本產生。

**Tech Stack:** Markdown、YAML frontmatter、Superpowers skills、Python 3 同步與連結檢查腳本

---

### Task 1：解除外部套件硬依賴

**Files:**
- Modify: `skills/new-issue/SKILL.md`
- Modify: `skills/decompose/SKILL.md`
- Modify: `skills/execute-task/SKILL.md`
- Modify: `skills/review/SKILL.md`
- Modify: `skills/create-pr/SKILL.md`

- [x] 將「無法調用即停止」改為「可用時優先調用，否則執行內建等價流程」。
- [x] 保留所有證據、獨立性、完整性與退回條件。

### Task 2：同步全域規則與維護指引

**Files:**
- Modify: `rules/AGENTS.md`
- Modify: `rules/AGENTS.zh-TW.md`
- Modify: `docs/AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `docs/usage.md`

- [x] 明確區分選用 Superpowers 與強制本地 gate。
- [x] 維持雙語章節一一對應。

### Task 3：補充根 README

**Files:**
- Modify: `README.md`

- [x] 說明 Superpowers 非必要依賴，建議安裝完整套件。
- [x] 列出五個核心對應與五個建議輔助 skills。
- [x] 連結既有五個平台 setup 文件，不重複安裝命令。

### Task 4：同步與驗證

**Files:**
- Generate: `workflows/shared/new-issue.md`
- Generate: `workflows/shared/decompose.md`
- Generate: `workflows/shared/execute-task.md`
- Generate: `workflows/shared/review.md`
- Generate: `workflows/shared/create-pr.md`

- [x] 執行 `python3 scripts/sync-skills.py`。
- [x] 執行 `python3 scripts/sync-skills.py --check`。
- [x] 執行 `python3 scripts/check-links.py` 與 `git diff --check`。
