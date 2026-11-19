# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due；TARGET main = BASE）
- Reviewed BASE SHA：71c48e2ef9a592dea9b780042535d2692ed09dd0
- Reviewed HEAD SHA：4853dbc9b53c0b8dff28c6833fab7ae71ea4cb52
- Reviewed patch-id：7f77e7135a4c8724ed5bfc766addc78ae0848562（已在 HEAD 用 `git diff 71c48e2 4853dbc | git patch-id --stable` 重算，結果相同）
- 獨立 reviewer：獨立 subagent（general-purpose）
- Review artifact：docs/issues/issue-3601/review-4853dbc.md
- 增量覆審：有上一份報告 docs/issues/issue-3601/review-775859c.md，但這次做完整審查。原因是增量覆審條件 1、2 都不成立：
  - 條件 1：分支已 rebase，該報告綁定的 HEAD 775859c 不是目前 HEAD 的祖先，H1 之後歷史已被改寫。
  - 條件 2：merge-base 由 e88e386 變成 71c48e2，與該報告的 Reviewed BASE 不同。

  該報告的結論都不沿用，全部在 4853dbc 重新查核。

## 問題與風險

### MUST FIX 1：SCN-002 的測試沒有涵蓋 Scenario 的 Given，驗不出「只回傳」
- 位置：`test_due.py:11-14`；對照 `docs/issues/issue-3601/README.md:30-34`。
- 落差：
  - Gherkin 的 Given 是兩筆**都有到期日**的未完成待辦（2026-11-01 與 2026-12-01），Then 是只回傳 11-01 那一筆。
  - `test_overdue` 用的卻是一筆 11-01，加上一筆**沒有到期日**的待辦。未到期的 12-01 這筆從沒出現在測試裡。
- 影響：這個測試分不出「已逾期」和「有到期日」。我在記憶體中把 `todo.overdue` 換成突變體 `lambda items, today: [i for i in items if todo.due_of(i)]`（回傳所有有到期日的待辦），`test_due.DueTest.test_overdue` 仍然通過（輸出 `OK`，`mutant(all-with-due) survived: True`）。
  - 所以 SCN-002 的區別性結果沒有可重現的證據。這是必要驗收的覆蓋缺口，不只是證據持久力不足。
  - 現行實作本身正確：用 SCN-002 原始 Given 在記憶體探測，`overdue(..., "2026-11-19")` 回傳 `[1]`。所以這屬於證據缺口，不是邏輯錯誤。
- 建議：
  - 讓 `test_overdue` 符合 Gherkin：兩筆未完成待辦，到期日 2026-11-01 與 2026-12-01，today 2026-11-19，斷言 id 只有 11-01 那筆。
  - 沒有到期日的情況可以留著，但改成另一個斷言或另一個案例。
  - 修好後在 implementation-plan 的 S2 列記錄這次修正的命令與結果。

### SHOULD FIX 1：S1、S2 的紅綠重構證據不完整
- 位置：`docs/issues/issue-3601/implementation-plan.md:9-10`。
- 落差：S1、S2 會改變可觀察行為，但只記了「`python3 -m unittest -v` 3 項全數通過」。外迴圈與單元測試的紅燈、失敗原因、被測提交和重構後綠燈都沒記（verification.md「紅綠重構證據」）。
- 現況：我在 HEAD 重跑測試，綠燈成立（見下方「驗收與證據」）。依指示只讀，這次沒在 BASE 重現紅燈。
- 建議：修 MUST FIX 1 時一併補上 S2 的紅燈（先在 BASE 或實作前跑新測試並記錄失敗原因）。S1 能從歷史重現紅燈就補記，不能重現就明列限制。

### SHOULD FIX 2（`需決策`）：到期當天算不算逾期，還沒核准
- 位置：`todo.py:38-39`（`due_of(i) < today`，嚴格小於）。
- 現況：實作與 docstring 都採「到期日早於 today 才算逾期」，到期當天不列入。這是合理的預設，但 SCN-002 沒有規定這個邊界，屬於規劃時推導出的可觀察行為，依 acceptance.md 應先取得使用者接受。目前也沒有測試鎖住這個邊界。
- 待決問題：到期日等於今天的未完成待辦，`overdue` 要不要列出？
- 可選做法：
  - (a) 不列入（維持現狀）。補一個 Scenario 或 SCN-002 的附註取得核准，並補測試 `due == today → 不回傳`。
  - (b) 列入。改成 `<=`，同樣補 Scenario 與測試。
- 建議：採 (a)。「逾期」一般指過了到期日，也和現有 docstring 一致。

