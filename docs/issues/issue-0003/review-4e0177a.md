# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，19 個提交、76 個檔案）；第四輪覆審，重點是上一輪 [review-4d0df5c](review-4d0df5c.md) 之後的修正 `31c6bae..4e0177a`
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：4e0177a217e710df2754c418ee8644b5aecbb182
- Reviewed patch-id：6d61d4df36e663e00e6edf6287b174bd0ebf8000（2026-11-11 以 `git diff 46e09a5 4e0177a | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-4e0177a.md
- 審查日期：2026-11-11
- 審查依據：README `## 待確認事項` TBD-2～TBD-6 的使用者決定。本報告照這些決定審查，不重新討論方向。TBD-6 決定記帳章節含 `<` 的行一律凍結，code span 裡的標籤名與佔位字因此判需重審，這是已接受的代價，本報告不列為缺陷。TBD-5 由 GitHub #4 處理，不在本 issue 範圍。

## 問題與風險

### MUST FIX

1. **檢查器的分行與行尾處理跟 CommonMark 不一樣。凍結章節裡只要加一個不可見字元（不含 `<`），就能改掉凍結內容的渲染，結果仍判 OK，變更區段也只列出報告**
   - 位置：`skills/review/scripts/verify-artifact.py:126-127`。
     - `text.splitlines()` 除了 `\n`、`\r\n`、`\r`，還會在 `\v`、`\f`、`\x1c`～`\x1e`、U+0085、U+2028、U+2029 斷行。CommonMark 和 GFM 只認前三種。
     - `raw.rstrip()` 會去掉行尾所有的 Unicode 空白（NBSP、U+3000、U+0085 等）。CommonMark 規定收尾 fence 後面只能接空白或 tab。
     - 所以檢查器拿來比對的行，和渲染器實際看到的行不一樣。
   - 實測方式：在 `<tmp>` 建拋棄式 repo，PASS 之後的提交只新增報告，並以下表方式改寫 README。marked 17.0.5（GFM）與 micromark 4.0.2 加 micromark-extension-gfm 3.0.0 各渲染一次，再用 parse5 7.3.0 判斷標記文字落在哪裡（腳本沿用上一輪的 `render.mjs`）。

     | 案例 | 寫法（都不含 `<`） | 檢查器 | 渲染結果 |
     |---|---|---|---|
     | U2a～c | Gherkin 收尾的 ```` ``` ```` 行尾加 NBSP、U+3000 或 U+0085 | OK，變更只列「新增報告」 | 兩個渲染器都認為 fence 沒有關閉，Gherkin 之後的所有章節與檔尾 metadata 都變成同一個 code block，標題、表格都消失 |
     | U2（實際 README） | 在 `4e0177a` 的拋棄式 clone 裡，`docs/issues/issue-0003/README.md:124` 行尾加 NBSP | OK，變更只列「新增報告」 | 同上：`## Gherkin 核准紀錄` 到 `**狀態**` 全部落在 `pre>code` |
     | U3 | 在凍結的 `## Gherkin 核准紀錄` 行首插入 U+2028 | OK | 標題變成段落文字 |
     | U4 | 凍結章節最後一列表格的行尾接 U+0085（或 U+2028）與 `## Gate 豁免紀錄`，下一行新增 `\| 範圍 \| SCN-001 已由使用者撤銷 \|` | OK（2.4、2.5 都是），變更列「Gate 豁免紀錄」 | 新增的列併入凍結章節的表格。假標題變成多出來的儲存格，不會渲染，畫面上看不到任何異狀（micromark 兩種字元都是這樣；marked 只有 U+0085 如此） |
     | U5 | 凍結段落尾接 U+2029 與 `## Gate 豁免紀錄`，之後新增一段文字 | OK | 新增的文字出現在凍結章節裡，假標題以文字形式留在段落尾 |
     | 對照 U1 | 在 fence 內的行首插入這些字元 | INVALID | fence 內的空行有列入比對 |

   - 影響：
     - 這正是 README「風險與首要驗證」列為最大風險的失敗形態：記帳提交改掉核准的驗收劇本與章節結構，PASS 照樣沿用。
     - U2 適用於每一份有 Gherkin fence 的 README。U4 可以在凍結章節裡偽造內容，而且畫面上看不出來。
     - 這些字元在 `git diff` 裡看不見，檢查器的輸出也不會提到 README 變動（U2、U3），reviewer 很難從輸出察覺。
     - 這不是 S10 造成的：v4.9.0 的檢查器（`46e09a5` 的同一支腳本 `:90-91`）就是這樣寫，但從來沒有登記成已知限制。本 issue 依 TBD-3 收緊所有記帳判定，而 `review-evidence.md:51` 寫的是「記帳區段以外都是凍結內容」，所以列為本 issue 的 MUST FIX。
   - 建議：
     - 分行改成 `re.split(r'\r\n|\r|\n', text)`，行尾只去掉 `' \t'`；`closes()` 的 `.strip()` 也改成 `.strip(' \t')`，讓收尾 fence 的判定一致。
     - reviewer 在 `<tmp>` 的副本裡試改前兩項：`test-evidence.py` 176 項全過，U1～U6 全部判 INVALID，前三輪的 74 個案例判定不變。
     - 補上 U2、U3、U4 的負向案例。

