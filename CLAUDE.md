# CLAUDE.md

## Repository Nature

本 repo 的產品是 Markdown 規則、技能與下游文件規範，另有 Python／Bash 維護腳本，無 package manager。

修改後執行：

```bash
python3 scripts/check-kit.py
python3 scripts/check-links.py
bash -n scripts/install.sh
python3 scripts/test-install.py
python3 scripts/test-evidence.py
```

流程語意另依 [workflow-regression](docs/workflow-regression.md) 在目標宿主的新 session 驗證。靜態檢查或 Git fixture 成功不能宣稱 agent 行為通過；未實跑與環境限制寫入驗證狀態。

## 檔案責任

| 位置 | 維護責任 |
|---|---|
| `rules/` | 通用行為原則、issue 流程觸發入口；本 kit 自身也遵守 |
| `skills/` | 各階段輸入、操作、完成判準與輸出；各平台直接安裝 |
| `docs/AGENTS.md` | 下游文件入口、分級與風險、核心欄位、流程契約版本 |
| `docs/agents/` | 按階段載入的核准、驗證、review 規範及範本 |
| `docs/agents/project.md` | 下游專案客製；上游更新保留此檔 |
| `scripts/` | kit 檢查、安裝與回歸工具 |

`docs/AGENTS.md` 是下游產品，不要求本 kit 每次維護都建立 issue。完整行為定義放權威參考檔，技能保留可執行步驟與指向該定義的 gate。

## 維護規範

- 修改規則、技能、CLAUDE.md 或 docs/agents/ 前使用 [writing-rules](skills/writing-rules/SKILL.md)。新增內容先檢查能否擴充既有檔；歷史原因主要放維護紀錄。
- Markdown、commit 與 PR 使用繁體中文；英版 rules 例外。日期區分本次系統日期、歷史事件與未來窗口，不能全部改為今天。Commit 不加入 `Co-Authored-By: Claude`。
- `SKILL.md` 必須有 YAML frontmatter 的 `name:` 與 `description:`；name 與目錄同名，description 同時說用途與觸發時機。
- 引用下游核心規範的技能宣告最低流程契約，不與文件編輯版本同步跳號。相容版本也須檢查引用章節與語意。
- 雙語 rules 一起改，`##` 章節數與順序對應；check-kit 只查結構，語意同步另覆核。
- issue 的任務與證據各有唯一來源；狀態與 Git 證據修正時同步檢查 dev-cycle、執行、review 與 PR 分支。使用者可明確豁免流程，但不能豁免誠實回報。
- Superpowers 是選用引擎：brainstorming 對應需要探索的新需求；writing-plans 對應 decompose；test-driven-development 對應 execute-task；requesting-code-review 對應 review；verification-before-completion 對應 create-pr。已有核准或等價證據不因引擎切換失效；缺少套件時用本地流程。
- 安裝路徑維護在 rules/README.md、skills/README.md 與 install.sh targets_for()，check-kit 驗證一致性；外部工具設定在 docs/setup/tools.md。README 與 usage 僅引用路徑說明。
- 改流程時檢查 README.md、docs/usage.md、範本與檢查清單；check-kit 不驗證敘述語意。新增規則在 [rule-verification-status](docs/rule-verification-status.md) 記可指認的驗證來源，未實跑保留「僅靜態撰寫」。
- 改部署行為時，以暫存專案驗證升級、客製保留、衝突時不部分寫入、dry-run 與 symlink；本機真實平台及下游專案不作測試目標。
