# Antigravity 設定指南

[Antigravity](https://antigravity.google) 是 Google 推出的 AI 編輯器，沿用 Gemini 的目錄結構儲存設定。本文件說明如何在 Antigravity 中安裝本 kit 的 workflows 與 skills，並配置 Serena、GitNexus、Superpowers。

## 路徑速查

Antigravity 的全域設定預設位於 `~/.gemini/antigravity/`：

| 檔案 / 目錄 | 用途 |
|------------|------|
| `mcp_config.json` | MCP server 設定 |
| `global_workflows/*.md` | slash command（對應本 kit `workflows/shared/` + `workflows/antigravity/`） |
| `skills/<name>/SKILL.md` | skills |
| `~/.gemini/GEMINI.md` | 全域規則（對應本 kit `rules/AGENTS.md`） |
| `~/.config/Antigravity/User/settings.json` | 編輯器偏好設定（VS Code-style） |

## 安裝 dev-rules-kit

把本 repo 的 workflows 與 skills 複製到 Antigravity：

```bash
# 1. 複製 shared workflows 與 antigravity 平台專屬流程
cp dev-rules-kit/workflows/shared/*.md ~/.gemini/antigravity/global_workflows/
cp dev-rules-kit/workflows/antigravity/*.md ~/.gemini/antigravity/global_workflows/

# 2. 複製 skills
mkdir -p ~/.gemini/antigravity/skills
cp -r dev-rules-kit/skills/* ~/.gemini/antigravity/skills/

# 3. 套用全域規則
cp dev-rules-kit/rules/AGENTS.zh-TW.md ~/.gemini/GEMINI.md
```

驗證：於 Antigravity 內輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue`、`fix-webview-conflict` 等指令。

## 設定 Serena（MCP）

[Serena](https://github.com/oraios/serena) 是 LSP 層級的程式碼分析 MCP 伺服器。需先安裝 [uv](https://docs.astral.sh/uv/)；首次啟動 `uvx` 會下載 Python 與相依套件，耗時數分鐘屬正常。

編輯 `~/.gemini/antigravity/mcp_config.json`，在 `mcpServers` 區塊加入：

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

## 設定 GitNexus（MCP）

[GitNexus](https://github.com/abhigyanpatwari/GitNexus) 是程式碼知識圖譜分析工具。先執行 `npm install -g gitnexus`，並於專案根目錄執行 `gitnexus analyze .` 建立索引（產生 `.gitnexus/`，建議加入 `.gitignore`）。然後在 `mcp_config.json` 加入：

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

> ⚠️ **無 hook 等價機制**：Antigravity 沒有與 Claude Code `PreToolUse` / `PostToolUse` 對應的 hook 系統，GitNexus 的「自動補圖譜上下文」功能僅在 Claude 中可用。Antigravity 內需透過 `gitnexus-*` skills 主動呼叫。

## 設定 Superpowers（手動安裝）

Antigravity 沒有 plugin marketplace，需從 git 手動安裝 [Superpowers](https://github.com/obra/superpowers)。

```bash
# 1. 取得 Superpowers 原始碼到任一位置
git clone https://github.com/obra/superpowers.git ~/Tools/superpowers

# 2. 將需要的 skills 連結（或複製）到 Antigravity 的 skills 目錄
ln -s ~/Tools/superpowers/skills/* ~/.gemini/antigravity/skills/
```

建議使用 symlink，後續 `git pull` 即可更新。

## 完整 mcp_config.json 範例

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

```bash
ls ~/.gemini/antigravity/global_workflows  # 應看到本 kit 的 *.md
ls ~/.gemini/antigravity/skills            # 應看到 dev-rules-kit + superpowers 的 skills
```

啟動 Antigravity 後檢查 MCP server 狀態列（通常在 chat 面板下方），`serena` 與 `gitnexus` 應顯示為 connected。

## 常見問題

- **WebView 快取衝突（與 Windsurf 並用時）**：執行已安裝的 `/fix-webview-conflict` workflow 即可清除快取
- **設定改了沒生效**：Antigravity 載入 MCP / workflows 是在啟動時，修改後需 `Developer: Reload Window`

## 參考連結

- [Antigravity 官方](https://antigravity.google)
- 各工具官方專案：[Serena](https://github.com/oraios/serena) · [GitNexus](https://github.com/abhigyanpatwari/GitNexus) · [Superpowers](https://github.com/obra/superpowers)
- 其他平台：[Claude Code](./claude.md) · [OpenCode](./opencode.md) · [Windsurf](./windsurf.md) · [Cursor](./cursor.md)
