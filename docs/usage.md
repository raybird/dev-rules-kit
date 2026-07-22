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

**關鍵行為**：需求有模糊地帶時（例如「帳號衝突如何處理？」），AI 會在文件中明確標注「未知，待確認」，並分別記錄規模、風險、首要驗證與完成證據，而非自行填入假設。

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

**關鍵行為**：此例的最大未知是 callback 與本地帳號流程能否端到端成立，所以選擇垂直切片。若未知只有 Google API 的欄位或錯誤碼，應先做最小真實請求的契約驗證，不必先串完整登入流程。垂直切片是候選手段，不是風險優先的預設答案。

---

### Step 3 — `execute-task`

**觸發**：

```
/execute-task Phase 1 Task 1.1
```

**AI 產出**：

實作 Phase 1 Task 1.1（設定 Google OAuth 憑證與環境變數），修改相關檔案，在對話中輸出：
- 修改摘要
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

```
標題：feat(auth): 新增 Google OAuth 2.0 登入支援

## 變更內容
- 新增 OAuth callback 路由與 token 交換邏輯
- 新增帳號建立／綁定流程
- UI 加入 Google 登入按鈕

## 測試方式
- [ ] 全新帳號透過 Google 登入，確認本地帳號建立
- [ ] 已有帳號透過 Google 登入，確認正確綁定
- [ ] 撤銷 token 後重新登入，確認處理正確
```

**關鍵行為**：PR 內容基於實際 git diff 生成，不會描述未實作的功能。

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

**關鍵行為**：`dev-cycle` 從 filesystem 與 git 狀態推斷進度，跨 session 重新呼叫也能正確恢復，不依賴對話記憶。

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
| **注意** | 分別評估規模與風險：`**分級**` 決定文件與 `decompose`，`**風險**` 決定首要驗證及完成證據；兩軸不得互相推導 |

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
| **注意** | **僅適用 Large**；先辨識最大未知並比較驗證手段，不預設採用垂直切片。需先有 `implementation-plan.md`；Task 粒度控制在 1–3 小時 |

---

### `execute-task`

| | |
|---|---|
| **觸發** | `/execute-task Phase {N} Task {N.M}`（Large）或 `/execute-task 步驟 {N}`（Small / Medium） |
| **產出** | 實作對應步驟 / Task 的程式碼變更，輸出修改摘要 |
| **注意** | 一次執行一個步驟 / Task；任務清單來源依分級而定（Small 讀 README、Medium 讀 implementation-plan、Large 讀 decomposition） |

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
| **產出** | PR 標題與 body 草稿（變更摘要 + 測試清單） |
| **注意** | 基於實際 git diff 生成；需要時可帶入指定 commit 範圍 |

---

### `review`

| | |
|---|---|
| **觸發** | `/review {commit 數量}` |
| **產出** | 審查報告，分 MUST FIX / NICE TO HAVE / LGTM 三級 |
| **注意** | 提供 `TASK_DESCRIPTION` 可讓 AI 更準確判斷需求符合度 |

---

### `dev-cycle`

| | |
|---|---|
| **查詢** | 「issue {ID} 到哪了」、「{ID} 進度」 |
| **推進** | `/dev-cycle {ID}`、「繼續 {ID}」 |
| **注意** | 依 README 的 `**分級**` 欄位分流：僅 Large 經過 `decompose`；本技能在所有平台均已提供對應的引導工作流程 |

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
| 2026-07-22 | Issue 評估改為規模與風險雙軸；補上驗證手段選擇及垂直切片適用條件 | - |
| 2026-07-21 | 補上分級分流說明（僅 Large 經過 decompose）；示範的 decompose 產出改為垂直切片 | - |
| 2026-06-20 | 整合 USAGE.md 說明內容，修復大小寫檔案衝突 | - |
| 2026-05-19 | 建立 new-issue 使用說明文件與指南 | - |

---

**建立日期**: 2026-05-19  
**最後更新**: 2026-07-22\
**文件版本**: 1.3
