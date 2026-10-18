# 審查報告
- 範圍：完整交付範圍（無 PR，本機分支；含上一輪報告提交 5a6d967）
- Reviewed BASE SHA：6e494291e23db564054d1df98e5bcd012051a97a
- Reviewed HEAD SHA：2e348b1dc670596166d81e24cb42994c619ab146
- Reviewed patch-id：a3fdcc6b24cbd4b1f3abdfc9ff93d568758f0f93
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose），未參與實作與上一輪審查
- Review artifact：docs/issues/issue-0001/review-2e348b1.md
- 審查日期：2026-10-18

範圍說明：`git log 6e49429..2e348b1` 共有 5 個提交，不是 3 個。除了 ca51b4b、5a6d967、2e348b1，還有 9d639f5（S1 基準、fixture 與 expected.md）和 2ca8db9（TBD-5 決定）。本次審查涵蓋全部 5 個提交。

## 上一輪發現的處理核對

| 上一輪項目 | 結果 | 位置與說明 |
|---|---|---|
| MUST FIX：行動層級沒有涵蓋全部類型 | 已處理，但修正引入新問題 | `skills/dev-cycle/references/pending-scan.md:76-80` 寫明每項只歸一個層級和各層級涵蓋的類型；資訊不足歸無法判定；待確認未結歸建議整理，阻擋到期 gate 時歸必須處理。這些都符合 TBD-6。s8 四輪落點一致，s6、s7 的失敗也如實揭露。但是「已合併而狀態未結案」這個條件把合法的 `等待外部驗收窗` 也算進必須處理，見下方 MUST FIX 1 |
| SHOULD FIX 1：優先序與來源矛盾 | 已處理 | `pending-scan.md:38`：有值時仍比對原文，原文明確指名另一個目標才算矛盾。s7 的 2113 誤報促成這次限縮，s8 兩輪正確 |
| SHOULD FIX 2：已合併、非終態、必要驗收未執行 | 已處理，但引入新問題 | `pending-scan.md:77`、fixture 新增 2216，s6～s8 六輪都列必須處理。但條件沒有排除 `等待外部驗收窗`，見 MUST FIX 1 |
| SHOULD FIX 3：未登記平台時全部列無法判定 | 已處理 | `pending-scan.md:79`；track 六輪都只在摘要說明 |
| SHOULD FIX 4：專案規則例外過寬 | 部分處理 | `pending-scan.md:13` 照上一輪建議改成「未豁免的 AC／SCN 為未執行，或窗口已到」，⏳ 改判確實不再受阻。但這個寫法拿掉了「已完成或已合併」的前提，例外反而比 `:77` 還寬，見 MUST FIX 1 |
| SHOULD FIX 5：假設收尾的邊界 | 已處理 | `docs/agents/acceptance.md:19`；s6 q1～q4 重跑 |
| SHOULD FIX 6：0／4 說得太強 | 已處理 | `docs/workflow-results/2026-10-18.md:147,191`、`docs/rule-verification-status.md:292` |
| SHOULD FIX 7：「曾失效並修正」追不到修改 | 已處理 | `docs/rule-verification-status.md:292` 寫明 S2／S5 的版本、審查後的修改與 s6 結果 |
| SHOULD FIX 8：`git diff --check` 的宣稱 | 部分處理 | S1、S5 的敘述已更正（`implementation-plan.md:77,94`）。但 `implementation-plan.md:114` 宣稱「`run_case.py` 不再寫入結尾空行」不成立，見 SHOULD FIX 2 |
| SHOULD FIX 9：證據遮蔽未揭露 | 部分處理 | `workflow-results/2026-10-18.md:12` 補了遮蔽規則；`implementation-plan.md:115` 也揭露了 s6～s8 另用 `sed` 補遮蔽。但第 12 行說審查後的重跑由 `run_case.py` 在寫入前遮蔽，和第 115 行矛盾，見 SHOULD FIX 2 |
| SHOULD FIX 10：WF-19、WF-24 的舊結果 | 已處理 | `docs/workflow-regression.md:49` |
| NICE TO HAVE（7 項） | 已處理 | README:19、AGENTS.md:201 的位置、權威位置宣稱（workflow-results:154）、去向範圍與回連（pending-scan:39,42）、快照併入 refs／config（run_case.py:25-30）、q2 時區（workflow-results:200）、驗證狀態補「取代」（rule-verification-status:291,295） |

