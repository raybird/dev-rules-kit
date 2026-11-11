# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，13 個提交、60 個檔案）；覆審，重點是上一輪 [review-5c2ca52](review-5c2ca52.md) 之後的修正 `d0e3287..acd488f`
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：acd488fff2506fccc63ae141d97fce0000cfcf07
- Reviewed patch-id：0ff304b8e02bca0713b7768a697e081e1abb9cfb（2026-11-11 以 `git diff 46e09a5 acd488f | git patch-id --stable` 計算）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5），沒有參與實作
- Review artifact：docs/issues/issue-0003/review-acd488f.md
- 審查日期：2026-11-11
- 審查依據：使用者對上一輪需決策項目的決定（README `## 待確認事項` TBD-2～TBD-4）。本報告依這些決定審查，不重新討論方向。

## 問題與風險

### MUST FIX

1. **上一輪 MUST FIX 1 只修了一部分：跨行的 HTML 開始標籤、清單外的標籤，以及既有多行註解的 `-->`，仍能在渲染時藏住所有凍結章節，檢查器判 OK**
   - 位置：`skills/review/scripts/verify-artifact.py:29-32`。`HTML_TAG` 是封閉清單，標籤名後面的 lookahead `(?=[\s>/])` 不接受行尾，而 `:110` 會先 `rstrip()` 每一行，所以 `<details ` 這種結尾帶空白的寫法也會落到行尾。另有 `:34-35`：`HTML_BLOCK` 要求同一行要有 `>`。`:100-102`：只檢查開頭的 `<!--`，不追蹤註解狀態。
   - 實測方式：在 `<tmp>` 建拋棄式 repo，流程契約 2.5，README 已有 `## 現況`。PASS 之後的提交只新增報告，並在 `## 現況` 加入下列寫法。渲染用 marked 17.0.5（GFM）加 parse5 7.3.0（HTML5 規格解析器）確認標記文字的位置，`<details` 那一組另外用 markdown-it 12.3.2（`html: true`）交叉確認。
     | 寫法 | 檢查器 | 渲染結果 |
     |---|---|---|
     | `<details` 單獨一行，下一行接 `class="note">` | OK | Gherkin 驗收劇本、核准紀錄、待確認事項、Timeline 與檔尾 metadata 全部落進收合的 `<details>` |
     | `<details `（結尾空白）單獨一行 | OK | 同上 |
     | 段落內 `補記 <details`，下一行接 `class="n">` | OK | 同上 |
     | `<script`、`<style`、`<textarea`、`<pre` 單獨一行 | OK | CommonMark 第 1 型 HTML 區塊一路延續到檔尾，後面不再做 Markdown 處理，交給瀏覽器後成為標籤屬性或原始文字，Gherkin 與 metadata 都不以文字出現 |
     | 段落內 `補記 <title>`／`<dialog>`／`<select>`／`<noembed>`／`<xmp>` | OK | 後續全部內容落進預設不顯示的元素（沒有 sanitizer 的渲染器） |
     | 段落內 `補記 <s>`／`<strike>`／`<a href="#x">`／`<small>`／`<code>`／`<i>`／`<em>`／`<u>` | OK | HTML5 會在後面每個區塊重建這些格式元素，整份 Gherkin 與 metadata 都變成刪除線、連結或小字 |
   - 以下兩種情況結果相同。整節新增 `## 現況` 時判 OK，且同樣藏住後文（訊息為「現況、現行 review（（無） → …）」）。流程契約 2.4 時寫在 `## 待確認事項`（`<details` 換行），判 OK，Timeline 與 metadata 被收合。
   - 既有多行註解的 `-->`：被審查版本的待確認事項如果有一段 `<!--`／說明／`-->` 的多行註解，之後的提交刪掉 `-->` 那行，或把它搬到 Timeline 的表格之後，都判 OK。渲染時，從註解開頭到檔尾（或到搬過去的位置）全部變成註解。原因在 `analyse()`：只凍結開頭那行，`-->` 被當成一般記帳行；而且記帳行和凍結行的相對順序（`sections` 與 `frozen` 分開存放）沒有比對。範本的註解都在同一行關閉，所以這條需要 issue 自己留有多行註解才會發生。
   - 對照組：同樣位置寫完整的 `<details><summary>x</summary>` 或一行 `<!--`，判 INVALID，也就是 S8 測試涵蓋的寫法確實擋住了。
   - 與規則文字的落差：`docs/agents/review-evidence.md:51` 寫「HTML 標籤（例如 `<h2>`、`<pre>`、`<details>`、`<strong>`、`<b>`）…視為凍結內容；同一行就關閉的註解與 `<br>` 照一般行處理」，讀起來是 `<br>` 以外的標籤都凍結，實作卻是封閉清單，而且不認行尾。`CHANGELOG.md:30` 也說原本的藏住問題已經解決。
   - 影響：和上一輪 MUST FIX 1 是同一個失敗形態，只是寫法不同：記帳提交藏住核准的驗收劇本，PASS 照樣沿用。這正是 README「風險與首要驗證」列的最大風險。`<details>` 是 GitHub 允許的標籤，而 cmark-gfm 依 CommonMark 規格，把「`<details` 後接行尾」視為第 6 型 HTML 區塊的開頭，所以這條在 GitHub 上應該同樣成立（沒有實際在 GitHub 渲染）。
   - 建議：
     - 改成允許清單：記帳章節裡只要出現 `<` 後接字母、`/`、`!` 或 `?` 的行，一律凍結；只放行 `<br>`、`<br/>`、`<wbr>` 與同一行就關閉的 `<!-- … -->`。這樣就不必判斷標籤會不會藏住內容，行尾與跨行的寫法也一併擋住。範本與測試裡的 `<sha>` 這類佔位字，改寫在 code span 裡；不放在 code span 時，GitHub 本來就會把它當成未知標籤刪掉。
     - 追蹤 HTML 註解的狀態，做法比照 fence：開頭沒有關閉時，後續每一行到 `-->` 為止都算凍結內容，含 `-->` 那行。
     - 補上 `<details` 換行、行尾帶空白、`<script` 單獨一行、行內 `<title>`／`<s>`，以及刪除既有 `-->` 的負向案例，整節新增與既有現況兩種都要。
     - `review-evidence.md:51` 與 `CHANGELOG.md:30` 的敘述跟著實作更新。

