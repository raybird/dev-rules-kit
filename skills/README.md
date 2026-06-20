# Skills

此目錄包含各種開發技能（skills），用於標準化 AI Agent 的開發輔助功能。

## 整合說明與架構由來

Claude 已將原先 `commands/` 的功能整合為 `skills/` 的一部分。目前 `skills/` 與 `workflows/` 並存，根據不同平台需求選用。

### 為什麼區分 Skills 與 Workflows？

這兩者的並存源於 **CLI AI 助理** 與 **IDE 視覺化助理** 在運作機制上的本質不同：

1. **Skills (適用於 Claude Code 等 CLI 平台)**：
   Claude Code 本身是一個運行於終端機的自主 Agent，不具備 IDE 視覺化步驟的 UI 介面。它運作時，是透過讀取並內化 `SKILL.md` 中的步驟描述來擴充自身的行為規則，當對話遇到相關情境時，以「技能 (Skill)」的自主方式在對話中執行。因此需要以 `skills/<name>/SKILL.md` 的資料夾結構來存放。
2. **Workflows (適用於 Windsurf / OpenCode / Antigravity 等 IDE 平台)**：
   IDE 平台有與編輯器深度整合的 UI 介面。它們需要單一的 `.md` 檔案來解析成輸入框的 Slash Command，並在 IDE UI 畫面上呈現視覺化的互動步驟清單，引導使用者與 AI 協同確認。因此適合存放在 `workflows/` 中。

為了解決這個跨平台重用的格式限制，本專案設計了雙子星對照結構，並提供 `scripts/sync-skills.py` 腳本，讓我們能在一處（`skills/`）開發，並一鍵自動產生/同步至各平台所需的 `workflows/` 格式。


## 專案目錄結構

```
dev-rules-kit/
├── skills/              # 技能定義（Claude 主要使用）
│   ├── code-simplify/
│   ├── create-commit/
│   ├── create-pr/
│   ├── decompose/
│   ├── dev-cycle/       # 追蹤與推進開發閉環的協調技能
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
