# 審查報告
- 範圍：完整 PR（main..issue-0003-current-state，9 個提交、48 個檔案）
- Reviewed BASE SHA：46e09a5c20cff4cf5ec9db27c20eec0fd8b288e0
- Reviewed HEAD SHA：5c2ca52e5f8641252228707e6cdbe155a15616f8
- Reviewed patch-id：1c69fbf96dad5d570d65c8009a2797ae482dc164（2026-11-10 重算，與委派值相同）
- 獨立 reviewer：獨立 subagent（claude-opus-5-5）
- Review artifact：docs/issues/issue-0003/review-5c2ca52.md
- 審查日期：2026-11-10
- 保存說明：協調者保存時把搜尋過的私有專案名稱、帳號名稱與本機路徑片段改為通用措辭（依本 repo 不寫其他專案資訊的慣例），其餘為 reviewer 原文

## 問題與風險

### MUST FIX

1. **一行不關閉的 HTML 註解就能讓核准的規格在渲染時整段消失，檢查器判有效**：`skills/review/scripts/verify-artifact.py:137-145`（記帳章節的一般行不分辨 HTML 區塊），連帶 `:178-180`（整節新增的章節位置不檢查）。
   - 輸入：流程契約 2.5、README 沒有 `## 現況`。PASS 之後的提交只新增報告，並在 `## 概述` 之後整節新增 `## 現況`（現行 review 與一列外部狀態），節內多一行 `<!--`，不關閉。
   - 實際：`verify-artifact.py` 回報「OK：…變更：新增報告…、現況、現行 review（（無） → review-NEW.md）」。以 marked 13.0.3（GFM）渲染，`## 現況` 之後的 Gherkin 驗收劇本、涉及檔案、核准紀錄、待確認事項、Timeline 與檔尾 metadata 全部進入 HTML 註解。改成節內 `<!--`、Timeline 內 `-->` 兩行時同樣判 OK，被藏住的是兩者之間的所有凍結章節。`<details>…</details>` 跨章節可以把它們折疊起來，同樣判 OK。被審查版本已有 `## 現況` 時，結果相同。
   - 影響：這正是 README「風險與首要驗證」列的最大風險：語意變更藏進現況區塊、沿用 PASS。凍結內容的文字沒變，但人在平台上看不到驗收劇本；agent 讀原文時，會把註解內的內容當成「最終輸出應移除」的說明（本 kit 範本自己就這樣使用 HTML 註解）。
   - 與 v4.9.0 的關係：同一類缺口在 v4.9.0 已經存在，只是需要先在凍結章節之前整節新增 `## Gate 豁免紀錄`（對照組在 2.4 下 base 與 head 都判 OK），issue #2 的已知限制也沒有列出這類寫法。本 PR 規定 `## 現況` 放在 `## 概述` 之後、所有凍結章節之前，把這個前提變成預設版面，曝險因此擴大。
   - 建議：在 `analyse()` 把記帳章節內會跨行的 HTML 區塊開頭當成凍結內容，至少包括同一行沒有 `-->` 的 `<!--`，以及 CommonMark HTML 區塊第 1、6、7 型的開頭（`<details`、`<div`、`<pre`、`<table` 等）。同一行就關閉的 `<!-- … -->` 可以照舊放行，範本的說明註解才不受影響。補上整節新增與既有現況兩種負向案例，以及 Timeline 收尾的跨章節案例；修正後涵蓋全部記帳章節，v4.9.0 的同類缺口一併處理，並寫進 CHANGELOG。

