# 審查報告
- 範圍：完整 PR（issue-0002-bookkeeping-commits 對 main）
- Reviewed BASE SHA：6bd2504d70047aa2982195cd138ee0e6c003289b
- Reviewed HEAD SHA：c77928cb834f2f1e005ee90612c9ea1aaebef553
- Reviewed patch-id：e8eb8249ef570a1b97bf81359a6ccad9f0bea825
- 獨立 reviewer：隔離 subagent（未參與實作）
- Review artifact：docs/issues/issue-0002/review-c77928c.md
- 審查日期：2026-11-03

範圍識別已自行重算：`git merge-base main HEAD` 為 `6bd2504`，`git diff 6bd2504 c77928c | git patch-id --stable` 為 `e8eb8249…`，與委派值相同。本 issue 的核准 commit 已回填為 `e383a69`（在第一個實作提交 `9148ef9` 順手回填，沒有單獨提交），因此本報告不記核准基線。`git diff e383a69 c77928c -- docs/issues/issue-0002/README.md` 只有連結錨點改名、核准 commit 回填與一列 Timeline，Gherkin 與核准紀錄沒有變更，原核准仍有效。

以下邊界案例由 reviewer 在 `<scratchpad>/review/` 的拋棄式 repo 以 HEAD 的 `verify-artifact.py` 實測（`adversarial.py`、`legacy_equiv.py`、`relative_cfg.py`、`extra.py`、`gtest/`），路徑依本 issue 證據的遮蔽慣例記為 `<scratchpad>`。

## 問題與風險

### MUST FIX

1. **SCN-005「協調者隨報告提交回填」實跑失效，沒有修正也沒有豁免**：`skills/review/SKILL.md:18`、`skills/dev-cycle/SKILL.md:44`、`docs/agents/acceptance.md:72`。
   - 證據：`docs/rule-verification-status.md:308` 自己登記「曾失效（未修正）」。`docs/workflow-results/2026-11-03.md:42` 寫明 28b2 的 reviewer 已記核准基線 `4ecaa4f`，但保存報告的提交 `53dba91` 沒有回填。我在 fixture 查核過，`53dba91` 的 README 仍是 `- **核准 commit**: 待提交`。根因已經指認：這句只寫在 acceptance.md，協調者在保存報告時讀的 review 技能步驟 5 與 dev-cycle 都沒有指示。
   - 影響：SCN-005 是已核准的驗收條件，它的第二個 Then 有反證，README 卻沒有對應的 Gate 豁免紀錄或待確認事項。`implementation-plan.md:35` 的 S4 仍標 ✅，`implementation-plan.md:82` 寫「候選組五個案例都符合判定」。依 review-evidence.md，PASS 需要「必要驗收及失敗面具證據或明確豁免」，目前兩者都沒有。
   - 建議：在 review 技能步驟 5 的保存報告處寫明：報告記有核准基線，且 README 仍是 `待提交` 時，保存報告的同一個提交要把 `**核准 commit**` 改成該 SHA。dev-cycle 第 44 行或「有效 review 為 PASS」那列同步補一句。接著重跑 reviewer 端的案例（28b2，或計畫原本的 28c「送審時待提交」），再更新 rule-verification-status。
   - `需決策`（只在不打算修時才需要決定）：待決問題是要不要保留「隨報告提交回填」。可選做法有三種：
     - (A) 照上面的建議修正並重跑。
     - (B) 修訂 SCN-005，改成「由下一個本來就要做的提交回填」。這是語意變更，需要重新核准。
     - (C) 在 Gate 豁免紀錄接受這個缺口。
     - 我建議 (A)：只改一句文字，而且根因已經找到。

