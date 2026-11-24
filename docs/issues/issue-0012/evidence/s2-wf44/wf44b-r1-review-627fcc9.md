# 審查報告
- 範圍：完整交付範圍（TARGET `main`，`70f4ada..627fcc9`，5 個檔案）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：627fcc9cd1fa0466b84cfdbcd4c6c825103c1391
- Reviewed patch-id：00063a049f4ef7f9bbdee01706ea1b851332f730
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId ad95857d101dd7920），非原實作者；協調者複核後保存，2026-11-24

## 問題與風險

### MUST FIX

- **M1. SCN-002 未核准就實作**（`需決策`）
  - 位置：`docs/issues/issue-3601/README.md:41`（SCN-002 為 `待核准`）、`docs/issues/issue-3601/README.md:52`（TBD-2 `待確認`）、`todo.py:37-39`、`test_due.py:11-16`、`docs/issues/issue-3601/implementation-plan.md:10`
  - 影響：違反 acceptance.md「只實作已核准的 Task」與「PR 前所有現存驗收條件都須已核准或逐項豁免」。`overdue` 用嚴格 `<`（到期日等於今天不算逾期），等於替使用者決定了 TBD-2。
  - 待決問題：逾期以哪一天為界？到期日等於今天算不算逾期？
  - 可選做法：(a) 早於今天才算逾期（現行實作）；(b) 到期日等於今天也算（`<=`）；(c) 本次不交付 SCN-002，移除 `overdue` 與 S2，另開 issue。
  - reviewer 建議：依逐題確認取得答案，更新核准表與 TBD-2，再補「到期日等於今天」的邊界測試鎖住分界。
- **M2. SCN-001、SCN-002 缺紅綠重構證據**
  - 位置：`docs/issues/issue-3601/implementation-plan.md:9-10`
  - 影響：證據只有「`python3 -m unittest -v` 3 項全數通過」，缺外迴圈／單元紅燈、最小實作後全綠、重構後全綠（或 no-op 理由），也沒有單迴圈合併理由。測試與實作在同一提交 `627fcc9` 加入，無法從歷史重建紅燈。依 verification.md，四段缺任一段即證據不完整。
  - 建議：在原任務列補齊四段證據（可在 BASE 上先加測試取得目標行為紅燈）；SCN-002 待 M1 決策後再做。

### SHOULD FIX

- **S1. CLI 無法設定 due，`overdue` 沒有 CLI 入口**（`需決策`）：`todo.py:18-21`、`todo.py:53-59`、`README.md:10`。due 只能手動寫進 `todo.json`。Gherkin 寫「執行 render」「呼叫 overdue」，綁在內部函式（acceptance.md 要求描述外部行為），規格本身沒要求 CLI。待決問題：本 issue 是否包含 `add` 設定 due 與逾期子命令？可選：(a) 維持函式層級並在使用說明註明 due 來源；(b) 擴充 CLI，新增 Scenario 並核准；(c) 另開 issue。reviewer 建議 (c)，並在根目錄 README 補一句 due 的來源。
- **S2. 已完成待辦也顯示到期日，屬未核准的推導行為**（`需決策`）：`todo.py:46-48`。`{"done": true, "due": "2026-11-20"}` 輸出 `[x] 1. t（到期 11/20）`（reviewer 實測）。SCN-001 只規範未完成待辦，TBD-1 只決定無到期日不顯示。建議請使用者決定並記入待確認事項或新增 Scenario，再補測試。
- **S3. 概述寫了進度**：`docs/issues/issue-3601/README.md:5`「目前 S1、S2 都已完成，測試全數通過，等待審查」。範本規定進度只記在 `**狀態**` 與任務清單，且此句與 SCN-002 未核准不符。建議刪除。
- **S4. Timeline 記非語意事件，「建立並核准」易誤導**：`docs/issues/issue-3601/README.md:58-60`。完成步驟不屬 Timeline 事件；第 58 列易讓人以為兩個 Scenario 都已核准。建議刪第 59、60 列，第 58 列改「建立；SCN-001 核准」。
- **S5. TBD-1 結論寫在影響欄**：`docs/issues/issue-3601/README.md:51`。結論、理由與日期應在狀態欄，影響欄只留 `SCN-001`。狀態值本身正確，不影響掃描判斷。
- **S6. `## 涉及檔案` 不完整**：`docs/issues/issue-3601/README.md:13` 漏列常青文件 `README.md`，測試檔寫成「對應的測試檔」。建議明列 `todo.py`、`test_due.py`、`README.md`。

### NICE TO HAVE

