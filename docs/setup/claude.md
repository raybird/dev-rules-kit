# Claude Code 設定指南

本文件說明如何在 [Claude Code](https://claude.com/claude-code) 中安裝本 kit 提供的 skills，以及配置三個推薦工具：Serena、GitNexus、Superpowers。

## 路徑速查

| 檔案 / 目錄 | 用途 |
|------------|------|
| `~/.claude/settings.json` | 全域設定（含 hooks、enabledPlugins、statusLine） |
| `~/.claude/skills/<name>/SKILL.md` | 全域 skills |
| `~/.claude/hooks/` | hook 腳本 |
| `~/.claude/plugins/` | plugin 安裝目錄（由 marketplace 管理） |
| MCP 設定 | 透過 `claude mcp add` 指令登錄 |

## 安裝 dev-rules-kit

把本 repo 的 skills 複製到全域 skills 目錄：

```bash
cp -r dev-rules-kit/skills/* ~/.claude/skills/
```

驗證：於 Claude Code 內輸入 `/`，應出現 `decompose`、`create-commit`、`new-issue` 等指令。

## 設定 Serena（MCP）

[Serena](https://github.com/oraios/serena) 是 LSP 層級的程式碼分析 MCP 伺服器，支援符號搜尋、重構、診斷。

**前置需求**：

- **uv / uvx**：Python 工具執行器
- **Python 3.13**：由 `uvx -p 3.13` 自動下載

```bash
# 若尚未安裝 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**登錄 MCP server**（user scope，全部專案可用）：

```bash
claude mcp add serena -s user -- \
  uvx -p 3.13 --from git+https://github.com/oraios/serena \
  serena start-mcp-server --context ide --project-from-cwd
```

> 首次啟動時 `uvx` 會下載並編譯 Serena 與相依套件，耗時數分鐘屬正常。

**使用注意事項**：

- 首次進入新專案時，Serena 規定要先呼叫 `initial_instructions` 工具讀取「Serena Instructions Manual」，再開始任何 coding 任務
- 進入大型專案後可執行 `mcp__serena__onboarding` 建立索引，可大幅加速後續符號查詢
- 已索引的 memory 存放於專案內 `.serena/`，可加入 `.gitignore`

## 設定 GitNexus（MCP + Hook）

[GitNexus](https://github.com/abhigyanpatwari/GitNexus) 是程式碼知識圖譜分析工具，支援影響分析、路由對應、API 形狀檢查。Claude Code 中以 **MCP server + Hook + Skills** 三部分整合。

**前置需求**：Node.js ≥ 18（建議透過 [nvm](https://github.com/nvm-sh/nvm) 管理）。

**1. 安裝 CLI**

```bash
npm install -g gitnexus
gitnexus --version
```

**2. 登錄 MCP server**

```bash
claude mcp add gitnexus -s user -- gitnexus mcp
```

**3. 安裝 Hook**（自動補上圖譜上下文）

GitNexus 的 hook 會在 `Grep` / `Glob` / `Bash` 之前自動把對應的圖譜上下文塞給 agent，並在 `Bash` 之後偵測索引是否過期。請將官方 hook 腳本（取自 [GitNexus 專案](https://github.com/abhigyanpatwari/GitNexus)）放到：

```
~/.claude/hooks/gitnexus/gitnexus-hook.cjs
```

並在 `~/.claude/settings.json` 加上：

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

**4. 為專案建立索引**

```bash
gitnexus analyze .
```

完成後產生 `.gitnexus/`，建議加入 `.gitignore`。

**使用注意事項**：

- 配套 skills：安裝後可用 `gitnexus-exploring`、`gitnexus-debugging`、`gitnexus-impact-analysis`、`gitnexus-pr-review`、`gitnexus-refactoring`、`gitnexus-cli`、`gitnexus-guide`
- 索引重建：commit 大量檔案或重構後，hook 會自動提醒；也可手動執行 `gitnexus analyze .`

## 設定 Superpowers（Plugin）

[Superpowers](https://github.com/obra/superpowers) 是強化 Claude Code 工作流程的能力包，提供 brainstorming、TDD、debugging、subagent-driven development、verification 等高品質 skills。透過 Claude 官方 plugin marketplace 安裝。

**加入 marketplace**：

```
/plugin marketplace add anthropics/claude-plugins-official
```

**安裝 plugin**：

```
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

**使用注意事項**：

- 核心原則：「若有 1% 機率某個 skill 適用，就必須先呼叫它」— 詳見 `superpowers:using-superpowers`
- 多數 skills 為流程型（rigid），會強制依步驟執行，例如 TDD 必定先寫測試
- Skill 優先順序：先用 process skill（brainstorming、debugging），再用 implementation skill
- 安裝內容位於 `~/.claude/plugins/cache/claude-plugins-official/superpowers/<version>/`

## 驗證全部設定

```bash
claude mcp list
```

預期輸出：

```
serena: uvx -p 3.13 ... - ✓ Connected
gitnexus: .../gitnexus mcp - ✓ Connected
```

於 Claude Code 內輸入 `/` 應看到本 kit 的 skills 與 `superpowers:*` 系列指令。

## 移除

```bash
# Serena
claude mcp remove serena -s user

# GitNexus
claude mcp remove gitnexus -s user
npm uninstall -g gitnexus
rm -rf ~/.claude/hooks/gitnexus/
# 並從 settings.json 移除 hook 區段

# Superpowers
/plugin uninstall superpowers@claude-plugins-official
```

## 參考連結

- [Serena GitHub](https://github.com/oraios/serena) · [uv 官方文件](https://docs.astral.sh/uv/)
- [GitNexus GitHub](https://github.com/abhigyanpatwari/GitNexus) · [Claude Code Hooks 文件](https://docs.claude.com/claude-code/hooks)
- [Superpowers GitHub](https://github.com/obra/superpowers) · [Claude Plugins marketplace](https://github.com/anthropics/claude-plugins-official)
- 其他平台：[OpenCode](./opencode.md) · [Antigravity](./antigravity.md) · [Windsurf](./windsurf.md) · [Cursor](./cursor.md)
