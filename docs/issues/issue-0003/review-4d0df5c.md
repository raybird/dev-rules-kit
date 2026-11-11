# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，16 個提交、71 個檔案）；第三輪覆審，重點是上一輪 [review-acd488f](review-acd488f.md) 之後的修正 `18f0e64..4d0df5c`
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：4d0df5c6e6c869808d2722d9964eb0b3a8af1ea4
- Reviewed patch-id：e18b0b96afa5086d62d96d636fef8267ae4896fa（2026-11-11 以 `git diff 46e09a5 4d0df5c | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-4d0df5c.md
- 審查日期：2026-11-11
- 審查依據：README `## 待確認事項` TBD-2～TBD-5 的使用者決定。本報告照這些決定審查，不重新討論方向；TBD-5 由 GitHub #4 處理，不在本 issue 範圍。

## 問題與風險

### MUST FIX

1. **放行清單裡的 `<br>`、`<wbr>`、`</br>` 與行首的單行註解會開出 CommonMark 的 HTML 區塊。區塊裡的 code span 與反斜線跳脫不再是 Markdown，檢查器卻照樣把它們去掉，結果判 OK，而後文全部被藏住**
   - 位置：`skills/review/scripts/verify-artifact.py:32-33`（`SAFE_HTML`）、`:144-146`（`html()`）、`:200`（每一行都先去 code span 與跳脫，才判斷 HTML）。檢查器只逐行判斷，不知道某一行是不是落在 HTML 區塊裡。
   - 機制：依 CommonMark，單獨一行的 `<br>` 是第 7 型 HTML 區塊，會一直延續到空行；以 `<!--` 開頭的行是第 2 型，`-->` 所在的那一整行都是原始 HTML。所以在 `<br>` 的下一行，或是在 `<!-- … -->` 的同一行後面，`` `<details>` `` 與 `\<details>` 都會原樣送進瀏覽器，開出一個沒有關閉的 `<details>`。
   - 實測方式：在 `<tmp>` 建拋棄式 repo，PASS 之後的提交只新增報告，並把下列內容加進記帳章節。marked 17.0.5（GFM）與 micromark 4.0.2 加 micromark-extension-gfm 3.0.0（依 CommonMark 規格實作，含 GitHub 的 tagfilter）各渲染一次，再用 parse5 7.3.0 判斷標記文字落在哪裡。

     | 案例 | 寫法 | 檢查器 | 兩個渲染器的結果 |
     |---|---|---|---|
     | G1 | `## 現況` 內：`<br>` 單獨一行，下一行 `` `<details>` `` | OK | Gherkin 與檔尾 metadata 都落進收合的 `<details>` |
     | G2 | 同 G1，下一行改成 `\<details>` | OK | 同上 |
     | G3 | 同 G2，第一行改成 `<wbr>` | OK | 同上 |
     | G4 | 同 G2，第一行改成 `</br>` | OK | 同上 |
     | G5 | 行首寫 `<!-- 備註 --> \<details>` | OK | 同上 |
     | G6 | 行首寫 ``<!-- 備註 --> `<details>` `` | OK | 同上 |
     | G7 | 流程契約 2.4，待確認事項表格之後空一行，接 G2 的寫法 | OK | metadata 被收合 |
     | G8 | 流程契約 2.4，Timeline 表格之後空一行，接 G2 的寫法 | OK | metadata 被收合 |
     | G9 | G2 的下一行改成 `\<script>` | OK | marked 把後文全部吞進 `<script>`；micromark 的 tagfilter 會把它轉成文字 |
   - 影響：這是 README「風險與首要驗證」列為最大風險的失敗形態，也是前兩輪 MUST FIX 1 的同一類問題：記帳提交藏住核准的驗收劇本，PASS 照樣沿用。這次的寫法在原始碼裡看起來完全合規。`docs/agents/review-evidence.md:51` 要求「提到標籤名時寫在 code span 裡或以反斜線跳脫」，`docs/AGENTS.md:129` 也要求寫在 code span 裡，所以這個寫法讀起來正是規範的做法。2.4 專案同樣受影響（G7、G8）。GitHub 用的是 cmark-gfm，同樣依 CommonMark 處理 HTML 區塊，而且允許 `<details>`，所以推論在 GitHub 上也成立（沒有實際在 GitHub 渲染）。
   - 建議：
     - 記帳章節裡，去掉容器前綴與最多 3 個空白之後以 `<` 開頭的行，一律凍結，`<br>` 與註解也一樣。放行清單只在行內（`<` 前面有其他文字）或表格列內有效。
     - 如果要保留行首的 `<br>`，就要追蹤 HTML 區塊：第 7 型凍結到空行，第 2 型凍結 `-->` 所在的整行，不做 code span 與跳脫的去除。
     - 補上 G1、G2、G5 與 2.4 的負向案例。

