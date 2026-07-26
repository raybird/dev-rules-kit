# BDD + TDD 硬性卡關設計

**日期**：2026-07-26
**狀態**：已實作

## 目標

將 Gherkin BDD 外迴圈與 TDD 內迴圈整合進既有 issue 開發閉環，讓需求共識、失敗測試、最小實作、重構、審查及 PR 證明都具備可追溯且不可跳過的完成 gate。

## 設計

- `new-issue` 在 `brainstorming` 可用時優先使用，否則執行內建等價流程；兩種模式都一次只問一題，共識核准後才寫入 Gherkin。
- `decompose` 在 `writing-plans` 可用時優先使用，否則以內建規則把每個 Scenario 拆成 BDD 外迴圈與 TDD 內迴圈。
- `execute-task` 在 `test-driven-development` 可用時優先使用，否則執行內建紅綠重構狀態機；缺少紅燈證據時一律禁止修改 production code。
- `review` 在 `requesting-code-review` 可用時優先使用，否則透過宿主原生能力取得獨立審查者；無獨立 reviewer 時仍阻塞。
- `create-pr` 在 `verification-before-completion` 可用時優先使用，否則執行內建證據 gate，只把具實際通過證據的 Scenario 列為 Proof of Test。
- `dev-cycle` 以文件中的 Gherkin、紅綠燈與審查 gate 判斷階段，不只依賴 branch、commit 或 PR 狀態。
- `docs/AGENTS.md` 作為 Gherkin 文件位置與證據格式的單一真相來源；雙語 `rules/` 提供無法繞過 skills 的全域底線。

PRD 中不存在的 Superpowers 名稱採可執行映射：`implementation-plan` 對應 `writing-plans`；`critic` 與 `architectural-compliance` 對應 `requesting-code-review` 加獨立審查者與架構 gate；`pull-request-spec` 的語意直接納入 `create-pr`，並以 `verification-before-completion` 防止虛構證明。

> [!NOTE]
> Superpowers 的依賴策略後續依 [Superpowers 選用整合設計](./2026-07-26-optional-superpowers-design.md) 調整為選用增強；本文件定義的完成 gate 維持強制。

## 適用性

所有會改變可觀察產品行為的功能、修正與重構都必須走完整 BDD + TDD 雙迴圈。純文件、格式或沒有可執行行為與測試入口的任務仍須用 Gherkin 定義驗收標準，但可用可重複的靜態或手動檢查替代 BDD runner，並記錄不適用理由；不得默默略過。

## 完成條件

- 單獨呼叫核心 skill 或透過 `dev-cycle` 都無法跳過對應 gate。
- Gherkin Scenario ID 可從 issue 文件追蹤至實作任務、測試證據、review 與 PR。
- 測試刪改、先寫 production code、沒有紅燈證據或虛構綠燈都會阻止流程前進。
- skill 與 workflow 經同步腳本保持逐位元組一致，雙語 rules 章節結構一致。
