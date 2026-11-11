# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，25 個提交、86 個檔案）；第六輪覆審，重點是上一輪 [review-ac2183c](review-ac2183c.md) 之後的修正 `0dd6306..20d0847`（主要是 `3fc926a`）
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：20d08477f3ca0757241844ea812f20e5e6fca653
- Reviewed patch-id：e0bbc133fb3a385cdf779a33831c9a5fc1e2e631（2026-11-11 以 `git diff 46e09a5 20d0847 | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-20d0847.md
- 審查日期：2026-11-11
- 審查依據：
  - README `## 待確認事項` TBD-2～TBD-6 的使用者決定。TBD-6 決定記帳章節含 `<` 的行一律凍結，code span 裡的標籤名與佔位字因此判需重審，這是已接受的代價，本報告不列為缺陷。TBD-5 由 GitHub #4 處理，不在本 issue 範圍。
  - README Timeline 2026-11-11 的使用者決定：本輪若只找到 v4.9.0 就有的同類缺口，另開 issue 處理，不阻擋本 issue。所以本報告把「本 issue 新引入的缺陷」與「v4.9.0 起就有的同類缺口」分開列。判定方式：同一個案例也用 `46e09a5` 的檢查器（v4.9.0）跑一次，判 OK 的就是 v4.9.0 起就有。
  - CHANGELOG 4.10.0「已知限制」已登記的項目不重報。

## 問題與風險

### MUST FIX

