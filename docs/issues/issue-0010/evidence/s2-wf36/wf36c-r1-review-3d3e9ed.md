# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：71c48e2ef9a592dea9b780042535d2692ed09dd0
- Reviewed HEAD SHA：3d3e9edfdf8aab36788fb5431fc4f26b4c43620b
- Reviewed patch-id：95ce37c7fca9502f25a38442a5c48b7afa7db467
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-3601/review-3d3e9ed.md
- 增量覆審：上一份報告 review-775859c.md；不採增量的原因：`git merge-base --is-ancestor 775859c HEAD` 判定 775859c 不是目前 HEAD 的祖先（rebase 改寫歷史），merge-base 也從 e88e386 換成 71c48e2，review-evidence.md 增量覆審第 1、2 項條件都不成立，改做完整審查。

## 問題與風險
- MUST FIX 1：SCN-002 的 Then 沒有被測試真正斷言。
  - 規格 docs/issues/issue-3601/README.md:32-34 的 Given 有兩筆未完成待辦，到期日 2026-11-01 與 2026-12-01，要求「只回傳到期日為 2026-11-01 的那一筆」。
  - 測試 test_due.py:11-14 的資料是一筆 2026-11-01 加一筆沒有到期日的待辦，沒有放「到期日晚於今天」的那一筆。
  - 結果是 todo.py:39 的日期比較 `due_of(i) < today` 沒有被任何測試約束。突變驗證：刪掉這個比較後，overdue 會回傳所有有到期日的未完成待辦，`python3 -m unittest` 仍然 4 項 OK。
  - 這是必要驗收的覆蓋缺口。上一份報告 review-775859c.md:15 判定 SCN-002 已由 `test_overdue` 覆蓋，這個結論不成立。
  - 修正方式：依 Given 原文補一筆 `due: "2026-12-01"` 的未完成待辦（可以和現有資料並存），斷言只回傳 id 1；並在 implementation-plan.md 補紅綠證據，紅燈可以用上述突變取得。
- SHOULD FIX 1：overdue 排除已完成待辦的條件沒有測試。
  - todo.py:39 的 `not i["done"]` 對應概述 README.md:5「逾期的未完成待辦」與 SCN-002 Given 的「未完成」。
  - 突變驗證：刪掉這個條件，測試仍然全綠。
  - 建議在 test_due.py 補一筆已逾期但 `done: True` 的待辦，斷言它不在回傳結果中。
- SHOULD FIX 2：implementation-plan.md 的證據不完整。
  - implementation-plan.md:9-11 的 S1、S2、S3 只記「unittest N 項全數通過」，沒有外迴圈或單元測試的紅燈、失敗原因，也沒有重構或 no-op 紀錄。
  - verification.md:94-101 規定只有「測試已通過」的文字不構成證據，四段缺任一段即為證據不完整。
  - 修正 MUST FIX 1 時一併補齊紅綠重構證據，或寫明單迴圈合併的理由。
- NICE TO HAVE 1（需決策）：到期日等於今天時算不算逾期，規格沒有定義。
  - 目前的行為：todo.py:39 用嚴格小於，所以 `due == today` 不算逾期（實測 `overdue([due 2026-11-19], "2026-11-19")` 回傳空串列），和 todo.py:38 docstring「早於 today」一致。但這個邊界不在核准的 Gherkin 內，也沒有測試；把比較改成小於等於，測試仍然全綠。
  - 待決問題：到期當天是否視為逾期？
  - 可選做法：(a) 維持「當天不算逾期」，新增 Scenario 送核准並補測試；(b) 改成當天也算逾期，新增 Scenario 送核准；(c) 不入規格，只在 README 待確認事項記為假設。
  - 建議：(a)。符合現有實作與 docstring，「逾期」的一般語意也是過了到期日。
