# 設計規格書：將審查範圍從 dev 分支改為指定 Commit 數量 n

- **建立日期**：2026-05-20
- **作者**：Antigravity
- **狀態**：設計中 (Draft)

## 1. 背景與動機
目前 `review` 技能/工作流程在獲取異動內容時，採用 `git diff dev...HEAD` 指令。這在實際開發中存在以下不便：
1. 本地 `dev` 分支經常未與遠端同步，導致 diff 出來的内容包含其他已合併的變更，開發者必須先執行 `git pull` 更新 `dev`。
2. 某些開發環境或 `git worktree` 下可能不存在本地 `dev` 分支，導致指令執行失敗。

為了改善此體驗，我們將審查基準調整為「由開發者告知總共 $n$ 個 commit」，並透過 `git diff HEAD~n HEAD` 來取得審查範圍。

## 2. 變更範圍與目標
本專案為 Markdown 範本庫，異動目標包含以下兩個互相配對的檔案：
1. `workflows/shared/review.md` (適用於各編輯器/工作流程平台)
2. `skills/review/SKILL.md` (適用於 Claude 技能定義)

此兩份檔案內容應保持完全一致。

## 3. 具體修改設計

### 3.1 `Input` 參數調整
新增 `COMMIT_COUNT` 參數，並說明其格式為正整數 $n$：
```markdown
## Input

| 參數 | 說明 | 範例 |
|------|------|------|
| `COMMIT_COUNT` | 本次審查包含的 Commit 數量（正整數 $n$） | `3` |
| `TASK_DESCRIPTION` | 本次變更的需求描述，可為 ticket 連結、PR title 或手動輸入 | `feat: 新增使用者登入流程` |
```

### 3.2 `Review Scope` 指令調整
更新變更來源之 git 指令：
```markdown
## Review Scope

請根據以下來源取得異動內容進行審查：

- **變更來源**：`git diff HEAD~{COMMIT_COUNT} HEAD`
- **審查對象**：所有受影響之檔案與程式邏輯
- **目標**：確認本次修改是否符合功能需求並維持良好程式品質
```

### 3.3 `Pre-analysis` 預分析指令調整
更新取得異動檔案清單之 git 指令：
```markdown
## Pre-analysis

審查正式開始前，請先執行以下步驟：

1. 執行 `git diff HEAD~{COMMIT_COUNT} HEAD --stat` 取得異動檔案清單
...
```

## 4. 驗證與測試計畫
由於本專案為純 Markdown 範本庫，驗證方式如下：
1. 確保 `workflows/shared/review.md` 與 `skills/review/SKILL.md` 內容完全一致（忽略空白差異）。
2. 在本地開發環境手動執行調整後的 `git diff HEAD~n HEAD` 與 `git diff HEAD~n HEAD --stat` 指令，確保其輸出格式正確符合預期。

## 5. 修訂紀錄 (Changelog)
- **2026-05-20**：初始設計草案建立，並提交評估。