### SHOULD FIX

1. **清單與引用裡的 setext 標題沒有凍結，和 TBD-3「巢狀容器一起收緊」的決定以及 review-evidence.md:51 的說法矛盾**
   - 位置：`verify-artifact.py:24-25`、`:139`。`SETEXT` 只接受行首 0～3 個空白，前一行是清單或引用（`NOT_PARAGRAPH`）時就略過不判。
   - 實測（2.5，`## 現況` 內，判 OK）：
     - `- 驗收條件已變更` 下一行接 `  ===`：marked 與 markdown-it 都渲染成 `<ul><li><h1>`。
     - `> 驗收條件已變更` 下一行接 `> ---`：渲染成 `<blockquote><h2>`。
   - 影響：這和上一輪 SHOULD FIX 1 是同一類缺口，屬於偽造看起來有權威的格式，不會藏住凍結內容。`review-evidence.md:51` 寫「看起來像標題的行…（含多層引用與清單、編號清單裡的寫法）…視為凍結內容」，和實作不符。
   - 建議：底線行先剝掉容器前綴（`CONTAINER`）再比對 `SETEXT`；前一行同樣剝掉容器前綴後，只要是段落文字就凍結。如果暫時不修，就登記成已知限制，並更正 `:51` 的敘述。

2. **收緊之後，記帳章節裡寫在 code span 的標籤名會被判 INVALID；這會改變 2.4 下游原本有效的記帳提交，但文件沒有提醒**
   - 位置：`verify-artifact.py:100-102`。`HTML_TAG.search`／`rfind('<!--')` 會掃整行，不排除 code span，也不排除反斜線跳脫。
   - 實測（v4.9.0 的檢查器在相同輸入下全部判 OK，新檢查器的結果如下）：
     - Timeline 列寫「修正 `` `<template>` `` 的生命週期」：INVALID。
     - Timeline 列寫「改用 `` `<table>` `` 呈現」：INVALID。
     - Timeline 列寫「修正未關閉的 `` `<!--` ``」：INVALID。
     - 待確認事項列寫「是否改用 `` `<details>` `` 摺疊」：INVALID。
     - `\<div>` 跳脫寫法：INVALID。
     - Timeline 用 `1. **2026-11-11**：…`：INVALID。
     - code span 裡的 `<title>`：OK，因為 `title` 不在清單上，判定不一致。
   - 影響：會誤判的都是安全的寫法，渲染成文字，不會藏住內容。代價是重新審查，而下游調查指出「記帳提交讓 PASS 失效」正是最大的使用成本。網頁類專案在 Timeline 提到元素名稱很常見。`CHANGELOG.md:30` 只提醒「編號清單加粗體寫豁免紀錄」，`docs/AGENTS.md:129` 的 Gate 豁免紀錄寫法說明、待確認事項與 Timeline 的說明，都沒有提到標籤。
   - 建議：在 MUST FIX 1 的判定之前，先移除同一行就成對關閉的 code span。要依 CommonMark 的規則處理反斜線跳脫的 backtick 與 backtick 串的長度，否則 `` \`<details>\` `` 這種寫法會被當成 code span 放行。如果不排除，就在 CHANGELOG「下游更新」與 `docs/AGENTS.md:129` 寫明：記帳章節（含 Timeline、待確認事項）不寫標籤名，編號清單加粗體也不能用。另外把 `CHANGELOG.md:30` 的「豁免紀錄」改成「記帳章節」。

3. **發布文件沒有跟上 S8 的結果**
   - `CHANGELOG.md:46` 還寫「`test-evidence.py` 143 項」，目前是 159 項。
   - `CHANGELOG.md:49` 還寫交接文件「兩組行為相同…沒有可觀察的效果」，也沒有提到審查後的重跑。依 S8，2026-11-10 兩組都依原文重判為未符合，2026-11-11 候選組依原文通過。
   - `docs/workflow-regression.md:55` 還寫「WF-32 只依較寬的寫定判準通過」，沒有指向「審查後重跑」。
   - `docs/issues/issue-0003/implementation-plan.md:31` 的 S6 列還寫「全部通過」，同檔 `:83`、`:104` 的 wf32 已經改判。
   - 影響：CHANGELOG 是給下游看的產品，與 `docs/rule-verification-status.md:333`、`docs/workflow-results/2026-11-10.md` 的說法不同。
   - 建議：四處都改成 S8 的結論，並註明每案一輪。

4. **wf32 重跑時，agent 把交接文件提交到 issue 分支，讓 PASS 失效；它沒有告知使用者，還把「合併進 main」列為下一步。紀錄只寫了 PASS 失效，這兩點沒有寫**　`需決策`
   - 證據：
     - `evidence/s8-rerun/wf32.md` 的最終輸出寫「下一步是用 `--no-ff` 把分支合併進 `main`」，全文沒有提到 PASS 失效或需要重審。原始 stream-json（`<tmp>` 的 `raw3/cand/wf32-turn1.jsonl`）裡也找不到「失效」「重新審查」「verify-artifact」。
     - fixture 的最終提交 `ee1c549` 同時改了 `docs/handover.md` 與 README，以新檢查器判定為 INVALID，與計畫 `:130` 相符。
     - `docs/workflow-results/2026-11-10.md:61` 只寫「結果讓 PASS 失效」。
   - 判定：照 SCN-007 原文，wf32 通過是正確的，交接文件的內容我也在 `<tmp>` 的 fixture 裡逐字核對過。不過這一輪觀察到的，正是本 issue 最高風險的失敗形態：一個沒人發現的假 PASS，下一步還是合併。這個失敗形態被低估了。上一輪兩組都停下來問，這一輪沒有，這個行為差異也沒有記下來。
   - 待決問題：要不要在本 issue 處理「交接文件放在 issue 目錄外，提交到 issue 分支就會讓 PASS 失效」？
   - 可選做法：
     - (a) 只補紀錄：在 workflow-results 與 rule-verification-status 寫明 agent 沒有告知 PASS 失效、還建議合併，另開 issue 處理。
     - (b) 在本 issue 補一句規則。例如 rules 或 docs/AGENTS.md：審查之後要在被審查分支提交記帳以外的檔案時，先說明會讓 PASS 失效；或者寫明交接文件應提交到哪裡。改完再重跑 wf32。
   - reviewer 建議：(a)。這不是 SCN-007 的範圍，靠 create-pr 的有效性檢查也還能擋住，但紀錄必須照實寫。

5. **`**現行 review**` 的格式：核准規格寫「檔名」，規則文字寫「repo-relative 路徑」，本 repo 與 fixture 用的是檔名**
   - 位置：
     - 核准規格：`docs/issues/issue-0003/README.md:35`（設計邊界）寫「本機報告的檔名或平台報告的連結」。
     - 規則文字：`docs/agents/document-types.md:27`、`docs/agents/readme-templates.md:42`、`:144`、`docs/agents/review-evidence.md:35` 都寫「repo-relative 路徑」。
     - 實際寫法：本 issue README 是 `**現行 review**: review-5c2ca52.md`；wf30 fixture 用檔名；wf31 的 agent 寫成相對連結 `[review-ec7d642.md](review-ec7d642.md)`；WF-28b 的 agent 寫 repo-relative 路徑。
   - 影響：同一個欄位實際出現三種寫法。dev-cycle 要判斷「指向不存在的檔案」（`skills/dev-cycle/SKILL.md:12`），如果照規則把檔名當成 repo 相對路徑解析，會誤報落差。規則文字也偏離了核准規格的措辭。上一輪沒有指出這一點。
   - 建議：規則與範本改成「issue 目錄內的報告檔名（或 repo-relative 路徑）或平台連結」，並寫明以 issue 目錄解析。這樣與核准規格一致，不必重新核准。

### NICE TO HAVE

1. 上一輪 NICE 4 的後半沒有修，也沒有登記：`## 現況` 裡的連結參照定義（`[spec]: https://…`）會覆蓋凍結章節的同名參照，因為第一個定義生效（實測判 OK，marked 輸出的 `href` 換成新的目標）。TBD-4 只登記了「現況位置」。建議登記成已知限制，或把記帳章節裡 `^\s*\[[^\]]+\]:` 開頭的行列為凍結。
2. 測試缺口：從 `HTML_TAG` 拿掉 `details` 之後，159 個測試仍然全過（變異 M4）。`<details><summary>` 的案例是靠 `summary` 擋住的，獨佔一行的 `<details>` 則由 `HTML_BLOCK` 擋住。建議補一個行內、不帶 `<summary>` 的 `<details>` 案例；MUST FIX 1 改成允許清單之後，這個問題自然消失。
3. `docs/workflow-results/2026-11-10.md:51` 寫重跑「環境同上」，但同檔 `:62` 說 fixture 已經移到只允許 fixture 目錄的沙箱。WF-32 的「已實跑驗證（僅候選組）」（`docs/rule-verification-status.md:333`）比的是 2026-11-10 的基準組與 2026-11-11 的候選組，兩次環境不同，而且各只跑一輪。建議在環境段寫明這項差異。另外，`:333` 的「基準組沒有對新文字重跑」語意不清，建議改成「基準組沒有在同一環境重跑」。
4. `evidence/s8-rerun/pre-fix/wf29d.md:5` 的 kit HEAD 記為 `9456504`，實際用的技能來自 `git archive d0e3287`。計畫 `:126` 有說明，但證據檔本身沒有。建議在檔頭補一行技能來源。
5. wf32 的證據沒有保存 agent 寫出的 `docs/handover.md` 全文：工具動作被截斷，最終輸出是 agent 自述。判定目前要靠未進版控的暫存區，而 2026-11-10 那輪的原始檔已經不在了。建議 run_case 在回合結束後，把該回合新增提交的 `git show --stat` 與文件 diff 寫進證據。
6. `docs/AGENTS.md:180` 的「外部狀態的查證結果寫回 README 的 `## 現況`」沒有條件；`docs/agents/document-types.md:30` 則是只查詢時不改檔。建議改成「需要保存查證結果時寫回…（時機見 document-types.md）」。
7. 上一輪 NICE 5 的後半（外部狀態列覆寫在 2.4 專案會讓 PASS 失效）沒有處理。因為 `## 現況` 只在 2.5 定義，影響很小，記下即可。
8. SCN-003 的 And 子句「只改 Timeline…的提交判定與現行相同」，與 TBD-3「所有記帳章節變嚴」字面上衝突：2.4 專案在 HTML 與巢狀寫法上的判定已經改變。使用者的決定已經記在 TBD-3，方向不必重議。建議在 TBD-3 的影響欄註明「SCN-003 的『與現行相同』不含 HTML 與巢狀寫法的收緊」，讓之後查核規格與實作的人不必自己推論。