- NICE TO HAVE 2：格式不正確的到期值會被靜默錯判。
  - overdue 用字串比較，render 用 `due[5:]` 切字串，兩者都假設 todo.json 裡是補零的 YYYY-MM-DD。
  - 實測 `2026-1-5` 會顯示成「（到期 1/5）」；`2026-2-1` 這類沒補零的值，字串順序大於 `2026-11-19`，會被判為未逾期。
  - `today` 傳入 datetime.date 時會丟 TypeError；`due` 為 null 或空字串時和沒有到期日一樣處理。
  - 目前 CLI 沒有設定到期日的入口（todo.py:18-21 的 add 不接受 due），這類值只會出現在手改的 todo.json，列為非阻塞。可考慮在 due_of 用 `date.fromisoformat` 驗證，或在 docstring 註明格式前提。
- NICE TO HAVE 3（需決策）：功能沒有接到 CLI。
  - main（todo.py:53-59）沒有設定到期日或列出逾期的子命令；使用者只能從 `python3 todo.py` 的列表看到手動寫入的到期日。
  - 核准的 Gherkin 以函式層級描述（「執行 render」「呼叫 overdue」），本次交付符合核准範圍。
  - 待決問題：是否要開放 CLI 設定到期日、列出逾期？
  - 可選做法：(a) 本 issue 維持函式層級；(b) 另開 issue，新增 CLI 子命令與對應 Scenario。
  - 建議：(a) 並另開 issue (b)。在本 issue 擴充會改變需求邊界，需要新的核准。

## 已查核維度
- 驗收與證據：
  - 核准來源：`git diff 15c547c a643668 -- docs/issues/issue-3601/` 輸出 0 行，映射成立。`git diff a643668 HEAD -- docs/issues/issue-3601/README.md` 只動到 `## 現況`、`**核准 commit**`、`## 待確認事項`、`## Timeline`、`**狀態**` 等記帳區段，Gherkin 區塊 README.md:21-35 和核准版本一致。`## 現況` 位於 `## 概述` 之後（README.md:7-9）。
  - SCN-001：test_due.py:7-9 以字面值斷言「[ ] 1. 繳費（到期 11/20）」，有效。
  - SCN-002：Then 沒有被斷言，見 MUST FIX 1。
  - 上一份報告的 SHOULD FIX 1 已修好：test_due.py:16-18 的 `test_render_without_due` 斷言沒有到期日時輸出「[ ] 2. 寫週報」。
  - reviewer 在 HEAD 執行 `python3 -B -m unittest -v`：test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 皆 ok，Ran 4 tests，OK。
  - 突變測試在 repo 外暫存目錄以 HEAD 檔案執行，三個突變全部存活：刪除 `< today`、刪除 `not done`、小於改成小於等於。
- 相關失敗面：
  - 依規格 Given 的實際資料：overdue 回傳 2026-11-01 那一筆，行為正確，但沒有測試，見 MUST FIX 1。
  - 沒有到期日：render 不帶括號，有測試；overdue 略過，test_due.py:12-14 間接覆蓋。
  - 已完成待辦：overdue 略過，實測正確，但沒有測試，見 SHOULD FIX 1。
  - 到期日等於今天：不算逾期，規格未定義，見 NICE TO HAVE 1。
  - 格式不正確、null、空字串、today 型別不符：見 NICE TO HAVE 2。
  - 日期字串比較：只有補零的 ISO 格式時，字串順序和日期順序一致，結論成立。
- 需求、架構、安全、品質（含跨 Task 重複與過度設計）：
  - `git diff --stat BASE HEAD` 只有 todo.py、test_due.py 與 docs/issues/issue-3601/ 下的文件；根目錄 README.md 的變更來自 main 上的 71c48e2（等於 BASE），不在本範圍。
  - 沒有安全或權限面，沒有新相依。
  - due_of（todo.py:32-34）由 render 與 overdue 共用，抽象程度適中；S3 是對 S1 的測試補強，沒有過度設計。
  - 常青文件（project.md：使用者功能要更新根目錄 README.md 使用說明）：本次沒有新增 CLI 命令或參數，判定不觸發；若日後依 NICE TO HAVE 3 開放 CLI，就要更新 README。
- 豁免、待確認與限制：
  - 沒有 Gate 豁免。TBD-1 已解決。
  - 流程契約 2.6。
  - 突變測試只涵蓋 overdue 的三個條件，沒有對 render 的切字串邏輯做突變。

## 流程判定
RETURN TO execute-task
