# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：e88e38689ab9bf8aa763c40c8b7504d5735f88ed
- Reviewed HEAD SHA：b5437e371f9689275f61e388eae1da4159c5c27e
- Reviewed patch-id：d85a5ca35c69cbd95fd5e563a8482dbab81bf87d
- 獨立 reviewer：獨立 subagent
- Review artifact：docs/issues/issue-3601/review-b5437e3.md
- 增量覆審：上一份報告 review-775859c.md；增量範圍 `775859c..b5437e3`

增量覆審前提查核（review-evidence.md「增量覆審」，流程契約 2.6）：H1 775859c 有持久化報告（PASS），H1 是 HEAD 的祖先，中間只有 275c7c4 與 b5437e3 兩個非 merge 提交，沒有改寫歷史；`git merge-base main HEAD` = e88e386 = 上一份報告的 Reviewed BASE；本報告由協調者另行指派的 reviewer 撰寫。三項都成立，所以採增量覆審。HEAD、merge-base、patch-id 都已自行重算，與協調者提供的一致；工作區乾淨（只有被忽略的 __pycache__）。

## 問題與風險

- MUST FIX 1：SCN-002 的驗收測試沒照核准的 Given 寫，測不出「未到期的不算逾期」。
  - 位置：test_due.py 第 10–14 行 `test_overdue`。
  - 落差：README 第 30–34 行 SCN-002 的 Given 是「未完成的待辦到期日分別為 2026-11-01 與 2026-12-01」，Then 是「只回傳 2026-11-01 那一筆」。測試的第二筆（第 12 行）沒有 due 欄位，不是 2026-12-01。
  - 影響：測試只驗到「沒到期日的略過」，沒驗到 SCN-002 的核心「未來到期日不回傳」。在複本中把 todo.py 第 39 行的 `due_of(i) and due_of(i) < today` 改成只剩 `due_of(i)`（完全不跟今天比較），4 項測試仍全數 OK（exit 0）。所以 SCN-002 等於沒有能擋缺陷的證據，屬於必要驗收覆蓋缺口。
  - 建議：照 Given 把第二筆改成（或加一筆）`"due": "2026-12-01"` 的未完成待辦，期望值維持 `[1]`。修正後先在上述變異下確認會紅燈，再於原實作確認綠燈，證據記入 implementation-plan.md。
- SHOULD FIX 1：`overdue` 略過已完成待辦，這個失敗面沒有測試。
  - 位置：todo.py 第 39 行 `not i["done"]`；test_due.py 沒有對應案例。
  - 影響：上一份報告「相關失敗面」寫了「已完成的待辦——overdue 略過」，但那只是讀程式的結論，沒有測試覆蓋。在複本刪掉 `not i["done"] and`，4 項測試仍全數 OK。SCN-002 的 Given 寫「未完成的待辦」、概述寫「列出逾期的未完成待辦」，這是需求的一部分。
  - 建議：補一筆 `done: True` 且到期日早於今天的待辦，斷言不在回傳結果中；可以和 MUST FIX 1 一起修。
- SHOULD FIX 2：S1–S3 的證據紀錄不完整。
  - 位置：implementation-plan.md 第 9–11 行。
  - 影響：只記「3 項／4 項全數通過」，沒有 verification.md 要求的紅綠重構證據（四段各自的命令、結果與原因），也沒記被測版本。S3 只新增測試、不改變行為，應依「不改變可觀察行為的任務」記等價證據並標明。目前測試可重現，本次也已重跑（見下），所以不判定不實回報。
  - 建議：修 MUST FIX 1 時一併補齊證據紀錄。
- SHOULD FIX 3 `需決策`：使用者功能沒有 CLI 入口，常青文件也未更新。
  - 位置：todo.py 第 18–21 行 `add` 與 `main`（約第 53 行起）；根目錄 README.md 第 5–9 行「使用說明」。
  - 現況：README 概述是「待辦可以帶到期日：清單顯示月/日，並能列出逾期的未完成待辦」。但 CLI 沒辦法設定到期日（`add` 只收標題），也沒有列出逾期的子命令（`overdue` 只是函式），使用者只能手改 todo.json 才看得到到期日。project.md「常青文件更新責任」規定使用者功能要更新根目錄 README.md 的使用說明，本分支沒有更新。
  - 待決問題：本 issue 的交付範圍是否只到函式層（Gherkin 目前寫「執行 render」「呼叫 overdue」，是綁內部函式的寫法）？
  - 可選做法：
    - (a) 範圍維持函式層：在 README 待確認事項記「不影響本次交付」並寫明去向（另開 issue 補 CLI），根目錄 README 等 CLI 入口完成時再更新。
    - (b) 擴大範圍：新增 CLI 設定到期日與列出逾期，修訂 Gherkin 並重新核准，再更新根目錄 README 使用說明。
    - (c) 範圍不變，只在根目錄 README 補一行：清單會顯示 todo.json 裡的 due 欄位。
  - reviewer 建議：(a)。核准規格只涵蓋 render／overdue 行為，擴大範圍需要重新核准；(c) 會把需要手改資料檔的用法寫成正式使用說明，不建議。
