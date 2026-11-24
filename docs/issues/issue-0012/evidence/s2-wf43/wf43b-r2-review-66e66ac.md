# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：66e66acba5afad7c4a898d449f569a2eba74b224
- Reviewed patch-id：a3c5b7783efae6348873bc66085c110d38dcaec3
- 獨立 reviewer：獨立 subagent
- 增量覆審：上一份報告 review-5bbeb0d.md，增量範圍 `5bbeb0d..66e66ac`，處理該報告的 SHOULD FIX 1、NICE TO HAVE 1

## 問題與風險
- MUST FIX 1（增量引入）：`todo.py:39` 的 `short_date()` 與原本的 `due[5:].replace("-", "/")` 不等價。新寫法對月、日各做 `lstrip("0")`，個位數的月或日不再補零。在新 HEAD 實測：
  - 2026-11-20：舊 `11/20`，新 `11/20`
  - 2026-11-05：舊 `11/05`，新 `11/5`
  - 2026-01-20：舊 `01/20`，新 `1/20`
  - 2026-01-01：舊 `01/01`，新 `1/1`
  - 2026-10-10：舊 `10/10`，新 `10/10`

  影響：
  - 列表輸出與根目錄 `README.md:10` 使用說明的「（到期 MM/DD）」不符，也與 `todo.py:38` docstring「轉成顯示用的 MM/DD」不符。
  - 上一份報告的建議只要求抽成 `short_date()`，是不改行為的重構；TBD-1 記載使用者選的也只是修正這兩項建議。不補零的輸出格式從未核准。
  - 提交標為 `refactor:`，`docs/issues/issue-3601/implementation-plan.md:11` S3 的證據只有「4 項全數通過」，沒有揭露行為變更。依 verification.md「不改變可觀察行為的任務」，重構中出現行為變更應退回。
  - 現有測試只用 11/20 這種兩位數日期，綠燈測不出差異。

  建議：
  - 讓 `short_date` 回到等價實作，例如 `return due[5:].replace("-", "/")`。
  - 補個位數月日的測試，期望值用已知字面值，例如 `short_date("2026-01-05") == "01/05"`，或 render 輸出含「（到期 01/05）」。
  - 更新 S3 的證據，記錄命令與輸出。
  - 若使用者其實想要不補零的 M/D，屬於新的需求邊界，需先核准並同步修改 SCN 與根 README，不在 TBD-1 的授權內；依現有核准範圍不需要使用者決策，所以本項不加 `需決策`。
- SHOULD FIX：無
- NICE TO HAVE：無

## 已查核維度
- 驗收與證據：SCN-001 仍由 `test_render_shows_due` 覆蓋並通過；SCN-002 不受增量影響，`test_overdue` 通過。在新 HEAD 重跑 `python3 -m unittest -v`：4 項（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done）全數 ok，`Ran 4 tests`、`OK`。綠燈真實，但沒有覆蓋 MUST FIX 1 的失敗面。
- 相關失敗面：
  - 到期日的月或日是個位數（例如 2026-01-05）：預期顯示 `01/05`；無測試覆蓋；實際 `1/5`，未通過（MUST FIX 1）。
  - 月日都是兩位數、不以 0 開頭（例如 2026-11-20、2026-10-10）：預期不變；`test_render_shows_due` 與手動實測；等價，通過。
  - 沒有到期日：預期 render 不加括號；新的 `test_render_without_due`（`test_due.py:18-20`，期望值為獨立字面值）；通過，SHOULD FIX 1 已修好。
- 需求、架構、安全、品質：`short_date` 在新 HEAD 只有一個呼叫端（`todo.py:53` render）；`overdue` 仍以 `due_of` 做 ISO 字串比較，不受影響；無安全面；增量引入未核准的可觀察行為變更（MUST FIX 1）。
- 增量範圍內各變動檔案：
  - `todo.py`：見 MUST FIX 1。
  - `test_due.py`：SHOULD FIX 1 已修好；缺少個位數月日的案例，列在 MUST FIX 1 的建議裡。
  - `docs/issues/issue-3601/implementation-plan.md`：S3 證據沒有揭露行為變更，隨 MUST FIX 1 修正。
  - `docs/issues/issue-3601/README.md`：`## 現況` 位在 `## 概述` 之後；TBD-1 已解決，有結論與日期；規格與核准紀錄未變，核准 commit 576385f 仍然有效；無問題。
  - `docs/issues/issue-3601/review-5bbeb0d.md`：7ef9a45 新增後未修改。
- 重新查核的項目與理由、沿用的結論：
  - 「沒有到期日時 render 不加括號」：增量補了測試，重新查核後成立。
  - 「render 與 overdue 共用 due_of」：render 的日期轉換改了，重新查核；due_of 與 overdue 未變，沿用。
  - 根目錄 `README.md:10` 的 MM/DD 說明：依賴輸出格式，重新查核後與新 HEAD 不一致（MUST FIX 1）。
  - `test_todo.py`：只測沒有到期日的項目，不受影響，沿用。
  - merge-base：`git merge-base main HEAD` 仍為 70f4ada，符合增量覆審條件。
- 其餘沿用 review-5bbeb0d.md
- 豁免、待確認與限制：無豁免；沒有新的待確認事項。

## 流程判定
RETURN TO execute-task