2. **28b2 的檢查器結果被誤記成「Gherkin 改動」，「改到驗收內容時仍重審」的實跑結論沒有證據支持**：`docs/workflow-results/2026-11-03.md:22`、`docs/rule-verification-status.md:305`。
   - 證據：候選組 28b2 的原始 stream-json（`<scratchpad>/wf28/raw-cand/wf28b2-turn1.jsonl`）裡，檢查器實際輸出 `INVALID：被審查提交之後變更了 docs/issues/issue-2802/implementation-plan.md（M），不屬於記帳區段；需重新審查`。我用 HEAD 的腳本對 `4dbe143..4ecaa4f` 重跑，結果相同。`4ecaa4f` 除了改 SCN-001，同時改了計畫的 S1 證據（4 個測試更正為 3 個），也把核准紀錄的單行改寫成表格。所以 agent 實跑時，檢查器擋下的是計畫檔，「只改驗收內容 → 檢查器 INVALID」這條路徑在實跑中沒有被單獨驗證過。目前只有 `test-evidence.py` 的 `test_gherkin_change_invalid` 覆蓋它。
   - 影響：提交的證據檔 `evidence/s4-candidate/wf28b2.md` 只列工具動作，不含工具輸出，讀者無從自行發現這個誤記。rule-verification-status 據此把「審查後的提交改到驗收內容時仍重審」標成「已實跑驗證」，高估了 SCN-002 與 SCN-006「改動驗收的對照組仍觸發重審」的實跑強度。依 review-evidence.md，這屬於不實回報。28b2 本身依 expected.md 的判準（不宣稱沿用 PASS、回報需要重審）仍然通過，這一點不受影響。
   - 建議：
     - 把第 22 行改成實際訊息，並註明同一提交還混有計畫與核准紀錄格式的變更。
     - 第 305 行改為如實描述：agent 確實重審了，但檢查器第一個違規是計畫檔；「只改驗收」的判定只有腳本測試。
     - 在 `evidence/s4-candidate/wf28b2.md` 補上檢查器的實際輸出。
     - 如要維持「已實跑驗證」，另跑一輪只改 Gherkin 的 28b2 變體。

### SHOULD FIX

3. **核准基線的推導命令沒有錨定在欄位行上，可能選錯基線並掩蓋未核准的規格修改**：`docs/agents/acceptance.md:69`。
   - 問題：`-G '\*\*核准來源\*\*'` 會比對到任何新增或刪除的行，只要那行含有字面上的 `**核准來源**`，例如 Timeline 列或說明文字。本 issue README 第 21、22、31 行就有這種寫法。
   - 重現（`<scratchpad>/review/gtest`）：核准提交 `5b3714a` → 未經核准把 Then 改成 B → 一列提到 `**核准來源**` 的 Timeline 提交 `062271f`。文件中的命令推導出 `062271f`，於是比對 `062271f..HEAD` 看不到中間的未核准修改。錨定版 `-G '^\s*([-*+]\s+)?\*\*核准來源\*\*\s*[:：]'` 正確推導出 `5b3714a`。
   - 影響：這正是 README「風險與首要驗證」列出的第二大風險（推導基線拿錯提交，掩蓋未核准的規格修改）。`test-evidence.py` 只測了範本形狀，沒有這個對照。
   - 建議：把命令改成錨定版，並在 `test-evidence.py` 補「說明文字或 Timeline 提到欄位名」的負向案例。

