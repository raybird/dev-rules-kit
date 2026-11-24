# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：8daeb0591073097d5f28ecce51c8d6077729435e
- Reviewed patch-id：cb427972f3d07d91b917963525435ad1974369b7（`git diff 70f4ada 8daeb05 | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者）
- 增量覆審：上一份報告 review-5bbeb0d.md（PASS，H1=5bbeb0d）；增量範圍 `5bbeb0d..8daeb05`，只處理使用者選擇修正的 SHOULD FIX 1 與 NICE TO HAVE 1，外加記帳。前提成立：H1 是 HEAD 的祖先、增量內無 merge 提交、merge-base 仍為 70f4ada。

## 問題與風險
- MUST FIX：無（H1 上也沒有 MUST FIX 等級的問題）
- SHOULD FIX：無
- NICE TO HAVE 1：`docs/issues/issue-3601/README.md:52` TBD-1 的影響欄只寫 SCN-001，但 short_date 是重構，不改變可觀察的行為；可寫成「SCN-001（測試）；short_date 為重構、不影響驗收」。
- NICE TO HAVE 2：`docs/issues/issue-3601/implementation-plan.md:9` S1、S2 的證據寫了測試名稱，S3 沒寫；可補上 test_render_without_due，方便對照證據。

## 已查核維度
- 上一份報告建議的修正：
  - SHOULD FIX 1 已修好：`test_due.py:18-20` 新增 `test_render_without_due`，斷言沒有到期日時輸出完全等於 `[ ] 2. 寫週報`，不帶括號。
  - NICE TO HAVE 1 已修好：`todo.py:37-39` 新增 `short_date()`，`todo.py:53` 改為呼叫它；以 2026-11-20、2026-01-05、2026-12-31 實測，新舊寫法輸出相同，行為等價。
- 增量範圍內各檔：
  - todo.py、test_due.py：通過。
  - README.md：通過。`## 現況` 位在 `## 概述` 之後；TBD-1 的狀態值合法；`**狀態**` 是階段描述，不是特殊狀態值。
  - implementation-plan.md：通過。S3 證據「4 項全數通過」與實跑相符。
  - review-5bbeb0d.md：通過。7ef9a45 新增後未再修改。
- 受影響之處重新查核：
  - render 的呼叫者：`todo.py:64` 的 `main()`，以及 test_due.py、`test_todo.py:7-9` 的 render 測試。輸出格式不變，全部重跑通過。
  - short_date 的輸入前提：唯一呼叫點有 `if due:` 擋住空字串；非 ISO 輸入的行為與 H1 相同，不是增量引入的問題。
  - overdue／due_of：未改動，也不使用 short_date，上一份報告的結論沿用。
  - 根目錄 README.md：增量未改動，說明仍與 short_date 的輸出相符。
- 驗收與證據：在 HEAD 執行 `python3 -m unittest -v`，4 項 ok（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done），`Ran 4 tests`、`OK`。原本只是推論的「沒有到期日時 render 不加括號」，現在由 test_render_without_due 直接證明。
- 其餘沿用 review-5bbeb0d.md。
- 豁免、待確認與限制：本輪無新增。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
