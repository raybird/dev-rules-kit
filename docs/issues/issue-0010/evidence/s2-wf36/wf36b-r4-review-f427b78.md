# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due），增量覆審
- Reviewed BASE SHA：e88e38689ab9bf8aa763c40c8b7504d5735f88ed
- Reviewed HEAD SHA：f427b78a40bafe10ac2f13f55008bd75935826c5
- Reviewed patch-id：f6f5526eda46ed191d92bbe6b962a2b864b35d37（`git diff e88e386 f427b78 | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者）
- Review artifact：本檔
- 增量覆審：上一份報告 [review-e2ff4af.md](review-e2ff4af.md)（PASS，H1 = e2ff4af8f05064c4178e34cf8cdd9c468f0c71b6）；增量範圍 `e2ff4af..f427b78`。前提：H1 是 HEAD 的祖先，中間無 merge、無改寫歷史；`git merge-base main f427b78` = e88e386，與上一份報告的 Reviewed BASE 相同；流程契約 2.6。

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE 1：`todo.py:39` 的 `overdue` 對同一筆待辦呼叫兩次 `due_of(i)`，行為正確；可以先存成變數再比較，也可以不動。
- NICE TO HAVE 2：`test_due.py:18-20` 的 `test_render_without_due` 與 `test_todo.py` 的 `test_render_marks_done` 都驗證沒有到期日時不帶括號，有輕微重複；新測試放在 issue 測試檔，對應 SCN-001 比較清楚，可保留。

## 已查核維度
- 驗收與證據：在 HEAD f427b78 執行 `python3 -m unittest -v`，4 項全數通過（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done）。SCN-001 由 `test_render_shows_due`、`test_render_without_due` 覆蓋；SCN-002 由 `test_overdue` 覆蓋。驗收集合與核准的 Scenario 相同。`git diff 15c547c f427b78` 中 Gherkin 區塊沒有變動，核准 commit 15c547c 仍有效。
- 上一份報告 SHOULD FIX 1：已修好。新測試以 `assertEqual` 比對手寫的完整字串。變異驗證：在記憶體中把 `todo.py:47` 的 `if due:` 換成 `if True:`，`test_render_without_due` 失敗（`'[ ] 2. 寫週報（到期 ）' != '[ ] 2. 寫週報'`），所以不是假綠燈。
- 相關失敗面：
  - 沒有 `due` 的待辦執行 render → 不帶括號；由 `test_render_without_due`、`test_render_marks_done` 覆蓋；通過。
  - 有 `due` 的待辦執行 render → 行尾「（到期 11/20）」；由 `test_render_shows_due` 覆蓋；通過。
  - 未完成且到期日早於今天／晚於今天／已完成／沒有到期日 → 只回傳第一種；由 `test_overdue` 覆蓋；通過。
  - ISO 字串比較日期 → 字串順序與日期順序一致；沿用上一份報告的結論。
- 需求、架構、安全、品質：完整範圍只改 `todo.py`、`test_due.py` 與 issue 文件，沒有安全面；CLI 沒有新增使用者入口，根目錄 README 不需要更新。沒有跨 Task 的重複實作或過度設計，`due_of` 是共用的小函式。
- 增量範圍各檔結論：
  - `test_due.py`：新增一個測試，不動正式程式與既有測試的前提；通過。
  - `docs/issues/issue-3601/implementation-plan.md`：新增 S3，證據「4 項全數通過」與重跑結果相符；通過。
  - `docs/issues/issue-3601/README.md`：只動記帳區段（`## 現況` 位於 `## 概述` 之後、`**核准 commit**` 改為祖先 15c547c、待確認事項 TBD-1、Timeline、`**狀態**`）；通過。
  - `docs/issues/issue-3601/review-e2ff4af.md`：新增上一份報告，之後沒有修改；通過。
- 增量覆審重新查核：測試結果（增量新增測試，在 HEAD 重跑全部測試）；SCN-001 覆蓋（受新測試影響，重新判定並做變異驗證）。
- 沿用的結論：`todo.py` 在 `e2ff4af..f427b78` 沒有差異，所以沿用 `render`、`overdue`、`due_of` 的正確性、ISO 字串比較、沒有安全面與共用 `due_of` 的結論；`test_overdue`、`test_render_shows_due` 沒有變動，結論沿用。
- 豁免、待確認與限制：無豁免；TBD-1 已解決（修正後覆審），本次覆審即完成該決定。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
