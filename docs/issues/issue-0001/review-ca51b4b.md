# 審查報告
- 範圍：完整交付範圍（無 PR，本機分支）
- Reviewed BASE SHA：6e494291e23db564054d1df98e5bcd012051a97a
- Reviewed HEAD SHA：ca51b4ba3127991b58f1a4cea369824ca1def109
- Reviewed patch-id：2c5adcdb4a164c1bc336731650bdc50844222622
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose），未參與實作
- Review artifact：docs/issues/issue-0001/review-ca51b4b.md
- 審查日期：2026-10-18

## 問題與風險

### MUST FIX

1. **行動層級沒有涵蓋全部偵測類型，最終實跑有一項沒有歸入任何層級，卻判 PASS**（`需決策`）
   - 位置：`skills/dev-cycle/references/pending-scan.md:76-80`（回報版面）、`:42`（資訊不足的缺追蹤）；判定在 `docs/workflow-results/2026-10-18.md:134-135`、`docs/issues/issue-0001/implementation-plan.md:85`。
   - 事實：三種層級只給了例子，沒有對應九類偵測類型。「待確認未結」沒有指定層級；「缺追蹤＋資訊不足」同時符合「建議整理」（追蹤紀錄）和「無法判定」（來源衝突）。結果是：
     - S5 scan 第二輪把 2215 另列「待確認未結（另列 1）」，沒有放進任何層級（`evidence/s5-final/scan-r2.md`）。
     - 第一輪放在「必須處理」段落裡，但在計數「必須處理（4）」與主表之外，以「另外」附表（`evidence/s5-final/scan.md`）。
     - S4 兩輪分別放在建議整理和必須處理。
     - track 的 2114 在 S5 兩輪分別落在建議整理和無法判定。
   - 影響：SCN-003 的 Then「各項依實際影響呈現必須處理、建議整理或無法判定」，在最終規則的 2 輪中有 1 輪對 2215 不成立。README「追蹤判定的可重現性」要求的「相同證據應得到相同結論」，在層級這個維度也不成立。expected.md 對 2215 寫的是「層級不限定」，意思是三種層級都可以，不等於可以不分層；但 S5 scan 那一列仍判 PASS。不穩定有揭露，所以不算隱匿；但判定與已核准的 Then 不一致，而且原因在規則文字本身，可以重現。
   - 待決問題：「待確認未結」和「資訊不足的缺追蹤」各自歸哪個層級？
   - 可選做法：
     - (a) 在回報版面補一句「每個列出的項目歸入且只歸入一個層級」，並明定兩者的層級（建議：資訊不足 → 無法判定；待確認未結 → 建議整理，若阻擋已到期的必要 gate 則改列必須處理）。之後 track、scan 各重跑兩輪，再更新判定。
     - (b) 使用者接受目前的不穩定為殘餘風險，記入 Gate 豁免紀錄。workflow-results 的 S5 判定也要改成「部分通過／不穩定」，不再寫 PASS。
   - 建議：(a)。修改很小，也能直接回應 SCN-003 和 README 的可重現性要求。

### SHOULD FIX

1. **「優先序」和「來源矛盾」兩條規則沒有說清楚要不要交叉比對**：`skills/dev-cycle/references/pending-scan.md:36-42`
   - 第 36～38 行寫「依下列優先序取得去向」，第 1 步只說 `null` 時才查原文，字面上是有結構化值就停止。第 42 行卻要求結構化欄位與原文不同時標資訊不足，前提是一定要讀原文。
   - 掃描命令可靠的專案，agent 依字面採用 `tracking` 就不會發現矛盾。fixture 的 `scan.py` 品質差，agent 本來就逐一讀了 README，所以實跑沒有暴露這個問題。
   - 建議：第 1 步改成「`tracking` 有值時仍比對原文；兩者指向不同目標即來源矛盾」。

2. **已合併但未結案、且必要驗收還沒做的 issue，可能被歸到錯的層級**：`skills/dev-cycle/references/pending-scan.md:23,25,77-78`
   - 「結案後仍有待觀察」只看 `已完成`。像 `審查中`、已合併、AC-2 `未執行` 而且沒有豁免的 issue，只會命中「已合併未結案」。照第 78 行「只有文件、狀態…需要補整」的語意，加上 fixture 2202 的示範，它會落在建議整理，但實質是合併後還沒滿足的必要 gate。
   - 建議：在必須處理加上「已合併且有未豁免的 AC／SCN 為未執行，不論狀態」，或在建議整理註明「沒有未執行的必要驗收時」。補一個 fixture 對照。