1. **表格的欄數算法和 GFM 不同。表頭多一個 `|` 時，檢查器仍當表格逐列判定，渲染器卻把整張表當成段落。`## 現況` 裡凍結的 code span 標籤因此能被解開，藏住之後的設計邊界、Gherkin 與 metadata，判 OK**
   - 位置：`skills/review/scripts/verify-artifact.py:124-130`（`cells()`、`starts_table()`）、`:201-203`、`:226-227`。
     - `cells()` 用 `line.strip('|')` 去掉頭尾所有的 `|`。GFM 只去掉頭尾各一個。
     - 所以 `|| 外部狀態 | 查證命令 | 上次結果 | 查證日期 |`：檢查器算 4 欄，和分隔列相同，判為表格，每列各自 flush。GFM 算 5 欄，和分隔列不同，不是表格，整張表是一個段落。表頭結尾多一個 `|` 也一樣。
     - 表頭含 `\\|` 時也有落差：檢查器不切開，marked 與 micromark 都切開（T1g）。
     - 段落裡的行內語法可以跨列。凍結列的渲染因此取決於同一張「表」裡的其他列，這正是 S12 想擋的 A2 形態。
   - 實測方式：
     - 在 `<tmp>` 建拋棄式 repo（沿用上一輪的 `probe4.py`），PASS 之後的提交新增報告並改寫 README。
     - 用 marked 17.0.5（GFM）與 micromark 4.0.2 加 micromark-extension-gfm 3.0.0 渲染，再用 parse5 7.3.0 找標記文字的位置（沿用 `render.mjs`）。下表兩個渲染器的結果都相同。
     - 同一組案例也用 `ac2183c` 與 `46e09a5` 的檢查器各跑一次。

     | 案例 | 審查版本 | 記帳提交（只動記帳章節，都不含 `<`） | HEAD | `46e09a5`（v4.9.0） | 渲染結果 |
     |---|---|---|---|---|---|
     | T1s | `## 現況` 的外部狀態表有一列 ``\| 收合 \| 用 `<details>` 收合 \| 否 \| 2026-11-10 \|``（含 `<`，凍結） | 表頭開頭加一個 `\|`；在凍結列前新增一列 ``\| 補記 ` \| - \| - \| - \|`` | OK，變更列「現況」 | INVALID（2.4 以前 `## 現況` 是凍結章節） | 落單反引號和凍結列的第一個反引號配對，`<details>` 跑出 code span。之後的設計邊界、Gherkin、metadata 全部收進關閉的 details |
     | T2s | `## 現況` 的表格之後空一行，接一段 ``**備註**：用 `<details>` 收合。``（凍結） | 表頭加一個 `\|`、表尾新增含落單反引號的列、刪掉中間的空行 | OK | INVALID | 同 T1s |
     | T1s-2.4 | 同 T1s，流程契約 2.4 | 同 T1s | INVALID | INVALID | 同 T1s（2.4 下 `## 現況` 凍結，判定正確） |
     | 對照 T0 | Timeline 表格有一列凍結的 `<details>` | 表頭不動，前一列加落單反引號 | OK | OK | 不受影響（真表格各列互不影響，同 A2c） |
     | 對照 T2c | 同 T2 | 表頭不動，刪掉空行 | OK | OK | metadata 看得到（凍結段落變成表格列，見 v4.9.0 一節的 V3） |

   - 影響：
     - 這是本 issue 新引入的缺陷。2.5 讓 `## 現況` 成為記帳章節，`46e09a5` 的檢查器對 T1s、T2s 都判 INVALID，HEAD 判 OK。
     - 藏住的是 README 剩下的全部內容：設計邊界、Gherkin 驗收劇本、核准紀錄與 metadata，PASS 照樣沿用。
     - S12 的「含 `<` 的列不影響同表其他列」（`CHANGELOG.md:35`）前提是表格判定和渲染器一致。這個前提不成立時，A2 的形態就重新出現。
     - 前提：審查版本的 `## 現況` 裡已經有含 HTML 標籤的 code span（表格列或段落都可以）。
       - 這違反 `docs/AGENTS.md:139` 的撰寫規範（`## 現況` 的內容不含 `<`）。
       - 本機 680 份不重複的 issue README 中，3 份有 `## 現況`，0 份符合前提。
       - 上一輪的 A2 也是同類前提，同樣列為 MUST FIX。
     - 同樣的寫法在 Timeline、待確認事項、Gate 豁免紀錄也成立，但那三節在 v4.9.0 本來就能寫任何 HTML。依使用者決定，列在「v4.9.0 起就有的同類缺口」V1。
   - 建議：
     - 讓 `cells()` 照 GFM 計數：頭尾各最多去掉一個 `|`。表頭含 `\|` 時不當表格，照段落處理；反斜線的算法各渲染器不同，寧可多凍結。
     - reviewer 在 `<tmp>/review6/fixcheck/verify-fix.py` 試改了約 6 行：
       - T1、T1t、T1g、T1h、T1s、T2、T2n、T2s、T3 全部判 INVALID；T0、T2c 仍判 OK。
       - `test-evidence.py` 216 項全過。
       - 前五輪 179 次案例執行的判定都不變。
       - 本 repo 歷來的記帳提交判定不變：`d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306` 判 OK，`18f0e64` 判 INVALID。
       - 下游 880 張記帳章節表格中，表頭頭尾是 `||` 或含 `\|` 的是 0 張，所以下游的判定不會變。
     - 補上 T1s、T2n 形狀的負向案例。這也會抓到本輪存活的變異 M11（拿掉欄數比對），見 NICE 1。
     - 修好之後，`rule-verification-status.md:327` 的「攻擊寫法全部 INVALID」與 CHANGELOG 驗證段的測試數要跟著更新。

### SHOULD FIX

1. **縮減表頭與分隔列的欄數，凍結列多出的儲存格就不渲染，判 OK（T4）**
   - 位置：`verify-artifact.py:201-203`、`:226-227`。逐列判定只比對凍結列本身的文字，沒有比對它所在表格的欄數。
   - 實測：Timeline 有凍結列 ``\| 2026-11-04 \| 改用 `<x>` \| SENTINEL_CELL \|``，記帳提交把表頭與分隔列改成兩欄。HEAD 判 OK，兩個渲染器都丟掉第三欄（GFM 規格：多出的儲存格忽略）。`46e09a5` 也判 OK。
   - 影響：
     - 藏住的只是凍結列自己後面的儲存格，例如 Timeline 的負責人、外部狀態表的上次結果，不是驗收劇本、核准紀錄或 metadata。
     - Timeline、待確認事項、Gate 豁免紀錄從 v4.9.0 起就有（V2）。`## 現況` 的版本是 2.5 才進入記帳範圍，所以列在這裡。
   - 建議：表格裡有凍結列時，把表頭與分隔列也記成凍結內容（或記下欄數）。這也會讓 T1 一類的表頭改動直接判 INVALID，和 MUST FIX 1 的修法互補。