4. **`verify-artifact.py` 遇到非範本寫法時會放行，方向與「只會更嚴」的原則相反**：`skills/review/scripts/verify-artifact.py:15-17`、`:90-110`，對照 `docs/agents/review-evidence.md:47` 與 README「設計邊界」。
   - 重現：流程契約 2.4，報告與 README 在同一個提交。以下情況全部回報 OK：
     - footer 寫成冒號在粗體內的 `**風險:** High` 改成 `Low`、`**分級:** Medium` 改成 `Small`。FIELD 不匹配這種寫法，整行被當成 Timeline 文字。
     - Timeline 內加入讀者會看成標題、腳本卻不認的寫法：` ## 驗收條件`（前置一格）、`##\t驗收條件`、setext `驗收條件\n---`、`# 驗收條件`、`<h2>驗收條件</h2>`，後面接 `- AC-9: 新增未審查條件`。
     - Timeline 內的 blockquote fence（`> ```gherkin`），或巢狀清單內縮 4 格的 fence。
     - 把 `## 待確認事項` 搬到概述之前，或在凍結章節之間插入第二個 `## Timeline`。這與「所有標題與順序凍結」的寫法不符。
   - 對照組都正確判定無效：第 0 欄的 `## 驗收條件`、第 0 欄的 fence、範本格式的 `**風險**: Low`、驗收條件內新增 `**狀態**` 行、多一個 `**核准 commit**` 行。
   - 影響：本機下游 126 份 issue README 抽查，footer 欄位全部是範本寫法，Timeline 標題也都是 `## Timeline`，所以目前觸發機率低。但這些寫法在 Markdown 很常見，例如 `**Status:**`。放寬的方向與 SCN-002 第三個 Then「藏在記帳區段、改標題……全部判定無效」的意圖相反，也與設計邊界「判定只會更嚴、不會更寬」矛盾。
   - 建議（fail-closed）：在記帳章節內，以下幾類行一律視為凍結：
     - 像標題的行：`^ {0,3}#{1,6}[ \t]`、`<h[1-6]`，以及非空行後接 `^ {0,3}(=+|-+)\s*$` 的 setext。空行後的 `---` 分隔線不算。
     - 前面帶 `>` 或清單符號的 fence 行。
     - 以粗體開頭的行（`^\s*(?:[-*+]\s+)?(\*\*|__)`），兩個記帳欄位除外。
   - 另外依序記錄記帳章節的標題，只允許待確認事項與 Gate 豁免紀錄整節新增或刪除。修正時補對應測試。若決定不修，就把上列寫法登記為已知限制（目前 `implementation-plan.md:49` 只列了縮排程式碼區塊）。

5. **技能引用 2.4 才有的章節與命令，最低契約卻維持 2.1／2.2**：`skills/review/SKILL.md:16`、`:18`，`skills/dev-cycle/SKILL.md:44`。
   - 問題：「審查之後的提交」這個章節與 acceptance.md 的推導命令，在流程契約 2.1～2.3 的下游文件裡都不存在。那些版本的章節名是「本機 artifact 提交後的有效性」，也沒有推導命令。
   - 衝突：`docs/AGENTS.md:27` 的齊備性檢查要求「確認此次分支所引用的材料、章節與欄位齊備；缺漏……暫停依賴該契約的操作」。照這條，技能更新、docs 停在 2.3 的下游可能被暫停，與 README 設計邊界（第 30 行）及 `CHANGELOG.md:32` 的「不會因此暫停」矛盾。這也不符合根目錄 AGENTS.md「相容版本也須檢查引用章節與語意」。這條路徑沒有 agent 實跑（`rule-verification-status` 已登記 2.3 僅靜態撰寫）。
   - 建議：改成跨版本也成立的寫法，例如「『審查之後的提交』（流程契約 2.3 以下為『本機 artifact 提交後的有效性』）」；步驟 3 改成「acceptance.md 有推導命令時依它推導，沒有時依該檔判定缺少核准基線」。
   - `需決策`（只在想改用另一種做法時才需要決定）：可選做法是把 review 與 dev-cycle 的最低契約升到 2.4。但這會讓未更新的下游暫停，與已核准的設計邊界衝突。我建議用措辭修正。

6. **SCN-006 結論與 S4 完成度的陳述不夠完整**：`docs/workflow-results/2026-11-03.md:28-36`、`docs/issues/issue-0002/implementation-plan.md:35`、`:82`。
   - 問題一：實跑前寫定的總計（`8eec4de`：28a＋28c）基準與候選都是 0，原判準「少於基準」其實不成立。回填指標 1→0 只來自看過結果後才追加的 28d，而且每組只跑一輪。expected.md 有寫 28d 是事後追加，也寫了 28a、28c 沒有重現單獨回填。但結論句「兩項指標都比基準組少……SCN-006 判定通過」沒有說明原判準下並未成立。
   - 問題二：SCN-006 第一個 Then 點名的「只為記帳的提交」數量沒有列表。28b 基準組有多個只存報告或只記決策的提交，候選組只有 1 個。
   - 問題三：S4 標 ✅，但它的完成判準（行為案例的 28c reviewer 端、刪除核准來源行的對照組、重跑 WF-14）沒有達成，SCN-005 也有失效項。
   - 建議：在結論處明寫原總計為 0 對 0，減少只來自追加的 28d；補一列記帳提交數；28d 每組再多跑至少一輪，或把結論標成「單輪、初步」。S4 改成部分完成，或註明經使用者決定縮減判準。

