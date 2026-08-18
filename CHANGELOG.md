# Changelog

本檔案記錄 dev-rules-kit 的重要變更，供下游專案更新已複製的檔案時參考。

**版本策略**：重要變更時打 git tag，規則如下——

- **Major**：破壞性變更（規則語意反轉、目錄結構調整、skill 改名或移除），下游更新前應檢視自己的客製內容
- **Minor**：新增 skill / workflow / 規則章節，下游可安全重新複製
- **Patch**：錯字修正、文字調整、文件補充，不影響行為

每個條目標注影響的目錄，方便下游判斷是否需要重新複製對應檔案。

---

## [2.13.0] - 2026-08-18

### 新增（`skills/writing-rules`、`workflows/shared/writing-rules.md`、`CLAUDE.md` — 下游可選擇性複製）

- **新增 `writing-rules` 技能**：本 repo 整個就是一堆 agent 會讀的文件，卻沒有任何東西規定它們該怎麼寫——既有約定散在 `CLAUDE.md` 的 Conventions，全屬格式層（description 寫法、檔名、雙語同步），沒有一條談注意力成本與觸發機制。

  後果是可觀測的：`docs/AGENTS.md` 曾在一天內從 686 行長到 797 行，其中還包含一個名為「精簡」的版本；盤點時有 46 處否定式指令、全檔零漸進揭露。v2.11.0 與 v2.12.0 修掉了結果，但**紀律本身沒有留在 repo 裡**，下次仍會以同樣方式重新累積。**沒有這道紀律時，增補永遠比刪減安全。**

  本技能涵蓋：pointer 措辭決定何時被讀到（弱 pointer + 必讀材料 = 變異來源，且不報錯）、in-file 與 disclosed 的 branching 取捨與 sprawl、正面表述、完成判準的清晰度與強度及提早結案的機制（藏後續步驟只在跨 context 邊界時有效）、leading word 優先於自創詞、單一真相來源與環境即真相來源、no-op 測試（判準相對於模型而非讀者，靠跑而非辯論解決）。另含本 kit 的額外約束：核心層字串維持原樣、雙語章節數相等、改完跑 `sync-skills.py --check`。

  `CLAUDE.md` 新增指向，要求修改任何規範文件前先套用。

  來源：[mattpocock/skills](https://github.com/mattpocock/skills) 的 `productivity/writing-for-agents`。本版是把該檔的原則沉澱成本 repo 可重複套用的紀律，而非再做一次一次性的改寫。

## [2.12.0] - 2026-08-18

### 變更（`docs/AGENTS.md` + 新增 `docs/agents/` — **下游改為複製整個目錄**；`skills/new-issue`、`workflows/shared/new-issue.md` 需重新複製）

- **以漸進揭露拆分 issue 文件規範**：`docs/AGENTS.md` 已長到 797 行且全部 in-file，沒有任何由 pointer 觸發的參考檔。過長本身就是一種失效——**即使每一行都有效且不重複，注意力仍會在多餘的篇幅上變薄**，而每多一行就多一行要維持相關性。

  判斷哪些該推出去用的是 **branching 測試**：每條流程分支都需要的留在主檔，只有部分分支會走到的推到 pointer 後面。據此移出四塊——「文件類型與內容規範」「README.md 範本」「常見文件類型範例」（只有建立或改寫 issue 文件的分支會走到）與「快速檢查清單」（只有 `new-issue` 收尾會走到）：

  | 檔案 | 何時載入 |
  |---|---|
  | `docs/agents/document-types.md` | 決定某份文件該寫什麼內容、查既有議題的文件組合範例 |
  | `docs/agents/readme-templates.md` | 建立或改寫 issue README |
  | `docs/agents/issue-checklist.md` | `new-issue` 結束前逐項驗收 |

  主檔 **797 → 534 行**，留下的是每條路徑都要讀的：客製邊界、分級與風險、BDD 驗收規格與 TDD 證據、核准紀錄與查核、待確認事項、合法狀態、常青文件責任、日期規範。主檔於各原位置留下 context pointer，敘明該參考檔涵蓋什麼與何時該讀；「客製邊界與同步策略」新增目錄結構說明。

  **下游同步方式改變**：本規範現在是一個目錄，複製時 `docs/AGENTS.md` 與 `docs/agents/` 一併複製。三份參考檔與主檔同屬一套規範，版本以主檔檔尾的 `**文件版本**` 為準（參考檔不各自編版）。`new-issue` 的「讀取權威規範」與完成 gate 已改為指向對應參考檔。

  來源：[mattpocock/skills](https://github.com/mattpocock/skills) 的 `productivity/writing-for-agents`，其 information hierarchy 與 progressive disclosure 章節。

## [2.11.0] - 2026-08-18

### 變更（`docs/AGENTS.md`、`rules/`、`skills/`、`workflows/shared/` — **下游需重新複製規範、規則檔與 `execute-task`、`review`**）

- **將否定式指令改寫為正面目標**：以禁令操控行為有個已知的反效果——**它把被禁的行為拉進 context，反而讓那個行為更容易被觸發**（"don't think of an elephant"）。禁令是弱修飾詞，會被它所強烈啟動的概念蓋過去，半句讀起來像是在指示做那件事。

  盤點後 `docs/AGENTS.md` 有 46 處否定式指令、平均每 17 行一處，`rules/AGENTS.zh-TW.md` 34 處、平均每 7 行一處。本次改寫 16 處為直述目標行為，`docs/AGENTS.md` 降至 27 處。例子：

  - 「不得先決定採用垂直切片，再回頭尋找理由」→「順序是先指出最大的未驗證假設，再由它決定手段」（原句把錯誤流程完整描述了一遍）
  - 「`待核准` 的 Scenario 不得實作」→「實作範圍僅限狀態為 `已核准` 的 Scenario」
  - 「分批核准時不得使用單行形式」→「分批核准時一律使用逐項表格」
  - 「不得判 MUST FIX、不得歸入假綠燈、不得據此退回實作」→「列 SHOULD FIX 並提出更穩固的替代斷言，本次驗收的判定維持通過」（連續三個否定改為一個正面目標）
  - 「不應直接抹除舊文件的歷史描述」→「保留舊敘述並在其旁補上帶日期的說明」

  **規則語意完全未變**，改的只是表述方向。保留否定的是無法正面表述的硬護欄（假綠燈不得作為證據、誠實回報不可豁免），且都已配上正面目標。

  來源：[mattpocock/skills](https://github.com/mattpocock/skills) 的 `productivity/writing-for-agents`，其 Leading words 章節將 negation 列為與 leading word 並列的失效模式。

## [2.10.0] - 2026-08-18

### 新增（`docs/AGENTS.md`、`rules/`、`skills/`、`workflows/shared/` — **下游需重新複製規範、規則檔與 `execute-task`、`review`**）

- **「假綠燈」新增同義反覆（tautological）條目**：原清單涵蓋了刪測試、mock 掉待驗收行為、硬編碼答案、無 assertion，但漏掉一個更隱蔽的變體——**斷言以與被測程式碼相同的方式重算期望值**（`expect(add(a, b)).toBe(a + b)`、以手算重跑一次相同實作邏輯得到的 snapshot）。它 passes by construction，永遠不可能與程式碼意見不合，因此測不出任何東西，而它的紅綠燈看起來完全正常。

  現要求**期望值必須來自獨立的真相來源**（已知良好的字面值、人工推導的實例、規格原文、或另一條不共用實作的取得路徑），判斷方式是問「**這個斷言有沒有可能與程式碼意見不合？**」——不可能，它就不是測試。`execute-task` 在 TDD 內迴圈紅燈階段即要求，`review` 對同義反覆列 MUST FIX，雙語規則檔一併補上。

  規範同時點明它與 2.8.0「觀測式驗收」反向自檢是**同一機制的兩種形態**：同義反覆是斷言與實作不獨立，觀測式假綠燈是判準與失敗模式不相交，兩者的綠燈都來自判準本身失效而非行為正確。

  來源：[mattpocock/skills](https://github.com/mattpocock/skills) 的 `engineering/tdd` 技能，其 anti-patterns 章節將 tautological 與 implementation-coupled、horizontal slicing 並列。

## [2.9.1] - 2026-08-18

### 新增（`docs/rule-verification-status.md`、`CLAUDE.md` — 下游不需重新複製）

- **新增規則驗證狀態文件**：本日 v2.6.0 至 v2.9.0 出現三個「規則寫得完整、但根本執行不了」的缺陷（2.7.0 分批誤用單行核准表使查核靜默通過、2.8.0 回填驗證對象寫成 `HEAD` 導致驗證等於沒驗、2.9.0 齊備性檢查只定義一端版本因而無法比對），三者都是當天新寫的規則，在紙上都成立，是有人真的去執行才垮的。靜態審查能檢查規則自不自洽，檢查不了它可不可執行。

  因此新增 [`docs/rule-verification-status.md`](docs/rule-verification-status.md)，逐條記錄每條規則是否被實際執行過，狀態分為已實跑驗證／本地測試驗證／來源為實跑（動機來自實跑但規則本身未被套用）／僅靜態撰寫／曾失效並修正。**未標為已驗證者應視為「可能有同類缺陷、尚未被發現」**，而非「已經生效」。

  同時記錄已知的驗證限制：樣本數 n=2 且同源（兩專案共有的盲點照不出來）、回饋迴路人力密集且無常設機制、規則總量淨成長（`docs/AGENTS.md` 686 → 780 行）、以及今日新規則的缺陷率偏高。該檔是 kit 自身的維護紀錄，不供下游複製；`CLAUDE.md` 新增指向與維護要求。

## [2.9.0] - 2026-08-18

### 修正（`docs/AGENTS.md`、`skills/`、`workflows/shared/`、`scripts/` — **下游需重新複製規範與全部技能**）

- **核心層齊備性檢查補上 skill 端的版本宣告**：2.8.0 要求 agent 在規範版本落後時停下來問，判斷依據卻只定義了 `docs/AGENTS.md` **一端**的版本——skill 那端沒有任何版本標記，agent 無從知道手上這支依據的是哪一版，**該檢查實際上執行不了**。下游實跑時唯一的辦法是 grep 特徵字串反推版本，而特徵字串每版不同、寫不進規範，沒有上下文的 agent 也推不出來。現於六支引用規範的 skill（`new-issue`、`execute-task`、`dev-cycle`、`create-pr`、`review`、`decompose`）在 frontmatter 後宣告依據版本，規範明訂比對方式為「讀 skill 宣告值 vs 讀本檔檔尾版本」並禁止以特徵字串反推；`sync-skills.py --check` 新增驗證：引用規範的 skill 必須有宣告，且宣告值需等於當前 `docs/AGENTS.md` 版本。

  宣告刻意寫在**內文而非 frontmatter**：2.4.0 已踩過 OpenCode 與 Antigravity 對 frontmatter 的嚴格性（缺 `name:` 整份靜默不載入），未知欄位若被 schema 擋下會是同一種災難，而內文宣告零平台風險且同樣可被 `--check` 驗證。

### 新增（`rules/AGENTS.md`、`rules/AGENTS.zh-TW.md`、`rules/README.md`、`CLAUDE.md` — **下游需重新複製規則檔**）

盤點發現 2.6.0–2.8.0 的五個新概念在雙語規則檔中**完全零覆蓋**，其中三處會與技能互相矛盾——agent 讀規則檔與讀技能會得到兩套指令：

- **Small 單迴圈合併**（原本無條件要求外迴圈與內迴圈各一份紅燈證據）
- **證據持久力與假綠燈的分界**，含「實作者主動揭露測試限制永遠不構成缺失」（原本只有假綠燈定義，寒蟬效應照樣存在）
- **規格修訂查核的作用域**與 hash 改寫後的回填（原本 `git diff {核准 commit}..HEAD` 沒有作用域說明）
- **觀測式驗收與反向自檢**「若這件事失敗了，這個判準會不會仍然是綠的？」——規則檔的適用範圍比技能更廣（未跑 issue 閉環時也生效），缺它比技能缺它影響更大
- **合法的中間狀態與終態**（原本「Loop until verified」可被讀成永不停止）

另補 `rules/` 自身的客製邊界：「語言規範」與「Monorepo 規則」兩節標為專案客製，`rules/README.md` 新增「客製邊界」段說明核心章節與 skill gate 一一對應、單邊改寫會產生互斥指令且不報錯。`CLAUDE.md` 的單一真相來源清單補齊 2.7.0–2.8.0 的四項（證據持久力、觀測式驗收、合法中間狀態與終態、客製邊界與同步策略），`--check` 範圍說明更新為五件事。

## [2.8.0] - 2026-08-18

### 新增（`docs/AGENTS.md` — **下游需重新複製**；`skills/`、`workflows/shared/` — **需重新複製 `new-issue`、`execute-task`、`dev-cycle`、`review`**）

本版來自兩個下游專案的實跑回饋（line-oa-plus 與 googleBooking），其中一項是 2.7.0 的規則缺陷修正。

- **新增「客製邊界與同步策略」**：本檔會被複製到各專案並隨其演化，但過去從未寫明哪些部分可改、哪些改了會壞掉，導致每次同步都要重新人工判斷——兩個下游專案對同一個問題給出了相反的同步建議（逐列合併 vs 覆蓋後補回），正是因為缺這個依據。現分三層：**核心**（狀態字串、metadata 欄位名、章節名、規則語意——被 `dev-cycle` 狀態偵測與各 gate 直接讀取，改名等同拿掉那道 gate 且不報錯，同步時以上游覆蓋）、**應客製**（目錄樹、常青文件對照表、範例編號、專案級前置閘門、本地案例——同步時保留專案自己的，本檔中以節首 `> [!NOTE]` 標明）、**可調整**（判定門檻描述、標記符號集合）。合併策略因此可推導，不必每次判斷。

  併入**核心層齊備性檢查**：各 skill 引用本檔章節前須確認章節存在且語意相符，缺漏、同名異義或版本落後時**明講並停下來問，禁止靜默套用上游預設**。實例來自 googleBooking——技能升到 2.6.0 而其 `docs/AGENTS.md` 停在祖先版，`decompose` 引用的「文件動態分級規範」在該專案**存在但語意不同**（只規定產出哪些檔案、沒有風險分級），指到同名的另一套東西比指到不存在更難察覺。`new-issue` 的「讀取權威規範」已接上此檢查。

- **新增「觀測式驗收」與反向自檢**：部分 AC 的最終判準不是測試而是生產環境觀測，這類證據**沒有紅燈基線**——測試至少會先紅一次證明它抓得到問題，觀測判準不會，因此判準本身失效時看起來與行為正確完全一樣。現要求每項觀測式 AC 回答 **「若這件事失敗了，這個判準會不會仍然是綠的？」**，答不出「不會」即不算通過；並要求**先以對照組驗證判準本身**、寫出失敗時的可觀察差異。實例來自 googleBooking #3477：三項判準（戳記數 731、錯誤數 0、可用量 1.65M）形式全過，實際 388 家靜默漏派——未派工的店保留舊戳記，判準在失敗情境下仍然顯示綠；另一實例 #3457 的「假零陷阱」是查詢寫錯回傳零筆被讀成「已清乾淨」。兩者都是**綠燈來自判準失效而非行為正確**，屬假綠燈，但 2.7.0 的判準涵蓋不到。`review` 與 `execute-task` 各接一處。

- **新增「合法的中間狀態與終態」**：閉環不是每個 issue 都以合併收尾，也不是沒有新 commit 就代表卡住。新增 `等待外部驗收窗`（判準依賴每週排程夜、月結、對帳日等外部時間窗，須記預定窗口與待觀察判準）與 `不修復`（經評估的合法終態，須記判定理由與追蹤方式）兩種 `**狀態**`，`dev-cycle` 狀態偵測補兩列，不再將其判為停滯或自行推進；`review` 覆核其記錄完備性。來源為 googleBooking 的 #3477（驗收窗以週為單位）與 #3473（結論為不修復）。

### 修正（同上範圍）

- **回填驗證對象更正為合併目標分支**：2.7.0 寫的是 `git merge-base --is-ancestor {SHA} HEAD`，但回填發生在合併**之後**——agent 若在尚未刪除的 issue 分支上執行，`HEAD` 仍是那條即將消失的分支，**驗證會通過但 SHA 日後照樣失效**，等於沒驗證。現更正為以合併目標分支（`origin/dev`、`origin/main` 等）為驗證對象，三處（`docs/AGENTS.md`、`dev-cycle`、`review`）一併修正。由 line-oa-plus 踩過後回報。

- **改寫 commit hash 的觸發條件由 squash 泛化**：2.7.0 只寫 squash，但 rebase、amend、cherry-pick 重放同樣會讓核准 commit 失效，走 merge commit 但合併前 rebase 的專案讀了會誤以為不適用。googleBooking #3477 實跑印證：rebase 到 dev 後 9 個 commit 全數 replay，核准 commit 由 `ca8bd47da` 變為 `c4a8aeac7`。

- **移除混入本檔的下游專案特徵**：目錄樹的 `angular.md`／`member.md`／`site-ssr.md`／`auth.md` 改為佔位符，`issue-3240`／`3238`／`3221` 改為泛用編號——後三者經確認是 googleBooking 的真實 issue 編號，混在通用規範裡四個月並隨每次複製擴散到新專案。它們本就屬「應客製」層，不該以具體值出現。

## [2.7.0] - 2026-08-18

### 新增與修正（`docs/AGENTS.md`、`skills/`、`workflows/shared/` — **下游需重新複製 `new-issue`、`execute-task`、`dev-cycle`、`create-pr`、`review` 及對應工作流程**）

本版三條全部來自下游專案的實跑回饋（line-oa-plus 的 issue #192 / #193 閉環，以及該專案主 worktree 對 squash 合併流程的觀察），補的都是「規則存在但守不住」的缺口：

- **分批核准時明令禁用單行核准表**：2.6.0 允許未分批時將逐項核准表省略為單行，條件寫了、展開時機也寫了，但缺一句明確禁令。這個誤用不會報錯——`review` 與 `create-pr` 查核的是 `待核准` / `待重新核准` 字串是否殘留，一旦在分批情境收斂成單行，掃不到殘留即視為全部已核准，未核准的 Scenario 會被當成可實作。**規則靜默失效而不報錯**，與 2.4.0 的 `name:` 屬同一失敗類型。現於 `docs/AGENTS.md` 加明確禁令，`new-issue` 完成 gate 新增對應查核，`review` 新增「分批情境使用單行形式列 MUST FIX」，`create-pr` 要求先展開再查核。

- **界定規格修訂查核的作用域，並規範 squash / rebase 後的核准 commit 回填**：「規格修訂的查核」靠 `git diff {核准 commit}..HEAD` 運作，但以 squash / rebase 合併的專案，分支上的核准 commit 在合併後 SHA **必然**失效（非偶發），合併後回查會斷。釐清後的結論是**查核的作用域本來就在實作期間**（合併前恆成立），所以修法不是換掉 `git diff` 機制，而是補上合併後的回填規則：以後續 commit 回填為合併後仍可達的 SHA，並以 `git merge-base --is-ancestor` 驗證；不得以 `amend` 改寫已推送歷史讓舊 SHA「看起來仍可達」。`dev-cycle` 的「完成」階段與 `review` 的 Pre-analysis 各補一處掛勾。

- **新增「證據持久力」，與假綠燈分開判定**：原「假綠燈」節把兩件事混在同一標籤下——「刻意製造不代表行為正確的綠燈」與「證據為真但守門脆弱」。判準應該是**這次的綠燈是否代表行為正確**，而不是**這個綠燈日後是否還擋得住回歸**。混用的副作用很實際：誠實揭露測試限制會被歸進帶指控意味的標籤，理性選擇就變成不揭露——一條讓誠實比沉默更危險的規則，正在傷害它要保護的東西。現分出「證據持久力」（探針綁在易變字串、斷言只驗代理指標等），明訂 `review` 列 SHOULD FIX 並提替代斷言、**不得判 MUST FIX、不得歸入假綠燈、不得據此退回實作**，且**實作者主動揭露限制永遠不構成缺失**；`execute-task` 對應改為鼓勵在證據中主動揭露。

## [2.6.0] - 2026-08-18

### 變更（`docs/AGENTS.md` — 下游建議重新複製）

- **精簡 issue 文件的儀式性作業**：全面盤點後發現，分級制度省的是**檔案數**，但每份檔案裡的固定章節與欄位沒有跟著分級，且多處資訊在 git 已有記錄或在多份文件間重複維護。本次以「誰在讀」為判準逐項精簡——被閉環自動化消費的欄位一項未動，砍的是機器與人都不讀的簿記：
  - **Low 風險可一行收斂**：原規範強制 Low 也填滿「最大風險／風險等級與理由／首要驗證／選擇理由／完成證據」五欄，結果是五行「無明顯未知」的變體。現允許 Low 且無特殊前置驗證時收斂為一行；升級為 Medium / High 時再展開五項。
  - **未分批核准表可省略為單行**：逐 Scenario 核准表的存在理由是分批核准（2.2.0）；一次全部核准時整張表每列日期相同、狀態相同。現允許省略為「全部 Scenario 於 YYYY-MM-DD 核准」，並明定此單行視同全表 `已核准`；發生分批或規格修訂時再展開。
  - **快速導覽與關鍵差異改為有對照才寫**：這兩節在重構、遷移類 issue 是全文件對人價值最高的章節，但被寫成 Medium / Large 一律必備，沒有新舊對照的 feature 只能硬填。改為條件性章節。
  - **Timeline 只記語意事件**（建立、核准、規格修訂、merge）：逐 Task 的「完成步驟 N」條目沒有任何流程讀取，進度由任務清單狀態符號表示；人讀的是敘事骨架，不是 git log 的複寫本。
  - **issue 文件移除檔尾 Changelog／維護紀錄**：issue 文件生命週期短、merge 後凍結，git 與段落內帶日期的 `> [!NOTE]` 已完整留痕——人是在讀到該段的當下需要知道它過時，不是讀完再查附表。
  - **issue README 範本移除 `文件版本` 與 `最後更新` metadata**：前者無任何讀者；後者的新鮮度標示對**常青文件**是核心資訊（保留並於日期規範明示適用範圍），對 merge 後凍結、以 `**狀態**` 宣告生命週期的 issue 文件則是會漂移的重複記帳。
  - **Small 層級重合時允許單迴圈合併**：單一檔案修正的可觀察行為常只存在於一個層級，強制外／內迴圈各留紅燈是同一個測試拆兩份寫。層級重合時四段證據縮為三段（合併紅燈、最小實作後全綠、重構後全綠），並必須記錄層級選擇理由；層級確實分開的 Small 仍走雙迴圈，Medium / Large 不適用。
  - **Small 任務清單不再預寫迴圈命令**：AC 本身已強制「可重複執行的檢查方式」，執行時又會記錄實際命令與輸出，計畫端逐項預寫外／內迴圈命令等於同一條命令寫三次、且執行後無人再讀。任務清單每步驟改為只標注 AC 編號與驗證方式。
  - **移除跨檔複寫**：`implementation-plan.md` 的風險五欄改為引用 README、`requirement-analysis.md` 不再複寫涉及檔案清單——副本會漂移，漂移對人的誤導比指向一份權威來源更糟。
  - **移除文件類型 emoji 標記**（⭐📋🔧🔍📊🧪💡🔄）：八種標記服務最多四個檔案，無任何流程讀取，且 🔄 與狀態標記語意衝突。狀態標記（✅⏳等）被任務清單狀態偵測消費，保留。
  - `docs/AGENTS.md` 自身的文件版本與修訂紀錄**保留**：它會被複製到下游、脫離 git 歷史，內嵌版本資訊是唯一的出處證明。

### 變更（`skills/`、`workflows/shared/` — **下游需重新複製 `new-issue`、`execute-task`、`dev-cycle`、`create-pr`、`review` 及對應工作流程**）

- **把上述規則接進掛勾端**（規則不掛進 skill 不會生效，同 2.5.0 的教訓）：`execute-task` 步驟 11 改為僅語意事件才補記 Timeline、移除 issue 文件 Changelog 回寫；`new-issue`、`dev-cycle`、`create-pr` 的核准表查核明示接受單行省略形式，`new-issue` 完成 gate 移除 issue 文件 Changelog 要求。另：`execute-task` 接入單迴圈合併與「執行時決定測試層級」、`new-issue` 的 Small 任務清單改標注驗證方式、`review` 新增單迴圈合併理由的覆核（不當合併列 MUST FIX）、`create-pr` 的自動化證據與 Proof 範本支援合併形式。
- **`review` 新增 Small 級短版報告**：文件分級花了整節規範省文件，review 卻對一行修正仍產出十二節完整報告。短版收斂為審查版本、整體評估、問題與風險、已查核維度、流程判定五節；**查核義務不變**（獨立 reviewer、規格修訂查核、至少 3 個破壞性邊界條件、假綠燈檢查、artifact 持久化照常執行），且無發現的維度必須明列於「已查核維度」——缺席的章節讀者無從分辨是沒查還是沒事，負面證據以一行保留。

### 新增（`scripts/` — 下游不需重新複製）

- **`sync-skills.py --check` 補驗 `name:` frontmatter**：2.4.0 修過「缺 `name:` 導致 OpenCode 與 Antigravity 靜默不載入」的 bug，但檢查腳本只驗 `description`，同一問題再發生時 CI 仍會綠燈。現驗證每個 `SKILL.md` 的 frontmatter 必須具備 `name:` 且值等於 skill 資料夾名。

## [2.5.0] - 2026-08-17

### 新增（`docs/AGENTS.md` — 下游建議重新複製）

- **`## 常青文件更新責任 (Evergreen Docs)`**：`docs/AGENTS.md` 原本只規範 `docs/issues/` 這一層——issue 文件何時建立、寫什麼、怎麼核准。但同一個 `docs/` 底下的 `architecture/`、`domain/`、`operations/` 是**常青文件**，描述的是系統當下的樣子，過去沒有任何規則說明誰該在什麼時候更新它們。

  結果是可預期的：常青文件停在最後一次有人想到要改它的那天，且不會宣告自己過期，仍以權威語氣描述一個不再存在的系統。本節以「什麼變更觸發哪份文件」的對照表把更新責任綁進 issue 收尾，涵蓋部署拓撲、路由與認證鏈、模組分層、領域規則、維運程序，以及使用者可見的功能異動。

  對照表明列為起點而非完整清單：專案新增自己的常青文件時，必須同時登記觸發條件，否則等於預約下一份沒人更新的文件。內容邊界（什麼該寫、防腐標頭格式）仍留給各專案的 `architecture/README.md`，本節只規定何時必須更新。

  來源為下游專案（issue 收尾時同步架構／領域／維運文件）的實務慣例，去專案化後回饋至本 kit。

### 新增（`skills/execute-task`、`skills/dev-cycle`、`workflows/shared/` — **下游需重新複製這兩個技能與對應工作流程**）

- **把常青文件檢查接進閉環**：規則只寫進 `docs/AGENTS.md` 不會自動生效——本 kit 其他規則章節（「規格修訂的查核」「假綠燈」「Gate 豁免紀錄」）都是由 skill 明確引用才會被讀到，新章節少了同樣的掛勾。現補上兩處：`execute-task` 步驟 11「回寫權威狀態」加入常青文件的觸發檢查（有觸發就一併更新，並把日期標頭改為系統當下日期）；`dev-cycle` 的 `create-pr` 階段加入開 PR 前的確認，未更新時退回 `execute-task` 補上。

  掛在 `create-pr` 而非合併後的「完成」階段，是為了讓常青文件的更新落在同一個 PR 裡接受 review，而不是變成事後補的孤立 commit。`review` 這次未加對應檢查項。

## [2.4.1] - 2026-08-07

### 補充（`docs/setup/tools.md` — 下游不需重新複製）

- **補上 Superpowers 的更新指令與 symlink 限制**：原文只寫「後續於 `~/Tools/superpowers/` 執行 `git pull` 即可更新」，漏掉一個實際會踩到的點——安裝指令的 `skills/*` 是展開當下的清單，上游**新增**技能時不會自動產生對應連結。現補上 `ln -sfn` 補連結指令，並說明其冪等性（`-f` 覆蓋既有連結、`-n` 避免連進目錄內部，重複執行不產生巢狀，也不影響同目錄下非 Superpowers 的技能）。另註明 Claude Code 與 OpenCode 走各自的 plugin 機制自動更新，不需要這份 clone，避免誤以為三個平台都得手動維護。

## [2.4.0] - 2026-08-07

### 修正（`skills/`、`workflows/shared/`、`CLAUDE.md`、`skills/README.md` — **下游需重新複製全部技能與工作流程**）

- **所有 `SKILL.md` 與 `workflows/shared/*.md` 補上 `name:` frontmatter 欄位**：原規範寫明「不要加 `name:` 欄位 — 名稱由檔名／資料夾名決定」，該敘述僅對 Claude Code 成立。OpenCode 1.18.14 與 Antigravity CLI（`agy` 1.1.7）**要求 frontmatter 具備 `name:`，缺少時整份 skill 會靜默不載入**——不報錯、不出現在 skill 清單、也無任何警告，因此本 kit 的 9 個技能過去在這兩個平台上其實從未生效（只有 slash command 那條路徑有作用）。

  實測依據：同一個 `~/.claude/skills/` 目錄下（OpenCode 會一併掃描），具備 `name:` 的第三方技能全數載入，本 kit 缺 `name:` 的 9 個全數未載入；Antigravity 端為同一份 `dev-cycle` 補上 `name:` 前後對照，補上後才出現在技能清單。

  workflow 端一併帶上 `name:` 無副作用：OpenCode 解析 slash command 時先以檔名推導 `name`，再以 frontmatter 覆寫，兩者同名故結果一致，且 schema 本就包含該欄位。

- **`CLAUDE.md` 的 Frontmatter 規範改為 `name:` 必填**，並記錄三平台的行為差異，避免日後再依「檔名即名稱」的假設移除該欄位。

## [2.3.1] - 2026-08-07

### 修正（`rules/README.md`、`skills/README.md`、`workflows/README.md`、`docs/setup/tools.md` — 下游不需重新複製）

2.3.0 收攏安裝路徑時沿用了既有敘述，其中 Antigravity 的路徑早已失效，OpenCode 的目錄慣例也與官方文件不符。本次以各平台實際安裝版本實測後更正：

- **Antigravity 全域路徑已遷移**：`~/.gemini/config/.migrated`（2026-05-20）之後，設定統一在 `~/.gemini/config/`，由 Antigravity、Antigravity IDE 與 Antigravity CLI（`agy`）三者共用。四處舊路徑一併更正——workflows 改為 `~/.gemini/config/global_workflows/`、skills 改為 `~/.gemini/config/skills/`、MCP 設定改為 `~/.gemini/config/mcp_config.json`，以及 `docs/setup/tools.md` 中把 Superpowers symlink 到舊 skills 目錄的指令（照舊指令安裝的技能不會被載入）
- **Antigravity 規則檔位置**：全域規則改記 `~/.gemini/config/AGENTS.md`，與 `~/.gemini/GEMINI.md` **同時載入**而非擇一（`agy` 1.1.7 以 marker 實測）。官方文件只記載 `GEMINI.md`，但放在 `config/AGENTS.md` 可與個人規則分離，重新複製規則檔時不會蓋掉個人設定。官方文件所述的專案層 `.agents/rules/*.md` 於 CLI 非互動模式實測未生效，已標注但保留記載
- **OpenCode 目錄單複數皆生效**：1.18.14 掃描的 glob 為 `{command,commands}/**/*.md` 與 `{skill,skills}/**/SKILL.md`，官方文件只列複數。兩種目錄同時存在會重複載入，README 補上擇一使用的提醒
- **OpenCode 不需 skills 與 commands 兩邊都裝**：兩者內容逐位元組相同且會同時載入，等於同一份內容有兩個入口，而 skill 的 `description` 常駐 context。已於 `skills/README.md` 說明取捨，並指出 `dev-cycle` 是值得單獨安裝的例外

## [2.3.0] - 2026-08-04

### 變更（`docs/setup/`、`rules/README.md`、`workflows/README.md`、`skills/README.md`、`README.md`、`docs/usage.md` — 下游不需重新複製）

- **五份平台安裝指南合併為一份工具設定指南**：原 `docs/setup/{claude,opencode,windsurf,antigravity,cursor}.md`（共 755 行）中，真正屬於本 kit 安裝教學的只有「路徑速查」與「安裝 dev-rules-kit」兩節，其餘 100+ 行都是 Serena / GitNexus / Superpowers 的環境設定，且五份之間高度重複（三個 IDE 平台的 MCP JSON 完全相同）。現改為：
  - 本 kit 的安裝路徑收攏到對應資料夾的 README——[`rules/README.md`](rules/README.md#安裝方式)、[`workflows/README.md`](workflows/README.md#安裝方式)、[`skills/README.md`](skills/README.md#安裝方式)，各自以表格列出五平台路徑與複製指令
  - 外部工具設定合併為單一 [`docs/setup/tools.md`](docs/setup/tools.md)，以工具為主軸、平台為分支，並新增 MCP 設定檔位置對照表
- **修正 `dev-cycle` 的過時敘述**：原 `opencode.md` 與 `antigravity.md` 稱 `dev-cycle`「不會出現在 `/` 指令清單（它沒有 workflow 對應檔）」，但 `workflows/shared/dev-cycle.md` 自 2.0 起即存在。合併後統一為「除 `/dev-cycle` 指令外，也可用自然語言觸發」
- **補上 `rules/` 的安裝說明**：原五份 setup 只有 Windsurf / Antigravity / Cursor 三平台寫了規則檔怎麼套用，`rules/README.md` 本身完全沒提。現補齊五平台對照表（OpenCode 一列為新增內容）

## [2.2.1] - 2026-08-03

### 修正（`README.md`、`docs/usage.md` — 下游不需重新複製）

2.2.0 更新了 `rules/`、`docs/AGENTS.md` 與全部 skill，但漏掉三處不在 `sync-skills.py` 範圍、需手動維護的使用者文件，導致它們仍在描述舊規則：

- `README.md`：「驗收標準的形式會依規模與風險自動調整（Small + Low 只需輕量驗收條件）」——形式已改為只由規模決定
- `docs/usage.md`：同一處過時敘述出現兩次（Step 1 說明與 `new-issue` 參考表），一併補上分批核准的說明
- `docs/usage.md`：將 `requirement-analysis.md` 的內容描述中的「待確認事項」改為「問題點與涉及檔案」。`docs/AGENTS.md` 對該檔的規範從未包含待確認事項，而 2.2.0 起 `## 待確認事項` 明確屬於 README，留著會誤導寫入位置

另將 `docs/AGENTS.md`「實作步驟的排序原則」中的未知來源指向 README 的 `## 待確認事項`，使其與 2.2.0 新增的區段一致。

`workflows/` 下的手動檔案（`README.md` 的清單、`antigravity/fix-webview-conflict.md`）經檢查無過時內容。`docs/superpowers/` 下的歷史規劃與設計文件依 Timeline 保留原則不修改。

## [2.2.0] - 2026-08-03

### 新增（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

- **Gherkin 分批核准**：核准表新增第三種狀態 `待核准`（原本只有 `已核准` 與 `待重新核准`）。Scenario 多時不必一次核准全部，未取得同意者標為 `待核准`，issue 文件即可建立並就已核准部分進入實作。放行門檻是已核准部分必須涵蓋核心目標的主要成功路徑與已辨識的重要失敗路徑；`create-pr` 前必須全部轉為 `已核准`。`decompose` 遇 `待核准` 不阻塞，只拆已核准部分，其餘列入新的「待核准 Scenario」段落且禁止產生 Task
- **`## 待確認事項`**：`new-issue` 原本允許把非阻塞未知「記錄為待確認事項」，但沒有規定寫在哪、也沒有任何節點負責關掉，寫下去就沉了。現在收斂到 README 固定區段（`TBD-N` 編號，狀態 `待確認` / `已解決` / `不影響本次交付`）。刻意設計為**揭露而非阻擋**：不阻止 `create-pr`，但必須在 PR 原文揭露；`review` 覆核 `已解決` 與 `不影響本次交付` 的理由是否成立

### 變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

- **驗收標準形式改由規模單獨決定**：原規則為「Small + Low 用輕量驗收條件，其餘一律完整 Gherkin」，導致 Small + High 的單檔案修正也要寫 Feature / Scenario / 逐項核准表，文件量遠大於 diff。現改為 **Small 一律輕量驗收條件、Medium / Large 一律完整 Gherkin**，風險不再改變形式。這同時修掉了規範的內部矛盾——原規則本身就違反 `docs/AGENTS.md` 明列的「規模與風險不得互相推導」
- **風險改為決定驗收標準的強度**：Small + Medium / High 維持輕量形式，但每項條件必須寫出失敗路徑、至少一項覆蓋最大風險，並記錄核准 commit 以套用輕量版「規格修訂的查核」（行尾標註 `（待重新核准）`，不需逐項核准表）。這補回放寬後原本會缺失的規格漂移防護
- **相容性**：既有 issue 已將 Small 任務寫成完整 Gherkin 者維持有效，依其實際形式查核，不需改寫，`dev-cycle` 也不會因此退回。本次規則只約束新建立的 issue 與規模變更後的重新規劃

### 修正（`rules/` — 下游建議重新複製）

`rules/AGENTS.md` 與 `AGENTS.zh-TW.md` 是唯一會被寫進 `.windsurfrules` 的檔案，在該環境下 agent 讀不到 `docs/AGENTS.md`，因此兩處措辭漂移實際造成規則弱化：

- **characterization test 漏掉綠燈要求**：原文為「先補上 characterization test 再重構」，缺少 `docs/` 版本的「**並取得綠燈**」，等於允許在紅燈狀態下開始重構
- **外迴圈替代方案漏掉記錄要求**：原文沒有「記錄採用的替代方式」，缺少該要求則無 BDD runner 時的替代選擇無從追溯

另統一三處措辭分歧：等價證據適用範圍（`純文件` / `純文件、格式` / `純文件、排版` → 統一為「純文件、排版或無可執行行為」）、豁免邊界（`docs/` 補上「也不得把假綠燈宣稱為測試通過」）、`略過` → `省略`。

### 重構（`skills/`、`workflows/shared/`）

行為不變，移除對 `docs/AGENTS.md` 的整段複製：

- **`decompose`**（254 → 233 行）：刪除「風險優先決策流程」的完整重述（5 步驟清單、風險來源對照表、垂直切片防誤用段與必答三問），改為要求讀取權威節。保留該 skill 獨有的正反對照範例，並將原本埋在重複清單裡的真實差異獨立寫出——拆解階段是**確認**風險理由是否仍成立，不是重新判定
- **`execute-task`**（198 → 195 行）：等價證據段的兩條完整定義改為一句話摘要加引用，與同檔「假綠燈檢查」的引用模式一致

### 效果

跨檔案完全相同的重複片語由 13 組降至 6 組，且剩餘 6 組全部落在 `docs/AGENTS.md` ↔ `rules/` 這一對——即設計上必須各留一份、且現已逐字一致的那組。`decompose` 與 `execute-task` 對權威規範的複製已完全消除。

## [2.1.1] - 2026-07-27

### 變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

行為與 gate 完全不變，只收攏重複敘述。導入兩個具名用語，把散落各檔的列舉收成單一定義，消除措辭漂移。

- **「紅綠重構證據」**：外迴圈紅燈、單元測試紅燈、最小實作後全綠、重構後全綠四段的合稱。原本這串列舉在 `dev-cycle`、`execute-task`、`review` 逐字複述，`docs/AGENTS.md`、`decompose`、`create-pr`、`rules` 還各有變體且措辭不一致（「實作後全綠」／「最小實作後全綠」）。現在定義於 `docs/AGENTS.md` 與 `rules/`，其餘檔案直接使用該詞
- **「假綠燈」**：以任何方式製造出不代表行為正確的綠燈（刪改測試、mock 掉受測行為、硬編碼答案、空 assertion）。取代原本分散在 `execute-task`、`review`、`rules` 的九項列舉；`execute-task` 的「誠實回報與防作弊檢查」步驟改名為「假綠燈檢查」
- **`git diff` 查核回歸單一真相來源**：2.1.0 把完整指令與三條分支邏輯複製到六個檔案，措辭各有出入。現在只留在 `docs/AGENTS.md`「規格修訂的查核」與 `rules/`（規則檔需自足），五個 skill 改為引用該節
- **Superpowers 樣板去重**：各 skill 不再重複解釋「選用增強、缺少套件不構成阻塞、gate 不降低」——該政策已在 `rules/` 定義，skill 端只保留「可用時優先調用 `{skill}`」

### 效果

六個 skill 合計減少 763 字元（約 2.8%）；`docs/AGENTS.md` 與 `rules/` 因納入定義而增加，全部檔案淨變化約 +168 字元。**主要收益是一致性而非 token**：同一概念先前在六個檔案有六種寫法，正是 `sync-skills.py --check` 抓不到的那類漂移。

## [2.1.0] - 2026-07-27

### 變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

2.0.0 的 gate 對「agent 自行降低標準」與「使用者自主決策」一視同仁，導致小任務與純重構付出不成比例的流程成本。本版把 gate 的對象收斂回 agent，並讓證據強度重新服從既有的規模與風險雙軸。**所有既有 issue 的格式仍然有效**，本版只放寬要求、不新增必填欄位。

- **Gate 豁免機制**（`rules/`、`docs/AGENTS.md`、全部閉環 skill）：使用者明確要求跳過某項 gate 時，agent 必須照做，並在 issue README 的 `## Gate 豁免紀錄` 寫下日期、豁免項目、使用者原話與殘餘風險；`dev-cycle` 依該紀錄放行，`review` 與 `create-pr` 如實揭露而非視為缺失。不得自行推定豁免——沉默、時間壓力或任務看起來很小都不算
- **唯一不可豁免的是誠實回報**：豁免可以跳過流程，但不得把未執行的驗證寫成已通過、未審查的變更寫成已審查。使用者要求刪改測試時照做，但必須記錄真實理由
- **驗收標準依規模與風險分級**（`docs/AGENTS.md`、`new-issue`）：**Small + Low** 改用輕量驗收條件（`AC-1` 起，一句話可觀察結果加可重複執行的檢查方式），不需 Gherkin 語法、Scenario ID 與逐項核准表；其餘組合維持完整 Gherkin。仍須取得使用者明確核准，風險升級時補齊 Gherkin
- **純重構免紅燈**（`rules/`、`docs/AGENTS.md`、`execute-task`、`decompose`、`review`）：紅燈要求只適用於會改變可觀察行為的任務。純重構改以「變更前後執行同一組既有測試皆綠」為等價證據，既有測試不足時先補 characterization test。標為不改變行為即承諾 diff 無行為變更，`review` 會據此查核
- **移除 Gherkin SHA-256，改以 git 見證規格修訂**（`docs/AGENTS.md`、`execute-task`、`decompose`、`review`、`create-pr`、`dev-cycle`）：內容雜湊只對「無法重算 hash 的對手」有效，而 agent 依設計就是唯一的計算者——它同時負責改規格、重算 hash 與判定變更性質，形成自我認證的循環；且自然語言規格本來就該在實作中演進，用防竄改機制約束它是類別錯誤。改為：
  - 核准紀錄記錄 `**核准 commit**` 與**逐 Scenario** 的核准日期與狀態（`已核准` / `待重新核准`），取代單一 hash
  - 查核改用 `git diff {核准 commit}..HEAD -- docs/issues/issue-{ID}/README.md`。見證者是 git 而非 agent，輸出是可讀的 diff 而非布林值，判定交給 reviewer 覆核同一份 diff
  - 差異未觸及 Gherkin 即直接繼續；改變條件、動作或預期結果時**只有受影響的 Scenario** 退回重新核准，其餘不受牽連；純措辭調整於 Timeline 補記即可
  - 明文寫入「規格在實作中被修訂是外迴圈的預期結果，不是違規」，與 kit 既有的 Timeline 保留原則一致
- **Review artifact 不綁特定平台**（`docs/AGENTS.md`、`review`、`dev-cycle`）：優先使用專案的 code review 平台（GitHub、GitLab、Gitea 等）；平台不可用、無權限或純本機流程時，改寫入 `docs/issues/issue-{ID}/review-{HEAD 前 7 碼}.md` 並隨變更提交。兩者都必須含 Reviewed HEAD SHA 與獨立 reviewer，兩種方式都無法完成時才輸出 `UNPERSISTED`
- **BDD runner 不再是硬性工具依賴**（`rules/`、`docs/AGENTS.md`、`execute-task`、`decompose`）：專案沒有 BDD runner 時，以標註 Scenario ID 的整合或端對端測試充當外迴圈。缺少特定工具不構成省略外迴圈的理由

### 相容性與遷移

除核准紀錄外，驗收標準、Proof of Test 與 review artifact 的既有格式全部保持有效，本版只增加可選路徑。既有 Small issue 若已寫完整 Gherkin，不需改寫成輕量格式。

**唯一需要轉換的是 2.0.0 建立的 `## Gherkin 核准紀錄`**：`**狀態**`、`**核准日期**`、`**Scenario IDs**`、`**Gherkin SHA-256**` 四個欄位改為 `**核准 commit**` 加逐 Scenario 核准表。轉換為機械式改寫，核准來源與已取得的核准本身不受影響；`**核准 commit**` 填寫承載該次核准內容的 issue 文件提交（未提交時填 `待提交`，首次提交後回填）。

`docs/AGENTS.md` 更新至 v1.7。

## [2.0.0] - 2026-07-26

### 破壞性變更（`rules/`、`docs/`、`skills/`、`workflows/shared/` — 下游更新前需檢查）

開發閉環改為 Gherkin BDD 外迴圈與 TDD 內迴圈，並以可持久化證據阻止 Agent 跳過需求核准、失敗測試、獨立審查或 PR 驗收。既有 issue 若缺少下列資料，`dev-cycle` 會退回對應階段補齊，不再依舊格式直接推進：

- README 中具唯一 Scenario ID 的 Gherkin 驗收劇本
- 核准狀態、日期、來源、完整 Scenario ID 集合與 Gherkin SHA-256
- BDD 紅燈、單元測試紅燈、最小實作後全綠及重構後全綠證據
- 對目前 PR HEAD 的獨立 review artifact
- 與核准 Scenario 集合完全一致的 PR Proof of Test

`execute-task`、`review`、`create-pr` 的輸入與完成契約因此比 1.x 嚴格。下游若有依賴舊版任務格式、只記錄「測試通過」、使用待測 checkbox 作為 PR 驗證，或未保存 review 結果，更新前需先調整。

### BDD + TDD 硬性閉環

- **需求規格化**（`new-issue`、`docs/AGENTS.md`）：一次只問一個問題，取得使用者明確核准後，將驗收標準寫成具 Scenario ID 的 Gherkin；以 SHA-256 綁定核准內容，Given / When / Then 異動後必須重新核准
- **雙迴圈拆解**（`decompose`）：每個 Scenario 映射至 BDD feature / Step Definitions、底層單元測試、預期紅燈原因、最小 production code 與重構後回歸命令
- **紅綠重構狀態機**（`execute-task`）：沒有相關 BDD 紅燈與單元測試紅燈前禁止修改 production code；最小實作與重構後都必須取得全綠證據
- **測試防作弊**（`execute-task`、`review`）：禁止為取得綠燈而刪除、略過、弱化或註解測試，也禁止過度 mock、硬編碼答案或空 assertion
- **雙重審查**（`review`）：要求獨立 reviewer、架構符合度、至少三個破壞性邊界案例，以及包含 Reviewed HEAD SHA 的持久化 PR review / comment
- **測試通過證明**（`create-pr`）：PR Proof of Test 必須完整覆蓋核准 Scenario 集合，並附 Gherkin 原文、hash、實際成功命令及結果
- **跨階段防繞過**（`dev-cycle`）：以 Gherkin 核准、紅綠燈證據、目前 HEAD review 與完整 Proof of Test 判斷下一階段

### Superpowers 相容策略

Superpowers 改為選用的流程增強套件，不是執行期必要依賴：

- 已安裝時優先使用 `brainstorming`、`writing-plans`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`
- 未安裝時由本 kit 的 skills 執行內建等價流程，所有核准、測試、獨立審查與完成 gate 維持強制
- README 新增核心 skill 對應、建議輔助 skills 與五個平台的完整套件安裝入口
- PRD 中不存在的 skill 名稱改為可執行能力映射，不形成無法安裝的外部依賴

### 下游更新

- 建議重新複製 `rules/AGENTS.md` 或 `rules/AGENTS.zh-TW.md`
- 重新複製 `skills/` 或其對應的 `workflows/shared/`
- 以新版 `docs/AGENTS.md` 更新 issue 文件規範
- 既有進行中 issue 應先補齊 Gherkin 核准紀錄與雙迴圈證據，再啟用新版 `dev-cycle`
- Superpowers 可選擇不安裝；若安裝，建議使用完整套件而非散裝複製單一 skill

## [1.5.0] - 2026-07-23

### 變更（`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

強化 skill 的輸入證據、完成判準與跨文件狀態回寫，降低 Agent 提前完成、破壞契約或產生無證據內容的風險。

- **契約安全**（`code-simplify`）：公開 API、跨模組、DI、反射／序列化、override 與 callback 簽章優先於簡化規則；無法證明安全時保留原狀
- **文件單一真相來源**（`docs/AGENTS.md`、`new-issue`）：Small／Medium／Large 的初始文件集合、README 連結、Timeline 與 Agent 工作時序保持一致；`new-issue` 改為引用權威規範並使用完整性 gate
- **Task 完成閉環**（`execute-task`）：完成判準、必要驗證、原任務狀態、驗證證據、README Timeline 與 Changelog 全部回寫後才能宣稱完成；移除未命名的獨立實作報告與程式碼副本
- **拆解覆蓋責任**（`decompose`）：每個 Task 新增完成判準、驗證方式、覆蓋項目與責任角色，並檢查需求、交付成果及風險證據都有唯一責任 Task
- **Shell 安全引用**（`git-squash`）：所有動態參數使用 POSIX 單引號，正確處理內含單引號及 `$()`、backtick、環境變數與雙引號
- **PR 證據追溯**（`create-pr`）：Why、How、變更與測試聲明都必須有來源；沒有測試證據時明列未執行項目、原因與殘餘風險

### 相容性

Skill 名稱、目錄結構與 frontmatter description 保持不變。`execute-task` 與 `create-pr` 的輸出契約更嚴格，下游若有依賴舊版實作報告或固定 PR placeholder，更新前應先調整整合方式。

## [1.4.1] - 2026-07-22

### 變更（`rules/` — 下游建議重新複製）

- 將工作流程分級同步改為「規模 + 風險」雙軸：規模決定流程重量，風險決定驗證順序，兩者不得互相推導
- 補上契約驗證、資料盤點、效能實驗、回歸保護網與垂直切片的選擇條件，並明訂垂直切片不是風險優先的預設答案
- `AGENTS.md` 與 `AGENTS.zh-TW.md` 已同步更新，章節數量與順序保持一致

## [1.4.0] - 2026-07-22

### 變更（`docs/`、`skills/`、`workflows/shared/` — 下游建議重新複製）

Issue 評估從單一規模分級改為「規模 + 風險」雙軸，並加強風險優先提示，避免 Agent 將垂直切片當成預設答案。

- **雙軸分工**：`**分級**`（Small / Medium / Large）只決定文件數量、任務清單來源與是否執行 `decompose`；新增 `**風險**`（Low / Medium / High），只決定任務順序、首要驗證與必要證據。Small + High 不增加文件，Large + Low 仍執行拆解
- **風險決策流程**：先辨識最大未知或失敗後果，再比較契約驗證、資料盤點、效能實驗、回歸保護網、垂直切片與一般相依順序；文件必須記錄最大風險、選擇理由及可重複確認的完成證據
- **垂直切片防誤用**：只有端到端整合或使用者行為是最大未知時才採用；外部契約本身未知時優先最小真實請求，資料樣態未知時優先資料盤點與 dry run
- **證據保存**：`execute-task` 執行首要驗證時，必須輸出實際命令結果、測試輸出、樣本觀察或等效資訊，不得只宣稱「已驗證」

### 相容性

既有 `**分級**` 欄位與 `dev-cycle` 分流邏輯保持不變。舊 issue 缺少 `**風險**` 時不自動推測，只有重新規劃或新增步驟時才補評估。

## [1.3.4] - 2026-07-21

### 變更（`skills/`、`workflows/shared/` — 下游建議重新複製）

四個「生成可複製內容」的 skill 統一加上檔案路徑規範，並改善 `git-squash` 的指令複製體驗。

- **相對路徑規範**（`review`、`create-pr`、`create-commit`、`git-squash`）：產出內容中的檔案路徑一律使用相對於 repo root 的路徑（如 `src/auth/login.ts`），不得使用絕對路徑或 `~` 開頭；需指出具體位置時附行號（如 `src/auth/login.ts:42`）。這些內容會貼到 PR、issue 或聊天工具供他人在不同環境閱讀，絕對路徑無法對應，也會洩漏本機目錄結構
- **`git-squash` 指令拆分**：合併方案的三個步驟改為**各自獨立的 code block**（原本是巢狀清單中的行內指令，複製時會沾到說明文字），並明文禁止合併成單一 block；Step 3 改用兩個 `-m`（subject + body），已實測可完整保留 `#` 開頭的 issue 編號

## [1.3.3] - 2026-07-21

### 修正（`skills/`、`workflows/shared/`、`docs/` — 下游建議重新複製）

以模擬 issue 目錄乾跑 `dev-cycle` 的分級判定後，修正兩個會實際卡住流程的漏洞：

- **`dev-cycle` 分級回推規則不完備**：舊規則（只有 README → Small；有 plan 但無 requirement-analysis → Medium；四件套齊全 → Large）在六種常見檔案組合中有三種無法判定（如 `README + requirement-analysis`、`README + plan + requirement-analysis`），會導致舊 issue 卡在分級判定。改為三條互斥且完備的有序 fallback：有分析文件 → Large；否則有 implementation-plan → Medium；否則 Small
- **Small 範本把「已完成」寫死**：`docs/AGENTS.md` 輕量級 README 範本的 `**狀態**` 欄原本固定為「已完成」，但 `new-issue` 是閉環第一步，實作尚未開始；且 `dev-cycle` 需依此欄位追蹤進度。改為 `{狀態}` 佔位並加註不得預先標記完成

### 文件

- `docs/AGENTS.md`：新增 `## 修訂紀錄 (Changelog)`（此前僅要求其他文件撰寫、自身缺漏），metadata 更新至 v1.2
- `docs/usage.md`：註明完整七步示範為 Large 路徑、Small / Medium 跳過 `decompose` 走六步；`dev-cycle` 章節補上分級分流說明
- `skills/README.md`：維護紀錄補記 `dev-cycle` 加入與本輪變更

## [1.3.2] - 2026-07-21

### 變更（`scripts/`、`workflows/README.md` — 下游若未複製 scripts 可略過）

補上守門機制的缺口：`workflows/README.md` 不在同步腳本的複製範圍內，其描述文字過去只能靠人工比對，實際已累積漂移。

- `scripts/sync-skills.py --check` 新增 `check_workflow_readme()`：驗證 `workflows/README.md` 的 Shared Workflows 清單與 `skills/` 一一對應，且每條描述等於對應 `SKILL.md` `description` 的第一句；可偵測描述漂移、漏列、多列孤兒三種情況
- `workflows/README.md`：修正啟用檢查後抓到的 5 條既有漂移（`create-commit` 仍寫著 commit convention 1.0.0、`new-issue` 停留在舊描述等），並加註此清單的維護規則
- `CLAUDE.md`：Conventions 新增 description 撰寫原則（同時寫出做什麼與何時使用）與 `workflows/README.md` 清單的首句約定

CI 既有的 `sync-skills.py --check` 步驟會自動套用新檢查，無需調整 workflow 設定。

## [1.3.1] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

針對 AI agent 的載入機制優化 skill 文件：`description` 是唯一常駐於 context 的部分，也是 agent 判斷「是否要載入整份 skill」的唯一依據，因此補齊觸發時機與適用範圍。

- **description 補齊觸發條件**：
  - `decompose`：明示**僅適用 Large**，agent 不必載入整份 body 即可排除 Small / Medium 的誤觸發
  - `create-pr`：`peer-request`（非通用術語）更正為 **Pull Request**，內文與 `workflows/README.md` 的殘留一併清除
  - `new-issue`：補上產出位置與觸發時機、三級產出說明
  - `create-commit`：補上 Conventional Commits 與「已 git add 後使用」
- **`decompose` 範本去重**：Output 範本中逐字重複的 Phase 2 結構改為結構說明，並加註「不要因為範本只列兩個 Phase 就固定產出兩個」（189 → 167 行）
- **分級規範 single source**：`docs/AGENTS.md`「文件動態分級規範」標示為唯一權威定義，`dev-cycle`、`execute-task` 內的分級表標注為摘要並指向該節

未引入多檔案 progressive disclosure：`sync-skills.py` 為單檔逐位元組複製，SKILL.md 若引用外部檔案會在其他平台的 workflow 端斷鏈。

## [1.3.0] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

為任務切分加入「風險優先」原則，避免 Phase / 步驟被切成技術分層而把整合風險留到最後。深度依分級遞減。

- `decompose`（Large）：新增「Phase 切分原則」——**Phase 1 應優先打通風險最高、假設最未經驗證的那條路徑**，垂直切片為手段而非目的；依未知的類型（外部整合／重構／資料遷移／需求已凍結）給出對應切法，並附正反對照。需求文件標為「未知／待確認」的事項即為排序第一依據
- `docs/AGENTS.md`（Medium / Large）：`implementation-plan.md` 章節新增「實作步驟的排序原則」，未經驗證的假設應排在最前面
- `new-issue`：新增分級自我校驗——規劃 Medium 步驟時若發現未知大到需要獨立探索階段，應升級為 Large 並補齊分析文件
- `docs/usage.md`：示範的 decompose 產出由技術分層改為垂直切片，與新原則一致

Small 級別不受影響。

## [1.2.0] - 2026-07-21

### 變更（`skills/`、`workflows/shared/`、`docs/AGENTS.md` — 下游建議重新複製）

依 issue 分級決定是否需要 `decompose`，修正 Small 級別在閉環中缺少任務清單來源、以及 Medium 級別把實作步驟寫兩遍的問題。

- `docs/AGENTS.md`：新增「任務清單來源」對照表；分級**必須**寫入 `README.md` 結尾 metadata 的 `**分級**` 欄位（兩份 README 範本已加上該欄位）；明訂 Small / Medium 不再產生額外的分解文件
- `new-issue`：將評估出的分級寫回 README；要求實作步驟寫成可直接執行的任務清單（每項有明確產出與完成判準）
- `dev-cycle`：新增「分級判定」小節，僅 Large 觸發 `decompose`，Small / Medium 直接進入 `execute-task`；舊 issue 缺少 `**分級**` 欄位時可由現有檔案回推並補寫
- `decompose`：新增「適用範圍」，標明僅適用 Large
- `execute-task`：description 與 Input 改為依分級查表取得任務清單，不再寫死 Implementation Plan Decomposition

### 下游更新注意事項

既有 issue 文件不需回頭補 `**分級**` 欄位，`dev-cycle` 會依實際存在的檔案自動回推；但新建立的 issue 一律會帶此欄位。

## [1.1.0] - 2026-07-06

### 變更（`skills/`、`workflows/shared/` — 下游建議重新複製）

- `execute-task`：新增「確認工作分支」為第一步，明定分支命名規範（`issue-{ID}` 開頭，可加描述後綴）
- `dev-cycle`：完成階段新增 issue 文件收尾動作（README 狀態、timeline 補記）；明示推進模式為全自動執行（直接 commit、直接建 PR），`create-commit` 的人工把關僅適用於單獨呼叫
- README 開發閉環章節註明 `git-squash` 為閉環外的獨立輔助工具

## [1.0.0] - 2026-07-06

首個正式版本，作為下游專案的更新基準點。

### 現有內容盤點

- **`rules/`**：AI 行為核心規則，中（`AGENTS.zh-TW.md`）英（`AGENTS.md`）雙版，各 10 章節
- **`skills/`**：9 個技能——`new-issue`、`decompose`、`execute-task`、`code-simplify`、`create-commit`、`create-pr`、`review`、`git-squash`、`dev-cycle`，構成完整開發閉環
- **`workflows/shared/`**：與 skills 一一對應的 9 個跨平台工作流（由 `scripts/sync-skills.py` 自動同步）；`workflows/antigravity/` 另有平台特定 workaround
- **`docs/`**：下游 issue 文件規範（`AGENTS.md`）、使用指南（`usage.md`）、實體文件模板（`_templates/`）、五平台安裝指南（`setup/`）

### 本版新增（2026-07-06）

- `scripts/sync-skills.py` 新增 `--check` 模式：驗證配對同步、偵測孤兒工作流、檢查雙語規則章節數
- 新增 `scripts/check-links.py` 與 GitHub Actions CI，於 push / PR 時自動執行檢查
- 新增本 CHANGELOG 與版本策略
- 移除誤入版控的 MCP memory 資料庫並補上 `.gitignore`
- 修正 `workflows/README.md` 漏列 `dev-cycle`、`new-issue` 描述不一致等文件矛盾

### 沿革（1.0.0 之前的里程碑）

- **2026-06-29**：README 新增 Claude Code 下游專案掛載規則（`@AGENTS.md` 匯入法）
- **2026-06-20**：新增 `sync-skills.py` 自動同步腳本、實體文件模板；`new-issue` 實作任務動態分級
- **2026-06-02**：新增 `git-squash` skill 與 workflow
- **2026-05-28**：新增 `dev-cycle` orchestration skill 與使用指南 `usage.md`
- **2026-05-18**：新增五平台安裝指南與 `CLAUDE.md` 維護指引
- **2026-05-08**：建立 `skills/` 目錄結構
- **2026-04-16**：初始版本（`rules/` 與 `workflows/`）