### SHOULD FIX 3（`需決策`）：CLI 沒有設定到期日或列出逾期的入口，常青 README 是否需要更新取決於範圍
- 位置：`todo.py:53-59`（`main` 只有 add／done／列出），`todo.py:18-21`（`add` 不寫入 `due`）；根目錄 `README.md:5-9`。
- 現況：
  - 已核准的 Gherkin 只到函式層（「執行 render」「呼叫 overdue」），實作符合核准範圍。
  - 但概述（`docs/issues/issue-3601/README.md:5`）寫的是使用者功能「待辦可以帶到期日……能列出逾期」。目前使用者只能手改 `todo.json` 才能讓 `due` 出現，`overdue` 也沒有 CLI 指令。
  - 因為沒有使用者入口，這次變更不會觸發 project.md「使用者功能 → 根目錄 README 使用說明」的更新責任，根目錄 README 不更新可以接受。
- 待決問題：這個 issue 要不要提供使用者入口？
- 可選做法：
  - (a) 維持函式層範圍，另開 issue 做 CLI 入口。在本 issue 的待確認事項記下這個決定。
  - (b) 在本 issue 新增 Scenario 並核准（例如 `add <標題> --due YYYY-MM-DD`、`overdue` 子命令），連同根目錄 README 使用說明一起交付。
- 建議：採 (a)，維持已核准範圍，避免未經核准的規格擴張。改採 (b) 時，根目錄 README 必須一起更新。

### NICE TO HAVE 1：沒有測試鎖住「已完成待辦不列入 overdue」
- 位置：`todo.py:39`（`not i["done"]`）；`test_due.py` 沒有已完成且已過期的案例。
- 現況：概述寫「逾期的**未完成**待辦」，SCN-002 的 Given 也限定未完成，所以這不是核准 Scenario 的明文結果。實作正確（記憶體探測時，已完成且到期日 11-01 的 id 3 沒有被回傳）。
- 建議：補一個已完成且已過期、不應回傳的案例，提升回歸防護。

### NICE TO HAVE 2：到期日格式沒有驗證，比較依賴 ISO 補零格式
- 位置：`todo.py:32-34, 39, 48`。
- 現況：`overdue` 以字串比較日期，`render` 用 `due[5:]` 切出月日，兩者都假設嚴格的 `YYYY-MM-DD`。
  - 遇到 `"2026-12-1"` 這類非補零值，字串比較會失真。探測：today `"2026-12-01"` 時回傳 `[]`。若 today 是 `"2026-12-10"`，`"2026-12-1" < "2026-12-10"` 會成立，結果才剛好正確，屬於偶然。
  - `render` 會顯示補零的 `01/05`。SCN-001 只驗 11/20，沒有規定要不要補零。
- 評估：目前沒有寫入 `due` 的程式入口，資料只會來自手改 JSON，風險低。
- 建議：之後加 CLI 入口（見 SHOULD FIX 3）時，在入口處用 `datetime.date.fromisoformat` 驗證並正規化。

### NICE TO HAVE 3：`overdue` 呼叫兩次 `due_of`
- 位置：`todo.py:39`。
- 建議：可簡化為 `due_of(i) and due_of(i) < today`，改寫成單次取值，或者直接利用 `"" < today` 恆為真的特性……後者不可行，會把沒有到期日的待辦也列入。所以只建議在可讀性上保持現狀，或用海象運算子取一次值。純可讀性，不阻塞。

## 已查核維度

### 驗收與證據
- 本次在 HEAD 4853dbc 執行 `python3 -m unittest -v`，exit 0：

  ```
  test_overdue (test_due.DueTest.test_overdue) ... ok
  test_render_shows_due (test_due.DueTest.test_render_shows_due) ... ok
  test_render_without_due (test_due.DueTest.test_render_without_due) ... ok
  test_render_marks_done (test_todo.RenderTest.test_render_marks_done) ... ok
  ----------------------------------------------------------------------
  Ran 4 tests in 0.000s

  OK
  ```

- SCN-001（`docs/issues/issue-3601/README.md:24-28`）：由 `test_due.py:7-9` 覆蓋。斷言完整行等於 `"[ ] 1. 繳費（到期 11/20）"`，期望值是規格原文的字面值，不是同義反覆。結論：通過。
- SCN-002（`docs/issues/issue-3601/README.md:30-34`）：`test_due.py:11-14` 沒有涵蓋 Given 的 12-01 未到期待辦，突變體會存活，見 MUST FIX 1。結論：**證據缺口**。實作行為經記憶體探測是正確的。
- S3（`implementation-plan.md:11`）：上一份報告的 SHOULD FIX 1（沒有到期日時 render 的測試）已處理。
  - `test_due.py:16-18` 斷言 `"[ ] 2. 寫週報"`，不帶括號，期望值是獨立字面值。
  - 使用者已選「修正後覆審」（README:52 TBD-1）。
  - 這是為既有行為補的測試，不改變行為，不需要紅燈。
  - 結論：已處理。
