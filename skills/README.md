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

## 安裝方式

各平台的全域 skills 目錄如下，複製後每個技能會成為 `<平台 skills 目錄>/<name>/SKILL.md`：

| 平台 | skills 目錄 | 備註 |
|------|------------|------|
| **Claude Code** | `~/.claude/skills/` | 主要使用 skills，不需另外安裝 workflows |
| **OpenCode** | `~/.config/opencode/skills/` | 另需複製 `workflows/shared/` 到 `commands/` |
| **Windsurf** | `~/.codeium/windsurf/skills/` | 另需複製 `workflows/shared/` 到 `global_workflows/` |
| **Antigravity** | `~/.gemini/config/skills/` | 另需複製 `workflows/` 到 `global_workflows/` |
| **Cursor** | `~/.cursor/skills/` | 另需複製 `workflows/shared/` 到 `commands/` |

> **OpenCode 的單複數目錄**：OpenCode（1.18.14 實測）掃描的 glob 是 `{skill,skills}/**/SKILL.md`，單數 `skill/` 與複數 `skills/` 都會載入。兩個目錄同時存在時同名技能會被載入兩次，請擇一使用。

> **Antigravity 的路徑遷移**：舊版路徑為 `~/.gemini/antigravity/skills/`，現行路徑是 `~/.gemini/config/skills/`（2026-05-20 遷移，三個 Antigravity 產品共用）。裝在舊路徑的技能不保證會被載入。

> **OpenCode 是否需要兩邊都裝**：`skills/` 與 `workflows/shared/` 的內容逐位元組相同，OpenCode 會同時載入兩者，等於同一份內容有 skill 與 slash command 兩個入口，而 skill 的 `description` 常駐 context。若已安裝 `commands/`，一般不需再複製全部技能；例外是 `dev-cycle`，它的價值在自然語言觸發，可單獨安裝。

```bash
# Claude Code
cp -r dev-rules-kit/skills/* ~/.claude/skills/

# 其他平台（以 Windsurf 為例，替換路徑即可）
mkdir -p ~/.codeium/windsurf/skills
cp -r dev-rules-kit/skills/* ~/.codeium/windsurf/skills/
```

驗證：於 AI 對話框輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue`、`dev-cycle` 等指令。

> **`dev-cycle` 使用方式**：這是一個 orchestration skill，除了 `/dev-cycle` 指令外，也可用自然語言觸發——直接說「issue 3396 到哪了」（查詢模式）或「繼續 3396」（推進模式），AI 會自動偵測 issue 目前所在階段並執行下一步。若未自動載入，可手動告知 AI 參考 `skills/dev-cycle/SKILL.md`。

workflows 的安裝路徑見 [workflows/README.md](../workflows/README.md#安裝方式)；規則檔見 [rules/README.md](../rules/README.md#安裝方式)；外部工具（Serena / GitNexus / Superpowers）見 [docs/setup/tools.md](../docs/setup/tools.md)。

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
| 2026-08-07 | 修正 Antigravity 路徑 | 改為遷移後的 `~/.gemini/config/skills/`，舊路徑不保證載入 |
| 2026-08-07 | 補 OpenCode 安裝細節 | 註明 `{skill,skills}` glob 單複數皆生效，以及與 `commands/` 重複安裝的取捨 |
| 2026-08-04 | 收攏安裝路徑 | 新增「安裝方式」章節，取代原 `docs/setup/<platform>.md` 的「安裝 dev-rules-kit」段落 |
| 2026-07-21 | 分級分流與 description 規範 | 依 issue 分級決定是否需要 `decompose`；`description` 補齊觸發時機與適用範圍 |
| 2026-06-02 | 新增 git-squash | 新增 git-squash 技能，對應新增的 git-squash 工作流程 |
| 2026-05-28 | 新增 dev-cycle | 新增 dev-cycle 協調技能，以 issue 為中心追蹤並推進開發閉環 |
| 2026-05-08 | 文件建立 | 建立 `skills/README.md`，說明 skills 與 workflows 的關係 |
| 2026-05-08 | 整合說明 | Claude 內部將 commands 功能整合至 skills 架構使用 |

---

**建立日期**: 2026-05-08  
**最後更新**: 2026-08-07  
**文件版本**: 1.4  
**適用範圍**: `skills/` 資料夾所有技能
