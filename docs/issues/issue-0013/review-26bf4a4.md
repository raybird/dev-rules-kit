# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：071fa2811ad504cad15383fe93820756f605b55d
- Reviewed HEAD SHA：26bf4a4b582f282e33854898bc6405450c7404a6
- Reviewed patch-id：849f2183a843d7d48ffb9948b39b2881b698c036
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose，claude-opus-5-5），唯讀（暫存目錄重跑），工具呼叫上限 30 次（實際 15 次）
- Review artifact：docs/issues/issue-0013/review-26bf4a4.md

## 問題與風險

- MUST FIX：無。
- SHOULD FIX S1 `需決策`：INSTALL.md:48 的可移除清單「`docs/agents/` 底下 project.md 以外的檔案」會涵蓋專案自己放在 docs/agents/ 的檔案（project.md 範本第 19 行請專案記錄獨立地雷檔的路徑，常放在此處）；init-project.py 只部署 docs/AGENTS.md 與 kit 的 docs/agents/*.md，並記在 docs/.dev-rules-kit.json 的 `files`。agent 照字面列清單會把專案自訂文件混進去，正是 README 列的最大風險。建議限定為 manifest `files` 列出的檔案加上 manifest 本身，或明列六份參考檔名。現行寫法與已核准的 AC-3 相同，收窄屬規格修訂，由使用者決定。待決問題：是否修訂 AC-3 收窄可移除清單。
- SHOULD FIX S2：docs/issues/issue-0013/evidence/s1-s2-upgrade.txt、s3-lite.txt 只有輸出，沒有 `$` 命令行、被測 kit 版本與工作區狀態；p2b 段只剩「# 既有」；README:63 五項檢查只有「全部通過」的文字。verification.md:20、87 要求記錄實際命令、結果與被測提交。結論在 reviewer 重跑後一致，但持久化證據無法照著重跑。建議補命令、kit 來源版本與五項檢查輸出摘要；evidence 不屬記帳區段，修正後需再送審。
- NICE TO HAVE N1：CHANGELOG.md:25、39、57 同一個 `[未發布]` 區段出現文件版本 2.15 與 2.16；發版時統一成一句（例如「更新到 2.16（含）以上」）。
- NICE TO HAVE N2：INSTALL.md:35 第 3 步分成三條路，沒寫不確定時由誰決定；建議補「是否使用 issue 流程不確定時，先問使用者」。
- NICE TO HAVE N3：project.md 範本刪掉第一句後，輕量專案沒有 docs/AGENTS.md，下游沒有地方說明「本檔由專案維護、更新時保留」；範本第 11、19 行提到的 document-types.md、`## 現況`、懸置掃描在輕量專案不存在。可在 INSTALL.md 輕量步驟加一句「範本裡 issue 流程相關的段落可以忽略」。
- NICE TO HAVE N4：CHANGELOG 與 README 說刪掉的第一句「docs/AGENTS.md『客製邊界與同步策略』已寫」略多：該節第 7、19 行涵蓋專案內容集中於 project.md 與 `--update` 保留既有 project.md；「初始化只在不存在時建立」只在 INSTALL.md:43。

## 已查核維度

- 核准基線：ac42c5f 之後 README 只改涉及檔案一行、核准欄位回填、TBD-1 結論、實作步驟證據、Timeline 一列與狀態；AC-1～AC-4 本文未改。
- AC-1：修訂紀錄表移除；三行版本資訊與 CHANGELOG 絕對網址正確；check-kit 以 `^\*\*流程契約\*\*` 讀取通過。全 repo（排除 issues 與 CHANGELOG）沒有要求新增這張表的列或引用它；docs/AGENTS.md:169、186 與 execute-task 範本講的是下游常青文件的修訂紀錄。CHANGELOG:735 舊決策「保留修訂紀錄作為出處證明」由版本三行加連結取代，不矛盾。
- AC-2：範本只刪第一句；新增雜湊 cc28be97…29fd 等於 `git show 071fa28:docs/agents/project.md | sha256sum`；test-install 歷代雜湊測試（test-install.py:91-93）通過。
- AC-3：輕量步驟（INSTALL.md:47）不存在才複製、已存在不動、不執行 init-project；之後完整初始化保留 project.md（實測）。移除前提寫在步驟本身（:48），由使用者決定，完成判準（:50）限定只移除上列檔案；清單不含 project.md 與 issue 目錄，但 docs/agents/ 範圍偏寬（S1）；舊版的 docs/_templates/ 不在清單，屬保守。分流句（:35）與原本「只安裝技能時略過」語意一致。create-commit（SKILL.md:6）與 project-worktrees（SKILL.md:8）只讀 project.md、不宣告流程契約，輕量專案可用。
- 證據：reviewer 以 `git archive 071fa28`／`git archive 26bf4a4` 在暫存目錄重跑 p1（升級無衝突、`--check` exit 0、無 `^## 修訂紀錄`、舊範本提醒照常）、p2（輕量後完整初始化，自訂內容保留）、p3（舊範本原文加候選版完整初始化仍被認出），與 README 描述一致。AC-1 改用 `^## 修訂紀錄`、AC-3 dry-run 改用等價證據的理由成立（acceptance.md:7）。移除說明在 README 與 rule-verification-status 都標只靜態，沒有把未執行寫成通過。格式缺口見 S2。
- AC-4：`git diff --stat 071fa28 26bf4a4` 10 個檔案，不含 skills/、rules/；流程契約 2.7；CHANGELOG 與 rule-verification-status 的 #13 段描述準確；docs/usage.md 錨點 `#3-初始化或更新專案文件` 人工核對正確（check-links 不驗錨點）。
- 五項檢查：在 26bf4a4 的乾淨工作樹全部 exit 0。
- README 格式：符合輕量格式；沒有現行審查與外部狀態時省略 `## 現況`；狀態只寫階段；TBD-1 結論在狀態欄；Timeline 只記建立與核准；沒有下游專案名稱。
- 重複與過度設計：只動文件、沒改安裝器，符合使用者選的方案；usage.md 只加指標；唯一重複是 N4 的出處說明。
- 限制：沒有實跑 agent 照 INSTALL.md 第 3 步執行；check-links 不驗錨點；CHANGELOG 外部網址未連線確認。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