2. **code span 的判定和渲染器不一致，雙向都有問題：一邊讓藏住的寫法判 OK，另一邊讓正當記帳判 INVALID**
   - 位置：
     - `verify-artifact.py:125`：遇到未跳脫的 `|` 就停止尋找配對的 backtick。這個條件沒有限定表格列，所以一般段落與清單也會套用。
     - `:198-199`：只要前一行以 `|` 開頭、這一行符合分隔列，就當成表格，沒有比對表頭和分隔列的欄數。GFM 規定欄數不同就不是表格，這些行會變回一般段落，而段落裡的 code span 可以跨行。
   - 藏住（實測方式同 MUST FIX 1）：

     | 案例 | 寫法 | 檢查器 | 兩個渲染器的結果 |
     |---|---|---|---|
     | H1 | `## 現況` 內一般段落：`` `|` <details> `|` `` | OK | Gherkin 與 metadata 都被收合。檢查器把第一個 backtick 當成未配對，再把第二、三個 backtick 配成一對，於是 `<details>` 被當成 code span 去掉 |
     | H3 | 流程契約 2.4，待確認事項表格後的段落，寫法同 H1 | OK | metadata 被收合 |
     | I1 | `## 現況` 內：`\| x \|`、`\|---\|---\|`（欄數不同）、`` \| a ` \| ``、``\| `<details>` \|`` | OK | 兩個渲染器都不認成表格，第 3、4 行的 backtick 跨行配對，`<details>` 變成原始 HTML，後文全部被收合 |

     H2 是同一寫法放在清單項裡，`</li>` 會把 `<details>` 關掉，後文仍然看得到。
   - 誤判（正當記帳判 INVALID）：
     - K1：Timeline 清單列「查證命令 `` `git log | head` `` 確認 `` `<template>` `` 已移除」，判 INVALID，報成 HTML。
     - K2：`## 現況` 段落第一行有 `` `curl -s x | grep -c title` ``，下一行有 `` `<title>` ``，判 INVALID。第一行的 backtick 被判成未配對，延續到下一行之後就不再去掉 code span。
   - 影響：
     - 藏住的部分和 MUST FIX 1 屬於同一失敗形態。
     - 誤判的部分讓上一輪 SHOULD FIX 2 只修好一半：查證命令裡常有管線符號 `|`，`## 現況` 的外部狀態又正好是放查證命令的地方。
     - 變異測試的結果：把 `:125` 的 `|` 條件整個拿掉會被既有測試抓到（表格內 `` `x | <details> | y` `` 的案例），所以修法是只在表格列套用這個條件，不是刪掉它。
   - 建議：
     - `|` 的界線只在已確認的表格列（含表頭列）套用。確認表格時比對表頭和分隔列的欄數。
     - 欄數不同的「表格」照一般段落處理，未配對的 backtick 會延續到下一行。
     - 補上 H1、I1 的負向案例，以及 K1、K2 的正向案例。

### SHOULD FIX

