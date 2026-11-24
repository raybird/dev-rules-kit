# 審查報告
- 範圍：完整交付範圍（`99183c1..03fb11b`，issue #12 分支自 issue #15 分支頂端開出）
- Reviewed BASE SHA：99183c172dedb70bf4484a0114c614a0f5dd4463
- Reviewed HEAD SHA：03fb11b74d6351ef3895918ca5526a6afe3d5829
- Reviewed patch-id：3ffecc8acb0077f4aa4282566465626d3f1e3c11（`git diff 99183c1 03fb11b | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（Claude Code，非原實作者），2026-11-24；工具呼叫上限 30 次

## 問題與風險
- MUST FIX：無
- SHOULD FIX 1：`skills/review/SKILL.md:33`、`skills/review/SKILL.md:51` 的兩處範本改動沒有加流程契約條件，但 `CHANGELOG.md:53`（「2.7 以下的專案照舊完整查核」）與 `docs/issues/issue-0012/implementation-plan.md:27`（「下游 docs 仍是 2.7 以下時……行為與現在相同」）都說舊契約的行為不變。技能最低契約仍是 2.1，所以舊 docs 搭新技能時實際會這樣：
  - 流程契約 2.3 以下的專案拿到的 PASS 提醒寫「提交 README 記帳區段與本報告以外的檔案會讓它失效」，等於說 README 記帳提交可以沿用 PASS。但 2.3 以下只有單獨新增報告的提交能沿用，原段落的「流程契約 2.3 以下只有單獨新增本報告的提交可沿用」被刪掉了。提醒指向的「審查之後的提交」在 2.3 以下的 docs 叫「本機 artifact 提交後的有效性」，同一檔的步驟 5（`skills/review/SKILL.md:20`）仍保留這個對照。
  - 2.7 以下 docs 的 review-evidence.md 要求報告記「判定與 artifact URL／路徑」，新範本卻在本機保存時省略。
  - 兩者都不會讓 gate 誤判：verify-artifact 依被審查提交的流程契約判定，只比對 `Reviewed HEAD SHA`。受影響的是提醒內容，以及相容性說明不準確。
  - 建議：PASS 那一句補回 2.3 以下的括號（或改寫成「依 review-evidence.md 判定」，不寫死哪些檔案可以提交）；`CHANGELOG.md:53` 與計畫的相容段改寫為「2.7 以下沒有只查修正與精簡報告的限制，增量覆審照舊；範本省略 Review artifact 行與縮短提醒對所有版本生效」，「完整查核」容易被讀成「完整審查」。
- SHOULD FIX 2：限制揭露不完整。
  - `docs/rule-verification-status.md:346` 把格式判定整條規則記為「宿主實跑」，但 WF-44b 只實跑了 MUST FIX 例外中的「缺核准來源」這一支。SCN-007 Given 的另一支「狀態值會讓 dev-cycle 判斷錯誤」，以及規則列的 `**核准 commit**`、待確認事項狀態寫錯，都沒有 fixture，也沒有下游案例。`CHANGELOG.md:66` 的「未實跑」只寫了 SCN-003。
  - SCN-004 最後一句「create-pr 以它作為完整範圍的審查證據」在 WF-43 與下游試用都沒有進到 PR，只驗了 verify-artifact。
  - 建議：這兩項在 `docs/rule-verification-status.md:345`、`:346` 與 `CHANGELOG.md:66` 補記為僅靜態撰寫或未實跑。
- NICE TO HAVE 1：`docs/agents/review-evidence.md:80` 的 MUST FIX 例外列了狀態值、`**核准 commit**`、待確認事項狀態，沒有列 `## 現況` 的 `**現行 review**`（dev-cycle 與 WF-30 靠它找現行報告），也沒有列計畫的任務狀態（dev-cycle 據此決定下一步）。總括條款「會讓 verify-artifact、dev-cycle、懸置掃描判斷錯誤」已經涵蓋這兩項；但同一句前半把「欄位寫法」列在降級清單，補上這兩個例子可以減少誤降級。
- NICE TO HAVE 2：`docs/agents/review-evidence.md:69` 的「增量同時夾帶其他修改時照一般增量覆審」沒有寫明，保存上一份報告與記錄建議結論的記帳提交不算「其他修改」。實跑的 reviewer 都自行判對了（wf43-r1 寫「外加記帳」），可以補半句。
- NICE TO HAVE 3：`docs/usage.md:69` 描述增量覆審，沒有提 2.8 起處理建議後只查修正、新建議只限增量引入。計畫 S3 判定 usage 不需改，理由是 usage 沒有提到被改的報告欄位；但這是使用者看得到的收斂行為，可以補一句。
- NICE TO HAVE 4：`docs/issues/issue-0012/evidence/s2-results.md:3` 的環境只寫候選版 `e857e33`，wf44／wf44b 的 r3～r6 實際在 `d4c5bd9`、`066ef00` 跑。各紀錄的 kit HEAD 欄與技能摘要（`969da1a5f024813f`，三者相同）寫得正確，總表可以補一句。
- NICE TO HAVE 5：`docs/issues/issue-0012/evidence/s4-downstream-trial.md:32` 的「依流程契約 2.7，這兩輪都要重查全部失敗面」說得太重。2.7 的增量覆審已允許確認不受影響的結論寫為沿用，差別主要在報告格式與能不能提新建議，建議改成實際的差異。

