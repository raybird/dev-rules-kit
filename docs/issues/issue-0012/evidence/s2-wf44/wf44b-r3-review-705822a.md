# 審查報告
- 範圍：完整交付範圍（`main..issue-3601-due`）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf（main 與 HEAD 的 merge-base）
- Reviewed HEAD SHA：705822aff82dd234c13326bdf701998b9d9aa863
- Reviewed patch-id：3e03df882e536395094d6e4b0ae5ef3df64aa26d（`git diff 70f4ada 705822a | git patch-id --stable`）
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId ac71c51a0650e94ca），不是原實作者；由協調者核對引用位置後保存

## 問題與風險

### MUST FIX

1. **SCN-002 還沒核准就實作並送審**（`需決策`）
   - 位置：`docs/issues/issue-3601/README.md:41`（SCN-002 的狀態是 `待核准`）、`docs/issues/issue-3601/README.md:52`（TBD-2 `待確認`）、`todo.py:37-39`、`test_due.py:11-16`。
   - 影響：違反 `docs/agents/acceptance.md:56` 的兩條規定：「只實作已核准…的 Task」，以及「PR 前所有現存驗收條件都須已核准」。這屬於 `docs/agents/review-evidence.md:80` 說的「缺少新行為的核准來源」。實作用 `due_of(i) < today`（`todo.py:39`），等於替使用者決定了 TBD-2：到期日等於今天時不算逾期。實測 `overdue([{... "due": "2026-11-19"}], "2026-11-19")` 回傳 `[]`。
   - 待決問題：到期日等於今天時，算不算逾期？SCN-002 是否核准？
   - 可選做法：
     - (a) 以今天為界，當天不算逾期（維持 `<`）。
     - (b) 當天就算逾期（改成 `<=`）。
     - (c) 把 SCN-002 和 `overdue` 移出本次交付。
     - (d) 依 Gate 豁免紀錄明列豁免。
   - 建議：(a)。「逾期」一般指過了到期日，現有實作也不用改。核准後補一個「到期日等於今天」的測試，再更新核准紀錄表和 TBD-2。

### SHOULD FIX

2. **沒有使用者可用的入口**（`需決策`）
   - 位置：`todo.py:18-21`（`add` 不收 due）、`todo.py:53-59`（CLI 沒有逾期指令）、根目錄 `README.md:10`。
   - 影響：使用者沒辦法照使用說明建立帶到期日的待辦，也沒辦法列出逾期。這和 issue 概述（`docs/issues/issue-3601/README.md:5`）的「能列出逾期」有落差。另外，兩個 Scenario 的 When 都綁在函式名稱（README:23「執行 render」、README:29「呼叫 overdue」），和 `docs/agents/acceptance.md:36`「描述外部行為，不綁內部函式」不一致。
   - 待決問題：本次交付要不要包含設定 due 的入口和 CLI 逾期清單？已完成的待辦要不要顯示到期日？目前會顯示 `[x] 1. t（到期 11/20）`，規格沒有定義。
   - 可選做法：
     - (a) 只交付函式層。根 README 註明 due 目前要手動編輯 todo.json，入口另開 issue 追蹤，記入待確認事項。
     - (b) 本次就加入口。Scenario 改寫成外部行為並重新核准，同時補格式驗證。
   - reviewer 建議：(b)。協調者補充：(a) 比較符合 YAGNI 和目前已核准的範圍。
3. **根目錄 `README.md:10` 只寫了顯示格式**：依 #2 的結論，補上設定 due 的方式，或逾期清單的用法。
4. **issue 流程文件的寫法**（`docs/agents/review-evidence.md:80`：格式類問題不阻塞）
   - `docs/issues/issue-3601/README.md:5` 的概述寫了「S1、S2 都已完成，測試全數通過」，進度出現在任務表以外的地方（`AGENTS.md:124`「進度只留在一處」）。
   - `docs/issues/issue-3601/README.md:59-60` 的 Timeline 記了「完成 S1／S2」，但 `docs/AGENTS.md:179` 規定 Timeline 只記建立、核准、規格修訂這類語意事件。同一個 Timeline 第 58 行的「建立並核准」，容易讓人以為兩個 Scenario 都核准了。
   - `docs/issues/issue-3601/README.md:51`：TBD-1 的結論寫在影響欄。`docs/AGENTS.md:139` 規定結論寫在狀態欄，影響欄只寫未確認時的影響。
   - `docs/issues/issue-3601/implementation-plan.md:9`：「被測內容即 H1 的 todo.py」裡的 H1 沒有定義，應改成具體的提交 SHA 或工作區狀態（`docs/agents/verification.md:87`）。

