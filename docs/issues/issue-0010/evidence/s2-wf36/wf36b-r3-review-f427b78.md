# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：e88e38689ab9bf8aa763c40c8b7504d5735f88ed
- Reviewed HEAD SHA：f427b78a40bafe10ac2f13f55008bd75935826c5
- Reviewed patch-id：f6f5526eda46ed191d92bbe6b962a2b864b35d37
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-3601/review-f427b78.md
- 增量覆審：上一份報告 review-e2ff4af.md；增量範圍 `e2ff4af..f427b78`

## 問題與風險
- MUST FIX：無
- SHOULD FIX 1（需決策）：問題在 `todo.py:18`（`add` 只收標題）與 `todo.py:53`（`main` 沒有列出逾期的入口）。到期日目前沒有使用者入口：`add` 不能帶到期日，`overdue` 只是函式，沒有 CLI 子命令能呼叫。使用者要讓待辦帶到期日，只能手動編輯 `todo.json`，也沒辦法從 CLI 列出逾期待辦。根目錄 `README.md` 的使用說明也沒更新；project.md 規定使用者功能要寫進這份文件。已核准的 SCN-001／SCN-002 只寫到 render 與呼叫 overdue 這一層，所以這不算違反核准範圍。但 README 概述寫的是「待辦可以帶到期日……並能列出逾期的未完成待辦」，和實際能做的事有落差。
  - 待決問題：本 issue 要不要包含 CLI 入口與使用說明。
  - 可選做法：(a) 維持現有範圍，只在 README 概述或待確認事項寫明「CLI 入口另開 issue」；(b) 擴大本 issue，加上 `add` 帶到期日、列出逾期的子命令與使用說明，並新增 Scenario 送核准。
  - reviewer 建議：(a)，另開 issue 處理 CLI 入口，避免沒核准的行為混進本次交付。
- SHOULD FIX 2：`docs/issues/issue-3601/implementation-plan.md:9-11` 的證據不完整。S1、S2 只寫了「3 項全數通過」，沒有 verification.md 要求的紅綠重構證據（紅燈命令、失敗原因、exit code）。S3 只新增測試、沒改產品行為，但沒有標成「不改變可觀察行為」，也沒說明為什麼沒有紅燈。這是證據記錄的問題，不阻擋本次判定，因為 reviewer 已獨立重現：
  - 在 BASE 的 `todo.py` 上，`render` 對有到期日的待辦輸出 `'[ ] 1. 繳費'`，不帶到期日，而且沒有 `overdue`。所以 `test_render_shows_due` 與 `test_overdue` 在 BASE 確實會紅燈。
  - 在 HEAD 兩項都綠燈。
  - 建議把紅燈證據與 S3 的不改變行為理由補進計畫。
- NICE TO HAVE 1：`todo.py:32-39`、`todo.py:48` 都假設 `due` 一定是 `YYYY-MM-DD` 字串，沒有任何檢查。例如手動寫成 `"11-20"` 時，render 會輸出 `（到期 ）`；寫成非 ISO 格式時，`overdue` 的字串比較會出錯。目前資料只能手動編輯 JSON 寫入，風險低。之後加 CLI 入口時，建議在寫入端驗證格式。
- NICE TO HAVE 2：`test_due.py:18-20` 的新測試和既有的 `test_todo.py:7-9` 重疊。`test_render_marks_done` 已經對沒有到期日的待辦斷言了完整輸出，所以「沒有到期日」這條路徑原本就有保護。新測試的價值是把這個案例明確對應到 issue-3601，保留無妨，不需要改。

## 已查核維度
- 驗收與證據：
  - 核准基線：核准 commit 是 15c547c。`git diff 15c547c f427b78 -- docs/issues/issue-3601/README.md` 只改了記帳區段（`## 現況`、`## 待確認事項`、Timeline、`**核准 commit**`、`**狀態**`），Gherkin 沒變，核准仍有效。
  - SCN-001 由 `test_render_shows_due` 覆蓋，期望值是字面值 `"[ ] 1. 繳費（到期 11/20）"`，和規格原文一致。另有 `test_render_without_due` 補充覆蓋。
  - SCN-002 由 `test_overdue` 覆蓋，用規格裡的資料（2026-11-01、2026-12-01，today 2026-11-19），斷言只回傳 id 1。
  - 在 HEAD、乾淨工作區重跑 `python3 -m unittest -v`，輸出如下：
    ```
    test_overdue (test_due.DueTest.test_overdue) ... ok
    test_render_shows_due (test_due.DueTest.test_render_shows_due) ... ok
    test_render_without_due (test_due.DueTest.test_render_without_due) ... ok
    test_render_marks_done (test_todo.RenderTest.test_render_marks_done) ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.000s

    OK
    ```
  - 三個斷言都用獨立的字面值，不是重算實作，沒有同義反覆或 mock。
