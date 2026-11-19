# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：e88e38689ab9bf8aa763c40c8b7504d5735f88ed
- Reviewed HEAD SHA：0378aac90027ff846f304fe50f84fac1f79a0e9d
- Reviewed patch-id：82f276454d789477ff1bd5b2ae49b3a43d197cb2（`git diff e88e386 0378aac | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者，唯讀）
- Review artifact：本檔
- 增量覆審：上一份報告 review-775859c.md（H1=775859c，PASS）；增量範圍 `775859c..0378aac`。前提成立：H1 是 HEAD 的祖先，中間沒有 merge 提交；`git merge-base main HEAD` 仍是 e88e386。

## 問題與風險
- MUST FIX 1：`todo.py:40` 的 `overdue` 仍以 `due_of(i) < today` 做字串比較，但 0378aac 讓 `due_of`（`todo.py:33-35`）改回傳 MM/DD，而 `today` 是 YYYY-MM-DD。MM/DD 開頭是 0 或 1，比年份開頭的 2 小，因此所有有到期日的未完成待辦都會被判為逾期，包含未來的日期。用 SCN-002 原文實測，HEAD 回傳 `[1, 2]`，規格要求 `[1]`；到期日 2027-01-05 也被列出；775859c 上回傳 `[1]`。這是已核准驗收的回歸。建議把用來比較的值和顯示格式分開：`overdue` 以 ISO 值比較，或新增函式負責 MM/DD 顯示、`due_of` 維持回傳 ISO。兩種做法都符合 review-775859c SHOULD FIX 1 的原意。
- SHOULD FIX 1：`test_due.py:11-14` 的 `test_overdue` 沒有照 SCN-002 原文建立資料：第二筆是「沒有到期日」，不是「到期日 2026-12-01」，少了「未來到期不應列出」這一面，所以 HEAD 有回歸仍是綠燈。建議依原文加入到期日為 2026-12-01 的待辦；沒有到期日的情況另立案例。
- SHOULD FIX 2：`docs/issues/issue-3601/implementation-plan.md:11` S3 的證據只寫「3 項全數通過」，沒有被測提交，也沒有重構前後的對照（verification.md 對重構的要求）；既有測試也沒有涵蓋被重構的行為。修正 MUST FIX 1 時，先用 SCN-002 原文資料在 0378aac 上取得紅燈，再記錄修正後的綠燈。
- NICE TO HAVE：無

## 已查核維度
- 驗收與證據：HEAD 上執行 `python3 -m unittest -v`，3 項通過（test_overdue、test_render_shows_due、test_render_marks_done）。SCN-001：實測 render 輸出 `[ ] 1. 繳費（到期 11/20）`，`test_render_shows_due` 的期望值與規格字面一致，證據有效。SCN-002：不符合規格（MUST FIX 1）；它的綠燈是假綠燈（SHOULD FIX 1），不能當作證據。
- 相關失敗面：
  - 未來到期的未完成待辦（到期 2026-12-01，today 2026-11-19）：應不列出，實際被列出，失敗。
  - 跨年的未來日期（到期 2027-01-05）：應不列出，實際被列出，失敗。
  - 過去到期（到期 2026-11-01）：有列出，但只是碰巧正確，不是因為比較了日期。
  - 已完成的待辦：回傳空清單，通過。
  - 沒有到期日：render 不加括號、overdue 略過，通過。
  - review-775859c「以 ISO 字串比較，字串順序與日期順序一致」的結論在 HEAD 已不成立。
- 需求、架構、安全、品質：
  - `todo.py`：格式處理已移進 `due_of`，render（`todo.py:47-49`）只負責組字串；但另一個呼叫端 `overdue` 因此出錯，review-775859c 的 SHOULD FIX 1 不算修好。`due_of` 同時用於顯示和比較，改回傳格式就破壞了比較語意。
  - README：`## 現況` 位在 `## 概述` 之後，位置正確；其餘改動都在記帳區段。`**狀態**` 寫「修正完成，待覆審」，與審查結果不符。
  - implementation-plan.md：S3 證據不足（SHOULD FIX 2）。
  - review-775859c.md：新增後未再修改。
  - 安全：沒有安全面。
- 增量覆審時：
  - 重新查核：(1) `due_of` 的所有呼叫端，搜尋整個 HEAD 只有 `todo.py:40` 與 `todo.py:47`，理由是回傳格式改變；結果 render 正確、overdue 回歸。(2) test_overdue，它原本假設 due_of 回傳 ISO，理由是這個前提被改掉了；結果發現覆蓋缺口。(3) render 的兩個測試，因為 render 的實作改了，已在 HEAD 重跑，都通過。(4) review-775859c 的失敗面結論：「沒有到期日」「已完成」兩項已重驗並通過，「ISO 字串比較」一項已推翻。
  - 沿用：改動侷限於 todo.py 與測試、沒有安全面。`test_todo.py` 不在增量範圍內，也不依賴 due 欄位（已在 HEAD 重跑）。
- 豁免、待確認與限制：沒有豁免。TBD-1 已解決（使用者選擇「修正後覆審」）；這次退回是修正本身有錯，不需要再做需求決策。只做了本機唯讀審查，沒有遠端可核對。

## 流程判定
RETURN TO execute-task

依據：MUST FIX 1 讓已核准驗收 SCN-002 出現邏輯錯誤，現有測試也抓不到它。修正後先用 SCN-002 原文資料取得紅燈，再取得綠燈，然後重新覆審。review-775859c 的 PASS 只適用於 775859c，不沿用到 0378aac。
