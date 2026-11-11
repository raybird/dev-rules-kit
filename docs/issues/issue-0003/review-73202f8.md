# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，31 個提交、97 個檔案）。第八輪覆審，重點是上一輪 [review-4d7ba1f](review-4d7ba1f.md) 之後的修正 `853db0c..73202f8`，主要是 `1b0d862`。
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：73202f8f75f9291beed8c62cf056b51252c8c709
- Reviewed patch-id：4f25d0ffb4731d9e086a9f8d46804e6cbc71401a（2026-11-11 以 `git diff 46e09a5 73202f8 | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-73202f8.md
- 審查日期：2026-11-11
- 審查依據：
  - README `## 待確認事項` TBD-2～TBD-6 的使用者決定。
    - TBD-3：跨行 HTML 區塊在本 issue 一起收緊。
    - TBD-6：記帳章節含 `<` 的行一律凍結，不模擬 CommonMark。code span 裡的標籤名與佔位字因此判需重審，這是已接受的代價，本報告不列為缺陷。
    - TBD-5 由 GitHub #4 處理，不在本 issue 範圍。
  - README Timeline 2026-11-11 的使用者決定：v4.9.0 起就有的同類缺口另開 issue，不阻擋本 issue。判定方式和上一輪相同：同一個案例也用 `46e09a5` 的檢查器（v4.9.0）跑一次，判 OK 的就是 v4.9.0 起就有。
  - CHANGELOG 4.10.0「已知限制」已登記的項目不重報，除非影響比登記的大。已登記的有：V3、V4／V6、縮排程式碼區塊、`|` 開頭的行接 `---`／`===`、不在行首的粗體。

## 問題與風險

### MUST FIX

