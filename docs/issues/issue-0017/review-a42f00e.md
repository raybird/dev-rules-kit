# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：b26efc5914d2c4f4fdb9dee26b6be2910c56d00e
- Reviewed HEAD SHA：a42f00e0b3dbbed64d8f5bbd5d5f72ec3e3b2ac0
- Reviewed patch-id：b509b3f91319d607a8434e025bf0c12a4fccc809
- 獨立 reviewer：Claude Code 獨立 subagent（claude-opus-5-5）

## 問題與風險

**MUST FIX**：無。

**SHOULD FIX**

1. `docs/AGENTS.md:139`「待確認事項」新寫的那一句比 verify-artifact 寬：「審查之後新增或修改的內容不符合這些寫法時……判為需重新審查」。舊文有兩句被拿掉，分別是 A3「新增的內容與含這些寫法的段落之間空一行」與 A5「或與它們同段落的內容在審查之後變動」，現在只寫在 `skills/review/references/frozen-content.md:21`，而那個檔要等檢查器判需重審之後才會讀。
   - 檢查器的實際行為：`scripts/test-evidence.py:693` 的 `test_append_to_paragraph_with_frozen_line` 證實，在含粗體開頭行的段落後面緊接補一行，就算補的那行本身合規，也判需重審。
   - 對照表的落差：`evidence/s1-rule-map.md` 的 A5 寫「AG 同一句的後半」，但 HEAD 那一句的後半已經沒有「同段落」這個條件。
   - 同類問題：`docs/agents/review-evidence.md:60` 的摘要只列了看起來像標題的行、`[` 開頭與 `<`，漏了粗體開頭與 code fence。粗體開頭在下游的記帳章節很常見（例如 `- **補充**：`）。
   - 影響：錯的方向是安全的（檢查器照樣擋，不會產生假的 PASS），但 agent 會照新文字補記，事後才被判重審，正好是 #17 想減少的成本。
   - 建議：AG 那一句補回「或與它們同段落的內容變動」與「新增內容與這類段落之間空一行」；review-evidence.md:60 補上粗體開頭與 code fence。

2. `docs/agents/readme-templates.md:82` 範本的核准來源寫「（SCN-001～SCN-002）」，但同一個範例表格 `:87` 的 SCN-002 是 `待核准`。
   - 影響：照範本寫出的核准來源會涵蓋還沒核准的 Scenario，與 `acceptance.md:41`「涵蓋的驗收編號」矛盾。更重要的是，`acceptance.md:50` 對 2.7.0 缺陷的守門（單行和仍為 `待確認` 的項目衝突時「先核對核准來源」）就是以核准來源為準；核准來源寫錯，這道核對會認可錯的單行。
   - 建議：範例改成「（SCN-001）」。

**NICE TO HAVE**

3. `docs/agents/review-evidence.md:41` 開頭「下列內容可以照常提交，原 PASS 沿用」沒有寫流程契約版本。它的第二項整條是 README 記帳區段，可是同節後面「流程契約 2.3 以下只接受單一報告提交」，所以對 2.3 的被審查提交，這份清單說得比檢查器寬。
   - 舊文的 R4 掛在「流程契約 2.4 起」之下，舊文 R21（可以併在同一個提交）同樣只對 2.4 起成立。
   - 建議：開頭加「流程契約 2.4 起」，或在清單後註明 2.3 以下見後段。

4. 2.7.0 缺陷（分批時誤用單行）的新守門沒有直接實跑。
   - 新守門的內容是「仍為 `待確認` 的項目寫明待核准時與單行矛盾」，加上 docs/AGENTS.md「待核准 Scenario 必須有對應項目」。
   - WF-47b 用的是表格形式；「單行寫錯、但待確認事項仍待核准」這個組合沒有案例。這一點已在 `docs/rule-verification-status.md:347` 揭露。
   - 建議擇一：加一組 wf47c；或在 acceptance.md:50 寫明單行的前提是現存 Scenario 都出現在核准來源的某一句。

5. `需決策`：只以逐題答案核准、使用者沒看過驗收條件清單時，可追溯性變弱（`docs/agents/acceptance.md:21`、`:41`）。
   - 舊規則記「建議內容」；新規則只記題號對應的驗收編號，答案內容只留在 agent 寫的 Scenario 裡。
   - 沒有登記成待確認事項的提問，reviewer 無從核對「核准範圍只含使用者原話與其接受的答案」（`acceptance.md:9`）。
   - 可選做法：(a) 列為已知限制，寫進 rule-verification-status；(b) 這條路徑改成必須以一則總結確認（acceptance.md 第 5 點已經有這個機制）。
   - reviewer 建議 (a)：這是使用者在 Q 題選定的取捨，而且多數情況會走「看過清單後核准」。

6. 證據的持久性有兩處缺口：
   - `docs/issues/issue-0017/evidence/s4-wf48/wf48-r3.md` 只記了 verify-artifact 的呼叫（第 39 行），沒有記它的輸出與 exit code；`s4-results.md` 寫的「輸出 OK（exit 0）」依據的是沒有提交的 stream-json，持久化的部分只有最終輸出的自述。建議 run_case 摘要附上檢查器的輸出那一行。
   - SCN-001 第三個 Then（範圍決定寫在概述）在 wf45 是「記錄不判定」，而且 r2 沒寫；CHANGELOG「驗證」一段卻寫成全數通過，可以補一句。