## 問題與風險

### MUST FIX

1. **合法的 `等待外部驗收窗` 會被列為「必須處理」，而且專案規則無法排除**（`需決策`：只限於這類 issue 最後落在哪裡）
   - 位置：`skills/dev-cycle/references/pending-scan.md:77`（「AC／SCN 為 `未執行`（已完成，或已合併而狀態未結案）」）、`:13`（專案規則的例外）、`:23`；同步出現在 `CHANGELOG.md:27-28`、`docs/workflow-regression.md:41`（WF-27）。
   - 事實：
     - `docs/AGENTS.md:145` 規定：「PR 已合併、仍有未豁免的未執行驗證時也記此狀態」，也就是記為 `等待外部驗收窗`。這種 issue 的狀態不是 `已完成`／`不修復`，所以會命中「已合併未結案」（`:23`）。它等待中的 AC 本來就是 `未執行`，依 `:77` 會被列為必須處理，即使窗口還沒到。
     - `:13` 的例外只寫「未豁免的 AC／SCN 為 `未執行`」，沒有「已完成或已合併」的前提。結果是專案判定規則不能排除這類 issue；連尚未完成、AC 本來就全是 `未執行` 的 issue，只要被專案規則排除，字面上也要「照常列出並註明衝突」。這比 `:77` 和 README「已確認而未豁免的必要驗收缺漏」都寬。
     - 實跑可以看出矛盾：s8 對 2216 建議「狀態應改成 `等待外部驗收窗`」（`docs/issues/issue-0001/evidence/s8-final/scan.md:50`、`scan-r2.md:55`）。照新規則，使用者照做之後，2216 仍然會一直列在必須處理，直到窗口到期。
   - 影響：
     - 違反已核准的 SCN-003 Then：「正常進行中的 issue 不被列為異常，專案判定規則仍優先」。
     - TBD-6 的使用者原話以「已到期的必要 gate」作為升級條件，這裡也不符合。
     - 這是 SCN-004 定義的錯誤阻塞。基準只把這類 issue 列為已合併未結案，專案規則還能排除；本次修正把它升到最高層級，而且拿掉了專案覆寫。
     - 下游常見「待真人驗收」這類等待狀態，`pending-scan.md:56-63` 的 JSON 範例本身就是這種情境，影響面不小。
     - fixture 沒有「已合併、等待外部驗收窗、窗口未到」的案例（2213 的窗口已到），所以 s6～s8 的 PASS 沒有涵蓋這個分支。
   - 建議：
     - `:77` 的「已合併而狀態未結案」排除 `等待外部驗收窗`，這類由「窗口到期」處理。
     - `:13` 的例外補上和 `:77` 相同的前提：已完成，或已合併且不是等待中的窗口。另外保留「窗口已到」。
     - 同步 CHANGELOG 與 WF-27。scan fixture 補一個「已合併、`等待外部驗收窗`、窗口未到、AC 未執行」的對照，跑兩輪。
   - 待決問題：已合併、`等待外部驗收窗`、窗口未到的 issue，排除在必須處理之外以後，要怎麼回報？
     - (a) 維持基準行為，以「已合併未結案」列在建議整理。這最小，也在已核准範圍內。
     - (b) 視為合法中間狀態，完全不列。這要修改「已合併未結案」的偵測條件，屬於偵測規則的變更。
     - 建議先採 (a)；(b) 另外決定。

### SHOULD FIX

1. **層級規則還有兩個沒有定義或互相衝突的落點**：`skills/dev-cycle/references/pending-scan.md:24,77,79-80`
   - 窗口事件「無法判斷時照列並註明」（`:24`；JSON 範例 `reached: "unknown"`）：依類型名稱會進必須處理（`:77`「窗口到期」），但它其實是資訊不足。TBD-6 規定資訊不足歸無法判定，而 `:79` 的無法判定只列了兩種情形，沒有包含這一種。
   - `:79` 定義無法判定是「只剩未知」，`:80` 卻規定命中多類時無法判定優先於建議整理。一個 issue 同時有已確認的文件落差（例如沒有未執行驗收的已合併未結案）和平台查詢失敗時，兩條規則的結論不同。
   - 這和上一輪 MUST FIX 是同一類「跨輪落點不一致」的風險，fixture 都沒有覆蓋到。
   - 建議：寫明窗口無法判斷時列哪一層。`:79` 刪掉「只剩」，或 `:80` 改成「有已確認的文件落差時列建議整理並揭露未知」，兩者擇一。

