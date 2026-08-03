# dev-rules-kit

一套給 AI 開發環境使用的規則、工作流程與技能範本庫，集中整理 `rules`、`workflows`、`skills` 三類 Markdown 資產，方便在 **Windsurf**、**OpenCode**、**Claude Code**、**Antigravity** 等工具中重複使用與維護。

這個 repo 的重點不是執行程式，而是提供可直接複製、調整、同步的開發規範與操作流程，讓個人或團隊能用一致方式管理 AI agent 的行為、工作流程與文件產出。

## 目錄結構

```
dev-rules-kit/
├── README.md              # 本說明文件
├── CHANGELOG.md           # 變更紀錄（下游更新參考）
├── CLAUDE.md              # AI 維護指引
├── scripts/               # 自動化工具
│   ├── sync-skills.py     # 雙子星自動同步腳本（--check 可驗證同步狀態）
│   └── check-links.py     # Markdown 相對連結檢查
├── docs/                  # 技術文件與規範說明
│   ├── AGENTS.md          # 文件資料夾說明（AGENTS）
│   ├── usage.md           # 使用指南（含開發閉環步驟）
│   └── _templates/        # 實體文件模板（架構、領域、Changelog）
├── rules/                 # 靜態規則檔（agents、coding style、linting 等）
│   ├── AGENTS.md
│   ├── AGENTS.zh-TW.md
│   └── README.md
├── workflows/             # 可執行的命令或工作流程（command/workflow）
│   ├── shared/            # 共通工作流程（含 dev-cycle.md 等 9 個工作流）
│   ├── antigravity/       # Antigravity 特定工作流程
│   └── README.md
└── skills/                # 可重複使用的技能定義（skill，共 9 個技能）
    ├── code-simplify/
    ├── create-commit/
    ├── create-pr/
    ├── decompose/
    ├── dev-cycle/
    ├── execute-task/
    ├── git-squash/
    ├── new-issue/
    └── review/
```

## 用途

此 repo 主要提供可跨平台重用的 Markdown 範本，依用途拆分為以下幾類：

- **`docs/`**  
  技術文件與規範說明，包含文件資料夾結構規範（AGENTS.md）與 issue 文件模板。  

- **`rules/`**  
  存放各種靜態規則，例如 AI agent 的行為規範、程式碼風格約定、專案架構準則等。  
  適合直接複製到專案的 `.windsurfrules`、`.cursorrules` 或對應的設定檔中。

- **`workflows/`**  
  定義常用的命令或自動化流程，包含 `shared/`（共通工作流程）與平台特定子目錄。  
  每個檔案應包含明確的觸發條件與執行步驟，方便在不同編輯器或 CLI 中重現。

- **`skills/`**  
  儲存可被 AI 或工具呼叫的「技能」，以子目錄形式組織，每個子目錄包含 `SKILL.md` 定義。  
  重量級 skill（如 `review`、`decompose`）包含完整的輸入、輸出規範與使用範例；輕量 skill（如 `create-commit`）僅列執行步驟，維持簡潔。

## 開發閉環

`workflows/shared/` 與 `skills/` 內的開發工具（包含 9 個雙子星對照技能/工作流）構成了一個開發閉環。其中核心的七個工作流構成日常開發循環：

```
new-issue        ← 分析需求、建立 issue 文件
    ↓
decompose        ← 將 implementation plan 拆解為 Phase / Task（僅 Large）
    ↓
execute-task  ←──────────────────────────────┐
    ↓                                        │
code-simplify    ← 精煉程式碼，提升可讀性        │
    ↓                                        │
create-commit    ← 生成 commit 訊息            │
    ↓                                        │
create-pr        ← 生成 PR 說明內容            │
    ↓                                        │
review           ← 審查變更，發現問題回頭修正 ───┘
    ↓
  通過合併
```

`decompose` 只在 issue 被評估為 **Large** 時執行；Small 與 Medium 的實作步驟本身即為可執行的任務清單，會由 `new-issue` 直接接到 `execute-task`。

review 發現需要修正時，回到 execute-task 修正後再走一次 commit → PR → review，循環直到通過。

若想以 issue 為中心自動推進整個閉環，可使用 `dev-cycle` 工作流或技能：輸入 issue ID，AI 自動偵測目前所在階段並執行下一步，循環直到 PR merged。也支援查詢模式（如「issue 3396 到哪了」），只回報進度不推進。

