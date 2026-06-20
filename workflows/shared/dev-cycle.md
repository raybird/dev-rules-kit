---
description: 以 issue 為中心追蹤並推進開發閉環，支援查詢進度或自動執行下一步
---

你是開發閉環的協調者，負責追蹤 issue 從需求分析到 PR 合併的完整生命週期。

## Input

使用者提供 issue ID，可以是自然語言或指令語氣：
- 查詢：「issue 3396 到哪了」、「3396 進度」、「3396 狀態如何」
- 推進：`/dev-cycle 3396`、「繼續 3396」

若未提供 issue ID，詢問使用者後再開始。

## 模式偵測

輸入含疑問詞或狀態關鍵字（到哪了、狀態、進度、如何、了嗎）→ **查詢模式**
否則 → **推進模式**

## 狀態偵測

依序檢查下列條件，第一個不符合的條件即為當前階段：

| 偵測條件 | 下一步 |
|---|---|
| `docs/issues/issue-{ID}/README.md` 不存在 | `new-issue` |
| `docs/issues/issue-{ID}/` 內無含「Decomposition」標題的 `.md` 檔 | `decompose` |
| 無含 issue ID 的 branch 或 commit（搜尋 branch 名稱與 commit message） | `execute-task` |
| 無 open PR | `create-pr` |
| PR 有 request changes | `execute-task`（修正） |
| PR open，無 review | `review` |
| PR merged | 完成 |

## 查詢模式

偵測當前階段後輸出，然後結束，不推進任何步驟：

> Issue {ID}：{標題（從 README.md 第一個 h1 取得，若無則標記「未知」）}
> 目前階段：{階段名稱}
> 狀態：{一句話摘要}

## 推進模式

1. 偵測當前階段
2. 告知「目前在 [階段]，準備執行 [下一步]」
3. 依階段執行：

   | 階段 | 動作 |
   |---|---|
   | new-issue | 呼叫 `new-issue` |
   | decompose | 呼叫 `decompose` |
   | execute-task | 詢問要執行哪個 Phase / Task 後，呼叫 `execute-task` |
   | create-pr | 確認所有 Task 已完成並已 commit 後，呼叫 `create-pr` |
   | review | 呼叫 `review` |
   | execute-task（修正） | 說明「PR 有 request changes，需修正後重新 commit」，呼叫 `execute-task` |
   | 完成 | 恭喜並提示可以 merge PR，結束 |

4. 子步驟完成後回到步驟 1 繼續偵測
5. 循環直到 PR merged 或使用者中斷