1. **連結參照定義的標籤可以跨行，`LINK_DEFINITION` 擋不住，`## 現況` 仍然能改掉凍結章節的連結目標**
   - 位置：`verify-artifact.py:35`。`CONTAINER + r'\[[^\]]+\]:'` 只比對同一行的 `[標籤]:`。
   - 實測：
     - 凍結的 `[審查 報告]: review.md` 寫在 `## 現況` 之後時，在 `## 現況` 加一行 `[審查`，下一行接 `報告]: https://example.invalid/evil`，判 OK（J3）。marked 與 micromark 都把凍結章節的 `[審查 報告]` 連到新網址。
     - 標籤不含空白也可以：`[spec`，下一行接 `]: https://example.invalid/evil`，判 OK（J4）。micromark 依 CommonMark 正規化標籤（去掉換行），結果改連到新網址；marked 不認。
     - 對照組：同一行寫 `[審查 報告]: …`，判 INVALID（J0、J2）。
   - 前提：凍結的定義要在記帳章節之後。`## 現況` 位在 `## 概述` 之後，所以多數定義都在它後面。
   - 影響：屬於改連結目標的偽造，不會藏住內容。不過 `CHANGELOG.md:33`（「連結參照定義…會改掉凍結章節同名連結的目標」）與 `docs/agents/review-evidence.md:51` 都寫成已經凍結。
   - 建議：記帳章節裡含 `]:` 的行，以及以 `[` 開頭、同一行沒有 `]` 的行，都列為凍結。

2. **清單續行縮排 4 格以上的 setext 標題，以及不是清單的長數字編號，仍然沒有凍結**
   - 位置：`verify-artifact.py:155-161`。前一行的容器前綴只有空白時，第一個判斷要求底線行最多 3 個空白，第二個判斷又因為 `not prefix.strip()` 直接回傳 False。
   - 實測（2.5，`## 現況` 內，判 OK）：
     - S1：`- 項目`、`    驗收條件已變更`、`    ===`：渲染成 `<ul><li><h1>`。
     - S3：巢狀清單的續行，寫法同 S1：渲染成 `<ul><li><ul><li><h1>`。
     - S2：`1234567890. 驗收條件已變更` 下一行接 `===`：10 位數字不是清單標記，渲染成 `<h1>`。
   - 影響：和上一輪 SHOULD FIX 1 是同一類，屬於偽造標題、不會藏住內容。`CHANGELOG.md:32` 與 `review-evidence.md:51` 寫的是「多層引用、清單…裡的標題（含 setext）」都凍結。
   - 建議：前一行只有空白前綴時，往回找它所屬的清單項，用清單項的內容欄位判斷底線行的縮排。如果嫌複雜，把「記帳章節中只含 `=` 或 `-` 的行，而且前一行是非空白的非表格行」一律凍結，誤判的代價很小。另把 `NOT_PARAGRAPH` 的數字限制在 1～9 位。

### NICE TO HAVE

1. **發布文件仍有三處沒跟上 S9**
   - `CHANGELOG.md:22` 的工作流程第 6 項仍寫「查證結果寫回 README 的 `## 現況`」，沒有條件；`docs/AGENTS.md:180` 已改成「要保存…時，寫回…（時機見 document-types.md）」。`docs/rule-verification-status.md:333` 的規則欄也一樣。
   - `CHANGELOG.md:50` 寫「每案一輪」，但同一段 `:53` 寫 wf32 5 輪。
   - `CHANGELOG.md:60` 的下游提醒只寫「code span 以外的 HTML 標籤」。實作凍結的是所有 `<` 接英文字母的寫法，一般文字的比較式 `n<k` 也判 INVALID（K7）。建議改成「`<` 直接接英文字母的寫法（含 `a<b` 這類比較式）」。
2. `docs/issues/issue-0003/implementation-plan.md:151` 的對抗案例計數兜不起來。reviewer 重跑同一批 46 個案例，結果是 37 個 INVALID、9 個 OK（C0 與 FP1～FP8）。計畫寫的是「攻擊寫法 37 個全部 INVALID；控制組與合理寫法 9 個中，8 個 OK」，換算下來是 38 個 INVALID。判定結論不受影響。
3. **wf32 的追加輪次沒有事先寫定**
   - `expected.md:112-122` 寫的是每案一輪，追加 3 輪是在看到第 1 輪失敗之後才決定的（`implementation-plan.md:155`）。
   - 四輪全部列出、第 1 輪照實判為未符合、整體標為不穩定，所以沒有挑選輪次，記載也誠實。
   - 建議：之後要跑多輪時，先在 expected.md 寫定輪數與通過門檻，再開始跑。
4. 變異測試有三個存活：
   - M9：拿掉 email 自動連結的放行。沒有正向案例。
   - M10：註解的關閉行如果又開新註解（`--> <!--`），檢查器不再追蹤。沒有負向案例。
   - M11：setext 底線不比對引用層數。沒有案例。
   
   都不會讓目前的攻擊寫法通過，但 M10 是註解追蹤的分支，建議補案例。
