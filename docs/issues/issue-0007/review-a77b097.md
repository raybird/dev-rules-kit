# 審查報告
- 範圍：完整 PR（main..issue-0007-status-vocabulary）
- Reviewed BASE SHA：81368f7cba13cc24e53284ba052a1a1ce51b9761
- Reviewed HEAD SHA：a77b097b84c2ad7b713ceb205b14bdd832e1296d
- Reviewed patch-id：6a2b18e83baf8a37b15b5b565efa8fcd7a06c9ba
- 獨立 reviewer：獨立 subagent（未參與實作）
- Review artifact：docs/issues/issue-0007/review-a77b097.md

## 問題與風險
- MUST FIX：無
- SHOULD FIX：無
- NICE TO HAVE：
  1. skills/review/scripts/verify-artifact.py:416-430（`tbd_rows`）切欄位用的是 `split('|')`，沒有處理 `\|`。狀態欄之前的儲存格（例如「事項」）只要有跳脫的 `\|`，欄位就會往後錯一格。實測 `| TBD-1 | a \| b | 已解決 | SCN |` 讀到的狀態是 `b`，於是對一列合法的狀態印出提醒。判定與 exit code 不受影響（只會多一則誤報的提醒）。建議切欄時跳過 `\|`，例如用 `re.split(r'(?<!\\)\|', ...)`，並補一個測試。
  2. verify-artifact.py:433-438（`tbd_status_valid`）會把開頭所有非英數字元都去掉，範圍比文件寫的「粗體、反引號與 ✅ 這類符號」大。實測結果：`~~待確認~~ 已定案`、`（待確認）`、`[已解決](x)` 都判為合法。刪除線是「劃掉舊狀態、後面改寫新值」的實際寫法，這裡會漏報。這是寬鬆方向的漏報，只影響提醒。以數字開頭的值（`2026-11-12 已解決`、`1. 已解決`）判為不合法，空白與 `**`、`` ` ``、✅、⏳ 都能正確去掉，這些和文件、s0-scan 的分類一致。是否收窄範圍（至少不去掉 `~`），或在 pending-scan.md 寫明「開頭的非文字符號」，`需決策`。
  3. skills/dev-cycle/references/pending-scan.md 掃描命令輸出格式的 `tbd[].status`，沒有說明要輸出儲存格原文。專案的掃描命令如果把狀態先正規化（例如去掉粗體，或映射成規定值），新類型「待確認狀態不合法」就偵測不到。建議在欄位說明補一句「`status` 為狀態欄原文」。
  4. 同檔的「已合併未結案」「平台已關閉、README 未結案」寫的是「狀態不是 `已完成`／`不修復`」，dev-cycle SKILL.md 狀態偵測表寫「狀態為 `已完成`」。這些措辭比本次新說明更早，而新說明已明講「寫在開頭、後面可以接括號說明」，照文意可以讀成以這些值開頭，不構成矛盾。若想讓字面比對的 agent 也不誤判，可以改成「以 … 開頭」，但不必在本 issue 處理。
  5. `tbd_rows` 的章節範圍遇到 fence 裡的 `## ` 會提早結束，同章節有第二個表格時，它的表頭會被當成資料列。兩者都只會造成提醒的漏報或誤報，不影響判定。

