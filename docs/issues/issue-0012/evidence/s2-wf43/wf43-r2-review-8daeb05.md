# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：8daeb0591073097d5f28ecce51c8d6077729435e
- Reviewed patch-id：cb427972f3d07d91b917963525435ad1974369b7（`git diff 70f4ada 8daeb05 | git patch-id --stable` 的重算結果，與指定值一致）
- 獨立 reviewer：獨立 subagent
- 增量覆審：上一份報告 review-5bbeb0d.md，增量範圍 `5bbeb0d..8daeb05`，只為處理其 SHOULD FIX 1、NICE TO HAVE 1

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE 1（本輪增量新增）：位置在 `docs/issues/issue-3601/implementation-plan.md:11`（S3）。
  - 問題：證據只寫「`python3 -m unittest -v` 4 項全數通過」，缺兩樣東西。一是被測提交。二是這兩項變更的性質：`short_date` 是純重構，新測試是 characterization test，一開始就是綠燈，沒有紅燈。
  - 影響：verification.md「不改變可觀察行為的任務」要求記下重構前後跑同一組測試的結果，「證據重用」要求記下被測提交。這屬於證據持久力的問題，不影響本輪判定，因為本報告已在 8daeb05 重跑測試，也在 5bbeb0d 驗過重構前的行為（見下）。
  - 建議：之後的提交如果本來就要改 implementation-plan.md，可以順手補上「被測 8daeb05；short_date 是純重構，重構前後的 render 輸出相同；test_render_without_due 是 characterization test」。這個檔案屬於凍結內容，不值得只為這件事開一個提交讓 PASS 失效。

## 已查核維度
- 驗收與證據：
  - 增量覆審的前提都成立。5bbeb0d 是 HEAD 的祖先，`5bbeb0d..HEAD` 之間沒有 merge 提交。`git merge-base main HEAD` = 70f4ada，與上一份報告的 Reviewed BASE 相同。上一份報告記的是完整範圍，判 PASS。增量裡 7ef9a45 是保存報告的提交，8daeb05 是修正，沒有夾帶其他修改。
  - SHOULD FIX 1 已修好。`test_due.py:18-20` 新增 `test_render_without_due`，斷言 `render` 對沒有到期日的待辦輸出 `"[ ] 2. 寫週報"`，結尾不帶括號。期望值是獨立的字面值，不是同義反覆；render 誤加括號或「（到期 ）」時測試會失敗。在 5bbeb0d 的 `todo.py` 上，`render([{'id':2,'title':'寫週報','done':False}])` 回傳 `'[ ] 2. 寫週報'`，重構前行為相同，屬 characterization test，沒有紅燈是正常的。
  - NICE TO HAVE 1 已修好。`todo.py:37-39` 新增 `short_date(due)`，回傳 `due[5:].replace("-", "/")`；`todo.py:53` 改成呼叫 `short_date(due)`。運算式與原本行內寫法相同，行為等價。5bbeb0d 的 `render` 對 `due: 2026-11-20` 回傳 `'[ ] 1. 繳費（到期 11/20）'`，與 HEAD 上 `test_render_shows_due` 的期望值一致。
  - 規格：`git diff 576385f 8daeb05 -- docs/issues/issue-3601/README.md` 顯示 Gherkin 劇本沒有變動，核准有效。
  - 在新 HEAD 執行 `python3 -m unittest -v` 的輸出：
    ```
    test_overdue (test_due.DueTest.test_overdue) ... ok
    test_render_shows_due (test_due.DueTest.test_render_shows_due) ... ok
    test_render_without_due (test_due.DueTest.test_render_without_due) ... ok
    test_render_marks_done (test_todo.RenderTest.test_render_marks_done) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.000s

    OK
    ```
- 相關失敗面：
  - 受 `short_date` 抽出影響的地方：整個 HEAD 只有 `todo.py:53`（`render`）呼叫它；`main` 經由 `render` 間接使用，CLI 列出輸出不變。`overdue`、`due_of` 沒有改動、也不呼叫 `short_date`，上一份報告中 overdue 的結論沿用。
  - `short_date("")` 回傳空字串，但呼叫處有 `if due:` 擋住，沒有到期日的路徑碰不到它，這條路徑現由 `test_render_without_due` 覆蓋。
  - `test_todo.py` 的 `test_render_marks_done`（沒有 due 欄位）前提沒有改變，在 HEAD 上仍綠燈。
  - 根目錄 `README.md` 的使用說明「（到期 MM/DD）」與輸出格式一致，不需要更新。
- 需求、架構、安全、品質：
  - `todo.py`：純重構，加了 issue 標註的 docstring，沒有行為變更，沒有安全面。通過。
  - `test_due.py`：新增一個斷言獨立的測試，既有測試沒有被修改或弱化。通過。
  - `docs/issues/issue-3601/implementation-plan.md`：新增 S3 列，對到 SCN-001，證據命令可重現。通過，附 NICE TO HAVE 1。
  - `docs/issues/issue-3601/README.md`：增量變動都在記帳區段（7ef9a45 新增位於 `## 概述` 之後的 `## 現況` 與 Timeline 一列；8daeb05 新增 `## 待確認事項` TBD-1 與 `**狀態**` 值）。`**狀態**: 修正完成，待覆審` 是階段描述，開頭不是 `等待外部驗收窗`／`不修復`／`已完成`，不會讓 verify-artifact、dev-cycle 或懸置掃描判斷錯誤，不列問題。通過。
- 其餘沿用 review-5bbeb0d.md
- 豁免、待確認與限制：本輪沒有新增豁免、待確認事項或限制。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
