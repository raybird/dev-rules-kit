# Workflows

此目錄包含各種開發工作流程（workflows），用於標準化開發流程。

## 目錄結構

```
workflows/
├── shared/           # 共通工作流程
└── antigravity/      # Antigravity 平台特定工作流程
```

## Shared Workflows

共通工作流程可於所有平台使用。

> 下列每條描述必須與對應 `skills/<name>/SKILL.md` 之 `description` 的**第一句**完全相同，
> 由 `python3 scripts/sync-skills.py --check` 驗證。修改 description 時請一併更新此清單。

- **code-simplify.md** - 在保留所有功能的前提下，簡化並精煉程式碼，提升清晰度、一致性與可維護性
- **create-commit.md** - 根據 git staged 的異動生成符合 Conventional Commits 規範的中文 commit 訊息
- **create-pr.md** - 根據指定 commit 範圍與實際通過的驗收標準證據生成 Pull Request 說明
- **decompose.md** - 將 Large issue 的 Gherkin 與 Implementation Plan 細化為 BDD 外迴圈、TDD 內迴圈及可執行的 Phase / Task
- **dev-cycle.md** - 以 issue 為中心追蹤並推進具驗收標準、測試證據與獨立審查卡關的開發閉環，支援查詢進度或自動執行下一步
- **execute-task.md** - 依驗收標準的 BDD 外迴圈與 TDD 內迴圈執行指定的 issue 步驟或 Phase / Task，取得紅綠燈或等價證據後實作最少程式碼
- **git-squash.md** - 分析目前分支與基準分支的差異，並自動整理 Squash 的 Commit 訊息與提供合併建議
- **new-issue.md** - 透過蘇格拉底式澄清將需求轉成使用者核准的驗收標準，並在 docs/issues/issue-{ID}/ 建立 issue 文件
- **review.md** - 以獨立批判者審查當前分支的驗收標準覆蓋、測試證據、架構符合度與程式碼變更，發現漏洞時退回實作

## Platform-Specific Workflows

### Antigravity

- **fix-webview-conflict.md** - 清除 Antigravity 與 Windsurf 衝突導致的 WebView 快取與 Service Worker 錯誤

## 使用方式

根據您的 IDE 平台選擇對應的工作流程，或使用 shared/ 目錄中的共通工作流程。

### 平台路徑對應

根據各平台官方文件：

- **Antigravity**: 預設路徑為 `global_workflows/`，目前支援 shared/ 共通工作流及 antigravity/ 平台特定工作流
- **OpenCode**: 預設路徑為 `commands/` 或 `.opencode/commands/`，目前支援 shared/ 共通工作流（原平台特定工作流已整合至 shared/）
- **Windsurf**:
  - Workspace: `.windsurf/workflows/*.md`（在當前工作區、子目錄或父目錄直到 git root）
  - Global: `~/.codeium/windsurf/global_workflows/*.md`（在機器上的所有工作區可用）
  - 目前支援 shared/ 共通工作流
