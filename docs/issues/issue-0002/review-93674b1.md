# 審查報告
- 範圍：完整 PR（issue-0002-bookkeeping-commits 對 main）
- Reviewed BASE SHA：6bd2504d70047aa2982195cd138ee0e6c003289b
- Reviewed HEAD SHA：93674b1f89361f9860e2d1d6b50b27ffabb3dc2d
- Reviewed patch-id：ac764f6543ed247b43fbfccbd38c2e6cf71589bf
- 獨立 reviewer：隔離 subagent（未參與實作）
- Review artifact：docs/issues/issue-0002/review-93674b1.md
- 審查日期：2026-11-03

本次是第三次審查，對象是 [review-9ee4139](review-9ee4139.md) PASS 之後的完整 PR。

範圍已自行重算：
- `git diff 6bd2504 93674b1 | git patch-id --stable` 得到 `ac764f65…`，與委派值相同，工作樹乾淨。
- 上次之後只有兩個提交：
  - `c592cbd`：保存 review-9ee4139，並改狀態、加一列 Timeline。
  - `93674b1`：依使用者決定處理 NICE TO HAVE 1～4。
- 兩個提交都沒有動到 `scripts/`、`skills/`、acceptance.md 與回歸紀錄，所以腳本行為與上次相同。上次對腳本、S7 證據與 SCN 的查核結論沿用，本次只審新增的文字。

核准狀態：核准 commit 仍為 `e383a69`。`git diff e383a69 93674b1 -- docs/issues/issue-0002/README.md` 只有關鍵差異表的連結改名、核准 commit 回填、狀態與 Timeline，Gherkin 與核准紀錄都沒有改，原核准仍有效。

對抗測試放在 `<scratchpad>/review/r2/adv3.py`，以 HEAD 的 `verify-artifact.py` 在拋棄式 repo 實測新增文字描述的行為。路徑依本 issue 證據的慣例遮蔽。

## 問題與風險

### MUST FIX

無。

### SHOULD FIX

無。

### NICE TO HAVE

1. **整節增刪限制漏列 code fence，也和 docs/AGENTS.md 的用詞不同**：`docs/agents/review-evidence.md:44`，同句出現在 `CHANGELOG.md:23`、`docs/issues/issue-0002/implementation-plan.md:51`、`docs/rule-verification-status.md:315`；另見 `docs/AGENTS.md:129`。
   - code fence：新增文字只寫「節內有標題或粗體開頭的行時整節增刪判定無效」。實測（`adv3.py`）發現，節內有 code fence 時同樣無效，新增含 fence 的 Gate 豁免紀錄、刪除含 fence 的待確認事項都是如此。
   - 用詞：docs/AGENTS.md 寫「用子標題或粗體欄位時」，review-evidence.md 寫「粗體開頭的行」。以粗體日期開頭的清單項目（`- **2026-11-04**：豁免 e2e`）算「一般清單」，但同樣會判定無效。
   - 為什麼不列為 SHOULD FIX：同檔 `:47` 已寫 code fence 一律凍結，漏列的方向又是 fail-closed，代價只是一次重審。
   - 建議：寫成「節內有標題、code fence 或粗體開頭的行時……」。docs/AGENTS.md 改為「行首不用粗體、不用子標題或 code fence」，或直接引用 review-evidence.md 的說法。

2. **計畫已知限制有兩處說得太寬**：`docs/issues/issue-0002/implementation-plan.md:51`。
   - 「HTML 形式的標題或粗體」會讓人以為 `<h2>` 都會放行。實際上行首的 `<h2>…` 判定無效（`test_loose_heading_in_bookkeeping_invalid`），放行的只有不在行首的寫法（`<div><h2>`），以及 `<strong>`、`<b>`。
   - 「只改檔案模式」指的是 README 的 mode 變更。報告檔可執行時仍然無效。
   - 建議：改成「不在行首的 HTML 標題」與「README 只改檔案模式」。