3. **沒登記平台查詢時，「無法判定」可能讓每個 issue 都被列出**：`skills/dev-cycle/references/pending-scan.md:79`
   - 「包括平台狀態未知而可能命中平台相關類型的 issue」：沒登記平台查詢時，第 12 行規定所有 issue 的平台狀態都是 `unknown`。這時每個 `已完成` 的 issue 都可能命中「README 終態、平台仍 open」，每個非終態的 issue 也可能命中「平台已關閉」，於是全部被列成無法判定。這會推翻 v4.7.1「未命中不列」與 WF-24 對照組的行為。
   - track fixture 的 project.md 明寫「沒有遠端平台」，所以這個分支沒有測到。
   - 建議：只限「已登記平台查詢、但該 issue 查詢失敗（403、逾時）」；未登記時維持摘要裡的一行說明。起點前狀態 `unknown` 的 issue 也要寫明照第 82 行只計數，不併入無法判定。

4. **專案規則的例外邊界可能比核准範圍大**：`skills/dev-cycle/references/pending-scan.md:13`
   - 括號裡寫的是類型名稱「結案後仍有待觀察」，但這一類同時涵蓋「步驟仍為 📝／⏳」。fixture 2206 正是依專案規則①合法改判 ⏳ 的案例。字面上可以讀成連 ⏳ 也不准專案規則排除，超出 README「不能藉排除規則隱藏已知未執行且未豁免的必要驗收」的範圍。實跑四輪 2206 都正確不列，所以目前只是文字風險。
   - 建議：改寫成具體條件：「未豁免的 AC／SCN 為 `未執行`，或 `等待外部驗收窗` 的窗口已到」。

5. **acceptance.md 新增的核准範圍句，與「逐題確認」第 5 步的「明說的假設」邊界不清**：`docs/agents/acceptance.md:9` 對 `:19`
   - 第 9 行說推導出的可觀察行為只揭露為假設不算已接受，必須併入提問或標 `待核准`。第 19 行仍允許「非阻塞未知…寫成明說的假設」就算清單清空。agent 可以把推導行為歸成「非阻塞未知」，用假設收尾。
   - 實跑有相近的表現：S5 q4 首則寫「這只是我的假設…不另外問」，後來才改口說會在總結時確認。
   - 建議：第 19 行註明「明說的假設不涵蓋寫入驗收條件的可觀察行為」。

6. **「推導行為擅自核准 0／4」比證據說的更強**：`docs/workflow-results/2026-10-18.md:132-133,146`、`docs/rule-verification-status.md:292`、`docs/issues/issue-0001/implementation-plan.md:85`
   - q4 在 S5 六則回覆中沒有任何 Write／Edit，也沒有產出 README。「不擅自核准 PASS」是沒寫入東西才成立的，應記為「未觀察」，指標改為 0／3、q4 未觀察。
   - q3（S5）的 `undo` 失敗路徑和「再刪除會取代前一筆」是推導出來的。它們不在任何編號題目裡，只在第 2 回合說「寫進 AC-2，等你最後核准時會一起確認」。使用者回「照建議」後，這些就成了已核准 AC-2，但核准來源只對應 TBD-2～5（`evidence/s5-final/artifacts/q3-issue-3103-README.md:22`），追不到題號。q1 的「依 `todo.json` 內順序」也類似。
   - 這些是邊界案例，不一定算違規，但應如實標成邊界，不應計為乾淨的 0。

7. **「S2 首版／曾失效並修正」的修正內容追不到**：`docs/rule-verification-status.md:292`
   - workflow-results 和計畫都沒有記錄 S2 q2 失敗後 acceptance.md 改了什麼。如果沒有改，S5 的 0 只是同一條規則重跑一次的結果，狀態應該寫「S2 1／5 輪失效、S5 未再出現」，不是「修正」。如果有改，要寫出改了什麼，以及 S2 證據對應的是哪一版文字。