- 相關失敗面：
  - 沒有到期日的待辦：`due_of` 回傳 `""`，render 不加括號（`test_render_without_due` 與 `test_render_marks_done` 都覆蓋），overdue 略過（`test_overdue` 的 id 4 覆蓋）。
  - 已完成的待辦：overdue 略過（id 3 覆蓋）。
  - 到期日剛好等於 today：用 `<` 比較，不算逾期，符合「早於 today」的定義。reviewer 在記憶體中執行 `overdue([{due:"2026-11-19"}], "2026-11-19")` 得到 `[]`。
  - 空字串到期日：`due_of(i) and ...` 會短路，不算逾期。
  - 日期比較：ISO 字串的排序與日期排序一致。
  - 格式不合法的到期日：沒有防護，見 NICE TO HAVE 1。
- 需求、架構、安全、品質（含跨 Task 重複與過度設計）：
  - 產品變更集中在 `todo.py` 的三個函式，`render` 與 `overdue` 共用 `due_of`，沒有重複邏輯，也沒有過度設計。
  - 沒有新增 I/O、外部輸入解析或權限面，沒有安全問題。
  - S3 和既有測試的重疊見 NICE TO HAVE 2。
  - 需求邊界的落差（缺 CLI 入口與常青文件）見 SHOULD FIX 1。
- 增量覆審：
  - 增量條件成立：H1 = e2ff4af 有持久化報告（PASS），是 HEAD 的祖先，中間 5f3a181、f427b78 都是單一 parent 的非 merge 提交，沒有改寫歷史；`git merge-base main HEAD` 仍是 e88e386，和上一份報告的 BASE 相同；流程契約是 2.6。
  - 各變動檔案的結論：
    - `test_due.py`（M）：新增 `test_render_without_due`，斷言 `todo.render([{"id":2,"title":"寫週報","done":False}]) == "[ ] 2. 寫週報"`。reviewer 在記憶體中用變異體驗證：拿掉 `if due:` 後輸出變成 `'[ ] 2. 寫週報（到期 ）'`，測試會失敗，所以這是會失敗的真測試。上一份報告的 SHOULD FIX 1 已確認修好。這個行為在 BASE 也成立（BASE 的 render 對同樣輸入輸出相同字串），所以它是特徵化與回歸測試，沒有紅燈是合理的。
    - `docs/issues/issue-3601/review-e2ff4af.md`（A）：新增上一份報告，內容沒有再修改。
    - `docs/issues/issue-3601/README.md`（M）：只改記帳區段。`## 現況` 位在 `## 概述` 之後；TBD-1 記下使用者的決定「修正後覆審」；Timeline 和 `**狀態**` 已更新；Gherkin 與其他凍結內容沒變。`**現行 review**` 還指向 review-e2ff4af.md，保存本報告的提交要改成 review-f427b78.md。
    - `docs/issues/issue-3601/implementation-plan.md`（M）：新增 S3 一列，對應 SCN-001，「4 項全數通過」和重跑的結果一致。證據寫得太簡略，見 SHOULD FIX 2。
  - 重新查核的項目與理由：增量範圍沒有改 `todo.py` 或任何產品程式碼，也沒有改資料格式或設定，所以上一份報告對 `render`／`overdue`／`due_of` 行為的結論不受影響。增量只新增測試，既有測試的前提沒變。不過驗收結論要對應新 HEAD，所以在 HEAD 重跑了全部測試（輸出見上），並重新核對了核准基線與 SCN-001／SCN-002 的對應。
  - 沿用的結論：上一份報告的失敗面分析（沒有到期日、已完成、ISO 字串比較）以及「沒有安全問題、共用 `due_of`」的結論，確認不受影響，沿用；也在 HEAD 程式碼上複核過，結果一致。
- 豁免、待確認與限制：
  - 沒有 Gate 豁免；TBD-1 已解決。
  - SHOULD FIX 1 需要使用者決定。
  - 上一份報告的 patch-id 寫成「不適用」，本報告已補上完整範圍的 patch-id。
  - 本次為唯讀審查，沒有寫入任何檔案；在 BASE 上的紅燈重現與變異體驗證都是在記憶體中執行，沒有更動工作區。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
