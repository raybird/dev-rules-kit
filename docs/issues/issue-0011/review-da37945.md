# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：166c86d837c86700982b4cc357a848255413688b
- Reviewed HEAD SHA：da379456e93e8bd4a67a2fbaff025b708bf4e530
- Reviewed patch-id：2bf75ee9cd6b62137d9aad4efa466a847864557c
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose，claude-opus-5-5），唯讀，工具呼叫上限 30 次（實際 17 次）
- Review artifact：docs/issues/issue-0011/review-da37945.md
- 增量覆審：上一份報告 review-6681a19.md，增量範圍 `6681a19..da37945`（2f38f53、03d474c、1a8a18a、da37945）

## 問題與風險

- MUST FIX：無。
- SHOULD FIX S1：四處仍寫「審查通過就寫 `已完成`」而沒有「沒有未豁免的待觀察項目時」的條件，因本增量的規則修訂而過時：docs/agents/readme-templates.md:210（下游產品，new-issue 建 README 時讀）、docs/usage.md:59、CHANGELOG.md:17 的摘要句、CHANGELOG.md:50「下游更新」。下游照這些說明做時，有待觀察項目的 issue 會在合併前寫成 `已完成`，合併後命中「PR 已 merged」直接結案，懸置掃描再列為結案後仍有待觀察。建議四處加上條件，有待觀察項目照等待窗口處理；改的是交付內容，改完需重新審查（可增量）。
- NICE TO HAVE N1：skills/dev-cycle/SKILL.md:59「依等待窗口處理」與 SCN-002「照原規則以 等待外部驗收窗 處理」沒講清楚要等合併的窗口在合併前怎麼寫；在合併前就寫成等待時，等待列回報事件未發生就結束，到不了 PR 列（與 BASE 相同，WF-42 兩輪都沒這樣做）。建議第 5 項寫明：窗口合併前就會到才記等待；要等合併的維持實際階段，合併後依狀態表第一列記等待。
- NICE TO HAVE N2：上一輪 N1（快轉到 Reviewed HEAD、記帳提交還沒進目標分支）評估為這輪不必處理；新規則下 `已完成` 寫在 Reviewed HEAD 之後的提交，只快轉到 Reviewed HEAD 時懸置掃描會列為已合併未結案，不是靜默錯誤。建議在 README 記結論（不修，或併入 #12 追蹤）。
- NICE TO HAVE N3：上一輪 N2（推測的合併判定直接結案）評估為不必處理；Reviewed HEAD 本來就在主幹上時內容已交付，rebase 造成的誤判方向偏安全。可選：依推測判定結案時在回報註明依據是推測。
- NICE TO HAVE N4：docs/issues/issue-0011/README.md:120 以單行寫「全部 Scenario 於 2026-11-20 核准；SCN-002 同日重新核准」，docs/agents/acceptance.md:50 規定有修訂時展開成表格；語意不會誤讀。
- NICE TO HAVE N5：README 沒有 `## 待確認事項`，review-67e37e0 M1 與 review-6681a19 S1 兩個 `需決策` 的結論只記在核准來源、Gate 豁免、Timeline 與計畫 S7；兩份都已不是現行報告，不會卡住，只是追溯不便。
- NICE TO HAVE N6：implementation-plan.md:10、:11 的設計段落與 rule-verification-status.md:339 的標題仍是修訂前的說法；S7 列已記修訂，可順手加註。
- NICE TO HAVE N7：CHANGELOG「未實跑」清單沒有點名合併前觀察做完之後的推進路徑（寫證據 → 重新審查 → 在 PASS 的提交寫 `已完成`）；wf41-r1 的選項 2（證據只記在記帳區段、計畫 S3 留 ⏳）若接著寫 `已完成` 會產生結案後仍有待觀察，但 agent 有先問使用者。

## 已查核維度