8. **`git diff --check` 為 0 的宣稱不成立**：`docs/issues/issue-0001/implementation-plan.md:77,94`
   - 對交付範圍執行 `git diff --check 6e49429 ca51b4b`，exit 2：evidence 的 artifacts 有行尾空白（agent 原文的 Markdown 換行），各證據檔結尾有多餘空行（`run_case.py:137-152` 產生）。當時的 0 應該是因為檔案還沒加入版控，`git diff` 不檢查未追蹤檔案，等於沒有檢查到。
   - 這不是五項必要檢查之一，但屬於誠實回報。建議：更正敘述，註明證據原文的空白刻意保留；如果想消除結尾空行，修 `run_case.py`。

9. **證據經過事後遮蔽，但沒有揭露**：`docs/issues/issue-0001/evidence/**`
   - 證據裡出現 `<scratchpad>…`、`<fixtures>`、`<隔離設定>` 等替代字串和截斷符號 `…`。`run_case.py` 本身沒有遮蔽邏輯（它的截斷用 `...`），可見提交的證據不是腳本的原始輸出。原始 jsonl 也沒有保存在 repo 裡。
   - 遮蔽做得正確（grep `kevin`、`/home/`、`-home-`、`claude-1000` 都沒有命中），但 workflow-results「環境」段應寫明遮蔽規則和做法，讓讀者知道證據有經過處理。

10. **WF-19、WF-24 改了期望，但沒標示未依新期望重跑**：`docs/workflow-regression.md:33,38,49`
    - 兩案的期望已改成新行為（預設合併、三層分組），第 49 行仍引用 2026-10-07、2026-10-16 依舊期望得到的結果。WF-24 的起點前計數、推測型合併、平台 unknown 對照組，在新版面下都沒有重跑。WF-25～27 只覆蓋其中一部分。
    - 建議：在第 49 行註明 WF-19、WF-24 的新期望由 WF-25～27 部分覆蓋，其餘待重跑；或在 rule-verification-status 標出來。

### NICE TO HAVE

- `docs/issues/issue-0001/README.md:19` 仍寫「尚未取得本輪宿主行為基準」，S1 完成後這句已經過時。
- `docs/AGENTS.md:201` 修訂紀錄把「推導出的可觀察行為」寫在「逐題確認」底下，實際位置是 acceptance.md「需求澄清與授權」第 9 行。
- `docs/workflow-results/2026-10-18.md:153` 說「去向定義只在 AGENTS.md」，但 `pending-scan.md:40,42` 又寫了一次不追蹤理由的三個要件和「目標要確認存在」，等於第二個維護位置。建議改成只引用定義，或修正這句宣稱。
- 去向定義有兩處落差：AGENTS.md 要求「該 issue 回連此項」，接受的去向限 issue 或 gate／地雷；pending-scan 第 39 行接受任何「issue／文件連結」，也沒提回連。fixture 只有 2114 涉及沒回連，有回連但目標存在的分支沒有測。
- `docs/issues/issue-0001/fixtures/run_case.py:88-96` 的唯讀快照排除了 `.git`，只看 HEAD。scan fixture 依賴 tag（`v1.1.0`），agent 新增或刪除 tag、分支或 git config 都抓不到。建議把 `git for-each-ref` 的輸出併入雜湊。實跑的工具動作中沒有看到這類寫入。
- q2 的時區：S1 和 S5 的 agent 都把「本機時間」放進時間格式題的建議裡，操作者只回了格式，沒有依 expected.md 回答 D2 的固定答案（UTC）。workflow-results:160 說這是 agent 自行假設，比較準確的說法是操作者沒有回答已被問到的子題。
- `docs/rule-verification-status.md:230,265` 舊列（「一起問」、依 open／closed 分段）依第 173 行的慣例保留歷史即可。v4.8.0 只在「一起問」那列寫了「取代」，分段與 30 字的取代可以補一句。

## 已查核維度

