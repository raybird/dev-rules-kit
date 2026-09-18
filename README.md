# dev-rules-kit

一套給 AI 開發環境使用的規則與技能範本庫，集中整理 `rules`、`skills` 兩類 Markdown 資產，方便在 **Codex**、**OpenCode**、**Claude Code**、**Antigravity** 等工具中重複使用與維護。

這個 repo 的重點不是執行程式，而是提供可直接複製、調整、同步的開發規範與操作流程，讓個人或團隊能用一致方式管理 AI agent 的行為、工作流程與文件產出。

## 目錄結構

```
dev-rules-kit/
├── README.md              # 本說明文件
├── CHANGELOG.md           # 變更紀錄（下游更新參考）
├── CLAUDE.md              # AI 維護指引
├── scripts/               # 自動化工具
│   ├── check-kit.py       # kit 一致性檢查（frontmatter、契約相容性、安裝路徑）
│   ├── check-links.py     # Markdown 相對連結檢查
│   ├── install.sh         # 平台安裝與更新
│   ├── init-project.py    # 下游專案文件初始化
│   ├── test-install.py    # 安裝與初始化回歸測試
│   └── test-evidence.py   # Git 證據與契約相容性測試
├── docs/                  # 技術文件與規範說明
│   ├── AGENTS.md          # 文件資料夾說明（AGENTS）
│   ├── agents/           # 按階段載入的規範及 project.md 客製檔
│   ├── usage.md           # 使用指南（含開發閉環步驟）
│   ├── setup/tools.md     # 外部工具設定（Serena / GitNexus / Superpowers）
│   └── _templates/        # 實體文件模板（架構、領域、Changelog）
├── rules/                 # 靜態規則檔（agents、coding style、linting 等）
│   ├── AGENTS.md          # 安裝路徑見 rules/README.md
│   ├── AGENTS.zh-TW.md
│   └── README.md
└── skills/                # 可重複使用的技能定義（skill，共 10 個技能）
    ├── code-simplify/
    ├── create-commit/
    ├── create-pr/
    ├── decompose/
    ├── dev-cycle/
    ├── execute-task/
    ├── git-squash/
    ├── new-issue/
    ├── review/
    └── writing-rules/
```

## 用途

此 repo 主要提供可跨平台重用的 Markdown 範本，依用途拆分為以下幾類：

- **`docs/`**  
  技術文件與規範說明，包含文件資料夾結構規範（AGENTS.md）與 issue 文件模板。  

- **`rules/`**  
  存放各種靜態規則，例如 AI agent 的行為規範、程式碼風格約定、專案架構準則等。  
  適合直接複製到專案的 `.cursorrules` 或對應的設定檔中。

- **`skills/`**  
  儲存可被 AI 或工具呼叫的「技能」，以子目錄形式組織，每個子目錄包含 `SKILL.md` 定義。  
  重量級 skill（如 `review`、`decompose`）包含完整的輸入、輸出規範與使用範例；輕量 skill（如 `create-commit`）僅列執行步驟，維持簡潔。

## 開發閉環

一般局部修改可直接執行；需要 issue 追蹤時使用 10 個技能中的核心流程：

```text
new-issue → decompose（Large，在原計畫細化）
          → execute-task（內含 code-simplify 與驗證）
          → create-commit → create-pr → review
                              ↑           │
                              └──修正後───┘
```

`dev-cycle` 協調已授權的工作，自動選擇相依滿足的 Task；查詢模式只讀不寫。等待合併、外部窗口或必要回答時回報並結束本次調用，之後可再次呼叫恢復。「不修復」保留決策與審查依據，不要求製造實作或 merge。

`git-squash` 是獨立合併輔助工具，`writing-rules` 用於維護規範。各技能可單獨使用，不需要把所有技能逐一執行。詳細範例見 [使用指南](docs/usage.md)。

## Superpowers 整合與安裝建議

Superpowers 是本 kit 的**選用流程增強套件，不是必要依賴**。未安裝時，`new-issue`、`decompose`、`execute-task`、`review`、`create-pr` 仍會執行各自內建的等價流程，驗收標準核准、真實驗證、獨立審查與 Proof of Test 依本地流程契約執行。已有授權與有效證據不因切換引擎重做。

> [!NOTE]
> 這些 gate 防的是 AI 自行降低標準，不是限制你的決策。驗收標準的形式依規模自動調整（Small 只需輕量驗收條件，風險高時補失敗路徑而不是改寫成 Gherkin），Scenario 多時可以分批核准，純重構與純文件任務改用等價證據；需要更快時，直接說「這次不用寫 Gherkin」或「不用先寫測試」即可豁免，AI 會照做並在 issue README 留下 `## Gate 豁免紀錄`。