## 已查核維度
- 驗收與證據：
  - SCN-001：WF-43 wf43 2／2，下游試用 2 輪增量覆審也符合。抽查 `evidence/s2-wf43/wf43-r1-review-8daeb05.md`：逐項確認兩項建議，`overdue` 寫為沿用，新建議只在增量內，PASS 後只有一句，沒有 Review artifact 行，有「其餘沿用 review-5bbeb0d.md」，與 s2-results 第 7 列相符。誘餌沒有鑑別力，已照實記在 s2-results、rule-verification-status 與 CHANGELOG（TBD-4）。
  - SCN-002：wf43b 2／2。
  - SCN-003：僅靜態撰寫，已揭露。
  - SCN-004：格式與 verify-artifact 部分已實跑，create-pr 部分未實跑（SHOULD FIX 2）。
  - SCN-005：WF-32 2／2。
  - SCN-006：wf44 修正 fixture 後 2／2，前兩次失敗都記錄為 fixture 缺陷，規則文字沒改。
  - SCN-007：wf44b 6／6，只涵蓋缺核准來源一支（SHOULD FIX 2）。
- 回歸證據的真偽：expected.md 的判準在 `e857e33` 與規則同一個提交；兩個重跑小節分別在 `d4c5bd9`、`066ef00` 提交。各輪紀錄的 kit HEAD 依序是 `e857e33`（第一次實跑 10 份加基準 2 份）、`d4c5bd9`（r3、r4 共 4 份）、`066ef00`（r5、r6 共 4 份），每次重跑都在對應判準小節提交之後執行，舊結果保留。
- 固定檢查清單：
  1. review-evidence.md 的兩段新增（`:65`、`:69`）和既有的增量覆審三項條件、「審查之後的提交」不矛盾：兩段都以「流程契約 2.8 起」標條件，2.7 以下照原規則。MUST FIX 例外的寫法（不受限、照常列出、寫明上一個 HEAD 就已存在）清楚。可補的地方見 NICE TO HAVE 2。
  2. `skills/review/scripts/verify-artifact.py:89` 只要求 `- Reviewed HEAD SHA` 行，另讀 README 的記帳欄位與流程契約，不讀 Review artifact 行。create-pr（`skills/create-pr/SKILL.md:15`）只引用報告與 BASE／HEAD，限制取自 README（`:16`）。省略這一行不影響兩者。
  3. 格式判定：例外涵蓋狀態值、核准 commit、待確認事項狀態、缺核准或證據、不實回報，加上總括條款。漏列的例子與措辭風險見 NICE TO HAVE 1。wf44 r1、r2 把缺紅綠重構證據列 MUST FIX，可見「必要證據」沒有被降級。
  4. 契約版本：docs/AGENTS.md 為文件版本 2.17、流程契約 2.8（`docs/AGENTS.md:196-198`）。技能最低契約不變（review 2.1、create-pr 2.0）。dev-cycle `:44` 與 review `:17`、`:44` 都以「流程契約 2.8 起」標條件，範本 `:33`、`:51` 沒有（SHOULD FIX 1）。CHANGELOG 已更新版本與下游更新；docs/usage.md 未改（NICE TO HAVE 3）。`scripts/skill-hashes.txt` 已重產：被換掉的兩列是 #15 分支工作區的雜湊（`00c78b89…` 等於 `99183c1` 的 dev-cycle，v5.2.0 tag 的 `03eb5b3a…` 保留）。check-kit 通過。
  5. dev-cycle「PASS 附建議」列（`skills/dev-cycle/SKILL.md:44`）與 review 步驟 2（`skills/review/SKILL.md:17`）一致：兩者都要求派工時寫明這是處理建議後的增量覆審，並指向 review-evidence.md「增量覆審」。dev-cycle 沒有重複「附上選了修正的建議」，交由 review 步驟 2 處理，不衝突。
  6. 見上方「回歸證據的真偽」；限制揭露的缺口見 SHOULD FIX 2。
  7. 核准 commit `05cf010` 是 HEAD 的祖先（`git merge-base --is-ancestor` 成功）。`git diff 05cf010 03fb11b -- README.md` 只動核准 commit 欄（待提交 → 05cf010）、待確認事項與 Timeline，Gherkin 區塊沒改。待確認事項 TBD-1～5 的狀態欄以 `不影響本次交付`／`已解決` 開頭，符合 `verify-artifact.py:50` 的合法值。S1～S4 的證據連結都存在（check-links 通過），S5 為 ⏳。README 沒有 `## 現況`，第一次保存報告時依規則建立。
  8. 對整份 diff 搜尋規定的下游名稱與 issue 編號，沒有命中。fixture 使用的 issue 3601 是 issue-0010 既有的虛構編號，`99183c1` 已在 issue-0010 的 evidence 出現。s4 只寫下游的提交 SHA，沒有名稱與業務內容。
  9. 重複定義：新規則的定義集中在 review-evidence.md（`:65`、`:69`、`:80`）。review 步驟 2、步驟 4 與 dev-cycle `:44` 只寫指標；範本 `:44` 重述報告格式，屬範本的必要內容。沒有分歧的重複，也沒有過度設計。
- 需求、架構、安全、品質：
  - 需求：範圍對應 README 的三類問題，問題 6、7 依 TBD-1 移到 #17。
  - 架構：verify-artifact 不改，檢查器邊界不變；規則留在權威參考檔，技能只放 gate 與指標，符合 AGENTS.md 的檔案責任。
  - 安全：只改文件與規則，不適用。
  - 品質：check-kit、check-links 通過；`python3 scripts/test-evidence.py` 315 項 OK。未跑 test-install（安裝相關檔案沒有改動）。
- 豁免、待確認與限制：
  - 沒有豁免。
  - 第一次審查，沒有增量覆審。
  - 實跑紀錄只抽查 `wf43-r1-review-8daeb05.md` 與 `wf44-r5.md` 開頭；其餘 40 份紀錄只核對 kit HEAD 欄與檔名，沒有逐份讀過判定。
  - 下游試用無法在本 repo 查證，只依 s4 的敘述與記錄的 SHA。
  - 沒有重跑任何 agent 實跑。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