5. review-acd488f 的 NICE 7（2.4 專案覆寫外部狀態列會讓 PASS 失效，記下即可）在 TBD 與計畫裡都沒有記錄。影響很小，可以在 S9 證據補一句。

### 需決策

無。MUST FIX 與 SHOULD FIX 都有不改變已決方向的修法（TBD-3 已決定記帳章節一起收緊）。

## 已查核維度

### 上一輪發現的處理（依 TBD-2～TBD-5）

| 上一輪 | 處理與依據 | 結論 |
|---|---|---|
| MUST FIX 1：跨行標籤、清單外標籤、多行註解 | 改用允許清單（`verify-artifact.py:31-34`），追蹤註解（`:180-184`、`:219`）。上一輪 37 個藏住寫法（`<tmp>/review3/adv/cases-out.txt`）重跑後除 C0 控制組外全部 INVALID；刪除或搬移 `-->` 判 INVALID（測試 `test_multiline_comment_frozen_until_close`）。文件更新：`review-evidence.md:51`、`CHANGELOG.md:30-33` | 原列寫法已擋住；但允許清單本身開出新的藏住路徑 → 本輪 MUST FIX 1、2 |
| SHOULD FIX 1：容器內 setext | `setext_underline()`（`:153-170`）；清單與引用的案例判 INVALID | 大致完成；縮排 4 格的續行與長數字仍漏 → 本輪 SHOULD FIX 2 |
| SHOULD FIX 2：code span 與跳脫的誤判 | `outside_code()`（`:106-141`）；FP1～FP8 重跑全部 OK，FP9（`1. **日期**`）依 TBD-3 判 INVALID。`docs/AGENTS.md:129`、`CHANGELOG.md:60` 已提醒 | 原列寫法已不再誤判；`|` 的處理帶來新的誤判與藏住 → 本輪 MUST FIX 2 |
| SHOULD FIX 3：發布文件 | `CHANGELOG.md:49`（175 項）、`:53`（交接文件改依原文）、`docs/workflow-regression.md:55`、`implementation-plan.md:31`（S6 加註重判） | 完成；新的落差見 NICE 1 |
| SHOULD FIX 4：交接文件讓 PASS 失效（TBD-5） | 使用者選「補紀錄、另開 issue」。`workflow-results/2026-11-10.md:61`、`:75`，`rule-verification-status.md:333`，`CHANGELOG.md:53`，README TBD-5 都寫明「沒有告知」。`gh issue view 4`：OPEN，2026-11-11 建立 | 完成 |
| SHOULD FIX 5：`**現行 review**` 的格式 | `document-types.md:27` 寫明以 issue 目錄解析；`readme-templates.md:42`、`:144` 與 `review-evidence.md:35` 改成「檔名或平台連結」；`CHANGELOG.md:61` | 完成 |
| NICE 1：連結參照定義 | `LINK_DEFINITION`（`:35`）；同一行的寫法判 INVALID | 部分完成；跨行標籤仍可繞過 → 本輪 SHOULD FIX 1 |
| NICE 2：`details` 的變異 | 封閉清單已移除 | 不再適用 |
| NICE 3：環境差異 | `workflow-results/2026-11-10.md:51`；`rule-verification-status.md:333` 改成「沒有在同一環境重跑」 | 完成 |
| NICE 4：wf29d 的技能來源 | `evidence/s8-rerun/pre-fix/wf29d.md:6` | 完成 |
| NICE 5：保存回合內提交 | `docs/issues/issue-0001/fixtures/run_case.py:114-120` 只取主旨，寫檔前經過 `mask()`；`evidence/s8-rerun/wf32.md` 補上交接文件全文 | 完成 |
| NICE 6：第 6 項加條件 | `docs/AGENTS.md:180` | 完成；CHANGELOG 與驗證狀態表沒有跟上（NICE 1） |
| NICE 7：記下 2.4 的外部狀態列 | 沒有找到紀錄 | 未處理（NICE 5） |
| NICE 8：TBD-3 補註 | README TBD-3 影響欄 | 完成 |

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | reviewer 以 HEAD 的檢查器重跑 `<tmp>` 的 fixture：wf31（`831e2ac`）與 WF-28b（`99acc53`）都是 OK，變更區段列出「現況、現行 review」。測試 `CurrentStateTests` 正向案例全過 | 通過 |
| SCN-002 | S9 新增 48 個負向案例。reviewer 以 `18f0e64` 的腳本配最終測試檔重跑：175 個測試、48 個失敗，失敗名稱與 `evidence/s9-red.txt` 完全相同。HEAD 版 175 個全過 | 有缺口：MUST FIX 1、2，SHOULD FIX 1、2 |
| SCN-003 | 2.4、2.3、無契約的案例全過；`LegacyBookkeepingTests` 新增的兩個案例回報需要 2.4 | 通過；2.4 也受 MUST FIX 1、2 影響（G7、G8、H3） |
| SCN-004 | wf29 回合 2 覆寫兩列、列數不變（`evidence/s9-rerun/wf29.md:108-111`）；wf31、WF-28b 的現況建立在 `## 概述` 之後 | 通過 |
| SCN-005 | wf29 回合 1 先跑 `git merge-base`，查詢模式不改檔（`wf29.md:11-12`） | 通過（無法區分） |
| SCN-006 | wf30c 指出指標落差，並說明應改成報告檔名（`wf30c.md:51`）；沒有執行檢查器，照實寫在 `:52` | 符合，揭露正確 |
| SCN-007 | wf32 共 4 輪：第 1 輪的交接文件有「目前進度」表與查證表（`wf32.md` 的 diff），依原文未符合；第 2～4 輪只有 README 連結與錨定 commit 的事件（`wf32-r2.md`～`wf32-r4.md`，reviewer 逐份核對 diff） | 3／4 通過，記為不穩定，屬實 |
| SCN-008 | 沒有觸發，登記為僅靜態撰寫 | 登記正確 |

