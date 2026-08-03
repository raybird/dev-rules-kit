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

### Skill ↔ Workflow 同步機制（最重要的維護規則）

`skills/<name>/SKILL.md` 與 `workflows/shared/<name>.md` 是對應的技能與工作流程。

**請勿手動進行兩邊的檔案複製**。當你修改或新增 `skills/` 底下的技能時，請一律在根目錄執行同步腳本來自動更新工作流程：

```bash
python3 scripts/sync-skills.py
```

在 PR 合併前，執行檢查模式驗證所有配對是否同步（會自動掃描全部配對，不需維護名單；CI 也會跑同一支檢查）：

```bash
python3 scripts/sync-skills.py --check
```

同步腳本為逐位元組複製，兩邊內容應完全一致。不要手動修改 `workflows/shared/` 端的配對檔案——任何差異都會在下次同步時被覆蓋。


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

- `docs/issues/issue-{ID}/` 依規模分級：Small 僅 `README.md`，Medium 加 `implementation-plan.md`，Large 才使用 `README.md`、`requirement-analysis.md`、`technical-analysis.md`、`implementation-plan.md` 四件套
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

## BDD + TDD 與 Superpowers 映射

核心開發閉環採 BDD 外迴圈與 TDD 內迴圈。Superpowers 是選用增強，不是執行期必要依賴；已安裝時優先調用，未安裝時由本地 skill 執行等價流程。維護相關 skill 時，必須保留下列映射與本地 gate：

| 節點 | 可用時優先調用的 Superpowers skill | 不可跳過的本地證據 |
|---|---|---|
| `new-issue` | `brainstorming` | 一次一題的需求澄清、使用者核准、依規模決定形式且依風險決定強度的驗收標準 |
| `decompose` | `writing-plans` | 每個 Scenario 的 BDD 外迴圈與 TDD 內迴圈映射 |
| `execute-task` | `test-driven-development` | 外迴圈紅燈、單元測試紅燈、最小實作後全綠、重構後全綠（不改變可觀察行為者改用等價證據） |
| `review` | `requesting-code-review` | 獨立 reviewer、架構符合度、至少 3 個破壞性邊界案例與流程判定 |
| `create-pr` | `verification-before-completion` | 可追溯至驗收標準原文與實際成功命令的 Proof of Test |

PRD 或文件若使用 `implementation-plan`、`critic`、`architectural-compliance`、`pull-request-spec` 等非現有 Superpowers skill 名稱，不得直接寫成不可執行依賴：語意分別映射至上表的 `writing-plans`、`requesting-code-review` 加架構 gate，以及 `create-pr` 內建規格加 `verification-before-completion`。未安裝 Superpowers 時執行各節點已明訂的本地等價流程。

`docs/AGENTS.md` 是驗收標準形式與強度、分批核准、Scenario ID、紅綠燈與等價證據格式、review artifact 存放位置、`## 待確認事項` 及 `## Gate 豁免紀錄` 的單一真相來源。修改任一節點時，同時檢查 `dev-cycle` 是否仍能阻止跨階段繞過；不得只加提示文字而沒有完成 gate。

**gate 的對象是 agent，不是使用者。** 所有 gate 都必須同時滿足兩件事：agent 不得自行降低標準；使用者明確要求豁免時必須照做並留下 `## Gate 豁免紀錄`。新增 gate 時一併確認它有豁免路徑，且豁免後 `dev-cycle` 能據紀錄放行。唯一不可豁免的是誠實回報——不得把未執行的驗證寫成已通過。

## Conventions

- **語言**：所有 Markdown 內容使用**繁體中文（台灣）**，包含 commit message 與 PR description
- **雙語規則檔**：修改 `rules/` 時，`AGENTS.md`（英）與 `AGENTS.zh-TW.md`（中）**必須同步修改**，章節結構（`## ` 數量與順序）保持一一對應；`sync-skills.py --check` 會驗證章節數是否一致
- **Commit 訊息**：Commit 絕對不添加相關 `Co-Authored-By: Claude` 在 message 內
- **日期**：文件內任何日期都使用系統當下日期，格式 `YYYY-MM-DD`
- **平台特定流程**：放在 `workflows/<platform>/`，不要混進 `workflows/shared/`
- **檔名與資料夾**：skill 用 kebab-case；skill 資料夾名、workflow 檔名、frontmatter 中 description 三者語意必須一致
- **description 撰寫**：`description` 是唯一常駐於 agent context 的內容，也是 agent 判斷「是否載入整份 skill」的依據，應同時寫出**做什麼**與**何時使用／適用範圍**（例如 `decompose` 標明僅適用 Large）
- **workflows/README.md 清單**：該檔不在同步腳本的複製範圍內，其 Shared Workflows 清單中每條描述必須等於對應 `SKILL.md` `description` 的**第一句**；改動 description 時要一併更新，`sync-skills.py --check` 會驗證