### 需決策

- SHOULD FIX 4：交接文件提交讓 PASS 失效、agent 卻沒有告知，要在本 issue 補規則，還是只補紀錄、另開 issue（reviewer 建議只補紀錄）。
- 其餘發現都有明確修法，不需要使用者決定。

## 已查核維度

### 上一輪發現的處理（依 TBD-2～TBD-4）

| 上一輪 | 決定 | 處理與依據 | 結論 |
|---|---|---|---|
| MUST FIX 1 跨行 HTML 區塊 | 修 | `verify-artifact.py:28-35`、`:100-102`、`:135-138`。一行 `<!--` 與完整的 `<details><summary>` 都判 INVALID（對照組），但跨行標籤、清單外標籤與既有 `-->` 仍判 OK | 部分完成 → 本輪 MUST FIX 1 |
| MUST FIX 2 SCN-007 | TBD-2 維持原文 | `docs/AGENTS.md:180` 已改成「只寫…不另存目前狀態或查證結果」。重跑判準在 `9456504` 先提交，重跑在後（見下方「判準先於重跑」）。舊輪次重判為未符合：計畫 `:83`、`:104`，`rule-verification-status.md:333`，`workflow-results/2026-11-10.md:28`、`:44` | 完成；有兩處漏改（SHOULD FIX 3） |
| SHOULD FIX 1 繞過寫法 | TBD-3 一起收緊 | `CONTAINER`（`:19`）套到 fence、ATX、FIELD、BOLD_LINE。`- - ```、1. - ```、1. **分級**、> **分級**、> ## …、<pre>、<strong>、<b>、行內 <h2>` 都判 INVALID（測試 `test_html_and_nested_forms_frozen_in_bookkeeping`）；縮排程式碼區塊與表格接 `---` 已登記（`CHANGELOG.md:31`） | 大致完成；容器內 setext 未收緊（SHOULD FIX 1） |
| SHOULD FIX 2 任務清單的權威來源 | 修 | `docs/AGENTS.md:180` 改成「任務來源（Small 在 README，Medium／Large 在 implementation-plan.md）的任務狀態」 | 完成 |
| SHOULD FIX 3 查詢模式的例外 | 修 | `docs/agents/document-types.md:28`、`:30`：「推進工作或使用者要求更新時覆寫該列；只查詢時回報差異，不改檔」。與 dev-cycle `:12` 一致 | 完成 |
| SHOULD FIX 4 暫存路徑漏遮 | 修 | `evidence/s6-rerun/wf28a.md:30` 已改成 `<tmp>`。`docs/issues/issue-0001/fixtures/run_case.py:38-47` 加入 kit 工作樹與系統暫存目錄的遮蔽，在截斷前執行 | 完成 |
| NICE 1 2.4 附註 | 修 | `verify-artifact.py:190-192` 只在現況的凍結內容或有無改變時附註；測試 `test_current_state_note_only_when_relevant` | 完成 |
| NICE 2 測試件數 | 修 | 計畫 `:37` 已更正為 142 個並說明原因 | 完成 |
| NICE 3 雙語範圍 | 修 | `rules/AGENTS.md:123` 補上「and similar state that other people or other processes can change」，與 `rules/AGENTS.zh-TW.md:122` 的開放類別對應 | 完成 |
| NICE 4 現況位置與連結參照 | 位置登記為已知限制 | `review-evidence.md:49`、`CHANGELOG.md:31` 已登記位置；連結參照的部分沒有處理也沒有登記 | 部分 → NICE 1 |
| NICE 5 dev-cycle 誤報 | 修 | `skills/dev-cycle/SKILL.md:12` 限定為「issue 已有審查報告而…」；wf29d 前後兩輪都沒有誤報（照實記為無法區分） | 前半完成，後半見 NICE 7 |
| NICE 6 平台報告的提交 | 修 | `review-evidence.md:35`、CHANGELOG `:29` | 完成 |
| NICE 7 code-simplify | 只清掉預設參數 | `analyse(text, bookkeeping_sections)`（`:105`），沒有預設值 | 完成 |
| NICE 8 技能摘要 | 修 | `workflow-results/2026-11-10.md:13`、計畫 `:139` | 完成 |

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | CurrentStateTests 正向案例；`d0e3287` 以新檢查器判 OK（reviewer 重跑）；wf31（`85b3041`）、WF-28b（`407ee6d`）由 reviewer 在 `<tmp>` 的 fixture 以新檢查器重跑，判 OK；S2 範本檢查以新檢查器重跑，2.5 判 OK、2.4 判 INVALID 並附註 | 通過 |
| SCN-002 | S8 新增 41 個負向案例。reviewer 以 d0e3287 版腳本配最終測試檔重現 159 個測試、41 個失敗，失敗名稱與 `s8-red.txt` 相符；HEAD 版 159 個全過 | 缺口：MUST FIX 1、SHOULD FIX 1 |
| SCN-003 | 2.4、2.3、無契約的既有案例仍然全過。本 repo 歷史上 11 份審查報告的提交，新舊檢查器判定一致（10 份相同；`d0e3287` 舊版判 INVALID 是因為 2.4 不認 `## 現況`，屬預期） | 通過；收緊造成的判定差異見 SHOULD FIX 2 與 NICE 8 |
| SCN-004 | wf29 兩回合重跑（查詢不改檔、推進覆寫兩列）；wf31、WF-28b 的現況都建立在概述之後 | 通過（無法區分） |
| SCN-005 | wf29、wf29d 重跑都先查證，查詢時詢問是否改列 | 通過（無法區分） |
| SCN-006 | wf30c 重跑回報指標落差，手動判有效；沒有執行檢查器，已照實記為部分未符合 | 符合，揭露正確 |
| SCN-007 | wf32 重跑：handover.md 只有 README 連結與三個錨定 commit 的事件（reviewer 在 `<tmp>` 的 fixture 核對全文）；查證日期寫回 README | 依原文通過；附帶觀察見 SHOULD FIX 4 |
| SCN-008 | 未觸發，登記為僅靜態撰寫 | 登記正確 |

