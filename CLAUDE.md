# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Nature

本 repo 是 **純 Markdown 範本庫**，不是應用程式：沒有 build / test / lint，也沒有 package manager。所有「驗證」都是人工閱讀 Markdown，或在目標平台（Windsurf / OpenCode / Antigravity / Claude）中試跑 skill / workflow。

對使用者而言，這個 repo 的「產品」是 `rules/`、`workflows/`、`skills/` 三個目錄裡的 Markdown 檔，使用者會把它們複製到自己的開發環境設定目錄（見下方平台對應表）。

## High-Level Architecture

四個並列目錄，各自獨立，不互相 import：

| 目錄 | 內容 | 給誰用 |
|------|------|--------|
| `rules/` | 靜態行為規則（`AGENTS.md` 中／英版） | 寫進 `.windsurfrules` / `.cursorrules` 等規則檔 |
| `workflows/shared/` | 跨平台共通 slash command 流程 | Windsurf `.windsurf/workflows/`、OpenCode `commands/`、Antigravity `global_workflows/` |
| `workflows/<platform>/` | 平台特定 workaround（如 `antigravity/fix-webview-conflict.md`） | 對應平台專屬 |
| `skills/<name>/SKILL.md` | Claude 用的 skill 定義 | Claude Code skills |
| `docs/AGENTS.md` | issue 文件結構規範 | 套用此 kit 的下游專案的 `docs/` 目錄 |

### Skill ↔ Workflow 配對（最重要的維護規則）

`skills/<name>/SKILL.md` 與 `workflows/shared/<name>.md` 是**同一份內容的兩份拷貝**，分別給 Claude 和其他平台讀取。配對清單：

```
code-simplify   create-commit   create-pr   decompose
execute-task    new-issue       review
```

**修改任何一份時，必須同步更新另一份**。可用以下指令快速比對所有配對是否同步（`-w` 忽略空白差異，避免尾端換行造成誤報）：

```bash
for n in code-simplify create-commit create-pr decompose new-issue review execute-task; do
  diff -qw "skills/$n/SKILL.md" "workflows/shared/$n.md"
done
```

只有 frontmatter 與少數平台無關語意差異是允許的，其餘內容應一致。新增 skill 時，務必同時建立兩份。

### Frontmatter 格式

`SKILL.md` 與 `workflows/shared/*.md` 都用同一種 YAML frontmatter：

```markdown
---
description: 一句話描述用途
---
```

不要加 `name:` 欄位 — 名稱由檔名／資料夾名決定。

## 文件規範（套用此 kit 的下游專案）

`docs/AGENTS.md` 是給**下游專案的 `docs/` 目錄**用的規範（不是本 repo 自身），定義了：

- `docs/issues/issue-{ID}/` 結構：`README.md`、`requirement-analysis.md`、`technical-analysis.md`、`implementation-plan.md` 至少四件
- **Timeline 保留原則**：實作時如發現與舊文件描述不符，**不可直接覆寫**舊內容。應在 README 的 Timeline 加上日期、在原文件用 `> [!NOTE]` 標日期補充、並在各檔末尾的 `## 修訂紀錄 (Changelog)` 補記
- 日期一律使用**系統當下日期**的 `YYYY-MM-DD`，禁止手寫或統一日期

`new-issue` skill 與 workflow 會直接引用此規範產出文件，修改 `docs/AGENTS.md` 等同於改變這些 skill 的輸出格式。

## 撰寫規則時要遵守的核心原則

`rules/AGENTS.md` 是本 repo 自身也要遵守的：

- **Think before coding**：不確定就問，不要默默選擇
- **Surgical changes**：只動該動的，不要順手「改善」鄰近內容
- **Simplicity first**：能 50 行就不寫 200 行
- **Token economy**：對小任務不要產出長篇分析

新增規則或 workflow 時，先檢查能否擴充既有檔案；不要為單一場景再開一份近似檔。

## Conventions

- **語言**：所有 Markdown 內容使用**繁體中文（台灣）**，包含 commit message 與 PR description
- **日期**：文件內任何日期都使用系統當下日期，格式 `YYYY-MM-DD`
- **平台特定流程**：放在 `workflows/<platform>/`，不要混進 `workflows/shared/`
- **檔名與資料夾**：skill 用 kebab-case；skill 資料夾名、workflow 檔名、frontmatter 中 description 三者語意必須一致
