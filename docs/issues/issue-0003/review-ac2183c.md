# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，22 個提交、81 個檔案）；第五輪覆審，重點是上一輪 [review-4e0177a](review-4e0177a.md) 之後的修正 `0ae68bb..ac2183c`
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：ac2183cc052083def125d79d0d0679b91d3e9eca
- Reviewed patch-id：043b7ec6f71017f3e795922f4f0e858ccf59e879（2026-11-11 以 `git diff 46e09a5 ac2183c | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-ac2183c.md
- 審查日期：2026-11-11
- 審查依據：README `## 待確認事項` TBD-2～TBD-6 的使用者決定。本報告照這些決定審查，不重新討論方向。TBD-6 決定記帳章節含 `<` 的行一律凍結，code span 裡的標籤名與佔位字因此判需重審，這是已接受的代價，本報告不列為缺陷。TBD-5 由 GitHub #4 處理，不在本 issue 範圍。CHANGELOG 4.10.0「已知限制」已登記的項目不重報。

## 問題與風險

### MUST FIX

1. **記帳章節裡，凍結行的上下文沒有列入比對。行內語法可以跨行，在凍結行的同一段落加一行，就能藏住檔尾 metadata，判 OK**
   - 位置：`skills/review/scripts/verify-artifact.py:122-193`（`analyse()`）。
     - 記帳章節的一般行只依章節收進 `sections[...]`，比對時只看「內容有沒有變」，不看它和凍結行是否在同一個段落。
     - 記帳章節的空行也不比對（`:185-188`）。
     - CommonMark 的 code span、連結 title、圖片 alt、連結文字都可以跨行，只要中間沒有空行。凍結行的渲染因此取決於同段落裡的記帳行。
   - 實測方式：在 `<tmp>` 建拋棄式 repo（沿用上一輪的 `probe4.py`），PASS 之後的提交新增報告並改寫 README。用 marked 17.0.5（GFM）與 micromark 4.0.2 加 micromark-extension-gfm 3.0.0 渲染，再用 parse5 7.3.0 找標記文字的位置（`render.mjs`，沿用上一輪）。下表兩個渲染器的結果都相同。

     | 案例 | 寫法（記帳提交只動記帳章節，都不含 `<`） | 檢查器 | 渲染結果 |
     |---|---|---|---|
     | A1 | Timeline 的 `---` 之後插入 `[補記](https://example.com/x "`，檔尾加一行 `")` | OK，變更列「Timeline」 | 檔尾 `**建立日期**`、`**分級**`、`**狀態**` 都變成連結的 title 屬性，頁面上看不到 |
     | A1b、A1c | 開頭不是 `[` 的 `補記 [a](https://example.com/x "`，或用括號當 title | OK | 同 A1。A1b 從 v4.9.0 起就成立（`46e09a5` 的檢查器也判 OK） |
     | A1d | `補記 ![` … `](https://example.com/a.png)` | OK | metadata 變成圖片的 alt，頁面上看不到 |
     | A1e、A1f | 用落單的反引號，或 `[` … `](網址)` 包住 metadata | OK | metadata 變成 code 或連結文字，還看得到，但粗體欄位的樣子消失 |
     | A1-2.4、A1g | 流程契約 2.4；或刪掉 `---`，空一行後再開 title | OK | 同 A1 |
     | A1（實際 README） | 在 `ac2183c` 的拋棄式 clone 對 `docs/issues/issue-0003/README.md` 做 A1 | OK，變更只列「新增報告、Timeline」 | `**分級**: Medium …` 與 `**狀態**: 實作中` 都不在頁面文字裡 |
     | A2 | 審查版本的 `## 現況` 有一行段落文字 ``用 `<details>` 收合舊說明。``（含 `<`，所以凍結）；記帳提交在它上一行補一個落單的反引號 | OK，變更列「現況」 | 反引號改成和凍結行的第一個反引號配對，`<details>` 跑出 code span 變成原始 HTML。之後的設計邊界、Gherkin、metadata 全部收進關閉的 details |
     | A3 | 審查版本的 `## 現況` 有一行 `<div id="x"></div>` 並接空行；記帳提交刪掉這個空行 | OK，變更只列「新增報告」 | 下一節的 `## 設計邊界` 落進 HTML 區塊，不再是標題 |
     | A3b | 同上，再刪掉中間的記帳行，讓含 `` `<details>` `` 的凍結行緊接在 HTML 區塊後 | OK | 同 A2，之後的內容全部收進 details |
     | 對照 A2c | 同樣的反引號寫在表格的另一列 | OK | 不受影響。表格各列的行內語法互不影響 |

   - 影響：
     - A1 不需要任何前提，每份照範本寫的 README 都適用：metadata 在 Timeline 的 `---` 之後，而 Timeline 是記帳章節。本機 683 份不重複的 issue README 中，370 份是這種結構。
     - `review-evidence.md:51` 明寫「寫在記帳章節底下的 `**分級**`、`**風險**`」屬凍結內容，A1 正好把它藏住，PASS 照樣沿用。這就是 README「風險與首要驗證」列為最大風險的失敗形態。
     - A2、A3 要審查版本的記帳章節裡已經有特定的行：A2 要非表格的 code span 標籤，本機有 2 份共 3 行；A3 要行首 `<`，本機 0 份。不過它們一旦成立，會藏住整份 README 的其餘部分。
     - TBD-6 接受的代價是誤判 INVALID。這幾個案例都是放行，不在 TBD-6 的範圍，也不在 CHANGELOG 的已知限制裡。
     - A1b 從 v4.9.0 起就成立，和上一輪的 MUST FIX 1 一樣。依 TBD-3「本 issue 收緊所有記帳判定」，仍列為本 issue 的 MUST FIX。
   - 建議：
     - 記帳章節裡，凍結行（表格列除外）所在的連續非空行一起凍結，並記下這段怎麼結束（空行、標題、分隔線或檔尾）。
     - 以 `|` 開頭的行與 `---` 這類分隔線當作段落邊界，追加 Timeline 列才不會受影響。
     - reviewer 在 `<tmp>/review5/fixcheck/` 的副本試改了約 25 行：
       - `test-evidence.py` 192 項全過；A1～A3 全部判 INVALID；A2c 仍判 OK。
       - 前四輪 111 個案例的判定都不變，包括 FP7、FP8、N4 系列這些正當寫法。
       - wf28b（`29a6c9f`）、wf31（`a0c67b4`）、`31c6bae`、`0ae68bb` 仍判 OK。
     - 代價：和凍結行連在一起的清單項會整段凍結，本機只有 2 份共 5 行（非表格的記帳行含 `<`）。這符合 TBD-6「寧可多凍結」的方向。
     - 補上 A1、A2、A3 的負向案例。修好之後，`rule-verification-status.md:327` 的「攻擊寫法全部 INVALID」與 CHANGELOG 的驗證段要跟著更新。

