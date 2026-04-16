# dev-rules-kit

通用開發規則、工作流程與技能範本庫，適用於 **Windsurf**、**OpenCode**、**Antigravity** 等開發環境。

## 目錄結構

```
dev-rules-kit/
├── README.md              # 本說明文件
├── rules/                 # 靜態規則檔（agents、coding style、linting 等）
│   ├── agents.md
│   ├── coding-style.md
│   └── ...
├── workflows/             # 可執行的命令或工作流程（command/workflow）
│   ├── debug-flow.md
│   ├── deploy.md
│   └── ...
└── skills/                # 可重複使用的技能定義（skill）
    ├── git-commit.md
    ├── pr-review.md
    └── ...
```

## 用途

- **`rules/`**  
  存放各種靜態規則，例如 AI agent 的行為規範、程式碼風格約定、專案架構準則等。  
  適合直接複製到專案的 `.windsurfrules`、`.cursorrules` 或對應的設定檔中。

- **`workflows/`**  
  定義常用的命令或自動化流程，例如測試、建置、部署、偵錯步驟。  
  每個檔案應包含明確的觸發條件與執行步驟，方便在不同編輯器或 CLI 中重現。

- **`skills/`**  
  儲存可被 AI 或工具呼叫的「技能」，例如 `git commit 訊息生成`、`PR 審查輔助`、`重構建議` 等。  
  每個 skill 檔案應包含清晰的輸入、輸出與使用範例。

## 使用方式

1. **複製整個範本庫**  
   ```bash
   git clone https://github.com/raybird/dev-rules-kit.git
   ```

2. **依環境選用內容**  
   - 若使用 **Windsurf**：將 `rules/` 中的內容合併至 `.windsurfrules`
   - 若使用 **OpenCode**：將 `workflows/` 中的流程匯入對應的 command 面板
   - 若使用 **Antigravity**：將 `skills/` 註冊為可用的 skill

3. **自訂與擴充**  
   根據個人或團隊需求修改／新增檔案，並定期同步回此倉庫作為中心範本。

## 貢獻

歡迎提出 issue 或 PR 來優化通用的規則、工作流程與技能，讓所有開發者受益。

## 授權

MIT © Raybird