`git-squash` 是**閉環之外的獨立輔助工具**：需要整理分支 commit（如 merge 前壓縮瑣碎提交）時單獨呼叫，不屬於閉環的固定步驟。

## Superpowers 整合與安裝建議

Superpowers 是本 kit 的**選用流程增強套件，不是必要依賴**。未安裝時，`new-issue`、`decompose`、`execute-task`、`review`、`create-pr` 仍會執行各自內建的等價流程，驗收標準核准、紅綠燈證據、獨立審查與 Proof of Test 等 gate 不會降低。

> [!NOTE]
> 這些 gate 防的是 AI 自行降低標準，不是限制你的決策。驗收標準的形式依規模自動調整（Small 只需輕量驗收條件，風險高時補失敗路徑而不是改寫成 Gherkin），Scenario 多時可以分批核准，純重構與純文件任務改用等價證據；需要更快時，直接說「這次不用寫 Gherkin」或「不用先寫測試」即可豁免，AI 會照做並在 issue README 留下 `## Gate 豁免紀錄`。

若要使用 Superpowers，建議安裝[完整套件](https://github.com/obra/superpowers)，不要只複製單一 skill。核心流程會在下列 skills 可用時優先調用：

| Superpowers skill | 對應節點 | 用途 | 未安裝時 |
|---|---|---|---|
| `brainstorming` | `new-issue` | 一次一題澄清需求、比較方案並取得驗收標準核准 | 執行 `new-issue` 內建澄清與核准流程 |
| `writing-plans` | `decompose` | 將 Scenario 拆成 BDD 外迴圈與 TDD 內迴圈 | 執行 `decompose` 內建 Phase / Task 與覆蓋規則 |
| `test-driven-development` | `execute-task` | 強制紅燈、最小實作、綠燈與重構 | 執行 `execute-task` 內建雙迴圈狀態機 |
| `requesting-code-review` | `review` | 將變更交給獨立 reviewer | 使用宿主原生 subagent / task；沒有獨立 reviewer 能力時仍會阻塞 |
| `verification-before-completion` | `create-pr` | 在產生 PR 前重新查驗完成證據 | 執行 `create-pr` 內建 Evidence Rules 與 Completion Gate |

以下 skills 不屬於閉環的必要映射，但安裝完整套件後建議搭配使用：

| Superpowers skill | 建議使用時機 |
|---|---|
| `using-superpowers` | 在任務開始時判斷應優先載入哪個流程型 skill |
| `systematic-debugging` | 測試失敗、錯誤來源不明或修正前需要先定位根因 |
| `receiving-code-review` | 收到 review 意見後先驗證合理性，再進入修正流程 |
| `subagent-driven-development` | 宿主支援 subagent，且要依計畫逐 Task 隔離執行與審查 |
| `executing-plans` | 無 subagent 或需要在同一 session 依既有計畫批次執行 |

PRD 中常見的 `implementation-plan`、`critic`、`architectural-compliance`、`pull-request-spec` 不是本整合要求安裝的實際 skill 名稱；其能力已分別映射到 `writing-plans`、`requesting-code-review` 加架構 gate，以及 `create-pr` 的內建規格。

各平台安裝完整套件的方式不同，請依環境參考：[Claude Code](./docs/setup/claude.md#設定-superpowersplugin)、[OpenCode](./docs/setup/opencode.md#設定-superpowersplugin)、[Antigravity](./docs/setup/antigravity.md#設定-superpowers手動安裝)、[Windsurf](./docs/setup/windsurf.md#設定-superpowers手動安裝)、[Cursor](./docs/setup/cursor.md#設定-superpowers手動安裝)。

## 使用方式

1. **複製整個範本庫**  
   ```bash
   git clone https://github.com/raybird/dev-rules-kit.git
   ```

2. **依平台選用內容**  
   - 若使用 **Claude Code**：參考 [docs/setup/claude.md](./docs/setup/claude.md)
   - 若使用 **OpenCode**：參考 [docs/setup/opencode.md](./docs/setup/opencode.md)
   - 若使用 **Antigravity**：參考 [docs/setup/antigravity.md](./docs/setup/antigravity.md)
   - 若使用 **Windsurf**：參考 [docs/setup/windsurf.md](./docs/setup/windsurf.md)
   - 若使用 **Cursor**：參考 [docs/setup/cursor.md](./docs/setup/cursor.md)

3. **了解日常使用方式**  
   參考 [docs/usage.md](./docs/usage.md) 查看完整閉環示範與各 skill 快速參考。

4. **自訂與擴充**  
   根據個人或團隊需求，修改或新增 `skills/` 底下的技能定義，修改後於根目錄執行：
   ```bash
   python3 scripts/sync-skills.py
   ```
   即可自動同步並生成 `workflows/shared/` 目錄中對應的工作流程檔案。

## 下游專案掛載規則（Claude Code）

`rules/AGENTS.md` 是要複製到**下游專案**的可攜行為規則。在 **Windsurf / Cursor** 直接貼進 `.windsurfrules` / `.cursorrules` 即可；但 **Claude Code 只讀 `CLAUDE.md`，不會自動載入 `AGENTS.md`**，且子目錄的記憶體檔僅在存取該目錄時才「按需」載入，因此需要用 `@` 匯入語法手動掛載：

1. **複製規則檔到專案**（建議放根目錄，維持檔名 `AGENTS.md`）
   ```
   your-project/
   ├── AGENTS.md        ← 從本 kit 複製
   └── CLAUDE.md        ← /init 生成
   ```

2. **執行 `/init`** 生成專案特定的 `CLAUDE.md`（build / test / 架構說明）。

3. **在 `CLAUDE.md` 開頭加一行 `@` 匯入**，讓通用規則當基底、專案特定內容接在後面補充：
   ```markdown
   # CLAUDE.md

   @AGENTS.md

   ## （以下為 /init 生成的專案特定內容）
   ...
   ```

`@` 的路徑相對於 `CLAUDE.md` 所在位置：放根目錄寫 `@AGENTS.md`，放子目錄則寫 `@docs/rules/AGENTS.md`。注意 `@` 必須獨立成一行，且不能包在反引號或程式碼區塊裡，否則不會被解析。

> [!NOTE]
> 重跑 `/init` 可能覆蓋 `CLAUDE.md`、洗掉手動加的匯入行。對策：重跑後再補一次，或不用 `/init`、自行維護精簡的 `CLAUDE.md` 只放專案指令加 `@AGENTS.md`。

採「`AGENTS.md` 當可攜規則 + `CLAUDE.md` 匯入」的分離法，日後本 kit 更新規則時，下游專案只要重新複製 `AGENTS.md` 一個檔即可，不必改動 `CLAUDE.md`。

## 推薦工具

以下為搭配本範本庫使用的推薦開發輔助工具：

| 工具 | 用途 | 推薦原因 |
|------|------|----------|
| **[Serena](https://github.com/oraios/serena)** | 程式碼分析與符號查詢 MCP 伺服器 | 支援 LSP 層級的符號搜尋、重構、診斷等功能，可深度理解程式碼結構 |
| **[GitNexus](https://github.com/abhigyanpatwari/GitNexus)** | 程式碼知識圖譜分析工具 | 建立程式碼知識圖譜，支援影響分析、路由對應、API 形狀檢查等進階查詢 |
| **[Superpowers](https://github.com/obra/superpowers)** | 選用的 AI 開發流程增強框架 | 提供 brainstorming、TDD、review 與交付驗證等流程型 skills；未安裝時由本 kit 執行內建等價 gate |
| **[Wave Terminal](https://github.com/wavetermdev/waveterm)** | AI 整合跨平台終端機 | 開源且內建 AI 助手，支援多種模型（OpenAI、Claude、Ollama 等），提供持久 SSH 連線、區塊化工作區與遠端檔案編輯 |

各平台完整安裝步驟：

- **Claude Code**：[docs/setup/claude.md](./docs/setup/claude.md)
- **OpenCode**：[docs/setup/opencode.md](./docs/setup/opencode.md)
- **Antigravity**：[docs/setup/antigravity.md](./docs/setup/antigravity.md)
- **Windsurf**：[docs/setup/windsurf.md](./docs/setup/windsurf.md)
- **Cursor**：[docs/setup/cursor.md](./docs/setup/cursor.md)

## 版本與更新

下游專案更新已複製的檔案前，請先查閱 [CHANGELOG.md](./CHANGELOG.md)：每個條目標注影響的目錄，Major 版本代表破壞性變更（更新前應檢視自己的客製內容），Minor / Patch 可安全重新複製。

## 貢獻

歡迎提出 issue 或 PR 來優化通用的規則、工作流程與技能，讓所有開發者受益。

## 授權

MIT © Raybird
