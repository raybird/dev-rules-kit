# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：66e66acba5afad7c4a898d449f569a2eba74b224
- Reviewed patch-id：a3c5b7783efae6348873bc66085c110d38dcaec3
- 獨立 reviewer：獨立 subagent
- 增量覆審：上一份報告 review-5bbeb0d.md，增量範圍 5bbeb0d..66e66ac（處理該報告 SHOULD FIX 1、NICE TO HAVE 1）

## 問題與風險
- MUST FIX 1（增量引入，需決策）：todo.py:39 `short_date()` 以 `part.lstrip("0")` 去掉月、日的前導零，把原本 `due[5:].replace("-", "/")` 的零填補 MM/DD 改成不補零的 M/D。NICE TO HAVE 1 只要求抽出函式，implementation-plan.md:11（S3）寫的是「抽成」，提交標為 refactor，所以這一項應是不改變可觀察行為的重構。實際上 render 與 CLI `python3 todo.py` 的輸出已經改變：
  - 2026-01-05：H1 顯示「（到期 01/05）」，HEAD 顯示「（到期 1/5）」
  - 2026-11-01：11/01 變成 11/1
  - 2026-09-30：09/30 變成 9/30
  影響：新行為沒有核准來源；和根目錄 README.md:10「（到期 MM/DD）」與函式自己的 docstring todo.py:38「轉成顯示用的 MM/DD」衝突；S3 的證據記成重構，沒有行為變更應有的紅綠重構證據（verification.md「不改變可觀察行為的任務」：發現行為變更時退回）。現有測試只用 11/20（月、日都沒有前導零），所以這個改變沒有被抓到。
  - 待決問題：到期日顯示要維持補零的 MM/DD，還是改成不補零的 M/D？
  - 可選做法 A：維持 MM/DD。`short_date` 恢復原本的運算式（`due[5:].replace("-", "/")`），補一個含前導零的 characterization test（例如 2026-01-05 顯示「（到期 01/05）」，期望值用手寫字面值），S3 補純重構的前後同組測試證據。
  - 可選做法 B：改成 M/D。使用者明確核准新格式並記入 issue README；根 README.md:10 與 todo.py:38 的 docstring 同步改寫；補紅燈→綠燈的測試（例如 2026-01-05 顯示「（到期 1/5）」）；S3 改記為行為變更並附紅綠重構證據。
  - reviewer 建議：A。NICE TO HAVE 1 與使用者在 TBD-1 選的修正都只是重構，現行文件寫的也是 MM/DD。
- SHOULD FIX：無
- NICE TO HAVE：無

## 已查核維度
- 驗收與證據：
  - 在 HEAD 66e66ac（工作區乾淨）執行 `python3 -m unittest -v`，輸出 `Ran 4 tests ... OK`：test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 全部 ok。
  - merge-base(main, HEAD) = 70f4ada，與原報告的 BASE 相同。H1 是 HEAD 的祖先，中間沒有改寫歷史，符合增量覆審的條件。
  - SCN-001（11/20）在 HEAD 仍成立。issue README 的 Gherkin 區塊與核准紀錄在增量範圍內沒有改動，核准 commit 576385f 維持有效。
- 相關失敗面：
  - 月或日有前導零：以 01-05、11-01、09-30、10-01、01-01 實際比較 H1 與 HEAD 的 render 輸出，全部不同（H1 補零，HEAD 不補零）。測試沒有覆蓋，判定 MUST FIX 1。
  - 月、日都沒有前導零：11-20、10-10、12-31 的輸出相同。
  - 沒有到期日：HEAD 輸出「[ ] 2. 寫週報」，不帶括號，由新增的 test_render_without_due 覆蓋，判定通過。
- 需求、架構、安全、品質：沒有安全面。`short_date` 只有 render 一個呼叫端；CLI `main()` 透過 render 輸出，所以使用者可見的 CLI 輸出受影響，見 MUST FIX 1。
- 上一份報告建議的逐項確認：
  - SHOULD FIX 1：已修好。test_due.py:18-20 新增沒有到期日的 render 測試，期望值為獨立的字面值，不是同義反覆。
  - NICE TO HAVE 1：函式已抽出（todo.py:37-39），但抽出時改變了行為，沒有達成「純抽出」，見 MUST FIX 1。
- 增量範圍內每個變動檔案的結論：
  - todo.py：MUST FIX 1。
  - test_due.py：新測試正確；缺少含前導零的案例，屬於 MUST FIX 1 的修正內容。
  - implementation-plan.md：S3 把行為變更記成重構，證據只有「4 項全數通過」，修正 MUST FIX 1 時一併更正。
  - docs/issues/issue-3601/README.md：`## 現況` 位在 `## 概述` 之後，`**現行 review**` 正確；TBD-1、Timeline、`**狀態**` 寫法沒有問題。保存本報告時把 `**現行 review**` 改成 review-66e66ac.md。
- 增量覆審：
  - 重新查核了 render 的輸出（short_date 唯一的呼叫端）、CLI 列出、根 README 使用說明（README.md:10）、SCN-001、上一份報告「render 不加括號」的結論，理由都是 render 改呼叫 short_date。
  - 沿用：overdue 與 SCN-002 不經過 short_date，仍使用 due_of 的 ISO 字串比較，不受影響；test_todo 的 render_marks_done 不含到期日，不受影響。
- 其餘沿用 review-5bbeb0d.md
- 豁免、待確認與限制：MUST FIX 1 標為需決策，待使用者回答後記入 issue README `## 待確認事項`。日期格式本身是否合法（例如 00 月）不在本輪範圍。

## 流程判定
RETURN TO execute-task
