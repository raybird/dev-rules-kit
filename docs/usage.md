# 使用指南

這套 kit 提供一組可跨平台重用的 rules、workflows 與 skills，讓 AI agent 在你的開發環境中按照一致的工作流程運作——從需求分析、實作規劃、程式碼撰寫，到 commit、PR、review，形成一個完整的開發閉環。

**前置條件**：請先依照你使用的平台完成安裝：[Claude Code](./setup/claude.md) · [Windsurf](./setup/windsurf.md) · [OpenCode](./setup/opencode.md) · [Antigravity](./setup/antigravity.md)

---

## 完整閉環示範

以「為現有 web app 新增 OAuth 登入功能」（issue-101）為例，完整走過七個步驟。

> 此範例的規模為 **Large**、風險為 **High**。Large 來自跨模組與登入架構整合，因此包含 Step 2 的 `decompose`；High 來自真實 callback 與帳號綁定行為尚未確認，因此首要活動必須取得解除該未知的證據。**Small 與 Medium 的 issue 會跳過 `decompose`**，風險高低不會改變文件數量。詳見 [AGENTS.md 的「文件動態分級規範」](./AGENTS.md#文件動態分級規範-issue-document-tiering)。

### Step 1 — `new-issue`

**觸發**：

```
/new-issue issue:101 主題:新增 OAuth 登入 內容:使用者目前只能用帳號密碼登入，需要支援 Google OAuth 2.0 登入流程，登入後取得 profile 資訊並建立或綁定本地帳號
```

**AI 產出**：

建立 `docs/issues/issue-101/`。由於此任務涉及 OAuth 與架構整合，規模被評估為 **Large**，因而建立完整四份文件；真實 callback 與帳號綁定行為尚未確認，風險另評估為 **High**：
- `README.md`：需求概覽、timeline
- `requirement-analysis.md`：使用者流程、新舊行為差異、待確認事項
- `technical-analysis.md`：OAuth 2.0 flow 分析、相關模組、潛在風險
- `implementation-plan.md`：高階實作方向

README 另包含經使用者核准、具 `SCN-001` 等唯一 ID 的 Gherkin 驗收劇本。

**關鍵行為**：若已安裝 Superpowers，AI 優先調用 `brainstorming`；否則執行 `new-issue` 的內建等價流程。兩種模式都一次只問一個問題，需求有模糊地帶時不自行填入假設，只有使用者核准 Gherkin 後才建立完整文件。

---

### Step 2 — `decompose`

> 此步驟**僅適用 Large issue**。Small 與 Medium 的實作步驟已經是可執行的任務清單，會直接跳到 Step 3。

**觸發**：

```
/decompose
```

AI 讀取 `docs/issues/issue-101/implementation-plan.md` 後自動執行。

**AI 產出**：

建立 `docs/issues/issue-101/implementation-plan-decomposition.md`：

- **Phase 1 — 登入最小路徑**（登入按鈕 → Google callback → 取得真實 profile → 建立新帳號 → 登入成功）
- **Phase 2 — 既有帳號綁定與衝突處理**（Step 1 標為「未知，待確認」的部分）
- **Phase 3 — 錯誤處理與邊界情境**（授權被拒、email 未驗證、token 過期）

每個 Phase 下細分 2–4 個 Task，每個 Task 預估 1–3 小時。

每個 Task 都標示所覆蓋的 Scenario ID，並明列 BDD 外迴圈（feature、Step Definitions、紅燈命令）與 TDD 內迴圈（單元測試、紅燈命令、最小實作及全綠命令）。

**關鍵行為**：此例的最大未知是 callback 與本地帳號流程能否端到端成立，所以選擇垂直切片。若未知只有 Google API 的欄位或錯誤碼，應先做最小真實請求的契約驗證，不必先串完整登入流程。垂直切片是候選手段，不是風險優先的預設答案。

---

### Step 3 — `execute-task`

**觸發**：

```
/execute-task Phase 1 Task 1.1
```

**AI 產出**：

若已安裝 Superpowers，AI 優先調用 `test-driven-development`；否則依 `execute-task` 內建流程，依序取得 BDD 紅燈、單元測試紅燈、最少 production code 全綠及重構後全綠。對話輸出：
- 修改摘要
- Scenario ID 與 BDD／單元測試紅燈證據
- 最小實作後與重構後的全綠證據
- 需要人工處理的事項（如：申請 Google API key）

完成後，AI 視程式碼複雜度決定是否建議 `code-simplify`，並執行 `create-commit` 產生 commit 訊息。

> **子步驟說明**：`code-simplify` 是選用步驟，AI 在判斷變更幅度或複雜度較高時才會提議。`create-commit` 依據 staged 差異產生符合 Conventional Commits 格式的 commit 訊息。

---

### Step 4 — `create-pr`

**觸發**：所有 Task 完成並 commit 後：

```
/create-pr
```

**AI 產出**：

產生 PR 標題與 body 草稿：

````markdown
標題：feat(auth): 新增 Google OAuth 2.0 登入支援

## 變更內容
- 新增 OAuth callback 路由與 token 交換邏輯
- 新增帳號建立／綁定流程
- UI 加入 Google 登入按鈕

## 測試通過證明 (Proof of Test)

### SCN-001：全新帳號透過 Google 登入
```gherkin
Scenario: 全新帳號完成 Google 登入
  Given 使用者尚未建立本地帳號
  When 使用者完成 Google 授權
  Then 系統建立本地帳號並完成登入
```
- BDD 命令：`npm test -- oauth-login.feature`
- 結果：PASS
````

**關鍵行為**：PR 內容基於實際 git diff 生成，不會描述未實作的功能；只有可追溯至核准 Gherkin 原文與實際成功命令的 Scenario 才會列入 Proof of Test。

---

### Step 5 — `review`

**觸發**：

```
/review 5
```

（5 代表本次 PR 包含 5 個 commit）

**AI 產出**：

審查報告分三級：

- **MUST FIX**：OAuth token 未在登出時 revoke，存在 token 洩漏風險
- **NICE TO HAVE**：callback error message 可以更具體
- **LGTM**：帳號綁定邏輯、環境變數處理方式正確

報告另由獨立 reviewer 檢查架構分層、BDD / TDD 證據與測試作弊，並列出至少 3 個破壞性邊界案例。存在任何 MUST FIX、Scenario 漏洞或必要邊界未覆蓋時，流程判定為 `RETURN TO execute-task`。

> **循環示範**：review 發現 MUST FIX 問題，開發者回到 `execute-task` 修正 token revoke 邏輯，再執行 `create-commit` 補上 fix commit，重新 `create-pr` 更新 PR 說明，最後再跑一次 `review` 確認問題已解決，第二次 review 通過。

---

### Step 6 — `dev-cycle`（以同一情境示範）

**查詢模式**（任何時間點可用）：

```
issue 101 到哪了
```

AI 輸出：

> Issue 101：新增 OAuth 登入
> 目前階段：create-pr
> 狀態：所有 Task 已完成並 commit，尚未開 PR

**推進模式**：

```
/dev-cycle 101
```

AI 自動偵測狀態，告知「目前在 create-pr 階段，準備執行 create-pr」，呼叫 `create-pr` 後繼續循環。

**關鍵行為**：`dev-cycle` 從 filesystem、issue 證據、git 狀態與持久化 PR review / comment 推斷進度，跨 session 重新呼叫也能正確恢復，不依賴對話記憶；缺 Gherkin 核准 hash、紅綠燈證據、完整 Proof of Test 或目前 HEAD 的持久化 review PASS 時都不會跳到下一階段。

**分級分流**：`dev-cycle` 會先讀 `README.md` 的 `**分級**` 欄位決定路徑——Large 才經過 `decompose`，Small 與 Medium 直接從 `new-issue` 進入 `execute-task`。若是舊 issue 沒有該欄位，會依現存檔案回推分級並補寫回 README。

**風險排序**：README 的 `**風險**` 欄位只影響任務順序與驗證方式，不形成新的 `dev-cycle` 分支。舊 issue 缺少風險時不由分級推測，只有重新規劃或新增步驟時才補評估。

兩軸可以自由組合：

- **Small + High**：單行權限條件修正仍只產出 README，但第一步先建立能重現越權問題的回歸案例。
- **Large + Low**：規格已凍結的跨模組機械式搬移仍建立完整文件並執行 `decompose`，但可按一般技術相依順序執行。

---

## 各 Skill 快速參考

### `new-issue`

| | |
|---|---|
| **觸發** | `/new-issue issue:{編號} 主題:{標題} 內容:{描述}` 或直接描述需求 |
| **產出** | 依任務複雜度評估為 **Small (僅 README)**、**Medium (README + 計畫)** 或 **Large (完整四件套)** 檔案 |
| **注意** | 可用時優先使用 `brainstorming`，否則執行內建等價流程；兩種模式都須一次一題並取得 Gherkin 核准 |

#### 指令式參數格式範例：
```
/new-issue
issue:123
主題:怎麼開始與調整網站
內容:
我們需要評估目前網站首頁的載入效能，並提出優化方案。
主要問題包括：
1. 首頁載入時間超過 5 秒
2. 多個未壓縮的圖片資源
3. 沒有使用快取策略
```

*註：在指令式介面中，`issue:`、`主題:` 和 `內容:` 三個欄位都是必填的。其中 `issue:` 的編號應為純數字（例如：123，而非 ISSUE-123）。*


---

### `decompose`

| | |
|---|---|
| **觸發** | `/decompose` |
| **產出** | `docs/issues/issue-{ID}/implementation-plan-decomposition.md`，Phase + Task 結構 |
| **注意** | **僅適用 Large**；可用時優先使用 `writing-plans`，否則由內建規則把每個 Scenario 映射至 BDD / TDD 雙迴圈 |

---

### `execute-task`

| | |
|---|---|
| **觸發** | `/execute-task Phase {N} Task {N.M}`（Large）或 `/execute-task 步驟 {N}`（Small / Medium） |
| **產出** | 實作對應步驟 / Task 的程式碼變更，輸出修改摘要 |
| **注意** | 可用時優先使用 `test-driven-development`；不論是否安裝，未取得 BDD 與單元測試紅燈前都禁止修改 production code |

---

### `code-simplify`

| | |
|---|---|
| **觸發** | `/code-simplify` 或 AI 主動建議 |
| **產出** | 精煉近期修改的程式碼，提升可讀性與一致性 |
| **注意** | 保留所有功能，只改善品質；預設聚焦近期修改 |

---

### `create-commit`

| | |
|---|---|
| **觸發** | `/create-commit` |
| **產出** | 依 staged 差異生成 Conventional Commits 格式的 commit 訊息 |
| **注意** | 執行前需先 `git add` 想提交的檔案 |

---

### `create-pr`

| | |
|---|---|
| **觸發** | `/create-pr` |
| **產出** | PR 標題與 body 草稿（變更摘要 + Gherkin Proof of Test） |
| **注意** | 可用時優先使用 `verification-before-completion`，否則執行內建證據檢查；只有具實際成功證據的 Scenario 才列為通過 |

---

### `review`

| | |
|---|---|
| **觸發** | `/review {commit 數量}` |
| **產出** | 獨立審查報告、架構符合度、至少 3 個破壞性邊界案例與流程判定 |
| **注意** | 可用時優先使用 `requesting-code-review`，否則使用宿主原生獨立 reviewer；無獨立審查能力時不得 PASS |

---

### `dev-cycle`

| | |
|---|---|
| **查詢** | 「issue {ID} 到哪了」、「{ID} 進度」 |
| **推進** | `/dev-cycle {ID}`、「繼續 {ID}」 |
| **注意** | 依分級分流，並檢查 Gherkin 核准、紅綠燈、Proof of Test 與 review gate，禁止跨階段繞過 |

---

## 常見問題 (Q&A)

**Q：如果我在執行 new-issue 時忘記提供某個參數會怎樣？**
A: 系統會透過自然語言對話方式，逐步詢問引導您提供缺失的資訊。

**Q：我可以修改產出的文件嗎？**
A: 可以，而且非常鼓勵這麼做！`new-issue` 只是提供一個基礎結構與起點，您應該根據專案實際情況，手動或透過其他 skill 來修改與補充文件內容。

**Q：如何確保我的 issue 文件格式正確？**
A: 請參考 [docs/AGENTS.md](./AGENTS.md) 中的「快速檢查清單」以及各文件類型的具體格式範例。

---

## 維護紀錄

| 日期 | 異動 | 負責人 |
|------|------|--------|
| 2026-07-26 | Superpowers 改為選用增強；未安裝時由本地 skills 執行等價硬性 gate | - |
| 2026-07-26 | 開發閉環加入 Gherkin BDD、TDD 紅綠燈、獨立審查與 PR Proof of Test 硬性卡關 | - |
| 2026-07-22 | Issue 評估改為規模與風險雙軸；補上驗證手段選擇及垂直切片適用條件 | - |
| 2026-07-21 | 補上分級分流說明（僅 Large 經過 decompose）；示範的 decompose 產出改為垂直切片 | - |
| 2026-06-20 | 整合 USAGE.md 說明內容，修復大小寫檔案衝突 | - |
| 2026-05-19 | 建立 new-issue 使用說明文件與指南 | - |

---

**建立日期**: 2026-05-19  
**最後更新**: 2026-07-26\
**文件版本**: 1.3