2. **SCN-007 的「只寫連結或事件、不另存目前狀態」沒有落到規則文字；唯一一次實跑中，候選組實際存了狀態副本，判定與登記卻寫成通過或符合**　`需決策`
   - 位置：`docs/AGENTS.md:180`（第 6 項只寫「寫 README 連結或錨定 commit 的事件」，沒有「只」，也沒有「不另存目前狀態」）；`docs/issues/issue-0003/fixtures/expected.md:69`（判準只在「沒有指向 README 或查證」時判失敗）；`docs/issues/issue-0003/implementation-plan.md:31`、`:103`；`docs/issues/issue-0003/README.md:148`（「基準與候選實跑全部通過」）；`docs/rule-verification-status.md:321`、`:332`；`docs/workflow-results/2026-11-10.md:27`。
   - 證據：`evidence/s6-candidate/wf32.md` 的最終輸出寫「今天（2026-11-10）重新查了外部狀態：**併入 main：否**…**production：沒有部署紀錄**」，同一段還宣稱「現況指向 issue README，不另抄一份狀態」。依 SCN-007 原文，這是另存的目前狀態，實作者自己在 `workflow-results/2026-11-10.md:43` 也這樣判斷。
   - 判定：寫定判準和要抓的失敗模式不相交。狀態副本只要附 README 連結就會是綠的，依 `docs/agents/verification.md`「觀測式驗收」的自檢，這類綠燈不能當作證據。`rule-verification-status.md:321` 把「已實跑，無法區分」定義為「候選組行為符合」，第 332 列的交接文件卻掛這個標籤，與實際觀察相反。實作者已經揭露判準較寬（`implementation-plan.md:85` 也寫明 SCN-007 的效果不以本組宣稱），揭露本身不算缺失；缺口在於核准的驗收條件既沒有落到規則文字，觀察到的行為也不符合。
   - 待決問題：SCN-007 要維持原文，還是放寬成允許「帶查證命令與日期的查證結果」？
   - 可選做法：(a) 維持原文：第 6 項改成「只寫 README 連結或錨定 commit 的事件，外部狀態的查證結果寫回 README `## 現況`」；判準改寫成與 SCN-007 原文一致，修正後的判準在實跑前另行提交（舊輪次保留、照實記為依原文未通過），再重跑 WF-32。(b) 放寬 SCN-007：走規格修訂並重新核准，再對齊規則文字與判準。(c) 不修：記入 Gate 豁免紀錄。三種做法都要把 README Timeline、計畫 S6、`rule-verification-status.md:332` 與回歸紀錄裡的「通過」或「無法區分」改成「依 SCN-007 原文未符合（兩組相同）」。
   - reviewer 建議：(a)。下游回報的失誤，正是交接文件裡帶日期的舊值被當成現況；交接文件存一份「併入 main：否」，就是下一次失誤的來源。

### SHOULD FIX

