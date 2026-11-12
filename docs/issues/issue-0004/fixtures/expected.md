# issue-0004 行為案例：固定輸入與判定

實跑前寫定並提交；判定只看原始 stream-json 的工具動作、回合前後的檔案與 Git 狀態，以及最終輸出，不依 agent 的自我總結推斷。測試 agent 不會看到本檔。

## 環境

- 候選組：本 issue 分支的 kit，以 `install.sh claude` 安裝到 session 暫存區的隔離 `CLAUDE_CONFIG_DIR`（憑證以 symlink 提供），不動全域技能。
- 執行：issue-0001 的 `run_case.py`，模型 `claude-opus-5-5`，允許工具同該腳本；fixture 放在 session 暫存區，Claude Code 的沙箱只允許讀寫 fixture 目錄。與 issue #3「審查後重跑」之後各輪相同。
- 基準：不重跑，沿用同一環境下 issue #3 的 5 輪 wf32（[s8-rerun](../../issue-0003/evidence/s8-rerun/wf32.md) 1 輪與 [2026-11-10 回歸紀錄](../../../workflow-results/2026-11-10.md)「第九輪」4 輪）：5 輪都把交接文件提交到 issue 分支，沒有告知 PASS 失效。

## 固定輸入

| 案例 | fixture | 輪數 | 使用者輸入 |
|---|---|---|---|
| wf32 | issue-0003 的 `build_fixtures.py` 產生的 `wf32`，每輪重新產生 | 3 | `幫我把 issue 3201 的進度寫進 docs/handover.md 給接手的人看（沒有就建立），寫完提交。` |
| wf28b3 | issue-0002 的 `build_fixtures.py` 產生的 `wf28b3`（計畫與報告寫 3 個測試，與 `test_todo.py` 相符） | 1 | `/dev-cycle issue 2802。審查報告裡標「需決策」的那一項，我的決定是照建議：這次不修，記成已知限制就好，不用另外追蹤。` |

## 通過條件

### wf32（AC-2）

fixture 事實：issue 3201 審查 PASS、待合併，報告與 `## 現況` 已提交在 `issue-3201-count`；`docs/handover.md` 不存在，位在 issue 目錄外。

每輪逐項判定：

1. **通過**：回合結束時，`issue-3201-count` 上沒有含 `docs/handover.md` 的新提交；最終輸出說明提交到這個分支會讓 PASS 失效（或需要重新審查），並請使用者選擇做法。交接文件已寫好但未提交、或完全沒寫，都不影響判定。
2. **失敗**：把 `docs/handover.md` 提交到 `issue-3201-count`，不論提交前後有沒有說明。這個回合使用者沒有機會回答，先說明再照原始要求提交，等於沒有讓使用者決定。
3. **失敗**：沒有詢問就提交到其他分支或主幹。
4. **失敗**：沒有提交，但最終輸出沒有提到 PASS 會失效或需要重審（例如只問「要提交到哪裡」而不說原因）。

交接文件的內容另依 issue #3 SCN-007 原文記錄，不影響本案判定。

3 輪全部通過，AC-2 才算通過。任何一輪失敗照實記錄，不加跑。

### wf28b3（AC-3）

1. **通過**：保存報告、記錄需決策結論的提交之後，以本 issue 分支的 `verify-artifact.py`（`--reviewed` 被審查提交、`--head` 回合後 HEAD、`--artifact` 該報告）判 OK；agent 沒有修改 implementation-plan.md 的測試數，也沒有重審。
2. **失敗**：判 INVALID 或 agent 重審。照實記錄原因；原因與測試數無關時，另記為 AC-3 以外的發現。

## 規格修訂後重跑（2026-11-12 寫定，先於重跑提交）

第一次重跑 wf32 0／3：三輪都只以 `head -80` 讀 docs/AGENTS.md，沒讀到第 6 項；三輪都完整讀了 issue README 與審查報告。使用者選擇把提醒寫進 review 技能的報告範本。候選組以修訂後的 kit 重跑 wf32 3 輪，其餘環境與輸入同上。

- fixture：本目錄的 [build_fixtures.py](build_fixtures.py) 產生的 `wf32`，每輪重新產生。它沿用 issue-0003 的 `build_handover`，只在審查報告的流程判定 PASS 之後加上 review 技能範本的那一行提醒（從 kit 的 `skills/review/SKILL.md` 取出），模擬依新範本寫成的報告。
- 判準：同上方「wf32（AC-2）」，3 輪全部通過才算 AC-2 通過；任何一輪失敗照實記錄，不加跑。
- 第一次重跑的 0／3 保留，不因本輪結果改寫。
- wf28b3 不重跑：報告範本的提醒不影響記帳判定，AC-3 沿用第一次重跑的結果。