### SHOULD FIX

1. **凍結章節的空行沒有列入比對。刪掉一個空行，凍結的 HTML 區塊或縮排程式碼就會吞掉後文**
   - 位置：`verify-artifact.py:183-184`。`if not line.strip(): continue` 對所有章節都生效，凍結章節的空行增刪不會被偵測到。
   - 實測（方式同 MUST FIX 1）：
     - W2：凍結章節有 `<div id="boundary"></div>`，空一行後是一段含 `` `<details>` `` 的文字。刪掉中間的空行，判 OK。兩個渲染器都把這段文字併進 HTML 區塊，`<details>` 成為原始 HTML，Gherkin 與檔尾 metadata 都落進收合的 `<details>`。
     - W1：凍結段落之後空一行接縮排程式碼 `    範例：<details> 元素不可用`。刪掉空行後，程式碼變成段落的續行，判 OK，結果同 W2。
   - 前提與實際分布：凍結內容要有這種結構才能利用。唯讀掃描本機 683 份不重複的 issue README（與 S10 同一份清單）：
     - 2 份共 7 處，在凍結章節裡有「行首 HTML、空行、含 `<` 的段落」。
     - 2 份在凍結章節裡有縮排程式碼。
   - 影響：可以完全藏住後文，屬於同一個失敗形態。同樣是 v4.9.0 就有的問題，`review-evidence.md:51` 的「記帳區段以外都是凍結內容」讀起來包含空行。
   - 建議：凍結章節（不在 `bookkeeping_sections` 的章節）的空行也記成凍結內容；記帳章節的空行維持不比對。reviewer 在 `<tmp>` 副本試改：176 項全過，W1、W2 判 INVALID，前三輪案例的判定不變。

2. **以 `[` 開頭的凍結規則也套用在引用與清單裡，GitHub alert 與以連結開頭的清單項都會判 INVALID，但寫作規範與下游提醒沒有說到這一點**
   - 位置：`verify-artifact.py:34`（`CONTAINER + r'\[…'`）。文件方面：
     - `docs/agents/review-evidence.md:51` 的「三者都含多層引用與清單」只涵蓋前三種寫法。
     - `CHANGELOG.md:33`、`:60` 只寫「以 `[` 開頭的行」。
     - `docs/AGENTS.md:139` 給撰寫者的規範只提到 `<`。
   - 實測（記帳章節，判 INVALID）：
     - N4：Timeline 寫 `- [#4](https://example.com/4) 另開 issue`。
     - N4b：`## 現況` 寫 `> [!NOTE]`。
     - N4c：`- [x]`，`]` 後面直接換行。
     - 對照 X1：`- [x] [spec2]: 新網址` 判 OK，兩個渲染器都沒有把它當成定義，凍結章節的連結仍指向原網址。任務清單的例外是安全的。
   - 下游分布：本機 683 份 README 的記帳章節中，有 5 份共 7 行在容器前綴之後以 `[` 開頭。其中 5 行是 `> [!…]` 這類 GitHub alert。`CHANGELOG.md:60` 列了 `<` 與粗體的筆數，沒有列這一類。
   - 影響：這些都是正當的記帳寫法，審查之後補寫就會讓 PASS 失效。讀到「以 `[` 開頭的行」的人不會想到 `> [!NOTE]` 也算在內。
   - 建議：
     - `review-evidence.md:51`、`CHANGELOG.md:33`、`:60` 寫明引用與清單裡的 `[` 開頭也凍結，舉 `> [!NOTE]` 與 `- [連結](…)` 為例，並補上下游筆數。
     - `docs/AGENTS.md:139` 的撰寫規範一併列出 `[` 開頭與「文字後接 `===`、`---`」。
     - 也可以選擇放行「同一行就關閉、括號內沒有 `\`、`[`、`]`，而且後面不是 `:`」的寫法，因為參照定義一定是 `]:`。這是可選的修法，修文件就足以處理本項。

### NICE TO HAVE

1. **已知限制的登記比實際放行的範圍小**
   - N1：`## 現況` 裡以 `|` 開頭、但不是表格的一行，後接 `===`，渲染成 h1，判 OK。N1b 是 2.4 待確認事項接 `---`，渲染成 h2，判 OK。
   - 已登記的是「以 `|` 開頭的段落後接 `---`」（`docs/issues/issue-0002/implementation-plan.md:51`，`CHANGELOG.md:34`「表格接 `---`」）。排除 `|` 的理由是 Timeline 末列會緊接 footer 的 `---`，但 `===` 沒有這個理由。
   - 建議：`setext_underline()` 只在底線是 `-` 時排除 `|`；或者在已知限制寫明 `===` 也放行。
   - 另外，`&nbsp;**風險**：低` 與 `_**風險**_：低`（N2、N3）會渲染成粗體欄位的樣子，判 OK。行中間本來就允許粗體，依欄位格式解析的工具也不會被騙，所以影響很小，需要時再登記即可。
