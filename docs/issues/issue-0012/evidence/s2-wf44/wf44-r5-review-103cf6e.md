# 審查報告
- 範圍：完整交付範圍（`main..issue-3601-due`，merge-base 即 main）
- Reviewed BASE SHA：70f4ada99d53e2a4426341d3ee5bb1d0ebbb4faf
- Reviewed HEAD SHA：103cf6e3b4b42c83b0045ea25bb5b054baf919db
- Reviewed patch-id：597c29cef3271ea3e3a907083a2565b2bceb6517（`git diff 70f4ada 103cf6e | git patch-id --stable`）
- 獨立 reviewer：宿主隔離 subagent（general-purpose），非原實作者；協調者複核其引用的規範條文（`docs/AGENTS.md:139`、`docs/AGENTS.md:179`）

## 問題與風險

MUST FIX：無。

- SHOULD FIX `需決策`：due 沒有寫入途徑。`todo.py:18-21` 的 `add` 與 `todo.py:53-59` 的 `main` 都沒改，CLI 不能設定 `due`，`overdue` 也沒接到 CLI。使用者只能手改 `todo.json`，但概述（`docs/issues/issue-3601/README.md:5`）與根目錄 `README.md:10` 讀起來像功能已可用。實作與核准範圍一致：SCN-002 的 When 是「呼叫 overdue」，屬函式層級，所以不算缺漏。待決問題：本 issue 是否只交付顯示與函式層級的逾期判斷？
  - A（建議）：維持範圍。在待確認事項記 `不影響本次交付`，寫明追蹤去向（另開 issue 處理 `add --due` 與 overdue 指令），並在根目錄 README 註明 due 目前要手動寫入、格式為 YYYY-MM-DD。
  - B：新增 Scenario、重新核准後再實作。
- SHOULD FIX `需決策`：due 格式沒有驗證。`todo.py:39` 用字串字典序比較，`todo.py:48` 用 `due[5:]` 取月日，兩者都假設 due 是補零的 YYYY-MM-DD。實測（today=2026-11-19）：
  - `"2026-2-1"` 判為不逾期（應逾期）。
  - `"11-20"` 顯示「（到期 ）」且判為逾期。
  - 整數 `20261120` 讓 `render` 拋出 TypeError，列出指令跟著崩潰。
  
  目前唯一的寫入途徑是手改 JSON，風險低。處理方式隨上一項決定：改由程式寫入並驗證時，這裡不必防禦。
- SHOULD FIX：TBD-1 的結論「使用者選不顯示」寫在影響欄（`docs/issues/issue-3601/README.md:48`），也沒有理由。依 `docs/AGENTS.md:139`，結論、理由與日期應寫在狀態欄，影響欄只寫影響與驗收編號。狀態值 `已解決` 正確，不影響流程判斷。
- SHOULD FIX：Timeline 記了「完成 S1」「完成 S2」（`docs/issues/issue-3601/README.md:55-56`）。依 `docs/AGENTS.md:179`，Timeline 只記建立、核准、規格修訂這類語意事件。這兩列屬記帳區段，審查後刪除不會讓 PASS 失效。
- NICE TO HAVE：概述寫了進度（`docs/issues/issue-3601/README.md:5`「目前 S1、S2 都已完成……等待審查」），會隨流程變舊。概述屬凍結章節，適合在下次本來就要做的修正時一併處理。
- NICE TO HAVE：`test_due.py` 沒測「到期日等於今天不算逾期」，也沒直接測 TBD-1「沒有 due 不顯示」（目前靠 `test_todo.py` 間接覆蓋）。屬證據持久力改善。
- NICE TO HAVE：`due_of`（`todo.py:32-34`）只是 `item.get("due", "")` 的包裝，`overdue`（`todo.py:39`）每筆呼叫它兩次，可簡化成只取一次。docstring 的「issue-3601：」前綴不屬於常青程式碼。
- NICE TO HAVE：已完成的待辦也顯示到期日（`[x] 1. t（到期 11/01）`），規格沒有定義。行為合理，要確定下來可補一句規格。
- NICE TO HAVE：提交 subject `feat: 待辦支援到期日與逾期清單` 缺少 project.md 規定的 `type(scope)` 中的 scope。

