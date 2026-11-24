# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf（main，即 merge-base）
- Reviewed HEAD SHA：627fcc9cd1fa0466b84cfdbcd4c6c825103c1391
- Reviewed patch-id：00063a049f4ef7f9bbdee01706ea1b851332f730（`git diff 70f4ada 627fcc9 | git patch-id --stable`）
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId afbf35b6b6a9953eb），不是原實作者；協調者另外核對 diff 與測試

## 問題與風險

### MUST FIX

- **M1 SCN-002 還沒核准就已實作並標為完成**（`需決策`）
  - 位置：`docs/issues/issue-3601/README.md:41`（SCN-002 是 `待核准`）、`docs/issues/issue-3601/README.md:52`（TBD-2 是 `待確認`）、`todo.py:37-39`、`test_due.py:11-16`、`docs/issues/issue-3601/implementation-plan.md:9`（S2 是 ✅）
  - 影響：acceptance.md「分批核准」只允許實作已核准的 Task，並要求 PR 前所有現存驗收條件都已核准。`overdue()` 用 `due < today`，等於自行決定了「到期當天不算逾期」，但這正是 TBD-2 還沒回答的問題。這屬於流程契約 2.8 的「缺少新行為的核准來源」。
  - 待決問題：到期日等於今天時，算不算逾期？
    - (a) 不算，用 `<`，也就是現在的實作；
    - (b) 算，用 `<=`。
  - reviewer 建議：取得使用者原話後，把 TBD-2 改成 `已解決` 並寫上結論與日期，SCN-002 改為 `已核准`，Then 補上「today 等於 due」的結果，再加一個邊界測試。如果答案是 (b)，程式與測試都要改。
- **M2 紅綠重構證據不完整**
  - 位置：`docs/issues/issue-3601/implementation-plan.md:8-9`
  - 影響：證據只有「`python3 -m unittest -v` 3 項全數通過」。外迴圈與單元紅燈、紅燈的失敗原因、重構階段（或 no-op 理由）、exit code、被測提交都沒有記錄。verification.md 規定四段缺任一段就是證據不完整，只有「測試已通過」的文字不構成證據。
  - 建議：每個 SCN 補上以下內容：
    - 紅燈的命令與失敗原因。例如在 BASE 上，render 少了「（到期 11/20）」而 assertion 失敗；overdue 不存在而 AttributeError。
    - 最小實作後的綠燈。
    - code-simplify 的結果或 no-op 理由。
    - 被測提交。
    - 如果外迴圈與內迴圈要合併，寫出合併理由。

### SHOULD FIX

- **S1 測試數量寫得不精確**
  - 位置：`docs/issues/issue-3601/implementation-plan.md:8`、`docs/issues/issue-3601/README.md:59`
  - 問題：「完成 S1，測試 3 項通過」把整套 3 項都算在 S1 名下。S1 只對應 test_render_shows_due 一項；S1、S2 又在同一個提交 `627fcc9`，沒有證據顯示 S1 單獨驗證過。以 HEAD 而言「3 項通過」本身屬實，所以不列為不實回報。
  - 建議：改寫成「於 `627fcc9` 執行，Ran 3 tests OK；SCN-001 對應 test_render_shows_due，SCN-002 對應 test_overdue」。
- **S2 核准來源沒寫對應的驗收編號**
  - 位置：`docs/issues/issue-3601/README.md:36`、`:58`
  - 問題：「使用者回覆『核准』」沒寫對應哪些 Scenario（acceptance.md「逐題確認」）。Timeline 寫「建立並核准」，但實際只核准了 SCN-001。
  - 建議：兩處都明寫「SCN-001」。
- **S3 Timeline 記了步驟完成**
  - 位置：`docs/issues/issue-3601/README.md:59-60`
  - 問題：Timeline 只記語意事件，進度看任務清單；另外「負責人」欄不在範本裡。
  - 建議：刪除這兩列。
- **S4 概述寫了進度**
  - 位置：`docs/issues/issue-3601/README.md:5`
  - 問題：「目前 S1、S2 都已完成，測試全數通過，等待審查」違反 document-types.md「進度只記在 `**狀態**` 與任務清單」，也把還沒核准的 S2 寫成完成。
  - 建議：概述只留目標與範圍。
- **S5 TBD-1 的結論寫在影響欄**
  - 位置：`docs/issues/issue-3601/README.md:51`
  - 問題：結論與理由應寫在狀態欄，影響欄只寫未確認時的影響與驗收編號。狀態值開頭仍是 `已解決`，工具不會判斷錯，所以列 SHOULD。
- **S6 使用者沒有任何 CLI 入口可以用這個功能**（`需決策`）
  - 位置：`todo.py:18-21`（add 不能帶 due）、`todo.py:53-59`（沒有 overdue 子命令）、`docs/issues/issue-3601/README.md:23,29`（When 寫的是「執行 render／呼叫 overdue」）
  - 問題：概述寫「能列出逾期的未完成待辦」，但實際上只在函式層成立。使用者只能手動編輯 todo.json 來設 due，也無法列出逾期。acceptance.md 要求 Scenario 描述外部行為，不綁內部函式。
  - 待決問題：本次範圍要不要包含 CLI 入口？
    - (a) 維持函式層，在概述與根目錄 README 寫明設定方式；
    - (b) 加 `add --due` 與 `overdue` 子命令，改寫 Gherkin 並重新核准；
    - (c) 另開 issue 追蹤。
  - reviewer 建議：(c) 或 (b)。