### NICE TO HAVE

7. **使用者設定 `diff.relative` 時，`--issue` 模式會放行**：`skills/review/scripts/verify-artifact.py:159` 用的是 porcelain 的 `git diff`。重現：使用者設定 `diff.relative=true`、`--repo` 指向子目錄，並以 `--issue` 執行時，就算改了 `app.txt` 仍回報 OK（`relative_cfg.py`）。`--artifact` 模式在同樣條件下會因路徑不符而判無效。觸發條件冷僻，修法也很簡單：改用 plumbing `git diff-tree -r --no-renames --name-status -z`，或加 `--no-relative`，或先解析 `rev-parse --show-toplevel`。
8. **核准 commit 新值的檢查過寬**：`skills/review/scripts/verify-artifact.py:19`、`:138`。新值可以帶任意尾隨文字，例如 `c1b825c 另外把 SCN-001 改為不需測試` 也會判有效。建議只接受單一 SHA（可加反引號）。另外，目前接受 R 本身或任何祖先，不要求等於推導出的核准基線。要收緊到等於基線是 `需決策` 事項，因為設計邊界寫的是「R 或其祖先」。
9. **平台模式只有正向測試**：`scripts/test-evidence.py:284` 的 `test_platform_report_mode` 只測正向。SCN-001 的平台子句寫的是「同樣只放行」，建議補 `--issue` 加 Gherkin 修改、或加其他檔案的負向案例。
10. **計畫文字與實作不一致**：`implementation-plan.md:11` 寫「讀目前 HEAD 的流程契約」「現行判定需要 `--artifact`」。實作讀的是被審查提交，這與 `review-evidence.md:39` 和 CHANGELOG 一致，而且 2.3 專案用 `--issue` 時，HEAD 等於 R 會回 OK。建議同步計畫文字。
11. **「核准基線」欄位的性質寫法不一**：`CHANGELOG.md:23` 與 `implementation-plan.md:26` 稱它為選填欄位，`review-evidence.md:33` 則列在必備欄位（待提交時）。建議統一為「核准 commit 為待提交時必填」，這也與 MUST FIX 1 相關。
12. **未來的 major 版本也會套用新判定**：`verify-artifact.py:198` 的 `version < (2, 4)` 讓 3.x 也走 2.4 判定。可以限定 major 為 2，其他走現行判定。
13. **小的措辭與標示問題**：
    - `skills/README.md:58`「本機報告檢查器」現在也涵蓋平台模式，可以改寫。
    - 證據檔的「kit HEAD」記的是 harness 工作樹的 HEAD：基準組 28b、28d 也顯示 `6874d9a`，候選 28d 實際用的是 `6874d9a` 的 archive（產品檔與 `8eec4de` 相同）。`workflow-results` 環境段只寫「候選組：git archive 8eec4de」，建議補註。
    - 建議在 rule-verification-status 補一列平台模式（目前只有本地測試）。

## 已查核維度

### 驗收與證據