1. **記帳章節對「標題、code fence、粗體欄位」的凍結有多種寫法可以繞過，`## 現況` 全數沿用；其中幾種沒有揭露，也和 review-evidence.md 的說法矛盾**　`需決策`
   - 位置：`skills/review/scripts/verify-artifact.py:18`（LOOSE_FENCE 只吃一層容器前綴）、`:20`（LOOSE_HEADING 只錨定行首的 `<h`）、`:23-24`（FIELD／BOLD_LINE 不含 `1.`／`>` 前綴）；`docs/agents/review-evidence.md:49`、`:51`；`CHANGELOG.md:27`；`docs/rule-verification-status.md:326`。
   - 實測（2.5，整節新增與既有現況兩種都判 OK）：
     - 隱式關閉的巢狀清單 fence，`- - ```gherkin` 或 `1. - ```gherkin` 後面接下一個清單項目。marked 渲染成 `<pre><code class="language-gherkin">`。
     - `1. **分級**: Small`、`> **分級**: Small`：`- **分級**` 判無效，這兩種卻放行。
     - `<pre>`、`<div><h2>…</h2></div>`、`<p><h2>`、`<strong>分級</strong>`、`<b>`。
     - 縮排程式碼區塊。
     - `| a | b |` 接 `---`：欄數不符，渲染成 `<h2>`。
   - 同一組寫法放在 Timeline，2.4 下 base 與 head 都判 OK，所以不是本 PR 引入的。issue #2 只把不在行首的 HTML 標題與粗體、`|` 段落接 `---`、縮排程式碼區塊登記為已知限制（`docs/issues/issue-0002/implementation-plan.md:51`）。巢狀清單 fence、`1.`／`>` 粗體、`<pre>` 沒有揭露，而且 `review-9ee4139.md:68` 寫「巢狀清單 fence 也無效」，那時只測了有明確關閉行的寫法。這些寫法直接牴觸 `review-evidence.md:51`「引用或清單裡的 code fence、以粗體開頭的行…視為凍結內容」，也是 SCN-002「在 ## 現況 內加入標題、code fence…回報無效」的反例。
   - 影響：記帳章節的一般行本來就能寫任意文字，增量風險在於「看起來具權威的格式」，所以列 SHOULD FIX。`## 現況` 位在 README 頂端、又是現況的唯一權威，這種格式最容易被誤讀。
   - 待決問題：要在本 issue 收緊 `analyse()`，還是只在 4.10.0 文件登記 `## 現況` 沿用的已知限制，另開 issue 處理？
   - 可選做法：(a) 收緊：容器前綴改成可重複（`(?:[ \t>]|[-*+][ \t]|\d+[.)][ \t])*`），FIELD／BOLD_LINE 加上 `\d+[.)]` 與 `>`，行內出現 `<h[1-6]`、`<pre`、`<strong>`、`<b>` 時凍結，並補測試。(b) 不收緊：在 review-evidence.md 與 CHANGELOG 寫明 `## 現況` 沿用的放行寫法，並更正 `:51` 的敘述。
   - reviewer 建議：與 MUST FIX 1 一起做 (a)，兩者改的是同一段程式。

2. **docs/AGENTS.md 第 6 項說 README 是「任務清單的狀態」的唯一權威，和任務來源的規則衝突**：`docs/AGENTS.md:180`。Medium／Large 的任務清單在 implementation-plan.md，本 issue 的 `README.md:9` 也寫「任務與證據只維護於 implementation-plan.md」。照字面讀，agent 可能把任務狀態抄進 README，形成第二個來源。計畫的檢查清單「規則文字…沒有兩種說法」（`implementation-plan.md:152`）也還沒勾。建議改成「issue 的現況以 issue 目錄的文件為準：README 的 `**狀態**` 與 `## 現況`，以及任務來源（Small 為 README，Medium／Large 為 implementation-plan.md）的狀態」。

3. **document-types.md 說「每次重新查證就覆寫該列」，沒有查詢模式的例外**：`docs/agents/document-types.md:28`、`:30`。SCN-005 是「推進模式同時更新…，查詢模式只回報」，dev-cycle（`skills/dev-cycle/SKILL.md:12`）也只在推進時覆寫，兩邊說法不同。在 dev-cycle 之外被問到「部署了嗎」時，照 document-types.md 會去改 README；在 2.4 專案或 PASS 之後改，還會影響審查有效性。建議改成「推進或使用者要求更新時覆寫該列；只查詢時回報差異」。

4. **公開 repo 的證據裡留有未遮蔽的本機暫存路徑片段**：`docs/issues/issue-0003/evidence/s6-rerun/wf28a.md:30` 有一段系統暫存目錄的路徑片段。同一行前段已遮成 `<tmp>`，被截斷的後段漏遮。建議改成 `<tmp>`，並讓遮蔽在截斷之前執行。

### NICE TO HAVE

