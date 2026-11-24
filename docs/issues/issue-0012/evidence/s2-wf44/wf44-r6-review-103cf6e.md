# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：103cf6e3b4b42c83b0045ea25bb5b054baf919db
- Reviewed patch-id：597c29cef3271ea3e3a907083a2565b2bceb6517
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId aaa73758ee7c75bdd），非原實作者；協調者 Claude Opus 5.5 彙整

## 問題與風險

- MUST FIX：無

- SHOULD FIX 1 `需決策`：使用者目前無法設定到期日，也無法從 CLI 列出逾期待辦（`todo.py:18-21` 的 `add` 不接受 due；`todo.py:37-39` 的 `overdue` 在正式程式中沒有呼叫者；`README.md:10`；`docs/issues/issue-3601/README.md:5` 的概述寫「能列出逾期的未完成待辦」）。這在核准範圍內：SCN-002 的 When 是「呼叫 overdue」，所以不算缺漏。影響是只有手動編輯 todo.json 才用得到到期日，逾期清單完全碰不到。
  - 待決問題：設定 due、把逾期清單接到 CLI，是否屬於後續需求？
  - 可選做法：
    - (a) 另開 issue，並在本 issue 待確認事項記一筆 `不影響本次交付`，寫「追蹤：#新編號」。
    - (b) 擴大本 issue 範圍，新增 Scenario 並重新核准。
    - (c) 只在根目錄 README 註明 due 要手動寫進 todo.json。
  - 建議：(a)。根目錄 README 是否同時補一句來源說明，由使用者決定。
- SHOULD FIX 2：TBD-1 的欄位寫法不符 AGENTS.md「待確認事項」規則（`docs/issues/issue-3601/README.md:48`）。狀態欄只有「已解決：2026-11-16」，結論卻寫在影響欄。
  - 建議：狀態欄改成「已解決：不顯示（無到期日），維持原輸出；使用者 2026-11-16 選擇」；影響欄改成「未確認時無法決定 render 對無 due 項目的輸出；SCN-001」。
  - 狀態值仍以「已解決」開頭，工具判斷不受影響。這一節屬記帳區段，審查後再修改不會讓 PASS 失效。
- SHOULD FIX 3：進度寫在任務表以外的地方。
  - `docs/issues/issue-3601/README.md:5` 的概述寫了「目前 S1、S2 都已完成，測試全數通過，等待審查」。概述應只描述需求，進度以 implementation-plan.md 為準。概述是凍結章節，審查後修改需要重審。
  - `docs/issues/issue-3601/README.md:55-56` 的 Timeline「完成 S1／S2」不是 AGENTS.md 規定要記的語意事件（建立、核准、規格修訂）。
- NICE TO HAVE 1：`due == today` 的邊界沒有測試固定（`todo.py:39`、`test_due.py:11-16`）。實作用 `<`，今天到期的不算逾期，符合 docstring 的「早於」。但依推理，改成 `<=` 測試仍會全綠。這屬於證據持久力的改善，不是假綠燈。建議補一筆 due 為 `"2026-11-19"`、預期不回傳的資料。
- NICE TO HAVE 2：`## 涉及檔案`（`docs/issues/issue-3601/README.md:13`）沒列出常青文件 `README.md`，也沒寫出測試檔名 `test_due.py`。
- NICE TO HAVE 3：
  - `todo.py:39` 呼叫了兩次 `due_of(i)`。
  - `due_of` 只是包一行 `item.get("due", "")`。
  - docstring 前綴「issue-3601：」把程式碼綁在 issue 編號上。
  - 都不影響功能。

## 已查核維度

- 驗收與證據：
  - SCN-001：`test_due.py:7-9` 斷言整行 `"[ ] 1. 繳費（到期 11/20）"`，期望值是規格原文的字面值。證據在 implementation-plan.md S1。通過。
  - SCN-002：`test_due.py:11-16` 以 today 2026-11-19、due 11-01 與 12-01 斷言只回傳 `[1]`，另外涵蓋已完成（id 3）與沒有 due（id 4）。證據在 implementation-plan.md S2。通過。
  - TBD-1（無到期日維持原輸出）：由未改動的 `test_todo.py:7-9` 覆蓋，兩筆資料都沒有 due，且斷言完整字串。通過。
  - 在 HEAD 重跑 `python3 -m unittest -v`：exit 0，Ran 3 tests OK（協調者與 reviewer 各跑一次）。
- 證據真偽：
  - S1 紅燈（輸出少了到期日的 AssertionError）與 S2 紅燈（回傳 `[]` 的 stub 得到 `[] != [1]`）都是目標行為紅燈。
  - 單迴圈合併理由成立：`main` 直接 `print(render(load()))`；SCN-002 本身是函式層級驗收。重構記為 no-op 的理由成立。
  - 沒有同義反覆，也沒有弱化既有測試。
  - 證據持久力：S1 的綠燈在未提交的工作樹上執行，紅燈無法從歷史重現，但紀錄有命令、exit code 與原因，最終綠燈已在 HEAD 重現。這只是持久力偏弱，不構成缺失。
- 相關失敗面：

  | 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
  |---|---|---|---|
  | 既有資料缺 due 欄位 | 維持原輸出、不算逾期 | test_todo.py、test_overdue 的 id 4 | 通過 |
  | `"due": null` | 不顯示、不逾期 | 無；探測結果為 render `[ ] 1. a`、overdue `[]` | 通過 |
  | due 等於 today | 不算逾期（依 docstring 的「早於」） | 無；探測結果為 `[]` | 通過，見 NICE 1 |
  | 已完成且逾期 | overdue 排除；render 仍顯示到期日 | overdue 有 | 通過 |
  | 格式不是 YYYY-MM-DD | 規格未定義 | 無；`2026-1-5` 會顯示 1/5，overdue 的字串比較也會錯 | 目前沒有寫入 due 的輸入路徑，不阻擋；若採 SHOULD FIX 1 的 (a)／(b)，新 issue 需定義驗證 |

- 需求：與核准範圍一致，沒有超出；CLI 缺口見 SHOULD FIX 1。規格未被實質修改：`git diff 30ddef5 103cf6e -- docs/issues/issue-3601/README.md` 只有核准 commit 回填（`待提交` 改為 30ddef5，承載目前規格）、Timeline 兩列與狀態變更。核准來源為 2026-11-16 使用者回覆「核准」。
- 架構：單一檔案 CLI，新增的純函式沒有越界。常青文件（根目錄 README.md）已依 project.md 更新。
- 安全：不適用。這是本機單一使用者的 CLI，沒有權限或外部輸入面，也沒有新增依賴或 lockfile。
- 品質（含跨 Task 重複與過度設計）：S1、S2 共用 `due_of`，沒有分歧的重複，也沒有過度設計；小重複見 NICE 3。
- 豁免、待確認與限制：
  - 沒有 Gate 豁免。
  - TBD-1 已解決，有測試覆蓋。
  - 限制：紅燈階段無法從 Git 歷史重現，只依任務紀錄判讀。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
