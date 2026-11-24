# 審查報告
- 範圍：完整交付範圍（main..HEAD）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：9a0450fcabb8640cbf8fcfa121fdb86539782b7a
- Reviewed patch-id：546a3a5ec083f72d01410fb705562fd6d1525803（`git diff 70f4ada 9a0450f | git patch-id --stable`）
- 獨立 reviewer：Claude Code 宿主隔離 subagent（general-purpose，agentId a27afaa15271e75cc），非原實作者；協調者於 2026-11-24 複核主要發現

## 問題與風險

### MUST FIX
1. **SCN-002 未核准卻已實作並標為完成** — `docs/issues/issue-3601/README.md:41`（SCN-002 為 `待核准`）、`docs/issues/issue-3601/README.md:52`（TBD-2 仍 `待確認`）、`docs/issues/issue-3601/implementation-plan.md:10`（S2 標 ✅）、`todo.py:37-39`、`test_due.py:11-16`。
   - 影響：acceptance.md「分批核准」只允許實作已核准的 Task，PR 前所有驗收條件須已核准或逐項豁免；S2 缺少新行為的核准來源（review-evidence.md「審查強度與流程判定」列為 MUST FIX）。實作採 `due < today`，等於替使用者決定了 TBD-2（逾期以今天還是明天為界）。
   - `需決策`。待決問題：SCN-002 是否核准？到期日等於今天時算不算逾期？
     - (a) 核准「到期日早於今天才算逾期」，維持現行實作。
     - (b) 改為「到期日不晚於今天就算逾期」，修改實作。
     - (c) SCN-002 移出本次交付，回退 `overdue` 與 S2。
     - reviewer 建議 (a)，在 Gherkin 補「到期日等於今天時不列出」的例子與對應測試，再由使用者核准。

### SHOULD FIX
2. **使用者無法經由 CLI 使用此功能** — `todo.py:18-21`、`todo.py:53-59`、`README.md:10`。`add` 不接受到期日，逾期清單也只有函式介面，只能手改 todo.json。兩個 Scenario 的 When 寫「執行 render」「呼叫 overdue」，綁在內部函式上，不符 acceptance.md「完整 Gherkin 的要求」（描述外部行為）。
   - `需決策`。待決問題：本 issue 要不要納入 CLI 設定到期日（例如 `add --due`）與列出逾期的子命令？
     - (a) 納入本 issue，補 Scenario、核准與實作。
     - (b) 記為本次不做，待確認事項寫 `不影響本次交付` 並附追蹤 issue。
     - reviewer 建議至少 (b)，並把 When 改寫成外部行為。
3. **到期日格式沒有驗證，逾期判斷依賴字典序** — `todo.py:39`、`todo.py:48`。協調者在 HEAD 實測 `overdue([{"due": "2026-2-1", ...}], "2026-11-19")` 回傳 `[]`，二月的待辦被判為未逾期。`"11/20"` 會顯示成「（到期 ）」。若採 CLI 寫入，建議寫入時用 `date.fromisoformat` 驗證；若維持手改，至少在根 README 寫明格式 YYYY-MM-DD。與發現 2 一併決策。
4. **根 README 說明不完整** — `README.md:10` 只寫顯示格式，沒寫如何設定到期日或格式要求。
5. **涉及檔案不準確** — `docs/issues/issue-3601/README.md:13`「對應的測試檔」應明列 `test_due.py`（新增），並補上有異動的常青文件根 `README.md`。
6. **概述寫了進度** — `docs/issues/issue-3601/README.md:5`「目前 S1、S2 都已完成，測試全數通過，等待審查」。進度只能記在 `**狀態**` 與任務清單；這句在實作前的核准提交 df95965 就已存在，當時與事實不符。建議刪除。
7. **Timeline 內容不符規定** — `docs/issues/issue-3601/README.md:58-60`。「完成 S1／S2」重複了任務狀態；「建立並核准」容易被讀成兩個 Scenario 都已核准。建議改為「建立；SCN-001 核准」並刪除完成列；額外的「負責人」欄非範本欄位。
8. **核准來源太籠統** — `docs/issues/issue-3601/README.md:36`「使用者回覆『核准』」沒寫涵蓋哪些 Scenario。建議記原話、題號與 Scenario ID。
9. **TBD-1 結論寫錯欄** — `docs/issues/issue-3601/README.md:51`。結論「使用者選不顯示」應寫在狀態欄（`已解決：2026-11-16，…`），影響欄只寫未確認時的影響與關聯編號。狀態值本身正確，不影響判讀工具，所以不到 MUST FIX。

