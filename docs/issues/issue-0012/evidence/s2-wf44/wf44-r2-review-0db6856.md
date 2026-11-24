# 審查報告
- 範圍：完整交付範圍（main..HEAD）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：0db6856e3853e4694b56d084538e763e04615cfb
- Reviewed patch-id：d17d1b24f53650fa49e6726287e283d20a696b95
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId a12a64f6140559cba），非原實作者；協調者抽查規則引用

## 問題與風險

### MUST FIX

- **M1 SCN-001、SCN-002 的紅綠重構證據不完整**
  - 位置：`docs/issues/issue-3601/implementation-plan.md:9-10`
  - 現況：兩列只寫「`python3 -m unittest -v` 3 項全數通過」和「同上」。
    - 沒有外迴圈或單元紅燈的命令、exit code 與失敗原因。
    - 沒有重構階段的紀錄或 no-op 理由，也沒有被測提交。
    - 沒寫單迴圈合併的理由。
  - 依據：verification.md「紅綠重構證據」規定四段缺任一段即為證據不完整；review-evidence.md 把缺少必要證據列為 MUST FIX。
  - reviewer 在 BASE 版 `todo.py` 上實測：
    - `test_render_shows_due` 以 AssertionError 失敗（少了「（到期 11/20）」），是真的行為紅燈。
    - `test_overdue` 以 `AttributeError: module 'todo' has no attribute 'overdue'` 失敗。這是缺符號，不算目標行為的紅燈。
  - 建議：
    - SCN-001：記錄紅燈命令與原因、實作後全綠、重構全綠或 no-op 理由，以及被測 SHA。
    - SCN-002：先放一個回傳 `[]` 的 stub，取得 `[] != [1]` 的行為紅燈，再補其餘各段。
    - 兩項都寫明單迴圈合併的理由。

### SHOULD FIX

- **S1 Gherkin 綁內部函式，CLI 無法設定到期日或列出逾期**（`需決策`）
  - 位置：`docs/issues/issue-3601/README.md:22`、`docs/issues/issue-3601/README.md:28`、`todo.py:53-59`
  - 現況：When 寫的是「執行 render」「呼叫 overdue」，acceptance.md 要求 Scenario 描述外部行為。`main()` 沒有 overdue 子命令，`add` 也不能帶到期日：`add 繳費 --due 2026-11-20` 會把整串當成標題。
  - 影響：使用者只能手改 `todo.json` 才看得到到期日，`overdue()` 從 CLI 碰不到。commit 訊息寫「逾期清單」，會讓人以為已經能用。
  - 待決問題：本 issue 是否包含「設定到期日」與「列出逾期」的 CLI 路徑？
    - (a) 擴大範圍：新增 `add {標題} --due YYYY-MM-DD` 與 `todo.py overdue`，Gherkin 改寫成 CLI 層級，SCN-001、SCN-002 標為待重新核准。
    - (b) 維持函式層級：概述寫明本次只交付內部 API，CLI 另開 issue，並記入待確認事項的追蹤去向。
  - reviewer 建議 (a)。這題的答案會改變要補的測試層級，應在補 M1 證據之前先問。
- **S2 日期格式未驗證，字串比較會靜默算錯**（`需決策`：格式異常時要報錯還是略過）
  - 位置：`todo.py:32-39`、`todo.py:46-48`
  - 實測：
    - `due="2026-11-5"`、today 為 `2026-11-19` 時不算逾期，答案錯誤。
    - `due="2026/11/01"` 不算逾期。
    - `due="20261120"` 顯示成「（到期 120）」。
    - 整數 due 讓 `render` 拋 TypeError。
  - 建議：用 `datetime.date.fromisoformat` 寫一個共用的解析函式，`render` 與 `overdue` 都使用，並補格式異常的測試。
- **S3 到期當天與已完成項目的行為未經核准**（`需決策`）
  - 位置：`todo.py:39`、`todo.py:44-48`
  - 現況：`due == today` 不算逾期（嚴格 `<`），已完成的待辦也會顯示到期日。這兩項都是推導出來的可觀察行為，依 acceptance.md 應寫入 Gherkin 或待確認事項。
  - 建議：寫成 Scenario 並各補一個測試。reviewer 建議到期當天不算逾期、已完成項目照樣顯示到期日。
- **S4 TBD-1 欄位放錯格**
  - 位置：`docs/issues/issue-3601/README.md:49`
  - 現況：結論寫在影響欄，狀態欄沒有理由。AGENTS.md「待確認事項」規定結論、理由與日期都寫在狀態欄。
  - 狀態值仍以「已解決」開頭，流程工具判讀不受影響，所以列 SHOULD FIX。
