# Skills

此目錄包含各種開發技能（skills），用於標準化 AI Agent 的開發輔助功能。本 kit 的流程只以 skill 提供，各平台都從這裡安裝。

## 專案目錄結構

```
dev-rules-kit/
└── skills/              # 技能定義（五個平台共用）
    ├── code-simplify/
    ├── create-commit/
    ├── create-pr/
    ├── decompose/
    ├── dev-cycle/       # 追蹤與推進開發閉環的協調技能
    ├── execute-task/
    ├── git-squash/
    ├── new-issue/
    ├── project-worktrees/
    ├── review/
    └── writing-rules/
```

## 安裝方式

各平台的全域 skills 目錄如下，複製後每個技能會成為 `<平台 skills 目錄>/<name>/SKILL.md`：

| 平台 | skills 目錄 |
|------|------------|
| **Codex** | `~/.codex/skills/`（[OpenAI Docs](https://developers.openai.com/use-cases/reusable-codex-skills)） |
| **Claude Code** | `~/.claude/skills/` |
| **OpenCode** | `~/.config/opencode/skills/` |
| **Antigravity** | `~/.gemini/config/skills/` |
| **Cursor** | `~/.cursor/skills/` |

> **OpenCode 的單複數目錄**：OpenCode（1.18.14 實測）掃描的 glob 是 `{skill,skills}/**/SKILL.md`，單數 `skill/` 與複數 `skills/` 都會載入。兩個目錄同時存在時同名技能會被載入兩次，請擇一使用。

> **frontmatter 的 `name:` 為必填**：OpenCode 與 Antigravity 要求 `SKILL.md` 的 frontmatter 具備 `name:`，缺少時整份技能會**靜默不載入**——不報錯，也不出現在技能清單中。Claude Code 則可由資料夾名推導，有無皆可。本 kit 自 2.4.0 起所有技能一律附帶 `name:`，從舊版更新時請重新複製全部技能。

> **Antigravity 的路徑遷移**：舊版路徑為 `~/.gemini/antigravity/skills/`，現行路徑是 `~/.gemini/config/skills/`（2026-05-20 遷移，三個 Antigravity 產品共用）。裝在舊路徑的技能不保證會被載入。

> **從 2.x 升級**：3.0.0 起不再提供 workflows。`install.sh` 會把舊版留在 workflow／command 目錄中與本 kit 同名的檔案改名為 `.bak-<時間戳>`，使用者自己的其他檔案不動。手動安裝者請自行移除這些舊檔——OpenCode 的同名 command 優先於 skill，留著的話 `/<name>` 會一直執行舊版且不報錯。Windsurf 已停止支援，`~/.codeium/windsurf/` 內的本 kit 檔案不會再被更新或清理，請自行移除。

於 repo 根目錄執行安裝腳本即可，它會依上表複製到對應目錄：

```bash
# 自動偵測已安裝的平台
bash scripts/install.sh

# 只裝 Codex
bash scripts/install.sh codex

# 只裝 Claude Code
bash scripts/install.sh claude
```

腳本更新本 kit 技能資料夾內的同名檔案，保留其他檔案與個人技能；不會移除上游已刪除的舊檔。舊版安裝器若已產生 `<name>/<name>/SKILL.md`，更新後請檢查並手動移除確認無客製內容的巢狀副本。

`review` 內含 `scripts/verify-artifact.py`，安裝時整個技能目錄一起複製；只複製 SKILL.md 會缺少本機報告檢查器。

核心技能另需專案內的文件規範：於本 kit 根目錄執行 `python3 scripts/init-project.py /path/to/project`。更新使用 `--update`，既有 `docs/agents/project.md` 保留。技能宣告最低流程契約，與文件編輯版本分離。詳見 [專案初始化](../README.md#使用方式)。

驗證：Codex 在對話框輸入 `/skills` 或以 `$` 提及技能；其他平台輸入 `/`。應可找到 `decompose`、`create-commit`、`new-issue`、`dev-cycle` 等技能。

> **`dev-cycle` 使用方式**：這是一個 orchestration skill，除了 `/dev-cycle` 指令外，也可用自然語言觸發——直接說「issue 3396 到哪了」（查詢模式）或「繼續 3396」（推進模式），AI 會自動偵測 issue 目前所在階段並執行下一步。若未自動載入，可手動告知 AI 參考 `skills/dev-cycle/SKILL.md`。

規則檔的安裝位置見 [rules/README.md](../rules/README.md#安裝方式)；外部工具（Serena / GitNexus / Superpowers）見 [docs/setup/tools.md](../docs/setup/tools.md)。

## 使用方式

各技能以 `SKILL.md` 文件定義，包含：

- **描述**：技能用途與適用場景
- **輸入**：執行技能前需要讀取的文件或資訊
- **執行步驟**：具體的操作指引
- **輸出**：預期的輸出格式與內容

## 維護紀錄

| 日期 | 異動 | 說明 |
|------|------|------|
| 2026-09-24 | 新增 project-worktrees | 建立與移除開發、審查用 git worktree；專案位置與認證方式由 `docs/agents/project.md` 提供 |
| 2026-09-18 | 新增 Codex | 安裝器支援自動偵測 Codex，並安裝到 `~/.codex/skills/` |
| 2026-09-11 | 移除 workflows 與 Windsurf | 本 kit 只提供 skills，並停止支援 Windsurf；說明舊 workflow 副本的處理 |
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
**最後更新**: 2026-09-24
**文件版本**: 2.2
**適用範圍**: `skills/` 資料夾所有技能
