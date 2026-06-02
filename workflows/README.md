# Workflows

此目錄包含各種開發工作流程（workflows），用於標準化開發流程。

## 目錄結構

```
workflows/
├── shared/           # 共通工作流程
└── antigravity/      # Antigravity 平台特定工作流程
```

## Shared Workflows

共通工作流程可於所有平台使用：

- **code-simplify.md** - 在保留所有功能的前提下，簡化並精煉程式碼，提升清晰度、一致性與可維護性
- **create-commit.md** - 根據 git staged 生成符合 commit convention 1.0.0 規範的精簡版條列訊息
- **create-pr.md** - 根據指定 commit 生成 peer-request 內容
- **decompose.md** - 將 Implementation Plan 細化為可執行的開發階段（Phase）與任務（Task）
- **execute-task.md** - 根據 Implementation Plan Decomposition 執行指定的 Phase 或 Task
- **git-squash.md** - 分析目前分支與基準分支的差異，並自動整理 Squash 的 Commit 訊息與提供合併建議
- **new-issue.md** - 依照目前專案既有的 coding style 與架構需求分析新需求
- **review.md** - 審查當前分支提交的程式碼變更，確認是否符合需求並提出改進建議

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
