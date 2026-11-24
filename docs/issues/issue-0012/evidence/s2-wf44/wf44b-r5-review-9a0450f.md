# 審查報告
- 範圍：完整交付範圍（TARGET `main`）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：9a0450fcabb8640cbf8fcfa121fdb86539782b7a
- Reviewed patch-id：546a3a5ec083f72d01410fb705562fd6d1525803
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId a070f626d47752000），非原實作者；協調者複核行號、核准基線推導與邊界變異測試

## 問題與風險

### MUST FIX

- **M1. SCN-002 未核准就實作並送審** `需決策`
  - 位置：`docs/issues/issue-3601/README.md:41`（SCN-002 狀態「待核准」）、`docs/issues/issue-3601/README.md:52`（TBD-2「待確認」）；實作 `todo.py:37-39`，測試 `test_due.py:11-16`。
  - 影響：acceptance.md「分批核准」只允許實作已核准的 Task，PR 前所有現存 Scenario 須已核准或逐項豁免。狀態只讀核准表，2026-11-16 的「核准」與 Timeline「建立並核准」都不能替 SCN-002 補核准。TBD-2 問的正是逾期分界；`due_of(i) < today` 等於自行選了「當天不算逾期」。把 `<` 改成 `<=` 後測試仍全綠（協調者已重現），邊界未被測到。
  - 待決問題：(1) SCN-002 是否核准？(2) 逾期以今天還是明天為界？
  - 可選做法：
    - (a) 取得 SCN-002 核准與 TBD-2 答案；README 更新核准表、TBD-2 結論與日期。Scenario 若補邊界例子則重新核准並覆寫核准 commit。實作端補「到期日等於今天」的邊界測試，並記紅綠證據。
    - (b) 本次只交付 SCN-001，移除 `overdue` 與 `test_overdue`，SCN-002 另開 issue 追蹤。
  - reviewer 建議：(a)，改動小，邊界測試本來就該有。

### SHOULD FIX

- **S1. 使用者端沒有入口** `需決策`
  - 位置：`todo.py:53-59`（`main` 沒有 overdue 子命令，`add` 也不能設定 due）；`docs/issues/issue-3601/README.md:5` 寫「能列出逾期」；根目錄 `README.md:10` 只說明顯示格式。
  - 影響：使用者只能手改 `todo.json` 才能設定到期日，也無法從 CLI 列出逾期。
  - 待決問題：本 issue 範圍是否包含 CLI 入口（例如 `add --due`、`overdue` 子命令）？
  - 可選做法：(a) 維持函式層級，在概述與根目錄 README 寫明 due 目前需手動寫入；(b) 另開 issue 做 CLI 入口，並記入待確認事項。
  - reviewer 建議：(b)，本次至少讓概述不暗示使用者已可直接使用。
- **S2. Gherkin 綁內部函式**：`docs/issues/issue-3601/README.md:23`、`:29`（「執行 render」「呼叫 overdue」）。acceptance.md 要求 Scenario 描述外部行為；S2 的單迴圈合併理由（`docs/issues/issue-3601/implementation-plan.md:10`）就建立在這個寫法上，結果沒有任何 CLI 層驗收。建議處理 M1 需修訂 Scenario 時一併改成可觀察寫法，一次重新核准。
- **S3. TBD-1 欄位放錯**（格式）：`docs/issues/issue-3601/README.md:51`。結論寫在影響欄，狀態欄只有日期。建議狀態欄改為「已解決：2026-11-16，使用者選不顯示，維持原輸出」，影響欄寫「決定無到期日時的輸出；SCN-001」。狀態以「已解決」開頭，工具判定不受影響。
- **S4. Timeline 記了非語意事件**：`docs/issues/issue-3601/README.md:58-60`。「完成 S1／S2」是任務進度，Timeline 只記建立、核准、規格修訂；「建立並核准」也與 SCN-002 未核准矛盾。建議刪除兩列「完成」，首列改為「建立；SCN-001 核准」。
- **S5. 概述寫了進度**：`docs/issues/issue-3601/README.md:5`。「目前 S1、S2 都已完成，測試全數通過，等待審查」屬進度，應只記在 `**狀態**` 與任務清單。建議刪除這句。

### NICE TO HAVE