1. `verify-artifact.py:169-174`：2.4 的 README 只要有 `## 現況`，任何違規都會附上「## 現況 列入記帳區段需要流程契約 2.5 以上」，Gherkin 變更也一樣（實測）。建議只在違規項目落在 `現況` 章節，或章節順序因現況而不同時才附註。
2. `docs/issues/issue-0003/implementation-plan.md:36` 寫「143 個測試中 11 個失敗」，但 `evidence/s1-red.txt:120` 是 `Ran 142 tests`。進度字串前綴相同、只少一個 `.`，所以紅燈之後補了一個排在失敗子測試之後的防護案例。reviewer 以最終測試檔配 base 版腳本重跑，得到 143 個測試、11 個失敗，名稱與 s1-red 相同，結論成立。建議更正數字或註明。
3. 雙語 rules 的範圍寬窄不同：中文版（`rules/AGENTS.zh-TW.md:122`）是開放類別「這類會被其他人或其他流程改變的狀態」，英文版（`rules/AGENTS.md:123`）讀起來是封閉的四項。建議英文補上「and similar state that other people or processes can change」。
4. 整節新增的 `## 現況` 位置不受檢查：加在檔尾 metadata 之後或核准紀錄之後都判 OK。`## 現況` 內的連結參照定義（`[x]: url`）因「第一個定義生效」，可以改寫凍結章節裡同名參照連結的目標。兩者都是 v4.9.0 選用章節就有的性質，可以和 MUST FIX 1 一起處理，或登記為已知限制。
5. `skills/dev-cycle/SKILL.md:12`：只為外部狀態建立的 `## 現況` 還沒有任何報告，這時「指標缺漏時回報落差」會誤報，建議限定在「issue 目錄已有報告時」。覆寫外部狀態列在 2.4 專案的 PASS 之後會使審查失效，可加上「流程契約 2.5 起」。
6. `docs/agents/review-evidence.md:35`：報告存在平台時沒有「保存報告的提交」，建議寫明改由更新 README 的那個提交記錄平台連結。
7. code-simplify：
   - `analyse()` 的預設參數（`verify-artifact.py:89`）已無呼叫端使用。
   - `current_review()`（`:156-160`）沒有再比對欄位名，依賴「現況節內只有現行 review 會符合 FIELD」這個不變式。
   - `check_readme`／`compare_readme` 拆開只是為了附註。
   - `build_fixtures.py` 的 `build_external`、`build_reviews`、`build_review_creates_state`、`build_handover` 重複「建規格→提交→實作→回填核准→提交」的流程。
   - 外部狀態表的表頭寫在 `scripts/test-evidence.py:543-548`、`build_fixtures.py:73-81` 與範本三處。
   - 以上都沒有分歧，也不影響正確性。
8. 回歸紀錄「環境」（`docs/workflow-results/2026-11-10.md:7`）可以補一句：隔離設定的 `skills/` 會被 Claude Code 寫入帳號同步的技能（`skills/synced/`）。兩組 wf29 的技能摘要都和同組其他案例不同，原因是這份同步在 wf29 第 1 回合結束時（17:26:42、17:33:48）寫入 `.last-complete-round`／`manifest.json`；kit 技能檔在實跑期間沒有變動，不是重跑。

## 已查核維度

### 驗收與證據

| 編號 | 證據 | 結論 |
|---|---|---|
| SCN-001 | `CurrentStateTests` 五個正向案例；reviewer 的對抗腳本 P1–P6；WF-30、30c、31、28b 的檢查器 OK | 通過 |
| SCN-002 | 測試涵蓋範本寫法（`###`、fence、`**分級**`、`**現行 review:**`、第二行現行 review、搬移、吞併、重複、節外欄位）；reviewer 實測 ATX／縮排 ATX／H1–H6／setext／行首 `<h2>`／`~~~`／引用與單層清單 fence／tab fence／未關閉 fence／`__`、`***`、`**分級：**`／`**狀態**`、`**核准 commit**` 放進現況／搬移 Gherkin 與涉及檔案／吞併概述與 fence／吞併檔尾 metadata／重複／改名／重排／刪標題留內容，全部判無效 | 缺口：MUST FIX 1、SHOULD FIX 1 |
| SCN-003 | 2.4 下 127 個情境與 base 腳本判定、訊息完全相同（只多附註）；2.3、無 AGENTS.md、3.0、3.5 各 6 個情境與 base 完全相同；2.10 視為 2.5 以上 | 通過（附註見 NICE 1） |
| SCN-004 | WF-31（報告提交同時在概述之後建立現況）、WF-31c（對照）、WF-28b 重跑、WF-29 回合 2（覆寫兩列、列數不變） | 通過；覆寫與否無法區分 |
| SCN-005 | WF-29、29b、29c 兩組都先查證 | 行為符合、無法區分；文件說法衝突見 SHOULD FIX 3 |
| SCN-006 | WF-30 只讀 `review-5be35f1.md`；WF-30c 回報指標落差 | 符合；只讀現行報告無法區分 |
| SCN-007 | WF-32 候選組另存「併入 main：否」等狀態 | 依原文未符合：MUST FIX 2 |
| SCN-008 | WF-33 沒有觸發部分範圍；WF-27 掃描重跑全部判定 | 僅靜態撰寫，登記正確 |

