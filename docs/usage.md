# 使用指南

這套 kit 提供一組可跨平台重用的 rules、workflows 與 skills，讓 AI agent 在你的開發環境中按照一致的工作流程運作——從需求分析、實作規劃、程式碼撰寫，到 commit、PR、review，形成一個完整的開發閉環。

**前置條件**：請先依照你使用的平台完成安裝：[Claude Code](./setup/claude.md) · [Windsurf](./setup/windsurf.md) · [OpenCode](./setup/opencode.md) · [Antigravity](./setup/antigravity.md)

---

## 完整閉環示範

以「為現有 web app 新增 OAuth 登入功能」（issue-101）為例，完整走過七個步驟。

### Step 1 — `new-issue`

**觸發**：

```
/new-issue issue:101 主題:新增 OAuth 登入 內容:使用者目前只能用帳號密碼登入，需要支援 Google OAuth 2.0 登入流程，登入後取得 profile 資訊並建立或綁定本地帳號
```

**AI 產出**：

建立 `docs/issues/issue-101/`，輸出四份文件：
- `README.md`：需求概覽、timeline
- `requirement-analysis.md`：使用者流程、新舊行為差異、待確認事項
- `technical-analysis.md`：OAuth 2.0 flow 分析、相關模組、潛在風險
- `implementation-plan.md`：高階實作方向

**關鍵行為**：需求有模糊地帶時（例如「帳號衝突如何處理？」），AI 會在文件中明確標注「未知，待確認」，而非自行填入假設。

---

### Step 2 — `decompose`

**觸發**：

```
/decompose
```

AI 讀取 `docs/issues/issue-101/implementation-plan.md` 後自動執行。

**AI 產出**：

建立 `docs/issues/issue-101/implementation-plan-decomposition.md`：

- **Phase 1 — OAuth 基礎建設**（Google API 設定、callback 路由）
- **Phase 2 — 帳號整合**（建立/綁定本地帳號邏輯）
- **Phase 3 — UI 整合**（登入按鈕、錯誤訊息）

每個 Phase 下細分 2–4 個 Task，每個 Task 預估 1–3 小時。

**關鍵行為**：Task 有明確的「預期產出」，讓開發者知道何時算完成，避免無邊界的工作。

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

---

## 各 Skill 快速參考

### `new-issue`

| | |
|---|---|
| **觸發** | `/new-issue issue:{編號} 主題:{標題} 內容:{描述}` 或直接描述需求 |
| **產出** | `docs/issues/issue-{ID}/` 下四份文件（README、requirement-analysis、technical-analysis、implementation-plan） |
| **注意** | 需求不足時列出待確認事項，不自行補假設 |

---

### `decompose`

| | |
|---|---|
| **觸發** | `/decompose` |
| **產出** | `docs/issues/issue-{ID}/implementation-plan-decomposition.md`，Phase + Task 結構 |
| **注意** | 需先有 `implementation-plan.md`；Task 粒度控制在 1–3 小時 |

---

### `execute-task`

| | |
|---|---|
| **觸發** | `/execute-task Phase {N} Task {N.M}` |
| **產出** | 實作對應 Task 的程式碼變更，輸出修改摘要 |
| **注意** | 一次執行一個 Task；需先有 decomposition 文件 |

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
| **注意** | Orchestration skill，不出現在 `/` 指令清單；非 Claude 平台需手動載入 `skills/dev-cycle/SKILL.md` |