- 核准基線：
  - 核准 commit 已填 `a643668`，不是 `待提交`，所以不用推導。
  - 我用 `git diff --quiet 15c547c a643668 -- docs/issues/issue-3601/` 確認，原核准 commit 15c547c 與 rebase 後的 a643668 在 issue 目錄內容完全相同（輸出 `SAME_ISSUE_DIR`），驗收區塊也就相同，映射成立。
  - `git diff a643668 4853dbc -- docs/issues/issue-3601/README.md` 只變更了以下內容：新增 `## 現況`、`**核准 commit**` 由 `待提交` 改為 `a643668`、新增 `## 待確認事項`（TBD-1）、Timeline 兩列、`**狀態**` 由 `待實作` 改為 `審查中`。
  - Gherkin 的條件、動作、結果都沒變，原核准（2026-11-16 使用者回覆「核准」）有效。

### 相關失敗面

| 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
|---|---|---|---|
| 有到期日、未完成，render | 行尾「（到期 MM/DD）」 | `test_due.py:7-9` | 通過 |
| 沒有到期日，render | 不帶括號 | `test_due.py:16-18` | 通過 |
| 已完成且有到期日，render | 顯示 `[x]` 並附到期日 | 無測試；探測輸出 `[x] 1. x（到期 01/05）` | 行為合理，規格未規定，不阻塞 |
| SCN-002 原始 Given（11-01 與 12-01），overdue | 只回傳 11-01 | 無；現有測試的突變體會存活 | **MUST FIX 1** |
| 沒有到期日，overdue | 不回傳（`due_of` 回傳 `""`，短路排除） | `test_due.py:12-14` 的 id 2 | 通過 |
| 已完成且已過期，overdue | 不回傳 | 無測試；探測正確 | NICE TO HAVE 1 |
| 到期日等於 today，overdue | 未核准；實作不回傳 | 無 | SHOULD FIX 2 `需決策` |
| 日期字串比較 | ISO `YYYY-MM-DD` 補零時，字串順序等於日期順序，結果正確 | 隱含在現有測試中 | 在補零前提下成立，見 NICE TO HAVE 2 |
| 非 ISO 或非補零的 due | 規格未定義 | 無；沒有寫入入口 | NICE TO HAVE 2，低風險 |
| 既有清單輸出回歸（沒有 due 的舊資料） | 輸出與變更前相同 | `test_todo.py:7-9` 仍綠，`test_due.py:16-18` | 通過 |

### 需求、架構、安全、品質
- 需求：實作符合已核准的函式層 Scenario。使用者入口的範圍有落差，已列為 SHOULD FIX 3 `需決策`。
- 架構：變更侷限在 `todo.py` 的純函式與新測試檔，`render` 與 `overdue` 共用 `due_of` 取值，沒有越界，也沒有更動資料讀寫。
- 安全：沒有新的外部輸入、權限、依賴或檔案存取面。不適用。
- 品質（code-simplify 標準）：
  - 跨 S1–S3 沒有分歧的重複邏輯，到期日取值集中在 `due_of`。
  - `due_of` 是很薄的包裝，但兩處共用，而且統一了「沒有 due 時回傳空字串」的語意，不算過度設計。
  - 只有 NICE TO HAVE 3 這種可讀性細節。
  - `render` 拆成迴圈，可讀性尚可。
- 常青文件：CLI 沒有可讓使用者設定 due 或查詢逾期的入口，所以這次不觸發根目錄 `README.md` 使用說明的更新責任。若決定加入口，就會觸發，見 SHOULD FIX 3。

### 豁免、待確認與限制
- 豁免：沒有 Gate 豁免紀錄。
- 待確認：TBD-1（`docs/issues/issue-3601/README.md:52`）已解決，對應的修正（S3）已確認完成。
- 限制：
  - 依指示只讀，沒有在 BASE 實際重現 S1、S2 的紅燈。
  - 突變與邊界探測都在記憶體中進行（`python3 -B -c`），沒有寫入 repo。
- 記帳提醒：`docs/issues/issue-3601/README.md:9` 的 `**現行 review**` 仍指向 review-775859c.md，保存這份報告的提交應改指 review-4853dbc.md。

## 流程判定
RETURN TO execute-task

原因：MUST FIX 1。SCN-002 的必要驗收證據沒有涵蓋 Scenario 的 Given 與「只回傳」的區別性結果。修正後需要重新審查。屆時若條件 1、2 都成立（4853dbc 為祖先、沒有改寫歷史、merge-base 仍是 71c48e2），可以用這份報告做增量覆審。SHOULD FIX 2、3 的 `需決策` 項目，請協調者依 acceptance.md「逐題確認」取得使用者答案後，記入 README `## 待確認事項`。