2. **證據處理有兩處敘述與事實不符**
   - `docs/issues/issue-0001/implementation-plan.md:114` 說「`run_case.py` 不再寫入結尾空行」。實際上 `fixtures/run_case.py:100` 的 `.rstrip() + "\n\n"`，產出和修改前的 `"\n".join(lines) + "\n"`（lines 最後是空字串）完全相同。`git diff --check` 對 s6～s8 的 16 個證據檔都回報 `new blank line at EOF`。
   - `docs/workflow-results/2026-10-18.md:12` 說「審查後的重跑由 `run_case.py` 寫入前遮蔽」，但 `implementation-plan.md:115` 承認 s6～s8 是用修正前的腳本產生，截斷處另外用 `sed` 補遮蔽。證據也看得出來：`s7-level-fix/track-r2.md:27`、`s8-final/scan.md:36` 都有 `<scratchpad>…`，連後面的反引號或分隔符一起被吃掉，這不是 committed 腳本會產生的輸出。
   - 遮蔽結果正確，不是假綠燈，但這正是上一輪 SHOULD FIX 8、9 要求如實揭露的內容。
   - 建議：更正這兩句，在第 12 行補「s6～s8 截斷處另以 `sed` 補遮蔽」。結尾空行要嘛真的修掉，要嘛把宣稱撤回。

### NICE TO HAVE

- `docs/workflow-results/2026-10-18.md:202` 限制段仍寫「q4 在 6 則上限停止，後續總結與核准紀錄未觀察」，與同檔第 186、191 行 s6 在上限後的觀察不一致。第 199 和 203 行重複揭露 AskUserQuestion 未測。
- `pending-scan.md:38`：「原文只描述內容、沒有指名目標時採用結構化去向」。如果原文寫的是「追蹤：無」加理由，結構化欄位卻指向某個 issue，兩者在語意上互相矛盾，字面規則卻會採用結構化去向。可以把「原文明示不追蹤」也算作來源矛盾。
- `pending-scan.md:78`：「已完成只剩 📝／⏳ 步驟」歸建議整理。這是實作者依 README 層級定義作的對應，不在 TBD-6 原話內，CHANGELOG 4.8.0 也沒有提。建議在 CHANGELOG 補一句，讓下游知道這類項目不再被當成必要缺漏。
- `expected.md:69` 的「審查後補充（重跑前寫定）」和 s6～s8 證據在同一個提交（2e348b1）。9d639f5 的「實跑前寫定」也一樣，git 無法佐證先後順序，只能採信自述。日後可以先提交正解再實跑。
- s6 scan 兩輪的工作樹雜湊（`176f783682ec8b7a`）與 s7、s8 相同 HEAD `a7bedb1` 的雜湊（`d8293001e1d0de53`）不同。我在 2e348b1 重建 fixture 並用現行 `snapshot()` 計算，結果與 s7、s8 相同。s6 scan 的 fixture 在 HEAD 以外的狀態有差異，原因沒有說明。各輪自身的前後雜湊一致，唯讀判定不受影響。
- 證據含 session id 與 tool_use_id（約 93 處）。它們不屬於本次隱私 grep 的目標，也不是個資；上一輪報告說「session id 沒有命中」，這句不正確，僅供記錄。

## 已查核維度