### NICE TO HAVE

- **N1** `todo.py:39`：`due_of(i)` 呼叫了兩次，可以寫成 `"" < due_of(i) < today`。`due_of` 只是一行包裝，內聯也可以。docstring 的「issue-3601：」前綴是交付歷程，不屬於程式語意。
- **N2** `todo.py:39,48`：日期比較靠字串字典序，沒有驗證格式。`"2026/11/01"`、`"2026-2-1"` 都會被誤判為不逾期，`"2026-1-5"` 會顯示成「1/5」。目前沒有寫入入口，依 YAGNI 可以接受；之後加入口時，在寫入端驗證。
- **N3** `todo.py:47-48`：已完成的待辦也會顯示到期日，SCN-001 只規定了未完成的情況。建議記入待確認事項，或在常青文件裡寫明。
- **N4** `docs/issues/issue-3601/README.md:13`：「對應的測試檔」太籠統，應寫明 `test_due.py` 與根目錄 `README.md`。
- **N5** `README.md:10`：常青文件已依 project.md 更新，內容正確，但沒說明到期日怎麼設定。

## 已查核維度

### 驗收與證據

| 編號 | 核准 | 證據位置 | 結論 |
|---|---|---|---|
| SCN-001 | 已核准 2026-11-16，核准 commit `df95965` | `test_due.py:7-9`；`docs/issues/issue-3601/implementation-plan.md:8` | 行為與規格一致；HEAD 綠燈（協調者重跑 `python3 -m unittest -v`：Ran 3 tests，OK）；紅燈與重構段缺（M2） |
| SCN-002 | **待核准** | `test_due.py:11-16`；`docs/issues/issue-3601/implementation-plan.md:9` | 缺核准來源（M1）；證據不完整（M2） |

- 核准基線：`df95965` 是最後一個修改 `**核准來源**` 欄位行的提交。
- `git diff df95965 627fcc9 -- docs/issues/issue-3601/README.md` 只改了 `**核准 commit**`（從 `待提交` 改成 `df95965`）、Timeline 與 `**狀態**`，Gherkin 沒動，所以 `df95965` 承載目前的規格。
- 測試真偽：
  - 期望值都是手寫字面值，沒有 mock、略過或同義反覆，不是假綠燈。
  - 從程式碼推論，BASE 上的紅燈會是真紅燈，但沒有實際跑，也沒有記錄。
  - 證據持久力：today 等於 due 的邊界沒有覆蓋，等 TBD-2 定案後補上。

### 相關失敗面

| 輸入／狀態 | 預期 | 實際 | 現有覆蓋 | 判定 |
|---|---|---|---|---|
| 沒有 due 欄位 | render 維持原輸出（TBD-1）；不逾期 | 符合 | `test_todo.py`；`test_due.py` 的 id 4 | 通過 |
| `due=""` 或 `None` | 視同沒有到期日 | 符合（falsy 守門） | 無 | 正確，沒有測試 |
| `due="2026/11/01"` 或 `"2026-2-1"`，today 為 2026-11-19 | 逾期 | 判為不逾期 | 無 | N2；目前沒有寫入入口 |
| today 等於 due | 規格沒有定義 | 不逾期 | 無 | M1，需決策 |
| 跨年 `2025-12-31` | 逾期，顯示 12/31 | 符合 | 無 | 通過 |
| done=True 且 due 已過 | 不列入逾期 | 符合；render 仍顯示到期日 | `test_due.py` 的 id 3 | 通過；顯示屬 N3 |
| 未來到期日 | 不逾期 | 符合 | `test_due.py` 的 id 2 | 通過 |
| CLI 設定 due 或列出逾期 | 概述宣稱可用 | 沒有入口 | 無 | S6，需決策 |

### 需求、架構、安全、品質

- 需求：SCN-001 符合規格。SCN-002 的邊界還沒核准（M1）。CLI 範圍見 S6。
- 架構：只改單檔 `todo.py`，沒有新增依賴，跟 project.md 的邊界一致。
- 安全：沒有新增輸入面、權限或外部依賴，不適用。
- 品質：跨 Task 的重複只有 `due_of` 的重複呼叫（N1），沒有分歧，也沒有過度設計。
- 常青文件：根目錄 `README.md` 已依 project.md 的觸發條件更新（N5）。

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。
- TBD-2 維持 `待確認`，它阻擋 SCN-002 的核准（M1）。
- 限制：新測試在 BASE 上的紅燈沒有實際跑，只從程式碼推論。邊界探測腳本放在 repo 外，沒有保存。

## 流程判定
RETURN TO execute-task

理由：有兩項 MUST FIX。
- M1：SCN-002 還沒核准就實作，而且 PR 前全部驗收已核准的條件不成立。
- M2：紅綠重構證據不完整。

先由使用者決定 M1、S6 這兩項 `需決策`，再補證據、修正文件，最後重新審查（符合條件時可增量覆審）。
