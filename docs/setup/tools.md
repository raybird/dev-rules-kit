# 外部工具設定指南

本文件說明如何在各平台配置搭配本 kit 使用的三個外部工具：**Serena**、**GitNexus**、**Superpowers**。

> **本 kit 自身的安裝方式不在這裡**，各資料夾的 README 已載明對應平台的複製路徑：
> [`rules/README.md`](../../rules/README.md#安裝方式) · [`workflows/README.md`](../../workflows/README.md#安裝方式) · [`skills/README.md`](../../skills/README.md#安裝方式)

## 前置需求

| 工具 | 需求 | 安裝 |
|------|------|------|
| Serena | uv / uvx（Python 工具執行器）；Python 3.13 由 `uvx -p 3.13` 自動下載 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| GitNexus | Node.js ≥ 18（建議用 [nvm](https://github.com/nvm-sh/nvm) 管理） | `npm install -g gitnexus` |
| Superpowers | 依平台而異，見下方對應章節 | — |

## MCP 設定檔位置

Serena 與 GitNexus 都以 MCP server 形式整合，各平台的設定檔與 JSON 結構如下：

| 平台 | 設定檔 | 頂層鍵 |
|------|--------|--------|
| Claude Code | 透過 `claude mcp add` 指令登錄 | — |
| OpenCode | `~/.config/opencode/config.json` | `mcp` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | `mcpServers` |
| Antigravity | `~/.gemini/antigravity/mcp_config.json` | `mcpServers` |
| Cursor | `~/.cursor/mcp.json` | `mcpServers` |

Windsurf / Antigravity / Cursor 三者的 JSON 格式完全相同，可直接互相沿用。

## 設定 Serena（MCP）

[Serena](https://github.com/oraios/serena) 是 LSP 層級的程式碼分析 MCP 伺服器，支援符號搜尋、重構、診斷。

> 首次啟動時 `uvx` 會下載並編譯 Serena 與相依套件，耗時數分鐘屬正常。

**Claude Code**（user scope，全部專案可用）：

```bash
claude mcp add serena -s user -- \
  uvx -p 3.13 --from git+https://github.com/oraios/serena \
  serena start-mcp-server --context ide --project-from-cwd
```

**OpenCode**（`config.json` 的 `mcp` 區塊）：

```json
{
  "mcp": {
    "serena": {
      "type": "local",
      "timeout": 60000,
      "command": [
        "uvx", "-p", "3.13",
        "--from", "git+https://github.com/oraios/serena",
        "serena", "start-mcp-server",
        "--context", "ide",
        "--project-from-cwd"
      ]
    }
  }
}
```

**Windsurf / Antigravity / Cursor**（`mcpServers` 區塊）：

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/oraios/serena",
        "serena", "start-mcp-server",
        "--context", "ide",
        "--open-web-dashboard", "False"
      ],
      "disabled": false
    }
  }
}
```

**使用注意事項**：

- 首次進入新專案時，Serena 規定要先呼叫 `initial_instructions` 工具讀取「Serena Instructions Manual」，再開始任何 coding 任務
- 進入大型專案後可執行 `onboarding` 建立索引，可大幅加速後續符號查詢
- 已索引的 memory 存放於專案內 `.serena/`，建議加入 `.gitignore`

## 設定 GitNexus（MCP + Hook）

[GitNexus](https://github.com/abhigyanpatwari/GitNexus) 是程式碼知識圖譜分析工具，支援影響分析、路由對應、API 形狀檢查。

**1. 安裝 CLI 並建立索引**

```bash
npm install -g gitnexus
gitnexus --version
gitnexus analyze .        # 於專案根目錄執行，產生 .gitnexus/（建議加入 .gitignore）
```

**2. 登錄 MCP server**

Claude Code：

```bash
claude mcp add gitnexus -s user -- gitnexus mcp
```

OpenCode（`config.json` 的 `mcp` 區塊）：

```json
{
  "mcp": {
    "gitnexus": {
      "type": "local",
      "command": ["gitnexus", "mcp"]
    }
  }
}
```

Windsurf / Antigravity / Cursor（`mcpServers` 區塊）：

```json
{
  "mcpServers": {
    "gitnexus": {
      "command": "gitnexus",
      "args": ["mcp"],
      "disabled": false
    }
  }
}
```

**3. 安裝 Hook（僅 Claude Code）**

GitNexus 的 hook 會在 `Grep` / `Glob` / `Bash` 之前自動把對應的圖譜上下文塞給 agent，並在 `Bash` 之後偵測索引是否過期。請將官方 hook 腳本（取自 [GitNexus 專案](https://github.com/abhigyanpatwari/GitNexus)）放到 `~/.claude/hooks/gitnexus/gitnexus-hook.cjs`，並在 `~/.claude/settings.json` 加上：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Grep|Glob|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$HOME/.claude/hooks/gitnexus/gitnexus-hook.cjs\"",
            "timeout": 10,
            "statusMessage": "Enriching with GitNexus graph context..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$HOME/.claude/hooks/gitnexus/gitnexus-hook.cjs\"",
            "timeout": 10,
            "statusMessage": "Checking GitNexus index freshness..."
          }
        ]
      }
    ]
  }
}
```