7. README 的 TBD-2 仍為 `待確認`，影響欄寫「審查時確認」。本報告的結論見下方「豁免、待確認與限制」；建議在記帳提交把它改成 `已解決`，這屬於記帳區段，不影響 PASS。

## 已查核維度

- **驗收與證據**
  - SCN-001 到 007 都有對應的步驟與證據：SCN-001 對 WF-45、SCN-002 對 WF-46、SCN-003 對 WF-46 與 WF-47、SCN-004 對 WF-47b、SCN-005 對 WF-48、SCN-006 對 WF-48b、SCN-007 對 S1 對照表、S2 與 test-evidence。
  - fixture 與判準只在 `8cfda94` 提交過，實跑紀錄在其後的 `378b2c3`、`a42f00e`，判準先於實跑。
  - 抽查四個判定，都與原始紀錄相符：
    - wf46 r1：TBD-1 寫成「已決定（2026-11-25）」，判準 3 失敗屬實。
    - wf46 r3：改為 `已解決`；核准來源在同一行加一句；Timeline 記了舊基線；已收回單行。
    - wf47b r1：HEAD 前後相同、git status 無變更；回報 SCN-002 待核准、下一步回 new-issue。
    - wf45 r2：核准來源約 130 字，選項只寫在 TBD-1。
  - wf48 r3 有執行 verify-artifact，差異只在整節新增的待確認事項與 Timeline 一列；但檢查器的輸出沒有持久化（見第 6 項）。
  - 五項檢查我重跑過，都通過：check-kit、check-links、`bash -n`、test-install 36 項、test-evidence 315 項。

- **相關失敗面**
  - 清單第 1 項（規則沒有遺失或改義）：R1 到 R26 與 R5a、R7a、R10a 在 HEAD 都找得到語意相同的文字，2.4／2.5／2.3 的條件與例外都在。例如 `核准 commit` 帶反引號或附註也算、`## 現況` 2.4 屬凍結、`**現行 review**` 例外、`<br>`／`<wbr>` 例外。差異只有兩處：A3、A5 在 AG 不完整（SHOULD FIX 1），以及開頭清單沒寫版本（NICE TO HAVE 3）。
  - 清單第 2 項（與 verify-artifact 一致）：verify-artifact.py 對 BASE 沒有 diff（`git diff --stat` 為空）。「可以改的內容」清單加上「依待確認事項寫法書寫」，與檢查器一致；docs/AGENTS.md 那一句偏寬（SHOULD FIX 1）。「凍結內容寫錯時」寫的是「符合下節條件時做增量覆審」，與「增量覆審」三項條件一致。wf48b r2 把增量範圍誤寫成從報告提交起算，但判準不檢查範圍，不影響判定。
  - 清單第 3 項（收回單行的守門）：acceptance.md:50、docs/AGENTS.md「待核准 Scenario 必須有對應項目」、dev-cycle 狀態表（有待核准時回 new-issue）三者一致。readme-templates 的範例有矛盾（SHOULD FIX 2）；守門缺少直接實跑（NICE TO HAVE 4）。
  - 清單第 4 項（核准來源一句）：重新核准那一句寫在同一個 `**核准來源**` 行上（wf46 的實跑也是這樣），所以以 `-G` 錨定欄位行推導 approval_commit 仍然有效，與「規格修訂的查核」相容。逐題答案的追溯性見第 5 項。

- **需求、架構、安全、品質（含重複與過度設計）**
  - 沒有新增 gate。frozen-content.md 是把原本的內文搬出去，沒有重寫成第二份規則；review-evidence.md:60 是指向它的一句摘要，可以接受。
  - skill-hashes 新增的兩列沿用「未發布先標最新發布版」的慣例（`e10971e` 與 `7b53a38` 都這樣做過）。
  - rules 雙語沒有改是合理的：rules/、README.md 都沒有提到核准來源寫法或凍結規則（grep 確認）。
  - 全 repo grep 舊寫法（題號、建議內容、展開表格、同日一次核准），只剩 WF-06、WF-19 註明的舊期望與歷史紀錄。
  - usage.md、CHANGELOG `[未發布]`、rule-verification-status、workflow-regression（WF-06、WF-19 改寫，WF-45～48 新增）的描述都與規則相符。

- **豁免、待確認與限制**
  - Gate 豁免紀錄（下游試用）寫了日期、依據、殘餘風險，格式符合規範，rule-verification-status 也有揭露。
  - TBD-1、TBD-3 都是 `已解決`，結論與日期寫在狀態欄。
  - TBD-2（流程契約是否升版）：只升文件版本到 2.18、流程契約維持 2.8 是正確的。依 docs/AGENTS.md:25-26，流程契約是給技能檢查相容性用的；這次沒有任何技能依賴核准表格式或核准來源寫法，review 技能只多了指向參考檔的一句，verify-artifact 的判定也不變，新舊文件配新舊技能都相容。
  - 核准紀錄自己也用了新格式，Q5 選了建議以外的答案，也照新規則引用了使用者選的那一項。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。

## 限制
- 用了 19 次工具呼叫，沒有到上限。
- s4 實跑紀錄只抽查了 wf45 r2、wf46 r1／r3、wf47b r1、wf48 r1／r3／r4；wf47、wf48b 與基準組沒有逐檔讀。
- 沒有用 fixture 重建 wf48 的 repo 重跑 verify-artifact，也沒有讀 run_case 的原始 stream-json（沒有入庫）。
- verify-artifact 的判定是透過現有的 test-evidence 案例確認的，沒有另外構造新的測試。