### NICE TO HAVE

1. **變異測試有 2 個存活**（7 個變異，5 個被抓到；腳本在 `<tmp>/review6/mut/`）：
   - M11：拿掉 `starts_table()` 的欄數比對，216 項仍全過。MUST FIX 1 的負向案例補上後就會被抓到。
   - M13：拿掉 `not block`，讓表格可以從段落中間開始，216 項仍全過。現行寫法是往多凍結的方向，沒有安全上的差別。可補一個案例：段落文字與凍結行之後不空行就接表格，判 INVALID。
   - 上一輪存活的 M6、M8 這一輪都被抓到（`test-evidence.py:502-504`）。M12（不記段落結尾）、M14（不合併空行）、M15（分隔列只看開頭的 `|`）都被抓到。
2. **`docs/AGENTS.md:139` 的「表格列不受影響」少了條件**：
   - `review-evidence.md:51` 與 `CHANGELOG.md:35` 寫的是「空行或標題之後開始、分隔列與表頭欄數相同的表格」。
   - 緊接在段落後、沒有空行的表格，GFM 照樣渲染成表格（reviewer 用兩個渲染器確認過），檢查器卻當段落：表格裡只要有凍結列，追加任何列都判需重審。
   - 本機下游有 21 張這種表格（13 份），目前都不含凍結內容，沒有實際誤判。建議在撰寫規範補「表格前空一行」。
3. **下游筆數無法照原定義重現**：
   - `CHANGELOG.md:62` 與 `implementation-plan.md:228` 寫「23 份共 34 段 269 行」與「537 行是檔尾 metadata 段落」。
   - reviewer 用 HEAD 的 `analyse()` 重掃（目前 680 份不重複）：
     - 因段落整段凍結而新凍結的行，總數 804 行。和原記載的 537＋269＝806 相符。
     - 但分類方式不同時結果不同。把含 `---` 的 Timeline 段落當成 metadata，得 422 行；其餘以粗體觸發的是 23 份、35 段、382 行。
   - 原記載沒有寫分類方式。建議補上定義，或照實際定義更正筆數。

### v4.9.0 起就有的同類缺口

以下案例 `46e09a5` 的檢查器也判 OK，依使用者決定另開 issue 處理，不阻擋本 issue。腳本在 `<tmp>/review6/adv/cases-r6.py`、`cases-r6b.py`，三個版本的輸出是 `cases-r6-out.txt`（HEAD）、`cases-r6-ac2183c-out.txt` 與 `cases-r6-main-out.txt`。

| 編號 | 寫法 | 前提 | 渲染結果 | 下游分布（本機 680 份） |
|---|---|---|---|---|
| V1 | 假表格：Timeline、待確認事項、Gate 豁免紀錄的表頭多一個 `\|`（T1、T1t），或表頭含 `\\|`（T1g），再加一列落單反引號；或在凍結段落前新增一張假表格並刪掉空行（T2、T2n） | 這三節已經有含 HTML 標籤的 code span（表格列，或前面有空行的段落） | 之後的內容全部收進關閉的 details；在 Timeline 時藏住 metadata | 表格列 6 份 7 列；非表格的段落 2 份 3 行。本 repo 自己的 README 有 2 列，但 `` `<details` `` 不是完整標籤，`` `<br>` `` 不會藏住內容。reviewer 對它實際套用 T1：檢查器判 OK，metadata 與 Gherkin 仍看得到 |
| V2 | 縮減表頭與分隔列的欄數（T4，見 SHOULD FIX 1） | 有凍結的表格列 | 凍結列多出的儲存格消失 | 凡是含 `<` 的表格列都適用 |
| V3 | 真表格與其後的凍結段落之間刪掉空行（T5、T2c） | 凍結段落的第一行不會中斷段落（例如粗體欄位、一般文字） | 凍結段落變成表格列：看得到，但版面改變。檢查器只記段落怎麼結束，沒記段落前面接什麼 | 常見（多數記帳章節的表格之後都接空行） |
| V4 | 記帳欄位的值：在 metadata 段落裡把 `**狀態**` 的值改成以落單反引號結尾（T6） | 同一段落中，`**狀態**` 之後還有凍結行含 HTML 標籤的 code span | 之後的內容收進關閉的 details | 1 份有這種形狀（完整的 style 標籤）。reviewer 對該份的暫存副本直接套用 T6，渲染沒有藏住內容，是否可利用未確認 |

