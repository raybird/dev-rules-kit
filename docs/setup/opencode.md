# OpenCode 設定指南

本文件說明如何在 [OpenCode](https://github.com/sst/opencode) 中安裝本 kit 提供的 workflows / skills，以及配置三個推薦工具（Serena、GitNexus、Superpowers）。

## 路徑速查

OpenCode 的全域設定預設位於 `~/.config/opencode/`：

| 檔案 / 目錄 | 用途 |
|------------|------|
| `config.json` | MCP server 設定 |
| `opencode.json` | plugin 宣告 |
| `commands/*.md` | slash command（對應本 kit `workflows/shared/`） |
| `skills/<name>/SKILL.md` | skills（對應本 kit `skills/`） |

專案層級可使用 `.opencode/` 或在專案根目錄放 `opencode.json` 覆寫全域設定。

## 安裝 dev-rules-kit

把本 repo 的 workflows 與 skills 複製到 OpenCode 對應目錄：

```bash
# 1. 複製 shared workflows 作為 slash commands
cp dev-rules-kit/workflows/shared/*.md ~/.config/opencode/commands/

# 2. 複製 skills 目錄
cp -r dev-rules-kit/skills/* ~/.config/opencode/skills/
```

驗證：於 OpenCode 內輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue` 等指令。

## 設定 Serena（MCP）

編輯 `~/.config/opencode/config.json`，在 `mcp` 區塊加入：

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
    }
  }
}
```

Serena 的前置需求與使用注意事項詳見 [Serena GitHub](https://github.com/oraios/serena)。需先安裝 [uv](https://docs.astral.sh/uv/)；首次啟動 `uvx` 會下載 Python 3.13 與 Serena 相依套件，耗時數分鐘屬正常。

## 設定 GitNexus（MCP）

先執行 `npm install -g gitnexus` 安裝 CLI，並於專案根目錄執行 `gitnexus analyze .` 建立索引（產生 `.gitnexus/`，建議加入 `.gitignore`）。接著在 `~/.config/opencode/config.json` 的 `mcp` 區塊加入：

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

> ⚠️ **無 hook 等價機制**：OpenCode 目前沒有與 Claude Code `PreToolUse` / `PostToolUse` 對應的 hook 系統，因此 GitNexus 的「自動補圖譜上下文」功能僅在 Claude 中可用。OpenCode 內需透過 `gitnexus-*` skills 主動呼叫。

## 設定 Superpowers（plugin）

OpenCode 不使用 Claude 的 plugin marketplace，但可直接從 git URL 安裝。編輯 `~/.config/opencode/opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "superpowers@git+https://github.com/obra/superpowers.git"
  ]
}
```

啟動 OpenCode 後會自動透過 bun / npm 安裝。詳細功能說明見 [Superpowers GitHub](https://github.com/obra/superpowers)。

## 完整 config.json 範例

把三個工具一起放進去的最小可運作設定：

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

搭配 `opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "superpowers@git+https://github.com/obra/superpowers.git"
  ]
}
```

## 驗證

```bash
opencode --version          # 確認 OpenCode 已安裝
ls ~/.config/opencode/commands  # 應看到本 kit 的 *.md
```

啟動 OpenCode，輸入 `/` 與 `@` 應分別列出 commands 與 MCP 工具；plugin 載入訊息會出現在啟動 log。

## 參考連結

- [OpenCode GitHub](https://github.com/sst/opencode)
- [OpenCode Config Schema](https://opencode.ai/config.json)
- 各工具官方專案：[Serena](https://github.com/oraios/serena) · [GitNexus](https://github.com/abhigyanpatwari/GitNexus) · [Superpowers](https://github.com/obra/superpowers)
- 其他平台：[Claude Code](./claude.md) · [Antigravity](./antigravity.md) · [Windsurf](./windsurf.md)