- 上一輪發現的處理：M1 已修正（docs/AGENTS.md:147 限定合併後；dev-cycle:59 有待觀察項目時合併前不寫終態；合併前觀察完成後證據寫進計畫會讓 PASS 失效、重審後依第 5 項寫 `已完成`，路徑一致；wf41 重跑兩輪都辨認出 PASS 會失效並先問使用者，推進模式未實跑見 N7）。S1 已不適用（等待列還原，窗口類型不再影響判定；剩下的寫法見本輪 N1）。S2 已修正（pending-scan.md:18 只排除 `已完成`）。S3 大致修正（CHANGELOG.md:21-23 已改，:17、:50 見本輪 S1）。N1、N2 未處理，評估見本輪 N2、N3。N3 已修正。
- 狀態表：`git diff 166c86d da37945 -- skills/dev-cycle/SKILL.md` 沒有等待列（:34），與 BASE 相同；表下段落只談未合併的 `已完成`。未合併的 `已完成` 落到審查／PR 列回報待合併，不假結案；已合併的 `已完成` 命中「PR 已 merged」，有待觀察項目時第一列先接住；未合併的等待與 BASE 相同（見 N1）；已合併的等待經第一列與等待列處理，觀察完成後依第 5 項寫 `已完成`；不經合併交付由 :33 放行；2.6 以下 `已完成` 只在合併後寫在主幹，等待列與 BASE 相同。不假結案、不卡死（BASE 既有情況除外），SCN-008 成立（僅靜態）。
- 完成條件與狀態值：推進步驟 3（:57）、5（:59），docs/AGENTS.md:147、:149，修訂紀錄 2.15（:204），CHANGELOG.md:21-23 說法一致，也與修訂後的 SCN-002 一致；grep「窗口要等合併、合併前已知、最後一個記帳提交」只剩 issue 目錄內有日期的歷史紀錄與 fixture 說明；另掃到 S1 的四處。
- 雙語 rules：增量沒有改 rules/，沿用上一輪結論。
- verify-artifact 與測試：增量沒有改 skills/review/ 與 scripts/ 的程式（只有 skill-hashes.txt）；五項檢查重跑都 OK（test-install 32 項、test-evidence 312 項）。
- 流程契約 2.7 相容性：pending-scan.md:18 只把目標分支還不包含的 `已完成` 視為非終態是正確的，`等待外部驗收窗` 本來就不是終態；同一句「讀目標分支上的 README」與「在功能分支或 worktree 掃描時」的關係不明確，讀成直接讀工作樹時合併前等待照樣列為窗口到期，符合使用者決定。祖先判定殘餘風險見 N2、N3。
- 判準與證據：expected.md「WF-41 重跑與 WF-42」在 03d474c（15:35:15）提交，四輪 kit HEAD 都是 1a8a18a（15:35:28），四個 session 第一筆時間戳 15:35:35～36（台北），證據在 da37945（15:38:45）提交，判準先於實跑。wf41 重跑兩輪都回報窗口已到、下一步執行 S3，不回報待合併，HEAD 與工作樹雜湊未變，支持 2／2。WF-42 兩輪狀態都維持「審查通過」，HEAD 停在 7d31c0c、沒合併、S3 未標完成，工作樹雜湊變化推測來自被忽略的 `__pycache__`，git status 乾淨，支持 2／2。
- 規格修訂的查核：`git diff 0379d3e 03d474c -- docs/issues/issue-0011/README.md` 的 Gherkin 只改 SCN-002，其他是非規格段落；核准來源有使用者的選項原話，舊基線 0379d3e 記在 Timeline，核准 commit 在 1a8a18a 回填為 03d474c。
- 揭露：CHANGELOG 與 rule-verification-status 寫了只測查詢、合併後才需要的提交未實跑、wf41b 已不適用、SCN-005 部分有效；漏列見 N7。
- 重新查核的項目與理由：等待列還原、第 5 項與 docs/AGENTS.md 改了說法，會影響沒改動的檔案，所以重新查核 dev-cycle 狀態表全表、整個 HEAD 的殘留說法（readme-templates、usage.md、README.md、CHANGELOG，因此找到 S1）、pending-scan 的合併判定與偵測規則、SCN-002 的修訂、patch-id（已重算，相符）與五項檢查。
- 沿用上一份報告：SCN-001、003、005（已豁免）、006、007 的驗收判定；雙語 rules；verify-artifact 負向案例（test_quoted_approval_sha_replaced_invalid）；安全與架構面；第一輪 WF-41 的證據判讀；基準組沒有跑的揭露。
- 限制：build_fixtures.py 的 wf42 部分只看 diff、沒有重建 fixture；證據只看最終輸出與前後狀態，沒有逐筆看 session 內容；隔離設定技能摘要 fe30e42dcffa63e4 沒有和 1a8a18a 比對；S1、N1 沒有以 agent 實跑驗證。

## 流程判定
PASS

PASS 只適用於上列 Reviewed HEAD SHA。之後在這個分支提交 issue README 記帳區段與本報告以外的檔案（例如交接文件），PASS 會失效、需要重新審查（流程契約 2.3 以下只有單獨新增本報告的提交可沿用）；提交前先告知使用者，由使用者決定做法。