其他證據查核：
- **判準先於重跑**：
  - `expected.md`「第二輪審查後重跑」在 `b2f321f`（11:41:36）提交。
  - 7 份 s9-rerun 證據都記錄 kit HEAD `b2f321f`，這個 SHA 不可能事先得知。
  - fixture 的回合提交都比判準晚：wf32 `98309bb` 11:42:27、WF-28b `99acc53` 11:42:54、wf29 `49f097b` 11:42:59、wf31 `831e2ac` 11:44:39，r2～r4 在 11:46。
  - 結果在 `4d0df5c`（11:48:00）提交。判準確實先於重跑；追加輪次的時機見 NICE 3。
- **記載一致性**：計畫 S9（`implementation-plan.md:142-169`）、README Timeline 最後一列、`workflow-results/2026-11-10.md:64-75`、`rule-verification-status.md:327`、`:333` 與 `CHANGELOG.md:53` 對 wf32 的說法一致：S9 4 輪 3 輪通過，加上 S8 的 1 輪，共 5 輪 4 輪通過，5 輪都沒有告知 PASS 失效。wf30c 照實記為部分未符合。沒有誇大，只有 NICE 1、2 的小落差。
- **reviewer 實測 wf32 的 PASS 失效**：4 個 fixture 以 HEAD 的檢查器判定，都是「變更了 docs/handover.md（A）…需重新審查」，與紀錄相符。
- **變異測試**：對新邏輯做 12 個變異，9 個被測試抓到（code span 不受 `|` 限制、不處理跳脫、不追蹤註解、不凍結連結定義、容器內 setext、表格旗標、backtick 延續、自動連結放行、清單續行縮排），3 個存活（NICE 4）。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 放行的 HTML 開出原始 HTML 區塊 | `<br>`／`<wbr>`／`</br>` 單獨一行接 code span 或跳脫的標籤；行首單行註解接同樣寫法 | INVALID | 判 OK，後文被收合（MUST FIX 1） |
| code span 判定不一致 | 非表格行的 `|`；欄數不符的表格 | INVALID | 判 OK，後文被收合（MUST FIX 2） |
| 正當記帳 | 清單或段落裡有含 `|` 的命令，又在 code span 提到標籤 | OK | 判 INVALID（MUST FIX 2）。表格列裡的 `\|`、雙 backtick、自動連結、`<br/>` 都是 OK |
| 偽造連結目標 | 跨行的參照定義標籤 | INVALID | 判 OK（SHOULD FIX 1） |
| 偽造標題 | 清單續行的 setext、長數字編號 | INVALID | 判 OK（SHOULD FIX 2） |
| 上一輪的 46 個案例 | `<tmp>/review3/adv/cases.py`、`fp.py` | 照上一輪的預期 | 全部符合 |
| 契約閘門 | 2.4、2.5，整節新增與既有現況 | 依規定 | 正確 |

