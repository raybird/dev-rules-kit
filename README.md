# dev-rules-kit

一套給 AI 開發環境使用的規則、工作流程與技能範本庫，集中整理 `rules`、`workflows`、`skills` 三類 Markdown 資產，方便在 **Windsurf**、**OpenCode**、**Claude Code**、**Antigravity** 等工具中重複使用與維護。

這個 repo 的重點不是執行程式，而是提供可直接複製、調整、同步的開發規範與操作流程，讓個人或團隊能用一致方式管理 AI agent 的行為、工作流程與文件產出。

## 目錄結構

```
dev-rules-kit/
├── README.md              # 本說明文件
├── docs/                  # 技術文件與規範說明
│   └── AGENTS.md          # 文件資料夾說明（AGENTS）
├── rules/                 # 靜態規則檔（agents、coding style、linting 等）
│   ├── AGENTS.md
│   ├── AGENTS.zh-TW.md
│   └── README.md
├── workflows/             # 可執行的命令或工作流程（command/workflow）
│   ├── shared/            # 共通工作流程
│   ├── antigravity/       # Antigravity 平台特定工作流程
│   └── README.md
└── skills/                # 可重複使用的技能定義（skill）
    ├── code-simplify/
    ├── create-commit/
    ├── create-pr/
    ├── decompose/
    ├── dev-cycle/
    ├── execute-task/
    ├── new-issue/
    ├── review/
    └── README.md
```

## 用途

此 repo 主要提供可跨平台重用的 Markdown 範本，依用途拆分為以下幾類：

- **`docs/`**  
  技術文件與規範說明，包含文件資料夾結構規範（AGENTS.md）與 issue 文件模板。  

- **`rules/`**  
  存放各種靜態規則，例如 AI agent 的行為規範、程式碼風格約定、專案架構準則等。  
  適合直接複製到專案的 `.windsurfrules`、`.cursorrules` 或對應的設定檔中。

- **`workflows/`**  
  定義常用的命令或自動化流程，包含 `shared/`（共通工作流程）與平台特定子目錄。  
  每個檔案應包含明確的觸發條件與執行步驟，方便在不同編輯器或 CLI 中重現。

- **`skills/`**  
  儲存可被 AI 或工具呼叫的「技能」，以子目錄形式組織，每個子目錄包含 `SKILL.md` 定義。  
  每個 skill 檔案應包含清晰的輸入、輸出與使用範例。

## 開發閉環

`workflows/shared/` 與 `skills/` 內的七個工作流剛好構成一個完整的日常開發循環：

```
new-issue        ← 分析需求、建立 issue 文件
    ↓
decompose        ← 將 implementation plan 拆解為 Phase / Task
    ↓
execute-task  ←──────────────────────────────┐
    ↓                                        │
code-simplify    ← 精煉程式碼，提升可讀性        │
    ↓                                        │
create-commit    ← 生成 commit 訊息            │
    ↓                                        │
create-pr        ← 生成 PR 說明內容            │
    ↓                                        │
review           ← 審查變更，發現問題回頭修正 ───┘
    ↓
  通過合併
```

review 發現需要修正時，回到 execute-task 修正後再走一次 commit → PR → review，循環直到通過。

若想以 issue 為中心自動推進整個閉環，可使用 `dev-cycle` skill：輸入 issue ID，AI 自動偵測目前所在階段並執行下一步，循環直到 PR merged。也支援查詢模式（如「issue 3396 到哪了」），只回報進度不推進。

## 使用方式

1. **複製整個範本庫**  
   ```bash
   git clone https://github.com/raybird/dev-rules-kit.git
   ```

2. **依平台選用內容**  
   - 若使用 **Claude Code**：參考 [docs/setup/claude.md](./docs/setup/claude.md)
   - 若使用 **OpenCode**：參考 [docs/setup/opencode.md](./docs/setup/opencode.md)
   - 若使用 **Antigravity**：參考 [docs/setup/antigravity.md](./docs/setup/antigravity.md)
   - 若使用 **Windsurf**：參考 [docs/setup/windsurf.md](./docs/setup/windsurf.md)
   - 若使用 **Cursor**：參考 [docs/setup/cursor.md](./docs/setup/cursor.md)

3. **了解日常使用方式**  
   參考 [docs/usage.md](./docs/usage.md) 查看完整閉環示範與各 skill 快速參考。

4. **自訂與擴充**  
   根據個人或團隊需求修改／新增檔案，並把這個 repo 當作集中維護規則、流程與技能範本的來源。

## 推薦工具

以下為搭配本範本庫使用的推薦開發輔助工具：

| 工具 | 用途 | 推薦原因 |
|------|------|----------|
| **[Serena](https://github.com/oraios/serena)** | 程式碼分析與符號查詢 MCP 伺服器 | 支援 LSP 層級的符號搜尋、重構、診斷等功能，可深度理解程式碼結構 |
| **[GitNexus](https://github.com/abhigyanpatwari/GitNexus)** | 程式碼知識圖譜分析工具 | 建立程式碼知識圖譜，支援影響分析、路由對應、API 形狀檢查等進階查詢 |
| **[Superpowers](https://github.com/obra/superpowers)** | AI 開發能力提升框架 | 強化 AI Agent 的開發能力，提供更豐富的上下文理解與操作介面 |
| **[Wave Terminal](https://github.com/wavetermdev/waveterm)** | AI 整合跨平台終端機 | 開源且內建 AI 助手，支援多種模型（OpenAI、Claude、Ollama 等），提供持久 SSH 連線、區塊化工作區與遠端檔案編輯 |

各平台完整安裝步驟：

- **Claude Code**：[docs/setup/claude.md](./docs/setup/claude.md)
- **OpenCode**：[docs/setup/opencode.md](./docs/setup/opencode.md)
- **Antigravity**：[docs/setup/antigravity.md](./docs/setup/antigravity.md)
- **Windsurf**：[docs/setup/windsurf.md](./docs/setup/windsurf.md)
- **Cursor**：[docs/setup/cursor.md](./docs/setup/cursor.md)

## 貢獻

歡迎提出 issue 或 PR 來優化通用的規則、工作流程與技能，讓所有開發者受益。

## 授權

MIT © Raybird