若要使用 Superpowers，建議安裝[完整套件](https://github.com/obra/superpowers)，不要只複製單一 skill。核心流程會在下列 skills 可用時優先調用：

| Superpowers skill | 對應節點 | 用途 | 未安裝時 |
|---|---|---|---|
| `brainstorming` | `new-issue` | 需要探索時釐清需求與方案；已有明確核准則沿用 | 依 `agents/acceptance.md` 核對來源並處理必要缺項 |
| `writing-plans` | `decompose` | 將 Scenario 拆成 BDD 外迴圈與 TDD 內迴圈 | 執行 `decompose` 內建 Phase / Task 與覆蓋規則 |
| `test-driven-development` | `execute-task` | 強制紅燈、最小實作、綠燈與重構 | 執行 `execute-task` 內建雙迴圈狀態機 |
| `requesting-code-review` | `review` | 將變更交給獨立 reviewer | 使用宿主原生 subagent / task；沒有獨立 reviewer 能力時仍會阻塞 |
| `verification-before-completion` | `create-pr` | 在產生 PR 前重新查驗完成證據 | 依 `agents/review-evidence.md` 核對範圍與有效證據 |

以下 skills 不屬於閉環的必要映射，但安裝完整套件後建議搭配使用：

| Superpowers skill | 建議使用時機 |
|---|---|
| `using-superpowers` | 在任務開始時判斷應優先載入哪個流程型 skill |
| `systematic-debugging` | 測試失敗、錯誤來源不明或修正前需要先定位根因 |
| `receiving-code-review` | 收到 review 意見後先驗證合理性，再進入修正流程 |
| `subagent-driven-development` | 宿主支援 subagent，且要依計畫逐 Task 隔離執行與審查 |
| `executing-plans` | 無 subagent 或需要在同一 session 依既有計畫批次執行 |

PRD 中常見的 `implementation-plan`、`critic`、`architectural-compliance`、`pull-request-spec` 不是本整合要求安裝的實際 skill 名稱；其能力已分別映射到 `writing-plans`、`requesting-code-review` 加架構 gate，以及 `create-pr` 的內建規格。

各平台安裝完整套件的方式不同（Claude Code 用 plugin marketplace、OpenCode 用 git URL、其餘平台需手動 clone 加 symlink），請參考 [docs/setup/tools.md 的 Superpowers 章節](./docs/setup/tools.md#設定-superpowers)。

## 使用方式

1. **複製整個範本庫**  
   ```bash
   git clone https://github.com/raybird/dev-rules-kit.git
   ```

2. **把需要的資產複製到你的平台**  

   ```bash
   bash scripts/install.sh            # 自動偵測平台，安裝 skills
   bash scripts/install.sh --dry-run  # 先看會做什麼
   bash scripts/install.sh --list     # 列出五個平台與對應路徑
   ```

   規則檔預設不安裝（該位置常有本機客製內容），需要時加 `--with-rules`。各平台的實際路徑與手動安裝方式見兩個資料夾的 README：
   - 規則檔：[rules/README.md](./rules/README.md#安裝方式)
   - 技能：[skills/README.md](./skills/README.md#安裝方式)

3. **初始化每個下游專案的文件規範**

   在本 kit 根目錄執行（目標專案目錄須已存在）：
   ```bash
   python3 scripts/init-project.py /path/to/project --dry-run
   python3 scripts/init-project.py /path/to/project
   python3 scripts/init-project.py /path/to/project --check
   ```
   這會部署 `docs/AGENTS.md`、`docs/agents/`、`docs/_templates/` 與部署基線。專案客製內容寫入 `docs/agents/project.md`，上游更新保留它。

   更新已初始化的專案：
   ```bash
   python3 scripts/init-project.py /path/to/project --update --dry-run
   python3 scripts/init-project.py /path/to/project --update
   ```

   更新只覆蓋與上次部署基線一致的核心；本地修改、缺基線的不同檔案、symlink／hardlink 或路徑衝突會整批停止。`--check` 查核心一致性與客製檔存在，客製語意仍需覆核。

   舊版首次升級需依 [客製邊界](docs/AGENTS.md#客製邊界與同步策略) 人工移出客製內容、合併核心，再初始化部署基線。技能改宣告最低「流程契約」版本，文件編輯版本另行記錄；純說明更新不迫使全部技能與專案同步跳號。

4. **（選用）設定外部工具**
   Serena、GitNexus、Superpowers 的各平台設定見 [docs/setup/tools.md](./docs/setup/tools.md)。

5. **了解日常使用方式**
   參考 [docs/usage.md](./docs/usage.md) 查看完整閉環示範與各 skill 快速參考。

6. **自訂與擴充**
   根據個人或團隊需求，修改或新增 `skills/` 底下的技能定義，修改後於根目錄執行：
   ```bash
   python3 scripts/check-kit.py   # 檢查 frontmatter 與契約相容性
   bash scripts/install.sh        # 重新安裝到各平台
   ```

## 下游專案掛載規則（Claude Code）

`rules/AGENTS.md` 是要複製到**下游專案**的可攜行為規則。在 **Cursor** 直接貼進 `.cursorrules` 即可；但 **Claude Code 只讀 `CLAUDE.md`，不會自動載入 `AGENTS.md`**，且子目錄的記憶體檔僅在存取該目錄時才「按需」載入，因此需要用 `@` 匯入語法手動掛載：

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

四個平台的完整設定步驟（MCP 設定檔位置、JSON 範例、驗證與移除）：[docs/setup/tools.md](./docs/setup/tools.md)

## 版本與更新

下游專案更新已複製的檔案前，請先查閱 [CHANGELOG.md](./CHANGELOG.md)：每個條目標注影響的目錄，Major 版本代表破壞性變更（更新前應檢視自己的客製內容），相容更新使用 `--update`，客製檔仍保留；既有核心有本地變更則先合併。

## 貢獻

歡迎提出 issue 或 PR 來優化通用的規則與技能，讓所有開發者受益。

## 授權

MIT © Raybird
