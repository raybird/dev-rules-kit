# Cursor 設定指南

[Cursor](https://cursor.com) 是 Anysphere 推出的 AI 編輯器。本文件說明如何在 Cursor 中安裝本 kit 的 rules、commands、skills，並配置 Serena、GitNexus、Superpowers。

## 路徑速查

Cursor 的全域設定預設位於 `~/.cursor/`（IDE 偏好則在 `~/.config/Cursor/User/`）：

| 檔案 / 目錄 | 用途 |
|------------|------|
| `~/.cursor/mcp.json` | MCP server 設定 |
| `~/.cursor/commands/*.md` | 全域 slash command（對應本 kit `workflows/shared/`） |
| `~/.cursor/skills/<name>/SKILL.md` | 全域 skills |
| 專案 `.cursor/rules/*.mdc` | 專案層 Cursor Rules |
| 專案 `.cursor/mcp.json` | 專案層 MCP 設定 |
| Cursor IDE Settings → Rules → User Rules | 全域使用者規則（GUI 設定） |

## 安裝 dev-rules-kit

```bash
# 1. 複製 shared workflows 到 commands
mkdir -p ~/.cursor/commands
cp dev-rules-kit/workflows/shared/*.md ~/.cursor/commands/

# 2. 複製 skills
mkdir -p ~/.cursor/skills
cp -r dev-rules-kit/skills/* ~/.cursor/skills/
```

### 套用全域規則

Cursor 沒有檔案系統層級的全域 rules 檔，需透過 IDE GUI 設定：

1. 開啟 Cursor → `Cmd/Ctrl + ,` → Settings
2. 切換到 **Rules** 分頁 → **User Rules**
3. 把 `dev-rules-kit/rules/AGENTS.zh-TW.md` 的內容貼進去

> 若想用專案層規則：複製 `rules/AGENTS.zh-TW.md` 到專案內 `.cursor/rules/agents.mdc`（Cursor Rules 支援 `.mdc` 與 metadata frontmatter）。

驗證：於 Cursor Chat 內輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue` 等指令。

## 設定 Serena（MCP）

[Serena](https://github.com/oraios/serena) 是 LSP 層級的程式碼分析 MCP 伺服器。需先安裝 [uv](https://docs.astral.sh/uv/)；首次啟動 `uvx` 會下載 Python 與相依套件，耗時數分鐘屬正常。

編輯 `~/.cursor/mcp.json`，在 `mcpServers` 區塊加入：

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

[GitNexus](https://github.com/abhigyanpatwari/GitNexus) 是程式碼知識圖譜分析工具。先執行 `npm install -g gitnexus`，並於專案根目錄執行 `gitnexus analyze .` 建立索引（產生 `.gitnexus/`，建議加入 `.gitignore`）。然後在 `~/.cursor/mcp.json` 加入：

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

> ⚠️ **無 hook 等價機制**：Cursor 沒有與 Claude Code `PreToolUse` / `PostToolUse` 對應的 hook 系統，GitNexus 的「自動補圖譜上下文」功能僅在 Claude 中可用。Cursor 內需透過 `gitnexus-*` skills 主動呼叫。

## 設定 Superpowers（手動安裝）

Cursor 沒有 plugin marketplace，需從 git 手動安裝 [Superpowers](https://github.com/obra/superpowers)。

```bash
# 1. 取得 Superpowers 原始碼到任一位置
git clone https://github.com/obra/superpowers.git ~/Tools/superpowers

# 2. 將需要的 skills 連結（或複製）到 Cursor 的 skills 目錄
ln -s ~/Tools/superpowers/skills/* ~/.cursor/skills/
```

建議使用 symlink，後續於 superpowers 倉庫執行 `git pull` 即可更新。

## 完整 mcp.json 範例

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
ls ~/.cursor/commands  # 應看到本 kit 的 *.md
ls ~/.cursor/skills    # 應看到 dev-rules-kit + superpowers 的 skills
```

啟動 Cursor 後到 **Settings → MCP** 應看到 `serena` 與 `gitnexus` 顯示為綠燈。

## 常見問題

- **`.cursor/rules/` vs `.cursorrules`**：`.cursorrules` 為舊版單檔規則（仍可用），新版建議改用 `.cursor/rules/*.mdc`，可分主題、支援 metadata
- **`~/.cursor/` vs `~/.config/Cursor/`**：前者是 Cursor CLI agent 設定（含 MCP、commands、skills），後者是 VS Code 風格的 IDE 偏好設定（settings.json、keybindings.json）
- **設定改了沒生效**：修改 `mcp.json` 後可在 Cursor 內按 `Cmd/Ctrl + Shift + P` → `Cursor: Reload MCP Servers`

## 參考連結

- [Cursor 官方文件](https://docs.cursor.com)
- [Cursor MCP 文件](https://docs.cursor.com/context/mcp)
- 各工具官方專案：[Serena](https://github.com/oraios/serena) · [GitNexus](https://github.com/abhigyanpatwari/GitNexus) · [Superpowers](https://github.com/obra/superpowers)
- 其他平台：[Claude Code](./claude.md) · [OpenCode](./opencode.md) · [Antigravity](./antigravity.md) · [Windsurf](./windsurf.md)