- 修法方向：
  - MUST FIX 1 的欄數修正同時關掉 V1，reviewer 試改後確認過。
  - SHOULD FIX 1 的建議關掉 V2。
  - V3 要記下凍結段落前面接的是什麼（空行、標題或表格列）。
  - V4 要限制凍結段落裡記帳欄位的值，不能含反引號、`[`、`!` 這類會跨行配對的字元。
- 已登記、不重報：假表格後接 `---` 變成 setext 標題（T3），屬 CHANGELOG 已知限制「以 `|` 開頭的行後接 `---` 或 `===`」。V1 的影響比登記的大（能藏住內容，不只是變成標題），所以另外列出。

### 需決策

無。MUST FIX 1 與 SHOULD FIX 1 的修法都是多凍結，符合 TBD-3、TBD-6 的方向。v4.9.0 起就有的缺口已由使用者決定另開 issue。

## 已查核維度

### 上一輪發現的處理

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：跨行的行內語法（A1～A3） | `analyse()` 改成記帳章節以段落為單位：`block` 收集連續非空行，`flush()` 在段落含凍結項目時整段凍結並記下結尾（`verify-artifact.py:143-160`、`:181-200`、`:229-230`），表格逐列 flush（`:201-203`、`:226-227`）。A1～A3 系列 12 個案例全部改判 INVALID（`ac2183c` 都判 OK）。在 HEAD 的拋棄式 clone 對實際 README 做 A1，判 INVALID。新增測試：`test-evidence.py:571-622` | 完成；表格判定的缺口見 MUST FIX 1 |
| SHOULD FIX 1：多一個空行就判 INVALID | 凍結章節的連續空行合併成一個（`:197`）。`d0e3287` 由 INVALID 改判 OK，F7 改判 OK，測試在 `:624-629`。文件已更新：`review-evidence.md:51`、`CHANGELOG.md:34` | 完成 |
| NICE 1：存活的變異 M6、M8 | `[x]:`、`[a\](b]:` 案例（`test-evidence.py:502-504`）。reviewer 重跑這兩個變異，都被抓到 | 完成 |
| NICE 2：計數與措辭 | `implementation-plan.md:204` 改為「192 個測試中 12 個子測試失敗」；`CHANGELOG.md:51` 改為 216 項；`rule-verification-status.md:327` 改為「五輪」與「失敗的子測試」 | 完成 |
| NICE 3：docstring | `verify-artifact.py:7-11` 補上 alert、行內連結與段落凍結 | 完成 |
| NICE 4：連結文字含方括號或反斜線 | `review-evidence.md:51` 補上「連結文字不含方括號與反斜線」 | 完成 |

前五輪的案例全部重跑（`<tmp>/review6/prev/`；review2～review5 的腳本共 179 次執行，108 個不重複名稱）：
- HEAD 與 `ac2183c` 的判定只差在兩處：
  - 第五輪的 A1～A3 系列 12 個改判 INVALID。
  - F7 改判 OK。
