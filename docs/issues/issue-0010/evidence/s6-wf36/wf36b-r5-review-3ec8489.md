# 審查報告
- 範圍：完整交付範圍（main..issue-3601-due）
- Reviewed BASE SHA：39045ddd5d3458dcf1b32a66f990983c56e2ef07
- Reviewed HEAD SHA：3ec84892aadda8d8d0a57abd541bca1a210ed20d
- Reviewed patch-id：32a6277b590820500acb514b215ec2e04de92565（`git diff 39045dd 3ec8489 | git patch-id --stable`）
- 獨立 reviewer：獨立 subagent（非原實作者）
- Review artifact：本檔
- 增量覆審：上一份報告 review-bcc1068.md（PASS，完整範圍），增量範圍 `bcc1068..3ec8489`（d654db0、3ec8489）；H1 是 HEAD 祖先、無 merge 與改寫歷史，merge-base 仍為 39045dd，流程契約 2.6

## 問題與風險
- MUST FIX 1（`需決策`）：常青文件沒有更新。project.md「常青文件更新責任」規定使用者功能要更新根目錄 `README.md` 使用說明（`docs/agents/project.md:15`）；完整範圍沒有改 `README.md`（`README.md:5-9`），但 `python3 todo.py` 的清單輸出已會多出「（到期 M/D）」。上一份報告沒有查核這一項。待決問題：CLI 沒有設定到期日的入口，`overdue` 也沒有接到 CLI，使用說明要寫到什麼程度。做法 A：說明 `todo.json` 的 `due` 欄位（YYYY-MM-DD）與清單顯示格式，不擴大範圍；做法 B：新增 `add --due` 或 `overdue` 子命令，需新增 Scenario 並重新核准；做法 C：判定不算使用者功能，記入 Gate 豁免紀錄。reviewer 建議 A。
- SHOULD FIX 1：任務證據不完整（`docs/issues/issue-3601/implementation-plan.md:7-9`）。S1、S2 只寫「3 項全數通過」，沒有 verification.md 要求的紅綠證據；S3 只新增測試，沒有標明不改變可觀察行為。本次 reviewer 以錯誤版本確認測試能抓錯並重跑全綠，行為面有證據，不阻擋判定；交付 Proof of Test 前應補命令、被測版本與輸出。
- NICE TO HAVE 1：TBD-1（`docs/issues/issue-3601/README.md:52`）只有結論與日期，缺 AGENTS.md「待確認事項」要求的理由；Timeline（`README.md:59`）記了「審查 PASS」，AGENTS.md 工作流程第 3 項規定 Timeline 只記建立、核准、規格修訂與結案等語意事件。
- NICE TO HAVE 2（`需決策`，不急）：規格沒有規定已完成待辦是否也顯示到期日、月日是否補零（目前為 `[x] 3. 報稅（到期 11/01）`、`（到期 01/05）`）。做法：維持現狀並記為假設，或修訂 SCN-001 後重新核准。reviewer 建議維持現狀並記為假設。

## 已查核維度
- 驗收與證據：SCN-001 由 `test_render_shows_due` 覆蓋，反向情況由 `test_render_without_due`（`test_due.py:18-20`）與 `test_render_marks_done`（`test_todo.py`）覆蓋；SCN-002 由 `test_overdue` 覆蓋。新 HEAD 執行 `python3 -m unittest -v`：Ran 4 tests，OK（test_overdue、test_render_shows_due、test_render_without_due、test_render_marks_done 全部 ok）
- 增量範圍逐檔：
  - `test_due.py`：新增 `test_render_without_due`，期望值為字面值 `"[ ] 2. 寫週報"`；reviewer 在記憶體中把 `due_of` 換成 `item["due"]` 與 `get("due","x")` 兩種錯誤版本，測試都會失敗，不是假綠燈。上一份報告 SHOULD FIX 1 已修好
  - `review-bcc1068.md`：新增上一份報告，必備欄位齊全
  - `README.md`（issue）：d654db0 新增 `## 現況`（位在 `## 概述` 之後）、TBD-1、Timeline 一列並改 `**狀態**`；3ec8489 改 `**狀態**`；都屬記帳區段
  - `implementation-plan.md`：新增 S3 與證據，見 SHOULD FIX 1
- 相關失敗面：
  - 沒有 `due` 的待辦執行 render：不加括號；`test_due.py`、`test_todo.py` 覆蓋，通過
  - `due` 為空字串或 None：render 不加括號、overdue 略過；手動驗證，無測試，可接受
  - 已完成且逾期的待辦呼叫 overdue：不列出；`test_overdue`（id 3）覆蓋，通過
  - 到期日等於今天：不算逾期（嚴格小於）；手動驗證，無測試，可接受
  - 已完成且有到期日執行 render、個位數月日：規格未規定，見 NICE TO HAVE 2
  - `due` 格式錯誤（例如 2026-1-5）：CLI 沒有輸入到期日的入口，不在範圍內
- 需求、架構、安全、品質：增量只動測試與文件，`todo.py` 未改；無安全面；沒有跨 Task 的重複邏輯或過度設計
- 增量覆審時：重新查核了測試集合（新增測試，在新 HEAD 重跑）與 render 在沒有到期日時的行為（SHOULD FIX 1 的前提），結論與上一份報告一致；另查核完整範圍的常青文件義務，得出 MUST FIX 1。沿用：SCN-001／SCN-002 覆蓋、overdue 略過已完成與沒有到期日的待辦、ISO 字串比較順序正確、無安全面（`todo.py` 在增量範圍未改動）
- 豁免、待確認與限制：無 Gate 豁免；TBD-1 已解決，修正已在 3ec8489 完成。決策結論（d654db0）與修正（3ec8489）分在兩個提交，與 dev-cycle「結論與修正放在同一個提交」不一致；不影響本次判定，但屬流程偏差

## 流程判定
RETURN TO execute-task（MUST FIX 1 待使用者選定做法後修正；修正後可以 H1 = 3ec8489 做增量覆審）
