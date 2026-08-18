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
- **writing-rules.md** - 依注意力成本與觸發機制撰寫或修改 agent 會讀的規範文件
- **review.md** - 以獨立批判者審查當前分支的驗收標準覆蓋、測試證據、架構符合度與程式碼變更，發現漏洞時退回實作

## Platform-Specific Workflows

### Antigravity

- **fix-webview-conflict.md** - 清除 Antigravity 與 Windsurf 衝突導致的 WebView 快取與 Service Worker 錯誤

## 安裝方式

各平台的 slash command 目錄不同，將 `shared/*.md` 複製過去即可（Antigravity 另需複製 `antigravity/*.md`）：

| 平台 | 全域路徑 | 專案層路徑 |
|------|---------|-----------|
| **Windsurf** | `~/.codeium/windsurf/global_workflows/*.md` | `.windsurf/workflows/*.md`（當前工作區、子目錄或父目錄直到 git root） |
| **Antigravity** | `~/.gemini/config/global_workflows/*.md` | — |
| **OpenCode** | `~/.config/opencode/commands/*.md` | `.opencode/commands/*.md` |
| **Cursor** | `~/.cursor/commands/*.md` | — |
| **Claude Code** | 不使用 workflows，改用 `~/.claude/skills/`（見 [skills/README.md](../skills/README.md#安裝方式)） | — |

> **OpenCode 的單複數目錄**：官方文件只列複數 `commands/`，但 OpenCode（1.18.14 實測）掃描的 glob 是 `{command,commands}/**/*.md`，單數 `command/` 同樣有效。兩個目錄同時存在時內容會被載入兩次，請擇一使用。

> **Antigravity 的路徑遷移**：舊版路徑為 `~/.gemini/antigravity/global_workflows/`，自 `~/.gemini/config/.migrated`（2026-05-20）起改為 `~/.gemini/config/global_workflows/`，由 Antigravity、Antigravity IDE 與 Antigravity CLI（`agy`）三者共用。舊路徑仍可能被當作 fallback 讀取，更新後建議清空，避免載入到遷移前的舊版流程。

```bash
# Windsurf
cp dev-rules-kit/workflows/shared/*.md ~/.codeium/windsurf/global_workflows/

# Antigravity（含平台專屬工作流）
cp dev-rules-kit/workflows/shared/*.md ~/.gemini/config/global_workflows/
cp dev-rules-kit/workflows/antigravity/*.md ~/.gemini/config/global_workflows/

# OpenCode
cp dev-rules-kit/workflows/shared/*.md ~/.config/opencode/commands/

# Cursor
mkdir -p ~/.cursor/commands
cp dev-rules-kit/workflows/shared/*.md ~/.cursor/commands/
```

驗證：於 AI 對話框輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue` 等指令（Antigravity 另有 `fix-webview-conflict`）。

規則檔的安裝位置見 [rules/README.md](../rules/README.md#安裝方式)；外部工具（Serena / GitNexus / Superpowers）見 [docs/setup/tools.md](../docs/setup/tools.md)。

## 使用方式

根據您的 IDE 平台選擇對應的工作流程，或使用 shared/ 目錄中的共通工作流程。工作流程檔案在平台啟動時載入，新增或修改後需重新載入視窗才會生效。
