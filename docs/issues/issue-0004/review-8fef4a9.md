# 審查報告
- 範圍：完整 PR（main..issue-0004-post-pass-commit）
- Reviewed BASE SHA：3185a223e5e16e099de11e636de2baa9f1c670fb
- Reviewed HEAD SHA：8fef4a91367427f085d48634418e2f5ac6bff5aa
- Reviewed patch-id：e2666c534f1659379dd061111b9ca9886a64051b
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0004/review-8fef4a9.md

## 問題與風險

- **MUST FIX**：第一次重跑的失敗原因寫錯了。各處都說 agent「以 `head -80` 讀 docs/AGENTS.md，沒讀到第 180 行」，但 agent 其實完全沒讀到 docs/AGENTS.md。
  - 寫錯的位置：
    - docs/issues/issue-0004/README.md:51
    - docs/issues/issue-0004/fixtures/expected.md:42
    - CHANGELOG.md:56（「agent 只讀該檔前 80 行」）
    - docs/rule-verification-status.md:334
  - 實際情形：
    - 三輪唯一讀 docs/AGENTS.md 的命令，是各證據檔第 1 個工具動作。它是以 `cd "$PWD"; …` 開頭的複合命令，在三份證據檔的「權限拒絕」都列著。
    - 原始 stream-json 的 tool_result 為 `is_error: true`，訊息是 "Quoted text in this command can't be checked before it runs"。之後三輪都沒有再讀這個檔，連前 80 行也沒讀到。
  - 影響：0／3 這個結果與判定不受影響。但「規則放得太後面、被截斷」這個診斷不成立，真正的原因是沙箱拒絕了複合命令，agent 沒有改用別的方式重讀。
    - 使用者做規格修訂的選擇（把提醒寫進審查報告）時，依據的是錯的診斷。
    - 修訂後 r2 在同樣被拒絕後改用 Read 讀了全文，可見「只寫在 docs/AGENTS.md 是否足夠」其實沒有測到。
  - 建議：
    - 四處都改為照實描述，並把權限拒絕列為環境限制。
    - expected.md 是先於重跑寫定的判準檔，用帶日期的 NOTE 補記更正，不要改寫原句。
    - rule-verification-status 補一句：docs/AGENTS.md 單獨的效果因讀取被拒而未測到。
  - `需決策`：診斷更正後，規格修訂的做法是否維持、是否要補測「只有 docs/AGENTS.md 規則」，由使用者決定。

- **SHOULD FIX**：報告範本的提醒在流程契約 2.1～2.3 的下游不成立。
  - 位置：skills/review/SKILL.md:47。這個技能宣告的最低流程契約是 2.1（SKILL.md:6）。
  - 問題：提醒寫「提交 issue README 記帳區段與本報告以外的檔案…PASS 會失效」，意思是提交記帳區段可以沿用 PASS。但依 review-evidence.md，流程契約 2.3 以下只接受單一報告提交，改 README 也會讓 PASS 失效。
  - 建議：提醒加上「流程契約 2.3 以下只有單一報告提交可沿用」，或改成「依 review-evidence.md『審查之後的提交』可沿用的提交以外」。改動時要同步更新 fixture，因為 issue-0004 的 builder 用 regex 從範本取出這一行。

- **SHOULD FIX**：`**核准 commit**` 還停在 `475ebcf`（docs/issues/issue-0004/README.md:33）。
  - 修訂後的 AC-1、AC-2 是在 `041514c` 核准的，從 `475ebcf` 比對會看到修訂內容出現在核准之後。
  - 依 verify-artifact 的第 3 條，審查後的記帳提交只能把 `待提交` 改成 SHA，不能把 `475ebcf` 改成 `041514c`。所以這項要在修正提交裡一起改，不能等到保存報告時才回填。

- **SHOULD FIX**：驗證狀態寫得比實測多（docs/rule-verification-status.md:334）。
  - 這一列整體標為「已實跑驗證」，但「審查報告的 PASS 判定附上同一句提醒」這一半，reviewer 有沒有照抄並沒有實跑；fixture 裡的報告是模擬出來的，限制欄雖然有寫。
  - 建議把狀態拆成兩段：交接文件情境「已實跑驗證（3 輪）」，reviewer 照抄提醒「僅靜態撰寫」。

