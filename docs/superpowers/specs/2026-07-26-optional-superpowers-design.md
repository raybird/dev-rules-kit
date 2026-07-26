# Superpowers 選用整合設計

**日期**：2026-07-26
**狀態**：已實作

## 決策

Superpowers 改為推薦安裝的流程增強套件，不再是 `dev-rules-kit` 的執行期硬依賴。所有不可跳過的 BDD + TDD gate 由本 kit 的 skills、rules、issue 證據與 `dev-cycle` 狀態轉移直接定義。

## 執行模式

- 已安裝 Superpowers：優先調用對應 process skill，再依本地 skill 的完成 gate 驗證結果。
- 未安裝 Superpowers：直接執行本地 skill 內建的等價步驟，不得降低、略過或以口頭宣稱取代 gate。
- 缺少的是必要能力而非套件時仍須停止。例如 review 沒有可隔離的獨立 reviewer、專案有測試入口卻無法取得紅燈，或無法持久化 PR review，都不能用「未安裝 Superpowers」作為放行理由。

## 對應能力

| 本地節點 | 優先使用的 Superpowers skill | 永遠強制的本地 gate |
|---|---|---|
| `new-issue` | `brainstorming` | 一次一題、明確核准、Gherkin ID 與 hash |
| `decompose` | `writing-plans` | Scenario 對 BDD / TDD 雙迴圈映射 |
| `execute-task` | `test-driven-development` | BDD 紅燈、單元紅燈、最小實作、重構後全綠 |
| `review` | `requesting-code-review` | 獨立 reviewer、架構 gate、破壞性案例、持久化結果 |
| `create-pr` | `verification-before-completion` | 完整 Scenario 集合與實際 Proof of Test |

## README 說明

根 README 在開發閉環後新增說明，明確標示 Superpowers 非必要依賴；若選擇安裝，建議安裝完整套件而非散裝複製單一 skill。README 列出上述五個核心對應，以及 `using-superpowers`、`systematic-debugging`、`receiving-code-review`、`subagent-driven-development`、`executing-plans` 等輔助技能，安裝命令維持由各平台 setup 文件管理。

## 完成條件

- 未安裝 Superpowers 時，不會因套件缺少而停止核心閉環。
- 所有原有 BDD、TDD、review 與 PR gate 保持不變。
- README 清楚區分「本地必須遵守的 gate」與「建議安裝的外部 skills」。
- skills 與 workflows 同步、雙語規則一致、Markdown 連結有效。