1. **`## 現況` 裡 HTML 區塊第 3～5 型的結束行不含 `<`，刪掉或改掉結束行後，HTML 區塊一路延伸到檔尾，藏住後面所有章節，檢查器仍判 OK**
   - 位置：`skills/review/scripts/verify-artifact.py:109-110`（`opens_comment()`）、`:174-177`、`:223-225`。
   - 原因：
     - CommonMark 的 HTML 區塊有幾型可以跨空行：
       - 第 2 型 `<!--`，到 `-->` 結束；
       - 第 3 型 `<?`，到 `?>` 結束；
       - 第 4 型 `<!` 加英文字母，到第一個 `>` 結束；
       - 第 5 型 `<![CDATA[`，到 `]]>` 結束。
     - 檢查器只追蹤第 2 型：`opens_comment()` 只看 `<!--`。
     - 第 3～5 型的開頭行含 `<`，所以會凍結。結束行如果和開頭行隔著空行，就是另一個段落；結束行不含 `<`，是可以改的記帳行。
     - 刪掉或改掉結束行後，兩個渲染器都把之後的內容當成原始 HTML 輸出，瀏覽器再把它當成 bogus comment。
   - 實測方式：
     - 在 `<tmp>` 建拋棄式 repo（沿用前幾輪的 `probe4.py`）。PASS 之後的提交只改記帳章節。
     - 渲染用 marked 17.0.5（GFM），以及 micromark 4.0.2 加 micromark-extension-gfm（table 2.1.1）。再用 parse5 7.3.0 找標記文字的位置（沿用 `render.mjs`）。
     - 同一組案例也用 `4d7ba1f`、`874992d`（`## 現況` 剛列入記帳區段）與 `46e09a5` 的檢查器各跑一次。腳本：`<tmp>/review8/adv/cases-r8.py`、`cases-r8b.py`。

     | 案例 | 審查版本的 `## 現況` | 記帳提交 | HEAD | `46e09a5`（v4.9.0） | 渲染結果（兩個渲染器相同） |
     |---|---|---|---|---|---|
     | Z2 | 外部狀態表之後空一行，接 `<?x 舊說明`、空行、`?>` | 刪掉 `?>`，保留空行 | OK | INVALID | 設計邊界、Gherkin 驗收劇本、核准紀錄、metadata 全部變成註解，看不到 |
     | Z3 | 同上，第 4 型（`<!X 舊說明` … `>`） | 刪掉 `>` | OK | INVALID | 同 Z2 |
     | Z4 | 同上，第 5 型（`<![CDATA[ 舊說明` … `]]>`） | 刪掉 `]]>` | OK | INVALID | 同 Z2 |
     | Z2r | `<?x 舊說明`、空行，接一張外部狀態表，其中一列含 `?>` | 把那一列的 `?>` 刪掉 | OK | INVALID | 同 Z2 |
     | Z2-2.4～Z4-2.4 | 同 Z2～Z4，流程契約 2.4 | 同上 | INVALID | INVALID | 同 Z2（2.4 下 `## 現況` 是凍結章節，判定正確） |
     | 對照 Z2c | `<?x 舊說明` 與 `?>` 同段落 | 刪掉 `?>` | INVALID | INVALID | 同 Z2（段落整段凍結，判定正確） |

   - 影響：
     - 這是本 issue 新引入的缺陷：
       - 2.5 讓 `## 現況` 成為記帳章節，`46e09a5` 對 Z2～Z4 判 INVALID，HEAD 判 OK。
       - `874992d` 與 `4d7ba1f` 也判 OK。所以從 `## 現況` 列入記帳區段起就存在，前七輪都沒有發現，不是 S14 引入的。
     - 藏住的是 README 剩下的全部內容：設計邊界、Gherkin 驗收劇本、核准紀錄與 metadata。PASS 照樣沿用。
     - 前提：審查版本的 `## 現況` 有一行以 `<?`、`<!` 加英文字母或 `<![CDATA[` 開頭，而且結束字串在空行之後的另一段。
       - 這違反 `docs/AGENTS.md:139` 的撰寫規範（`## 現況` 的內容不含 `<`）。前提的性質和上一輪 MUST FIX 1（U1）相同。
       - 本機 687 份不重複的 issue README 中，3 份有 `## 現況`。記帳章節裡沒有任何一行以這三種寫法開頭，行中出現的也是 0 行（`<tmp>/review8/scan_html35.py`）。
     - 同樣的寫法在 Timeline、待確認事項、Gate 豁免紀錄也成立，但 v4.9.0 就判 OK，列在「v4.9.0 起就有的同類缺口」V7。
   - 建議：
     - 把 `opens_comment()` 推廣成「回傳尚未關閉的結束字串」：
       - 行內任何位置出現 `<!--`、`<?`、`<![CDATA[`、`<!` 加英文字母，而同一行後面沒有對應的 `-->`、`?>`、`]]>`、`>`，就從這一行凍結到含結束字串的那一行。
       - 這和現行 `<!--` 的處理方式相同，不看行首位置，也不模擬 CommonMark，符合 TBD-6。
     - reviewer 在 `<tmp>/review8/verify-fix.py` 試改約 20 行（`unclosed()` 取代 `opens_comment()`；`comment` 改存結束字串）。結果：
       - Z2～Z4、Z2r、Z2m（把 `?>` 改成 `? >`），以及 Timeline 版本 Z2t～Z4t 全部判 INVALID。
       - `test-evidence.py` 228 項全過。
       - 前七輪 206 次案例執行的判定都和 HEAD 相同。
       - 本 repo 歷來的記帳提交判定不變。S14 兩個重跑 fixture 的記帳提交仍判 OK。
       - 下游 687 份 README 的 `analyse()` 結果 0 份改變。
     - 補上 `<?`、`<!X`、`<![CDATA[` 結束行在另一段的負向案例。
     - `review-evidence.md:51` 與 `CHANGELOG.md:31` 的「同一行沒有關閉的 `<!--` 到 `-->` 為止整段凍結」要跟著改。

### SHOULD FIX

無。

### NICE TO HAVE

