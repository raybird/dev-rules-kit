# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：e88e38689ab9bf8aa763c40c8b7504d5735f88ed
- Reviewed HEAD SHA：b5437e371f9689275f61e388eae1da4159c5c27e
- Reviewed patch-id：d85a5ca35c69cbd95fd5e563a8482dbab81bf87d
- 獨立 reviewer：獨立 subagent（agent a900a6805d3f81ae7）
- Review artifact：docs/issues/issue-3601/review-b5437e3.md
- 增量覆審：上一份報告 review-775859c.md；增量範圍 775859c..b5437e3

## 問題與風險
- MUST FIX 1：SCN-002 的測試沒有照核准劇本寫，日期比較這個核心行為沒有任何測試擋住。
  - 劇本的 Given 是兩筆未完成待辦，到期日分別為 2026-11-01 與 2026-12-01。`test_due.py:11-14` 的 `test_overdue` 第二筆卻沒有到期日，劇本裡尚未到期的 2026-12-01 沒有出現在測試中。
  - 變異測試：把 `todo.py:39` 的條件改成 `not i["done"] and due_of(i)`，也就是拿掉 `< today`，`test_overdue` 仍然通過；用劇本的 Given 跑這個變異版本，會同時回傳 11-01 與 12-01 兩筆。
  - 正式程式目前的行為正確，缺的是驗收證據。上一份報告「SCN-002 由 test_overdue 覆蓋」的結論本次推翻。
  - 修法：加入到期日 2026-12-01 的未完成待辦，斷言只回傳 2026-11-01 那一筆，期望值用劇本原文的字面值；補完後重跑，並把命令與輸出寫進 implementation-plan.md。
- SHOULD FIX 1（需決策）：根目錄 `README.md` 的使用說明沒有更新。
  - project.md「常青文件更新責任」規定使用者功能要更新根目錄 `README.md` 的使用說明。完整範圍內沒有改動根目錄 README.md，但 `python3 todo.py` 的清單輸出已經會多出「（到期 MM/DD）」。上一份報告沒有查這一項。
  - 待決問題：CLI 沒有設定到期日的入口（`add` 不收 due），也沒有列出逾期的指令，要讓清單出現到期日只能手動編輯 `todo.json`。這樣算不算使用者功能？
  - 可選做法：
    - (a) 在使用說明補上清單會顯示到期日，以及 `todo.json` 的 `due` 欄位格式 YYYY-MM-DD。
    - (b) 判定本 issue 只交付函式層能力，不算使用者功能：在待確認事項記下理由，另開 issue 處理 CLI 入口與文件。
  - reviewer 建議：(a)，並另開後續 issue 處理 CLI 入口。
- NICE TO HAVE 1（需決策）：沒有驗證到期日格式。
  - `"11-20"` 會顯示「（到期 ）」，而且被判為逾期。
  - `"2026-9-1"` 早於今天，卻不算逾期。
  - `"2026/11/20"` 永遠不會被判為逾期。
  - 整數 `20261120` 會讓 render 拋出 TypeError。
  - 這些值目前只有手動編輯 `todo.json` 才會產生，核准範圍也沒有格式驗證，所以不阻擋。
  - reviewer 建議：留給 CLI 入口的後續 issue，在輸入端驗證。
- NICE TO HAVE 2：有兩個邊界沒有測試。
  - 已完成的待辦會被排除：拿掉 `not i["done"]` 後 `test_overdue` 仍然通過。
  - 到期日等於今天：把比較改成小於等於後 `test_overdue` 仍然通過。
  - 兩者都不在核准的 Gherkin 裡。docstring 寫的是「早於」，建議補測試固定這兩個邊界。
- NICE TO HAVE 3：implementation-plan.md 的證據欄只寫了「N 項全數通過」，沒有被測 commit，也沒有輸出。S3 只是替既有行為補測試，本來就不會有紅燈，計畫沒有寫明這個理由。

## 已查核維度
- 驗收與證據：
  - 在 HEAD b5437e3 執行 `python3 -B -m unittest -v`，4 項 ok（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done），輸出為 `Ran 4 tests` / `OK`。
  - SCN-001：`test_render_shows_due` 斷言與劇本字面值完全相等，成立。
  - SCN-002：不成立，見 MUST FIX 1。
- 上一份報告的 SHOULD FIX 1：已修好。
  - `test_render_without_due` 走的是 `due_of` 回傳空字串的路徑。
  - 「一律加括號」與「空字串也加括號」兩個變異都會讓它失敗，不是假綠燈。
- 相關失敗面：
  - 沒有到期日：render 不加括號，overdue 略過，有覆蓋。
  - 尚未到期：沒有覆蓋，見 MUST FIX 1。
  - 已完成、到期日等於今天：沒有覆蓋，見 NICE TO HAVE 2。
  - 格式不正確：見 NICE TO HAVE 1。
  - due 為 null：兩個函式都會略過，安全。
  - 合法的 YYYY-MM-DD：字串順序與日期順序一致，沿用上一份報告的結論。
- 需求、架構、安全、品質：
  - 改動侷限在 `todo.py` 的 `due_of`、`overdue`、`render`，舊資料向下相容，沒有安全面。
  - render 與 overdue 共用 `due_of`，沒有重複邏輯或過度設計。
  - 常青文件見 SHOULD FIX 1。
- 增量覆審：
  - 條件成立：H1 有持久化的 PASS 報告，而且是 HEAD 的祖先；中間沒有 merge 提交；merge-base 仍為 e88e386；流程契約 2.6。
  - 增量範圍內各檔案的結論：
    - review-775859c.md 為新增的歷史報告。
    - issue README 只動了記帳區段：`## 現況` 位在 `## 概述` 之後，另有 `## 待確認事項`、Timeline 與狀態；凍結章節未變。
    - implementation-plan.md 新增 S3，與 TBD-1 一致。
    - test_due.py 只新增一個測試。
    - 以上皆可接受。
  - 重新查核：render 沒有到期日的路徑，以及 test_due.py 整檔；在整檔中發現 MUST FIX 1，屬上一份報告的遺漏。
  - 沿用：todo.py 在增量範圍內沒有變動，沿用字串比較、安全與架構三項結論；test_todo.py 沒有變動，沿用。
- 豁免、待確認與限制：
  - 沒有 Gate 豁免，TBD-1 已解決。
  - 變異測試在記憶體中替換原始碼後執行，沒有修改 repo。

## 流程判定
RETURN TO execute-task

原因：MUST FIX 1，SCN-002 的必要驗收證據不成立。修正後，增量覆審條件仍成立時，可以從 b5437e3 做增量覆審。