2. `verify-artifact.py:26-27` 的 `SETEXT` 與 `NOT_PARAGRAPH` 已經沒有任何地方使用（code-simplify）。
3. **變異測試有 4 個存活**（8 個變異，4 個被抓到：行首 `<`、任務清單例外、setext 去引用、`<BR>` 大小寫）：
   - M2：`html()` 改成只用 `lstrip()`、不去容器前綴。沒有 `- <br>`、`> <br>` 的負向案例。
   - M4：setext 不排除 `|`。沒有「表格末列緊接 `---`」的正向案例，這正是保留這個排除的理由。
   - M6：`LINK_DEFINITION` 不含容器前綴。沒有 `> [spec]: …` 的案例。
   - M7：註解關閉後不再判斷是否重開。`test-evidence.py:492` 是為上一輪 NICE 4（M10）補的案例，但第一行 `<!-- 開頭` 本來就含 `<` 而被凍結，所以抓不到這個變異。新規則下，註解追蹤只對被審查版本裡已經存在的多行註解有作用（攻擊方式是刪掉最後的 `-->`），案例要照這個形狀寫。

### 需決策

無。MUST FIX 與兩項 SHOULD FIX 都有不改變已決方向的修法：TBD-3 決定本 issue 收緊所有記帳判定，TBD-6 的「寧可多凍結」方向也不受影響。

## 已查核維度

### 上一輪發現的處理（依 TBD-2～TBD-6）

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：`<br>`／`<wbr>`／`</br>` 與行首註解開出 HTML 區塊（G1～G9） | `html()`（`verify-artifact.py:100-103`）：去掉容器前綴後以 `<` 開頭就凍結，其餘行只放行 `<br>`、`<wbr>`。G1～G9 重跑全部 INVALID；新增測試 `test-evidence.py:480-492`、`:781` | 完成 |
| MUST FIX 2：code span 判定不一致（藏住 H1、H3、I1；誤判 K1、K2） | 移除 code span、跳脫與表格的模擬。H1～H3、I1 判 INVALID。K1、K2 依 TBD-6 判 INVALID，這是已接受的代價。文件已說明：`docs/AGENTS.md:139`、`CHANGELOG.md:60`、README TBD-6，說法和實作一致 | 完成（依 TBD-6） |
| SHOULD FIX 1：跨行的參照定義標籤（J3、J4） | `LINK_DEFINITION`（`:34`）把以 `[` 開頭的行一律凍結；J0～J4 都判 INVALID，測試在 `:489` | 完成；附帶的誤判見本輪 SHOULD FIX 2 |
| SHOULD FIX 2：清單續行與長數字的 setext（S1～S3） | `setext_underline()`（`:110-118`）不再比對縮排與層數；S1～S3 判 INVALID，測試在 `:490-491` | 完成；`NOT_PARAGRAPH` 已不再使用（NICE 2） |
| NICE 1：發布文件 | `CHANGELOG.md:22` 已加條件、`:50` 改為「每案一輪，WF-32 另跑多輪」、`:60` 已補 `n<k`；`rule-verification-status.md:333` 已加條件 | 完成 |
| NICE 2：對抗案例計數 | `implementation-plan.md:152` 已更正為 37 個 INVALID、9 個 OK | 完成 |
| NICE 3：wf32 追加輪次 | `implementation-plan.md:168` 已揭露；S10 的 expected.md 事先寫定每案一輪 | 完成 |
| NICE 4：變異存活 | M9（autolink）已不適用，改由 `test_current_review_platform_link_forms` 判 INVALID；M11（引用層數）依設計不再比對；M10 補了案例，但變異仍然存活 | 部分完成（NICE 3） |
| NICE 5：上一輪 NICE 7 | `implementation-plan.md:185` 已記錄 | 完成 |

