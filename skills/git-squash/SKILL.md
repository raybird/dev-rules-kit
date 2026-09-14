---
name: git-squash
description: 分析目前分支與基準分支的差異，並自動整理 Squash 的 Commit 訊息與提供合併建議
---

當使用者執行此指令時，請依照以下步驟執行：

1. **確認目前分支與基準分支**：
   - 檢查目前的本地分支名稱，並確認基準分支（優先讀現有 PR 與專案設定，無法確定才詢問）。
   - 檢查工作區狀態（`git status`），確認是否有未提交的變更，並提醒使用者。

2. **分析 Commit 歷史**：
   - 執行 `git log <base-branch>..HEAD --oneline` 取得當前分支相較於基準分支多出來的所有 commit 紀錄。
   - 若無任何差異，告知使用者目前分支已與基準分支同步。

3. **生成 Squash Commit 訊息**：
   - 分析淨 diff 與上述 commits 的訊息，將其歸納為結構化的 Commit 訊息。
   - 訊息格式依 `create-commit` 的專案優先與預設格式；issue 編號預設放 footer `Refs: #ID`，不固定前綴。
   - 在 Body 中依範疇（如 docs, feat, refactor, fix）條列說明具體的異動內容。
   - 訊息中若提及檔案路徑，一律使用**相對於 repo root 的路徑**（如 `src/auth/login.ts`），不得使用絕對路徑或 `~` 開頭的路徑。

4. **提供合併方案（git merge --squash）**：
   - 依專案合併策略提供方案；允許本機 squash 時可用下列 `git merge --squash`。受保護或要求 PR 的目標分支，提供平台合併步驟。只提供命令，明確要求執行時才執行。
   - **三個步驟必須各自獨立成一個 code block**，讓使用者能逐步複製執行，不要合併成單一 block，也不要與說明文字混排。
   - 所有動態 Shell 參數（基準分支、功能分支、subject、body）一律使用 POSIX shell 單引號包住，避免 `$()`、backtick、變數與雙引號被 Shell 展開。
   - 動態內容中的每個單引號 `'` 必須轉成 `'\''`：先結束單引號、以反斜線引用該字元，再重新開始單引號。例如 `feature/o'brien` 必須輸出成 `'feature/o'\''brien'`。
   - 輸出前逐一檢查所有動態參數；任一值未安全引用時，不得輸出可執行命令。
   - 依下列格式輸出（分支名稱與訊息替換為實際內容）：

````markdown
**Step 1 — 切換至基準分支**

```bash
git checkout 'dev'
```

**Step 2 — Squash 合併**

```bash
git merge --squash 'feature/your-branch'
```

**Step 3 — 提交**

```bash
git commit -m 'feat(member): 實作會員登入流程' -m '- feat: 新增 OAuth 授權與 callback 處理
- refactor: 抽離 session 建立邏輯
- docs: 補充環境變數設定說明' -m 'Refs: #3403'
```
````

   - Step 3 分別用 `-m` 傳入 subject、body 與 issue footer；動態訊息含多行時也可寫到暫存檔，以 `git commit -F` 使用。