1. **變異測試有 1 個存活，但不影響安全**（腳本在 `<tmp>/review8/mut/`）：
   - 存活的是 M24：`cells()` 不要求表頭以 `|` 結尾，228 項仍全過。
     - 兩個渲染器也都把 `| a b` 加 `|-|`、`| a | bc` 加 `|-|-|` 當表格，所以沒有安全上的差別。
     - 可以補一個「表頭省略結尾 `|`」的案例，讓白名單的每個條件都有測試擋住。
   - 被抓到的有 M19（表頭項目不含分隔列）、M21（拿掉反斜線條件）、M22（拿掉空白字元條件）、M23（拿掉空格子條件），各 2 個失敗。CurrentStateTests 繼承 BookkeepingTests，所以每個變異在兩個類別各失敗一次。`implementation-plan.md` 寫「M19 有 1 個失敗」，是照單一類別計算，和上一輪的算法一致。
   - M25（分隔列接受 tab）與 M26（拿掉 `len(line) < 3`）是等價變異：`cells()` 已經擋掉 tab，長度不足的寫法也已經回傳 None。
2. **`rule-verification-status.md:327` 寫「除 #5 登記的 v4.9.0 起就有的寫法外，攻擊寫法全部 INVALID」，少列了 CHANGELOG 已知限制的寫法**
   - HEAD 判 OK 的攻擊寫法除了 #5 的 V3、V4、V6，還有 N1、N1c（`|` 開頭的行接 `===`）與 N2、N3（不在行首的粗體）。
   - 這幾項登記在 `CHANGELOG.md:36` 的已知限制，不在 #5。
   - 建議改為「除 #5 與 CHANGELOG 已知限制登記的寫法外」。
3. **`implementation-plan.md:266` 寫「第七輪 11 個案例」，少算了 W1**：
   - 11 是 `cases-r7*.py` 三支腳本的案例數。
   - 第七輪報告另有 `w1.py` 的 W1（V6）。reviewer 重跑仍判 OK，和登記的 V6 一致。

### v4.9.0 起就有的同類缺口

以下案例 `46e09a5` 的檢查器也判 OK。依使用者決定另開 issue 處理，不阻擋本 issue。

| 編號 | 寫法 | 前提 | 渲染結果 | 下游分布（本機 687 份） |
|---|---|---|---|---|
| V7（MUST FIX 1 的 v4.9.0 版本） | 在 Timeline、待確認事項或 Gate 豁免紀錄，刪掉 HTML 區塊第 3～5 型的結束行（Z2t、Z3t、Z4t） | 該節有一行以 `<?`、`<!` 加英文字母或 `<![CDATA[` 開頭，結束字串在空行之後的另一段 | 之後的內容變成註解；在 Timeline 時藏住 metadata | 0 行 |

- 修法：MUST FIX 1 的修法一併關掉 V7（reviewer 試改後確認過）。修好後不必補進 #5。
- 已登記、不重報：
  - Z1、Z1u（`## 現況` 的外部狀態表與後面的凍結段落之間刪掉空行）是 V3 在 `## 現況` 的版本。`46e09a5` 也判 OK，因為 v4.9.0 不比對凍結章節的空行。
    - 渲染後內容看得到，和登記的影響相同。
    - reviewer 試過讓跨行 code span 拆成兩列，使 `<details>` 脫出。`</td>` 會關掉它，藏不住表格之後的內容。
  - Z5（縮排程式碼區塊前新增清單項）屬已登記的縮排程式碼區塊限制。`<details>` 被 `</li>` 關掉，看得到後面的章節。
  - V4、V6（記帳欄位的值以落單反引號結尾）已在 #5 與 `CHANGELOG.md:36`。W2、W1 重跑仍判 OK，和登記一致。

### 需決策

無。MUST FIX 1 的修法是多凍結，符合 TBD-3（跨行 HTML 區塊在本 issue 一起收緊）與 TBD-6（不模擬 CommonMark）的方向。V7 由同一個修法關掉。

## 已查核維度