前三輪的對抗與誤判案例全部重跑（`<tmp>/review4/adv/prev-out.txt`，共 74 個）：判 OK 的只有 C0、FP7（行中間的 `<br/>`）、FP8（不帶粗體的編號清單）與 K6（腳本實際沒有改動 README），其餘 70 個都是 INVALID。這和 `implementation-plan.md:181` 的記載相符。

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 `<tmp>` 的 fixture：wf31（`a4f74f6`→`2eaf42b`）與 WF-28b（`4f4fae5`→`48ae482`）都是 OK，變更區段含「現況、現行 review」；`CurrentStateTests` 全過 | 通過 |
| SCN-002 | S10 新增 24 個負向案例。reviewer 以 `31c6bae` 的腳本配 HEAD 的測試檔重跑：176 項、25 個失敗，其中 24 個和 `evidence/s10-red.txt` 的失敗名稱完全相同，多出的是紅燈之後才補的 `test_current_review_platform_link_forms`（`implementation-plan.md:180` 已揭露）。HEAD 版 176 項全過 | 有缺口：MUST FIX 1、SHOULD FIX 1 |
| SCN-003 | 2.4、2.3 與無契約的案例全過 | 通過；2.4 同樣受 MUST FIX 1（U4-2.4）影響 |
| SCN-004 | WF-28b、wf31 重跑時，`## 現況` 都建在 `## 概述` 之後（reviewer 逐份核對 diff） | 通過 |
| SCN-005～008 | 本輪沒有修改，沿用上一輪的判定 | 同 review-4d0df5c |

其他證據查核：
- **判準先於重跑**：
  - `expected.md:124`「第三輪審查後重跑」和修正一起在 `cff0449`（12:22:51）提交。
  - 兩份 s10-rerun 證據都記錄 kit HEAD `cff0449`，這個 SHA 不可能事先得知。
  - fixture 的回合提交都比判準晚：WF-28b `48ae482` 12:24:29、wf31 `2eaf42b` 12:26:48。結果在 `4e0177a`（12:28:08）提交。
  - 結論：判準確實先於重跑。
- **記載一致性**：
  - 以下幾處說法一致：`implementation-plan.md:191-194`、`workflow-results/2026-11-10.md:77-86`、`rule-verification-status.md:327`、README Timeline 最後一列，都寫「各一輪、記帳提交沒有 `<`、檢查器 OK」。
  - 各處都寫明只有一輪、穩定性未知，沒有誇大。
  - reviewer 核對 WF-28b 的 diff：TBD-1 把報告裡的 `` `done <id>` `` 改寫成「`done` 會同時標記兩筆」，記帳內容 0 處含 `<`。agent 第一次執行檢查器沒有通過，於是把章節移到 Timeline 前、amend 尚未推送的提交後才 OK。這段經過在證據的最終輸出裡寫得很清楚。
- **既有記帳提交**：`31c6bae` 判 OK、`18f0e64` 判 INVALID，和 `implementation-plan.md:182` 相符；`d0e3287` 也是 OK。
- **變異測試**：見 NICE 3（腳本在 `<tmp>/review4/mut/`）。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 分行與行尾正規化 | 凍結行行尾加 NBSP／U+3000／U+0085；行首或行尾插入 U+2028、U+0085 加上假標題 | INVALID | 判 OK，fence 不關閉、標題消失、可以注入內容（MUST FIX 1） |
| 凍結章節的空行 | 刪掉 HTML 區塊或縮排程式碼前後的空行 | INVALID | 判 OK，後文被收合（SHOULD FIX 1） |
| 記帳章節的 `<` | 前三輪的 G、H、I、K 系列，以及容器前綴的 `<br>` | INVALID | 全部 INVALID；`- <br>` 沒有測試（NICE 3） |
| fence、標題 | tab 縮排的 fence、`> - ```` ````、`#<tab>x`、`**現行 review**` 下一行接 `===` | INVALID | 全部 INVALID（X2～X5） |
| 參照定義與腳註 | `[spec\n]:`、`[^1]:`、`- [x] [spec2]:`、`&#91;spec]:` | 定義判 INVALID，非定義判 OK | 定義都判 INVALID；任務清單與實體開頭的兩種都不是定義，判 OK，連結目標沒有被改（X1、X7） |
| setext | 清單續行、長數字編號、`\|` 開頭的段落接 `===` | INVALID | 前兩種 INVALID；`\|` 開頭的那種判 OK（NICE 1） |
| 正當記帳 | 行中間的 `<br/>`、任務清單、一般網址、不帶粗體的編號清單 | OK | OK |
| 正當記帳 | `> [!NOTE]`、以連結開頭的清單項 | OK 或文件有說明 | INVALID，文件沒有說明（SHOULD FIX 2） |
| 正當記帳 | code span 裡的標籤名、`{id}` 以外的佔位字、`<網址>`、`n<k` | 依 TBD-6 判 INVALID | INVALID，文件有說明 |
| 契約閘門 | 2.4、2.5，整節新增與既有的現況 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - review-evidence.md:51、docs/AGENTS.md:129、:139、CHANGELOG.md:30-33、:60、document-types.md:27 與檢查器 docstring（`verify-artifact.py:7-10`），對「含 `<` 就凍結、只放行行中間的 br／wbr、`[` 開頭、文字後的 `===`／`---`」的描述彼此一致。
  - docs/AGENTS.md 要求記帳內容完全不含 `<`，比檢查器嚴，作為撰寫規範是合理的。
  - 落差只有 SHOULD FIX 2 提到的容器內 `[`。
  - TBD-6 對代價的描述（code span 裡的標籤名與佔位字也要重審）是準確的。