其他證據查核：
- **判準先於重跑**：`9456504`（expected.md「審查後重跑」與 wf29d 的 fixture）的提交時間是 2026-11-11 10:51:12。s8-rerun 的每個證據檔都記錄 kit HEAD `9456504`，SHA 不可能事先得知。fixture wf32 的重跑提交 `ee1c549` 時間是 10:52:29，結果在 `acd488f`（10:59:03）才提交。判準確實先於重跑。`3e448fc` 與 `9456504` 的時間戳相同，但兩者都在重跑之前。
- **紅燈與變異測試**：紅燈可以重現（見上表）。對新程式做 12 個變異：拿掉註解判定、拿掉 HTML_BLOCK、容器不可重複、拿掉 `pre`、拿掉 `strong|b`、附註永遠出現、刪除 html 分支、LOOSE_HEADING 不吃容器、FIELD 與 BOLD_LINE 同時不吃容器，都被測試抓到。只有拿掉 `details` 存活（NICE 2）。FIELD 或 BOLD_LINE 單獨不吃容器也會存活，但兩者互為備援，不算缺口。
- **重跑紀錄**：wf29、wf29d（前後兩輪）、wf30c、wf31、wf32、WF-28b 的工具動作與最終輸出，都和計畫 S8 表格、README Timeline 和 workflow-results「審查後重跑」相符；wf30c 的「部分未符合」也照實寫明，沒有誇大。誇大或過時的只有 SHOULD FIX 3 列的四處。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 記帳章節藏住凍結內容 | `<details` 換行、`<script` 等單獨一行、行內清單外標籤、格式元素、刪除或搬移既有 `-->` | INVALID | 判 OK，渲染時藏住或改變後文（MUST FIX 1） |
| 記帳章節偽造標題 | 清單或引用裡的 setext | INVALID | 判 OK（SHOULD FIX 1） |
| 正當記帳更新 | code span 裡的標籤名、`\<div>`、編號清單加粗體的 Timeline | 依安全性應判 OK，或事先告知 | 判 INVALID（SHOULD FIX 2）；`<br/>`、`<br />`、同一行關閉的註解、一般編號清單判 OK |
| 契約閘門 | 2.4、2.5，整節新增與既有現況 | 依規定判定 | 正確；附註只在現況變動時出現 |
| 證據誠實 | 判準與重跑的順序、標籤、發布文件 | 一致 | 順序正確；四處過時（SHOULD FIX 3）；wf32 的附帶失敗低報（SHOULD FIX 4） |

