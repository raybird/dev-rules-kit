# Windsurf 設定指南

[Windsurf](https://windsurf.com) 是 Codeium 推出的 AI 編輯器。本文件說明如何在 Windsurf 中安裝本 kit 的 rules、workflows 與 skills，並配置 Serena、GitNexus、Superpowers。

## 路徑速查

Windsurf 的全域設定預設位於 `~/.codeium/windsurf/`：

| 檔案 / 目錄 | 用途 |
|------------|------|
| `mcp_config.json` | MCP server 設定 |
| `global_workflows/*.md` | 全域 slash command（對應本 kit `workflows/shared/`） |
| `skills/<name>/SKILL.md` | 全域 skills |
| `memories/global_rules.md` | 全域規則（對應本 kit `rules/AGENTS.md`） |

專案層級可用 `.windsurf/workflows/*.md` 與 `.windsurfrules` 覆寫全域設定。

## 安裝 dev-rules-kit

```bash
# 1. 複製 shared workflows 到全域 workflows
cp dev-rules-kit/workflows/shared/*.md ~/.codeium/windsurf/global_workflows/

# 2. 複製 skills
mkdir -p ~/.codeium/windsurf/skills
cp -r dev-rules-kit/skills/* ~/.codeium/windsurf/skills/

# 3. 套用全域規則
cp dev-rules-kit/rules/AGENTS.zh-TW.md ~/.codeium/windsurf/memories/global_rules.md
```

驗證：於 Windsurf Cascade 內輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue` 等指令。

> **`dev-cycle` 使用方式**：`dev-cycle` 是 orchestration skill，**不會出現在 `/` 指令清單**（它沒有 workflow 對應檔）。使用方式：在對話中直接說「issue 3396 到哪了」（查詢）或「繼續 3396」（推進），Cascade AI 會讀取 `skills/dev-cycle/SKILL.md` 並執行對應行為。若未自動載入，可手動告知 AI 參考該檔案。

## 設定 Serena（MCP）

[Serena](https://github.com/oraios/serena) 是 LSP 層級的程式碼分析 MCP 伺服器。需先安裝 [uv](https://docs.astral.sh/uv/)；首次啟動 `uvx` 會下載 Python 與相依套件，耗時數分鐘屬正常。

編輯 `~/.codeium/windsurf/mcp_config.json`，在 `mcpServers` 區塊加入：

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

> ⚠️ **無 hook 等價機制**：Windsurf 沒有與 Claude Code `PreToolUse` / `PostToolUse` 對應的 hook 系統，GitNexus 的「自動補圖譜上下文」功能僅在 Claude 中可用。Windsurf 內需透過 `gitnexus-*` skills 主動呼叫。

## 設定 Superpowers（手動安裝）

Windsurf 沒有 plugin marketplace，需從 git 手動安裝 [Superpowers](https://github.com/obra/superpowers)。

```bash
# 1. 取得 Superpowers 原始碼
git clone https://github.com/obra/superpowers.git ~/.codeium/windsurf/superpowers

# 2. 將需要的 skills 連結（或複製）到 Windsurf 的 skills 目錄
ln -s ~/.codeium/windsurf/superpowers/skills/* ~/.codeium/windsurf/skills/
```

建議使用 symlink，後續於 `~/.codeium/windsurf/superpowers/` 執行 `git pull` 即可更新。

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
ls ~/.codeium/windsurf/global_workflows  # 應看到本 kit 的 *.md
ls ~/.codeium/windsurf/skills            # 應看到 dev-rules-kit + superpowers 的 skills
cat ~/.codeium/windsurf/memories/global_rules.md | head  # 確認規則套用
```

啟動 Windsurf 後於 Cascade 視窗中檢查 MCP server 狀態，`serena` 與 `gitnexus` 應顯示為 connected。

## 常見問題

- **WebView 快取衝突（與 Antigravity 並用時）**：兩者底層皆為 VS Code 衍生，共用 Chromium WebView。可參考本 kit `workflows/antigravity/fix-webview-conflict.md` 的清除步驟（同樣會清掉 Windsurf 快取）
- **設定改了沒生效**：MCP / workflows 在啟動時載入，修改後需 `Developer: Reload Window`
- **memories vs rules**：Windsurf 將「全域規則」存於 `memories/global_rules.md`；專案層的 `.windsurfrules` 會疊加而非覆寫

## 參考連結

- [Windsurf 官方文件](https://docs.windsurf.com)
- 各工具官方專案：[Serena](https://github.com/oraios/serena) · [GitNexus](https://github.com/abhigyanpatwari/GitNexus) · [Superpowers](https://github.com/obra/superpowers)
- 其他平台：[Claude Code](./claude.md) · [OpenCode](./opencode.md) · [Antigravity](./antigravity.md) · [Cursor](./cursor.md)
