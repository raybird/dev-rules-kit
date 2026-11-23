# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：166c86d837c86700982b4cc357a848255413688b
- Reviewed HEAD SHA：67e37e05f8bb9949e4585aa62dda4f71765a9765
- Reviewed patch-id：178fc227ca9cc0ddf24f62488f3b3cce2b02c0d5
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose，claude-opus-5-5），唯讀，工具呼叫上限 30 次（實際約 22 次）
- Review artifact：docs/issues/issue-0011/review-67e37e0.md

## 問題與風險

- MUST FIX M1 `需決策`：skills/dev-cycle/SKILL.md:34、:49 的等待列加上「已合併或交付不經合併」的條件，並寫明分支上未合併的 `等待外部驗收窗` 不命中等待列。狀態表不分版本，2.6 以下也受影響，違反 SCN-008。kit 原本支援合併前的等待窗口（WF-23 對照二，docs/workflow-results/2026-10-16.md，PASS：未合併、窗口已到，執行觀察、記錄證據、不結案）；改後這種 issue 不執行到期觀察，落到審查／PR 列並回報待合併，使用者可能在觀察完成前合併。與 docs/AGENTS.md:147「到達才執行待觀察項目」衝突，workflow-regression.md 的 WF-23 期望也沒有同步。建議：「未合併就不命中等待列」只限流程契約 2.7、合併前寫好且窗口依賴合併的終態；2.6 以下與不依賴合併的窗口照舊執行到期觀察。待決問題：2.7 是否仍支援合併前的觀察窗（例如 staging 驗證後才合併）？建議答案：支援，以「窗口是否依賴合併」區分。
- SHOULD FIX S1：skills/dev-cycle/SKILL.md:59、docs/AGENTS.md:149 的「合併後不補提交」是無條件的說法，但合併後的 `等待外部驗收窗` 做完觀察後要在主幹記證據，狀態表第 1 列（合併後才發現未執行驗證）也要在主幹改記等待。觀察完成後在哪裡寫 `已完成` 沒有定義，README 可能永遠停在等待、懸置掃描一直列出。建議寫明例外：記錄觀察結果的主幹提交順手寫 `已完成`；合併後才發現待觀察項目時同樣在主幹記等待。
- SHOULD FIX S2：skills/dev-cycle/references/pending-scan.md:23、:25、:30 沒有指定讀哪個 ref 的 README。2.7 起分支上就有 `已完成`，在功能分支或 worktree 掃描時，未合併的 `已完成` 會命中「README 終態、平台仍 open」（建議關閉平台 issue，等於提前結案）或「結案後仍有待觀察」。建議寫明讀目標分支的 README，或把目標分支尚未包含的 `已完成` 視為非終態。issue README 的涉及檔案列了 pending-scan.md，但這次沒有改。
- SHOULD FIX S3：結案只看合併判定，但單一 issue 查詢時合併判定的預設定義只在 pending-scan.md:14（平台 PR merged → Git merge commit），認不出快轉合併。dev-cycle:33 的 `已完成` 結案列已限縮為不經合併的依據，快轉合併、沒有平台 PR、project.md 未登記合併判定的專案，已合併的 `已完成` 會一直回報待合併（卡住，不是假結案）。WF-38 的 fixture 登記了 `--no-ff`，快轉沒有測到。建議 dev-cycle 指向單一定義，並納入「被審查 HEAD 是目標分支的祖先」；至少在 rule-verification-status 揭露快轉未測。
- SHOULD FIX S4：SCN-005 未達標（wf40b 1／6），使用者接受的決定只記在實作計畫、CHANGELOG 與 rule-verification-status，README 沒有 Gate 豁免紀錄或待確認事項；依 docs/AGENTS.md，未豁免的必要驗收照常列為缺漏，create-pr 與懸置掃描會判 SCN-005 未完成。建議在 README 的 Gate 豁免紀錄記使用者原話、範圍與殘餘影響。
- NICE TO HAVE N1：終態寫在哪個提交有三種說法：docs/AGENTS.md:149「交付合併前的最後一個記帳提交」、dev-cycle:59「保存 PASS 報告的提交，或記錄建議結論的提交」、SCN-002「保存報告的提交或之後的記帳提交」；WF-39 實際是報告之後另一個提交。建議統一成 SCN-002 的說法。
- NICE TO HAVE N2：issue README 的 `**狀態**` 仍是「待實作」，S1～S6 已完成。
- NICE TO HAVE N3：test-evidence 沒有直接測「帶反引號的 SHA 改成其他值」；程式邏輯涵蓋。