- NICE TO HAVE 1：「到期日等於今天」的邊界沒有測試。todo.py 第 39 行用 `<`（今天到期不算逾期），和 docstring「早於 today」一致；但把它改成 `<=`，測試仍全綠。規格沒有定義這個邊界，可以補一個今天到期、不回傳的案例來固定行為。
- NICE TO HAVE 2：todo.py 第 48 行 `due[5:]` 與第 39 行的字串比較，都假設 due 一定是 YYYY-MM-DD 格式，格式錯了不會報錯。規格沒有涵蓋，目前資料只能手改 todo.json，風險低。

## 已查核維度

- 驗收與證據：
  - 在 HEAD b5437e3 自行執行 `python3 -m unittest -v`：Ran 4 tests，OK（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 全部 ok）。
  - SCN-001：由 test_render_shows_due 覆蓋（字面期望值「[ ] 1. 繳費（到期 11/20）」，來源是規格原文，不是同義反覆），有效。
  - SCN-002：test_overdue 的資料和 Given 不一致，證據不足以擋住核心缺陷，見 MUST FIX 1。
  - 核准規格查核：`git diff 15c547c HEAD -- docs/issues/issue-3601/README.md` 只動到記帳內容：新增 `## 現況`（位在 `## 概述` 之後，位置正確）、`**核准 commit**` 由「待提交」回填為 15c547c（是被審查 HEAD 的祖先）、新增 `## 待確認事項` 的 TBD-1、Timeline 加一列、`**狀態**` 改值。Gherkin 劇本與核准紀錄的其他內容未改，原核准有效。
- 相關失敗面：在 scratchpad 複本裡對 HEAD 的 todo.py 做變異，分別搭配 775859c 與 b5437e3 兩個版本的測試執行：
  - render 一律加到期後綴（拿掉第 47 行的 `if due`）：用舊測試時 test_render_marks_done 失敗，用新測試時 test_render_without_due 也失敗。有覆蓋。
  - overdue 不跟今天比較：兩版測試都全綠。沒覆蓋，見 MUST FIX 1。
  - overdue 不排除已完成：兩版測試都全綠。沒覆蓋，見 SHOULD FIX 1。
  - `<` 改成 `<=`：兩版測試都全綠。規格未定義，見 NICE TO HAVE 1。
  - 沒有到期日的待辦：render 不加括號（test_render_without_due 與 test_render_marks_done 都會擋）；overdue 略過（test_overdue 第 12 行會擋，`due_of` 回傳空字串）。有覆蓋。
- 需求、架構、安全、品質（含跨 Task 重複與過度設計）：
  - 程式只改了 todo.py 和測試檔，沒有新相依、I/O 或權限變化，也沒有安全面。
  - `due_of` 有 render 與 overdue 兩個呼叫端，不算只用一次的抽象。
  - S3 是 S1 的補測試，沒有重複實作，也沒有過度設計。
  - 常青文件責任與 CLI 入口的缺口見 SHOULD FIX 3。
- 增量覆審：
  - 增量內各檔結論：
    - test_due.py（b5437e3，第 16–18 行新增 test_render_without_due）：期望值「[ ] 2. 寫週報」是人工寫出的字面值，和實作不同源，不是同義反覆。缺陷存在時（後綴不再受 `if due` 控制）它會失敗，已用變異驗證。SHOULD FIX 1（上一份報告）已修好。但這個缺陷 test_render_marks_done 本來就擋得住，新測試的價值主要在把 SCN-001 的無到期日情境明確標出來。
    - docs/issues/issue-3601/review-775859c.md（275c7c4 新增）：上一份報告的原文，新增後沒有再修改，內容和協調者描述的一致。
    - docs/issues/issue-3601/README.md（275c7c4、b5437e3）：只改 `## 現況`、`## 待確認事項`、Timeline 與 `**狀態**`，都是記帳區段，Gherkin 未變。`**狀態**` 為「修正完成，待覆審」，與事實相符。
    - docs/issues/issue-3601/implementation-plan.md（b5437e3，第 11 行新增 S3）：任務與 SCN-001 對應正確；證據紀錄不完整，見 SHOULD FIX 2。
  - 重新查核：
    - SCN-002 的證據與「相關失敗面」：增量沒有改到 todo.py，但協調者要求檢查整個 BASE..HEAD 有沒有漏看的地方。用變異測試確認，上一份報告寫成已覆蓋的「overdue 以日期比較」與「已完成略過」其實沒有測試擋，所以推翻上一份報告的這部分結論。
    - 常青文件責任：上一份報告沒有查核，本次補查。
    - 核准規格是否在 15c547c 之後被修改：本次補查，結論是未修改。
  - 沿用：todo.py 在增量內沒有變動，上一份報告「改動侷限於 todo.py 與測試檔、無安全面、render 與 overdue 共用 due_of」的結論已在 HEAD 重新確認後沿用；「due_of 回傳 YYYY-MM-DD 時字串順序與日期順序一致」的推論沿用，格式假設見 NICE TO HAVE 2。
- 豁免、待確認與限制：README 沒有 Gate 豁免紀錄。TBD-1 已解決（使用者 2026-11-18 選「修正後覆審」），本次已確認修正完成。SHOULD FIX 3 需要使用者決定，協調者依 acceptance.md「逐題確認」詢問，結論記入 README `## 待確認事項`。限制：變異測試只在 scratchpad 複本執行，repo 內檔案沒有修改。

## 流程判定
RETURN TO execute-task
