---
description: 分析目前分支與基準分支的差異，並自動整理 Squash 的 Commit 訊息與提供合併建議
---

當使用者執行此指令時，請依照以下步驟執行：

1. **確認目前分支與基準分支**：
   - 檢查目前的本地分支名稱，並確認基準分支（預設為 `dev`，若不存在則使用 `main` 或 `master`）。
   - 檢查工作區狀態（`git status`），確認是否有未提交的變更，並提醒使用者。

2. **分析 Commit 歷史**：
   - 執行 `git log <base-branch>..HEAD --oneline` 取得當前分支相較於基準分支多出來的所有 commit 紀錄。
   - 若無任何差異，告知使用者目前分支已與基準分支同步。

3. **生成 Squash Commit 訊息**：
   - 分析上述 commits 的訊息，將其歸納為結構化的 Commit 訊息。
   - 格式必須符合專案規範：`#<issue_number> <type>(<scope>): <subject>`（例如 `#3403 feat(member): 實作...`）。
   - 在 Body 中依範疇（如 docs, feat, refactor, fix）條列說明具體的異動內容。

4. **提供合併方案（git merge --squash）**：
   - 一律使用 `git merge --squash` 方案進行合併，避免互動式 rebase 的複雜操作。
   - 提供以下步驟指令：
     1. 切換至基準分支：`git checkout <base-branch>`
     2. 進行 Squash 合併：`git merge --squash <your-branch>`
     3. 進行 Commit 提交（直接提供帶有生成好 Commit 訊息的 `git commit -m "..."` 指令，確保 `#` 符號完美保留）。