- **雙語 rules**：本輪沒有修改 `rules/`；check-kit 的章節數檢查通過。
- **CHANGELOG 的下游影響**：`<` 的筆數（33 份、44 行）與粗體的筆數都能從 S10 的清單重現。漏掉 `[` 開頭的那一類（SHOULD FIX 2）。MUST FIX 1 與 SHOULD FIX 1 修好後，已知限制和驗證段落要跟著更新。
- **核准範圍**：自 `fe43877` 起，README 只改了 `## 現況`、`**核准 commit**`（`待提交` → `fe43877`）、待確認事項（TBD-5、TBD-6、TBD-3 補註）與 Timeline。Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：檢查器仍然唯讀。但「記帳提交改掉凍結內容」的失敗形態還有兩條不含 `<` 的路徑（MUST FIX 1、SHOULD FIX 1），所以 gate 的豁免範圍還不安全。
- **code-simplify**：
  - S10 移除了 code span、跳脫與表格的狀態，HTML 判定剩一個函式，方向正確。
  - 還留著兩個沒用到的常數（NICE 2）。
  - MUST FIX 1 的修法只改兩行，不會增加新的模擬。
- **資訊衛生**：
  - 在 `46e09a5..4e0177a` 的 7849 行新增內容中搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`，以及帳號名與信箱前綴。只命中前幾輪報告裡列出這些搜尋字樣的三行，沒有實際路徑。
  - 用本機其他專案的名稱另外搜尋一次，0 筆。
  - `31c6bae..4e0177a` 新增的 URL 只有 `example.com`／`example.invalid`。
  - s10-rerun 證據的路徑都已遮蔽成 `<隔離設定>`、`<fixtures>`。
  - 19 個提交的訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。
  - 本報告提到的下游掃描只寫筆數，不寫專案名稱。
- **五項檢查**（reviewer 於 2026-11-11 在 `4e0177a` 自行執行，工作樹乾淨）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：176 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4、TBD-6 已解決，TBD-5 不影響本次交付，由 #4 追蹤。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs6/`）與原始輸出（`raw6/`），這些都沒有進版控。
- 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 實際渲染。
  - micromark 依 CommonMark 規格實作，cmark-gfm 同樣只以 `\n`、`\r` 分行，也只允許收尾 fence 後接空白或 tab，所以推論 U2、U4 在 GitHub 上也成立。
  - GitHub 的數學區塊（`$$`）沒有測。
- 對抗、誤判與變異腳本都在 `<tmp>/review4/`，都沒有進版控：
  - `adv/probe4.py`、`adv/cases-r4.py`、`cases-r4b.py`、`cases-r4c.py`、`cases-r4d.py`，以及各自的 `*-out.txt`
  - `adv/prev-out.txt`（前三輪案例重跑）
  - `mut/mut.py`
  - `fixcheck/`（MUST FIX 1 與 SHOULD FIX 1 的試改副本）
  - `realclone/`（實際 README 的 U2）
  - `redcheck/`（紅燈重現）
  - `scan.py`（下游掃描，只輸出筆數）
- 已揭露、不構成缺失的限制：wf32 不穩定；WF-28b、wf31 各只跑一輪；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