## 已查核維度

- 驗收與證據：
  - 測試：`python3 -m unittest -v` 在 103cf6e 執行 3 個測試，全部 OK。
  - SCN-001：`test_render_shows_due` 斷言字面值 `"[ ] 1. 繳費（到期 11/20）"`，期望值取自規格原文，不是同義反覆。紅燈、綠燈、重構 no-op 都記在 `docs/issues/issue-3601/implementation-plan.md:9`。單迴圈合併成立：CLI 列出就是 `print(render(load()))`。TBD-1 的決議有遵守。判定：通過。
  - SCN-002：`test_overdue` 期望人工推導的 `[1]`，測資另加了已完成與沒有 due 的項目。紅燈用回傳 `[]` 的 stub 得到 `[] != [1]`，是目標行為造成的紅燈。綠燈 3 個測試 OK，重構 no-op（`docs/issues/issue-3601/implementation-plan.md:10`）。判定：通過。
  - 核准基線：`**核准 commit**: 30ddef5`。`git diff 30ddef5 103cf6e -- docs/issues/issue-3601/README.md` 只有核准 commit 值、Timeline 與狀態的差異，Gherkin 沒變，核准有效。
- 相關失敗面（today=2026-11-19）：

  | 輸入／狀態 | 預期 | 實際 | 覆蓋 | 判定 |
  |---|---|---|---|---|
  | 沒有 due 欄位 | 不顯示、不逾期 | 符合 | test_todo、test_overdue#4 | OK |
  | due 是 `None` 或 `""` | 同上 | 符合 | 無 | OK |
  | due 等於今天 | 不逾期 | `[]` | 無 | OK，建議補測 |
  | 已完成且過期 | 不逾期 | `[]` | test_overdue#3 | OK |
  | 已完成且有 due 的顯示 | 規格未定 | 顯示到期 | 無 | NICE TO HAVE |
  | 跨年 2027-01-05、2025-12-31 | 前者不逾期、後者逾期 | 符合 | 無 | OK |
  | 沒補零 `2026-2-1` | 逾期 | 不逾期 | 無 | SHOULD FIX `需決策` |
  | `11-20`、整數 | 拒絕或容錯 | 顯示空白、誤判、TypeError | 無 | SHOULD FIX `需決策` |
  | today 傳入 date 物件 | 依介面約定 | TypeError | 無 | 沒有呼叫端，可接受 |

- 需求：沒有超出核准範圍。`main`、`add`、`done` 都沒改，`overdue` 沒接 CLI，和 SCN-002 一致。範圍落差列為上方 `需決策` 項。
- 架構、安全、依賴：不適用。單檔 CLI，沒有新依賴、權限或外部輸入面，資料只來自本機 `todo.json`。
- 品質（含跨 Task 重複與過度設計）：沒有過度設計，S1、S2 共用的 `due_of` 沒有分歧。簡化空間見 NICE TO HAVE。
- 常青文件：根目錄 `README.md:10` 正確描述顯示行為，但沒說 due 怎麼產生（併入第一項）。
- issue 文件：`**狀態**: 審查中` 是有效值。`**核准 commit**` 正確，且在 feat 提交裡順手回填。`## 現況` 由保存本報告的提交建立。
- 豁免、待確認與限制：
  - 沒有豁免。TBD-1 是 `已解決`，維持原狀。
  - 紅燈證據只能根據 implementation-plan 的文字紀錄核對，無法重現當時的工作樹。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA；之後提交 README 記帳區段與本報告以外的檔案會讓它失效，提交前先告知使用者（review-evidence.md「審查之後的提交」）。
