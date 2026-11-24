# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due），TARGET=main
- Reviewed BASE SHA：4f9778b64863723dbb7a6cdb756fb1783a5f1a93
- Reviewed HEAD SHA：412bb1925826d5caf1371898fdde33cab83db7a0
- Reviewed patch-id：7009e08f632df4e4cca2a2c2485a1283dd0a22ce（`git diff 4f9778b 412bb19 | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者，唯讀）
- Review artifact：本檔
- 增量覆審：上一份報告 review-d232d03.md（H1=d232d03，PASS，完整範圍）；增量範圍 `d232d03..412bb19`。條件：H1 是 HEAD 的祖先、中間無 merge、merge-base(main, HEAD) 仍為原 BASE 4f9778b

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE 1：`docs/issues/issue-3601/implementation-plan.md:11`（S3 列）證據只寫「4 項全數通過」，沒有實際輸出，也沒有重構前跑同一組測試的紀錄。依 verification.md「不改變可觀察行為的任務」，建議記重構前後同一組測試的命令與全綠輸出，並標明不改變可觀察行為。不阻塞：reviewer 已重現等價證據（見下）。

## 已查核維度
- 驗收與證據：HEAD 上 `python3 -m unittest -v` 輸出 `Ran 4 tests ... OK`（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 皆 ok）。SCN-001 由 `test_render_shows_due` 覆蓋（期望值為規格字面值「（到期 11/20）」），SCN-002 由 `test_overdue` 覆蓋。d232d03 的 `todo.py` 搭配 HEAD 的測試同樣 4 項全過，確認 `short_date` 抽取不改變行為。假綠燈檢查（行程內 monkeypatch，未改 repo）：讓沒有到期日的待辦也加後綴時 `test_render_without_due` 失敗；`short_date` 改回傳 `due[2:]` 時 `test_render_shows_due` 失敗。期望值皆為獨立字面值。
- 相關失敗面：
  - 沒有到期日：`{"id":2,"title":"寫週報","done":False}` → `[ ] 2. 寫週報`；`test_render_without_due`（新增）與 `test_render_marks_done` 覆蓋，通過。
  - `short_date` 轉換：`2026-11-20` → `11/20`；經 `render` 由 `test_render_shows_due` 覆蓋，通過。
  - `due` 為 None 或空字串：`if due:` 擋掉，不呼叫 `short_date`；實測輸出 `[ ] 1. a`，不影響結論。
  - 格式不對的 `due`（`2026-1-5`、`11/20`、含時間）：規格與 `due_of` 皆定義為 YYYY-MM-DD，CLI 無寫入 `due` 的途徑，且此運算式行為在 d232d03 已存在、重構未改變；不在本次範圍，若要驗證屬新需求。
- 需求、架構、安全、品質：增量未改核准行為，Gherkin 未變（核准 commit 4fe7314 有效）。`short_date` 僅 `todo.py:53` 一個呼叫點，一行實作為使用者選擇的建議，不算過度設計；`due_of`、`short_date`、`overdue` 間無重複邏輯。無新輸入或權限面。
- 增量覆審逐檔結論：
  - `todo.py`：新增 `short_date`（37–39 行）、`render` 改呼叫它（53 行）；純重構，NICE TO HAVE 1 已修。
  - `test_due.py`：新增 `test_render_without_due`（18–20 行）；有效測試，SHOULD FIX 1 已修。
  - `docs/issues/issue-3601/README.md`：`## 現況` 位於 `## 概述` 之後；TBD-1 結論、日期、影響欄格式正確；Timeline 與上一份報告一致。
  - `docs/issues/issue-3601/implementation-plan.md`：S3 列內容準確，證據形式見 NICE TO HAVE 1。
  - `docs/issues/issue-3601/review-d232d03.md`：上一份報告，內容一致。
- 重新查核的項目與理由：`render` 實作有改，其呼叫端 `main()`（`todo.py:64`）與三個 render 測試於 HEAD 重跑，皆通過。上一份 SHOULD FIX 1 的前提：`test_render_marks_done` 已間接覆蓋沒有到期日的情況，新測試把它明確化，不影響結論。根目錄 `README.md:10` 使用說明仍與輸出一致。
- 沿用的結論：`overdue`／`due_of` 以 ISO 字串比較、順序與日期一致；已完成與沒有到期日的待辦被 `overdue` 略過；安全面無。增量未改這些程式及其依賴的資料格式，`test_overdue` 本次亦重跑通過。
- 豁免、待確認與限制：豁免無；TBD-1 已解決；H1 patch-id 未計算（以 SHA 識別）。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