> ⚠️ **其他平台無 hook 等價機制**：OpenCode / Windsurf / Antigravity / Cursor 都沒有與 Claude Code `PreToolUse` / `PostToolUse` 對應的 hook 系統，因此「自動補圖譜上下文」僅在 Claude Code 中可用。其他平台需透過 `gitnexus-*` skills 主動呼叫。

**使用注意事項**：

- 配套 skills：安裝後可用 `gitnexus-exploring`、`gitnexus-debugging`、`gitnexus-impact-analysis`、`gitnexus-pr-review`、`gitnexus-refactoring`、`gitnexus-cli`、`gitnexus-guide`
- 索引重建：commit 大量檔案或重構後，Claude Code 的 hook 會自動提醒；其他平台需手動執行 `gitnexus analyze .`

## 設定 Superpowers

[Superpowers](https://github.com/obra/superpowers) 是強化 AI 開發流程的能力包，提供 brainstorming、TDD、debugging、subagent-driven development、verification 等流程型 skills。對本 kit 而言是**選用增強，不是必要依賴**——未安裝時各節點會執行內建的等價流程，詳見 [README 的 Superpowers 整合章節](../../README.md#superpowers-整合與安裝建議)。

**Claude Code**（官方 plugin marketplace）：

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install superpowers@claude-plugins-official
```

確認 `~/.claude/settings.json` 含：

```json
{
  "enabledPlugins": {
    "superpowers@claude-plugins-official": true
  }
}
```

安裝內容位於 `~/.claude/plugins/cache/claude-plugins-official/superpowers/<version>/`。

**OpenCode**（直接從 git URL 安裝，編輯 `~/.config/opencode/opencode.json`）：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "superpowers@git+https://github.com/obra/superpowers.git"
  ]
}
```

啟動 OpenCode 後會自動透過 bun / npm 安裝。

**Windsurf / Antigravity / Cursor**（無 plugin marketplace，需手動安裝）：

```bash
# 1. 取得 Superpowers 原始碼到任一位置
git clone https://github.com/obra/superpowers.git ~/Tools/superpowers

# 2. 將 skills 連結（或複製）到平台的 skills 目錄
ln -s ~/Tools/superpowers/skills/* ~/.codeium/windsurf/skills/     # Windsurf
ln -s ~/Tools/superpowers/skills/* ~/.gemini/antigravity/skills/   # Antigravity
ln -s ~/Tools/superpowers/skills/* ~/.cursor/skills/               # Cursor
```

建議使用 symlink，後續於 `~/Tools/superpowers/` 執行 `git pull` 即可更新。

**使用注意事項**：

- 核心原則：「若有 1% 機率某個 skill 適用，就必須先呼叫它」— 詳見 `using-superpowers`
- 多數 skills 為流程型（rigid），會強制依步驟執行，例如 TDD 必定先寫測試
- Skill 優先順序：先用 process skill（brainstorming、debugging），再用 implementation skill

## 完整設定檔範例

把 Serena 與 GitNexus 一起放進去的最小可運作設定。

**OpenCode** — `~/.config/opencode/config.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "serena": {
      "type": "local",
      "timeout": 60000,
      "command": [
        "uvx", "-p", "3.13",
        "--from", "git+https://github.com/oraios/serena",
        "serena", "start-mcp-server",
        "--context", "ide",
        "--project-from-cwd"
      ]
    },
    "gitnexus": {
      "type": "local",
      "command": ["gitnexus", "mcp"]
    }
  }
}
```

**Windsurf / Antigravity / Cursor** — `mcp_config.json` 或 `mcp.json`：

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/oraios/serena",
        "serena", "start-mcp-server",
        "--context", "ide",
        "--open-web-dashboard", "False"
      ],
      "disabled": false
    },
    "gitnexus": {
      "command": "gitnexus",
      "args": ["mcp"],
      "disabled": false
    }
  }
}
```

## 驗證

| 平台 | 驗證方式 |
|------|----------|
| Claude Code | `claude mcp list`，預期 `serena` 與 `gitnexus` 皆顯示 `✓ Connected`；輸入 `/` 應看到 `superpowers:*` 系列指令 |
| OpenCode | 輸入 `@` 應列出 MCP 工具；plugin 載入訊息會出現在啟動 log |
| Windsurf | 於 Cascade 視窗檢查 MCP server 狀態，應顯示 connected |
| Antigravity | 檢查 chat 面板下方的 MCP server 狀態列 |
| Cursor | **Settings → MCP** 應看到 `serena` 與 `gitnexus` 顯示為綠燈 |

## 常見問題

- **設定改了沒生效**：MCP 設定在啟動時載入。Windsurf / Antigravity 需執行 `Developer: Reload Window`；Cursor 可按 `Cmd/Ctrl + Shift + P` → `Cursor: Reload MCP Servers`
- **WebView 快取衝突（Antigravity 與 Windsurf 並用時）**：兩者底層皆為 VS Code 衍生，共用 Chromium WebView。執行本 kit 的 `/fix-webview-conflict` workflow 即可清除（同樣會清掉 Windsurf 快取）
- **`~/.cursor/` vs `~/.config/Cursor/`**：前者是 Cursor CLI agent 設定（含 MCP、commands、skills），後者是 VS Code 風格的 IDE 偏好設定（settings.json、keybindings.json）

## 移除

Claude Code：

```bash
claude mcp remove serena -s user
claude mcp remove gitnexus -s user
npm uninstall -g gitnexus
rm -rf ~/.claude/hooks/gitnexus/          # 並從 settings.json 移除 hook 區段
/plugin uninstall superpowers@claude-plugins-official
```

其他平台：從對應的 MCP 設定檔移除 `serena` / `gitnexus` 區塊，並刪除 Superpowers 的 symlink 與 clone 目錄。

## 參考連結

- [Serena GitHub](https://github.com/oraios/serena) · [uv 官方文件](https://docs.astral.sh/uv/)
- [GitNexus GitHub](https://github.com/abhigyanpatwari/GitNexus) · [Claude Code Hooks 文件](https://docs.claude.com/claude-code/hooks)
- [Superpowers GitHub](https://github.com/obra/superpowers) · [Claude Plugins marketplace](https://github.com/anthropics/claude-plugins-official)
- 平台官方文件：[Claude Code](https://claude.com/claude-code) · [OpenCode](https://github.com/sst/opencode) · [Windsurf](https://docs.windsurf.com) · [Antigravity](https://antigravity.google) · [Cursor](https://docs.cursor.com)