- **N1. due 格式異常會靜默出錯**（`todo.py:39`、`todo.py:48`）：`"11-20"`、`"  "` 顯示成「（到期 ）」；`"2026/11/01"` 在 today 為 `"2026-11-19"` 時不算逾期（`/` 的字元序大於 `-`）。目前沒有寫入路徑，風險低；日後加 CLI 入口時再驗證格式，或改用 `date.fromisoformat` 比較。
- **N2. 已完成項目也顯示到期日**（`todo.py:46-48`）：輸出如 `[x] 1. t（到期 11/20）`。Gherkin 只描述未完成項目，這是推導出的行為，可順便確認或補測試。
- **N3. 小精簡**：`overdue` 呼叫兩次 `due_of(i)`（`todo.py:39`）；docstring 的「issue-3601：」標籤（`todo.py:33`、`todo.py:38`）交給 Git 即可。
- **N4. 涉及檔案寫得籠統**：`docs/issues/issue-3601/README.md:13`「對應的測試檔」可改成明列 `test_due.py` 與根目錄 `README.md`。
- **N5. 提交訊息少 scope**：`9a0450f` 的 `feat: 待辦支援到期日與逾期清單` 缺 project.md 規定的 `type(scope)`。修正要改寫歷史，建議只在之後的提交改正。

## 已查核維度

- 驗收與證據：
  - 核准基線：`**核准 commit**` 為 df95965；以 acceptance.md 的 `git log -G` pattern 對 HEAD 推導，同樣得到 df95965。`git diff df95965 9a0450f -- docs/issues/issue-3601/README.md` 只動核准 commit 回填、Timeline 與 `**狀態**`，規格未改。核准表與 Scenario 集合相等，都是 {SCN-001, SCN-002}。
  - SCN-001（`docs/issues/issue-3601/implementation-plan.md:9`，`test_due.py:7-9`）：期望值是字面值，不是同義反覆。單迴圈合併理由成立（`render` 回傳值即 CLI 輸出）。以 BASE 的 `todo.py` 重現紅燈（缺「（到期 11/20）」）。HEAD 上 `python3 -m unittest -v` exit 0，Ran 3 tests OK。重構 no-op 有理由。四段證據齊全，**通過**。
  - SCN-002（`docs/issues/issue-3601/implementation-plan.md:10`，`test_due.py:11-16`）：紅燈來自 stub，屬目標行為紅燈；期望值為字面值；拿掉「未完成」過濾後測試會紅。today 邊界 `<=` 變異存活，屬證據持久力不足，不是假綠燈。缺核准，見 M1，**不通過**。
  - 未發現假綠燈。
- 相關失敗面：

| 輸入／狀態 | 預期 | 實際 | 覆蓋 | 判定 |
|---|---|---|---|---|
| 既有資料沒有 due 欄位 | 輸出與原本相同 | 相同 | `test_todo.py` `test_render_marks_done`、`test_overdue` 第 4 筆 | 通過 |
| due 為 null | 不顯示 | 不顯示 | 無 | 可接受 |
| due 等於 today | 依 TBD-2 決定 | 不算逾期 | 無，`<=` 變異存活 | M1 |
| 已完成項目逾期 | 不列出 | 不列出 | `test_overdue` 第 3 筆 | 通過 |
| 已完成項目有 due | 未定義 | 會顯示 | 無 | N2 |
| due 格式異常、空白字串 | 未定義 | 顯示錯亂、比較錯誤 | 無 | N1 |
| 從 CLI 設定 due 或列出逾期 | 不在 Scenario 內 | 做不到 | 無 | S1 |

- 需求：SCN-002 缺核准、TBD-2 未解（M1）；CLI 入口範圍待決（S1）。
- 架構：變更限於 `todo.py` 的純函式與 `render`，未越界。
- 安全：無權限面，無新 I/O，無依賴或 lockfile 變更，不適用。
- 品質：無跨 Task 重複邏輯（`due_of` 由 `render` 與 `overdue` 共用，合理），無過度設計；小精簡見 N3。常青文件：根目錄 `README.md:10` 已補顯示說明，overdue 的說明取決於 S1。
- 豁免、待確認與限制：
  - 無 Gate 豁免紀錄。
  - TBD-2 維持「待確認」，阻擋 SCN-002 交付（M1）。
  - reviewer 未重跑 S2 stub 紅燈，改以 BASE 重現 `AttributeError` 並用變異驗證斷言有效。
  - S1 綠燈紀錄綁在未提交工作樹，以 HEAD 重跑作為最終狀態證據。

## 流程判定
RETURN TO execute-task
