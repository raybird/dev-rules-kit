# 審查報告
- 範圍：完整 PR（issue-0002-bookkeeping-commits 對 main）
- Reviewed BASE SHA：6bd2504d70047aa2982195cd138ee0e6c003289b
- Reviewed HEAD SHA：37f0d4507a89ade492e6f39d65efd37eb26aa70d
- Reviewed patch-id：7af39b3e8c63567141a5e1216edf3853fc681f36
- 獨立 reviewer：隔離 subagent（未參與實作）
- Review artifact：docs/issues/issue-0002/review-37f0d45.md
- 審查日期：2026-11-03

本次是依使用者指定的最後一輪覆審，對象是 [review-93674b1](review-93674b1.md) PASS 之後的完整 PR。範圍已自行重算：`git diff 6bd2504 37f0d45 | git patch-id --stable` 得到 `7af39b3e…`，與委派值相同，工作樹乾淨。

上次之後有兩個提交：
- `ff2ce1c` 保存 review-93674b1，並改狀態、加一列 Timeline。
- `37f0d45` 依使用者決定處理 review-93674b1 的 NICE TO HAVE 1～4。

兩個提交都沒有動到 `scripts/`、`skills/`、acceptance.md 與回歸紀錄，所以腳本行為與前兩輪相同。review-9ee4139 對腳本、S7 證據與 SCN 的查核結論沿用；本次只審新增的文字與範本。

核准狀態：核准 commit 仍為 `e383a69`。`git diff e383a69 37f0d45 -- docs/issues/issue-0002/README.md` 只有關鍵差異表的連結改名、核准 commit 回填、狀態與 Timeline。Gherkin 與核准紀錄沒有變更，原核准仍有效。

對抗測試沿用 `<scratchpad>/review/r2/adv3.py`，並加測範本註解的各種放置方式。兩者都在拋棄式 repo 以 HEAD 的 `verify-artifact.py` 執行，路徑依本 issue 證據的慣例遮蔽。

## 問題與風險

### MUST FIX

無。

### SHOULD FIX

無。

### NICE TO HAVE

依使用者指示，以下各項只留在報告，不再要求修正。

1. **Gate 範本註解沒有標「最終輸出移除本註解」**：`docs/agents/readme-templates.md:103`、`:172`。
   - 範本其他註解都附這句，只有這兩則沒有，下游可能把它留在 README 裡。
   - 實測：註解留在凍結章節時，若在審查後用 Gate 豁免紀錄取代註解，判定無效。例如第一份範本省略待確認事項，註解就落在前一個凍結章節；第二份範本的註解本來就在「實作與驗證步驟」。
   - 下列做法都判定有效：
     - 第一份範本保留待確認事項，註解留在該節內。
     - 把新節加在註解之後。
     - 註解已移除。
   - 本機 126 份下游 README 都沒有保留範本註解，觸發機率極低，而且是 fail-closed。第二份範本的註解在 main 上就沒有這句。
   - 可選做法：
     - 兩則註解都補「最終輸出移除本註解」。
     - 或寫明「加在本註解之後」。

2. **計畫已知限制的列舉讀起來有歧義**：`docs/issues/issue-0002/implementation-plan.md:51`。
   - 「行首的 `<h2>` 則判定無效、以 `|` 開頭的段落後接 `---`」用頓號接續，容易誤讀成後者也判定無效。
   - 可選做法：
     - 把「行首的 `<h2>` 則判定無效」改放括號。
     - 或改用分號分隔各項。

3. **驗證狀態的來源沒有跟著補上 code fence**：`docs/rule-verification-status.md:315`。
   - 規則欄已補上 code fence，但驗證來源欄仍只引用 review-9ee4139 的語料結果。fence 的實測出自 review-93674b1（`adv3.py`）。
   - 可選做法：來源欄補上 review-93674b1。

4. **範本指標的改動沒有記入版本紀錄**：`CHANGELOG.md:26` 那一節與 `docs/AGENTS.md:201` 的 2.8 列。
   - 第一份範本新增 Gate 指標，兩份範本的指標都改指 docs/AGENTS.md，兩處版本紀錄都沒有提到。
   - 這屬於指標與範例層級的變動，不影響流程契約；4.9.0 也還沒發布。
   - 可選做法：在 CHANGELOG 補半句。

## 已查核維度

### review-93674b1 NICE TO HAVE 1～4 的處理