### 上一輪發現的處理

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：表頭只有一個 `\|` 的假表格 | `cells()` 改成白名單（`verify-artifact.py:124-139`）：頭尾都是 `\|`、每格有空格以外的內容、空白只有一般空格、沒有反斜線；`DELIMITER_ROW` 不再接受 tab。<br>• U1、U1b、U1c、U2、U3、U4、U5、U6 改判 INVALID，U1d 仍判 OK（`4d7ba1f` 這八個都判 OK）<br>• 新增測試：`test-evidence.py:661-671`<br>• 文件已同步：`review-evidence.md:51`、`CHANGELOG.md:35`、`docs/AGENTS.md:139`<br>• #5 的留言已更正正文「V1 已修正」的說法 | 完成 |
| SHOULD FIX 1：驗證狀態誇大 | `rule-verification-status.md:327`：<br>• 補上「除 #5 登記的 v4.9.0 起就有的寫法外」<br>• 683 份（S10）與 686 份（S14）的掃描分開寫 | 完成；措辭還能再精確（NICE 2） |
| SHOULD FIX 2：下游筆數無法重現 | 提交 `evidence/scan_downstream.py`，分類方式寫在腳本開頭；CHANGELOG、計畫與驗證狀態改用它的輸出 | 完成，可重現（見下方「其他證據查核」） |
| NICE 1：M19 存活 | `test-evidence.py:630` 補上「分隔列對齊改變」的案例。reviewer 重跑 M19，2 個失敗 | 完成 |
| NICE 2：表頭凍結沒寫進撰寫規範 | `docs/AGENTS.md:139` 補「表格裡有這些寫法的列時，表頭與分隔列也不改」 | 完成 |
| NICE 3：第六輪案例數 | `implementation-plan.md:247` 改為 16 個 | 完成 |
| V5、V6 | V5 由白名單關掉，U2、U3 判 INVALID；V6 補進 #5 的留言 | 完成 |

前七輪的案例全部重跑（`<tmp>/review8/prev/`）：
- 範圍：review2～review7 的腳本共 206 次執行（前六輪 195 次，第七輪 11 次），另外單獨重跑 `w1.py`。
- HEAD 與 `4d7ba1f` 只差在第七輪的 U1、U1b、U1c、U2、U3、U4、U5、U6，都改判 INVALID。
- HEAD 判 OK 的 30 次：
  - 上一輪列出的 28 次，沒有變化。
  - 第七輪的對照組 U1d，以及已登記的 W2（V6）。
- W1（V6）仍判 OK，和登記的一致。

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 S14 的 fixture，兩份的 `## 現況` 都建在 `## 概述` 之後（第 7 行）：<br>• wf28b（`9699e00`→`abbf17a`）判 OK，變更含 Timeline、待確認事項、現況、現行 review<br>• wf31（`ea69a09`→`07e7043`）判 OK，變更含現況、現行 review<br>兩份用 MUST FIX 1 的試改版也判 OK | 通過 |
| SCN-002 | S14 的紅燈可以重現：HEAD 的測試檔配 `4d7ba1f` 的檢查器跑 228 項，8 個子測試失敗，失敗名稱和 `s14-red.txt` 完全相同。HEAD 228 項全過 | 有缺口：MUST FIX 1 |
| SCN-003 | 2.4 的案例全過；Z2-2.4～Z4-2.4、U1-2.4 在 2.4 下都判 INVALID（`## 現況` 凍結），正確 | 通過 |
| SCN-004 | 見 SCN-001 | 通過 |
| SCN-005～008 | 本輪沒有修改，沿用前幾輪的判定 | 同 review-4d7ba1f |

其他證據查核：
- **判準先於重跑**：
  - `expected.md:145`「第七輪審查後重跑」和修正一起在 `1b0d862` 提交（15:08:11）。
  - 兩份 s14-rerun 證據都記錄 kit HEAD `1b0d862`。
  - fixture 的回合提交都比判準晚：wf28b `abbf17a` 15:09:45，wf31 `07e7043` 15:10:58。
  - 結果在 `73202f8`（15:12:06）提交。
  - 結論：判準確實先於重跑。
- **記載一致性**：
  - 以下幾處都寫「各一輪、新檢查器 OK、沒有重審」，彼此一致，和 fixture 的實際提交相符：
    - `implementation-plan.md` S14 列（`:39`）與 S14 證據（`:258-276`）
    - `workflow-results/2026-11-10.md:100-102`
    - README Timeline 最後一列
  - 誇大或少算的地方見 NICE 2、3。
