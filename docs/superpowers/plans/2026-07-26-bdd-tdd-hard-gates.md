# BDD + TDD 硬性卡關實作計畫

> **For agentic workers:** When available, prefer `subagent-driven-development` or `executing-plans`; otherwise execute this plan task-by-task with the same checkpoints. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將可追溯的 Gherkin BDD 外迴圈、TDD 內迴圈與 Superpowers 完成 gate 整合進既有開發閉環。

**Architecture:** `docs/AGENTS.md` 定義 issue 文件與證據契約，雙語 `rules/` 定義全域底線，各核心 skill 執行單一節點 gate，`dev-cycle` 負責跨節點狀態轉移。所有 shared workflows 由同步腳本從 skills 單向產生。

**Tech Stack:** Markdown、YAML frontmatter、Gherkin、Superpowers skills、Python 3 同步與檢查腳本

---

### Task 1：建立權威 BDD 文件契約

**Files:**
- Modify: `docs/AGENTS.md`

- [x] 定義 Scenario ID、標準 Gherkin 語法、各分級存放位置與非程式任務例外。
- [x] 將 Gherkin 與雙迴圈證據加入 README／Implementation Plan 規範及完成檢查清單。
- [x] 使用系統日期更新版本與 Changelog。

### Task 2：加入全域 BDD + TDD 底線

**Files:**
- Modify: `rules/AGENTS.md`
- Modify: `rules/AGENTS.zh-TW.md`

- [x] 在兩份規則的相同位置加入一一對應章節。
- [x] 規定共識、Gherkin、紅燈、最小實作、重構與防作弊 gate。

### Task 3：強化規劃節點

**Files:**
- Modify: `skills/new-issue/SKILL.md`
- Modify: `skills/decompose/SKILL.md`

- [x] `new-issue` 在 `brainstorming` 可用時優先調用，否則執行內建澄清 gate，並輸出具 Scenario ID 的 Gherkin。
- [x] `decompose` 在 `writing-plans` 可用時優先調用，否則執行內建規劃 gate，建立 BDD 外迴圈與 TDD 內迴圈追蹤。

### Task 4：強化執行、審查與 PR 節點

**Files:**
- Modify: `skills/execute-task/SKILL.md`
- Modify: `skills/review/SKILL.md`
- Modify: `skills/create-pr/SKILL.md`

- [x] `execute-task` 落實 test-driven-development 的紅綠重構狀態機與防作弊條款。
- [x] `review` 要求獨立審查、架構符合度與至少三個破壞性邊界案例。
- [x] `create-pr` 只以可追溯通過證據產生 Gherkin Proof of Test。

### Task 5：封閉跨節點繞過路徑

**Files:**
- Modify: `skills/dev-cycle/SKILL.md`
- Modify: `CLAUDE.md`
- Modify: `workflows/README.md`

- [x] `dev-cycle` 在狀態偵測與自動推進時檢查 Gherkin、紅綠燈及 review gate。
- [x] `CLAUDE.md` 記錄實際 Superpowers 技能映射與維護原則。
- [x] 若 skill description 首句改變，同步更新 workflow 清單。

### Task 6：同步與驗證

**Files:**
- Generate: `workflows/shared/new-issue.md`
- Generate: `workflows/shared/decompose.md`
- Generate: `workflows/shared/execute-task.md`
- Generate: `workflows/shared/review.md`
- Generate: `workflows/shared/create-pr.md`
- Generate: `workflows/shared/dev-cycle.md`

- [x] 執行 `python3 scripts/sync-skills.py`，預期顯示 9 個 skills 全部同步。
- [x] 執行 `python3 scripts/sync-skills.py --check`，預期輸出 `OK`。
- [x] 執行 `python3 scripts/check-links.py`，預期無失效 Markdown 相對連結。
- [x] 檢查 diff，確認 workflow 僅由同步產生且未修改無關檔案。