| SCN | 證據位置 | 結論 |
|---|---|---|
| SCN-001 | `test-evidence.py` BookkeepingTests 的有效案例（一個或多個提交、Gate 豁免整節、平台模式、只新增報告）；候選 28b `64d6842`（reviewer 重跑檢查器為 OK，並列出 Timeline、待確認事項）；28b 最終輸出列出被審查 HEAD、目前 HEAD 與變更區段 | 主要行為成立。平台子句只有正向腳本測試（NICE 9）。非範本寫法的放寬見 SHOULD FIX 4 |
| SCN-002 | `test-evidence.py` 的 18 個負向案例，訊息都指出路徑、章節或欄位（`evidence/s1-messages.txt`）；候選 28b2 實跑 | 腳本層成立，對抗案例見 SHOULD FIX 4。實跑層的檢查器 INVALID 來自計畫檔，不是驗收（MUST FIX 2） |
| SCN-003 | `LegacyBookkeepingTests`、`NoContractBookkeepingTests`；reviewer 以 v4.8.1 與 HEAD 腳本對 10 種情境比對，2.3 與無 AGENTS.md 下結果完全相同，無效訊息附註需要 2.4 | 成立。新增行為：2.3 下 `--issue` 在 HEAD 等於 R 時回 OK，無害。沒有 agent 實跑，已登記僅靜態撰寫 |
| SCN-004 | 28a、28c、28d 的 fixture 提交（reviewer 逐一用 git 查核）：候選組回填都併入實作提交；28d 候選維持 `待提交`；28c 以 `cc1d449` 為基線 | 成立。28a、28c 基準組也沒有單獨回填，只有 28d 能區分兩組，而且每組一輪 |
| SCN-005 | Then 1：28b2 報告記錄核准基線 `4ecaa4f`（推導正確）；Then 2：28b2 失效；Then 3：只有命令測試（`test_baseline_missing_without_approval_source`） | **未通過**：Then 2 有反證（MUST FIX 1）；推導命令有誤判路徑（SHOULD FIX 3）；Then 3 沒有 agent 實跑，已揭露 |
| SCN-006 | `docs/workflow-results/2026-11-03.md`、`evidence/s2-baseline`、`evidence/s4-candidate`、fixture repo | 方向成立：28b 記帳觸發的重審 1→0，28d 單獨回填 1→0，28b2 沒有沿用 PASS。但原定總計為 0 對 0，減少來自事後追加的單輪案例（SHOULD FIX 6）。改動證據與程式的對照組沒有 agent 實跑；改動驗收的對照組有混雜因素（MUST FIX 2） |

根目錄五項檢查（reviewer 於 2026-11-03 在 `c77928c` 自行執行）：`check-kit.py` exit 0、`check-links.py` exit 0、`bash -n scripts/install.sh` exit 0、`test-install.py` 14 個測試 OK（exit 0）、`test-evidence.py` 75 個測試 OK（exit 0）。`test-evidence.py` 相對 base 只有新增、沒有刪除行，既有 6 個測試原樣保留。

### 相關失敗面

| 輸入／狀態 | 預期 | 現有覆蓋 | 判定 |
|---|---|---|---|
| 2.3 或無 AGENTS.md，任何記帳提交 | 維持舊判定 | 測試類別，加上 reviewer 新舊腳本比對 | 通過 |
| 範本形狀的凍結章節、欄位、fence 變更，以及標題吞內容、搬 Gherkin | 無效並指出位置 | 腳本測試與 reviewer 對照組 | 通過 |
| 非範本寫法的標題、欄位、fence，以及記帳章節重排或重複 | 無效（設計原則） | 沒有覆蓋 | 會放行（SHOULD FIX 4） |
| 核准 commit 改成另一個 SHA、不可解析值、非祖先、孤兒提交 | 無效 | 腳本測試 | 通過 |
| 核准 commit 改成 SHA 加尾隨文字，或改成 R 本身 | 嚴格應只接受 SHA | 沒有覆蓋 | 放行（NICE 8） |
| merge 夾在範圍內、R 不是祖先、報告新增後又改、既有報告被改、symlink 或可執行報告、README 改成 symlink | 無效 | 腳本測試與 reviewer 實測 | 通過 |
| 淨差異相同但中間提交改過程式又還原 | 依 TBD-3 以淨差異判定 | 設計已核准 | 符合設計 |
| 使用者設定 `diff.relative`，`--issue` 模式，子目錄 `--repo` | 無效 | 沒有覆蓋 | 放行（NICE 7） |
| 推導基線時，說明文字或 Timeline 含 `**核准來源**` | 推導出真正的核准提交 | 沒有覆蓋 | 誤判並掩蓋修改（SHOULD FIX 3） |
| 刪除核准來源行 | 判定缺少基線 | 命令測試，規則要求 ref 上仍有該行 | 文字正確；agent 未實跑 |
| rebase／squash | 依改寫規則重新核對 | 腳本「R 不是祖先」即判無效；推導命令在 rebase 後自然取得新 SHA；squash 會把未核准修改併入基線，由 acceptance.md 第 80 行的改寫規則承擔 | 可接受 |
| dev-cycle 第 44 行：RETURN 加 `需決策` | 重審 | 「原判定為 PASS」守住 RETURN；語意變更由檢查器擋下 | 文字正確；它只能和檢查器一樣強（SHOULD FIX 4）；回填沒有指示（MUST FIX 1） |
| 2.3 下游配新技能 | 不暫停 | 沒有實跑 | 可能暫停（SHOULD FIX 5） |

