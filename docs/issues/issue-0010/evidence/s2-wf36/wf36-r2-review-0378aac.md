# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：e88e38689ab9bf8aa763c40c8b7504d5735f88ed
- Reviewed HEAD SHA：0378aac90027ff846f304fe50f84fac1f79a0e9d
- Reviewed patch-id：82f276454d789477ff1bd5b2ae49b3a43d197cb2（`git diff BASE HEAD | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者）
- Review artifact：本檔
- 增量覆審：上一份報告 [review-775859c.md](review-775859c.md)（H1 = 775859c，PASS）；增量範圍 `775859c..0378aac`。適用條件：流程契約 2.6；H1 是 HEAD 的祖先，中間沒有 merge 提交也沒有改寫歷史；`git merge-base main HEAD` 仍是原 BASE e88e386

## 問題與風險
- MUST FIX 1：`todo.py:40` 的 `overdue` 仍寫 `due_of(i) < today`，但 `due_of`（`todo.py:32-35`）現在回傳 MM/DD（如 `"11/01"`），`today` 卻是 YYYY-MM-DD（`"2026-11-19"`）。字串比較時 `"1x/.."` 一定小於 `"2..."`，所以每筆有到期日的未完成待辦都會被判成逾期。SCN-002 在 HEAD 失敗：輸入 2026-11-01 與 2026-12-01，實際回傳 `[1, 2]`，規格要求 `[1]`。H1 版本回傳 `[1]`。建議：顯示和比較各用自己的值。`overdue` 改比較原始 ISO 日期（例如拆出一個取 ISO 日期的函式），MM/DD 格式化留給顯示用的函式，`render` 不做格式化邏輯，這樣仍符合 SHOULD FIX 1 的意圖。
- MUST FIX 2：`test_due.py:11-14` 的 `test_overdue` 跟 SCN-002 不一致。測試放的是「一筆 2026-11-01，加一筆沒有到期日」，不是規格的「2026-11-01 與 2026-12-01」，所以抓不到上面的回歸，HEAD 仍是 3/3 OK。implementation-plan.md S3 把「3 項全數通過」當作 SCN-002 仍成立的證據，構成假綠燈。建議：照 SCN-002 原文加入未來到期（2026-12-01）的未完成待辦，斷言只回傳 `[1]`。
- SHOULD FIX：無
- NICE TO HAVE 1：在 `test_due.py` 補跨年、尚未到期的反例（due 2027-01-05、today 2026-11-19，預期不是逾期），擋住只比月日的實作。HEAD 目前回傳 `[3]`。

不需要使用者決定需求邊界，沒有 `需決策` 項目。

## 已查核維度
- 驗收與證據：
  - SCN-001 由 `test_render_shows_due` 覆蓋，HEAD 通過。
  - SCN-002 在 HEAD 不成立。`test_overdue` 跟規格不一致，所以 `python3 -m unittest -v` 3/3 OK 不能當作 SCN-002 的證據（MUST FIX 1、2）。
- 相關失敗面：

  | 失敗面 | 輸入 | 預期 | HEAD 實際 | 覆蓋 | 判定 |
  |---|---|---|---|---|---|
  | SCN-002 原文 | today 2026-11-19；未完成，due 2026-11-01、2026-12-01 | `[1]` | `[1, 2]` | 無 | 失敗 |
  | 跨年、尚未到期 | due 2027-01-05、today 2026-11-19 | `[]` | `[3]` | 無 | 失敗（同 MUST FIX 1） |
  | SCN-001 顯示 | due 2026-11-20 | `[ ] 1. 繳費（到期 11/20）` | 相同 | test_render_shows_due | 通過 |
  | 沒有到期日 | 沒有 `due` 欄位 | render 不加括號，overdue 略過 | 符合 | test_todo、test_overdue | 通過 |
  | 已完成且過期 | done=True、due 2026-11-01 | overdue 略過 | `[]` | 無直接測試，實跑驗證 | 通過 |
- 需求、架構、安全、品質：改動仍只在 todo.py 與 test_due.py，沒有新增輸入面、權限或 I/O。顯示格式和比較用的格式共用同一個函式，造成行為分歧（MUST FIX 1）。
- 增量覆審：
  - 各變動檔案：
    - todo.py：SHOULD FIX 1 的目標已達成，`render`（`todo.py:47-49`）不再切字串，但連帶弄壞 `overdue`，判不通過。
    - README.md：只改到記帳區段，`## 現況` 位在 `## 概述` 之後，Gherkin 與核准 commit 未變。
    - implementation-plan.md：S3 的證據不實（MUST FIX 2）。
    - review-775859c.md：上一份報告，保留作歷史。
  - 重新查核：
    - `overdue`：依賴 `due_of` 的回傳格式，實跑後確認壞了。
    - `render`：直接呼叫 `due_of`，重新查核後正常。
    - `main` 與 test_todo.py：只經 `render` 用到，或資料沒有 `due`，不受影響。
    - test_due.py：前提變了，重新評估後發現跟規格不一致。
    - 全 repo 搜尋：沒有其他呼叫點。
  - 沿用：上一份報告的「需求、架構、安全」結論沿用。上一份報告「overdue 以 ISO 字串比較，順序與日期一致」的結論不沿用，已被推翻。
- 實跑（HEAD 0378aac）：`python3 -B -m unittest -v` → 3 tests OK。以 SCN-002 的輸入呼叫 `todo.overdue` → `[1, 2]`；用 `git show 775859c:todo.py` 取出 H1 版本，同樣輸入 → `[1]`。協調者在 HEAD 獨立重現了 `[1, 2]`。
- 豁免、待確認與限制：沒有 Gate 豁免。TBD-1 已解決（使用者選擇修正後覆審），維持原狀。

## 流程判定
RETURN TO execute-task
