# 使用 Commit 數量審查程式碼實作計畫

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 `review` 工作流程與技能的基準從 `git diff dev...HEAD` 改為以指定的 Commit 數量 `COMMIT_COUNT` 進行 `git diff HEAD~{COMMIT_COUNT} HEAD` 審查。

**Architecture:** 同步修改 `workflows/shared/review.md` 與 `skills/review/SKILL.md`，並使用 `diff -qw` 驗證其內容的一致性。

**Tech Stack:** Markdown, Git

---

### Task 1: 修改工作流程與技能檔

**Files:**
- Modify: `workflows/shared/review.md`
- Modify: `skills/review/SKILL.md`

- [ ] **Step 1: 修改 workflows/shared/review.md**
  更新 `Input` 參數以新增 `COMMIT_COUNT`，並將 `Review Scope` 與 `Pre-analysis` 內部的 `git diff` 指令從 `git diff dev...HEAD` 替換為以 `COMMIT_COUNT` 指向的 `git diff HEAD~{COMMIT_COUNT} HEAD`。

- [ ] **Step 2: 修改 skills/review/SKILL.md**
  進行與 Step 1 完全相同的內容修改，確保兩份檔案的結構與文字完全一致。

- [ ] **Step 3: 驗證檔案內容同步性**
  在專案根目錄下執行 diff 驗證指令：
  Run: `diff -qw workflows/shared/review.md skills/review/SKILL.md`
  Expected: 無任何輸出或只回傳成功（無差異）。

- [ ] **Step 4: 提交變更**
  Run:
  ```bash
  git add workflows/shared/review.md skills/review/SKILL.md
  git commit -m "docs(review): change review diff target from dev branch to commit count"
  ```