- **NICE TO HAVE**：docs/issues/issue-0004/evidence/wf28b3.md 只有 agent 的命令和它自己的總結，沒有附 `verify-artifact.py` 的原始輸出。
  - expected.md 寫明不依 agent 的自我總結判定。
  - 我已從原始 stream-json 確認 tool_result 為 OK，並在保留的 fixture 上用 HEAD 的 verify-artifact.py 重跑，結果 OK、exit 0。
  - 建議把這行輸出補進證據檔或 README 的步驟 3。

## 已查核維度

- **驗收與證據**：
  - AC-1：
    - docs/AGENTS.md 第 6 項寫了提交前說明、列出可選做法、由使用者決定、project.md 有登記時照登記。
    - review-evidence.md 指向該項，錨點 `#agent-工作流程與時序保留-workflow--timeline-tracking` 和標題的 slug 相符，check-links 也通過。
    - 報告範本有新增的提醒。三處用語一致（「該 issue README 記帳區段與該次報告以外」），和流程契約 2.4 以上「記帳區段沿用 PASS」不衝突；2.3 以下的問題見上方 SHOULD FIX。
  - AC-2：
    - 第一次 0／3 照實保留：三份證據檔的回合內都有提交 `docs/handover.md`，最終輸出都沒提到 PASS 失效，判定正確。
    - 修訂後 3／3：三輪回合後 HEAD 都仍是 `7a5a4ba`，`docs/handover.md` 未追蹤，最終輸出都說明 PASS 會失效，並列出 3～4 種做法請使用者選，符合 expected.md 的通過條件 1。
    - README 說「r1 只引用報告，r2 讀全文、r3 用 grep 引用 docs/AGENTS.md」，和工具動作相符。
  - AC-3：wf28b3 有 1 個記帳提交（只改 README 和新增報告），implementation-plan.md 沒有修改，也沒有重審；verify-artifact 已獨立重跑，結果 OK。
  - 判準與重跑的順序：
    - 原判準在 `abb9f8a`，第一次重跑的 kit HEAD 也是 `abb9f8a`。
    - 修訂判準在 `041514c`，修訂後重跑的 kit HEAD 也是 `041514c`。
    - 兩次的結果都在之後的提交（`61a9c46`、`8fef4a9`）才記錄，判準都先於重跑。
- **相關失敗面**：
  - fixture 可重現：
    - 用 3185a22 版和 HEAD 版的 issue-0003 builder 各產生一次，log 相同，所有 fixture 的分支 SHA 都相同，wf32 是 `a2cb341`，與第一次重跑「前：HEAD」一致。PASS_NOTE 預設是空字串，issue #3 的 fixture 不變。
    - issue-0004 的 builder 產生的 wf32 是 `7a5a4ba`，與修訂後重跑一致；它的報告和 issue-0003 的版本只差提醒那一行。
  - 檢查：
    - `check-kit.py`：OK。
    - `check-links.py`：OK。
    - `test-evidence.py`：244 個測試 OK。
- **需求、架構、安全、品質**：
  - 隱私：diff 新增的行沒有本機絕對路徑或其他專案名稱，證據檔已遮蔽為 `<fixtures>`、`<隔離設定>`。
  - 署名：新增行裡有 3 處 `Co-Authored-By`，都在測試 agent 自己的 Bash commit 指令內，屬於被記錄的測試行為，不是本 repo 的提交訊息。本 repo 5 個提交的訊息沒有 AI 署名。
- **豁免、待確認與限制**：
  - 未逐字核對 issue #3 基準 5 輪的證據，因為不在範圍內。基準組是否也受同樣的權限拒絕影響，未查。
  - 無法確認使用者在對話中的核准原文，只核對了 README 核准來源的敘述。
  - 依指示未跑 claude，也未做回歸實跑。
  - 工具呼叫用量：20／30 次。

## 流程判定
RETURN TO execute-task