3. **範本的格式指標指向另一節**：`docs/agents/readme-templates.md:170`。
   - 註解寫 Gate 豁免紀錄「格式見『BDD 驗收規格與 TDD 證據』」，但這次新增的書寫建議放在 docs/AGENTS.md 的「Gate 豁免紀錄」一節，兩者是同層的不同章節。
   - 照範本註解查找的 agent 看不到新建議。另外，第一份範本（第 7～112 行）完全沒有提到 Gate 豁免紀錄放在哪裡，plan:51 的「照範本放在 Timeline 之前」只有第二份範本做得到。
   - 這個指標在 main 上就是如此，不是本 PR 引入的；但本次的建議要靠讀者找得到才有效。
   - 建議：把指標改成「格式見 docs/AGENTS.md『Gate 豁免紀錄』，放在 Timeline 之前」。

4. **CHANGELOG 小節標題沒列 docs/AGENTS.md**：`CHANGELOG.md:19`、`:23`。
   - 新條目寫在「變更（`docs/agents/review-evidence.md`、`skills/review/`）」底下，內容卻包含 docs/AGENTS.md 的改動。4.8.1 的寫法是把 docs/AGENTS.md 列在小節標題裡。
   - 建議：標題補上 `docs/AGENTS.md`。

## 已查核維度

### review-9ee4139 NICE TO HAVE 1～4 的處理

| 項目 | 處理 | 查核 | 結論 |
|---|---|---|---|
| NICE 1 計畫 SCN-006 結論 | `implementation-plan.md:84` 改成「依第一輪判準通過」，並寫明 28a＋28c 兩組都是 0、減少來自追加的 28d，指向 S7 與「SCN-006 綜合對照」 | 與回歸紀錄第 38、77 行一致，指向的章節都存在（check-links 通過） | 已處理 |
| NICE 2 對抗腳本出處與已知限制 | `:94` 的出處改為 review-9ee4139；`:51` 補上仍放行的寫法與反方向的 fail-closed | 出處屬實：review-9ee4139 記有重跑結果。列出的放行寫法與 reviewer 實測相符。本機 126 份 README 在記帳章節內都沒有不帶粗體的欄位、HTML 標題或粗體、`|` 接 `---`、縮排程式碼區塊（reviewer 重掃）。「footer 換節判定無效、照範本放在 Timeline 之前不會碰到」與 `adv2.py` 結果相符 | 已處理；措辭見 NICE 2 |
| NICE 3 HTML／表格放行 | 登記為已知限制，並說明不排除 `|` 的理由 | 理由正確：Timeline 表格末列緊接 `---` 時會被誤判成 setext | 已處理 |
| NICE 4 整節增刪限制與書寫建議 | review-evidence.md:44 補限制；docs/AGENTS.md:129 建議用表格或一般清單；CHANGELOG 與驗證狀態同步 | 實測：表格（即使儲存格以粗體開頭）與行中帶粗體的清單整節新增都有效；既有欄位式的節補一筆一般清單有效、補一筆欄位無效；含 `###`、setext 的節整節增刪無效。以上與文字相符；code fence 漏列見 NICE 1 | 已處理；措辭見 NICE 1 |
| NICE 5 驗證狀態用詞 | 依使用者決定維持 | — | 不處理，屬使用者決定 |

### 新增文字與其他規則的一致性

- **docs/AGENTS.md:129**：
  - 新句只是書寫建議，和 review-evidence.md:44、:47 的判定一致。
  - review-evidence.md:51 寫的是「使用者決定不重審時記入豁免」，那時 PASS 已經失效，不受新句影響；dev-cycle:44 寫的是「接受未修的 MUST FIX 記入豁免」，照新建議書寫時可沿用 PASS。兩處都不衝突。
  - 流程契約 2.3 以下，審查之後的任何提交本來就讓 PASS 失效，新句在舊契約下仍然成立。
  - 沒有其他規則要求用欄位寫豁免紀錄：reviewer 搜尋過 skills、rules、docs/agents、usage 與 INSTALL。
- **review-evidence.md:44**：
  - 新增的括號限制是 S6 判定的直接後果，屬於 issue README 設計邊界「所有章節標題」「其他粗體欄位行」凍結的範圍。
  - 方向只會更嚴，沒有放寬 TBD-3「可整節新增或刪除」的核准內容，也不需要重新核准。
