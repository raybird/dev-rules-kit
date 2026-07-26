---
description: 根據指定 commit 範圍與實際通過的 Gherkin Scenario 證據生成 Pull Request 說明。變更已提交、準備以 Proof of Test 供 reviewer 驗收時使用。
---

## Input Evidence

依序取得以下證據：

1. 使用者指定的 commit 範圍；未指定或無法確認時先詢問，不自行選擇。
2. 該範圍的 commit 訊息、淨 diff 與異動檔案清單。
3. 可取得的 issue、需求、任務或設計文件。
4. 實際執行的測試與驗證紀錄。
5. issue README 中核准的 Gherkin、完整 Scenario ID 清單、Gherkin SHA-256，以及各 Scenario 的 BDD / 單元測試全綠證據；先依 `docs/AGENTS.md` 重算 hash，確認劇本內容未在核准後異動。符合非程式任務例外者，改取得不適用理由、替代驗證命令或步驟及成功結果。
6. 若已安裝 Superpowers，優先調用 `verification-before-completion`；未安裝時依本 skill 的 Evidence Rules 與 Completion Gate 逐項重跑命令、讀取最新輸出並核對證據。缺少套件不構成阻塞，但任一驗證失敗或無法取得最新證據時必須停止，不得生成看似已驗收的 PR 說明。

## Evidence Rules

- **Why**：只能來自需求、issue、任務文件或可辨識的 commit 意圖。來源不足時明寫「需求背景未提供」，只陳述能由 diff 證實的目的，不反向捏造動機。
- **How**：只能描述淨 diff 與相關文件能證實的實作方式及決策。無法證實決策理由時省略理由。
- **實際變更**：以淨 diff 為準，涵蓋新增、修改、刪除、rename、測試與文件變更。
- **測試驗證**：只有實際紀錄才能標示為已執行或通過。沒有證據時使用下方固定的未執行格式。
- **Proof of Test 完整性**：README 核准紀錄中的每個 Scenario ID 都必須各有一個 Proof 區塊，且集合必須完全一致；不可省略缺證據的 Scenario、加入未核准 Scenario，或只用一個案例代表其餘案例。
- **核准完整性**：重算的 Gherkin SHA-256 必須與 README 核准紀錄一致；hash 不符時停止並退回 `new-issue`，不得產生 Proof of Test。
- **自動化證據**：一般任務只有同時具備核准 Gherkin、Scenario ID、實際 BDD 命令與成功輸出及相關單元測試成功輸出才能列為通過。單元測試不能取代 BDD 驗收證據；不得把待測 checkbox 當成通過證明。
- **替代證據**：只有 issue 計畫已依 `docs/AGENTS.md` 記錄無可執行行為／測試入口的不適用理由時，才可列出可重複的靜態命令或手動步驟與實際成功結果；不得把此例外用於存在測試入口的產品行為。
- 所有檔案路徑使用相對於 repo root 的路徑；指出位置時附行號。不得輸出絕對路徑或 `~` 開頭路徑。

## Output

將完成的 Markdown 放在 code block 內供複製，使用以下結構：

````markdown
## 背景描述 (Why)

<有來源的需求背景；若來源不足，明確標示需求背景未提供及可確認的目的>

## 實作方法 (How)

<由淨 diff 與文件證實的實作方法及架構決策>

## 實際變更（做了什麼）

- <可由淨 diff 證實的主要變更>

### 測試驗證

<有證據時列出實際命令或案例與結果；沒有證據時改用：>

- **未執行**：<未執行的檢查>
- **原因**：<可證實的原因>
- **殘餘風險**：<合併前仍需確認的事項>

### 測試通過證明 (Proof of Test)

- **Gherkin SHA-256**：`<README 核准紀錄中的 hash>`

#### <SCN-NNN：Scenario 名稱>

```gherkin
<issue 文件中核准的 Scenario 原文>
```

- **BDD 命令**：`<實際執行命令>`
- **結果**：PASS（<可追溯的成功摘要>）
- **底層測試**：`<實際執行的相關單元測試命令與成功摘要>`

<!-- 非程式任務只在符合權威例外時，以「替代驗證」與「不適用理由」取代 BDD 命令及底層測試；最終輸出移除此註解。 -->
````

截圖或錄影、補充說明、相關連結只有在有實質內容時才加入；不適用時整段省略。

## Completion Gate

輸出前逐項確認：

- commit 範圍有效，且所有淨變更都已檢查。
- Why、How、變更與測試的每項事實都有可追溯來源。
- 未執行的測試已列出原因與殘餘風險，沒有暗示其已通過。
- 目前 Gherkin 的 SHA-256 與核准紀錄一致，且 Proof of Test 的 Scenario ID 集合與 README 核准紀錄完全一致；每個 Scenario 都能追溯至 issue 原文及最新自動化成功輸出，或符合權威例外的替代驗證。任一項不符時停止，不輸出 PR 說明。
- 所有範例 placeholder 與 HTML 註解都已移除。
- 選用區塊沒有空標題，檔案路徑均為 repo-relative。

任一項未通過時先補正或標示限制，不輸出看似完整但無證據的 PR 說明。
