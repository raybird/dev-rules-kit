# dev-rules-kit

通用開發規則、工作流程與技能範本庫，適用於 **Windsurf**、**OpenCode**、**Antigravity** 等開發環境。

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
    ├── execute-task/
    ├── new-issue/
    ├── review/
    └── README.md
```

## 用途

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

## 使用方式

1. **複製整個範本庫**  
   ```bash
   git clone https://github.com/raybird/dev-rules-kit.git
   ```

2. **依環境選用內容**  
   - 若使用 **Windsurf**：將 `rules/` 中的內容合併至 `.windsurfrules`，將 `workflows/shared/` 中的流程複製至 `.windsurf/workflows/`
   - 若使用 **OpenCode**：將 `workflows/shared/` 中的流程匯入對應的 command 面板
   - 若使用 **Antigravity**：將 `workflows/shared/` 中的流程複製至 `global_workflows/`
   - 若使用 **Claude**：載入 `skills/` 中各子目錄的 `SKILL.md` 作為技能定義

3. **自訂與擴充**  
   根據個人或團隊需求修改／新增檔案，並定期同步回此倉庫作為中心範本。

## 推薦工具

以下為搭配本範本庫使用的推薦開發輔助工具：

| 工具 | 用途 | 推薦原因 |
|------|------|----------|
| **[Serena](https://github.com/oraios/serena)** | 程式碼分析與符號查詢 MCP 伺服器 | 支援 LSP 層級的符號搜尋、重構、診斷等功能，可深度理解程式碼結構 |
| **[GitNexus](https://github.com/abhigyanpatwari/GitNexus)** | 程式碼知識圖譜分析工具 | 建立程式碼知識圖譜，支援影響分析、路由對應、API 形狀檢查等進階查詢 |
| **[Superpowers](https://github.com/obra/superpowers)** | AI 開發能力提升框架 | 強化 AI Agent 的開發能力，提供更豐富的上下文理解與操作介面 |

## 貢獻

歡迎提出 issue 或 PR 來優化通用的規則、工作流程與技能，讓所有開發者受益。

## 授權

MIT © Raybird
