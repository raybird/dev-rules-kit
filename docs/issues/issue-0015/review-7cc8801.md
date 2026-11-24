# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：cd252252d76f05093fc54a74f4c916de436ec118
- Reviewed HEAD SHA：7cc8801cc6f1d47671c97fe98d1ab149f7ad371b
- Reviewed patch-id：4998f241dfb1df4812203acb2c6b9cf0bc5dbfd7
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose，claude-opus-5-5），唯讀（暫存 HOME 與替身 claude 實跑），工具呼叫上限 30 次（實際 11 次）；本輪只查核上一份報告五項的修正與修正本身
- Review artifact：docs/issues/issue-0015/review-7cc8801.md
- 增量覆審：上一份報告 review-fbaac77.md，增量範圍 `fbaac77..7cc8801`（3a10bea 保存報告、7cc8801 依報告修正）

## 問題與風險

- MUST FIX：無。
- SHOULD FIX：無。
- NICE TO HAVE N3（報告原編號 N1，改號以免與上一份報告的 N1 混淆）：scripts/trial-session.sh:61 印出的「設定目錄」是 `$SP/.claude`，docs/workflow-regression.md:67 與腳本註解第 12 行說的設定目錄是上一層 `trial-{SHA 前 7 碼}-XXXX`。照「試用結束後刪除」刪印出的路徑會留下同一層的 `kit/`，佔用 ~/.cache，不影響正確性。建議印出時多一行「試用結束後刪除：$SP」，或步驟 1 寫明刪上一層。

## 已查核維度

- 增量範圍：3a10bea 只保存報告與 README 記帳；7cc8801 只含 trial-session.sh 修正與兩個新測試、test-evidence 的 N1 案例、CHANGELOG／rule-verification-status／workflow-regression 說法、計畫 S4～S6、README TBD-2 與最大風險一句、s6-symlink.txt 新增與 kit-checks.txt 覆寫；沒有範圍外變更。
- M1：暫存 HOME 實跑，`~/.claude/skills` 為絕對或相對 symlink、kit 技能為指向別處的 symlink、`~/.claude/skills` 不存在、`~/.claude/skills` 是斷掉的 symlink，HOME（不含 .cache）的檔案雜湊與連結目標都不變。`shopt -s nullglob dotglob` 只包住迴圈並還原，dotglob 不配對 `.`、`..`；trap 在 mktemp 成功後才設、單引號延遲展開、SP 未被重新指定，只刪這次建的目錄；exec 前 `trap - EXIT`。PATH 上沒有 claude 時 exec 失敗會留下已印出的目錄，屬可接受邊界。
- M2：相對連結的技能在設定目錄可讀，skills 底下沒有 symlink；頂層斷掉的連結略過並印到 stderr；技能內部有斷掉的連結時非 0 結束、不留目錄、不啟動 claude。
- 測試：以 `git show fbaac77:scripts/trial-session.sh` 換回舊腳本，3 項失敗，訊息與 s6-symlink.txt 相同，都是目標行為缺失（第 3 項是新做法的失敗路徑）。變異測試：`cp -R` 第 1、3 項失敗；`cp -RH` 第 3 項失敗；拿掉 trap 第 3 項失敗；拿掉斷連結略過第 1 項失敗；逐項 glob 已穿過 skills 目錄連結，第 1 項守住解參照，分工合理。拿掉 `HOME="$SP"` 兩項快照測試失敗。N1：argparse 取最後一個 `--repo`，把 verify-artifact.py:411 的 UsageError 改成 Invalid 時該 subTest 失敗，確實測到。
- S1、N2：腳本註解、CHANGELOG、rule-verification-status 改為腳本本身不修改、session 中對共用檔案的寫入會進原檔；狀態註明到啟動 session 為止，「四項試用腳本測試」數目正確；workflow-regression 步驟 1 寫明每次重跑新建目錄、試用結束後刪除，佔位字無 `<`。唯一差異見 N3。
- 計畫與 README：`## 現況` 只有現行 review；TBD-2 狀態合法、附日期與結論；狀態只寫階段；Timeline 與既有慣例一致；S6 證據與 s6-symlink.txt 一致；S4 註明 kit-checks.txt 由 S6 覆寫，test-evidence 仍 315 項（N1 為 subTest）。
- 五項檢查：check-kit、check-links、`bash -n scripts/install.sh`、test-install 36 項、test-evidence 315 項全部通過，`bash -n scripts/trial-session.sh` 通過。
- 沿用 review-fbaac77：核准基線、SCN-001～005 其餘查核、證據檔、docs/AGENTS.md 與流程契約未動、重複與過度設計。
- 限制：沒有真的啟動 claude，`.claude.json`、plugins／MCP 在真實 session 是否照常與 session 寫入共用檔的情形未實跑；實跑都在暫存 HOME，對真實 `~/.claude` 沒有讀寫。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
