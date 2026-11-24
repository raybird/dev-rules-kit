# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：cd252252d76f05093fc54a74f4c916de436ec118
- Reviewed HEAD SHA：fbaac7747a599cdf01b00d398bdda4c3557e1412
- Reviewed patch-id：363928fa4573d44564451fd943d2d97dda99e31c
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose，claude-opus-5-5），唯讀（暫存 HOME 與替身 claude 實跑），工具呼叫上限 30 次（實際 16 次）
- Review artifact：docs/issues/issue-0015/review-fbaac77.md

## 問題與風險

- MUST FIX M1：scripts/trial-session.sh:33-35 以 `cp -a` 複製 `~/.claude/skills`，symlink 原樣複製，install.sh 隨後順著連結寫到原處，違反 SCN-003「原本的 ~/.claude 沒有被修改」，即 README 的最大風險。暫存 HOME 實跑：(A) `~/.claude/skills` 本身是 symlink 時，候選版 kit 技能裝進連結目標（`dotfiles/skills/review/SKILL.md` 被覆蓋，exit 0、沒有提示）；(C) kit 技能目錄是指向其他位置的 symlink 時，install.sh 穿過連結覆寫原處，備份只在 `$SP/.claude/skill-backups`。建議改 `cp -RL`（暫存複本實測 A、C 原處保持原樣）；斷掉的 symlink 會讓 `cp -RL` 失敗並留下已建的設定目錄，要略過或寫明；test-install 補 `~/.claude/skills` 是 symlink、kit 技能目錄是 symlink、相對 symlink 的其他技能三個案例。
- MUST FIX M2：同一行，相對 symlink 的其他全域技能（例如 `archify -> ../../.agents/skills/archify`）搬到 `$SP/.claude/skills/` 後解析到不存在的位置，試用 session 讀不到（實跑情況 B）；維護者本機有 8 個這類技能，違反 SCN-003「其他全域技能照常可用」。修法同 M1；現有測試只用一般目錄的技能，抓不到。
- SHOULD FIX S1：CHANGELOG.md:46、docs/rule-verification-status.md #15 第二列、scripts/trial-session.sh:9 寫「原本的 ~/.claude 不被修改」說過頭：測試只驗證到 exec 之前，session 執行中對 symlink 共用的 CLAUDE.md、settings、projects、hooks、plugins 的寫入會進原檔。建議改成「腳本本身不修改；session 中對共用檔案的寫入會進原檔」，rule-verification-status 註明只涵蓋到啟動前。
- NICE TO HAVE N1：skills/review/scripts/verify-artifact.py:409-411 `--repo` 不是 Git repo 歸為用法錯誤，沒有測試；在 `test_usage_errors_exit_2` 補一個案例。
- NICE TO HAVE N2：scripts/trial-session.sh:28 與 workflow-regression 步驟 1：每次重跑都新建 `trial-{sha}-XXXX`，沒提怎麼清理；步驟 1 補「試用結束後刪除該目錄」。

## 已查核維度

- 核准基線：70f176a 之後 README 只改核准 commit 與狀態，Gherkin 本文未改。
- SCN-001／002：UsageError 只用於參數字串或 rev-parse 可判斷的情況；`issue_dir` 其他呼叫點只有 `tbd_reminders`（包在 except 內），沒有有效性情況被誤歸；所有 Invalid 檢查在其後，`test_usage_error_wins_over_validity_failure` 證實順序。exit 2 跳過待確認事項提醒合理。`--repo` 不是 repo 同屬參數本身、與 argparse 的 exit 2 一致，恰當（缺測試見 N1）。review SKILL.md 補的句子沒有給出不重跑就沿用的路徑，與「結果有效才沿用」一致。skill-hashes 新列與實際檔案 sha256 相符，check-kit 通過。
- SCN-003：HOME 未設時 set -u 停下不寫入；不存在或像選項的 SHA exit 1、不建目錄，縮寫歧義在 rev-parse 失敗；技能取自 git archive（測試在工作區有未提交修改下驗證）；install.sh 在建 symlink 之前執行，不寫進共用的 projects；路徑含空白正確加引號；反向檢查重跑成立。不足：沒有 symlink 案例（M1、M2）。
- SCN-004／005：兩種做法與代價寫在步驟 2，代價與 issue-0011/evidence/s8-downstream.md:38 一致；`--update` 專案路徑、檔案回報、evidence 檔與完成判準都有；全 repo 沒有其他地方要求寫進 `## 現況`。
- 證據：三個 evidence 檔與計畫一致，有命令與 exit code；兩個紅燈重現，來自目標行為缺失；下游試用做法標「僅靜態撰寫」。
- CHANGELOG 與 rule-verification-status：除 S1 與 M1 下不成立的敘述外準確；docs/AGENTS.md 與流程契約未動。
- 五項檢查：全部 exit 0（test-install 34、test-evidence 315），`bash -n scripts/trial-session.sh` 通過。
- README／計畫格式：符合標準格式；TBD-1 狀態合法；狀態只寫階段；Timeline 只記語意事件；沒有其他專案名稱。
- 重複與過度設計：腳本註解與 workflow-regression 少量重疊屬用法說明，可接受；測試 helper 範圍剛好。
- 限制：沒有真的啟動 claude；`.claude.json`、plugins／MCP 在真實 session 是否照常未實跑；所有實跑在暫存 HOME，對真實 `~/.claude` 只做唯讀 `ls`。

## 流程判定
RETURN TO execute-task