- **差異掃描**（`<tmp>/review8/fuzz/`）：
  - 用 review7 的三個產生器重跑：檢查器當成表格的 814 組表頭與分隔列、7174 列、44～51 組表頭配對，兩個渲染器都當表格。和 `implementation-plan.md:267` 的記載相同。
  - reviewer 另寫一個產生器 `fz1.py`。字元集涵蓋行內語法符號、HTML 實體、組合字元、零寬連接字、Hangul filler、全形 `｜`、emoji、`<` 等。
    - 三個種子各約 42600 組白名單承認的表頭與分隔列，兩個渲染器都當表格，0 筆不一致。
  - `ctx.py`：在 24 種前文之後放一張範本表格。
    - 檢查器當表格、渲染器不當表格的，只有前文是 HTML 區塊第 1 型（`<pre>`、`<script>`、`<style>`、`<textarea>`）或第 3～5 型的情況。
    - 第 1 型的結束行含 `<`，會凍結，改不掉。
    - 第 3～5 型就是 MUST FIX 1。
- **下游筆數重現**：
  - 用 `scan_downstream.py` 掃描 review7 留下的 README 清單（2026-11-11），得到：
    - 不重複的 README 687 份；
    - 同段落凍結的行：檔尾 metadata 段落 423 行，其他 23 份 35 段 382 行；
    - 含凍結列的表格 31 份 32 張（凍結列 40 列）；
    - 不合範本形狀的表格 0 張。
  - 和記載（686 份、422 行，其餘相同）只差一份 README、一行。差的是本 issue README 在 `73202f8` 改過、成為新的不重複內容。
  - `4d7ba1f` 與 HEAD 的 `analyse()` 對這 687 份的結果完全相同，符合「S13 與 S14 的結果相同」。
  - 35 段依章節分：Gate 豁免紀錄 16 段、Timeline 12 段、待確認事項 7 段，觸發凍結的都是粗體行，符合 CHANGELOG 的描述。
- **既有記帳提交**（HEAD 檢查器），和 `implementation-plan.md:268` 的記載相符：
  - `d0e3287`、`31c6bae`、`0ae68bb`、`0dd6306`、`b4e8708`、`853db0c` 判 OK。
  - `18f0e64` 照 TBD-6 判 INVALID。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 假表格：表頭只有 `\|`、空格子、tab、U+2028、NBSP | U1～U6 | INVALID | 全部 INVALID |
| 白名單承認、渲染器不當表格的表頭 | 差異掃描約 12.9 萬組 | 0 筆 | 0 筆 |
| 範本表格前文是跨空行的 HTML 區塊 | `ctx.py` 24 種前文 | 依渲染器 | 第 1 型的結束行凍結，安全；第 3～5 型不一致（MUST FIX 1） |
| HTML 區塊第 3～5 型的結束行在另一段 | Z2～Z4、Z2r、Z2m | INVALID | `## 現況` 判 OK（MUST FIX 1）；其他記帳章節判 OK（V7） |
| 真表格後刪空行 | Z1、Z1u、T5、T2c | 依文件 | OK，看得到（V3，已登記） |
| 縮排程式碼區塊 | Z5 | 依文件 | OK，看得到（已登記） |
| 記帳欄位的值 | W1、W2、T6 | INVALID | OK（V4、V6，已登記） |
| 凍結列前後補列（正當） | T0、Z1c、`test-evidence.py:611-622` | OK | OK |
| 正當記帳被誤判 INVALID | 下游 687 份：S13 與 S14 的 `analyse()` 結果 0 份不同；不合範本形狀的表格 0 張 | 只有文件寫明的情況會多重審 | 沒有找到文件沒寫的誤判。白名單排除的寫法（省略頭尾 `\|`、空格子、全形空格、反斜線）都寫在 `review-evidence.md:51` 與 `CHANGELOG.md:35`；`docs/AGENTS.md:139` 只寫「頭尾都是 `\|`」，但照範本寫就符合 |
| 契約閘門 | 2.4、2.5 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - 以下幾處對表格白名單、表頭凍結與段落凍結的描述彼此一致：
    - `review-evidence.md:51`
    - `CHANGELOG.md:35-36`
    - `docs/AGENTS.md:139`
    - `verify-artifact.py` 的 docstring 與 `cells()` 註解
  - `docs/AGENTS.md:139` 是撰寫規範，只寫「頭尾都是 `|`」，完整條件在 `review-evidence.md`，分工合理。
  - 本輪沒有修改 `rules/` 與 `skills/*/SKILL.md`。check-kit 的雙語章節檢查通過。