| 項目 | 處理 | 查核 | 結論 |
|---|---|---|---|
| NICE 1 漏列 code fence、用詞不一 | review-evidence.md:44、CHANGELOG:23、plan:51、rule-verification-status:315 都補上「code fence」；docs/AGENTS.md:129 改成「行首不用粗體，也不放子標題或 code fence」 | 實測與文字相符（`adv3.py` 與上次結果）：<br>- 節內有 `###`、setext、code fence、欄位寫法、以粗體日期開頭的清單項目時，整節增刪判定無效。<br>- 表格（儲存格以粗體開頭也可）、行中帶粗體的清單，判定有效。<br>docs/AGENTS.md 改用「行首」的說法後，涵蓋了以粗體開頭的清單項目，與 review-evidence.md:47 一致 | 已處理 |
| NICE 2 已知限制太寬 | plan:51 改為「不在行首的 HTML 標題（例如 `<div><h2>`）與 HTML 粗體」，並註明行首的 `<h2>` 判定無效；「README 只改檔案模式（報告檔可執行時仍判定無效）」 | 與 `test_loose_heading_in_bookkeeping_invalid`（行首 `<h2>`）、可執行報告的負向測試，以及 `adv2.py` 的放行結果相符 | 已處理；措辭見 NICE 2 |
| NICE 3 範本指標 | 兩份範本的註解都改成「在 Timeline 之前另加 `## Gate 豁免紀錄`（格式見 docs/AGENTS.md「Gate 豁免紀錄」）」；第一份範本在待確認事項表格之後、`## Timeline` 之前新增同一則註解 | 位置正確：<br>- 第一份範本的章節順序是「風險與首要驗證／待確認事項／Timeline」，註解放在 Timeline 正前方，照做時新節位於 Timeline 之前，footer 不會換節。<br>- 實測照範本加入、保留註解並在其後加入、或取代待確認事項內的註解，都判定有效。<br>- 指向的章節存在（`docs/AGENTS.md:127`），check-links 也通過 | 已處理；邊界情況見 NICE 1 |
| NICE 4 CHANGELOG 小節標題 | 標題補上 `docs/AGENTS.md` | 與 4.8.1 的寫法一致 | 已處理 |

### 這次 diff 的其他查核

- **記帳提交 `ff2ce1c`**：
  - reviewer 自行重跑 `verify-artifact.py --reviewed 93674b1 --head ff2ce1c`，結果 OK，列出三項變更：新增報告、狀態（審查中 → 審查通過，待合併）、Timeline。
  - 保存的報告結尾為 PASS，之後的提交沒有再修改它。
- **`37f0d45`**：
  - 動到 CHANGELOG、計畫等凍結內容，因此送覆審是正確的。
  - README 狀態已改回「審查中」。
  - 新增的 Timeline 列記下使用者原話「修正後覆審，最後一輪」，也寫明停止條件。
- **與其他規則的一致性**：
  - docs/AGENTS.md:129 的新句與 review-evidence.md:44、:47 的判定一致。
  - 新句也不和 review-evidence.md:51、:57、dev-cycle:44、:50 的 Gate 豁免用法衝突。
  - 範本註解指向的是核心文件中真正寫有格式的章節，修正了 main 上原本指錯章節的指標。
- **版本**：
  - 文件版本 2.8、流程契約 2.4、最後更新 2026-11-03 都沒有變；2.8 還沒發布，同日修訂合理。
  - 技能與最低契約沒有改，check-kit 通過。
  - 範本指標的改動沒有記入版本紀錄（NICE 4）。

### 驗收與證據

SCN-001～006 的證據與結論同 review-9ee4139。腳本、技能與 S7 實跑證據都沒有變動，本次 diff 只改了文件與範本註解。

根目錄五項檢查由 reviewer 於 2026-11-03 在 `37f0d45` 自行執行，全部 exit 0：

| 檢查 | 結果 |
|---|---|
| `check-kit.py` | exit 0 |
| `check-links.py` | exit 0 |
| `bash -n scripts/install.sh` | exit 0 |
| `test-install.py` | 14 個測試 OK，exit 0 |
| `test-evidence.py` | 99 個測試 OK，exit 0 |

### 相關失敗面（本次新增文字與範本）

| 輸入／狀態 | 文件描述 | 實測 | 判定 |
|---|---|---|---|
| 整節增刪，節內有 code fence | 無效 | INVALID | 一致 |
| 以粗體日期開頭的清單項目 | 行首不用粗體 | INVALID | 一致 |
| 表格寫法、行中帶粗體的清單 | 有效 | OK | 一致 |
| 照第一份範本在 Timeline 前加 Gate 豁免紀錄（註解已移除） | 有效 | OK | 一致 |
| 保留註解：放在待確認事項內，或在註解之後加新節 | 未明說 | OK | 一致 |
| 保留註解：註解落在凍結章節，又被新節取代 | 未明說 | INVALID | fail-closed（NICE 1） |

### 需求、架構、安全、品質

- **需求**：範圍只限 review-93674b1 的 NICE 1～4，沒有擴張，也沒有改變腳本或判定。
- **單一說法**：整節增刪的限制以 review-evidence.md:44 為準。CHANGELOG、計畫與驗證狀態三處說法一致；docs/AGENTS.md 只寫書寫建議，與上述一致。
- **安全與品質**：沒有程式變更。範本新增的只有一則註解，注意力成本低。

### 豁免、待確認與限制

- README 沒有 Gate 豁免紀錄。TBD-1～3 都已解決。review-9ee4139 的 NICE 5 依使用者決定維持。
- 已揭露的限制都不變：
  - S4 部分完成。
  - 「只改驗收 → 檢查器無效」在 agent 層無法區分。
  - 2.3 相容、平台模式與 Gate 書寫建議只有靜態撰寫或腳本測試。
  - 只測 Claude Code。
- 本次沒有重跑宿主 agent。
- 依使用者指定，本輪是最後一輪；上列 NICE TO HAVE 只記錄，不阻擋判定。

## 流程判定
PASS
