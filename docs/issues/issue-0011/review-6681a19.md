# 審查報告
- 範圍：完整交付範圍
- Reviewed BASE SHA：166c86d837c86700982b4cc357a848255413688b
- Reviewed HEAD SHA：6681a19726c3cb7ad3af0efb2e0b60b673208e84
- Reviewed patch-id：3e5fba736e9ef5508f28fc6cdf0f8e4732ea9735
- 獨立 reviewer：Claude Code 獨立 subagent（general-purpose，claude-opus-5-5），唯讀，工具呼叫上限 30 次（實際 11 次）
- Review artifact：docs/issues/issue-0011/review-6681a19.md
- 增量覆審：上一份報告 review-67e37e0.md，增量範圍 `67e37e0..6681a19`（706c457、c689f6d、68651d2、6681a19）

## 問題與風險

- MUST FIX M1：合併前的觀察做完後，終態的寫法前後矛盾。docs/AGENTS.md:147 新增「做完觀察、記錄證據的提交同時把本欄改成 `已完成`」沒有限定合併後，合併前（staging）的觀察也適用；依 review-evidence.md，implementation-plan.md 與 evidence 是凍結內容，證據寫進計畫時原 PASS 失效，同一個提交寫 `已完成` 違反 :149 的必須記錄「有效 PASS」。wf41-r2 的下一步正是「同一個提交把 S3 標成 ✅、附上輸出，並把狀態改成 `已完成`……接下來就是等你合併」，沒有發現 PASS 會失效（wf41-r1 自己發現並轉問使用者）。分支上可能出現 PASS 已失效的 `已完成`，合併後第 2 列直接結案。另外 skills/dev-cycle/SKILL.md:59 把寫 `等待外部驗收窗` 限縮成「要等合併後才能觀察的項目」，審查通過時還有合併前的待觀察項目時照字面要寫 `已完成`，與 SCN-002、:149 矛盾。建議：147 那句限定合併後；合併前觀察完成時，證據記在記帳區段就沿用 PASS 並同一提交寫 `已完成`，寫進計畫或 evidence 時先重新審查（可增量）再依第 5 項寫終態；第 5 項補上審查通過時還有合併前待觀察項目就寫等待；補推進模式的 WF-41 案例。
- SHOULD FIX S1 `需決策`：窗口是否要等合併沒有規定要寫在 README。docs/AGENTS.md:147 的必須記錄沒有這一項，WF-41 的 fixture 在窗口文字明寫了，實際 README 不一定會寫；把要等合併的窗口誤判成合併前的窗口（例如只寫「下一次發版」）時，每次都命中等待列、事件未發生就結束，到不了 PR 列，等於卡死，是 2.7 新出現的情境。建議必須記錄加上「窗口是否要等合併」，第 5 項寫等待時一併寫明。待決問題：沒寫明時預設當成哪一種？建議答案：當成要等合併（回報待合併），並在回報裡請使用者確認窗口。
- SHOULD FIX S2：skills/dev-cycle/references/pending-scan.md:18「目標分支還不包含的 `已完成`、`等待外部驗收窗` 不算終態」把兩種等待都排除，在 worktree 掃描時，窗口已到的合併前等待不會被列為窗口到期，與使用者「照舊支援合併前觀察窗」的決定不一致；`等待外部驗收窗` 本來就不在本檔的終態裡，語意不清。建議只對 `已完成` 與要等合併的等待這樣處理。
- SHOULD FIX S3：CHANGELOG.md:21 仍是舊說法（「合併前已知要等待」包含 staging 窗口、「最後一個記帳提交」、「合併後不補提交」沒有例外），與 docs/AGENTS.md:204 不一致。建議改成相同說法。
- NICE TO HAVE N1：目標分支快轉到 Reviewed HEAD、記帳提交（報告與 `已完成`）還沒進去時，pending-scan.md:14 的祖先判定讓 dev-cycle 判已合併並結案，但目標分支的 README 不是終態；懸置掃描之後會列為已合併未結案，不是靜默錯誤。建議祖先判定確認已合併時，一併確認寫入終態的提交也在目標分支上。
- NICE TO HAVE N2：祖先判定在懸置掃描標「推測」，但 dev-cycle 單一 issue 引用它後直接結案，回報沒有說明依據是推測；被審查 HEAD 本來就在主幹上（例如主幹上的決策審查）時祖先判定一定成立。
- NICE TO HAVE N3：docs/rule-verification-status.md:348 仍寫「合併後不補提交」，可補上合併後才需要的提交的例外。