- 判 OK 的 23 次是：C0、FP7、FP8、K6、N1～N5、X1、X7、A2c、F4～F7。
- 這和 `implementation-plan.md:227` 的記載相符。

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 S12 的 fixture，兩份的 `## 現況` 都建在 `## 概述` 之後，記帳內容 0 處含 `<`：<br>• wf28b（`7c828b9`→`346789c`）判 OK，變更含「Timeline、待確認事項、現況、現行 review」<br>• wf31（`16c5e20`→`d747bc2`）判 OK，變更含「現況、現行 review」 | 通過 |
| SCN-002 | S12 的紅燈可以重現：HEAD 的測試檔配 `ac2183c` 的檢查器，216 項、16 個失敗，失敗名稱和 `s12-red.txt` 完全相同。HEAD 216 項全過 | 有缺口：MUST FIX 1 |
| SCN-003 | 2.4、2.3 與沒有契約的案例全過。T1s 在 2.4 下判 INVALID（`## 現況` 凍結），正確 | 通過 |
| SCN-004 | 見 SCN-001 | 通過 |
| SCN-005～008 | 本輪沒有修改，沿用前幾輪的判定 | 同 review-ac2183c |

其他證據查核：
- **判準先於重跑**：
  - `expected.md:137`「第五輪審查後重跑」和修正一起在 `3fc926a`（13:57:23）提交。
  - 兩份 s12-rerun 證據都記錄 kit HEAD `3fc926a`。
  - fixture 的回合提交都比判準晚：wf28b `346789c` 13:59:08，wf31 `d747bc2` 14:01:43。結果在 `20d0847`（14:02:50）提交。
  - 結論：判準確實先於重跑。
- **記載一致性**：
  - 以下幾處都寫「各一輪、新檢查器 OK、沒有重審」，彼此一致，也沒有誇大：`implementation-plan.md` S12 列（`:37`）與 S12 證據（`:218-235`）、`workflow-results/2026-11-10.md:92-94`、`rule-verification-status.md:327`、README Timeline 最後一列。
  - 落差只有 NICE 3 的下游筆數。
  - `rule-verification-status.md:327` 的「五輪審查留下的對抗案例中攻擊寫法全部 INVALID」就字面而言正確；MUST FIX 1 是本輪新找到的寫法。
- **既有記帳提交**（HEAD 檢查器），和 `implementation-plan.md:226` 的記載相符：
  - `d0e3287` 判 OK。
  - `18f0e64` 判 INVALID：新增的 Timeline 列含 `` `<details` ``，依 TBD-6 判定。
  - `31c6bae`、`0ae68bb`、`0dd6306` 判 OK。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 跨行的行內語法（段落） | A1～A1g、A2、A2b、A3、A3b，以及實際 README 的 A1 | INVALID | 全部 INVALID |
| 表格判定與渲染器不一致 | 表頭頭尾多一個 `\|`、表頭含 `\\|` | INVALID 或照段落處理 | 檢查器當表格，判 OK；在 `## 現況` 會藏住後面的章節（MUST FIX 1），其他記帳章節見 V1 |
| 表格欄數縮減 | 表頭與分隔列減欄 | INVALID | OK，凍結列的儲存格消失（SHOULD FIX 1、V2） |
| 凍結段落的開頭 | 真表格後刪掉空行 | 依文件 | OK，凍結段落變成表格列，看得到（V3） |
| 凍結段落裡的記帳欄位值 | `**狀態**` 的值以落單反引號結尾 | INVALID | OK（V4） |
| 表格逐列判定（正當） | 凍結列後追加列、刪掉分隔列 | OK／INVALID | 正確（`test-evidence.py:611-622`） |
| 段落後補記（正當） | 空一行後補記、不空行直接接續 | OK／INVALID | 正確（`:598-609`） |
| 凍結章節的空行 | 多一個空行；刪掉唯一的空行（W1、W2） | OK／INVALID | 正確 |
| 段落結尾 | 刪掉凍結 HTML 後的空行（A3）；下一個標題之前沒有空行就追加內容 | INVALID | A3 判 INVALID。後者下游有 0 個凍結段落直接接下一個標題，沒有誤判 |
| 表格前沒有空行（正當） | 段落後不空行就接表格 | 依文件 | 檢查器當段落；`review-evidence.md` 有寫條件，`docs/AGENTS.md` 沒寫（NICE 2）。下游 0 筆實際誤判 |
| 契約閘門 | 2.4、2.5，整節新增與既有的現況 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - 以下幾處對段落凍結、表格逐列判定與空行合併的描述彼此一致：`review-evidence.md:51`、`CHANGELOG.md:34-35`、`:62`、`docs/AGENTS.md:139`、`verify-artifact.py` 的 docstring。
  - 落差只有 NICE 2 的表格條件。
  - 本輪沒有修改 `rules/` 與 `skills/*/SKILL.md`；check-kit 的雙語章節檢查通過。