### NICE TO HAVE
10. `todo.py:39` 呼叫兩次 `due_of(i)`，可化簡為 `i.get("due") and i["due"] < today` 之類；`due_of` 只是 `dict.get` 的薄包裝，可接受。docstring 的「issue-3601：」追溯資訊放在 Git 即可。
11. `overdue` 的 `today` 若傳入 `datetime.date` 會拋出 TypeError；docstring 已寫明需傳 YYYY-MM-DD 字串，可接受。
12. 提交 subject `feat: 待辦支援到期日與逾期清單` 缺 scope，不符 project.md 的 `type(scope): 中文摘要`。
13. TBD-2 事項欄的「等使用者確認」屬狀態描述，可移除；標題分隔符號與 metadata 換行和範本略有差異。

## 已查核維度
- **驗收與證據**
  - SCN-001：`test_due.py:7-9` 斷言獨立字面值。紅燈（缺少到期日輸出的 AssertionError）、綠燈、重構 no-op 均記在 `docs/issues/issue-3601/implementation-plan.md:9`。單迴圈合併理由成立：`main` 直接印出 `render(load())`。有效。
  - SCN-002：`test_due.py:11-16` 含已完成（id 3）與無到期日（id 4）的反例，紅燈來自回傳 `[]` 的 stub。測試本身不是假綠燈，但 SCN-002 未核准，不能作為驗收依據（見 MUST FIX 1）。
  - 測試：reviewer 與協調者於 2026-11-24 在 HEAD 9a0450f 執行 `python3 -m unittest -v`，exit 0，Ran 3 tests OK。
- **核准基線**：`**核准 commit**` 已回填為 df95965。依 acceptance.md 推導命令，最後修改 `**核准來源**` 行的提交亦為 df95965，兩者一致。`git diff df95965 9a0450f -- docs/issues/issue-3601/README.md` 只變動核准 commit、Timeline 兩列與 `**狀態**`，Gherkin 未變，SCN-001 原核准有效。
- **相關失敗面**

  | 輸入／狀態 | 預期 | 實際 | 覆蓋 | 判定 |
  |---|---|---|---|---|
  | 無到期日 | 不顯示、不算逾期（TBD-1） | 符合 | `test_todo.py:7-9`、`test_due.py` id 4 | OK |
  | 已完成且過期 | 不算逾期 | 不列出 | `test_due.py` id 3 | OK |
  | 到期日等於今天 | 未定（TBD-2） | 不列出 | 無 | 併入 MUST FIX 1 |
  | `due: null` | 視為無到期日 | 符合 | 無 | OK |
  | 格式不合（`2026-2-1`、`11/20`） | 未定義 | 誤判未逾期、顯示異常 | 無 | SHOULD FIX 3 |
  | 經 CLI 設定到期日或列出逾期 | 概述宣稱可用 | 無入口 | 無 | SHOULD FIX 2 |

- **需求**：SCN-002 超出已核准範圍（MUST FIX 1）；CLI 範圍待決（SHOULD FIX 2）。
- **架構**：改動限於 `todo.py` 單檔與新增測試，符合 project.md 邊界。
- **安全**：不涉及權限、外部輸入或依賴，不適用。
- **品質（含跨 Task 重複與過度設計）**：S1、S2 共用 `due_of`，沒有分歧的重複邏輯，也沒有過度設計。小幅精簡見 NICE TO HAVE 10。
- **常青文件**：根 README 已更新顯示格式，但內容不完整（SHOULD FIX 4）。
- **豁免、待確認與限制**
  - 無 Gate 豁免紀錄。
  - TBD-2 維持 `待確認`，阻擋 SCN-002 的交付。
  - 無遠端平台，報告保存在本機。

## 流程判定
RETURN TO execute-task

理由：SCN-002 未核准就已實作並標為完成，TBD-2 仍待確認，不符「PR 前所有驗收條件須已核准或豁免」。SCN-001 的實作與證據有效，返工時可以沿用。建議協調者先依 acceptance.md「逐題確認」取得 MUST FIX 1 與 SHOULD FIX 2、3 的使用者決定，再依決定補上或回退 S2，並修正 SHOULD FIX 4–9。