## 已查核維度

- 上一輪發現的處理：M1 部分修正（等待列只在 2.7、窗口要等合併時加合併條件；WF-23 期望註明；WF-41 兩組各 2／2；觀察完成後的終態有新缺陷，見本輪 M1、S1）。S1 已修正（dev-cycle:59、AGENTS.md:149；147 太寬見本輪 M1；CHANGELOG 見 S3）。S2 部分修正（見本輪 S2）。S3 已修正（dev-cycle 引用單一定義、祖先判定可辨認快轉，快轉只靜態已揭露；殘餘見 N1、N2）。S4 已修正（Gate 豁免紀錄）。N1 大致修正（CHANGELOG:21 未改）。N2、N3 已修正。
- 狀態表逐列（增量重新查核）：未合併 `已完成`（2.7）落到審查／PR 列回報待合併，不假結案；未合併、窗口合併前就會到的等待：日期未到命中等待列回報後結束（必要工作照常，與 BASE 相同，未實跑），日期已到執行觀察（wf41 2／2，只測查詢），之後的終態見 M1；未合併、窗口要等合併的等待（2.7）落到 PR 列回報待合併（wf41b 2／2），依賴窗口類型判斷（S1）；已合併的 `已完成` 命中第 2 列，已合併的等待經第 1 列與等待列處理，觀察完成後依第 5 項寫 `已完成`；不經合併交付放行；2.6 以下的未合併等待與 BASE 相同，SCN-008 成立（僅靜態）。
- 完成條件與狀態值用詞：終態寫在哪個提交，AGENTS.md:149、dev-cycle:59、SCN-002 三處一致；步驟 3 與第 5 項一致；AGENTS.md:147 與 :149、第 5 項與 SCN-002 的落差見 M1。
- 雙語 rules：增量沒有改 rules/，沿用上一輪結論。
- verify-artifact 負向案例：verify-artifact.py 增量未變；新增 `test_quoted_approval_sha_replaced_invalid`（scripts/test-evidence.py:991）若程式把帶反引號的 SHA 誤當待提交會判有效而失敗，能分辨對錯；test-evidence 312 項 OK。
- 流程契約 2.7 相容性與祖先判定：2.6 以下多抓出快轉合併後未標結案的 issue，屬偵測改善；報告存在平台時仍取得 Reviewed HEAD；分支沒有提交時沒有報告、不會誤判；被審查 HEAD 在主幹上與快轉缺記帳提交見 N1、N2。dev-cycle 讀工作樹並以合併判定排除未合併終態、懸置掃描讀目標分支，對 `已完成` 結論一致，合併前等待的可見度見 S2。
- 重新查核：WF-23 期望與新規則一致；usage.md:59 只講 `已完成`、沒有衝突，README.md 沒有相關敘述；CHANGELOG 與 rule-verification-status 的未實跑揭露誠實（快轉、合併後寫 `已完成`、懸置掃描讀目標分支、WF-41 只測查詢），尚未列出合併前窗口日期未到與推進模式；WF-41 判準在 c689f6d 提交，四輪 kit HEAD 都是之後的 68651d2，先於實跑；證據支持 wf41、wf41b 各 2／2（wf41b 工作樹雜湊變化只來自被忽略的 `__pycache__`），但 fixture 的窗口文字明寫是否要等合併，泛化有限（S1）。五項檢查重跑都 OK（test-install 32 項、test-evidence 312 項）。
- 沿用上一份報告：SCN-001、003、005（已豁免）、006、007 的驗收判定；核准基線與 Gherkin 未變；雙語 rules；安全與架構面；基準組沒有跑的揭露。
- 限制：build_fixtures.py 的新增部分只看 diff；本輪 M1、S1、S2、N1 沒有以 agent 實跑驗證，M1 的依據是 wf41-r2 的輸出與 review-evidence 的凍結規則；沒有核對證據的 session 時間戳與隔離設定技能摘要；沒有重算 patch-id。

## 流程判定
RETURN TO execute-task