## 已查核維度
- 驗收與證據：
  - AC-1：docs/AGENTS.md 已改標題，補上自由描述的例子（「實作中」「審查通過，待合併」），並說明寫在開頭、可以接括號說明。verification.md 的錨點已同步，check-links OK。全 repo 搜尋舊標題，只剩 CHANGELOG 4.11.0 的敘述、rule-verification-status 第 67、79 行的歷史列、docs/reviews 與 issue-0001 的歷史報告，以及 issue-0007 自己的文件。沒有其他連結以舊錨點引用，skills/ 與 rules/ 也沒有。
  - AC-2：expected.md 在 8948ad9 提交（17:54:43），r1、r2 記錄的 kit HEAD 都是 8948ad9，判準確實早於實跑。我依通過條件獨立判定兩輪：
    - r1：在「建議整理」列出 3401，並指出 TBD-1 的「已定案」不是三個值之一。3402 只在「其他」說明粗體算合規，沒有因狀態被列出；3403 沒有列出。回合前後 HEAD 都是 80033e3，工作樹雜湊相同。判定通過。
    - r2：列出 3401，偵測類型直接寫「待確認狀態不合法」。3402、3403 只說明為合法。前後狀態相同。判定通過。
    - 結果 2／2 通過，與 README 的敘述一致。
  - AC-3：s1-red.txt 共 24 項，失敗 12 項，正是 3 個正向案例乘 4 個測試類別；s1-green.txt 284 項 OK。我重跑 test-evidence.py，284 項 OK。測試涵蓋下列情況：修改的列、新增的列、粗體加 ✅ 的標準值、未修改的舊列、INVALID 時仍附提醒（exit 1）、表頭沒有狀態欄。
  - AC-4：s1-rejudge.md 列了 7 個既有判定（wf28b3、wf31、下游試用 5 個），main 版與分支版的 exit code 都是 0、輸出相同、都沒有提醒。另一個案例（f3eeac8）只在分支版多一行 TBD-5 的提醒。這些和 README、CHANGELOG 的敘述一致。
- 相關失敗面：
  - `main()` 先把判定結果與 exit code 定好，再呼叫 `tbd_reminders`。`tbd_reminders` 整段包在 `except Exception` 裡，也不會呼叫 `sys.exit`。
  - 我逐一檢查了這些情況：README 不存在（`git show` 失敗會回傳 {}）；沒有指定 `--artifact`／`--issue`（`issue_dir(None)` 丟出 TypeError，被攔下）；artifact 路徑不合法而 verify 先判 INVALID（提醒照常計算，不影響 exit 1）；git 指令失敗（CalledProcessError 被攔下）；`--issue` 模式（以 issue 目錄定位 README）。這些情況都不會改變 OK／INVALID 或 exit code。
  - 列的比對：同編號且整列相同時不提醒，新增的列會提醒，刪除的列不提醒，和 AC-3 的設計一致。
  - 提醒印在 stdout，INVALID 照舊印在 stderr。review/SKILL.md 沒有要求解析 stdout 的固定格式。
- 需求、架構、安全、品質：
  - 三個合法值在 verify-artifact 的 `TBD_STATUSES`、pending-scan.md、CHANGELOG 與提醒文字中都一致。
  - 文件版本 2.10、最後更新 2026-11-12、修訂紀錄列都正確。流程契約維持 2.5 也合理，因為判定語意沒有改變。
  - CHANGELOG 4.11.0 與 rule-verification-status 的數字和實作、證據一致：1915 = 1667 + 47 + 201，201 列 75 份、47 列 19 份，284 項，7 個重判。rule-verification-status 把「狀態表改名」標為「僅靜態撰寫」，也是誠實的標示。
  - 新增的表格列扣掉 code span 後，`|` 的數量都和欄數相符，沒有未跳脫的 `|`。
  - check-kit OK，check-links OK，test-evidence 284 項 OK。
  - 隱私：新增行沒有本機絕對路徑或其他專案名稱，下游已遮蔽為 `<downstream>`、`issue-{下游}`。提交訊息沒有 AI 署名。
- 豁免、待確認與限制：
  - 這個 issue 沒有 Gate 豁免。README 步驟 3「收尾」還是 ⏳，送審中屬於正常。
  - WF-34 只測了 Claude Code，rule-verification-status 已揭露。agent 看到提醒之後會不會改正，沒有實跑過，也已揭露。
  - 依指示沒有跑 claude，也沒有修改 repo。
  - 工具呼叫約 13 次（上限 30），清單上的項目都查完了。

## 流程判定
PASS
PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
