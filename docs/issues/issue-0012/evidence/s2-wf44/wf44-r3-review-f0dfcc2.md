# 審查報告
- 範圍：完整交付範圍（`main..issue-3601-due`）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：f0dfcc225a0c36e6770eea06315f4f4946b8c839
- Reviewed patch-id：4315cef861f7890aecb5669c3eb4251ae1e3af81
- 獨立 reviewer：宿主隔離 subagent（general-purpose，agentId a91314e56994fa0e9），非原實作者；審查日期 2026-11-24

## 問題與風險
- MUST FIX：無
- SHOULD FIX `需決策` — F1：CLI 不能設定到期日，也不能列出逾期。`todo.py:53-59` 的 `add` 不收到期日，也沒有 `overdue` 子命令。使用者只能手動編輯 `todo.json` 才會看到「（到期 MM/DD）」，`overdue` 也只能從程式碼呼叫。issue 概述（`docs/issues/issue-3601/README.md:5`「能列出逾期的未完成待辦」）與根目錄 `README.md:10` 會讓人以為 CLI 能做到。已核准的 SCN-001／SCN-002 本來就寫在函式層級（「執行 render」「呼叫 overdue」），所以這不是驗收缺口。
  - 待決問題：這次交付要不要包含 CLI 入口（設定到期日、列出逾期）？
  - 做法 A：維持函式層級，根目錄 README 與 issue 概述註明到期日要在 `todo.json` 寫 `"due": "YYYY-MM-DD"`，逾期清單還沒有 CLI 入口。
  - 做法 B：照 A 修正文件，另開追蹤 issue 做 CLI 入口，並在 `## 待確認事項` 記一項 `不影響本次交付`，寫上追蹤 issue 編號。
  - 做法 C：這次擴大範圍，新增 Scenario 並重新核准，再實作 `add --due` 與 `overdue` 子命令（同時要做日期格式驗證，例如 `date.fromisoformat`）。
  - reviewer 建議：B。
- SHOULD FIX — F2：根目錄 `README.md:10` 的常青文件只寫了到期日的顯示方式，沒說到期日從哪裡來、格式是什麼，也沒寫逾期功能目前沒有入口。依 `docs/AGENTS.md:169` 也還缺最後驗證日期（這項在本次之前就缺）。內容跟著 F1 的決定修正。
- NICE TO HAVE — F3：有兩個邊界沒有測試鎖住。一是 `due == today` 不算逾期（`todo.py:39` 用嚴格的 `<`，語意合理，但規格沒寫）。二是「沒有到期日時維持原輸出」（TBD-1）只有舊測試 `test_render_marks_done` 間接鎖住。這屬證據持久力，建議補這兩個案例。
- NICE TO HAVE — F4：`todo.py:32-34` 的 `due_of` 只是把 `item.get("due", "")` 包成一個函式，而且 `todo.py:39` 呼叫了兩次。可以直接寫 `i.get("due")`。docstring 開頭的「issue-3601：」是流程用語，可以拿掉。
- NICE TO HAVE — F5：`docs/issues/issue-3601/implementation-plan.md:9` 的「被測內容即 H1 的 todo.py」沒有定義 H1。建議改成 `f0dfcc2`，並註明 S1／S2 的綠燈是同一次執行的共用證據。
- NICE TO HAVE — F6：issue 文件格式有三處可改：
  - Timeline（`docs/issues/issue-3601/README.md:54-55`）記了「完成 S1／S2」，但 `docs/AGENTS.md:179` 規定 Timeline 只記建立、核准、規格修訂等語意事件。
  - `## 涉及檔案`（第 13 行）寫「對應的測試檔」太模糊，也漏列了根目錄 `README.md`。
  - 這些寫法不會讓 verify-artifact 或 dev-cycle 判斷錯：狀態值、核准 commit、待確認事項狀態都正確。

## 已查核維度
- 驗收與證據：
  - 核准基線：`**核准 commit**` 是 `30ddef5`，`**核准來源**` 推導命令的結果也是 `30ddef5`，兩者一致。`git diff 30ddef5 f0dfcc2 -- docs/issues/issue-3601/` 只改了核准 commit 的值、Timeline、狀態與任務狀態，Gherkin 沒有變更，原核准有效。
  - SCN-001：`test_due.py:7-9` 斷言整行字面值。紅綠重構證據在 `implementation-plan.md:9`，四段完整（單迴圈合併與重構 no-op 都寫了理由）。reviewer 把 `70f4ada` 的 todo.py 放回去重現紅燈，結果與紀錄相符。判定：通過。
  - SCN-002：`test_due.py:11-16` 涵蓋逾期、未到期、已完成、沒有 `due` 鍵四種情況。證據在 `implementation-plan.md:10`，四段完整。判定：通過。
  - 測試結果：協調者與 reviewer 各自在 HEAD 跑 `python3 -m unittest -v`，exit 0，Ran 3 tests OK。
  - 假綠燈：期望值都是手寫字面值，與實作獨立，可能與程式碼不一致，不是同義反覆；也沒有 mock 或弱化測試。判定：無。
- 相關失敗面：

  | 輸入／狀態 | 預期 | 實際 | 覆蓋 | 判定 |
  |---|---|---|---|---|
  | 沒有 `due` 鍵 | 輸出與舊版相同（TBD-1） | 相同 | 舊測試與 `test_overdue` 的 id4 間接覆蓋 | 正確 |
  | `due` 為 `None` 或空字串 | 不顯示，不算逾期 | 相同 | reviewer 手動驗證 | 正確 |
  | 已完成且到期日已過 | 不算逾期 | 相同 | 有測試 | 正確 |
  | 到期日等於今天 | 不算逾期 | 相同 | 沒有測試 | 合理，見 F3 |
  | 格式不符（`2026-2-1`、`11/20`、帶時間、非字串） | 正確判斷，或拒絕輸入 | 字串比較會判錯、顯示錯誤，非字串會讓 render 拋出 TypeError | 沒有測試 | 目前只有手動編輯 JSON 才會碰到，不阻擋；若採 F1 做法 C，必須加格式驗證 |
  | 合格的 `YYYY-MM-DD` | 字串比較等同日期比較 | 相同 | 有測試 | 正確 |

- 需求：已核准的兩個 Scenario 都達成，TBD-1 的決定也遵守了。CLI 入口與文件之間的落差見 F1、F2。
- 架構：改動只在單檔 CLI 的 render 與一個查詢函式。`due` 是可選欄位，資料格式向後相容。判定：沒有越界。
- 安全：不適用。沒有新的外部輸入路徑，也沒有權限或 I/O 變更。
- 相依：不適用。沒有新相依，也沒有 lockfile 變更。
- 品質：只有一個任務動到程式，沒有跨任務重複，也沒有過度設計。小幅精簡見 F4。
- 豁免、待確認與限制：
  - 豁免：無。
  - 待確認事項：TBD-1 已解決，已覆核其結論。
  - 限制一：S2 的 stub 紅燈沒有重跑，只依紀錄判斷合理。
  - 限制二：原始核准原話只有「核准」，無法判斷使用者原本是否期待 CLI 入口，所以 F1 標 `需決策`。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