其他證據查核：
- **S1 紅燈與綠燈**：以最終測試檔配 base 腳本重跑，11 個失敗，案例名稱與 `s1-red.txt` 相同；HEAD 版 143 個測試全數通過。
- **變異測試**：對新程式做 9 個變異，全部被測試抓到，沒有假綠燈。變異包括現行 review 不限現況、閘門改 2.4／2.6、不檢查重複現行 review、現況不可整節增刪、去掉附註、現況不檢查重複、不列新舊值、現況內粗體全放行。
- **判準先於實跑**：提交順序是 `b26c73a`（fixture 與 expected.md）→ 基準組實跑（證據記錄的 kit HEAD 為 b26c73a）→ `f10c3c1`（追加 wf29b、wf30b 的判準與基準組結果）→ wf29b、wf30b 的基準組與全部候選組實跑（kit HEAD 為 f10c3c1）→ `1732f68`。判準確實在實跑前提交。f10c3c1 對 build_fixtures.py 的修改只新增 legacy、with_state 分支，既有案例的預設行為不變。
- **沒有挑輪次**：唯讀檢查同一 session 暫存區的隔離設定，每個 fixture、每組只有一個 session（wf29 以 resume 跑兩回合），原始輸出也只有一份。
- **逐案核對**：WF-29 兩回合、29b（只多被 gitignore 的 `__pycache__/`、`.deploy/`）、30、31、32、33、28b 與掃描重跑的工具動作、前後雜湊與最終輸出，都和計畫、回歸紀錄的描述相符。

### 相關失敗面

| 失敗面 | 輸入／狀態 | 預期 | 覆蓋與判定 |
|---|---|---|---|
| 契約閘門 | 2.5 以上的 2.x 才把 `現況` 列入記帳區段；2.4 新增現況判無效並附註；2.3、無契約、其他 major 走 legacy | 依規定判定 | 正確；差分比對見上 |
| 現況夾帶凍結內容 | 見上方 SCN-002 | 判無效 | 範本寫法全擋；跨章節 HTML 區塊與多種非範本寫法放行（MUST FIX 1、SHOULD FIX 1） |
| 重複與節外的現行 review | 節內兩行（含 `- **現行 review**`）、Timeline 或待確認事項內、節外改值、節外搬進節內 | 判無效 | 全部判無效 |
| 整節增刪、重排、改名 | 整節刪除、刪除後在別處新增、從概述後搬到 Timeline 前、`現況（舊）`、`##  現況`、`## 現況 ##`、待確認事項與 Timeline 互換 | 有效或無效依規定 | 整節刪除有效，其餘無效，正確 |
| 測試真偽 | 新測試在缺少實作時是否會失敗 | 會失敗 | 紅燈重現、9 個變異全殺 |
| 證據誠實 | 判準與實跑的先後、輪次、判定與標籤 | 一致 | 順序與輪次正確；WF-32 的判定與標籤不正確（MUST FIX 2）；件數小誤（NICE 2） |

### 需求、架構、安全、品質