- **S5 概述與 Timeline 混入進度**
  - 位置：`docs/issues/issue-3601/README.md:5`、`docs/issues/issue-3601/README.md:56-57`
  - 現況：document-types.md 規定進度只記在 `**狀態**` 與任務清單，AGENTS.md 規定 Timeline 只記語意事件。
  - 建議：刪掉概述的進度句，以及 Timeline 的「完成 S1／S2」兩列。
- **S6 implementation-plan 缺測試層級與完成判準**
  - 位置：`docs/issues/issue-3601/implementation-plan.md`
  - 現況：verification.md「雙迴圈追蹤」要求計畫記錄可觀察層級與完成判準。

### NICE TO HAVE

- N1 `docs/issues/issue-3601/README.md:13`：涉及檔案寫明 `test_due.py`，並列入根目錄 `README.md`。
- N2 `todo.py:32-34`：`due_of` 只包了一層 `.get`，`overdue` 又呼叫它兩次；docstring 的「issue-3601：」是交付歷程，不屬於程式碼。若照 S2 改成共用解析函式，這兩點會一起消失。
- N3 `README.md:10`：常青文件沒說到期日從哪裡來，等 S1 決定後一起補。
- N4 commit subject 沒有依 project.md 的 `type(scope):` 帶 scope。

## 已查核維度

- **驗收與證據**
  - SCN-001 由 `test_render_shows_due`（`test_due.py:7-9`）覆蓋，SCN-002 由 `test_overdue`（`test_due.py:11-16`）覆蓋，集合完整。
  - 期望值都是手寫字面值，沒有同義反覆，也沒有 mock。
  - 在 HEAD 執行 `python3 -m unittest -v` 得到 3/3 OK。
  - 證據完整度不符，見 M1。
- **規格修訂**
  - 核准 commit 是 `30ddef5`，為 HEAD 的祖先。
  - `git diff 30ddef5 0db6856 -- docs/issues/issue-3601/README.md` 只有核准 commit 回填、Timeline 與狀態的變動，Gherkin 未變，原核准有效。
- **相關失敗面**

| 輸入／狀態 | 預期 | 實際 | 覆蓋 | 判定 |
|---|---|---|---|---|
| 未完成，due 2026-11-20 | 行尾「（到期 11/20）」 | 符合 | 有測試 | OK |
| 沒有 due 欄位（TBD-1） | 輸出不變 | 符合 | test_render_marks_done | OK |
| due 為空字串或 None | 不顯示 | 不顯示 | 無測試 | OK |
| 已完成且有 due | 規格未定 | 照樣顯示 | 無測試 | S3 |
| due 等於 today | 規格未定 | 不算逾期 | 無測試 | S3 |
| 已完成且逾期 | 排除 | 排除 | 有測試 | OK |
| 跨年：due 2025-12-31，today 2026-01-01 | 逾期 | 逾期 | 無測試 | OK |
| due 2026-11-5（沒補零） | 逾期 | 不算逾期 | 無測試 | S2 |
| due 2026/11/01、20261120、整數 | 報錯或略過 | 靜默錯誤，整數拋 TypeError | 無測試 | S2 |
| 缺 done 欄位 | 規格未定 | KeyError | 無測試 | 既有資料一定有 done，不列為發現 |
| 從 CLI 設定到期日或列出逾期 | 使用者可操作 | 沒有入口 | 無測試 | S1 |

- **需求**：Gherkin 綁內部函式，使用者路徑不完整，見 S1。
- **架構**：只改單檔 `todo.py`，符合 project.md 的單檔 CLI 邊界。
- **安全**：沒有新依賴，沒有 I/O 或權限變動，不適用。
- **品質**：
  - 跨 Task 重複：S1、S2 都經由 `due_of` 取得到期日，取值邏輯一致，沒有分歧。
  - 過度設計：沒有，只有 N2 的小問題。
- **常青文件**：根目錄 `README.md` 已更新顯示說明，但不完整，見 N3。
- **issue 文件**：`**分級**` Medium、`**風險**` Low、`**狀態**`、`**核准 commit**` 都可被流程工具正確判讀。格式問題見 S4–S6、N1。

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。
- TBD-1 已解決，SCN-001 的無到期日行為與其結論相符。
- 限制：reviewer 的紅燈實測是把新測試跑在 BASE 版程式上重建的，不是實作當下的紀錄，不能代替 M1 要補的證據。

## 流程判定

RETURN TO execute-task

主因是 M1，必要驗收的證據有缺口。S1、S2、S3 需要使用者決策，建議在補證據前先取得答案，因為答案可能改變 Gherkin 與測試層級。