### 需求、架構、安全、品質

- **規則一致性**：
  - docs/AGENTS.md 第 6 項、document-types.md、review-evidence.md、review SKILL、dev-cycle SKILL、usage.md、CHANGELOG 對 `## 現況`、查詢與推進、只寫連結或錨定事件的說法一致。
  - 新的矛盾有三處：`review-evidence.md:51` 與實作不符（MUST FIX 1、SHOULD FIX 1）；`**現行 review**` 的格式與核准規格不同（SHOULD FIX 5）；第 6 項的寫回沒有條件（NICE 6）。
- **雙語 rules**：兩段逐句對應：適用範圍是開放類別、來源、對外陳述或行動前查證、結果不同時以實查為準並指出差異、查不到時附來源與日期。check-kit 通過，`##` 章節數一致。
- **核准範圍**：自核准提交 `fe43877` 起，README 只改了 `## 現況`、核准 commit 回填、待確認事項 TBD-2～4、Timeline 與狀態，Gherkin 與設計邊界沒有變動。
- **安全與 gate**：檢查器仍然唯讀。豁免範圍內的藏住缺口仍在（MUST FIX 1）。
- **code-simplify**：`html()` 一個函式供所有記帳章節共用，沒有新的重複。`HTML_TAG` 的封閉清單同時造成漏放（MUST FIX 1）與不一致（code span 裡的 `<title>` 放行、`<table>` 凍結），改成允許清單可以一起簡化。
- **資訊衛生**：
  - 在 `46e09a5..acd488f` 的新增行中搜尋 `/home/`、`/tmp/claude`、`claude-1000`、`/Users/`、`Documents/`、`.claude/projects`、`-home-`，以及家目錄名與帳號名，都沒有結果。
  - `/tmp/red.log` 是 fixture 內 agent 自己用的通用路徑；`~/.claude/skills/review/` 是遮蔽後的家目錄（`evidence/s8-rerun/wf30c.md:32`），不含個人資訊。
  - email 只有 `example.invalid`；URL 只有本 repo 的 GitHub issue；13 個提交訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。