- **規則一致性**：document-types.md、readme-templates.md 的兩種範本、review-evidence.md、review SKILL 步驟 5、dev-cycle SKILL、pending-scan.md、usage.md、INSTALL.md、CHANGELOG 對 `## 現況` 的位置、兩項內容、現行 review 的更新時機、記帳判定與懸置掃描部分範圍的說法一致。兩種說法有兩處：SHOULD FIX 2、3。SCN-007 的排他性沒有落到規則文字：MUST FIX 2。
- **雙語 rules**：兩檔都在第六節末尾新增一段，`##` 章節數一致（check-kit 通過），語意逐句對應，只有範圍寬窄不同（NICE 3）。
- **核心字串**：被刪除的行都改寫成包含原字串的超集；`**分級**`、`**風險**`、`**狀態**`、`**核准 commit**`、核准狀態、review 判定字串與 `需決策` 都沒有改名。
- **版本**：docs/AGENTS.md 為文件版本 2.9、流程契約 2.5，修訂紀錄 2.9 列、CHANGELOG [4.10.0] 的下游更新、usage.md 與 review-evidence.md 一致。
- **技能最低契約**：維持原值（review 2.1、dev-cycle 2.2、其他 2.0／2.1），check-kit 通過。review 技能以「流程契約 2.5 起」、dev-cycle 以「README 有 `## 現況` 時」作條件，舊專案不會被誤導；邊角情形見 NICE 5。
- **安全與 gate**：檢查器仍然唯讀；本次擴大的豁免範圍有 MUST FIX 1 的跨章節隱藏缺口。核准後 issue README 只改了核准 commit 回填、Timeline 與狀態，規格段落沒有變動。
- **資訊衛生**：
  - diff 沒有 `/home/`、`~/`、`Documents/` 路徑，只有一處系統暫存目錄的路徑片段（SHOULD FIX 4）。
  - 不分大小寫搜尋使用者其他私有專案的名稱、內部主機與帳號名稱，都沒有出現；issue 編號只有 fixture 的合成編號。
  - email 只有 `example.invalid`；GitHub 連結是本 repo 自己。
  - 下游專案一律以「三個下游專案」這類通用措辭出現。
  - 9 個提交訊息都沒有 `Co-Authored-By` 或 AI 署名尾行。
- **code-simplify**：新增的判定程式約 50 行，結構沿用既有程式；重複與過度設計都屬輕微，沒有分歧（NICE 7）。
- **五項檢查（reviewer 於 2026-11-10 在 5c2ca52 自行執行，工作樹乾淨）**：
  - `check-kit.py`：OK
  - `check-links.py`：OK
  - `bash -n scripts/install.sh`：rc 0
  - `test-install.py`：14 項 OK
  - `test-evidence.py`：143 項 OK

### 豁免、待確認與限制

- 沒有 Gate 豁免紀錄；TBD-1 已解決。
- reviewer 沒有自行重跑宿主 agent 實跑，行為面只核對已提交的證據檔，並唯讀檢查同一 session 暫存區的隔離設定與原始輸出目錄（未進版控，與回歸紀錄的說明一致）。
- 渲染結果以本機 marked 13.0.3（GFM）代替 GitHub。HTML 區塊與註解的語意屬 CommonMark 標準，結論應該相同，但沒有在 GitHub 實際渲染。
- 對抗與差分腳本都在 scratchpad（`adv/adversarial.py`、`adv/results.json`、`adv/timeline_probe.py`、`adv/comment_probe.py`、`adv/diff24.py`、`adv/mutate.py`），沒有進版控。
- 已揭露、不構成缺失的限制：每案一輪不能判斷穩定性；外部狀態實查、交接文件、掃描都無法和 v4.9.0 區分；wf30c 的 agent 用了 kit 工作樹的檢查器；平台留言、跨 session 記憶與部分範圍掃描都只有靜態撰寫。

## 流程判定
RETURN TO execute-task