## 已查核維度

- 驗收與證據：SCN-001 通過（docs/AGENTS.md:143；WF-40 wf40 改 document-types 前 1／2、後 2／2）。SCN-002 通過（WF-39 2／2；有待觀察項目寫 `等待外部驗收窗` 未實跑，已揭露）。SCN-003 通過（WF-38 兩組各 2／2，判準先於實跑提交）。SCN-004 僅靜態，已揭露（readme-templates 已無負責人欄）。SCN-005 未達標、使用者已接受，揭露誠實，豁免紀錄缺漏見 S4。SCN-006 僅靜態，已揭露。SCN-007 通過（本地測試已重跑）。SCN-008 僅靜態且有反例（M1）。核准基線：`git diff 0379d3e 67e37e0 -- docs/issues/issue-0011/README.md` 只改不在範圍那一行與核准 commit 回填，Gherkin 未變。五項檢查重跑：check-kit、check-links、`bash -n`、test-install 32 項、test-evidence 308 項都 OK。
- 相關失敗面（狀態表逐列）：未合併的 `已完成` 不命中「PR 已 merged」兩列與不修復列，第 33 行限不經合併的依據、第 49 行明文排除，落到 create-pr／等待合併，不會假結案（WF-38 未合併組 2／2）；已合併命中第 1 或第 2 列直接結案（WF-38b 2／2）；`不修復` 未改；不經合併交付的 `已完成` 仍能由第 33 行結案；已合併的 `等待外部驗收窗` 依第 34 行處理正常。未合併的 `等待外部驗收窗` 回歸（M1）；快轉或未登記合併判定的專案卡在待合併（S3）。
- 完成條件（推進步驟 3、5）：合併前寫終態、修正後改回實際階段、2.6 以下照舊，與 docs/AGENTS.md:147、:149 大致一致；`**狀態**` 屬 verify-artifact.py 的 BOOKKEEPING_FIELDS，2.4 以上寫終態判有效（WF-39 2／2，agent 實際執行 verify-artifact）。缺口見 S1、N1。
- 雙語 rules：兩版都在第六節「外部狀態以實查為準」之後，逐句對應（只記一處、其他地方指向它、開頭只寫規則並附例句、改完逐段檢查），check-kit 章節數一致。
- verify-artifact 負向案例：`lstrip('`')` 只去開頭反引號，以反引號開頭但不是待提交的值（例如 `` `abc1234` ``）仍無效；新值仍須是 SHA 且為被審查提交或其祖先；三種寫法的回填後代、不存在 SHA 都判無效，SHA 改成其他值由既有案例涵蓋；2.3 與無契約子類別的覆寫正確。
- 流程契約 2.7 相容性：文件版本 2.15、契約 2.7、修訂紀錄齊全；技能最低需求不變，check-kit 相容檢查通過；2.6 以下 README 不需遷移。dev-cycle 狀態表不分版本影響 2.6 以下的等待窗口（M1）；pending-scan 需指定 ref（S2）。skill-hashes 依 build 腳本把未發布內容標成目前最新版，與既有慣例相同。
- 需求、架構、安全、品質：沒有安全或權限面；跨檔重複見 N1，沒有過度設計。
- 豁免、待確認與限制：基準組沒有跑，rule-verification-status 與 CHANGELOG 照實寫明。reviewer 只抽查 wf38-r1、wf39 兩輪的工具動作與 wf40b 第二次重跑兩輪的 diff，其餘輪次核對計畫摘要；build_fixtures.py 未逐行審查；M1、S2、S3 為靜態推論，未以 agent 實跑驗證。

## 流程判定
RETURN TO execute-task