- **版本紀錄**：
  - docs/AGENTS.md 的 2.8 修訂列已補上這句。文件版本 2.8、流程契約 2.4、最後更新 2026-11-03 都沒有變；2.8 尚未發布，同日修訂合理。
  - CHANGELOG 4.9.0 已補條目，只差小節標題（NICE 4）。
  - rule-verification-status 新增一列「僅靜態撰寫」，來源寫的是語料模擬，與 review-9ee4139 的內容相符。
  - 技能與最低契約沒有改。

### 記帳提交與流程紀錄

- `c592cbd`：reviewer 重跑 `verify-artifact.py --reviewed 9ee4139 --head c592cbd`，結果 OK，列出新增報告、狀態（實作中 → 審查通過，待合併）與 Timeline，與協調者所述相符。保存的報告共 149 行，判定 PASS，之後沒有再被修改。
- `93674b1`：改到 CHANGELOG 與計畫等凍結內容，檢查器以 CHANGELOG.md 判定無效。協調者因此送覆審，做法正確。README 狀態改回「審查中」，新增的 Timeline 列記下使用者原話「修正後再覆審一次」。
- 計畫 S5 已標 ✅，同時寫明「再送覆審」，沒有把待審的 HEAD 說成已通過。

### 驗收與證據

SCN-001～006 的證據與結論同 review-9ee4139：腳本與 S7 實跑證據都沒有變動，本次 diff 只改文件。

根目錄五項檢查由 reviewer 於 2026-11-03 在 `93674b1` 自行執行：

| 檢查 | 結果 |
|---|---|
| `check-kit.py` | exit 0 |
| `check-links.py` | exit 0 |
| `bash -n scripts/install.sh` | exit 0 |
| `test-install.py` | 14 個測試 OK，exit 0 |
| `test-evidence.py` | 99 個測試 OK，exit 0 |

### 相關失敗面（本次新增文字）

| 輸入／狀態 | 文件描述 | 實測 | 判定 |
|---|---|---|---|
| 整節新增 Gate 豁免紀錄（表格，含粗體儲存格） | 有效 | OK | 一致 |
| 整節新增 Gate 豁免紀錄（清單，粗體在行中） | 有效 | OK | 一致 |
| 整節新增或刪除，節內有 `###`、setext 或欄位寫法 | 無效 | INVALID | 一致 |
| 整節新增或刪除，節內有 code fence | 未提及 | INVALID | 漏列（NICE 1） |
| 清單項目以粗體日期開頭 | AGENTS.md 未明說，review-evidence 已涵蓋 | INVALID | 用詞不一（NICE 1） |
| 既有欄位式豁免節補一筆一般清單或欄位 | 「用粗體欄位時補記會讓 PASS 失效」 | 補清單 OK，補欄位 INVALID | 建議偏保守，可接受 |
| 新節插在 Timeline 與 footer 之間 | 無效 | INVALID（上次 `adv2.py`） | 一致 |

### 需求、架構、安全、品質

- **需求**：範圍只限 NICE 1～4 的文件修正，沒有擴張，也沒有改腳本或規則判定。
- **單一說法**：同一限制寫在 review-evidence.md、CHANGELOG、計畫與驗證狀態四處，內容一致，但都漏列 fence（NICE 1）。權威定義仍在 review-evidence.md。
- **安全與品質**：沒有程式變更。新句放在核心文件的對應章節，只有一句，注意力成本低。

### 豁免、待確認與限制

- README 沒有 Gate 豁免紀錄，TBD-1～3 都已解決。NICE 5 依使用者決定維持。
- review-9ee4139 列出的已揭露限制都不變：S4 部分完成、「只改驗收 → 檢查器無效」在 agent 層無法區分、2.3 與平台模式只有靜態撰寫或腳本測試、只測 Claude Code。
- 本次沒有重跑宿主 agent；新增的書寫建議是否被 agent 遵守沒有實跑，已登記為僅靜態撰寫。

## 流程判定
PASS
