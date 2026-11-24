# 審查報告
- 範圍：完整交付範圍（TARGET `main`）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：f0dfcc225a0c36e6770eea06315f4f4946b8c839
- Reviewed patch-id：4315cef861f7890aecb5669c3eb4251ae1e3af81
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId a3d5425f2b5586759），非原實作者；協調者複核規範引用
- 審查日期：2026-11-24

## 問題與風險

- **MUST FIX M1**：`docs/issues/issue-3601/implementation-plan.md:9-10`。S1 的綠燈紀錄寫「`python3 -m unittest -v` exit 0，Ran 3 tests OK」，但 S2 的紅燈紀錄寫的是 S1 之後才「先放回傳 `[]` 的 `overdue`」。在 S1 當下只可能是以下兩種情況，都不會得到「3 tests OK」：
  - test_due.py 只有 render 測試：test_todo 的 1 個加上 1 個，應為 Ran 2 tests。
  - test_due.py 已含 `test_overdue`：會出現 AttributeError，結果是 ERROR。

  「3 tests OK」只符合 S2 完成後的狀態。整個交付只有一個提交，無法從 Git 還原 S1 的真實狀態，所以 S1「最小實作後全綠」這一段不可信，紅綠重構證據不完整（verification.md）。目前沒有直接證據證明有意不實回報。
  - 建議：在只有 S1 變更的狀態下重跑並記錄真實結果；無法重建時，如實註明紀錄有誤與原因。
- **SHOULD FIX S1**：`implementation-plan.md:9-10`。S1 寫「被測內容即 H1 的 todo.py」，但 issue 裡沒有定義 H1；S2 則完全沒記被測提交或工作區狀態。這不符合 verification.md「證據重用」要記被測版本的要求。
  - 建議：寫明被測提交，或寫明被測的是哪個工作區狀態。
- **SHOULD FIX S2**：`todo.py:37-39`、`test_due.py:11-16`。到期日等於 today 的邊界沒有定義也沒有測試。實作用的是嚴格 `<`，若誤改成 `<=` 測試仍會通過。這屬於證據持久力問題，不影響本次驗收。
  - 建議：補一筆 `due == today` 的測試。若要把這個邊界寫進 Scenario，需先取得使用者核准。
- **SHOULD FIX S3 `需決策`**：`docs/issues/issue-3601/README.md:5`、`todo.py:18-21,53-59`。概述寫「待辦可以帶到期日…並能列出逾期」，但 CLI 既不能設定 due，也沒有列出逾期的命令。使用者只能手改 todo.json 才看得到到期日，`overdue` 從 CLI 無法觸發。交付符合已核准的 SCN-001／SCN-002，但兩個 Scenario 都綁在內部函式上（「執行 render」「呼叫 overdue」），和 acceptance.md「描述外部行為，不綁內部函式」不一致，這是核准時就有的問題。
  - 待決問題：本 issue 是否要讓使用者能從 CLI 使用這兩項功能？
  - 可選做法：
    - (a) 擴大範圍：新增 `add <標題> --due YYYY-MM-DD` 與 `overdue` 子命令，Scenario 需重新核准。
    - (b) 維持函式層級，在常青 README 說明 due 只能透過 todo.json 的 `due` 欄位設定。
    - (c) 另開 issue 追蹤，並記入 `## 待確認事項`。
  - reviewer 建議 (a) 或 (c)。
- **SHOULD FIX S4**：根目錄 `README.md:10`。常青文件只寫了顯示格式，沒有說明怎麼設定到期日，也沒有記載逾期功能。
  - 建議：依 S3 的決定補齊。
- **SHOULD FIX S5**：`docs/issues/issue-3601/README.md:5`。概述寫了進度（「S1、S2 都已完成，測試全數通過，等待審查」），違反 document-types.md:15「進度只記在 `**狀態**` 與任務清單」。這句在實作前的 30ddef5 就已存在，當時並不屬實。
  - 建議：改成只寫目標與範圍。
