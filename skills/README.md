# Skills

此目錄包含各種開發技能（skills），用於標準化 AI Agent 的開發輔助功能。

## 整合說明

Claude 已將 `commands/` 的功能整合為 `skills/` 的一部分。目前 `skills/` 與 `workflows/` 並存，根據不同平台需求選用。

## 專案目錄結構

```
dev-rules-kit/
├── skills/              # 技能定義（Claude 主要使用）
│   ├── code-simplify/
│   ├── create-commit/
│   ├── create-pr/
│   ├── decompose/
│   ├── dev-cycle/       # orchestration skill（無 workflow 對應檔）
│   ├── execute-task/
│   ├── git-squash/
│   ├── new-issue/
│   └── review/
└── workflows/           # 工作流程（Windsurf、OpenCode 使用）
    ├── shared/
    ├── antigravity/
    └── README.md
```

## 各平台使用方式

| 平台 | 使用目錄 | 說明 |
|------|----------|------|
| **Windsurf** | `workflows/` | 使用 `.windsurf/workflows/` 路徑 |
| **OpenCode** | `workflows/` | 原 `commands/` 功能已整合至 `workflows/shared/` |
| **Antigravity** | `workflows/` 或 `skills/` | 視功能需求選用 |
| **Claude** | `skills/` | 主要使用 skills 目錄結構 |

> **Orchestration skill 注意事項**：`dev-cycle` 等 orchestration skill 只有 `SKILL.md`，沒有 `workflows/shared/` 對應檔，因此**不會出現在 `/` 指令清單**。非 Claude 平台需手動將 SKILL.md 加入 AI context，再以自然語言觸發（如「issue 3396 到哪了」）。

## 使用方式

各技能以 `SKILL.md` 文件定義，包含：

- **描述**：技能用途與適用場景
- **輸入**：執行技能前需要讀取的文件或資訊
- **執行步驟**：具體的操作指引
- **輸出**：預期的輸出格式與內容

### 調用方式

根據各 IDE 平台的 slash command 機制：

- **Windsurf**: 使用 `/{workflow-name}` 調用工作流程（如 `/decompose`）
- **OpenCode**: 使用 `/{workflow-name}` 調用工作流程（如 `/code-simplify`）
- **Antigravity**: 使用 `/{workflow-name}` 調用工作流程，或使用 skill 調用技能
- **Claude**: 透過 system prompt 載入 `SKILL.md` 定義的技能行為

## 維護紀錄

| 日期 | 異動 | 說明 |
|------|------|------|
| 2026-06-02 | 新增 git-squash | 新增 git-squash 技能，對應新增的 git-squash 工作流程 |
| 2026-05-08 | 文件建立 | 建立 `skills/README.md`，說明 skills 與 workflows 的關係 |
| 2026-05-08 | 整合說明 | Claude 內部將 commands 功能整合至 skills架構使用 |

---

**建立日期**: 2026-05-08  
**最後更新**: 2026-06-02  
**文件版本**: 1.1  
**適用範圍**: `skills/` 資料夾所有技能