### NICE TO HAVE

5. `todo.py:39` 呼叫了兩次 `due_of(i)`，可以只呼叫一次。`due_of`（`todo.py:32-34`）只是一行 `.get` 包裝，也可以直接內嵌。
6. 補測試：到期日等於今天（依 #1 的答案）、多筆且有無 due 混在一起的 render、已完成待辦帶到期日的 render（依 #2 的答案）。
7. 提交訊息 `feat: 待辦支援到期日與逾期清單` 缺少 scope 和 `Refs: #3601`（`docs/agents/project.md:11`）。`docs/issues/issue-3601/README.md:13` 的「對應的測試檔」應寫明是 `test_due.py`，並列入根目錄 `README.md`。

## 已查核維度

### 驗收與證據

- **SCN-001**：已核准（2026-11-16，README:40）。
  - 測試在 `test_due.py:7-9`，期望值是規格原文的字面值 `"[ ] 1. 繳費（到期 11/20）"`，不是同義反覆。
  - 單迴圈合併的理由成立：`todo.py:59` 直接 `print(render(load()))`。
  - TBD-1（沒有到期日時輸出不變）由既有的 `test_todo.py` 覆蓋。
  - 證據有效。
- **SCN-002**：測試在 `test_due.py:11-16`，期望值是字面值 `[1]`，並且排除了已完成和沒有 due 的待辦，沒有 mock，不是假綠燈。但這個 Scenario 是 `待核准`，見 MUST FIX 1。
- **重跑結果**（在 705822a、工作區乾淨下執行）：`python3 -m unittest -v`，exit 0，`Ran 3 tests ... OK`（`test_overdue`、`test_render_shows_due`、`test_render_marks_done`）。
- **核准基線**：README 的 `**核准 commit**` 是 df95965（不是 `待提交`）。
  - 用 `docs/agents/acceptance.md:69` 的推導命令在 705822a 上取得的也是 df95965，兩者一致。
  - `git diff df95965 705822a -- docs/issues/issue-3601/README.md` 只動到三處：核准 commit 回填、Timeline 加兩列、`**狀態**` 從 `待實作` 改成 `審查中`。Gherkin 和核准表都沒變，df95965 承載的就是目前的規格。
- **證據持久力**（不阻塞）：沒有測試守住「到期日等於今天」的邊界；render 只測了單筆資料。

### 相關失敗面

| 輸入或狀態 | 預期 | 實際 | 覆蓋 | 判定 |
|---|---|---|---|---|
| 舊資料沒有 due 欄位 | 輸出不變（TBD-1） | `[ ] 1. t` | `test_todo.py` | 正確 |
| `due` 是 `""` 或 `None` | 視為沒有到期日 | 不加後綴；overdue 不列入 | 無 | 正確 |
| 已完成的待辦帶 due | 規格沒定義 | 顯示到期日 | 無 | 推導出的行為，併入 SHOULD FIX 2 |
| due 等於 today | TBD-2 未定 | 不算逾期 | 無 | MUST FIX 1 |
| 已完成的待辦已過期 | 不列入逾期 | 不列入 | `test_due.py:14` | 正確 |
| 不是補零的 YYYY-MM-DD，或 due 是整數 | 沒定義 | 字串比較會錯；`due[5:]` 會切錯，整數時丟出 TypeError | 無 | 目前沒有寫入 due 的入口，只能手改 todo.json。依 `AGENTS.md:31`（不處理不可能發生的錯誤），本次不阻塞。加入入口時，必須同時加格式驗證（SHOULD FIX 2） |

### 需求、架構、安全、品質

- **需求**：SCN-001 符合規格。SCN-002 未核准（MUST FIX 1）。入口範圍待決定（SHOULD FIX 2）。
- **架構**：改動只在單檔 `todo.py`，符合 `docs/agents/project.md:7`。資料結構只多了可選的 `due` 欄位，舊資料相容。
- **安全**：不適用。沒有新的輸入來源、權限或外部依賴，也沒有改動 lockfile 或依賴。
- **品質**：兩個 Task 之間沒有分歧的重複邏輯，共用 `due_of`，也沒有過度設計。小幅簡化見 NICE TO HAVE 5。
- **常青文件**：根目錄 `README.md` 已更新顯示格式，內容不完整（SHOULD FIX 3）。

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。
- TBD-1 已解決。TBD-2 `待確認`，維持原狀態，交付影響見 MUST FIX 1。
- 限制：邊界案例用 repo 外的探針腳本實測，沒有保存到 repo。

## 流程判定
RETURN TO execute-task