- **NICE TO HAVE N1**：`todo.py:32-39`。`due_of` 只包了一層 `item.get("due", "")`，在 `overdue` 中同一筆還呼叫兩次。docstring 的「issue-3601：」前綴把程式碼綁在追蹤編號上。
  - 建議：可以把這層包裝內聯，或在 comprehension 裡只取一次值。
- **NICE TO HAVE N2**：日期用字串比較，正確性依賴補零的 ISO 格式。例如 `2026-1-5` 對 today `2026-01-10` 會漏判。目前沒有輸入路徑能寫入這種資料。
  - 建議：日後加 CLI 輸入時，用 `date.fromisoformat` 驗證。
- **NICE TO HAVE N3**：`docs/issues/issue-3601/README.md:55-56`。Timeline 記了「完成 S1／S2」，但 docs/AGENTS.md:179 規定 Timeline 只記語意事件。
  - 建議：移除這兩列。
- **NICE TO HAVE N4**：`docs/issues/issue-3601/README.md:48`。TBD-1 的結論寫在影響欄（issue-checklist.md:14），狀態值本身正確，不影響工具判定。
  - 建議：把結論移到狀態欄。

## 已查核維度

- **驗收與證據**
  - 核准：依 acceptance.md 推導出的核准基線是 30ddef527b20780fe65cbe42380201c676422cc3，與 README 記的 `**核准 commit**: 30ddef5` 一致。30ddef5..HEAD 的 README 差異只有三處：核准 commit 回填、Timeline 兩列、`**狀態**`。Gherkin、核准來源與 TBD-1 都沒有變動，原核准有效。回填放在實作提交裡，符合規範。
  - SCN-001：`test_due.py:7-9` 以規格字面值斷言整行輸出，不是同義反覆。
  - SCN-002：`test_due.py:11-16` 以人工推導的 `[1]` 斷言，另含已完成與沒有 due 兩個干擾項。
  - TBD-1（沒有到期日時不顯示）：由 `test_todo.py:7-9` 承擔。
  - 在 HEAD 執行 `python3 -m unittest -v`：exit 0，Ran 3 tests，OK。
  - 結論：測試真實、沒有假綠燈，但 S1 的紀錄有 M1 的矛盾。
- **相關失敗面**
  | 輸入／狀態 | 預期 | 覆蓋 | 判定 |
  |---|---|---|---|
  | 沒有 due | 輸出維持原樣 | test_todo | 通過 |
  | due 為 null | 不顯示、不算逾期 | 實測正確，沒有測試 | 通過 |
  | 已完成且逾期 | 不在 overdue 清單 | test_due 的 id 3 | 通過 |
  | 已完成且有 due 時的 render | 規格沒有定義 | 會顯示到期日 | 可接受 |
  | due 等於 today | 不算逾期 | 實測正確，沒有測試 | S2 |
  | 非補零日期 | 沒有定義 | 字串比較會漏判 | N2 |
  | 跨年 | 只顯示 MM/DD | 符合規格 | 通過 |
- **需求**：符合已核准的 Scenario；需求範圍的缺口見 S3／S4。
- **架構**：變更只在 `todo.py`，沒有新增依賴。
- **安全**：沒有新的輸入路徑、權限面或依賴變更，不適用。
- **品質**：沒有跨 Task 的重複邏輯，也沒有過度設計；小幅簡化見 N1。
- **豁免、待確認與限制**：沒有 Gate 豁免。TBD-1 已解決，維持原狀。單一提交無法還原各 Task 當下的狀態，這是 M1 無法進一步查證的原因。

## 流程判定
RETURN TO execute-task

依據：M1 是必要的紅綠重構證據缺口（review-evidence.md「審查強度與流程判定」）。功能在 HEAD 是正確的。修正 M1 時建議一併處理 S1–S5；S3 需由使用者決定。