### 需求、架構、安全、品質

- **需求**：TBD-1～3 的決策都落實在腳本與規則中。腳本先於規則文字完成（`9148ef9` 早於 `6feffbf`），符合首要驗證的順序。範圍沒有擴張到 issue 列出的不在範圍項目。
- **架構與單一說法**：review-evidence.md、usage.md、review 技能、dev-cycle、CHANGELOG 與 docs/AGENTS.md 修訂紀錄，對「2.4 起放行記帳區段、2.3 維持單一報告提交、契約取自被審查提交」的說法一致。不一致的地方有三處：
  - 實作計畫的契約來源與 `--artifact` 必填（NICE 10）。
  - 「核准基線」是選填還是必備（NICE 11）。
  - acceptance.md 寫了協調者回填，執行該動作的技能卻沒有寫（MUST FIX 1）。
- **版本**：文件版本 2.8、流程契約 2.4、最後更新 2026-11-03、CHANGELOG [4.9.0]（2026-11-03）、修訂紀錄彼此一致。技能宣告的最低契約沒有改。下游更新方式寫在 `CHANGELOG.md:32`，安裝指令沒有變，INSTALL.md 不需要改。雙語 rules 沒有改動。
- **安全**：指令維持唯讀；artifact 路徑、symlink 與檔案模式的檢查都沿用。發現的放行路徑見 SHOULD FIX 4 與 NICE 7、8。
- **品質與過度設計**：腳本約 200 行，`legacy()` 原樣保留舊邏輯，新判定集中在 `analyse()`、`check_readme()`、`bookkeeping()`，沒有分歧的重複邏輯。測試以真實 Git 執行，負向案例斷言了違規位置，沒有發現假綠燈。`derive_baseline` 依 acceptance.md 第三個 bash 區塊取命令，對區塊順序敏感，但壞掉時會大聲失敗，屬於證據持久力的問題，不是假綠燈。

### 豁免、待確認與限制

- README 沒有 Gate 豁免紀錄；TBD-1～3 都已解決。MUST FIX 1 目前沒有任何豁免。
- 已揭露且屬實的限制：WF-14 沒有另外實跑；28c 改成實作前推導；刪除核准來源行的對照組沒有 agent 實跑；平台模式只有腳本測試；只測 Claude Code；每組一輪。fixture 預寫的 PASS 報告本身有誤，已在「觀察」揭露。依 verification.md，揭露限制不構成缺失。
- 設計上的殘餘風險（已由 TBD-1、3 核准，不列為缺失）：
  - PASS 後新增的 Gate 豁免紀錄與待確認事項不再經過 reviewer 覆核，只靠檢查器列出的變更區段與 PR 證據揭露。
  - Timeline 的純文字內容可以自由寫入。
  - 新規則下，記帳不再觸發重審，原審查漏掉的問題也不會再被順帶抓到（回歸紀錄「觀察」已說明）。
- 本次只做靜態審查與腳本實測，沒有重跑宿主 agent。

## 流程判定
RETURN TO execute-task