### 需求、架構、安全、品質

- **規則一致性**：
  - review-evidence.md、docs/AGENTS.md 的 Gate 豁免紀錄、CHANGELOG 與檢查器的 docstring（`verify-artifact.py:7-9`），對允許清單、註解追蹤與連結定義的描述彼此一致。
  - 與實作不符的只有 SHOULD FIX 1、2 列出的兩種寫法。
  - `**現行 review**` 的格式在規則、範本與核准規格之間已經一致。
  - 第 6 項的條件只差 CHANGELOG 與驗證狀態表沒有跟上（NICE 1）。
- **雙語 rules**：本輪沒有修改 `rules/`；check-kit 的章節數檢查通過。
- **核准範圍**：自 `fe43877` 起，README 只改了 `## 現況`、待確認事項（新增 TBD-5、TBD-3 補註）與 Timeline，Gherkin 與設計邊界都沒有變動。
- **安全與 gate**：檢查器仍然唯讀。但「記帳提交藏住凍結內容」這個失敗形態仍有兩條路徑（MUST FIX 1、2），所以 gate 的豁免範圍還不安全。
- **code-simplify**：判斷 HTML 只剩 `SAFE_HTML` 與 `ANY_HTML`，code span 和註解狀態各有一個輔助函式，沒有跨 Task 的重複。不過檢查器一直在用逐行的正則表達式近似 CommonMark 的區塊結構，三輪下來每輪都還有分歧。建議修 MUST FIX 1、2 時一律選保守的方向：看不準就凍結，不要再擴大放行。
- **資訊衛生**：
  - 在 `46e09a5..4d0df5c` 的新增行中搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`，以及帳號名，只命中 review-acd488f 報告裡列出這些搜尋字樣的兩行，沒有實際路徑。
  - 用其他專案的名稱另外搜尋一次，0 筆。
  - 新增的 `/tmp/rv3101` 是 fixture 內 agent 自己用的通用路徑（`evidence/s9-rerun/wf31.md:37`）。
  - URL 只有本 repo 的 GitHub issue 與 `example.com`／`example.invalid`。
  - `noreply@anthropic.com` 出現在 fixture agent 的提交命令裡（`wf32-r3.md:28`），屬於受測 agent 的行為紀錄，不是本 repo 的提交。本 repo 16 個提交都沒有 `Co-Authored-By` 或 AI 署名尾行。
- **五項檢查**（reviewer 於 2026-11-11 在 `4d0df5c` 自行執行，工作樹乾淨）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：175 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄。TBD-1～TBD-4 已解決，TBD-5 不影響本次交付，由 #4 追蹤。
- reviewer 沒有實跑宿主 agent。行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture（`runs4/`、`runs5/`）與原始輸出（`raw4/`），這些都沒有進版控。追加輪次第一次執行時產生的 3 份無效證據已被刪除，無法查核，計畫 `:169` 已揭露。
- 渲染以 marked 17.0.5 與 micromark 4.0.2（GFM）加 parse5 7.3.0 為準，沒有在 GitHub 實際渲染。MUST FIX 1、2 的寫法在兩個渲染器的結果相同，而且都只用到 `<details>`，GitHub 的 sanitizer 允許這個標籤。
- 對抗、誤判與變異腳本都在 `<tmp>/review3/`：`adv/cases3.py`、`adv/cases4.py`、`adv/fp3.py`、`adv/render.mjs`、`redrepro/mut.py`，以及紅燈重現的 `redrepro/red.txt`。都沒有進版控。
- 已揭露、不構成缺失的限制：wf32 不穩定；wf30c 沒有執行檢查器；WF-32 的前後比較跨兩種環境；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