### SHOULD FIX

1. **凍結章節的空行改成逐行比對之後，整節新增 `## 現況` 時多一個空行就會判 INVALID。kit 自己歷史上的記帳提交 `d0e3287`，上一輪判 OK，這一輪判 INVALID**
   - 位置：`verify-artifact.py:185-187`。凍結章節的每個空行都記成凍結內容，連續空行的數量也要相同。
   - 實測：
     - `--reviewed 5c2ca52 --head d0e3287` 判 INVALID，訊息是「被審查版本為章節「文件清單」的「## 文件清單」，目前為章節「概述」的空行」。
     - 原因是 `d0e3287` 新增 `## 現況` 時，`## 概述` 結尾多了一個空行（兩個連續空行），渲染結果完全相同。
     - review-4e0177a 記載這個提交判 OK，S11 的證據沒有重新核對既有的記帳提交，所以沒有發現這個變化。
     - F7：凍結段落後多一個空行，判 INVALID。
   - 影響：
     - 整節新增 `## 現況` 是 review 技能步驟 5 要 agent 做的事。目前已知的 3 次整節新增中（`d0e3287`、wf28b、wf31），有 1 次多了空行。這種寫法會讓 PASS 失效，造成多一輪重審。
     - `review-evidence.md:51` 寫了「其他章節（含空行…）」，但 CHANGELOG `:61` 的下游影響清單沒有列出「渲染相同的空行增減也要重審」。這是 v4.9.0 以來的行為變更。
   - 建議（擇一）：
     - 比對前把連續空行合併成一個。多個空行和一個空行在 CommonMark 的渲染相同（fence 內另外凍結），W1、W2 刪掉唯一的空行仍判 INVALID。
     - 或者保留現行判定，在 CHANGELOG 下游影響與 review 技能步驟 5 寫明：整節新增 `## 現況` 時不要增減前一節的空行。

