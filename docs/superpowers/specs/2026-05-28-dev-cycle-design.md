# dev-cycle Skill 設計規格

**日期**：2026-05-28  
**狀態**：待實作

## 背景

`dev-rules-kit` 的 README 中記錄了一個由七個 skill 組成的開發閉環：

```
new-issue → decompose → execute-task → code-simplify → create-commit → create-pr → review → (循環或完成)
```

本設計的目標是新增一個 `dev-cycle` orchestration skill，以 issue 為中心追蹤整個閉環狀態，支援查詢目前進度或自動推進到下一步，同時保持七個子 skill 可獨立使用。

## 設計決策

### 特例：僅建 SKILL.md，不建 workflow 對應檔

`dev-cycle` 是一個 orchestration skill，其核心能力是「理解自然語言意圖 + 讀取環境狀態 + 呼叫子 skill」。這三件事在任何載入此 SKILL.md 的 AI 平台上都能運作，不需要平台特定的 workflow 版本。

其他平台（Windsurf、OpenCode、Antigravity）可直接載入 `skills/dev-cycle/SKILL.md` 作為規則或 context，AI 同樣能回應自然語言觸發並執行閉環流程。

這是本 repo 第一個不建 `workflows/shared/` 對應檔的 skill（詳見 CLAUDE.md 維護規則更新）。

### 以 Issue 文件與 Git 為狀態機

狀態完全從 filesystem + git 讀取，無需額外狀態儲存。閉環七個階段的判斷依據如下：

| 偵測條件（依序檢查） | 代表下一步 |
|---|---|
| `docs/issues/issue-{ID}/README.md` 不存在 | `new-issue` |
| `docs/issues/issue-{ID}/` 內無含「Decomposition」標題的 `.md` 檔 | `decompose` |
| 無含 issue ID 的 branch 或 commit（搜尋 branch 名稱與 commit message） | `execute-task` |
| 無 open PR | `create-pr` |
| PR 有 request changes | `execute-task`（修正） |
| PR open，無 review | `review` |
| PR merged | 完成 |

`code-simplify` 與 `create-commit` 沒有獨立可偵測的 artifact，歸入 execute-task 階段的子步驟，不單獨列為狀態。

### 模式偵測

從使用者輸入的措辭判斷意圖，不需要額外旗標：

- **查詢模式**：輸入含疑問詞或狀態關鍵字（到哪了、狀態、進度、如何、了嗎）
- **推進模式**：輸入為指令語氣或純 issue ID（`/dev-cycle 3396`、`繼續 3396`）

### 平台中性執行語言

子步驟呼叫一律寫「呼叫 `[skill-name]`」，不指定機制：
- Claude Code：透過 `Skill` 工具載入並執行
- 其他平台：AI 自行以可用機制執行（讀取 workflow 檔或直接遵循指示）

## SKILL.md 規格

### 輸入

使用者提供 issue ID，可以是自然語言或指令語氣。若未提供 issue ID，詢問使用者。

### 查詢模式流程

1. 偵測當前階段
2. 輸出狀態摘要：
   ```
   Issue {ID}：{標題}
   目前階段：{階段名稱}
   狀態：{一句話摘要}
   ```
3. 結束，不推進

### 推進模式流程

1. 偵測當前階段
2. 告知使用者「目前在 [階段]，準備執行 [下一步]」
3. 呼叫對應 skill
4. 完成後依以下條件確認再回到步驟 1：
   - `execute-task` 前：詢問要執行哪個 Phase / Task
   - `create-pr` 前：確認所有 Task 已完成並 commit
   - `review` 後有 request changes：明確說明「需修正，回到 execute-task」
5. 直到 PR merged 或使用者中斷

## 需更新的現有檔案

- `CLAUDE.md`：新增段落說明 orchestration skill 不建 workflow 對應檔的原則
- `README.md`：在開發閉環章節補充 `dev-cycle` 的說明

## 不在本次範圍內

- 修改任何現有的七個 skill/workflow
- 建立 `workflows/shared/dev-cycle.md`
- 跨 session 的狀態持久化（狀態完全依賴 filesystem + git）