- **驗收與證據**：
  - Gherkin 區塊與 `a6bf934` 逐字相同（awk 擷取後 diff）。SCN-001～004 核准表與 TBD-5 的使用者選擇都有紀錄。
  - SCN-001：q1 回覆數由 4 降為 1（S2 為 1／2）；q2、q3 的複雜題與前提題單獨問，無關的 D2 不問；q4 依偏好逐題。有證據。
  - SCN-002：2111、2112、2113、2115 不列；2116、2117、2119、2120 列出；2114 標資訊不足；2118 的 AC-2 照列，也判定空泛理由不能代替豁免。兩輪 S3 和兩輪 S5 一致，基準每輪誤報 3 筆的對照也有。
  - SCN-003：2207 的漏檢由 1 降為 0；平台 403 列無法判定；正常、已豁免、合法改判的 issue 不列；四輪前後雜湊與 HEAD 相同。層級完整性未達成，見 MUST FIX。
  - SCN-004：指標、誤報、必要 gate 漏檢（0）、重複維護位置與未測分支都有記錄。
  - 判準一致性：expected.md 寫明在實跑前寫定，S1 的判定與它一致；基準 FAIL、候選 PASS 沒有發現事後改判準。只有 2215 的「層級不限定」被放寬解讀為可以不分層。
- **相關失敗面**：
  - 規則一致性：README.md、usage.md、new-issue、workflow-regression、CHANGELOG、AGENTS.md 修訂紀錄沒有殘留「一次問一題」「一起問」「依平台 open／closed 分段」「結論沒有『追蹤：』」等舊說法（只剩歷史紀錄與舊 review）。引用的章節「逐題確認」「待確認事項」「偵測規則」「追蹤判定」都存在，check-links 通過。
  - 追蹤判定的優先序與來源矛盾、九類類型與層級的對應、專案規則邊界，已逐條推演邊界案例：結構化值有效但原文不同、已合併非終態加未執行 AC、未登記平台、⏳ 專案改判、待確認未結。結論見上方 MUST FIX 與 SHOULD FIX 1～4。
  - 測試真偽：install.sh 用 `cp -r` 安裝技能，fixture 建在 scratchpad。工具動作只碰到 fixture 與隔離設定，沒有讀 expected.md 或 kit repo，測試 agent 拿不到正解。測試允許 Edit／Write，所以唯讀是真的被測到；快照比對涵蓋工作樹全部檔案（含被忽略的檔案）與 HEAD。S2 q2 失敗、S4／S5 的不穩定、q4 未完成都有揭露，沒有挑選成功輪次。
- **需求、架構、安全、品質（含跨步驟重複與過度設計）**：
  - 範圍：修改只落在 README「涉及檔案」列出的位置；rules/ 沒動；沒有新增 schema、enum 或設定機制。TBD-5 加強了核准來源，不是削弱，而且有使用者明確選擇。
  - 核心介面：`**分級**`、`**風險**`、`**狀態**`、`**核准 commit**`、已核准／待核准／待重新核准、PASS／RETURN TO execute-task／UNPERSISTED、需決策都沒有變。核准來源、必要驗證、獨立審查、誠實回報沒有被削弱，必要驗收在專案排除下反而更不容易被藏住。
  - 版本：文件版本 2.6、流程契約維持 2.3，判斷合理。章節名沒改；新文件配舊技能只會多問或多列，舊文件配新技能仍能判定；dev-cycle 宣告的最低契約 2.2 仍相容。
  - 檢查：五項檢查我親自執行，全部 exit 0（check-kit、check-links、`bash -n`、test-install 14 項、test-evidence 6 項）。`git diff --check` 對交付範圍為 2，見 SHOULD FIX 8。
  - 隱私：grep `kevin`、`/home/`、`-home-`、`claude-1000`、session id 都沒有命中，路徑已遮蔽，只是沒有揭露，見 SHOULD FIX 9。
  - 重複與過度設計：fixture 產生器和執行腳本的大小與用途相稱，沒有多餘抽象。追蹤要件重述一次屬於輕微重複，見 NICE TO HAVE。
- **豁免、待確認與限制**：
  - 本範圍沒有 Gate 豁免。
  - 已揭露的限制不列為缺失：單一宿主與模型、提問多為一輪、q4 未完成、互動模式的 AskUserQuestion 未測、fixture 的 tag 日期瑕疵、沒有真實平台。
  - 證據持久力：原始 jsonl 與 fixture 沒有保存在 repo，但 build_fixtures.py 可重建，不等於假綠燈。
  - README 狀態「實作中」與計畫 S5「獨立 review 未執行」，和本次審查前的實況一致。

## 流程判定
RETURN TO execute-task
