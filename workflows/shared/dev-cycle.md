---
name: dev-cycle
description: 以 issue 為中心追蹤並推進具驗收標準、測試證據與獨立審查卡關的開發閉環，支援查詢進度或自動執行下一步
---

> 本 skill 依據 `docs/AGENTS.md` **1.15**。專案的該檔版本低於此值、或引用的章節不存在或語意不符時，依「核心層齊備性檢查」明確說出缺什麼並停下來問，不得自行套用預設值繼續。
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
| README 缺少該規模與風險對應的驗收標準或其核准紀錄（Small 為輕量驗收條件加核准日期與來源，風險 Medium / High 另需核准 commit；Medium / Large 為具唯一 Scenario ID 的 Gherkin 加核准 commit 與逐項核准表——未分批時的單行核准紀錄視同全表 `已核准`，見 `docs/AGENTS.md`。既有 Small issue 已採完整 Gherkin 者依其實際形式查核，不因形式規則調整而退回），或核准表沒有任何 `已核准` 項目，或存在 `待重新核准` 項目 | `new-issue`（繼續澄清與核准，不得實作） |
| 分級為 Large 且 `docs/issues/issue-{ID}/` 內無含「Decomposition」標題的 `.md` 檔 | `decompose` |
| 任務清單有未完成項目，或指定項目缺少對應證據（會改變行為者需完整紅綠重構證據，不改變行為者需等價證據） | `execute-task` |
| 無含 issue ID 的 branch 或 commit（搜尋 branch 名稱與 commit message） | `execute-task` |
| README `**狀態**` 為 `等待外部驗收窗`，且記錄的窗口尚未到達 | 等待外部驗收窗（回報預定窗口與待觀察判準，不推進、不判為卡住） |
| README `**狀態**` 為 `不修復` | 完成（依 `docs/AGENTS.md` 確認判定理由與追蹤方式已記錄） |
| PR 已 merged | 完成 |
| 核准表存在 `待核准` 項目 | `new-issue`（補齊剩餘 Scenario 核准，或由使用者裁示刪除該 Scenario，之後再回到 `execute-task`） |
| 無 open PR | `create-pr` |
| open PR body 的 Proof of Test 編號集合與 README 核准清單不完全相等（已記錄豁免者除外） | `create-pr`（更新 PR 說明，不得進入 review） |
| 找不到針對目前 HEAD SHA 的持久化 review artifact（code review 平台或 `docs/issues/issue-{ID}/review-{短SHA}.md`） | `review`（對話中的報告或舊 commit review 不構成證據） |
| 目前 HEAD 的 review 結果為 `RETURN TO execute-task`／request changes，或有 MUST FIX、架構違規、不實回報、驗收標準／必要邊界漏洞 | `execute-task`（修正後產生新 commit，再審查新 HEAD） |
| 目前 HEAD 的 review 結果為 `PASS` | 等待合併 |

紅綠重構證據、等價證據與假綠燈的定義見 `docs/AGENTS.md`。只有狀態符號、commit 存在或「測試通過」文字不得讓流程前進。編號集合比較採完全相等，不只檢查核准編號是否存在，也拒絕任何額外未核准編號。

**規格修訂**：依 `docs/AGENTS.md`「規格修訂的查核」判斷規格是否在核准後被修訂。採完整 Gherkin 時，差異未觸及 Gherkin 不影響任何偵測條件，受影響的 Scenario 退回 `new-issue`，其餘可繼續推進；Small + Medium / High 的輕量驗收條件套用同一查核，被標註 `（待重新核准）` 的條目退回 `new-issue`。Small + Low 沒有核准 commit，不套用查核。規格被修訂本身不是錯誤，未取得同意才是。

**分批核准**：依 `docs/AGENTS.md`「分批核准」，`待核准` 的 Scenario 不阻擋其他已核准 Scenario 的實作——只要核准表至少有一項 `已核准`，閉環就繼續推進到 `execute-task`。`待核准` 在**開 PR 前**才收口：任務推進完畢仍有 `待核准` 時退回 `new-issue`，因此它延後的是核准時機，不是核准要求。

**待確認事項**：`## 待確認事項` 是揭露機制，**不作為任何偵測條件**。仍為 `待確認` 的項目不阻擋 `create-pr`，但 `create-pr` 必須在 PR 揭露；狀態的變更只能來自實際結論或可寫出的判定理由，自動模式下不得為了推進而改寫。

**Gate 豁免**：issue README 的 `## Gate 豁免紀錄` 中已記錄的項目，不再作為卡關條件——該筆紀錄本身即為通過該偵測條件的依據。豁免只對紀錄中明列的項目生效，不擴及其他 gate；沒有紀錄時不得推定豁免。

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
   | create-pr | 確認所有 Task 已完成、證據齊全並已 commit 後，呼叫 `create-pr`；Proof of Test 未完整覆蓋核准的驗收標準時更新 PR body。另依 `docs/AGENTS.md`「常青文件更新責任」確認本次變更觸發的常青文件已更新，未更新時先回到 `execute-task` 補上再開 PR |
   | review | 對目前 PR HEAD 呼叫 `review` 並依 `docs/AGENTS.md` 持久化報告；只有該 SHA 的持久化 `PASS` artifact 才能等待合併，`RETURN TO execute-task` 修正並產生新 commit 後重新審查 |
   | execute-task（修正） | 說明「目前 HEAD 的 review 未通過，需修正並建立新 commit 後重新審查」，呼叫 `execute-task` |
   | 完成 | 依 `docs/AGENTS.md` 收尾 issue 文件：README 狀態標記為已完成、timeline 補記 merge 日期；合併流程含 squash / rebase / amend / cherry-pick 等改寫 hash 的操作時，依「規格修訂的查核」以後續 commit 回填 `**核准 commit**`，並以 `git merge-base --is-ancestor {SHA} {合併目標分支}` 驗證可達（對象為合併目標分支，不是當下 `HEAD`），然後恭喜並結束 |

4. 子步驟完成後回到步驟 1 繼續偵測
5. 循環直到 PR merged 或使用者中斷

## 推進模式下的自動執行

推進模式由 dev-cycle 全自動驅動，不需人工把關：

- `execute-task` 只有在核准的驗收標準與對應證據齊全時，才依 `code-simplify` 精煉程式碼、依 `create-commit` 規範生成訊息並**直接執行 commit**
- `create-pr` 在 Superpowers 可用時先通過 `verification-before-completion`，未安裝時改通過 `create-pr` 內建 Completion Gate；兩種模式都必須確認 PR body 含可追溯的完整 Proof of Test，才可**直接建立或更新 PR**
- `review` 只有在獨立 reviewer 的報告成功持久化為目前 HEAD 的 artifact 時才接受結果；`UNPERSISTED` 必須停止
- `create-commit` 的「不要直接提交、訊息放 code block 供複製」僅適用於**單獨呼叫**該 skill 時；在 dev-cycle 推進模式下不適用
- 自動模式不得把使用者沉默視為驗收標準核准或 gate 豁免，也不得自動核准測試契約變更；遇到這三種情況必須暫停並詢問
- 使用者在推進過程中明確要求跳過某項 gate 時照做，依 `docs/AGENTS.md` 寫入 `## Gate 豁免紀錄` 後才繼續推進