- **CHANGELOG 的下游影響**：
  - `:62` 新增「與上述內容同一段落的任何行」與「先空一行」，方向正確。
  - 「既有內容不變、補記與它們空一行時不受影響」只在表格判定正確時成立（MUST FIX 1）。
  - 筆數的分類方式見 NICE 3。
- **核准範圍**：
  - 用 HEAD 的 `analyse()` 比對 `fe43877` 與 `20d0847` 的 README：凍結章節的 135 個項目完全相同。
  - 差異只有新增的 `## 現況`、`**核准 commit**`（待提交 → `fe43877`）與 `**狀態**`。Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：
  - 檢查器仍然唯讀。
  - 上一輪不需要前提的 A1 已經關掉。
  - 本 issue 新引入、需要前提的路徑還有一條：`## 現況` 的假表格（MUST FIX 1）。
  - v4.9.0 起就有的路徑見 V1～V4。
- **code-simplify**：
  - S12 用 `keep()`／`flush()` 兩個內部函式把逐行判定改成逐段判定，沒有模擬行內語法，結構清楚。
  - 表格判定只差在欄數算法；修法不需要新的結構。
- **資訊衛生**：
  - 在 `46e09a5..20d0847` 的 10300 行新增內容中搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`，以及帳號名與信箱前綴。只命中前幾輪報告裡列出這些搜尋字樣的五行，沒有實際路徑。
  - 本輪新增的 1160 行沒有任何命中。
  - 用本機 28 個專案目錄的名稱另外搜尋一次，只命中本 repo 自己的名稱。
  - 新增的 URL 只有 `example.com`／`example.invalid` 與本 repo 的 GitHub issue。
  - s12-rerun 證據的路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`。
  - 25 個提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。fixture 內 agent 提交的署名沒有進入 kit 的證據檔。
  - 本報告提到的下游掃描只寫筆數，不寫專案名稱。
- **五項檢查**（reviewer 於 2026-11-11 在 `20d0847` 自行執行，工作樹乾淨）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：216 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4、TBD-6 已解決，TBD-5 不影響本次交付，由 #4 追蹤。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs8/`）。
- 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 實際渲染。GFM 規格寫明表頭與分隔列的欄數不同時不構成表格，cmark-gfm 只去掉頭尾各一個 `|`，所以推論 MUST FIX 1 在 GitHub 上也成立。
- 下游掃描在 2026-11-11 執行，不重複的 README 是 680 份（前幾輪是 683 份），差異來自下游檔案在期間有變動。
- 對抗、變異與修正試改的腳本都在 `<tmp>/review6/`，都沒有進版控：
  - `adv/cases-r6.py`、`cases-r6b.py`，以及各版本的 `*-out.txt`
  - `prev/`（前五輪案例重跑；`out-head.txt`、`out-ac2183c.txt`、`out-fix.txt`）
  - `mut/`（變異）
  - `red/`、`red-fails.txt`（紅燈重現）
  - `fixcheck/verify-fix.py`（MUST FIX 1 的試改）
  - `realclone/`（實際 README 的 A1 與 T1）
  - `scan6.py`、`vh_instr.py`（下游掃描，只輸出筆數）
- 已揭露、不構成缺失的限制：wf32 不穩定；WF-28b、wf31 各只跑一輪；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