### NICE TO HAVE

1. **變異測試有 2 個存活，對應的實作是正確的，只是缺案例**（11 個變異，5 個被抓到；腳本在 `<tmp>/review5/mut/`）：
   - M6：連結例外的標籤允許 `\`。缺 `[a\](b]: 網址` 這種案例：標籤裡跳脫的 `]` 讓它成為參照定義。
   - M8：任務清單例外不要求 `]` 後接空白。缺 `[x]: 網址` 這種案例。
   - HEAD 對這兩種都判 INVALID（Y1、Y2），補上負向案例即可。
   - 其他存活的變異沒有安全上的差別：
     - M1（splitlines）：凍結章節的空行比對已經能擋下。
     - M3、M9（closes／setext 改用 `strip()`）：都是往更嚴的方向誤判。
     - M10：已登記的已知限制。
   - 上一輪存活的 M2、M6、M7，這一輪都被抓到。
2. **計數與措辭和證據不符**：
   - `implementation-plan.md:203` 寫「181 個測試 12 個失敗」，但 `evidence/s11-red.txt` 是 192 個測試、12 個失敗。reviewer 重現紅燈也是 192 個、失敗的名稱相同。
   - `CHANGELOG.md:50` 仍寫「176 項」，目前是 192 項。
   - `rule-verification-status.md:327`：
     - 「三輪審查留下的對抗案例」應為四輪。
     - 「S11 12 個新案例都先紅後綠」：12 是失敗的子測試數；3 個防護案例與綠燈後補的 2 個案例沒有經過紅燈（plan 有揭露）。
3. `verify-artifact.py:7-10` 的 docstring 仍寫「以 `[` 開頭的行（連結參照定義；任務清單除外）」，沒有提到 alert、行內連結與空行。這段 docstring 也是 `--help` 的說明文字。
4. 連結文字含 `[`、`]` 或 `\` 時，不符合連結例外，判 INVALID，例如 `- [[WIP] 修正](網址)`（F2、F3）。`review-evidence.md:51` 的「同一行就關閉、後接 `(` 的連結」沒有說到這一點。這種寫法很少見，補一句說明即可。

### 需決策

無。MUST FIX 1 的建議修法是「多凍結」，符合 TBD-3 與 TBD-6 的方向。SHOULD FIX 1 的兩種修法都不改變已決定的方向。

## 已查核維度

### 上一輪發現的處理

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：分行與行尾空白（U1～U6） | `LINE_END`、`BLANK`（`verify-artifact.py:35-36`），`analyse()` 以 `LINE_END.split`、`rstrip(BLANK)` 處理（`:128-129`），`closes()` 改為 `strip(BLANK)`（`:98`）。重跑 U1a～U6 全部判 INVALID。新增測試 `test-evidence.py:535-547`，涵蓋 U2、U3、U4 的形狀 | 完成 |
| SHOULD FIX 1：凍結章節的空行（W1、W2） | `:185-187` 把凍結章節的空行記成凍結內容。W1、W2 判 INVALID，測試在 `:549-554` | 完成；附帶的誤判見本輪 SHOULD FIX 1 |
| SHOULD FIX 2：容器內 `[` 開頭的寫法誤判 | 選了可選的修法：`LINK_DEFINITION`（`:33`）放行任務清單、獨佔一行的 alert，以及同一行就關閉、後接 `(` 的連結。N4、N4b、N4c 判 OK，測試在 `:564-568`；`[x foo`／`]:`、`[!NOTE]:` 判 INVALID（`:496-497`）。文件已更新：`review-evidence.md:51`、`CHANGELOG.md:33`、`:61`、`docs/AGENTS.md:139`。reviewer 重掃 683 份 README，新規則下以 `[` 開頭而凍結的記帳行是 0，和 plan 的記載相符 | 完成；測試缺口見 NICE 1，說明缺口見 NICE 4 |
| NICE 1：`\|` 接 `===` 與仿粗體 | CHANGELOG `:35` 的已知限制已改為「以 `\|` 開頭的行後接 `---` 或 `===`」，並登記 `_**風險**_：`、`&nbsp;**風險**：` 兩種寫法 | 完成（登記） |
| NICE 2：沒用到的常數 | `SETEXT`、`NOT_PARAGRAPH` 已移除 | 完成 |
| NICE 3：存活的變異 | M2：補了 `- <br>`（`:494`）。M6：補了 `> [spec]:`（`:495`）。M7：`test_comment_reopened_after_close_stays_frozen`（`:556`）照建議的形狀寫。reviewer 重跑這三個變異，都被抓到。M4 依已知限制不補，plan `:208` 有寫理由 | 完成 |

前四輪的案例全部重跑（`<tmp>/review5/prev/`，共 111 個）：
- 96 個判 INVALID。
- 判 OK 的 15 個是：C0、FP7、FP8、K6、N1、N1b、N1c、N2、N3、N4、N4b、N4c、N5、X1、X7。
- 這和 `implementation-plan.md:205` 的記載相符。

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 S11 的 fixture：wf28b（`fb8d0dd`→`29a6c9f`）判 OK，變更含「Timeline、待確認事項、現況、現行 review」；wf31（`8efe0c3`→`a0c67b4`）判 OK，變更含「現況、現行 review」。兩份的 `## 現況` 都建在 `## 概述` 之後，記帳內容 0 處含 `<` | 通過 |
| SCN-002 | S11 的紅燈可以重現：HEAD 的測試檔配 `0ae68bb` 的檢查器，192 項、12 個失敗，失敗名稱和 `s11-red.txt` 完全相同。HEAD 192 項全過 | 有缺口：MUST FIX 1 |
| SCN-003 | 2.4、2.3 與沒有契約的案例全過。A1-2.4 在 2.4 下同樣判 OK | 同樣受 MUST FIX 1 影響 |
| SCN-004 | 見 SCN-001 | 通過 |
| SCN-005～008 | 本輪沒有修改，沿用上一輪的判定 | 同 review-4e0177a |

其他證據查核：
- **判準先於重跑**：
  - `expected.md:133`「第四輪審查後重跑」和修正一起在 `df2a444`（13:04:04）提交。
  - 兩份 s11-rerun 證據都記錄 kit HEAD `df2a444`，這個 SHA 不可能事先得知。
  - fixture 的回合提交都比判準晚：wf28b `29a6c9f` 13:05:54，wf31 `a0c67b4` 13:07:41。結果在 `ac2183c`（13:08:58）提交。
  - 結論：判準確實先於重跑。
- **記載一致性**：
  - 以下幾處都寫「各一輪、新檢查器 OK、沒有重審」，彼此一致，也沒有誇大：`implementation-plan.md` S11 列與 S11 證據、`workflow-results/2026-11-10.md:88-90`、`rule-verification-status.md:327`、README Timeline 最後一列。
  - 只有 NICE 2 的計數不符。
  - s11-rerun 證據只收錄 agent 的最終輸出，沒有收錄維護者事後執行檢查器的輸出。reviewer 自己重跑，結果相符。
- **既有記帳提交**（HEAD 檢查器）：
  - `31c6bae`、`0ae68bb` 判 OK。
  - `18f0e64` 判 INVALID，和上一輪相同。
  - `d0e3287` 由 OK 變成 INVALID（SHOULD FIX 1）。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 分行與行尾正規化 | U1～U6（NBSP、U+3000、U+0085、U+2028、`\f`、`\v`、`\x1c`） | INVALID | 全部 INVALID |
| 凍結章節的空行 | W1、W2 | INVALID | INVALID |
| 凍結章節的空行（正當） | 多一個空行、整節新增現況時多一個空行 | OK 或文件有說明 | INVALID，下游說明沒有寫（SHOULD FIX 1） |
| 跨行的行內語法 | 連結 title、圖片 alt、code span、連結文字跨過凍結的 metadata | INVALID | OK，metadata 被藏住（MUST FIX 1 的 A1） |
| 凍結行的 code span 配對 | 同段落的上一行補落單的反引號 | INVALID | OK，之後全部被收合（A2） |
| 記帳章節的 HTML 區塊邊界 | 刪掉凍結 HTML 行後的空行 | INVALID | OK（A3） |
| `[` 開頭的放行 | 任務清單、alert、行內連結；`[x foo`／`]:`、`[!NOTE]:`、`[x]:`、`[a\](b]:`、`> [spec]:` | 正當的 OK，參照定義 INVALID | 都正確；`[x]:`、`[a\](b]:` 沒有測試（NICE 1） |
| `[` 開頭（正當，少見） | 參照式連結 `- [#4][r]`、連結文字含方括號或反斜線 | 依文件 | 參照式連結：文件說只放行三種，判 INVALID 符合文件。方括號、反斜線：INVALID，文件沒有說明（NICE 4） |
| 記帳章節的 `<`、fence、標題、setext | 前三輪的 G、H、I、J、K、S、X 系列 | INVALID | 全部 INVALID |
| 契約閘門 | 2.4、2.5，整節新增與既有的現況 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - 以下幾處對分行、凍結章節空行與三種 `[` 放行的描述彼此一致：`review-evidence.md:51`、`docs/AGENTS.md:139`（撰寫規範補上行首粗體、`[` 與分隔線）、`CHANGELOG.md:30-35`、`:61`。
  - 落差只有 docstring（NICE 3）與連結文字的細節（NICE 4）。
  - 本輪沒有修改 `rules/`；check-kit 的雙語章節檢查通過。
- **CHANGELOG 的下游影響**：
  - `<` 的筆數（33 份、44 行）與粗體的筆數（11 份）都能重現。
  - 以 `[` 開頭的記帳行在新規則下是 0，所以不必另列筆數。
  - 少了「凍結章節的空行增減也要重審」（SHOULD FIX 1）。
  - 驗證段的測試數是舊的（NICE 2）。
- **核准範圍**：自 `fe43877` 起，README 只改了 `## 現況`、`**核准 commit**`、待確認事項與 Timeline。Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：
  - 檢查器仍然唯讀。
  - 但「記帳提交藏住凍結內容」還有一條不需要前提的路徑：A1 藏住檔尾 metadata。另有兩條有前提的路徑：A2、A3。所以 gate 的豁免範圍還不安全（MUST FIX 1）。
- **code-simplify**：
  - S11 的修改集中在兩個常數和一個空行分支，沒有新增模擬，方向正確。
  - MUST FIX 1 的試改是在 `analyse()` 外加一層段落追蹤，不需要模擬行內語法。
- **資訊衛生**：
  - 在 `46e09a5..ac2183c` 的 8971 行新增內容中搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`，以及帳號名。只命中前幾輪報告裡列出這些搜尋字樣的四行，沒有實際路徑。
  - 用本機 33 個其他專案的名稱另外搜尋一次，0 筆。
  - 新增的 URL 只有 `example.com`／`example.invalid` 與本 repo 的 GitHub issue。
  - s11-rerun 證據的路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`。
  - 22 個提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。fixture 內 agent 提交的署名沒有進入 kit 的證據檔。
  - 本報告提到的下游掃描只寫筆數，不寫專案名稱。
- **五項檢查**（reviewer 於 2026-11-11 在 `ac2183c` 自行執行，工作樹乾淨）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：192 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4、TBD-6 已解決，TBD-5 不影響本次交付，由 #4 追蹤。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs7/`）。
- 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 實際渲染。
  - CommonMark 規格允許行內連結的 title 跨行（不能有空行），cmark-gfm 依規格實作，所以推論 A1 在 GitHub 上也成立：title 只會在滑鼠停留時出現。
  - 圖片 alt（A1d）在圖片載入失敗時，瀏覽器可能顯示出來。
- 對抗、誤判與變異腳本都在 `<tmp>/review5/`，都沒有進版控：
  - `adv/cases-r5.py`、`cases-r5b.py`、`cases-r5c.py`，以及各自的 `*-out.txt`
  - `prev/`（前四輪案例重跑；`r*-out.txt` 是 HEAD 的結果，`r*-fix-out.txt` 是試改後的結果）
  - `mut/mut.py`、`mut2.py`、`red/`（紅燈重現）
  - `fixcheck/`（MUST FIX 1 的試改副本）
  - `realclone/`（實際 README 的 A1）
  - `scan5.py`（下游掃描，只輸出筆數）
- 已揭露、不構成缺失的限制：wf32 不穩定；WF-28b、wf31 各只跑一輪；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