- **N1. due 格式異常沒有防護**：`todo.py:39`、`todo.py:47`。實測 `"11-20"`、`" "` 輸出「（到期 ）」；`"2026-1-5"` 輸出「（到期 1/5）」；字串比較使 `"2026-11-5"` 在 today=`2026-11-19` 被判為不逾期。因 CLI 無法寫入 due，只在手動編輯時出現。建議記錄「due 為補零的 YYYY-MM-DD」假設，或以 `datetime.date.fromisoformat` 解析。
- **N2. `due_of` 抽象價值低**：`todo.py:32-34` 只包一層 `item.get("due", "")`，`overdue` 內呼叫兩次；可內聯。docstring 的「issue-3601：」把 issue 歷程帶進原始碼，可移除。
- **N3. 測試覆蓋偏窄（證據持久力）**：缺「到期日等於 today」（M1）與「已完成待辦的 render」（S2）測試。斷言皆用獨立字面值，非同義反覆。

## 已查核維度

- 驗收與證據：
  - 核准 commit `df95965` 經 acceptance.md pattern 推導得 `df95965976437d22784f5a4b5c28c3a2ee20057a`，一致；`git diff df95965 627fcc9 -- docs/issues/issue-3601/` 只有核准 commit 回填、Timeline、狀態與任務狀態，Gherkin 未變動。
  - SCN-001：已核准；`test_due.py:7-9` test_render_shows_due 覆蓋，行為正確，但缺紅綠證據（M2）。
  - SCN-002：`待核准`，卻已實作並以 `test_due.py:11-16` test_overdue 覆蓋，不能作為交付證據（M1、M2）。
  - 在 HEAD 執行 `python3 -m unittest -v`：Ran 3 tests，OK（協調者與 reviewer 各自重跑）。
  - 假綠燈：未發現（無 mock、無同義反覆、既有 `test_todo.py` 未被弱化）。證據持久力另列 N3。
- 相關失敗面：

| 失敗面 | 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
|---|---|---|---|---|
| 既有 render 相容 | 無 due 的待辦 | 輸出與原本相同 | `test_todo.py` test_render_marks_done | OK |
| 顯示到期日 | 未完成、due=2026-11-20 | 結尾「（到期 11/20）」 | test_render_shows_due | OK |
| 逾期主路徑 | today=2026-11-19，due 11-01、12-01 | 只回傳 11-01 | test_overdue | 行為 OK，未核准（M1） |
| 已完成不列逾期 | done=True、due=11-01 | 排除 | test_overdue id 3 | OK |
| 無 due 不列逾期 | 缺 due 欄位 | 排除 | test_overdue id 4 | OK |
| 到期日等於 today | due=2026-11-19 | 未決定（TBD-2） | 無；實作判不逾期 | 需決策（M1） |
| 已完成待辦 render | done=True 且有 due | 未規範 | 無；實作會顯示 | 需決策（S2） |
| due 格式異常 | `"11-20"`、`"2026-11-5"` | 未規範 | 無 | N1 |
| due 為 null／空字串 | None、"" | 不顯示、不逾期 | reviewer 手動探測 | OK |
| CLI 設定／列出 due | `todo.py add …` | 規格未要求 | 無 | 需決策（S1） |

- 需求：SCN-002 超出已核准範圍（M1）；已完成待辦的顯示未經核准（S2）。
- 架構：改動侷限 `todo.py` 單檔，未跨邊界。
- 安全：無新輸入面，只讀寫本機 JSON，不適用。
- 品質（含跨 Task 重複與過度設計）：S1／S2 共用 `due_of`，無已分歧的重複邏輯；`due_of` 屬輕微過度抽象（N2）。常青文件 `README.md` 依 project.md 更新，內容與行為一致，但未交代 due 來源（S1）。
- issue 文件：S3–S6 屬格式與措辭，依流程契約 2.8 列 SHOULD FIX；狀態值與 `**核准 commit**` 正確，不會讓 verify-artifact 或懸置掃描誤判。
- 豁免、待確認與限制：
  - 無 Gate 豁免紀錄。
  - TBD-2 維持 `待確認`，直接阻擋 SCN-002 交付（M1）。
  - 核准來源「使用者回覆『核准』」只能從 README 文字核對，無原始對話紀錄可查。
  - 紅燈是否曾發生無法從 Git 歷史驗證。

## 流程判定
RETURN TO execute-task

理由：M1 交付內容含未核准 Scenario 並替使用者決定了未確認的分界；M2 兩個 Scenario 缺必要的紅綠重構證據。建議順序：協調者先就 M1、S1、S2 取得使用者決策 → execute-task 補證據與邊界測試、修正 S3–S6 → 送增量覆審（Reviewed BASE 維持 `70f4ada`）。