- **五項檢查**（reviewer 於 2026-11-11 在 `acd488f` 自行執行，工作樹乾淨）：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：159 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄；TBD-1～TBD-4 都已解決，本報告依這些決定審查。
- reviewer 沒有實跑宿主 agent，行為面只核對已提交的證據，並唯讀查看同一 session 暫存區的 fixture 與原始輸出（`runs3/`、`raw3/`，未進版控）。
- 渲染以 marked 17.0.5、markdown-it 12.3.2 與 parse5 7.3.0 為準，沒有在 GitHub 實際渲染。GitHub 會濾掉 `<title>`、`<dialog>`、`<script>` 這類標籤，所以 MUST FIX 1 在 GitHub 上成立的部分以 `<details` 換行為主；其餘寫法在沒有 sanitizer 的渲染器（例如直接交給瀏覽器的 marked 輸出），以及讀原始文字的 agent 身上成立。
- 對抗與重現腳本都放在 `<tmp>/review2/adv/`（`probe.py`、`cases.py`、`fp.py`、`render.mjs`、`verify-base.py`）與 `<tmp>/review2/redrepro/`，沒有進版控。
- 已揭露、不構成缺失的限制：每案一輪；wf29d 修正前後無法區分；wf30c 沒有執行檢查器；平台留言、記憶與部分範圍的掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