- **驗收與證據**：
  - Gherkin 區塊：從 `a6bf934` 與 `2e348b1` 的 README 各自擷取後 diff，兩者相同。SCN-001～004 核准表、TBD-5 與 TBD-6 的使用者決定都有紀錄，TBD-6 的內容與 `pending-scan.md:76-80` 的對應一致（MUST FIX 1 的缺口除外）。
  - SCN-001：s6 q1 一則回覆；q2、q3 的複雜題和前提題單獨問；q4 逐題，上限後觀察，7 條 AC 都追得到題號（已抽查 `s6-review-fix/q1.md`、`artifacts/q4-issue-3104-README.md`）。
  - SCN-002：s8 兩輪抽查完整輸出。2111、2112、2113、2115 不列；2114 歸無法判定並附兩個來源；2116、2117、2119、2120 歸建議整理；2118 歸必須處理，也判定空泛理由不能代替豁免。
  - SCN-003：s8 兩輪抽查完整輸出。必須處理為 2201、2207（註明與規則②衝突）、2211、2213、2216；建議整理為 2202、2203、2209、2212、2214、2215、2299；無法判定為 2204；每項只出現在一個層級，與 expected.md 補充一致。
  - 我在 2e348b1 重建 fixture，q、scan、track 的 HEAD 分別是 `4ae3020`、`a7bedb1`、`fe37d52`。用現行 `snapshot()` 計算的雜湊，與 s6 q1、s8 track／scan 證據完全相同，證實這些輪次部署的是最終版的 docs。
  - SCN-004 指標、錯誤阻塞、漏檢與重複維護位置都有記錄。MUST FIX 1 的錯誤阻塞分支沒有被 fixture 覆蓋。
- **相關失敗面**：
  - s6 scan 第二輪 2211 放進無法判定（`s6-review-fix/scan-r2.md:54-60`），s7 track 第二輪 2113 誤判為來源矛盾（`s7-level-fix/track-r2.md:54-56`），都在 workflow-results:173-174、rule-verification-status:294-295 如實揭露。
  - 判準沒有在事後放寬。2215 與 2114 依 TBD-6 收緊為單一層級；2216 是新增的對照。每次修正規則後都以新的隔離設定重跑，沒有挑選成功輪次。最終規則下 track、scan 各只有兩輪，穩定度有限，已列入殘餘風險。
  - 測試真偽：
    - `run_case.py` 快照涵蓋 HEAD、for-each-ref、`.git/config` 和工作樹全部檔案；`.git/index`、hooks 與 objects 不在內，對唯讀查詢來說足夠。
    - fixture 建在 scratchpad。抽查證據的工具動作，沒有讀取 kit repo 或 expected.md，只讀了 fixture 自己的 `docs/.dev-rules-kit.json`。
- **需求、架構、安全、品質（含跨步驟重複與過度設計）**：
  - 範圍：修改落在 README「涉及檔案」之內，`rules/` 沒動，沒有新增 schema、enum 或設定機制。
  - 核心介面：`**分級**`、`**風險**`、`**狀態**`、`**核准 commit**`、已核准／待核准／待重新核准、PASS／RETURN TO execute-task／UNPERSISTED、需決策，都沒有被修改（docs/AGENTS.md 的 diff 只有待確認事項段落與版本）。
  - 版本：文件版本 2.6、流程契約維持 2.3，判斷合理。章節名沒改，新舊組合只會多問或多列；各技能宣告的最低契約（2.0～2.2）仍相容。
  - 檢查：五項檢查我親自執行，全部 exit 0（check-kit、check-links、`bash -n`、test-install 14 項、test-evidence 6 項）。排除 evidence 目錄後，`git diff --check` 為 0。
  - 文件一致性：README.md、docs/usage.md、skills/new-issue/SKILL.md、workflow-regression、AGENTS.md 修訂紀錄，都沒有殘留「一起問」「一次問一題」「依 open／closed 分段」「前 30 字」等舊說法（rule-verification-status 的歷史列依慣例保留，並標了「取代」）。CHANGELOG、WF-27 要和 MUST FIX 1 一起同步。
  - 隱私：在 evidence 與整個 diff 中 grep `kevin`、`/home/`、`claude-1000`、`-home-`，除了上一輪報告引用這些字串本身以外，沒有命中。
  - 重複與過度設計：pending-scan 現在引用 AGENTS.md 的不追蹤理由定義，不再重述。層級列舉偏長，但用途是讓結果可重現，屬於必要。fixture 與腳本的規模和用途相稱。
- **豁免、待確認與限制**：
  - 本範圍沒有 Gate 豁免。
  - 已揭露的限制不列為缺失：單一宿主與模型、提問一輪、互動模式的 AskUserQuestion 未測、WF-24 部分對照未重跑、2216 不在 S1 基準內、無真實平台。
  - 原始 stream-json 沒有進版控，屬於證據持久力的限制，不等於假綠燈。
  - README 狀態「實作中」、計畫 S5 為 ⏳「等待重新審查」，和本次審查前的實況一致。

## 流程判定
RETURN TO execute-task
