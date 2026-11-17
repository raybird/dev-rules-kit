# 審查報告
- 範圍：完整 PR（差異覆審，本輪只審 65beeeb..ae6c231，其餘沿用 review-ee77c12、review-151871c、review-65beeeb 的查核）
- Reviewed BASE SHA：c0c7e9f17cbc14a96bd8f28425b910a27be2d3f9
- Reviewed HEAD SHA：ae6c231c67a356edacb64682b8b2ea161fc91817
- Reviewed patch-id：0ee95455924e2575766ba3c57063d04dc7954cbb（以 `git diff c0c7e9f ae6c231 | git patch-id --stable` 重算，結果相同）
- 獨立 reviewer：Claude Code subagent（general-purpose）
- Review artifact：docs/issues/issue-0008/review-ae6c231.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE（`需決策`）：`CHANGELOG.md:37`，SCN-005 第二個 Then 的字面對應。
  - **字面落差**：SCN-005 寫的是「寫明**刪除前**先檢查專案自己的文件有沒有引用 docs/_templates/」。新寫法是「可以手動刪除。不論刪不刪，更新後都檢查……」，條目裡已經沒有「刪除前」這個時機。
  - **語意上仍成立**：檢查改成更新後一律要做，涵蓋先刪再查的情況。檢查的對象是文件裡的文字，刪除之後照樣找得到，結果一樣。這也是使用者在 TBD-6 選擇的寫法，所以我判 SCN-005 成立，不阻擋 PASS。
  - **若要字面一致，可選兩種做法**：
    - 條目改成「更新後、刪除前都先檢查」，不動規格。
    - 把 SCN-005 的 Then 改成「更新後檢查」並重新核准。

    兩種做法都要另做提交，會讓本 PASS 失效。

## 已查核維度
- **驗收與證據**：
  - **核准 commit（清單第 1 項）**：結論是基線成立，沒有造成新的基線問題。
    - 65beeeb 是 HEAD 的祖先。
    - 以 `diff` 比對 65beeeb 與 ae6c231 兩個版本的 README：Gherkin 區塊與核准表都逐字相同。65beeeb 承載目前核准的全部 Scenario 文字，包括修訂後的 SCN-003、006，以及未修訂的 SCN-001、002、004、005。這符合 acceptance.md 對核准 commit 的定義：承載當次核准規格的提交。
    - 核准來源在 65beeeb 之後補了「修訂後的規格由 65beeeb 承載；原核准 c0c7e9f」。這是在核准紀錄欄位補寫追溯資訊，沒有改變任何條件、動作、結果或必要檢查，適用「規格修訂的查核」裡「差異未改變……原核准有效」那條。一個提交本來就不可能寫進自己的 SHA，所以這句只能事後補。
    - 用最後一個修改核准來源的提交來推導基線，只適用於核准 commit 為 `待提交` 的情況，本案不適用。
    - 之後的記帳提交不會再動 `**核准 commit**`，與 verify-artifact.py 第 346～353 行的限制相容。
  - **狀態欄（清單第 2 項）**：
    - `docs/rule-verification-status.md:343` 的狀態欄只剩「本地測試驗證」，屬於「狀態定義」表裡的狀態。
    - 「下游套用（經通知，2026-11-17）：……」移到了驗證來源欄，寫法比照第 250、256 行。
    - 句中有兩個全形冒號（「下游套用（經通知，2026-11-17）：一個下游專案以候選版 `151871c` 更新：2 份核心……」），只是措辭上的小瑕疵，不列為問題。
  - **「更新後檢查」措辭（清單第 3 項）**：
    - `docs/AGENTS.md:204` 的 2.12 修訂紀錄寫「可以刪除；更新後檢查 project.md 等專案文件有沒有寫到它（例如要求它與基線一致）」。`CHANGELOG.md:37` 寫「不論刪不刪，更新後都檢查……例如要求它與基線一致，這類說明已不成立」。
    - 兩處的檢查時機、對象與例子一致，也都涵蓋不刪舊檔的專案。
    - 與 `docs/AGENTS.md:21`「已移除的上游檔案不自動刪除，依版本說明處理」沒有矛盾。
    - SCN-005 的字面對應見 NICE TO HAVE。
- **相關失敗面**：本輪沒有改腳本、測試或技能。init-project.py 的行為沿用 review-ee77c12 的實測結果。
- **記帳性質（清單第 4 項）**：
  - README 的變更有：`**現行 review**` 改指 review-65beeeb.md、`**核准 commit**` 與核准來源（屬送審前的修正，已依第 1 項審查）、新增 TBD-6、Timeline 一列、狀態行。implementation-plan.md 只改了 S6 的狀態欄。Gherkin 與核准表都沒有變動。
  - 新增的 review-65beeeb.md 共 70 行，與我上一輪交回的報告一致：Reviewed SHA、patch-id、三項發現、9 次工具呼叫，以及流程判定 RETURN TO execute-task。
- **根目錄五項檢查（清單第 5 項）**：在 HEAD ae6c231、工作樹乾淨的狀態下執行，全部通過。
  - check-kit：OK
  - check-links：OK
  - `bash -n scripts/install.sh`：OK
  - test-install：16 項 OK
  - test-evidence：296 項 OK
- **需求、架構、安全、品質**：三項修正都是最小改動，沒有新增重複內容或過度設計，也沒有安全面的變化。

## 豁免、待確認與限制
- 沒有豁免。
- 實際 issue 的試用依 TBD-5，等該 issue 至少跑完規劃再進行，不在本輪範圍。
- 工具呼叫用量：本輪 3 次，未超過 30 次上限，必查清單 1～5 項都已查完。比對核准表時，在 scratchpad 寫了一個暫存檔：實作 session 的 scratchpad（t65.txt）。沒有修改 repo，也沒有碰任何真實下游專案。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
