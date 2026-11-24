# Issue 15 — 實作計畫

## 設計與來源

[README](README.md) 是範圍、驗收與核准的唯一來源；風險與首要驗證依 [README 的風險策略](README.md#風險與首要驗證)。本檔是唯一任務與執行證據來源。

### verify-artifact 的錯誤分類

用法錯誤另立例外類別（例如 `UsageError`），`main()` 依類別輸出 `用法錯誤：…；修正參數後重跑，這不是有效性判定` 並回 2；其餘 `Invalid` 與 `CalledProcessError` 照舊回 1。歸為用法錯誤的是參數本身就能判斷的情況：`issue_dir()` 辨認不出 issue 目錄、`--artifact` 與 `--issue` 都沒給、artifact 路徑與 `--reviewed` 不符、兩者指向不同 issue，以及 `--reviewed`／`--head` 在 `git rev-parse --verify {sha}^{commit}` 失敗。判斷要在任何有效性檢查之前完成，避免同一組參數因檢查順序得到不同結束碼。待確認事項的提醒照舊附在後面。

不改的：判定邏輯、輸出 OK 的條件、`INVALID：` 訊息的內容。review 技能只補一句「exit 2 是用法錯誤，修正參數後重跑」，「結果有效才沿用」不變。

### trial-session.sh

由 `~/.cache/dev-rules-kit/kit11-trial-session.sh` 整理：

- 參數：候選版 SHA（必填），其餘參數轉給 `claude`。kit 路徑由腳本位置推出。
- 技能來源：`git archive <SHA>` 解到暫存目錄，再以 `HOME=<設定根> bash <解出的 kit>/scripts/install.sh claude` 覆蓋；不讀 kit 工作區，所以不需要原本的「與 PIN 不同就停止」與 #11 的檢查字串。
- 設定目錄：`~/.cache/dev-rules-kit/trial-<SHA 前 7 碼>-XXXX`，重開機不會被清掉。複製 `~/.claude/skills`，symlink CLAUDE.md、settings、projects、plugins、hooks、credentials、keybindings；複製 `~/.claude.json`（不回寫原檔）。
- 啟動前印出完整 SHA 與設定目錄；最後 `exec env CLAUDE_CONFIG_DIR=… claude "$@"`。
- 只支援 Claude Code；其他宿主在文件寫明未支援。

### workflow-regression「下游試用」一節

放在「結果紀錄」之前，只寫維護者照著做的步驟：

1. 候選版提交後，在下游 issue 的 worktree 執行 `bash <kit>/scripts/trial-session.sh <SHA>`；重開機或重開 session 時以同一個 SHA 重跑。
2. 第一則訊息請下游 session 先問使用者 docs 放法，列兩種做法與代價（SCN-004），選定後以 `python3 <kit>/scripts/init-project.py --update <專案路徑>` 更新，做成一個獨立提交。
3. 試用 session 不在 session 清單時，請它把回報寫到指定檔案。
4. 結果寫進該 kit issue 的 evidence 檔，實作步驟與 rule-verification-status 引用它；下游專案名稱不寫進本 repo。

根目錄 AGENTS.md 的試用段改成「結果記在該 kit issue 的 evidence 檔，做法見 workflow-regression『下游試用』」。

## 實作步驟

| 編號 | 工作與產出 | 相依／啟用條件 | 驗收編號 | 完成判準 | 狀態／證據 |
|---|---|---|---|---|---|
| S1 | `scripts/trial-session.sh` 與 test-install 的測試（首要驗證） | SCN-003 已核准 | SCN-003 | 測試以暫存 HOME 與替身 `claude` 執行：HOME 底下 `.claude/`、`.claude.json` 前後雜湊相同；設定目錄的 kit 技能與 `git archive <SHA>` 的 skills/ 逐檔相同，其他技能保留；symlink 指向原檔；SHA 不存在時 exit 非 0 且沒建立設定目錄。kit 工作區有未提交修改時另跑一次，技能仍與 SHA 相同 | ✅ 2026-11-24 [s1-trial-session.txt](evidence/s1-trial-session.txt)：腳本不存在時兩個測試失敗（紅燈）；加入後通過。`test_trial_session_uses_pinned_skills_and_keeps_real_config` 在 kit 工作區有未提交修改（review 的 SKILL.md）的狀態下執行，設定目錄的 kit 技能與 `git archive` 的 skills/ 逐檔相同，其他技能保留，CLAUDE.md、settings.json、projects 是指向原檔的 symlink，`.claude.json` 是複本，HOME 底下 `.cache` 以外的檔案前後雜湊相同，參數轉給 `claude`；`test_trial_session_rejects_unknown_sha`：SHA 不存在時 exit 1、沒建立設定目錄、沒啟動 `claude`，沒給 SHA 時 exit 2。反向檢查：拿掉 install.sh 那行的 `HOME="$SP"`，快照比對失敗（原本的 `~/.claude` 多出 skill-backups 與覆蓋後的技能） |
| S2 | verify-artifact 的用法錯誤分類；test-evidence 新增用法錯誤的案例；review 技能補一句；重產技能歷代雜湊 | SCN-001、002 已核准 | SCN-001、002 | SCN-001 列的五種參數錯誤各有測試，都 exit 2、`用法錯誤：` 開頭、不含 INVALID；既有測試全部通過（含 exit 1 的案例） | ✅ 2026-11-24 [s2-usage-error.txt](evidence/s2-usage-error.txt)：修改前新測試 7 項失敗（六種參數錯誤都回 exit 1 與 INVALID，`--reviewed`、`--head` 不存在時印出 git 的 CalledProcessError）；修改後 `test_usage_errors_exit_2`（六種：`--issue 15`、artifact 檔名與 SHA 不符、`--reviewed`／`--head` 不存在、兩者指向不同 issue、兩者都沒給）、`test_usage_error_wins_over_validity_failure`（範圍內有未審查變更、`--issue 1` 仍判用法錯誤）、`test_validity_failure_still_exit_1` 通過，test-evidence 全部 315 項通過。另把 `--repo` 不是 Git repo 也歸為用法錯誤。review 技能步驟 5 補「exit 2 是參數錯誤，修正參數後重跑，不代表 PASS 失效」；`build-skill-hashes.py` 重產技能雜湊，check-kit 通過 |
| S3 | workflow-regression「下游試用」一節；根目錄 AGENTS.md 試用段 | SCN-004、005 已核准 | SCN-004、005 | 靜態核對：兩種做法與代價、`--update` 的專案路徑、檔案回報、evidence 檔都寫在步驟裡；全 repo 沒有其他地方要求把試用結果寫進 `## 現況` | ⏳ |
| S4 | CHANGELOG `[未發布]`、rule-verification-status、docs/usage.md 與 README.md 的影響檢查；五項檢查 | S1～S3 | SCN-001～005 | 五項檢查通過；rule-verification-status 寫明 SCN-004、005 只靜態撰寫，實際使用見 #12 | ⏳ |
| S5 | 送獨立審查（工具呼叫上限 30 次，固定檢查清單） | S4 | SCN-001～005 | PASS，或已依使用者決定處理 | ⏳ |
