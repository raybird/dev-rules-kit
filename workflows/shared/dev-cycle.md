---
description: 以 issue 為中心追蹤並推進具 Gherkin BDD、TDD 紅綠燈與審查硬性卡關的開發閉環，支援查詢進度或自動執行下一步
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

## 分級判定

讀取 `docs/issues/issue-{ID}/README.md` 結尾 metadata 的 `**分級**` 欄位，決定任務清單來源（分級規則的權威定義見 `docs/AGENTS.md`「文件動態分級規範」，下表為摘要）：

| 分級 | 任務清單來源 | decompose |
|---|---|---|
| Small | README 的「實作與驗證步驟」 | 跳過 |
| Medium | `implementation-plan.md` 的「實作步驟」 | 跳過 |
| Large | 拆解後的 Decomposition 文件 | 需要 |

若 README 沒有 `**分級**` 欄位（舊文件），依實際存在的檔案依序回推（三條互斥且涵蓋所有組合，取第一個成立者）：

1. 存在 `requirement-analysis.md` 或 `technical-analysis.md` → **Large**
2. 否則存在 `implementation-plan.md` → **Medium**
3. 否則 → **Small**

回推後將分級補寫回 README。

README 的 `**風險**` 欄位只影響任務順序與驗證方式，**不影響是否執行 `decompose` 或任何狀態偵測分支**。舊 issue 缺少 `**風險**` 時，不得由分級或現存檔案推測；只有重新規劃或新增步驟時，才依 `docs/AGENTS.md` 重新評估並補寫。

## 狀態偵測

依序檢查下列條件，第一個成立的條件即為當前階段：

| 偵測條件 | 下一步 |
|---|---|
| `docs/issues/issue-{ID}/README.md` 不存在 | `new-issue` |
| README 無具唯一 Scenario ID 的標準 Gherkin，或核准紀錄缺少 `已核准` 狀態、日期、完整 Scenario ID 清單、Gherkin SHA-256、來源，或重算 hash 不符 | `new-issue`（繼續澄清與核准，不得實作） |
| 分級為 Large 且 `docs/issues/issue-{ID}/` 內無含「Decomposition」標題的 `.md` 檔 | `decompose` |
| 任務清單有未完成項目，或指定項目缺少 BDD 紅燈、單元測試紅燈、最小實作後全綠、重構後全綠證據 | `execute-task` |
| 無含 issue ID 的 branch 或 commit（搜尋 branch 名稱與 commit message） | `execute-task` |
| PR 已 merged | 完成 |
| 無 open PR | `create-pr` |
| open PR body 的 Proof of Test Scenario ID 集合與 README 核准清單不完全相等，或 Gherkin hash 不符 | `create-pr`（更新 PR 說明，不得進入 review） |
| PR reviews / comments 中沒有針對目前 PR HEAD SHA 的持久化 review artifact | `review`（對話中的報告或舊 commit review 不構成證據） |
| 目前 HEAD 的 review 結果為 `RETURN TO execute-task`／request changes，或有 MUST FIX、架構違規、測試作弊、Scenario／必要邊界漏洞 | `execute-task`（修正後產生新 commit，再審查新 HEAD） |
| 目前 HEAD 的 review 結果為 `PASS` | 等待合併 |

紅綠燈證據必須包含 Scenario ID、實際命令、exit code 或結果摘要及與目標行為相關的失敗／成功原因。只有狀態符號、commit 存在或「測試通過」文字不得讓流程前進。純文件等例外必須具有 `docs/AGENTS.md` 要求的不適用理由與替代驗證證據。Scenario 集合比較採完全相等，不只檢查核准 ID 是否存在，也拒絕任何額外未核准 ID。

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
   | decompose | 呼叫 `decompose`（僅 Large） |
   | execute-task | 依「分級判定」取得任務清單，詢問要執行哪個步驟 / Phase / Task 後，呼叫 `execute-task` |
   | create-pr | 確認所有 Task 已完成、紅綠燈證據齊全並已 commit 後，呼叫 `create-pr`；Proof of Test 未完整覆蓋核准 Scenario ID 時更新 PR body |
   | review | 對目前 PR HEAD 呼叫 `review` 並將報告持久化至 PR；只有該 SHA 的持久化 `PASS` artifact 才能等待合併，`RETURN TO execute-task` 修正並產生新 commit 後重新審查 |
   | execute-task（修正） | 說明「目前 HEAD 的 review 未通過，需修正並建立新 commit 後重新審查」，呼叫 `execute-task` |
   | 完成 | 依 `docs/AGENTS.md` 收尾 issue 文件：README 狀態標記為已完成、timeline 補記 merge 日期，然後恭喜並結束 |

4. 子步驟完成後回到步驟 1 繼續偵測
5. 循環直到 PR merged 或使用者中斷

## 推進模式下的自動執行

推進模式由 dev-cycle 全自動驅動，不需人工把關：

- `execute-task` 只有在 Gherkin、BDD 紅燈、單元測試紅燈、最小實作後全綠及重構後全綠證據齊全時，才依 `code-simplify` 精煉程式碼、依 `create-commit` 規範生成訊息並**直接執行 commit**
- `create-pr` 在 Superpowers 可用時先通過 `verification-before-completion`，未安裝時改通過 `create-pr` 內建 Completion Gate；兩種模式都必須確認 PR body 含可追溯的完整 Proof of Test，才可**直接建立或更新 PR**
- `review` 只有在獨立 reviewer 的報告成功保存為目前 HEAD 的 PR review / comment 時才接受結果；`UNPERSISTED` 必須停止
- `create-commit` 的「不要直接提交、訊息放 code block 供複製」僅適用於**單獨呼叫**該 skill 時；在 dev-cycle 推進模式下不適用
- 自動模式不得把使用者沉默視為 Gherkin 核准，也不得自動核准測試契約變更；遇到這兩種 gate 必須暫停並詢問