- **CHANGELOG 的下游影響與已知限制**：
  - `:35` 的白名單描述和程式一致。
  - `:36` 把 V3 與 V4／V6 合寫成兩類，和 #5 的登記一致；V5 已關閉，沒有寫進已知限制，正確。
  - `:62` 的筆數可以用提交的腳本重現。
  - `:31` 只寫 `<!--`，MUST FIX 1 修好後要補上。
- **核准範圍**：
  - 用 HEAD 的 `analyse()` 比對 `fe43877` 與 `73202f8` 的 README：記帳章節以外的 135 個凍結項目完全相同。
  - 差異只有：新增的 `## 現況`、`**核准 commit**`（待提交 → `fe43877`）、`**狀態**`（待實作 → 實作中），以及待確認事項與 Timeline 新增的列。
  - Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：
  - 檢查器仍然唯讀。
  - 上一輪的 U1～U6 已經關掉。
  - 本 issue 新引入、需要前提的路徑還有一條：`## 現況` 的 HTML 區塊第 3～5 型（MUST FIX 1）。
- **code-simplify**：
  - `cells()` 的白名單寫成一個條件式加一行回傳，比前兩輪逐一追渲染器算法清楚。
  - `starts_table()` 拿掉多餘的 `startswith('|')`，`cells()` 已經檢查過。
  - MUST FIX 1 的修法用一個函式取代 `opens_comment()`，不需要新結構。
- **資訊衛生**：
  - 本輪新增 1025 行、全範圍新增 12775 行。搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`、`scratchpad`、`~/`，以及帳號名與信箱前綴。
    - 本輪新增內容沒有任何命中。
    - 全範圍只命中三類：已遮蔽的 `<scratchpad>`、`<fixtures>` 佔位字；fixture 證據裡 agent 指令中的 `~/.claude/skills`、`/tmp/rv3101` 這類通用路徑；以及前幾輪報告裡列出搜尋字樣的行。沒有本機實際路徑。
  - 用本機 115 個專案目錄的名稱另外搜尋本輪新增內容，只命中本 repo 自己的名稱。
  - 本輪新增的 URL 只有本 repo 的 #5 與 `https://…` 佔位字。
  - s14-rerun 證據的路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`。
  - GitHub #5 的正文與留言都沒有本機路徑或其他專案的名稱。留言說 V5「由第八輪覆審確認」，本輪已確認。
  - 31 個提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。
  - 本報告提到的下游掃描只寫筆數，不寫專案名稱。
- **五項檢查**（reviewer 於 2026-11-11 在 `73202f8` 自行執行，執行前後工作樹都是乾淨的）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：228 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4、TBD-6 已解決，TBD-5 不影響本次交付，由 #4 追蹤。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs10/`）。
- 渲染限制：
  - 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 或 cmark-gfm 實際渲染。
  - Z2～Z4 在 GitHub 上的結果是推論：HTML 區塊第 3～5 型是 CommonMark 規格，兩個渲染器結果相同。GitHub 會過濾部分原始 HTML，實際藏住的範圍可能不同。
- 差異掃描是以有限字元集隨機產生，不是窮舉。
- 下游掃描在 2026-11-11 執行，清單沿用 review7 的 README 路徑，去重後是 687 份。
- 對抗、變異、差異掃描與修正試改的腳本都在 `<tmp>/review8/`，都沒有進版控：
  - `adv/`（`cases-r8.py`、`cases-r8b.py`）
  - `prev/`（前七輪案例重跑；`out-head.txt`、`out-4d7ba1f.txt`、`out-main.txt`、`out-fix.txt`）
  - `fuzz/`（`fz1.py`、`ctx.py`，以及 review7 的三個產生器）
  - `mut/`（變異）
  - `fixtree/`、`verify-fix.py`（MUST FIX 1 的試改）
  - `redtree/`、`red.txt`（紅燈重現）
  - `scan_html35.py`、`scan_sec.py`、`cmp_fix.py`（下游掃描，只輸出筆數）
- 已揭露、不構成缺失的限制：wf32 不穩定；WF-28b、wf31 各只跑一輪；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
