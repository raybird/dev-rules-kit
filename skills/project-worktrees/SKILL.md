---
name: project-worktrees
description: 建立或移除開發、審查用的 git worktree；使用者要為 issue 開 worktree、檢出他人分支或已合併提交來審查、清理 worktree 時使用。
---

## 專案慣例

動手前依序從 `docs/agents/project.md`、`git worktree list` 與既有分支名取得 worktree 位置、分支命名、基準分支與遠端認證方式。都沒有定義時使用預設：

| 項目 | 預設 |
|---|---|
| 開發用位置 | 主 repo 同層目錄 `<repo 名>-<issue>` |
| 審查用位置 | 主 repo 同層目錄 `<repo 名>-<issue>-review` |
| 開發分支 | issue 編號加描述，如 `342-member-login` |
| 基準分支 | 現有 PR 或專案設定的 base；無法確定才詢問 |

完成判準：路徑、分支名與基準分支都能指出來源（專案文件、既有慣例或上表預設）。

## 遠端存取

所有 fetch 加上 `GIT_TERMINAL_PROMPT=0`，讓缺少認證時立即失敗，而不是停在帳密輸入。

需要 token 時，以 credential helper 從環境變數提供，讓 token 留在命令列參數、remote URL 與輸出之外：

```bash
GIT_TOKEN="$(<讀取 token 的專案命令>)" GIT_TERMINAL_PROMPT=0 \
  git -c credential.helper= \
      -c credential.helper='!f() { echo username=<平台使用者名>; echo "password=$GIT_TOKEN"; }; f' \
      fetch origin <ref>
```

取 token 的方式與使用者名依專案文件；找不到認證方式時回報失敗訊息，請使用者提供。

## 建立開發用 worktree

1. `git fetch origin <base>`。
2. 確認目標路徑不存在；`git branch --list <branch>` 已有同名分支時，確認它屬於此 issue 後改用 `git worktree add <path> <branch>` 檢出，不屬於則回報衝突。
3. `git worktree add --no-track <path> -b <branch> origin/<base>`；upstream 留待首次 `git push -u` 設定，移除前的未推送檢查才會比對到此分支自己的遠端。

完成判準：回報路徑、分支與基準 commit（`git -C <path> log -1 --oneline`），且 `git -C <path> status --short` 為空。

## 建立審查用 worktree

審查用 worktree 一律 `--detach` 檢出，不建立本地分支，移除後不留殘餘。

- **未合併的遠端分支**：以 `git ls-remote --heads origin` 找出含 issue 編號的分支，多個候選時詢問。`git fetch origin <branch> <base>` 後執行 `git worktree add --detach <path> origin/<branch>`；BASE 為 `git merge-base origin/<base> origin/<branch>`。
- **已合併的提交**：`git fetch origin <base>` 後以 `git log origin/<base> --oneline -E --grep='#<issue>([^0-9]|$)'` 找出提交，逐一確認屬於該 issue。以最新一筆執行 `git worktree add --detach <path> <sha>`；BASE 為最早一筆的父提交 `<sha>^`。

完成判準：回報路徑、HEAD SHA 與 BASE SHA；兩者即 `review` 的固定審查範圍。

## 移除 worktree

1. 檢查 `git -C <path> status --short`；有 upstream 的分支另查 `git -C <path> log @{upstream}..HEAD --oneline`，沒有 upstream 的分支比對它與 `origin/<base>` 的差異。有未提交或未推送的內容時列出並詢問處理方式，worktree 保留到使用者決定。
2. `git worktree remove <path>`。`--force` 只在使用者看過上一步清單並同意捨棄後使用。
3. 開發分支預設保留；使用者要求刪除時，已合併用 `git branch -d`，未合併先確認再用 `-D`。

完成判準：`git worktree list` 不再含該路徑，並回報剩餘的 worktree 清單。
