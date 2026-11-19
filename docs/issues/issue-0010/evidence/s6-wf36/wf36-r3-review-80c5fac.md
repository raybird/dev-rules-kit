# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：39045ddd5d3458dcf1b32a66f990983c56e2ef07
- Reviewed HEAD SHA：80c5facb93056d735ee9eb8d61eab40c6b0da495
- Reviewed patch-id：d691168220ed86168e157ee5ed5830e505324c83
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-3601/review-80c5fac.md
- 增量覆審：上一份報告 review-bc1f2b0.md，增量範圍 bc1f2b0..80c5fac（bc1f2b0 是 HEAD 的祖先、無 merge 與改寫歷史；merge-base 仍為 39045dd；流程契約 2.6）

## 問題與風險
- MUST FIX 1（邏輯錯誤，增量引入的回歸）：`todo.py:35` 的 `due_of` 改回傳 MM/DD 後，`todo.py:40` 的 `overdue` 仍以 `due_of(i)` 與 YYYY-MM-DD 的 `today` 做字串比較。MM/DD 首字元只會是 0 或 1，小於 today 的首字元 2，因此所有未完成且有到期日的待辦都被判為逾期。實測今天 2026-11-19、到期日 2026-11-01 與 2026-12-01 時，HEAD 回傳 [1, 2]，bc1f2b0 回傳 [1]，違反 SCN-002。建議把比較用的 ISO 日期與顯示格式分開（例如 `overdue` 直接讀 `item.get("due", "")`，或另設格式化函式給 render），並先補 MUST FIX 2 的測試取得紅燈再修。
- MUST FIX 2（必要驗收覆蓋缺口／假綠燈）：`test_due.py:11-14` 的 `test_overdue` 第二筆待辦沒有到期日，而 SCN-002 的 Given 是到期日 2026-11-01 與 2026-12-01 兩筆，「未來到期日不算逾期」完全沒有斷言；HEAD 上行為錯誤而 3 項測試全綠。上一份報告「SCN-002 由 test_overdue 覆蓋」的結論本就不完整。建議測試資料改為規格原文，期望 [1]，並保留無到期日、已完成兩種情況。
- SHOULD FIX 1（證據不足）：`docs/issues/issue-3601/implementation-plan.md:11` 的 S3 把改動當成不改變行為的重構，只記錄「3 項全數通過」，實際上 `overdue` 的可觀察行為已改變。依 verification.md，既有覆蓋不足時應先補 characterization test 再重構。建議修正後補齊紅綠證據，並如實記錄 S3 曾造成回歸。
- NICE TO HAVE：無

## 已查核維度
- 驗收與證據：SCN-001 由 `test_render_shows_due` 以字面值「[ ] 1. 繳費（到期 11/20）」斷言，HEAD 實測正確，覆蓋為真。SCN-002 覆蓋不完整且 HEAD 行為錯誤（MUST FIX 1、2）。HEAD 重跑 `python3 -m unittest -v`：Ran 3 tests，OK（test_overdue、test_render_shows_due、test_render_marks_done），此綠燈不代表 SCN-002 正確。
- 相關失敗面（HEAD 臨時腳本實測，腳本在 /tmp，未寫入 repo）：
  - 沒有到期日：`due_of` 回傳空字串，render 不加括號，overdue 略過——正確。
  - 已完成且有過去到期日：overdue 略過——正確。
  - 未來到期日 2026-12-01：被誤判逾期——錯誤。
  - 跨年過去到期日 2025-12-31：有回傳，但只是碰巧正確，MM/DD 一律小於 today。
  - 上一份報告「due_of 回傳 YYYY-MM-DD，字串順序與日期順序一致」的前提已被增量推翻，overdue 結論不沿用。
- 需求、架構、安全、品質：上一份 SHOULD FIX 1 的目標（render 不再自行切日期，`todo.py:47-49` 直接用 due_of）已達成；但 due_of 原是 render 與 overdue 共用的資料存取點，改成顯示格式化函式造成職責混用與 MUST FIX 1。due_of 呼叫端只有 `todo.py:40` 與 `todo.py:47`；overdue 無其他 production 呼叫端；render 呼叫端為 `todo.py:60`、test_due.py、test_todo.py。無安全面。
- 增量範圍逐檔結論：
  - `todo.py`：SHOULD FIX 1 目標達成，但引入 MUST FIX 1。
  - `docs/issues/issue-3601/implementation-plan.md`：S3 證據不足（SHOULD FIX 1）。
  - `docs/issues/issue-3601/README.md`：只改記帳區段（現況、待確認事項、Timeline、狀態），凍結內容（Gherkin、核准紀錄、分級、風險）未變動。
  - `docs/issues/issue-3601/review-bc1f2b0.md`：上一份報告，未再修改。
- 增量覆審時重新查核的項目與理由：overdue（呼叫被修改的 due_of 且依賴其格式）——不合格；render 與 test_todo.py（render 被修改）——重跑通過；test_overdue（前提被改變）——發現覆蓋缺口；上一份報告的相關失敗面（論證前提被推翻）——重新查核如上。
- 沿用的結論：「改動侷限於 todo.py 與 test_due.py，無安全面」——完整範圍的程式檔仍只有這兩個，沿用。其餘皆重新查核。
- 豁免、待確認與限制：無 Gate 豁免；兩項 MUST FIX 都是規格內的明確錯誤，不需使用者決策。

## 流程判定
RETURN TO execute-task

修正後以本報告（綁定 80c5fac、完整範圍）為上一份報告做增量覆審。
